# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from vial_sanguis2.config import RunConfig
from vial_sanguis2.population import run_generations, write_run

BANNER = "Closed vial. Diet ladder. Delayed kinship cap with pair fallback. z_max=3."
REPO = Path(__file__).resolve().parents[2]


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="vial-sanguis2", description=BANNER)
    sub = p.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("run")
    run.add_argument("--arm", default="vampire", choices=["vampire", "random", "knn"])
    run.add_argument("--mode", default="knn", choices=["knn", "random"])
    run.add_argument("--k", type=int, default=3)
    run.add_argument("--kinship-cap", choices=["on", "off"], default="on")
    run.add_argument("--phi-max", type=float, default=0.25)
    run.add_argument("--cap-on-at", choices=["immediate", "recover"], default="recover")
    run.add_argument("--min-accepted-pairs", type=int, default=8)
    run.add_argument("--generations", type=int, default=2500)
    run.add_argument("--n", type=int, default=1000)
    run.add_argument("--seed", type=int, default=1)
    run.add_argument("--starve-at", type=int, default=5)
    run.add_argument("--out", type=Path, default=REPO / "logs" / "run.json")
    run.add_argument("--cap", choices=["on", "off"], default="off")
    run.add_argument("--fruit-forever", action="store_true")
    run.add_argument("--n-floor", type=int, default=8)
    return p


def _mode(arm: str, mode: str) -> str:
    if arm == "knn":
        return "assortative_knn"
    if arm == "random" or mode == "random":
        return "random"
    return "assortative_knn"


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.cmd != "run":
        return 2
    mate = _mode(args.arm, args.mode)
    cfg = RunConfig(
        n=args.n,
        generations=args.generations,
        seed=args.seed,
        t_starve=args.starve_at,
        fruit_forever=bool(args.fruit_forever),
        mating_mode=mate,
        k=args.k,
        kinship_cap=False if mate == "random" else args.kinship_cap == "on",
        kinship_cap_on=str(args.cap_on_at),
        phi_max=float(args.phi_max),
        min_accepted_pairs=int(args.min_accepted_pairs),
        arm=args.arm,
        cap=args.cap,
        n_floor=args.n_floor,
        fail_n_min=args.n_floor,
        n_ceiling=args.n if args.cap == "on" else 1200,
    )
    out = Path(args.out)
    result = run_generations(cfg, jsonl_path=out.with_suffix(".jsonl"))
    write_run(result, out)
    last = result["generations"][-1]
    print(
        f"t={last['t']} n={last['n']} F={last['F']:.4f} p_biter={last['p_biter']:.3f} "
        f"min_n={result['min_n']} t_held={result['t_held_biter']} "
        f"F1500={result.get('F_1500')} F2500={result.get('F_2500')} "
        f"F10000={result.get('F_10000')} "
        f"fallback_gens={result.get('n_cap_fallback_gens')} extinct={result['extinct']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
