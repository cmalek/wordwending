# Copyright (C) 2026 Chris Malek.
"""Evaluation policy and metric contract models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from wordwending.models.ocr import (
    PageClass,
    PageEvaluationSummary,
    PreparationMode,
    SchemaModel,
)


class MetricProfile(BaseModel):
    """Versioned, deterministic evaluation policy."""

    #: Forbid unknown keys so persisted metric profiles stay stable.
    model_config = ConfigDict(extra="forbid")
    #: Stable profile identifier for persisted evaluation policy.
    profile_id: str
    #: Semantic version of the profile contract.
    version: str
    #: Whether whitespace differences affect token comparison.
    whitespace_significant: bool = True
    #: Whether punctuation differences affect token comparison.
    punctuation_significant: bool = True
    #: Whether character case affects token comparison.
    case_sensitive: bool = True
    #: Whether line-break placement affects comparison.
    line_breaks_significant: bool = True
    #: Regex pattern used to tokenize diplomatic text for scoring.
    tokenizer_pattern: str = r"\w+(?:['’]\w+)*|[^\w\s]"  # noqa: RUF001
    #: Minimum IoU for region geometry to count as a match.
    region_iou_threshold: float = Field(default=0.5, gt=0, le=1)
    #: Exclude illegible gold targets from metric denominators.
    exclude_illegible: bool = True
    #: Treat unknown style facets as incorrect rather than ignored.
    unknown_style_is_incorrect: bool = True


class PageEvaluationRecord(SchemaModel):
    """One evaluated page with run, preparation, and runner context."""

    #: Run identifier that produced this evaluation.
    run_id: str
    #: Document identifier within the evaluation corpus.
    document_id: str
    #: Page identifier within the document.
    page_id: str
    #: Final page-class label used for cohort grouping.
    page_class: PageClass
    #: Preparation mode applied before OCR.
    preparation_mode: PreparationMode
    #: Prepared-page identifier used for this evaluation.
    prepared_page_id: str
    #: Runner identifier that produced the scored witness.
    runner_id: str
    #: Per-page grouped evaluation output.
    summary: PageEvaluationSummary


class EvaluationCohortKey(SchemaModel):
    """Grouping key for one fixed evaluation cohort view."""

    #: Page-class label shared by every record in the cohort.
    page_class: PageClass
    #: Optional preparation-mode dimension for the cohort.
    preparation_mode: PreparationMode | None = None
    #: Optional runner dimension for the cohort.
    runner_id: str | None = None


class EvaluationCohortSummary(SchemaModel):
    """Aggregated evaluation output for one cohort."""

    #: Grouping key identifying this cohort.
    key: EvaluationCohortKey
    #: Document identifiers represented in the cohort.
    document_ids: list[str]
    #: Page identifiers represented in the cohort.
    page_ids: list[str]
    #: Weighted evaluation summary for the cohort.
    summary: PageEvaluationSummary


class EvaluationCohortReport(SchemaModel):
    """Fixed cohort views emitted by evaluation aggregation."""

    #: Summaries grouped by page class only.
    by_page_class: list[EvaluationCohortSummary]
    #: Summaries grouped by page class and preparation mode.
    by_page_class_and_preparation_mode: list[EvaluationCohortSummary]
    #: Summaries grouped by page class and runner.
    by_page_class_and_runner: list[EvaluationCohortSummary]
