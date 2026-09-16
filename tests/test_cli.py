# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import argparse
import json
from pathlib import Path

from vial_sanguis2.cli import _parser, main


def test_tiny_run(tmp_path: Path) -> None:
    out = tmp_path / "tiny.json"
    rc = main(
        [
            "run",
            "--arm",
            "knn",
            "--generations",
            "4",
            "--n",
            "24",
            "--seed",
            "1",
            "--starve-at",
            "2",
            "--kinship-cap",
            "off",
            "--out",
            str(out),
        ]
    )
    assert rc == 0
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["seed"] == 1
    assert "n_cap_fallback" in payload["generations"][-1]
    assert payload["config"]["z_max"] == 3.0
    assert payload["config"]["kinship_cap"] is False
    assert "t_held_biter" in payload
    assert "F_1500" in payload
    assert out.with_suffix(".jsonl").is_file()


def test_cli_defaults_are_delayed_cap() -> None:
    p = _parser()
    run_p = None
    for action in p._actions:
        if isinstance(action, argparse._SubParsersAction):
            run_p = action.choices["run"]
    assert run_p is not None
    help_text = run_p.format_help()
    assert "--cap-on-at" in help_text
    assert "recover" in help_text
    assert "bite-weight" not in help_text
    assert "host-shift" not in help_text
    assert "exudate" not in help_text
    assert "scab" not in help_text
    run = p.parse_args(["run"])
    assert run.kinship_cap == "on"
    assert run.cap_on_at == "recover"
    assert run.phi_max == 0.25
    assert run.min_accepted_pairs == 8
    assert run.generations == 2500
