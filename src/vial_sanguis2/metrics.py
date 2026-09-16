# Copyright (c) 2026 Martial Systems LLC
"""Census meters. Heme clock is tax-gated. First-biter is a flicker."""

from __future__ import annotations

from typing import Any

import numpy as np

from vial_sanguis2.config import RunConfig
from vial_sanguis2.fitness import Phenotype
from vial_sanguis2.genome import FEMALE, MALE, QTL_AUTO, Pop
from vial_sanguis2.mating import Pairing


def _py(x: Any) -> Any:
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, np.bool_):
        return bool(x)
    return x


def heterozygosity_qtl(pop: Pop) -> float:
    if pop.n == 0:
        return 0.0
    return float((pop.founder_qtl_auto[:, :, 0] != pop.founder_qtl_auto[:, :, 1]).mean())


def mean_pairwise_phi(founder: np.ndarray) -> float:
    n, k, _ = founder.shape
    if n < 2 or k == 0:
        return 0.0
    acc = np.zeros((n, n), dtype=np.float64)
    for loc in range(k):
        mat, pat = founder[:, loc, 0], founder[:, loc, 1]
        acc += (mat[:, None] == mat[None, :]).astype(np.float64)
        acc += (mat[:, None] == pat[None, :]).astype(np.float64)
        acc += (pat[:, None] == mat[None, :]).astype(np.float64)
        acc += (pat[:, None] == pat[None, :]).astype(np.float64)
    acc *= 0.25 / k
    return float(acc[np.triu_indices(n, k=1)].mean())


def record_generation(
    pop: Pop,
    ph: Phenotype,
    pairing: Pairing | None,
    cfg: RunConfig,
    h0_qtl: float,
    n_eggs: int,
    n_viable: int,
) -> dict:
    n_f = int(np.sum(pop.sex == FEMALE)) if pop.n else 0
    n_m = int(np.sum(pop.sex == MALE)) if pop.n else 0
    h_qtl = heterozygosity_qtl(pop)
    f_t = 0.0 if h0_qtl <= 0 else 1.0 - (h_qtl / h0_qtl)
    qtl_mean: dict[str, float] = {}
    qtl_p95: dict[str, float] = {}
    n_names = min(len(QTL_AUTO), ph.z.shape[1] if ph.z.ndim == 2 else 0)
    for i, name in enumerate(QTL_AUTO[:n_names]):
        col = ph.z[:, i] if pop.n else np.empty(0)
        qtl_mean[name] = float(col.mean()) if pop.n else 0.0
        qtl_p95[name] = float(np.quantile(col, 0.95)) if pop.n else 0.0
    rec = {
        "t": int(pop.t),
        "n": int(pop.n),
        "n_female": n_f,
        "n_male": n_m,
        "F": float(f_t),
        "mean_pairwise_phi": mean_pairwise_phi(pop.founder_qtl_auto) if pop.n else 0.0,
        "mean_w": float(ph.w.mean()) if pop.n else 0.0,
        "mean_survive": float(ph.survive.mean()) if pop.n else 0.0,
        "mean_fertility": float(ph.fertility.mean()) if pop.n else 0.0,
        "qtl_mean": qtl_mean,
        "qtl_p95": qtl_p95,
        "mean_energy_fruit": float(ph.energy_fruit.mean()) if pop.n else 0.0,
        "mean_energy_tears": float(ph.energy_tears.mean()) if pop.n else 0.0,
        "mean_energy_sweat": float(ph.energy_sweat.mean()) if pop.n else 0.0,
        "mean_energy_wound": float(ph.energy_wound.mean()) if pop.n else 0.0,
        "mean_energy_bite": float(ph.energy_bite.mean()) if pop.n else 0.0,
        "mean_usable_blood": float(ph.usable_blood.mean()) if pop.n else 0.0,
        "mean_heme_load": float(ph.heme_load.mean()) if pop.n else 0.0,
        "p_exudate": float(np.mean(ph.exudate > cfg.exudate_threshold)) if pop.n else 0.0,
        "p_biter": float(np.mean(ph.biter)) if pop.n else 0.0,
        "max_bite": float(ph.energy_bite.max()) if pop.n else 0.0,
        "max_rasp": float(ph.z[:, 2].max()) if pop.n else 0.0,
        "accepted_pairs": 0 if pairing is None else int(pairing.n_accepted),
        "kinship_rejects": 0 if pairing is None else int(pairing.n_kinship_reject),
        "n_cap_fallback": 0 if pairing is None else int(pairing.n_cap_fallback),
        "n_eggs": int(n_eggs),
        "n_viable": int(n_viable),
        "extinct": bool(pop.n == 0 or n_f == 0 or n_m == 0),
    }
    return {k: _py(v) if not isinstance(v, dict) else v for k, v in rec.items()}


def first_times(records: list[dict], cfg: RunConfig) -> dict:
    t_crash = t_min_n = t_recover = None
    t_first_biter = t_held_biter = t_majority_biter = None
    t_wound_load = t_heme_safe_rise = t_heme_safe_rise_mean = None
    min_n = None
    crashed = False
    hold_run = 0
    hold_start: int | None = None
    w_hold = max(1, int(cfg.held_biter_w))
    for rec in records:
        t, n = int(rec["t"]), int(rec["n"])
        p_b = float(rec.get("p_biter", 0.0))
        if t >= cfg.t_starve and not cfg.fruit_forever:
            if t_crash is None and n < 80:
                t_crash, crashed = t, True
            if min_n is None or n < min_n:
                min_n, t_min_n = n, t
            if crashed and t_recover is None and n >= 400:
                t_recover = t
        if t_first_biter is None and p_b > 0.0:
            t_first_biter = t
        if t_majority_biter is None and p_b >= 0.5:
            t_majority_biter = t
        if p_b >= cfg.held_biter_p:
            if hold_run == 0:
                hold_start = t
            hold_run += 1
            if t_held_biter is None and hold_run >= w_hold:
                t_held_biter = hold_start
        else:
            hold_run = 0
            hold_start = None
        wound = float(rec.get("mean_energy_wound", 0.0))
        bite = float(rec.get("mean_energy_bite", 0.0))
        heme = float(rec.get("qtl_mean", {}).get("heme_safe", 0.0))
        if t_wound_load is None and wound > cfg.eps_heme:
            t_wound_load = t
        if t_heme_safe_rise_mean is None and heme >= cfg.heme_rise:
            t_heme_safe_rise_mean = t
        if t_heme_safe_rise is None and (wound + bite) > cfg.eps_heme and heme >= cfg.heme_rise:
            t_heme_safe_rise = t
    f1500 = next((float(r["F"]) for r in records if int(r["t"]) == 1500), None)
    f2500 = next((float(r["F"]) for r in records if int(r["t"]) == 2500), None)
    return {
        "t_crash": t_crash,
        "t_min_n": t_min_n,
        "min_n": min_n,
        "t_recover": t_recover,
        "t_first_biter": t_first_biter,
        "t_held_biter": t_held_biter,
        "t_majority_biter": t_majority_biter,
        "t_wound_load": t_wound_load,
        "t_heme_safe_rise": t_heme_safe_rise,
        "t_heme_safe_rise_mean": t_heme_safe_rise_mean,
        "F_1500": f1500,
        "F_2500": f2500,
    }
