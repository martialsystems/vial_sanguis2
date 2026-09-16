# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_readme() -> None:
    text = (REPO / "README.md").read_text(encoding="utf-8")
    assert text.startswith("# vial_sanguis2\n")
    body = text.split("\n", 1)[1].lstrip()
    assert body.startswith("Under an explicit diet ladder")
    paras = [p.strip() for p in body.split("\n\n") if p.strip()]
    assert paras[0].startswith("Under an explicit diet ladder")
    assert paras[1].startswith("Delayed-cap can hold F about 0.23.")
    assert "4946ab5" in paras[1]
    assert "Vampire-as-bite fails as a 3-seed claim and as a meal share." in paras[1]
    assert "What it is not" not in text
    assert "—" not in text
    assert "z_max=3.0" in text
    assert "n_cap_fallback" in text
    assert ".venv/bin/python -m pytest" in text
    assert "12835f747d6360781f3cc7f91f243178" in text
    assert "LONG_ARM.md" in text
    assert "min_accepted_pairs" in text or "fewer than 8 pairs" in text
    assert "logs/knn_delayed_2500_s1.json" in text
    assert "2,490" in text
    assert "extinct t=11" in text
    assert "t_held_biter" in text
    assert "0.228" in text
    assert "fallback-dominated" in text
    assert "Vampire checklist failed as a 3-seed claim." in text
    assert "one held kit off F=1" in text
    assert "Do not average seed 3" in text
    assert "Origin 10k stays closed" in text
    assert "Bridge-ramp stays closed" in text
    assert "Do not raise" in text
    assert "knn_delayed_10000_s3.json" in text
    assert "F@10k=0.228" in text
    assert "Exudate stayed the meal" in text
    assert "Pierce -0.150" in text
    assert "intact-skin engine is a new repo" in text
    assert "different default meal" in text
    assert "[Fly research index](https://gist.github.com/martialsystems/12835f747d6360781f3cc7f91f243178)" in text
    agents = (REPO / "AGENTS.md").read_text(encoding="utf-8")
    assert "—" not in agents
    assert "Do not pin GraphForge" in agents
    assert "4946ab5" in agents
    assert "Next legal node: none" in agents
    long_arm = (REPO / "LONG_ARM.md").read_text(encoding="utf-8")
    assert "—" not in long_arm
    assert "Do not raise bite_weight" in long_arm
    assert "4946ab5" in long_arm
    assert "next legal node: none" in long_arm
    assert (REPO / "LICENSE").is_file()
    assert "matplotlib" not in (REPO / "pyproject.toml").read_text(encoding="utf-8")
