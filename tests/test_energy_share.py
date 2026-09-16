# Copyright (c) 2026 Martial Systems LLC
"""Host-calorie shares from locked seed-3 JSON. No new run."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


def host_calorie_shares(row: dict, bite_weight: float = 1.0) -> dict[str, float]:
    tears = float(row["mean_energy_tears"])
    sweat = float(row["mean_energy_sweat"])
    wound = float(row["mean_energy_wound"])
    bite = float(row["mean_energy_bite"])
    usable = float(row["mean_usable_blood"])
    host = tears + sweat + usable
    blood = wound + bite_weight * bite
    wound_cal = usable * (wound / blood) if blood > 0 else 0.0
    bite_cal = usable * (bite_weight * bite / blood) if blood > 0 else 0.0
    return {
        "tears_pct": 100.0 * tears / host,
        "sweat_pct": 100.0 * sweat / host,
        "wound_pct": 100.0 * wound_cal / host,
        "bite_pct": 100.0 * bite_cal / host,
        "sweat_wound_pct": 100.0 * (sweat + wound_cal) / host,
        "p_biter": float(row["p_biter"]),
        "F": float(row["F"]),
    }


def _by_t(name: str) -> dict[int, dict]:
    path = REPO / "logs" / name
    if not path.is_file():
        pytest.skip(f"{name} not generated")
    run = json.loads(path.read_text(encoding="utf-8"))
    return {int(r["t"]): r for r in run["generations"]}


def test_origin_and_persist_agree_through_2500() -> None:
    origin = _by_t("knn_delayed_2500_s3.json")
    persist = _by_t("knn_delayed_10000_s3.json")
    for t in (754, 1500, 2500):
        a = host_calorie_shares(origin[t])
        b = host_calorie_shares(persist[t])
        assert abs(a["bite_pct"] - b["bite_pct"]) < 1e-12
        assert abs(a["sweat_wound_pct"] - b["sweat_wound_pct"]) < 1e-12
        assert abs(a["p_biter"] - b["p_biter"]) < 1e-12


def test_locked_share_rows() -> None:
    persist = _by_t("knn_delayed_10000_s3.json")
    rows = {
        754: (1.06, 97.62, 0.058),
        2500: (2.31, 96.74, 0.936),
        4644: (5.74, 93.34, 1.000),
        10000: (0.15, 98.88, 0.066),
    }
    for t, (bite, sw, p_b) in rows.items():
        s = host_calorie_shares(persist[t])
        assert abs(s["bite_pct"] - bite) < 0.01, t
        assert abs(s["sweat_wound_pct"] - sw) < 0.01, t
        assert abs(s["p_biter"] - p_b) < 0.002, t


def test_after_hold_bite_is_a_side_channel() -> None:
    persist = _by_t("knn_delayed_10000_s3.json")
    after = [host_calorie_shares(r) for r in persist.values() if int(r["t"]) >= 754]
    bite = [s["bite_pct"] for s in after]
    sw = [s["sweat_wound_pct"] for s in after]
    assert max(bite) < 6.0
    assert min(sw) > 93.0
    assert all(b < 20.0 for b in bite)
    peak = max(after, key=lambda s: s["bite_pct"])
    assert abs(peak["bite_pct"] - 5.74) < 0.01
    assert persist[4644]["p_biter"] == 1.0


def test_readme_has_share_table() -> None:
    text = (REPO / "README.md").read_text(encoding="utf-8")
    for needle in (
        "93.34",
        "5.74",
        "2.31",
        "0.15",
        "96.74",
        "98.88",
        "Bite is not a meal",
        "No ramp",
        "This tree is finished",
        "usable_blood",
    ):
        assert needle in text, needle
    agents = (REPO / "AGENTS.md").read_text(encoding="utf-8")
    long_arm = (REPO / "LONG_ARM.md").read_text(encoding="utf-8")
    assert "Bite is not a meal" in agents
    assert "This tree is finished" in agents
    assert "Bite is not a meal" in long_arm
    assert "This tree is finished" in long_arm
