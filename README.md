# vial_sanguis2

Under an explicit diet ladder and an allowed population crash, does a Drosophila-like sponging labellum evolve prestomal-tooth rasping and a costly shallow bite, and can that kit hold with F off 1 if kinship cap waits until after recovery and falls back to random pairing instead of vetoing every pair?

This is not an origin of hematophagy. Successor to [vial_sanguis](https://github.com/martialsystems/vial_sanguis). Cliff result there stands. This engine starts from that measurement: delayed cap, pair fallback, `z_max=3.0`. Origin arm has no host shift and does not step exudate to zero.

## Origin

n=1,000, t_starve=5, 2,500 generations, seeds 1 to 3. k-NN delayed-cap (`n>=50` after starve, then `phi_max=0.25`). If the cap would accept fewer than 8 pairs, that generation uses random pairing (`n_cap_fallback`). Random mating control. Fruit-forever t=400. No host-shift.

Delayed cap plus fallback gives one held kit off F=1 in three seeds; that kit is exudate-heavy; the other two either die in the crash or spend the run in fallback. Successor engine works. Vampire checklist failed as a 3-seed claim. Residual risk is the finding, not a bug. Do not average seed 3 with the other two.

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

Seed 3 k-NN held a kit at F about 0.23. Flicker t=109: mean rasp 0.562, mean pierce 0.096. Hold t=754, majority t=931. F@1500=0.228, F@2500=0.236. At t=2,500: n=1,200, p_biter=0.936, rasp 2.916 (under `z_max=3.0`), pierce 0.457, saliva -1.228. Sweat 4.59 and wound 3.41 beat bite 0.20. Majority p_biter here is a threshold on a fly that still lives on exudate, not a bite economy. One fallback generation.

Random 1 and 3 lived without a hold. Random 2 died. Mating system is still not required for survival and still not enough for a hold except on one k-NN seed.

Fruit-forever seed 1 to t=400: last p_biter=0, F=0.217, digest +0.081, heme_safe down. No bite kit.

## Seed 3 persistence

New question, new locks, seed 3 only. Same frozen origin knobs. No host shift, no exudate cliff, no `bite_weight` change. Fruit-forever unused.

On the one line that held a kit at F about 0.23, does that kit persist to 10k, and does bite energy ever catch sweat and wound, or does exudate stay the meal?

`--generations 10000 --seed 3` delayed-cap recipe. Same line as origin seed 3: flicker 109, hold 754, F@1500=0.228, F@2500=0.236. Cap arm: fallback gens still 1. F@10k=0.228. n=1,200. Last p_biter=0.066, last 10 gens all above 0.05. `t_held_biter` is still 754. p_biter last sat above 0.5 at t=8,711 and dipped below 0.05 at t=9,176.

At t=10,000: sweat 4.591, wound 3.410, tears 0.076, bite 0.013. Bite did not catch sweat or wound. Exudate stayed the meal. Saliva -1.096. Rasp 2.926 under `z_max=3.0`. Pierce -0.150 (it was 0.457 at t=2,500). This is persistence of F off 1 on a cap arm, with the shortcut still the economy. It is not a vampire-checklist pass.

JSON: `logs/knn_delayed_10000_s3.json` (local). Halt. No bridge-ramp. Do not raise `bite_weight`.

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
| `AGENTS.md` | Five laws. VBD gate. No GraphForge. |
| `LONG_ARM.md` | origin locked; seed-3 persistence 10k |
| `tests/` | five laws, bridge does not step to zero, cap fallback, origin locks |
| `logs/knn_delayed_2500_s{1,2,3}.json` | origin k-NN locks (local). Seed 1 is fallback-dominated. |
| `logs/random_2500_s{1,2,3}.json` | origin random locks (local) |
| `logs/fruit_forever_400_s1.json` | fruit-forever lock (local) |
| `logs/knn_delayed_10000_s3.json` | seed-3 persistence (local) |

Do not raise `bite_weight`. Do not pin GraphForge. Do not patch vial_sanguis.

Research index: https://gist.github.com/martialsystems/12835f747d6360781f3cc7f91f243178
