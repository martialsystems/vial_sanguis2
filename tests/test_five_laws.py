# Copyright (c) 2026 Martial Systems LLC
"""Five laws as pytest assertions. No GraphForge pin."""

from __future__ import annotations

import inspect
from pathlib import Path

import numpy as np

from vial_sanguis2.config import RunConfig
from vial_sanguis2.diet import HOST_CHANNELS
from vial_sanguis2.fitness import energy_channels, phenotype
from vial_sanguis2.genome import (
    BLOOD_QTLS,
    I_DIGEST,
    I_FLUID,
    I_HEME,
    I_RASP,
    I_SALIVA,
    QTL_AUTO,
    init_population,
)
from vial_sanguis2.mating import mating_traits
from vial_sanguis2.population import cap_uniform, run_generations
from vial_sanguis2 import mating, population

REPO = Path(__file__).resolve().parents[1]


def test_five_laws_defaults() -> None:
    cfg = RunConfig()
    assert cfg.n_load >= 64 and cfg.s_let == 1.0
    assert cfg.z_max == 3.0
    assert cfg.kinship_cap is True
    assert cfg.kinship_cap_on == "recover"
    assert cfg.kinship_recover_n == 50
    assert cfg.phi_max == 0.25
    assert cfg.min_accepted_pairs == 8
    assert cfg.bite_weight == 1.0
    assert not hasattr(cfg, "host_shift_at")
    assert not hasattr(cfg, "exudate_after_hold")
    assert QTL_AUTO == (
        "fruit_use",
        "fluid_detect",
        "rasp",
        "pierce",
        "saliva",
        "seek",
        "digest",
        "heme_safe",
        "locomotion",
        "fertility",
        "stab",
    )
    assert "fa" not in QTL_AUTO
    assert HOST_CHANNELS == ("tears", "sweat", "wound", "bite")
    assert I_DIGEST != I_SALIVA
    names = " ".join(QTL_AUTO)
    assert "mandible" not in names and "stylet" not in names


def test_law1_closed_vial_never_invents_adults() -> None:
    cfg = RunConfig(
        n=40,
        generations=8,
        seed=7,
        t_starve=2,
        n_ceiling=4000,
        cap="off",
        fail_n_min=1,
        fail_viability=0.0,
        kinship_cap=False,
    )
    result = run_generations(cfg)
    for g in result["generations"]:
        if g["t"] > 0:
            assert g["n"] <= g["n_viable"]
            assert g["n_viable"] <= g["n_eggs"]
    rng = np.random.default_rng(0)
    pop = init_population(RunConfig(n=12, seed=0, generations=1), rng)
    capped = cap_uniform(pop, 100, rng)
    assert capped.n == pop.n
    src = inspect.getsource(population)
    assert "immigrat" not in src.lower()
    assert "not restock" in src.lower() or "pairing, not restock" in src


def test_law2_load_required_and_hidden_from_mating() -> None:
    cfg = RunConfig()
    rng = np.random.default_rng(1)
    pop = init_population(cfg, rng)
    assert pop.load.shape == (cfg.n, cfg.n_load, 2)
    ph = phenotype(pop, cfg)
    traits = mating_traits(ph, pop.t, cfg)
    assert traits.shape[1] == 2
    mate = inspect.getsource(mating)
    assert "pop.load" not in mate
    assert "load" not in inspect.getsource(mating_traits).lower()


def test_law3_census_may_fall() -> None:
    cfg = RunConfig(
        n=80,
        generations=10,
        seed=1,
        t_starve=3,
        n_ceiling=80,
        cap="off",
        fail_n_min=1,
        fail_viability=0.0,
        kinship_cap=False,
    )
    result = run_generations(cfg)
    after = [g["n"] for g in result["generations"] if g["t"] >= cfg.t_starve]
    before = [g["n"] for g in result["generations"] if g["t"] < cfg.t_starve]
    assert after
    assert min(after) < min(before)


def test_law4_diet_ladder_digest_not_a_blood_switch() -> None:
    z = np.zeros((1, 11), dtype=np.float64)
    z[0, I_FLUID] = 1.0
    z[0, I_RASP] = 1.0
    z[0, I_SALIVA] = 0.4
    e0 = energy_channels(z, 0.0, 1.0)
    z_d = z.copy()
    z_d[0, I_DIGEST] = 2.0
    e_d = energy_channels(z_d, 0.0, 1.0)
    z_s = z.copy()
    z_s[0, I_SALIVA] = 2.0
    e_s = energy_channels(z_s, 0.0, 1.0)
    assert float(e_d.wound[0]) == float(e0.wound[0])
    assert float(e_d.usable_blood[0]) > float(e0.usable_blood[0])
    assert float(e_s.wound[0]) != float(e0.wound[0])
    assert float(e_d.heme_load[0]) == float(e0.heme_load[0])
    assert I_DIGEST in BLOOD_QTLS
    assert I_HEME in BLOOD_QTLS
    assert float(e0.tears[0]) > 0.0
    assert float(e0.sweat[0]) > 0.0
    assert float(e0.wound[0]) > 0.0


def test_law5_prestomal_path_not_stylet() -> None:
    assert QTL_AUTO[2] == "rasp" and QTL_AUTO[3] == "pierce"
    src_root = REPO / "src" / "vial_sanguis2"
    blob = "\n".join(p.read_text(encoding="utf-8") for p in src_root.glob("*.py"))
    assert "stylet" not in blob.lower()
    assert "mandible" not in blob.lower()
    assert "flywire" not in blob.lower()
    assert "malecns" not in blob.lower()


def test_bridge_does_not_step_to_zero() -> None:
    src = (REPO / "src" / "vial_sanguis2" / "fitness.py").read_text(encoding="utf-8")
    assert "exudate_cap" not in src
    assert "wound_scab" not in src
    assert "skin_tough" not in inspect.getsource(energy_channels)
    z = np.zeros((1, 11))
    z[0, I_FLUID] = 1.0
    z[0, I_RASP] = 1.0
    e = energy_channels(z, 0.0, 1.0)
    assert float(e.tears[0]) > 0.0
    assert float(e.sweat[0]) > 0.0
    assert float(e.wound[0]) > 0.0


def test_no_graphforge() -> None:
    assert not (REPO / "engine_pin.json").exists()
    assert not (REPO / "product_laws.py").exists()
    assert not (REPO / "vialforge").exists()
    agents = (REPO / "AGENTS.md").read_text(encoding="utf-8")
    assert "Do not pin GraphForge" in agents
    assert "LONG_ARM.md" in agents
    long_arm = (REPO / "LONG_ARM.md").read_text(encoding="utf-8")
    assert "Curiosity is not a transition." in long_arm
    assert "Unfreezing a diet knob is a halt." in long_arm
    assert "origin" in long_arm
    assert "Do not raise bite_weight" in long_arm
    assert "Vampire checklist failed as a 3-seed claim." in long_arm
    assert "fallback-dominated" in long_arm
    assert "state: halt" in long_arm
    assert "next legal node: none" in long_arm
    assert "F@10k=0.228" in long_arm
    assert "Do not patch vial_sanguis" in long_arm
