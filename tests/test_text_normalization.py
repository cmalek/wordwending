# Copyright (C) 2026 Chris Malek.
"""Tests for text normalization policy models and TextNormalizer service."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from bochord.models import (
    BundlePage,
    CoordinateSpace,
    LineJoinKind,
    LineRecord,
    NoteKind,
    NoteMarkerNormalizedForm,
    NoteRecord,
    ObjectProvenance,
    PageClass,
    PreparationMode,
    PreparedPage,
    RegionKind,
    RegionRecord,
    SpanRecord,
    SuperscriptNormalizedForm,
    TextNormalizationPolicy,
    UnicodeNormalizationForm,
)
from bochord.services.text_normalization import (
    DEFAULT_TEXT_NORMALIZATION_POLICY,
    TextNormalizer,
)

_CASES_PATH = Path(__file__).parent / "fixtures/text_normalization/cases.json"


def _provenance() -> ObjectProvenance:
    """Return valid single-page object provenance."""
    return ObjectProvenance(
        source_page_id="page-0001",
        witness_ids=["wit-1"],
        runner_ids=["olmocr"],
        machine_confidence=0.91,
        merge_confidence=0.84,
    )


def _policy_from_overrides(overrides: dict[str, Any]) -> TextNormalizationPolicy:
    """Build a policy from fixture override fields."""
    return TextNormalizationPolicy(
        policy_id="text-norm-test",
        version="1",
        **overrides,
    )


def _load_cases() -> list[dict[str, Any]]:
    return json.loads(_CASES_PATH.read_text(encoding="utf-8"))


def test_default_policy_preserves_historical_characters() -> None:
    policy = TextNormalizationPolicy(policy_id="text-norm-v1", version="1")
    assert policy.preserve_historical_characters is True
    assert policy.unicode_form is UnicodeNormalizationForm.NFC


def test_policy_rejects_historical_modernization_flag() -> None:
    with pytest.raises(ValidationError):
        TextNormalizationPolicy(
            policy_id="bad",
            version="1",
            preserve_historical_characters=False,
        )


def test_default_text_normalization_policy_matches_v1_contract() -> None:
    assert DEFAULT_TEXT_NORMALIZATION_POLICY.policy_id == "text-norm-v1"
    assert DEFAULT_TEXT_NORMALIZATION_POLICY.version == "1"


@pytest.mark.parametrize("case", _load_cases(), ids=lambda case: case["id"])
def test_fixture_case(case: dict[str, Any]) -> None:
    policy = _policy_from_overrides(case["policy_overrides"])
    normalizer = TextNormalizer(policy)
    method = case["method"]

    if method == "join_line_texts":
        normalized, record = normalizer.join_line_texts(
            case["left_diplomatic"],
            case["right_diplomatic"],
            left_line_id=case["left_line_id"],
            right_line_id=case["right_line_id"],
            join_kind=LineJoinKind(case["join_kind"]),
        )
        assert normalized == case["expected_normalized"]
        assert record.removed_hyphen is case["expected_removed_hyphen"]
        assert record.left_line_id == case["left_line_id"]
        assert record.right_line_id == case["right_line_id"]
        assert record.policy_id == policy.policy_id
        return

    normalizer_method = getattr(normalizer, method)
    assert normalizer_method(case["input_diplomatic"]) == case["expected_normalized"]


def test_apply_to_page_leaves_diplomatic_unchanged() -> None:
    provenance = _provenance()
    page = BundlePage(
        page_id="page-1",
        page_number=1,
        prepared_page=PreparedPage(
            prepared_page_id="prepared-page-1",
            preparation_mode=PreparationMode.FULL_PAGE,
            page_class=PageClass.ORDINARY_PROSE,
            image_path="page.png",
            source_artifact_id="source-1",
            image_checksum="sha256:image",
            preparation_recipe_id="prep-v1",
            preparation_recipe_digest="digest-prep-v1",
            coordinate_space=CoordinateSpace(
                space_id="prepared-page-1",
                width_px=100,
                height_px=100,
            ),
        ),
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
                text_diplomatic="  ǣ\tþ  ",
                text_normalized=None,
                provenance=provenance,
            )
        ],
        notes=[
            NoteRecord(
                note_id="note-1",
                note_kind=NoteKind.SIDE_NOTE,
                text_diplomatic="See*†",
                text_normalized=None,
                provenance=provenance,
            )
        ],
    )
    policy = TextNormalizationPolicy(
        policy_id="text-norm-v1",
        version="1",
        note_marker_form=NoteMarkerNormalizedForm.PLACEHOLDER,
    )
    normalizer = TextNormalizer(policy)
    result = normalizer.apply_to_page(page)

    assert result.spans[0].text_diplomatic == "  ǣ\tþ  "
    assert result.spans[0].text_normalized == "ǣ þ"
    assert result.notes[0].text_diplomatic == "See*†"
    assert result.notes[0].text_normalized == "See[n][n]"


def test_join_hyphen_at_line_end_false_skips_removal() -> None:
    policy = TextNormalizationPolicy(
        policy_id="text-norm-test",
        version="1",
        join_hyphen_at_line_end=False,
    )
    normalizer = TextNormalizer(policy)
    normalized, record = normalizer.join_line_texts(
        "word-",
        "break",
        left_line_id="line-1",
        right_line_id="line-2",
        join_kind=LineJoinKind.HYPHEN_JOIN,
    )
    assert normalized == "word-break"
    assert record.removed_hyphen is False


def test_apply_to_span_and_note_copy_records() -> None:
    provenance = _provenance()
    span = SpanRecord(
        span_id="span-1",
        line_id="line-1",
        text_diplomatic="x²",
        text_normalized="old",
        provenance=provenance,
    )
    note = NoteRecord(
        note_id="note-1",
        note_kind=NoteKind.SIDE_NOTE,
        text_diplomatic="*",
        text_normalized="old",
        provenance=provenance,
    )
    policy = TextNormalizationPolicy(
        policy_id="text-norm-v1",
        version="1",
        superscript_form=SuperscriptNormalizedForm.FLATTEN,
        note_marker_form=NoteMarkerNormalizedForm.PLACEHOLDER,
    )
    normalizer = TextNormalizer(policy)

    updated_span = normalizer.apply_to_span(span)
    updated_note = normalizer.apply_to_note(note)

    assert span.text_normalized == "old"
    assert updated_span.text_normalized == "x2"
    assert note.text_normalized == "old"
    assert updated_note.text_normalized == "[n]"
