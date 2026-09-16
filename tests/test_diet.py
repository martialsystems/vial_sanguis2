# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import numpy as np

from vial_sanguis2.config import RunConfig
from vial_sanguis2.diet import fruit_available
from vial_sanguis2.fitness import energy_channels
from vial_sanguis2.genome import I_FLUID, I_FRUIT, I_RASP, QTL_AUTO


def test_qtl_order() -> None:
    assert QTL_AUTO[0] == "fruit_use"
    assert QTL_AUTO[2] == "rasp"
    assert QTL_AUTO[6] == "digest"
    assert QTL_AUTO[7] == "heme_safe"
    assert "fa" not in QTL_AUTO


def test_fruit_and_tears() -> None:
    cfg = RunConfig()
    assert fruit_available(4, cfg) == 1.0
    assert fruit_available(5, cfg) == 0.0
    z = np.zeros((1, 11))
    z[0, I_FRUIT] = 1.2
    z[0, I_FLUID] = 1.0
    z[0, I_RASP] = 0.5
    e = energy_channels(z, 1.0, 1.0)
    assert float(e.fruit[0]) == 1.2
    assert float(e.tears[0]) == 0.35
    assert float(e.sweat[0]) > 0.0


def test_frozen_diet_knobs() -> None:
    cfg = RunConfig()
    assert cfg.t_starve == 5
    assert cfg.k_tears == 40.0
    assert cfg.bite_weight == 1.0
    assert cfg.c_pierce == 0.05
    assert cfg.c_digest == 0.40
    assert cfg.c_heme == 0.40
    assert cfg.c_heme_in == 0.30
    assert cfg.beta_heme == 2.0
    assert cfg.survive_thresh_host == 0.075
    assert cfg.n_floor == 8
    assert cfg.n_ceiling == 1200
    assert cfg.z_max == 3.0
    assert cfg.k_a == 11
