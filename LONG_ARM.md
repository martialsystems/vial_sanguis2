# Long arm

Autonomous continue is allowed only along LONG_ARM.md.
Curiosity is not a transition.
Unfreezing a diet knob is a halt.

## Status

state: halt
next legal node: none

Origin 2500 finished. Vampire checklist failed as a 3-seed claim. Do not average seed 3
with the other two. Origin 10k stays closed. Bridge-ramp stays closed.

Seed-3 persistence 10k finished. Same frozen origin knobs. Cap arm (fallback gens=1).
F@10k=0.228. Last p_biter=0.066. Sweat 4.591 and wound 3.410 beat bite 0.013.
Pierce went negative. Saliva still negative. Rasp still at z_max.

Host-calorie table from those JSON files (no new run): after t_held=754, sweat+wound
is at least 93.34% of host. Peak bite share 5.74% at t=4,644. At t=2,500 bite is
2.31% of host with p_biter=0.936. At t=10,000 bite is 0.15% of host. p_biter is a
threshold on a side channel. Bite is not a meal. No ramp. This tree is finished.
Halt.

## Origin sentence (locked)

Delayed cap plus fallback gives one held kit off F=1 in three seeds; that kit is
exudate-heavy; the other two either die in the crash or spend the run in fallback.
Successor engine works. Vampire checklist failed as a 3-seed claim.
Residual risk is the finding, not a bug.

Seed 1 is fallback-dominated, not k-NN. Seed 2 is bottleneck extinction.
Seed 3 is a held kit at F about 0.23 that still lives on sweat and wound.

## Frozen diet

t_starve=5, k_tears=40, bite_weight=1.0, c_pierce=0.05, c_digest=0.40,
c_heme=0.40, c_heme_in=0.30, beta_heme=2.0, survive_thresh_host=0.075,
n_floor=8, n_ceiling=1200, phi_max=0.25, z_max=3.0, min_accepted_pairs=8,
cap-on-at recover.

Do not raise bite_weight after a fail.
Do not pin GraphForge.
Do not patch vial_sanguis.

## Origin JSON (do not restamp)

- `logs/knn_delayed_2500_s1.json` seed 1: fallback-dominated, min n=2, flicker 128, no hold, F@1500=0.887, fallback gens=2,490
- `logs/knn_delayed_2500_s2.json` seed 2: extinct t=11, 64 accepted pairs, fallback never fired
- `logs/knn_delayed_2500_s3.json` seed 3: min n=11, flicker 109, hold 754, F@1500=0.228, p_biter=0.936, saliva negative, exudate-heavy
- `logs/random_2500_s{1,2,3}.json`
- `logs/fruit_forever_400_s1.json` last p_biter=0

## Seed 3 persistence JSON (do not restamp)

- `logs/knn_delayed_10000_s3.json` seed 3: t_held=754, F@1500=0.228, F@10k=0.228, p_biter=0.066, fallback gens=1, sweat 4.591, wound 3.410, bite 0.013, saliva -1.096, rasp 2.926, pierce -0.150
