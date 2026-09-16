# vial_sanguis2

Under an explicit diet ladder and an allowed population crash, does a Drosophila-like sponging labellum evolve prestomal-tooth rasping and a costly shallow bite, and can that kit hold with F off 1 if kinship cap waits until after recovery and falls back to random pairing instead of vetoing every pair?

This is not an origin of hematophagy. Successor to [vial_sanguis](https://github.com/martialsystems/vial_sanguis). Cliff result there stands. This engine starts from that measurement: delayed cap, pair fallback, `z_max=3.0`. Origin arm has no host shift and does not step exudate to zero.

## Origin

n=1,000, t_starve=5, 2,500 generations, seeds 1 to 3. k-NN delayed-cap (`n>=50` after starve, then `phi_max=0.25`). If the cap would accept fewer than 8 pairs, that generation uses random pairing (`n_cap_fallback`). Random mating control. Fruit-forever t=400. No host-shift.

Crash is real on every starve arm. Fruit-forever last p_biter=0 (max 0.0008). Vampire at t=2,500 held on 1 of 3 k-NN seeds. Do not average that seed with the extinct one or with the fallback census.

| seed | mate | min n | t_recover | flicker | t_held_biter | F@1500 | F@2500 | final p_biter | fallback gens |
|-----:|------|------:|----------:|--------:|-------------:|-------:|-------:|--------------:|--------------:|
| 1 | knn delayed-cap | 2 | 28 | 128 | | 0.887 | 0.939 | 0.001 | 2,490 |
| 1 | random | 7 | 19 | 137 | | 0.680 | 0.805 | 0 | 0 |
| 2 | knn delayed-cap | 1 | | | | | | extinct t=11 | 0 |
| 2 | random | 3 | | | | | | extinct t=5 | 0 |
| 3 | knn delayed-cap | 11 | 21 | 109 | 754 | 0.228 | 0.236 | 0.936 | 1 |
| 3 | random | 23 | 16 | 142 | | 0.578 | 0.760 | 0 | 0 |

Seed 1 k-NN recovered (min n=2 at t=16, recover t=28). Cap armed at t=9. Then 2,490 generations fell back to random pairing. Census lived at n=1,200. That is the n=68 all-pairs-veto death avoided, not a restock. No hold. Flicker at t=128: mean rasp 0.502, mean pierce 0.134. At t=2,500 saliva is negative and p_biter=0.001. F@1500=0.887 is under 0.9; F@2500=0.939. Do not call F near 1 a bug.

Seed 2 k-NN died at t=11, n=1, after the cap armed at t=8 with 64 accepted pairs. Fallback never fired. Crash death, same class as v1 seed deaths, not a veto.

Seed 3 k-NN held. Flicker t=109: mean rasp 0.562, mean pierce 0.096. Hold t=754, majority t=931. F@1500=0.228, F@2500=0.236. At t=2,500: n=1,200, p_biter=0.936, rasp 2.916 (under `z_max=3.0`), pierce 0.457, saliva -1.228, digest 2.585, heme_safe 2.886. Wound 3.41 and sweat 4.59 still beat bite 0.20. One fallback generation. heme_safe rose at t=448 after wound load at t=20.

Random recovered on seeds 1 and 3, flickered, and lost the kit. Seed 2 random extinct at t=5.

Fruit-forever seed 1 to t=400: last p_biter=0, F=0.217, digest +0.081, heme_safe down. No bite kit.

Vampire on the pre-registered checklist is 1 of 3 seeds (held, p_biter>=0.05, rasp>pierce at flicker, F@1500<0.9). Saliva is negative on that seed. 10k closed.

## Long arm

10k stays closed: held biters on 1 of 3 seeds. A later bridge-ramp arm is a new question with new locks, only if an origin 10k still has p_biter high while wound and tears dominate energy. Origin graph: halt.

Do not raise `bite_weight`. Do not pin GraphForge.

## How to run

```text
python3.12 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/python -m pytest
.venv/bin/python -m vial_sanguis2 run --arm knn --mode knn --k 3 \
    --kinship-cap on --phi-max 0.25 --cap-on-at recover \
    --generations 2500 --n 1000 --seed 1 --starve-at 5 \
    --out logs/knn_delayed_2500_s1.json
```

## Files

| Path | Role |
|------|------|
| `src/vial_sanguis2/` | config, genome, diet, fitness, mating, inheritance, population, metrics, cli |
| `AGENTS.md` | Five laws. VBD gate. No GraphForge. |
| `LONG_ARM.md` | origin, optional 10k, halt |
| `tests/` | five laws, bridge does not step to zero, cap fallback |
| `logs/knn_delayed_2500_s{1,2,3}.json` | origin k-NN locks (local) |
| `logs/random_2500_s{1,2,3}.json` | origin random locks (local) |
| `logs/fruit_forever_400_s1.json` | fruit-forever lock (local) |

Research index: https://gist.github.com/martialsystems/12835f747d6360781f3cc7f91f243178
