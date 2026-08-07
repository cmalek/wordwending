# Copyright (C) 2026 Chris Malek.
"""Assemble request models: raw witness refs and per-page assemble inputs."""

from __future__ import annotations

from pydantic import Field

from wordwending.models.ocr import (
    CoordinateSpace,
    PreparedPage,
    SchemaModel,
)


class RawWitnessRef(SchemaModel):
    """
    Raw persisted witness artifact reference for one assemble page.

    Paths are relative posix strings resolved against the assemble
    ``bundle_root`` (or absolute when already absolute) at the orchestrator
    call site before adaptation.
    """

    #: Witness artifact identifier for provenance and bundle layout.
    witness_id: str
    #: Runner that produced this raw witness.
    runner_id: str
    #: Posix path strings relative to bundle_root (or absolute); min one entry.
    artifact_paths: list[str] = Field(min_length=1)
    #: Coordinate space for provisional adapt geometry.
    coordinate_space: CoordinateSpace


class AssemblePageRequest(SchemaModel):
    """One page's prepared input plus raw witness refs for assemble."""

    #: Stable page identifier under the document bundle.
    page_id: str
    #: One-based page number within the source order.
    page_number: int
    #: Accepted prepared page variant all witnesses must align to.
    prepared_page: PreparedPage
    #: Raw witness refs to adapt before merge (Wave A: exactly one).
    raw_witnesses: list[RawWitnessRef] = Field(min_length=1)
