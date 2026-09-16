# Agent notes: vial_sanguis2

MIT. Closed-form NumPy generation engine. Not a fork of vial_sanguis.

Question: under an explicit diet ladder and an allowed population crash, does a Drosophila-like sponging labellum evolve prestomal-tooth rasping and a costly shallow bite, and can that kit hold with F off 1 if kinship cap waits until after recovery and falls back to random pairing instead of vetoing every pair?

## Five laws

1. Closed vial. No immigration, no restock.
2. Load required. Hidden recessives exist. Load is excluded from mating similarity.
3. Census may fall. Never invent adults. Cap fallback is random pairing, not restock.
4. Diet ladder required. Tears, sweat, wound, bite. Origin arm does not step exudate to zero.
5. Mouthpart path is prestomal-tooth rasp. No mandibles. No mosquito stylets. digest and heme_safe are their own QTLs.

Do not pin GraphForge. Do not reuse vialforge. VBD is the finish gate.
Do not raise bite_weight after a cliff. Do not average a living biter seed with an extinct seed.
Do not call F=1 a bug. Do not open a 10k arm unless held biters and F@1500 < 0.9 on at least 2 seeds.

Frozen diet: t_starve=5, k_tears=40, bite_weight=1.0, c_pierce=0.05,
c_digest=0.40, c_heme=0.40, c_heme_in=0.30, beta_heme=2.0,
survive_thresh_host=0.075, n_floor=8, n_ceiling=1200, phi_max=0.25,
z_max=3.0, min_accepted_pairs=8, cap-on-at recover.

Autonomous continue is allowed only along LONG_ARM.md.
Curiosity is not a transition.
Unfreezing a diet knob is a halt.

This repo only (not the home VBD pack).

## Verify

`python3 ~/agent_laws_verify_before_done/vbd_gate.py check --app-root . --claim-done`
`.venv/bin/python -m pytest`
