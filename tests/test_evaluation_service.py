# Copyright (C) 2026 Chris Malek.
"""Tests for diplomatic OCR page evaluation."""

from __future__ import annotations

from pathlib import Path

from bochord.models import (
    BoundingBox,
    BundlePage,
    CoordinateSpace,
    GoldCoverage,
    GoldPageAnnotation,
    GoldTextSpan,
    LineRecord,
    MetricProfile,
    ObjectProvenance,
    PageClass,
    PreparationMode,
    PreparedPage,
    RegionKind,
    RegionRecord,
    ReviewDimension,
    SpanRecord,
)
from bochord.services.evaluation import EvaluationService

_PROFILE_PATH = Path(__file__).parent / "fixtures/evaluation/metric-profile-v1.json"


def profile() -> MetricProfile:
    """Load the frozen v1 metric profile without mutating defaults."""
    return MetricProfile.model_validate_json(_PROFILE_PATH.read_text(encoding="utf-8"))


def _provenance() -> ObjectProvenance:
    """Return valid single-page object provenance."""
    return ObjectProvenance(
        source_page_id="page-0001",
        witness_ids=["wit-1"],
        runner_ids=["olmocr"],
        machine_confidence=0.91,
        merge_confidence=0.84,
    )


def text_case(
    predicted: str,
    reference: str,
    *,
    do_not_score: bool = False,
    illegible: bool = False,
    coverage_do_not_score: bool = False,
) -> tuple[BundlePage, GoldPageAnnotation]:
    """Build one predicted span and one exhaustive target-anchored gold text span."""
    provenance = _provenance()
    page = BundlePage(
        page_id="page-1",
        page_number=1,
        prepared_page=PreparedPage(
            preparation_mode=PreparationMode.FULL_PAGE,
            page_class=PageClass.ORDINARY_PROSE,
            image_path="page.png",
            source_artifact_id="source-1",
            image_checksum="sha256:image",
            preparation_recipe_id="prep-v1",
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
                text_diplomatic=predicted,
                text_normalized=predicted,
                bounding_box=BoundingBox(x0=0, y0=0, x1=40, y1=10),
                provenance=provenance,
            )
        ],
    )
    coverage_kwargs: dict[str, object] = {
        "coverage_id": "coverage-1",
        "dimensions": [ReviewDimension.TEXT],
        "target_object_ids": ["span-1"],
        "exhaustive": True,
    }
    if coverage_do_not_score:
        coverage_kwargs["do_not_score"] = True
        coverage_kwargs["exclusion_reason"] = "out of scope"
    span_kwargs: dict[str, object] = {
        "annotation_id": "gold-span-1",
        "target_object_id": "span-1",
        "text_diplomatic": reference,
        "illegible": illegible,
    }
    if do_not_score:
        span_kwargs["do_not_score"] = True
        span_kwargs["exclusion_reason"] = "annotator abstained"
    gold = GoldPageAnnotation(
        page_id="page-1",
        page_number=1,
        source_run_id="run-1",
        base_graph_revision="graph-1",
        prepared_image_checksum="sha256:image",
        coverage=[GoldCoverage(**coverage_kwargs)],
        text_spans=[GoldTextSpan(**span_kwargs)],
    )
    return page, gold


def test_text_metrics_use_nfc_graphemes_and_explicit_denominators() -> None:
    prediction, gold = text_case(
        predicted="þæt drēam",
        reference="þæt dre\u0304am",
    )

    summary = EvaluationService().evaluate_page(prediction, gold, profile())
    metrics = {metric.metric_id: metric for metric in summary.text.metrics}

    assert metrics["character_error_rate"].value == 0
    assert metrics["character_error_rate"].denominator == 9
    assert metrics["word_error_rate"].value == 0
    assert metrics["macron_recall"].value == 1
    assert metrics["thorn_eth_preservation_rate"].value == 1


def test_empty_covered_gold_scores_zero_over_zero() -> None:
    prediction, gold = text_case(predicted="", reference="")

    summary = EvaluationService().evaluate_page(prediction, gold, profile())
    metrics = {metric.metric_id: metric for metric in summary.text.metrics}

    assert metrics["character_error_rate"].value == 0
    assert metrics["character_error_rate"].denominator == 0
    assert metrics["character_error_rate"].numerator == 0
    assert metrics["word_error_rate"].value == 0
    assert metrics["word_error_rate"].denominator == 0
    assert metrics["exact_span_match_rate"].value == 0
    assert metrics["exact_span_match_rate"].denominator == 0


def test_empty_reference_nonempty_prediction_is_unit_error() -> None:
    prediction, gold = text_case(predicted="ghost", reference="")

    summary = EvaluationService().evaluate_page(prediction, gold, profile())
    metrics = {metric.metric_id: metric for metric in summary.text.metrics}

    assert metrics["character_error_rate"].value == 1
    assert metrics["character_error_rate"].denominator == 0
    assert metrics["character_error_rate"].note is not None
    assert metrics["word_error_rate"].value == 1
    assert metrics["word_error_rate"].denominator == 0
    assert metrics["word_error_rate"].note is not None


def test_do_not_score_text_span_never_enters_denominator() -> None:
    prediction, gold = text_case(
        predicted="wrong",
        reference="right",
        do_not_score=True,
    )

    summary = EvaluationService().evaluate_page(prediction, gold, profile())
    metrics = {metric.metric_id: metric for metric in summary.text.metrics}

    assert metrics["character_error_rate"].denominator == 0
    assert metrics["character_error_rate"].value == 0
    assert metrics["exact_span_match_rate"].denominator == 0
    assert metrics["exact_span_match_rate"].value == 0


def test_exclude_illegible_skips_gold_text() -> None:
    prediction, gold = text_case(
        predicted="wrong",
        reference="right",
        illegible=True,
    )

    summary = EvaluationService().evaluate_page(prediction, gold, profile())
    metrics = {metric.metric_id: metric for metric in summary.text.metrics}

    assert metrics["character_error_rate"].denominator == 0
    assert metrics["exact_span_match_rate"].denominator == 0


def test_punctuation_policy_strips_before_compare() -> None:
    prediction, gold = text_case(predicted="hello,", reference="hello")
    policy = profile().model_copy(update={"punctuation_significant": False})

    summary = EvaluationService().evaluate_page(prediction, gold, policy)
    metrics = {metric.metric_id: metric for metric in summary.text.metrics}

    assert metrics["character_error_rate"].value == 0
    assert metrics["exact_span_match_rate"].value == 1


def test_missing_watchlist_characters_emit_flag_and_lower_recall() -> None:
    prediction, gold = text_case(
        predicted="paet dream",
        reference="þæt drēam æ",
    )

    summary = EvaluationService().evaluate_page(prediction, gold, profile())
    metrics = {metric.metric_id: metric for metric in summary.text.metrics}

    assert metrics["macron_recall"].value == 0
    assert metrics["thorn_eth_preservation_rate"].value == 0
    assert metrics["ligature_preservation_rate"].value == 0
    assert {flag.flag_type for flag in summary.text.flags} == {
        "missing_watchlist_character"
    }
