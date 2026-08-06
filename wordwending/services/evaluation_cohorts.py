# Copyright (C) 2026 Chris Malek.
"""Weighted aggregation of page evaluation records into fixed cohort views."""

from __future__ import annotations

from collections import defaultdict

from wordwending.models import (
    EvaluationFamilySummary,
    MetricScore,
    PageClass,
    PageEvaluationSummary,
    PreparationMode,
    StyleEvaluationSummary,
)
from wordwending.models.evaluation import (
    EvaluationCohortKey,
    EvaluationCohortReport,
    EvaluationCohortSummary,
    PageEvaluationRecord,
)


def _aggregate_metric(scores: list[MetricScore]) -> MetricScore:
    """
    Sum numerators and denominators for one metric across cohort pages.

    Args:
        scores: Metric scores sharing the same ``metric_id``.

    Returns:
        Weighted aggregate score for the cohort.

    """
    denominator = sum(score.denominator or 0.0 for score in scores)
    if denominator == 0:
        unit_error = any(
            score.numerator is None and score.value == 1.0 for score in scores
        )
        return MetricScore(
            metric_id=scores[0].metric_id,
            value=1.0 if unit_error else 0.0,
            numerator=None if unit_error else 0.0,
            denominator=0.0,
            note=(
                "one or more empty-reference predictions produced unit error"
                if unit_error
                else None
            ),
        )
    numerator = sum(score.numerator or 0.0 for score in scores)
    return MetricScore(
        metric_id=scores[0].metric_id,
        value=numerator / denominator,
        numerator=numerator,
        denominator=denominator,
    )


def _aggregate_family(
    families: list[EvaluationFamilySummary],
) -> EvaluationFamilySummary:
    """
    Aggregate one evaluation family across cohort pages.

    Args:
        families: Family summaries from each page in the cohort.

    Returns:
        Weighted family summary with flags in stable record order.

    """
    metrics_by_id: dict[str, list[MetricScore]] = {}
    metric_order: list[str] = []
    flags = []
    for family in families:
        flags.extend(family.flags)
        for score in family.metrics:
            if score.metric_id not in metrics_by_id:
                metrics_by_id[score.metric_id] = []
                metric_order.append(score.metric_id)
            metrics_by_id[score.metric_id].append(score)
    return EvaluationFamilySummary(
        metrics=[
            _aggregate_metric(metrics_by_id[metric_id]) for metric_id in metric_order
        ],
        flags=flags,
    )


def _aggregate_summaries(
    summaries: list[PageEvaluationSummary],
) -> PageEvaluationSummary:
    """
    Aggregate full page summaries for one cohort.

    Args:
        summaries: Per-page summaries belonging to the cohort.

    Returns:
        Weighted cohort summary preserving family boundaries.

    """
    return PageEvaluationSummary(
        text=_aggregate_family([summary.text for summary in summaries]),
        structure=_aggregate_family([summary.structure for summary in summaries]),
        style=StyleEvaluationSummary(
            typography=_aggregate_family(
                [summary.style.typography for summary in summaries]
            ),
            note_linkage=_aggregate_family(
                [summary.style.note_linkage for summary in summaries]
            ),
        ),
    )


def _cohort_summary(
    cohort_records: list[PageEvaluationRecord],
    key: EvaluationCohortKey,
) -> EvaluationCohortSummary:
    """
    Build one cohort summary from grouped page records.

    Args:
        cohort_records: Records sharing the same cohort key.
        key: Grouping key for the cohort.

    Returns:
        Aggregated cohort summary with sorted identifiers.

    """
    return EvaluationCohortSummary(
        key=key,
        document_ids=sorted({record.document_id for record in cohort_records}),
        page_ids=sorted({record.page_id for record in cohort_records}),
        summary=_aggregate_summaries([record.summary for record in cohort_records]),
    )


def _summarize_by_page_class(
    records: list[PageEvaluationRecord],
) -> list[EvaluationCohortSummary]:
    """
    Group records by page class and aggregate each cohort.

    Args:
        records: Page evaluation records to summarize.

    Returns:
        Cohort summaries ordered by page-class value.

    """
    groups: dict[PageClass, list[PageEvaluationRecord]] = defaultdict(list)
    for record in records:
        groups[record.page_class].append(record)
    return [
        _cohort_summary(
            groups[page_class],
            EvaluationCohortKey(page_class=page_class),
        )
        for page_class in sorted(groups, key=lambda item: item.value)
    ]


def _summarize_by_page_class_and_preparation_mode(
    records: list[PageEvaluationRecord],
) -> list[EvaluationCohortSummary]:
    """
    Group records by page class and preparation mode.

    Args:
        records: Page evaluation records to summarize.

    Returns:
        Cohort summaries ordered by page class then preparation mode.

    """
    groups: dict[tuple[PageClass, PreparationMode], list[PageEvaluationRecord]] = (
        defaultdict(list)
    )
    for record in records:
        groups[(record.page_class, record.preparation_mode)].append(record)
    return [
        _cohort_summary(
            groups[group_key],
            EvaluationCohortKey(
                page_class=group_key[0],
                preparation_mode=group_key[1],
            ),
        )
        for group_key in sorted(
            groups,
            key=lambda item: (item[0].value, item[1].value),
        )
    ]


def _summarize_by_page_class_and_runner(
    records: list[PageEvaluationRecord],
) -> list[EvaluationCohortSummary]:
    """
    Group records by page class and runner id.

    Args:
        records: Page evaluation records to summarize.

    Returns:
        Cohort summaries ordered by page class then runner id.

    """
    groups: dict[tuple[PageClass, str], list[PageEvaluationRecord]] = defaultdict(list)
    for record in records:
        groups[(record.page_class, record.runner_id)].append(record)
    return [
        _cohort_summary(
            groups[group_key],
            EvaluationCohortKey(
                page_class=group_key[0],
                runner_id=group_key[1],
            ),
        )
        for group_key in sorted(
            groups,
            key=lambda item: (item[0].value, item[1]),
        )
    ]


class EvaluationCohortService:
    """
    Aggregate page evaluation records into fixed cohort views.

    Emits weighted summaries grouped by page class, page class with preparation
    mode, and page class with runner. Metrics sum numerators and denominators;
    no blended page score is produced.
    """

    def summarize(
        self,
        records: list[PageEvaluationRecord],
    ) -> EvaluationCohortReport:
        """
        Build the three fixed cohort views from page evaluation records.

        Args:
            records: Per-page evaluation outputs to aggregate.

        Returns:
            Report with weighted cohort summaries for each fixed grouping.

        """
        return EvaluationCohortReport(
            by_page_class=_summarize_by_page_class(records),
            by_page_class_and_preparation_mode=_summarize_by_page_class_and_preparation_mode(
                records
            ),
            by_page_class_and_runner=_summarize_by_page_class_and_runner(records),
        )
