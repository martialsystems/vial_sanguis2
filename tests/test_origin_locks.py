# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


def _load(name: str) -> dict | None:
    path = REPO / "logs" / name
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _knn(seed: int) -> dict | None:
    return _load(f"knn_delayed_2500_s{seed}.json")


def test_knn_origin_order_if_present() -> None:
    found = [_knn(s) for s in (1, 2, 3)]
    if any(r is None for r in found):
        pytest.skip("origin knn JSON not generated")
    living = [r for r in found if r is not None and not r["extinct"]]
    for run in found:
        assert run is not None
        assert run["config"]["z_max"] == 3.0
        assert run["config"]["kinship_cap_on"] == "recover"
        assert run["config"]["min_accepted_pairs"] == 8
        assert run["config"]["bite_weight"] == 1.0
        assert run["min_n"] is None or run["min_n"] <= 80 or run["extinct"]
        if run["extinct"]:
            continue
        assert run["t_first_biter"] is not None
        rec = next(g for g in run["generations"] if g["t"] == run["t_first_biter"])
        assert rec["qtl_mean"]["rasp"] > rec["qtl_mean"]["pierce"]
        if run.get("t_wound_load") is not None and run.get("t_heme_safe_rise") is not None:
            assert int(run["t_wound_load"]) <= int(run["t_heme_safe_rise"])
    s1, s2, s3 = found
    assert s1["t_held_biter"] is None
    assert s1["n_cap_fallback_gens"] == 2490
    assert abs(float(s1["F_1500"]) - 0.887) < 0.001
    assert s1["t_first_biter"] == 128
    assert s2["extinct"] is True
    assert s2["final_t"] == 11
    assert s3["t_first_biter"] == 109
    assert s3["t_held_biter"] == 754
    assert abs(float(s3["F_1500"]) - 0.228) < 0.001
    living_held = [r for r in living if r.get("t_held_biter") is not None]
    assert len(living_held) == 1
    last3 = s3["generations"][-1]
    assert float(last3["qtl_mean"]["saliva"]) < 0.0
    assert float(last3["mean_energy_wound"]) + float(last3["mean_energy_sweat"]) > float(
        last3["mean_energy_bite"]
    )


def test_random_origin_if_present() -> None:
    for seed in (1, 2, 3):
        run = _load(f"random_2500_s{seed}.json")
        if run is None:
            pytest.skip("origin random JSON not generated")
        assert run["min_n"] is None or run["min_n"] <= 80 or run["extinct"]
        if not run["extinct"]:
            last = run["generations"][-1]
            if float(last["p_biter"]) < 0.05:
                assert run.get("t_held_biter") is None


def test_fruit_forever_if_present() -> None:
    run = _load("fruit_forever_400_s1.json")
    if run is None:
        pytest.skip("fruit-forever JSON not generated")
    gens = [g for g in run["generations"] if g["t"] <= 400]
    assert max(g["p_biter"] for g in gens) <= 0.05
    first, last = gens[0], gens[-1]
    assert last["p_biter"] == 0.0
    assert last["qtl_mean"]["digest"] <= first["qtl_mean"]["digest"] + 0.12
    assert last["qtl_mean"]["heme_safe"] <= first["qtl_mean"]["heme_safe"] + 0.05
