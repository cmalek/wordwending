# Copyright (C) 2026 Chris Malek.
"""Tests for abstaining merge policy models and merge service (Task 1: models only)."""

from __future__ import annotations

import json

from bochord.models import (
    CoordinateSpace,
    LineRecord,
    MergePolicy,
    ObjectProvenance,
    PassWitnessPage,
    RegionKind,
    RegionRecord,
    SpanRecord,
)


def _provenance() -> ObjectProvenance:
    """Return valid single-page object provenance."""
    return ObjectProvenance(
        source_page_id="page-0001",
        witness_ids=["wit-1"],
        runner_ids=["olmocr"],
        machine_confidence=0.91,
        merge_confidence=0.84,
    )


def test_merge_policy_defaults_empty_runner_text_precedence() -> None:
    """Empty precedence list means abstain on text disagreement (pre-benchmark)."""
    policy = MergePolicy(policy_id="merge-v1", version="1.0.0")
    assert policy.runner_text_precedence == []
    assert policy.structure_scaffold_runner_ids == []
    assert policy.min_merge_confidence_to_accept == 0.6
    assert policy.iou_match_threshold == 0.5
    assert policy.text_normalization_policy_id == "text-norm-v1"


def test_pass_witness_page_round_trip() -> None:
    """PassWitnessPage serializes and validates a runner page graph fragment."""
    provenance = _provenance()
    coordinate_space = CoordinateSpace(
        space_id="prepared-page-1",
        width_px=100,
        height_px=100,
    )
    witness = PassWitnessPage(
        witness_id="wit-1",
        runner_id="olmocr",
        prepared_page_id="prepared-page-1",
        coordinate_space=coordinate_space,
        regions=[
            RegionRecord(
                region_id="region-1",
                region_kind=RegionKind.BODY,
                reading_order_index=1,
                line_ids=["line-1"],
                provenance=provenance,
            )
        ],
        lines=[
            LineRecord(
                line_id="line-1",
                region_id="region-1",
                line_order=1,
                span_ids=["span-1"],
                provenance=provenance,
            )
        ],
        spans=[
            SpanRecord(
                span_id="span-1",
                line_id="line-1",
                text_diplomatic="hello",
                text_normalized="hello",
                provenance=provenance,
            )
        ],
        machine_confidence=0.88,
    )
    payload = witness.model_dump(mode="json")
    round_tripped = PassWitnessPage.model_validate_json(json.dumps(payload))
    assert round_tripped.witness_id == "wit-1"
    assert round_tripped.runner_id == "olmocr"
    assert round_tripped.prepared_page_id == "prepared-page-1"
    assert len(round_tripped.regions) == 1
    assert len(round_tripped.lines) == 1
    assert len(round_tripped.spans) == 1
    assert round_tripped.machine_confidence == 0.88
