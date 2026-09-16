# vial_sanguis2

Under an explicit diet ladder and an allowed population crash, does a Drosophila-like sponging labellum evolve prestomal-tooth rasping and a costly shallow bite, and can that kit hold with F off 1 if kinship cap waits until after recovery and falls back to random pairing instead of vetoing every pair?

Delayed-cap can hold F about 0.23. The fly that passes `p_biter` still lives on sweat and wound. Vampire-as-bite fails as a 3-seed claim and as a meal share. Science lock `4946ab5`. That is the end of vial_sanguis2.

Successor to [vial_sanguis](https://github.com/martialsystems/vial_sanguis) `@b7347ce`. Cliff result there stands. This engine: delayed cap, pair fallback, `z_max=3.0`.

A later intact-skin engine is a new repo with a different default meal, not an arm on this tree.

## Origin

n=1,000, t_starve=5, 2,500 generations, seeds 1 to 3. k-NN delayed-cap (`n>=50` after starve, then `phi_max=0.25`). If the cap would accept fewer than 8 pairs, that generation uses random pairing (`n_cap_fallback`). Random mating control. Fruit-forever t=400. No host-shift.

Delayed cap plus fallback gives one held kit off F=1 in three seeds; that kit is exudate-heavy; the other two either die in the crash or spend the run in fallback. Vampire checklist failed as a 3-seed claim. Residual risk is the finding, not a bug. Do not average seed 3 with the other two.

Crash is real on every starve arm. Fruit-forever last p_biter=0 (max 0.0008). Origin 10k stays closed. Bridge-ramp stays closed.

| seed | mate | min n | t_recover | flicker | t_held_biter | F@1500 | F@2500 | final p_biter | fallback gens |
|-----:|------|------:|----------:|--------:|-------------:|-------:|-------:|--------------:|--------------:|
| 1 | fallback-dominated | 2 | 28 | 128 | | 0.887 | 0.939 | 0.001 | 2,490 |
| 1 | random | 7 | 19 | 137 | | 0.680 | 0.805 | 0 | 0 |
| 2 | knn delayed-cap | 1 | | | | | | extinct t=11 | 0 |
| 2 | random | 3 | | | | | | extinct t=5 | 0 |
| 3 | knn delayed-cap | 11 | 21 | 109 | 754 | 0.228 | 0.236 | 0.936 | 1 |
| 3 | random | 23 | 16 | 142 | | 0.578 | 0.760 | 0 | 0 |

Seed 1 is not a delayed-cap result. Cap armed at t=9. Then 2,490 generations were random fallback. Census lived at n=1,200. That is the n=68 all-pairs-veto death avoided, not a restock. No hold. F@1500=0.887; F@2500=0.939. Log it as fallback-dominated, not as k-NN. Do not tighten fallback so this seed counts as cap-on.

Seed 2 k-NN died at t=11, n=1, after the cap armed at t=8 with 64 accepted pairs. Fallback never fired. Bottleneck extinction, same class as v1 seed deaths.

Seed 3 k-NN: flicker t=109, hold t=754, majority t=931. F@1500=0.228, F@2500=0.236. At t=2,500: n=1,200, p_biter=0.936, rasp 2.916 (under `z_max=3.0`), pierce 0.457, saliva -1.228. One fallback generation.

Random 1 and 3 lived without a hold. Random 2 died.

Fruit-forever seed 1 to t=400: last p_biter=0, F=0.217, digest +0.081, heme_safe down. No bite kit.

Seed 3 to 10k, same frozen knobs, cap arm, fallback gens still 1. F@10k=0.228. n=1,200. Last p_biter=0.066. At t=10,000: sweat 4.591, wound 3.410, tears 0.076, bite 0.013. Exudate stayed the meal. Saliva -1.096. Rasp 2.926. Pierce -0.150. JSON: `logs/knn_delayed_10000_s3.json` and `logs/knn_delayed_2500_s3.json`. Do not restamp.

## Host calories

Copied from those two JSON files. Host calories: tears + sweat + usable_blood. Wound and bite split usable_blood in proportion to the logged channel means (`bite_weight=1`). No new run.

| t | p_biter | F | tears % | sweat % | wound % | bite % | sweat+wound % |
|--:|--------:|--:|--------:|--------:|--------:|-------:|--------------:|
| 754 hold | 0.058 | 0.236 | 1.32 | 52.20 | 45.42 | 1.06 | 97.62 |
| 2,500 | 0.936 | 0.236 | 0.95 | 57.25 | 39.49 | 2.31 | 96.74 |
| 4,644 peak bite | 1.000 | 0.223 | 0.91 | 55.08 | 38.26 | 5.74 | 93.34 |
| 10,000 | 0.066 | 0.228 | 0.97 | 58.32 | 40.57 | 0.15 | 98.88 |

After t_held=754, sweat+wound is at least 93.34% of host. Peak bite share is 5.74% (t=4,644, p_biter=1). `p_biter` counts flies with non-zero `energy_bite` on an exudate meal.

## How to run

```text
python3.12 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/python -m pytest
.venv/bin/python -m vial_sanguis2 run --arm knn --mode knn --k 3 \
    --kinship-cap on --phi-max 0.25 --cap-on-at recover \
    --generations 2500 --n 1000 --seed 1 --starve-at 5 \
    --out logs/knn_delayed_2500_s1.json
.venv/bin/python -m vial_sanguis2 run --arm knn --mode knn --k 3 \
    --kinship-cap on --phi-max 0.25 --cap-on-at recover \
    --generations 10000 --n 1000 --seed 3 --starve-at 5 \
    --out logs/knn_delayed_10000_s3.json
```

## Files

| Path | Role |
|------|------|
| `src/vial_sanguis2/` | config, genome, diet, fitness, mating, inheritance, population, metrics, cli |
| `AGENTS.md` | Five laws. VBD gate. No GraphForge. Closed at `4946ab5`. |
| `LONG_ARM.md` | next legal node: none |
| `tests/` | five laws, cap fallback, origin locks, host-calorie shares |
| `logs/knn_delayed_2500_s{1,2,3}.json` | origin k-NN locks (local). Seed 1 is fallback-dominated. |
| `logs/random_2500_s{1,2,3}.json` | origin random locks (local) |
| `logs/fruit_forever_400_s1.json` | fruit-forever lock (local) |
| `logs/knn_delayed_10000_s3.json` | seed-3 persistence (local) |

Do not raise `bite_weight`. Do not pin GraphForge. Do not patch vial_sanguis.

[Fly research index](https://gist.github.com/martialsystems/12835f747d6360781f3cc7f91f243178)
