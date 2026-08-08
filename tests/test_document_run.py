# Copyright (C) 2026 Chris Malek.
"""Tests for document run configuration models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from wordwending.models.document_run import (
    DocumentRunConfig,
    DocumentRunnerSpec,
    DocumentRunStage,
)


def runner_spec() -> DocumentRunnerSpec:
    """Return a minimal runner spec for config validation tests."""
    return DocumentRunnerSpec(
        runner_id="olmocr",
        runner_reference_path="runners/olmocr-ref.json",
        policy_path="runners/olmocr-policy.json",
    )


def valid_config(**overrides: object) -> DocumentRunConfig:
    """Return a minimal valid document run config with optional overrides."""
    payload: dict[str, object] = {
        "run_id": "run-001",
        "document_id": "doc-source-001",
        "bundle_root": "bundles/doc-source-001",
        "source_path": "sources/source.pdf",
        "recipe_paths": ["recipes/default.json"],
        "source_json": "provenance/source.json",
        "bibliographic_json": "provenance/bibliographic.json",
        "acquisition_json": "provenance/acquisition.json",
        "merge_policy_path": "policies/merge.json",
        "runners": [runner_spec().model_dump()],
    }
    payload.update(overrides)
    return DocumentRunConfig.model_validate(payload)


def test_document_run_config_rejects_empty_runners() -> None:
    with pytest.raises(ValidationError, match="runners"):
        valid_config(runners=[])


def test_document_run_config_rejects_empty_recipe_paths() -> None:
    with pytest.raises(ValidationError, match="recipe_paths"):
        valid_config(recipe_paths=[])


def test_document_run_config_rejects_unknown_stage_strings() -> None:
    with pytest.raises(ValidationError, match="stages"):
        valid_config(stages=["prepare", "not-a-stage"])


def test_default_stages_without_gold() -> None:
    config = valid_config()
    assert config.resolved_stages() == [
        DocumentRunStage.PREPARE,
        DocumentRunStage.RUN,
        DocumentRunStage.ASSEMBLE,
        DocumentRunStage.ISSUE_REVIEW_TASKS,
        DocumentRunStage.EXPORT,
    ]


def test_default_stages_with_gold_and_metric_profile() -> None:
    config = valid_config(
        gold_page_paths={"page-001": "gold/page-001.json"},
        metric_profile_path="metrics/default.json",
    )
    assert config.resolved_stages() == [
        DocumentRunStage.PREPARE,
        DocumentRunStage.RUN,
        DocumentRunStage.ASSEMBLE,
        DocumentRunStage.EVAL,
        DocumentRunStage.ISSUE_REVIEW_TASKS,
        DocumentRunStage.EXPORT,
    ]


def test_default_stages_without_eval_when_only_gold_paths() -> None:
    config = valid_config(gold_page_paths={"page-001": "gold/page-001.json"})
    assert DocumentRunStage.EVAL not in config.resolved_stages()


def test_default_stages_without_eval_when_only_metric_profile() -> None:
    config = valid_config(metric_profile_path="metrics/default.json")
    assert DocumentRunStage.EVAL not in config.resolved_stages()


def test_default_stages_skip_export_when_stages_none() -> None:
    config = valid_config(skip_export=True)
    assert config.resolved_stages() == [
        DocumentRunStage.PREPARE,
        DocumentRunStage.RUN,
        DocumentRunStage.ASSEMBLE,
        DocumentRunStage.ISSUE_REVIEW_TASKS,
    ]


def test_explicit_stages_ignore_skip_export() -> None:
    config = valid_config(
        stages=[DocumentRunStage.PREPARE, DocumentRunStage.EXPORT],
        skip_export=True,
    )
    assert config.resolved_stages() == [
        DocumentRunStage.PREPARE,
        DocumentRunStage.EXPORT,
    ]
