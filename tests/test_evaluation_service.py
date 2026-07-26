# Copyright (C) 2026 Chris Malek.
"""Tests for diplomatic OCR page evaluation."""

from __future__ import annotations

from pathlib import Path

from bochord.models import (
    BoundingBox,
    BundlePage,
    CoordinateSpace,
    FontSlant,
    FontWeight,
    GoldCoverage,
    GoldLineJoin,
    GoldNoteLink,
    GoldPageAnnotation,
    GoldRegionAnnotation,
    GoldStyleSpan,
    GoldTextSpan,
    LineRecord,
    MetricProfile,
    NoteKind,
    NoteRecord,
    ObjectProvenance,
    PageClass,
    PreparationMode,
    PreparedPage,
    RegionKind,
    RegionRecord,
    ReviewDimension,
    SpanRecord,
    TextRole,
    Typography,
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
            prepared_page_id="prepared-page-1",
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


def test_coverage_do_not_score_excludes_spans_from_denominators() -> None:
    prediction, gold = text_case(
        predicted="wrong",
        reference="right",
        coverage_do_not_score=True,
    )

    summary = EvaluationService().evaluate_page(prediction, gold, profile())
    metrics = {metric.metric_id: metric for metric in summary.text.metrics}

    assert metrics["character_error_rate"].denominator == 0
    assert metrics["character_error_rate"].value == 0
    assert metrics["exact_span_match_rate"].denominator == 0
    assert metrics["exact_span_match_rate"].value == 0


def test_iou_fallback_matches_highest_same_family_span() -> None:
    provenance = _provenance()
    prediction = BundlePage(
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
                line_ids=["line-1", "line-2"],
                provenance=provenance,
            )
        ],
        lines=[
            LineRecord(
                line_id="line-1",
                region_id="region-1",
                line_order=1,
                span_ids=["span-near"],
                provenance=provenance,
            ),
            LineRecord(
                line_id="line-2",
                region_id="region-1",
                line_order=2,
                span_ids=["span-far"],
                provenance=provenance,
            ),
        ],
        spans=[
            SpanRecord(
                span_id="span-near",
                line_id="line-1",
                text_diplomatic="match",
                bounding_box=BoundingBox(x0=0, y0=0, x1=40, y1=10),
                provenance=provenance,
            ),
            SpanRecord(
                span_id="span-far",
                line_id="line-2",
                text_diplomatic="other",
                bounding_box=BoundingBox(x0=60, y0=60, x1=90, y1=90),
                provenance=provenance,
            ),
        ],
    )
    gold = GoldPageAnnotation(
        page_id="page-1",
        page_number=1,
        source_run_id="run-1",
        base_graph_revision="graph-1",
        prepared_image_checksum="sha256:image",
        coverage=[
            GoldCoverage(
                coverage_id="coverage-1",
                dimensions=[ReviewDimension.TEXT],
                target_object_ids=["span-near", "span-far"],
                exhaustive=True,
            )
        ],
        text_spans=[
            GoldTextSpan(
                annotation_id="gold-span-1",
                bounding_box=BoundingBox(x0=0, y0=0, x1=38, y1=10),
                text_diplomatic="match",
            )
        ],
    )

    summary = EvaluationService().evaluate_page(prediction, gold, profile())
    metrics = {metric.metric_id: metric for metric in summary.text.metrics}

    assert metrics["character_error_rate"].value == 0
    assert metrics["character_error_rate"].denominator == 5
    assert metrics["exact_span_match_rate"].value == 1


def test_empty_ref_note_omitted_when_other_spans_contribute_denom() -> None:
    prediction, gold = text_case(predicted="ghost", reference="")
    provenance = _provenance()
    prediction.spans.append(
        SpanRecord(
            span_id="span-2",
            line_id="line-1",
            text_diplomatic="ok",
            bounding_box=BoundingBox(x0=50, y0=0, x1=80, y1=10),
            provenance=provenance,
        )
    )
    prediction.lines[0].span_ids.append("span-2")
    gold.coverage[0].target_object_ids.append("span-2")
    gold.text_spans.append(
        GoldTextSpan(
            annotation_id="gold-span-2",
            target_object_id="span-2",
            text_diplomatic="ok",
        )
    )

    summary = EvaluationService().evaluate_page(prediction, gold, profile())
    metrics = {metric.metric_id: metric for metric in summary.text.metrics}

    assert metrics["character_error_rate"].denominator == 2
    assert metrics["character_error_rate"].value == 0
    assert metrics["character_error_rate"].note is None
    assert metrics["word_error_rate"].note is None


