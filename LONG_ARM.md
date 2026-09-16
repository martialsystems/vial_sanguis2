# Long arm

Autonomous continue is allowed only along LONG_ARM.md.
Curiosity is not a transition.
Unfreezing a diet knob is a halt.

## Status

state: halt
next legal node: none

Origin 2500 finished. Seeds 1 to 3 k-NN delayed-cap, random control, fruit-forever 400.
10k closed: held biters on 1 of 3 k-NN seeds (seed 3). Seed 1 lived on cap fallback
(2,490 gens) without a hold. Seed 2 extinct t=11. Do not average them.

No host-shift on origin. No exudate cliff. No Q2/Q3 from vial_sanguis.
A later bridge-ramp arm is a new question with new locks, only after origin 10k
and only if p_biter is high but wound+tears still dominate energy. Origin 10k
did not run.

## Frozen diet

t_starve=5, k_tears=40, bite_weight=1.0, c_pierce=0.05, c_digest=0.40,
c_heme=0.40, c_heme_in=0.30, beta_heme=2.0, survive_thresh_host=0.075,
n_floor=8, n_ceiling=1200, phi_max=0.25, z_max=3.0, min_accepted_pairs=8,
cap-on-at recover.

Do not raise bite_weight after a fail.
Do not pin GraphForge.

## Origin JSON (do not restamp)

- `logs/knn_delayed_2500_s1.json` seed 1: min n=2, flicker 128, no hold, F@1500=0.887, fallback gens=2,490
- `logs/knn_delayed_2500_s2.json` seed 2: extinct t=11
- `logs/knn_delayed_2500_s3.json` seed 3: min n=11, flicker 109, hold 754, F@1500=0.228, p_biter=0.936
- `logs/random_2500_s{1,2,3}.json`
- `logs/fruit_forever_400_s1.json` last p_biter=0
