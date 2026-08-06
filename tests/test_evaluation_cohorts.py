# Copyright (C) 2026 Chris Malek.
"""Tests for weighted evaluation cohort aggregation."""

from __future__ import annotations

from wordwending.models import (
    EvaluationFamilySummary,
    MetricScore,
    PageClass,
    PageEvaluationSummary,
    PreparationMode,
)
from wordwending.models.evaluation import PageEvaluationRecord
from wordwending.services.evaluation_cohorts import EvaluationCohortService


def metric(family: EvaluationFamilySummary, metric_id: str) -> MetricScore:
    """Return one metric from a family summary by id."""
    return {item.metric_id: item for item in family.metrics}[metric_id]


def record(  # noqa: PLR0913
    document_id: str,
    *,
    page_id: str | None = None,
    numerator: float | None = 0.0,
    denominator: float = 0.0,
    value: float | None = None,
    note: str | None = None,
    mode: PreparationMode = PreparationMode.FULL_PAGE,
    runner: str = "olmocr",
    page_class: PageClass = PageClass.ORDINARY_PROSE,
) -> PageEvaluationRecord:
    """Build one page evaluation record with a single macron_recall metric."""
    if value is None:
        metric_value = (
            0.0
            if numerator is None or denominator == 0.0
            else numerator / denominator
        )
    else:
        metric_value = value
    return PageEvaluationRecord(
        run_id="run-1",
        document_id=document_id,
        page_id=page_id or f"{document_id}-page",
        page_class=page_class,
        preparation_mode=mode,
        prepared_page_id=f"prepared-{document_id}",
        runner_id=runner,
        summary=PageEvaluationSummary(
            text=EvaluationFamilySummary(
                metrics=[
                    MetricScore(
                        metric_id="macron_recall",
                        value=metric_value,
                        numerator=numerator,
                        denominator=denominator,
                        note=note,
                    )
                ]
            )
        ),
    )


def test_page_class_summary_sums_metric_denominators() -> None:
    report = EvaluationCohortService().summarize(
        [
            record("doc-a", numerator=8, denominator=10),
            record("doc-b", numerator=1, denominator=2),
        ]
    )
    score = metric(report.by_page_class[0].summary.text, "macron_recall")
    assert (score.numerator, score.denominator, score.value) == (9.0, 12.0, 0.75)
    assert report.by_page_class[0].document_ids == ["doc-a", "doc-b"]


def test_reports_split_same_class_by_mode_and_runner() -> None:
    report = EvaluationCohortService().summarize(
        [
            record("doc-a", mode=PreparationMode.FULL_PAGE, runner="olmocr"),
            record("doc-b", mode=PreparationMode.COLUMNS, runner="kraken"),
        ]
    )
    assert len(report.by_page_class) == 1
    assert len(report.by_page_class_and_preparation_mode) == 2
    assert len(report.by_page_class_and_runner) == 2


def test_empty_input_returns_three_empty_lists() -> None:
    report = EvaluationCohortService().summarize([])
    assert report.by_page_class == []
    assert report.by_page_class_and_preparation_mode == []
    assert report.by_page_class_and_runner == []


def test_zero_denominator_unit_error_aggregates_as_unit_error() -> None:
    report = EvaluationCohortService().summarize(
        [
            record(
                "doc-a",
                numerator=None,
                denominator=0.0,
                value=1.0,
            ),
            record("doc-b", numerator=0.0, denominator=0.0, value=0.0),
        ]
    )
    score = metric(report.by_page_class[0].summary.text, "macron_recall")
    assert score.value == 1.0
    assert score.numerator is None
    assert score.denominator == 0.0
    assert score.note == (
        "one or more empty-reference predictions produced unit error"
    )


def test_zero_denominator_without_unit_error_aggregates_to_zero() -> None:
    report = EvaluationCohortService().summarize(
        [
            record("doc-a", numerator=0.0, denominator=0.0, value=0.0),
            record("doc-b", numerator=0.0, denominator=0.0, value=0.0),
        ]
    )
    score = metric(report.by_page_class[0].summary.text, "macron_recall")
    assert score.value == 0.0
    assert score.numerator == 0.0
    assert score.denominator == 0.0
    assert score.note is None
