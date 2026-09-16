# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_readme() -> None:
    text = (REPO / "README.md").read_text(encoding="utf-8")
    assert text.startswith("# vial_sanguis2\n")
    body = text.split("\n", 1)[1].lstrip()
    assert body.startswith("Under an explicit diet ladder")
    assert "This is not an origin of hematophagy." in text
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
    assert "10k closed" in text
    assert "1 of 3" in text
    assert "Do not raise" in text
    agents = (REPO / "AGENTS.md").read_text(encoding="utf-8")
    assert "—" not in agents
    assert "Do not pin GraphForge" in agents
    long_arm = (REPO / "LONG_ARM.md").read_text(encoding="utf-8")
    assert "—" not in long_arm
    assert "Do not raise bite_weight" in long_arm
    assert (REPO / "LICENSE").is_file()
    assert "matplotlib" not in (REPO / "pyproject.toml").read_text(encoding="utf-8")
