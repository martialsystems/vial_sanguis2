# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


def test_seed3_persist_if_present() -> None:
    path = REPO / "logs" / "knn_delayed_10000_s3.json"
    if not path.is_file():
        pytest.skip("seed-3 persistence JSON not generated")
    run = json.loads(path.read_text(encoding="utf-8"))
    cfg = run["config"]
    assert cfg["seed"] == 3
    assert cfg["generations"] == 10000
    assert cfg["z_max"] == 3.0
    assert cfg["kinship_cap"] is True
    assert cfg["kinship_cap_on"] == "recover"
    assert cfg["phi_max"] == 0.25
    assert cfg["min_accepted_pairs"] == 8
    assert cfg["bite_weight"] == 1.0
    assert cfg["fruit_forever"] is False
    assert cfg["t_starve"] == 5
    assert "host_shift_at" not in cfg
    assert "exudate_after_hold" not in cfg
    assert run["extinct"] is False
    assert run["t_held_biter"] == 754
    assert abs(float(run["F_1500"]) - 0.228) < 0.001
    assert abs(float(run["F_2500"]) - 0.236) < 0.001
    assert abs(float(run["F_10000"]) - 0.228) < 0.001
    assert int(run["n_cap_fallback_gens"]) == 1
    last = run["generations"][-1]
    assert int(last["t"]) == 10000
    assert float(last["p_biter"]) >= 0.05
    assert abs(float(last["p_biter"]) - 0.066) < 0.002
    n_fb = int(run["n_cap_fallback_gens"])
    n_post = max(1, int(last["t"]) - int(run["t_kinship_on"] or 0))
    assert n_fb / n_post < 0.5, "fallback took over; this is not a cap arm"
    sweat = float(last["mean_energy_sweat"])
    wound = float(last["mean_energy_wound"])
    bite = float(last["mean_energy_bite"])
    rasp = float(last["qtl_mean"]["rasp"])
    pierce = float(last["qtl_mean"]["pierce"])
    saliva = float(last["qtl_mean"]["saliva"])
    assert abs(sweat - 4.591) < 0.01
    assert abs(wound - 3.410) < 0.01
    assert bite < 0.05
    assert bite < sweat and bite < wound
    assert saliva < 0.0
    assert rasp > 2.9
    assert rasp <= 3.0 + 1e-9
    assert pierce < 0.0
    g2500 = next(g for g in run["generations"] if int(g["t"]) == 2500)
    assert float(g2500["qtl_mean"]["pierce"]) > 0.4