def _prepared_page() -> PreparedPage:
    """Return a shared prepared-page shell for multi-object fixtures."""
    return PreparedPage(
        prepared_page_id="prepared-page-1",
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
    )


def structured_prediction() -> BundlePage:
    """Two ordered body regions with an explicit left-to-right line join."""
    provenance = _provenance()
    return BundlePage(
        page_id="page-1",
        page_number=1,
        prepared_page=_prepared_page(),
        regions=[
            RegionRecord(
                region_id="region-1",
                region_kind=RegionKind.BODY,
                reading_order_index=1,
                bounding_box=BoundingBox(x0=0, y0=0, x1=40, y1=20),
                line_ids=["line-1"],
                provenance=provenance,
            ),
            RegionRecord(
                region_id="region-2",
                region_kind=RegionKind.BODY,
                reading_order_index=2,
                bounding_box=BoundingBox(x0=0, y0=30, x1=40, y1=50),
                line_ids=["line-2"],
                provenance=provenance,
            ),
        ],
        lines=[
            LineRecord(
                line_id="line-1",
                region_id="region-1",
                line_order=1,
                span_ids=["span-1"],
                joins_to_line_id="line-2",
                provenance=provenance,
            ),
            LineRecord(
                line_id="line-2",
                region_id="region-2",
                line_order=1,
                span_ids=["span-2"],
                provenance=provenance,
            ),
        ],
        spans=[
            SpanRecord(
                span_id="span-1",
                line_id="line-1",
                text_diplomatic="a",
                provenance=provenance,
            ),
            SpanRecord(
                span_id="span-2",
                line_id="line-2",
                text_diplomatic="b",
                provenance=provenance,
            ),
        ],
    )


def structured_gold() -> GoldPageAnnotation:
    """Gold structure matching ``structured_prediction`` with one join."""
    return GoldPageAnnotation(
        page_id="page-1",
        page_number=1,
        source_run_id="run-1",
        base_graph_revision="graph-1",
        prepared_image_checksum="sha256:image",
        coverage=[
            GoldCoverage(
                coverage_id="coverage-structure",
                dimensions=[ReviewDimension.STRUCTURE],
                target_object_ids=["region-1", "region-2", "line-1", "line-2"],
                exhaustive=True,
            )
        ],
        regions=[
            GoldRegionAnnotation(
                annotation_id="gold-region-1",
                target_object_id="region-1",
                region_kind=RegionKind.BODY,
                reading_order_index=1,
            ),
            GoldRegionAnnotation(
                annotation_id="gold-region-2",
                target_object_id="region-2",
                region_kind=RegionKind.BODY,
                reading_order_index=2,
            ),
        ],
        line_joins=[
            GoldLineJoin(
                annotation_id="join-1",
                left_line_id="line-1",
                right_line_id="line-2",
                joined=True,
            )
        ],
    )


def bold_but_not_italic_prediction() -> BundlePage:
    """One span that is bold but upright (not italic)."""
    provenance = _provenance()
    return BundlePage(
        page_id="page-1",
        page_number=1,
        prepared_page=_prepared_page(),
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
                text_diplomatic="word",
                typography=Typography(
                    weight=FontWeight.BOLD,
                    slant=FontSlant.UPRIGHT,
                ),
                provenance=provenance,
            )
        ],
    )


