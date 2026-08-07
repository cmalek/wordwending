# Copyright (C) 2026 Chris Malek.
"""Bake-off matrix models for Spec 0004 Phase 5 harness (not Phase COMPLETE)."""

from __future__ import annotations

from pydantic import Field

from wordwending.models.ocr import (
    BundlePage,
    GoldPageAnnotation,
    PageClass,
    PageEvaluationSummary,
    SchemaModel,
)

#: On-disk filename written by :class:`~wordwending.services.bakeoff.BakeoffService`.
BAKEOFF_MATRIX_FILENAME = "bakeoff-matrix-v1.json"
#: Schema version embedded in every bake-off matrix artifact.
BAKEOFF_MATRIX_SCHEMA_VERSION = "bakeoff-matrix/v1"
#: Deferred Spec 0004 Phase 5 exits documented on every matrix.
DEFERRED_BAKEOFF_NOTES: tuple[str, ...] = (
    "cost scoring deferred (placeholder fields only)",
    "license scoring deferred (placeholder fields only)",
    "operability scoring deferred (placeholder fields only)",
    "full corpus held-out slices deferred",
    "Spec 0004 Phase 5 NOT COMPLETE under Wave F harness alone",
)


class BakeoffCandidate(SchemaModel):
    """One bake-off runner candidate with deferred scoring placeholders."""

    #: Stable logical runner id (``olmocr``, ``kraken``, …).
    runner_id: str
    #: License scoring placeholder until Phase 5 license exit lands.
    license_placeholder: str | None = None
    #: Cost scoring placeholder until Phase 5 cost exit lands.
    cost_placeholder: str | None = None
    #: Hugging Face operability placeholder until Phase 5 ops exit lands.
    operability_placeholder: str | None = None


class BakeoffInvocationOutcome(SchemaModel):
    """One candidate invoke result for a single bake-off page."""

    #: Predicted page graph when the invoke succeeded.
    prediction: BundlePage | None = None
    #: Wall-clock latency in milliseconds when measured.
    latency_ms: float | None = None
    #: Failure message when the invoke failed; ``None`` on success.
    failure: str | None = None


class BakeoffMatrixCell(SchemaModel):
    """One runner x page cell in the bake-off matrix artifact."""

    #: Runner that produced the prediction for this cell.
    runner_id: str
    #: Page identifier shared with gold.
    page_id: str
    #: Page-class cohort for this cell.
    page_class: PageClass
    #: EvaluationService score families when scoring succeeded.
    score_families: PageEvaluationSummary | None = None
    #: Invoke latency in milliseconds when measured.
    latency_ms: float | None = None
    #: Failure message when invoke or scoring failed; ``None`` on success.
    failure: str | None = None
    #: License scoring placeholder copied from the candidate.
    license_placeholder: str | None = None
    #: Cost scoring placeholder copied from the candidate.
    cost_placeholder: str | None = None
    #: Operability scoring placeholder copied from the candidate.
    operability_placeholder: str | None = None


class BakeoffMatrix(SchemaModel):
    """Reproducible bake-off matrix written as ``bakeoff-matrix-v1.json``."""

    #: Matrix schema version string.
    schema_version: str = BAKEOFF_MATRIX_SCHEMA_VERSION
    #: Candidates compared in this matrix (real runners in product schema).
    candidates: list[BakeoffCandidate] = Field(min_length=1)
    #: Per runner x page cells with scores, latency, and failure fields.
    cells: list[BakeoffMatrixCell] = Field(default_factory=list)
    #: Deferred Phase 5 exits (cost/license/ops/full held-out corpus).
    deferred: list[str] = Field(default_factory=lambda: list(DEFERRED_BAKEOFF_NOTES))


class BakeoffPageCase(SchemaModel):
    """One held-out page case for bake-off scoring."""

    #: Page identifier matching gold and predictions.
    page_id: str
    #: Page-class cohort for matrix grouping.
    page_class: PageClass
    #: Gold annotation slice for the page.
    gold: GoldPageAnnotation


class BakeoffRequest(SchemaModel):
    """In-memory bake-off request over candidates and page cases."""

    #: Candidates to compare (defaults should be olmocr + kraken).
    candidates: list[BakeoffCandidate] = Field(min_length=1)
    #: Held-out page cases to score.
    pages: list[BakeoffPageCase] = Field(min_length=1)


class BakeoffPageRef(SchemaModel):
    """Filesystem reference to one bake-off page gold annotation."""

    #: Page identifier matching gold and predictions.
    page_id: str
    #: Page-class cohort for matrix grouping.
    page_class: PageClass
    #: Posix path to ``GoldPageAnnotation`` JSON (relative to bundle root).
    gold_path: str


class BakeoffPredictionRef(SchemaModel):
    """Filesystem reference to one recorded prediction for a candidate."""

    #: Runner that produced the recorded prediction.
    runner_id: str
    #: Page identifier matching gold.
    page_id: str
    #: Posix path to ``BundlePage`` JSON (relative to bundle root).
    prediction_path: str
    #: Optional recorded latency in milliseconds.
    latency_ms: float | None = None
    #: Optional recorded failure (skips loading the prediction when set).
    failure: str | None = None


class BakeoffManifest(SchemaModel):
    """Operator manifest for offline/recorded ``wordwending bakeoff`` runs."""

    #: Candidates to compare.
    candidates: list[BakeoffCandidate] = Field(min_length=1)
    #: Page gold refs (relative paths resolved against ``--bundle-root``).
    pages: list[BakeoffPageRef] = Field(min_length=1)
    #: Recorded prediction refs for each candidate x page cell.
    predictions: list[BakeoffPredictionRef] = Field(default_factory=list)


def default_bakeoff_candidates() -> list[BakeoffCandidate]:
    """
    Return the ADR 0007 real candidates targeted by the Phase 5 matrix schema.

    Returns:
        ``olmocr`` and ``kraken`` candidates with deferred scoring placeholders.

    """
    placeholders = {
        "license_placeholder": "TBD",
        "cost_placeholder": "deferred",
        "operability_placeholder": "deferred",
    }
    return [
        BakeoffCandidate(runner_id="olmocr", **placeholders),
        BakeoffCandidate(runner_id="kraken", **placeholders),
    ]
