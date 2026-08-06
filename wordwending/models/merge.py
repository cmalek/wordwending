# Copyright (C) 2026 Chris Malek.
"""Abstaining merge policy, witness input, and result contract models."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import Field

from wordwending.models.ocr import (
    BundlePage,
    CoordinateSpace,
    LineRecord,
    NoteRecord,
    ObjectProvenance,
    PreparedPage,
    RegionRecord,
    SchemaModel,
    SpanRecord,
)


class MergeFlagType(StrEnum):
    """Material merge disagreement categories emitted as review flags."""

    #: Normalized diplomatic text differs across witnesses.
    TEXT_DISAGREEMENT = "text_disagreement"
    #: One or more typography facets conflict across witnesses.
    TYPOGRAPHY_CONFLICT = "typography_conflict"
    #: Semantic text roles conflict across witnesses.
    ROLE_CONFLICT = "role_conflict"
    #: Multiple note-link candidates remain after merge.
    NOTE_LINK_AMBIGUOUS = "note_link_ambiguous"
    #: Competing layout scaffolds could not be reconciled.
    STRUCTURE_SCAFFOLD_CONFLICT = "structure_scaffold_conflict"
    #: Evidence was too weak to accept a derived value.
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"


class AlternateCandidate(SchemaModel):
    """One rejected or alternate merge interpretation kept in provenance."""

    #: Witness artifact that supplied this alternate value.
    witness_id: str
    #: Runner that emitted the witness supplying this alternate.
    runner_id: str
    #: Facet kind for the alternate payload (``text``, ``typography``, etc.).
    value_kind: str
    #: Small typed payload serialized as a plain mapping.
    value: dict[str, Any]
    #: Machine confidence reported for this alternate when available.
    machine_confidence: float | None = Field(default=None, ge=0, le=1)


class MergePolicy(SchemaModel):
    """Versioned deterministic merge precedence and acceptance thresholds."""

    #: Stable merge policy identifier.
    policy_id: str
    #: Semantic version of the merge contract.
    version: str
    #: Runner precedence for text; empty means abstain on text disagreement.
    runner_text_precedence: list[str] = Field(default_factory=list)
    #: Preferred runner order when choosing a structure scaffold.
    structure_scaffold_runner_ids: list[str] = Field(default_factory=list)
    #: Minimum merge confidence required to accept without abstaining.
    min_merge_confidence_to_accept: float = Field(default=0.6, ge=0, le=1)
    #: IoU threshold for aligning layout objects across witnesses.
    iou_match_threshold: float = Field(default=0.5, ge=0, le=1)
    #: Text normalization policy used when comparing and emitting text.
    text_normalization_policy_id: str = "text-norm-v1"


class PassWitnessPage(SchemaModel):
    """One runner's proposed page graph fragment for merge input."""

    #: Witness artifact identifier for this runner output.
    witness_id: str
    #: Runner that produced this witness fragment.
    runner_id: str
    #: Prepared-page identifier this witness aligns to.
    prepared_page_id: str
    #: Coordinate space for geometry in this witness fragment.
    coordinate_space: CoordinateSpace
    #: Region nodes proposed by this witness.
    regions: list[RegionRecord] = Field(default_factory=list)
    #: Line nodes proposed by this witness.
    lines: list[LineRecord] = Field(default_factory=list)
    #: Span nodes proposed by this witness.
    spans: list[SpanRecord] = Field(default_factory=list)
    #: Note nodes proposed by this witness.
    notes: list[NoteRecord] = Field(default_factory=list)
    #: Machine confidence for this witness page when available.
    machine_confidence: float | None = Field(default=None, ge=0, le=1)


class MergePageInput(SchemaModel):
    """Competing witness fragments prepared for single-page merge."""

    #: Stable page identifier under merge.
    page_id: str
    #: One-based page number within the source order.
    page_number: int
    #: Accepted prepared page variant all witnesses must align to.
    prepared_page: PreparedPage
    #: One or more runner witness fragments for this page.
    witnesses: list[PassWitnessPage] = Field(min_length=1)


class MergeFlag(SchemaModel):
    """One material merge disagreement surfaced for human review."""

    #: Stable flag identifier within the merge result.
    flag_id: str
    #: Disagreement category for this flag.
    flag_type: MergeFlagType
    #: Derived object identifiers affected by this flag.
    target_object_ids: list[str]
    #: Human-readable explanation of the disagreement.
    message: str


class MergePageResult(SchemaModel):
    """Accepted page graph plus merge flags and abstention state."""

    #: Accepted derived page graph for this merge.
    page: BundlePage
    #: Material disagreements emitted during merge.
    flags: list[MergeFlag] = Field(default_factory=list)
    #: Whether merge abstained from asserting full certainty.
    abstained: bool = False


ObjectProvenance.model_rebuild()
