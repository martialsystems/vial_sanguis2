# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import numpy as np

from vial_sanguis2.config import RunConfig
from vial_sanguis2.fitness import phenotype
from vial_sanguis2.genome import init_population
from vial_sanguis2.mating import freeze_sigma0, mating_traits, pair
from vial_sanguis2.population import run_generations


def test_cap_fallback_pairs_instead_of_inventing_adults() -> None:
    cfg = RunConfig(
        n=24,
        seed=1,
        mating_mode="assortative_knn",
        kinship_cap=True,
        phi_max=-0.01,
        min_accepted_pairs=8,
    )
    rng = np.random.default_rng(1)
    pop = init_population(cfg, rng)
    n0 = pop.n
    ph = phenotype(pop, cfg)
    sigma0 = freeze_sigma0(mating_traits(ph, pop.t, cfg), cfg)
    pairing = pair(pop, ph, cfg, rng, sigma0, cap_armed=True)
    assert pairing.n_cap_fallback == 1
    assert pairing.n_accepted > 0
    assert pairing.n_accepted <= n0 // 2 + 2


def test_fallback_logged_on_run_not_restock() -> None:
    cfg = RunConfig(
        n=24,
        generations=4,
        seed=1,
        t_starve=1,
        mating_mode="assortative_knn",
        kinship_cap=True,
        kinship_cap_on="immediate",
        phi_max=-0.01,
        min_accepted_pairs=8,
        fail_n_min=1,
        fail_viability=0.0,
        n_ceiling=4000,
    )
    result = run_generations(cfg)
    assert result["n_cap_fallback_gens"] >= 1
    assert any(int(g.get("n_cap_fallback", 0)) == 1 for g in result["generations"])
    for g in result["generations"]:
        if g["t"] > 0:
            assert g["n"] <= g["n_viable"]
            assert g["n_viable"] <= g["n_eggs"]


def test_census_not_padded() -> None:
    cfg = RunConfig(
        n=40,
        generations=6,
        seed=1,
        t_starve=2,
        n_ceiling=4000,
        fail_n_min=1,
        fail_viability=0.0,
        kinship_cap=False,
    )
    result = run_generations(cfg)
    for g in result["generations"]:
        if g["t"] > 0:
            assert g["n"] <= g["n_viable"]
            assert g["n_viable"] <= g["n_eggs"]