def bold_italic_gold() -> GoldPageAnnotation:
    """Gold style requiring both bold and italic facets."""
    return GoldPageAnnotation(
        page_id="page-1",
        page_number=1,
        source_run_id="run-1",
        base_graph_revision="graph-1",
        prepared_image_checksum="sha256:image",
        coverage=[
            GoldCoverage(
                coverage_id="coverage-typography",
                dimensions=[ReviewDimension.TYPOGRAPHY],
                target_object_ids=["span-1"],
                exhaustive=True,
            )
        ],
        style_spans=[
            GoldStyleSpan(
                annotation_id="gold-style-1",
                target_object_id="span-1",
                typography=Typography(
                    weight=FontWeight.BOLD,
                    slant=FontSlant.ITALIC,
                ),
            )
        ],
    )


def wrong_note_link_prediction() -> BundlePage:
    """Note linked to the wrong marker span."""
    provenance = _provenance()
    return BundlePage(
        page_id="page-1",
        page_number=1,
        prepared_page=_prepared_page(),
        regions=[
            RegionRecord(
                region_id="region-1",
                region_kind=RegionKind.BODY,
                reading_order_index=1,
                line_ids=["line-1"],
                note_ids=["note-1"],
                provenance=provenance,
            )
        ],
        lines=[
            LineRecord(
                line_id="line-1",
                region_id="region-1",
                line_order=1,
                span_ids=["span-marker", "span-other"],
                provenance=provenance,
            )
        ],
        spans=[
            SpanRecord(
                span_id="span-marker",
                line_id="line-1",
                text_diplomatic="1",
                roles=[TextRole.FOOTNOTE_MARKER],
                provenance=provenance,
            ),
            SpanRecord(
                span_id="span-other",
                line_id="line-1",
                text_diplomatic="x",
                provenance=provenance,
            ),
        ],
        notes=[
            NoteRecord(
                note_id="note-1",
                note_kind=NoteKind.FOOTNOTE_BLOCK,
                region_id="region-1",
                text_diplomatic="note body",
                linked_marker_span_ids=["span-other"],
                provenance=provenance,
            )
        ],
    )


def note_link_gold() -> GoldPageAnnotation:
    """Gold requiring marker ``span-marker`` to link to ``note-1``."""
    return GoldPageAnnotation(
        page_id="page-1",
        page_number=1,
        source_run_id="run-1",
        base_graph_revision="graph-1",
        prepared_image_checksum="sha256:image",
        coverage=[
            GoldCoverage(
                coverage_id="coverage-notes",
                dimensions=[ReviewDimension.NOTE_LINKAGE],
                target_object_ids=["note-1", "span-marker"],
                exhaustive=True,
            )
        ],
        note_links=[
            GoldNoteLink(
                annotation_id="gold-note-1",
                marker_span_ids=["span-marker"],
                note_target_id="note-1",
            )
        ],
    )


def test_structure_scores_region_order_iou_and_line_joins() -> None:
    summary = EvaluationService().evaluate_page(
        structured_prediction(),
        structured_gold(),
        profile(),
    )
    metrics = {metric.metric_id: metric.value for metric in summary.structure.metrics}
    assert metrics["region_coverage"] == 1
    assert metrics["line_ordering_correctness"] == 1
    assert metrics["line_join_fidelity"] == 1


def test_style_facets_are_independent() -> None:
    summary = EvaluationService().evaluate_page(
        bold_but_not_italic_prediction(),
        bold_italic_gold(),
        profile(),
    )
    metrics = {metric.metric_id: metric.value for metric in summary.typography.metrics}
    assert metrics["font_weight_accuracy"] == 1
    assert metrics["font_slant_accuracy"] == 0


def test_style_family_collapse_is_partial_xor() -> None:
    partial = EvaluationService().evaluate_page(
        bold_but_not_italic_prediction(),
        bold_italic_gold(),
        profile(),
    )
    assert "style_family_collapse" in {
        flag.flag_type for flag in partial.typography.flags
    }

    both_wrong_prediction = bold_but_not_italic_prediction()
    both_wrong_prediction.spans[0].typography = Typography(
        weight=FontWeight.REGULAR,
        slant=FontSlant.UPRIGHT,
    )
    both_wrong = EvaluationService().evaluate_page(
        both_wrong_prediction,
        bold_italic_gold(),
        profile(),
    )
    assert "style_family_collapse" not in {
        flag.flag_type for flag in both_wrong.typography.flags
    }

    weight_only_gold = bold_italic_gold()
    weight_only_gold.style_spans[0].typography = Typography(weight=FontWeight.BOLD)
    weight_only = EvaluationService().evaluate_page(
        bold_but_not_italic_prediction(),
        weight_only_gold,
        profile(),
    )
    assert "style_family_collapse" not in {
        flag.flag_type for flag in weight_only.typography.flags
    }


