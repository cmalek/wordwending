# Copyright (C) 2026 Chris Malek.
"""Wave A exit proof: assemble → eval → export with assemble-scoped fixtures."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from wordwending.cli.cli import cli

_FIXTURES = Path(__file__).parent / "fixtures" / "assemble"
_WITNESS_FIXTURE = _FIXTURES / "olmocr-chat-completion-v1.json"
_MANIFEST_FIXTURE = _FIXTURES / "manifest-v1.json"
_GOLD_FIXTURE = _FIXTURES / "gold-v1.json"
_PROFILE_FIXTURE = _FIXTURES / "metric-profile-v1.json"


def _stage_bundle_inputs(bundle_root: Path) -> None:
    """Copy witness fixture and prepared image under ``bundle_root``."""
    witnesses_dir = bundle_root / "raw" / "witnesses"
    witnesses_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(_WITNESS_FIXTURE, witnesses_dir / "olmocr-chat-completion-v1.json")

    image_dir = bundle_root / "prepared"
    image_dir.mkdir(parents=True, exist_ok=True)
    (image_dir / "page.png").write_bytes(b"fake-png-bytes")


def test_assemble_eval_export_wave_a_exit(runner, tmp_path: Path) -> None:
    """Assemble page graph scores against assemble gold, then export markdown."""
    bundle_root = tmp_path / "bundle"
    bundle_root.mkdir()
    _stage_bundle_inputs(bundle_root)

    assemble_result = runner.invoke(
        cli,
        [
            "assemble",
            "--bundle-root",
            str(bundle_root),
            "--manifest",
            str(_MANIFEST_FIXTURE),
        ],
    )
    assert assemble_result.exit_code == 0, assemble_result.output

    prediction = bundle_root / "pages" / "page-0001" / "graph" / "page_graph.json"
    assert prediction.exists()
    prediction_payload = json.loads(prediction.read_text(encoding="utf-8"))
    assert prediction_payload["page_id"] == "page-0001"
    assert [span["span_id"] for span in prediction_payload["spans"]] == [
        "prepared-page-1:s0",
        "prepared-page-1:s1",
    ]

    scores_path = tmp_path / "scores.json"
    eval_result = runner.invoke(
        cli,
        [
            "eval",
            "--prediction",
            str(prediction),
            "--gold",
            str(_GOLD_FIXTURE),
            "--profile",
            str(_PROFILE_FIXTURE),
            "--output-json",
            str(scores_path),
        ],
    )
    assert eval_result.exit_code == 0, eval_result.output
    scores = json.loads(scores_path.read_text(encoding="utf-8"))
    assert set(scores) == {"text", "structure", "style"}
    text_metrics = {item["metric_id"]: item for item in scores["text"]["metrics"]}
    assert "exact_span_match_rate" in text_metrics
    assert text_metrics["exact_span_match_rate"]["value"] == 1.0
    assert text_metrics["exact_span_match_rate"]["denominator"] == 2.0

    bundle_json = bundle_root / "document-bundle.json"
    assert bundle_json.exists()
    export_result = runner.invoke(
        cli,
        ["export", str(bundle_json), "--bundle-root", str(bundle_root)],
    )
    assert export_result.exit_code == 0, export_result.output
    assert (bundle_root / "exports" / "document.md").exists()