def test_wrong_line_join_lowers_fidelity() -> None:
    prediction = structured_prediction()
    prediction.lines[0].joins_to_line_id = None
    summary = EvaluationService().evaluate_page(
        prediction,
        structured_gold(),
        profile(),
    )
    metrics = {metric.metric_id: metric.value for metric in summary.structure.metrics}
    assert metrics["line_join_fidelity"] < 1


def test_wrong_note_edge_emits_targeted_flag() -> None:
    summary = EvaluationService().evaluate_page(
        wrong_note_link_prediction(),
        note_link_gold(),
        profile(),
    )
    metrics = {
        metric.metric_id: metric.value for metric in summary.note_linkage.metrics
    }
    assert metrics["note_linkage_success"] == 0
    assert {flag.flag_type for flag in summary.note_linkage.flags} == {
        "ambiguous_note_linkage"
    }


def test_image_scoped_coverage_scores_intersecting_spans() -> None:
    prediction, gold = text_case(predicted="þæt", reference="þæt")
    gold.coverage = [
        GoldCoverage(
            coverage_id="coverage-box",
            dimensions=[ReviewDimension.TEXT],
            bounding_box=BoundingBox(x0=0, y0=0, x1=50, y1=20),
            exhaustive=True,
        )
    ]

    summary = EvaluationService().evaluate_page(prediction, gold, profile())
    metrics = {metric.metric_id: metric for metric in summary.text.metrics}

    assert metrics["character_error_rate"].denominator > 0
    assert metrics["character_error_rate"].value == 0


def test_image_scoped_coverage_skips_nonintersecting_spans() -> None:
    prediction, gold = text_case(predicted="þæt", reference="þæt")
    gold.coverage = [
        GoldCoverage(
            coverage_id="coverage-elsewhere",
            dimensions=[ReviewDimension.TEXT],
            bounding_box=BoundingBox(x0=80, y0=80, x1=90, y1=90),
            exhaustive=True,
        )
    ]

    summary = EvaluationService().evaluate_page(prediction, gold, profile())
    metrics = {metric.metric_id: metric for metric in summary.text.metrics}

    assert metrics["character_error_rate"].denominator == 0
    assert metrics["character_error_rate"].value == 0


def test_missing_left_line_does_not_inflate_unjoined_fidelity() -> None:
    prediction = structured_prediction()
    gold = structured_gold()
    gold.coverage[0].target_object_ids = [
        *gold.coverage[0].target_object_ids,
        "line-missing",
    ]
    gold.line_joins = [
        GoldLineJoin(
            annotation_id="join-missing",
            left_line_id="line-missing",
            right_line_id="line-2",
            joined=False,
        )
    ]

    summary = EvaluationService().evaluate_page(prediction, gold, profile())
    metrics = {metric.metric_id: metric for metric in summary.structure.metrics}

    assert metrics["line_join_fidelity"].denominator == 1
    assert metrics["line_join_fidelity"].value == 0


def test_note_target_annotation_id_matches_predicted_note() -> None:
    prediction = wrong_note_link_prediction()
    prediction.notes[0].linked_marker_span_ids = ["span-marker"]
    gold = note_link_gold()
    gold.regions = [
        GoldRegionAnnotation(
            annotation_id="gold-note-body",
            target_object_id="note-1",
            region_kind=RegionKind.FOOTNOTE,
            reading_order_index=1,
        )
    ]
    gold.note_links[0].note_target_id = "gold-note-body"

    summary = EvaluationService().evaluate_page(prediction, gold, profile())
    metrics = {
        metric.metric_id: metric.value for metric in summary.note_linkage.metrics
    }

    assert metrics["note_linkage_success"] == 1
    assert summary.note_linkage.flags == []
