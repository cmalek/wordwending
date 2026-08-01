# Copyright (C) 2026 Chris Malek.
"""Spec 0002 on-disk bundle path helpers and manifest models."""

from __future__ import annotations

from datetime import datetime  # noqa: TC003
from pathlib import Path  # noqa: TC003

from pydantic import Field

from bochord.models.ocr import (
    AcquisitionProvenance,
    BibliographicProvenance,
    RunnerReference,
    SchemaModel,
    SourceDescriptor,
    WitnessReference,
)

#: Canonical bundle schema version written to document manifests.
BUNDLE_SCHEMA_VERSION = "bochord-bundle-v1"


def page_dir_name(page_number: int) -> str:
    """
    Return the stable page directory name for one 1-based page number.

    Args:
        page_number: 1-based page index within the document bundle.

    Returns:
        Directory basename such as ``page-0001``.

    """
    return f"page-{page_number:04d}"


class BundlePaths:
    """
    Relative path helpers for one document bundle root.

    Args:
        root: Filesystem root directory for one document bundle tree.

    """

    def __init__(self, root: Path) -> None:
        """
        Initialize path helpers for one bundle root.

        Args:
            root: Filesystem root directory for one document bundle tree.

        """
        #: Filesystem root directory for one document bundle tree.
        self.root = root

    @property
    def document_manifest(self) -> Path:
        """
        Return the document-level manifest path.

        Returns:
            Path to ``manifest.json`` under the bundle root.

        """
        return self.root / "manifest.json"

    def source_dir(self) -> Path:
        """
        Return the source artifact directory.

        Returns:
            Path to the ``source/`` directory.

        """
        return self.root / "source"

    def source_provenance(self) -> Path:
        """
        Return the source provenance manifest path.

        Returns:
            Path to ``source/provenance.json``.

        """
        return self.source_dir() / "provenance.json"

    def source_pages_dir(self) -> Path:
        """
        Return the directory holding source page images.

        Returns:
            Path to ``source/pages/``.

        """
        return self.source_dir() / "pages"

    def source_page_image(self, page_number: int, extension: str) -> Path:
        """
        Return the source page image path for one page number and extension.

        Args:
            page_number: 1-based page index within the source document.
            extension: Source image extension, with or without a leading dot.

        Returns:
            Path such as ``source/pages/0001.jp2``.

        """
        trimmed = extension.strip()
        if not trimmed:
            msg = "extension must not be empty"
            raise ValueError(msg)
        normalized = trimmed if trimmed.startswith(".") else f".{trimmed}"
        return self.source_pages_dir() / f"{page_number:04d}{normalized}"

    def page_dir(self, page_number: int) -> Path:
        """
        Return the page bundle directory for one page number.

        Args:
            page_number: 1-based page index within the document bundle.

        Returns:
            Path such as ``pages/page-0001``.

        """
        return self.root / "pages" / page_dir_name(page_number)

    def page_manifest(self, page_number: int) -> Path:
        """
        Return the page manifest path for one page number.

        Args:
            page_number: 1-based page index within the document bundle.

        Returns:
            Path such as ``pages/page-0001/manifest.json``.

        """
        return self.page_dir(page_number) / "manifest.json"

    def page_image_dir(self, page_number: int) -> Path:
        """
        Return the prepared page image directory for one page number.

        Args:
            page_number: 1-based page index within the document bundle.

        Returns:
            Path such as ``pages/page-0001/image``.

        """
        return self.page_dir(page_number) / "image"

    def witnesses_dir(self, page_number: int, family: str) -> Path:
        """
        Return the witness artifact directory for one page and family.

        Args:
            page_number: 1-based page index within the document bundle.
            family: Witness family such as ``text`` or ``layout``.

        Returns:
            Path such as ``pages/page-0001/witnesses/text``.

        """
        return self.page_dir(page_number) / "witnesses" / family

    def page_graph(self, page_number: int) -> Path:
        """
        Return the normalized page graph artifact path.

        Args:
            page_number: 1-based page index within the document bundle.

        Returns:
            Path such as ``pages/page-0001/graph/page_graph.json``.

        """
        return self.page_dir(page_number) / "graph" / "page_graph.json"

    def evaluation_scores(self, page_number: int) -> Path:
        """
        Return the page evaluation scores artifact path.

        Args:
            page_number: 1-based page index within the document bundle.

        Returns:
            Path such as ``pages/page-0001/evaluation/scores.json``.

        """
        return self.page_dir(page_number) / "evaluation" / "scores.json"

    def evaluation_flags(self, page_number: int) -> Path:
        """
        Return the page evaluation flags artifact path.

        Args:
            page_number: 1-based page index within the document bundle.

        Returns:
            Path such as ``pages/page-0001/evaluation/flags.json``.

        """
        return self.page_dir(page_number) / "evaluation" / "flags.json"

    def review_events(self, page_number: int) -> Path:
        """
        Return the append-only review event log path.

        Args:
            page_number: 1-based page index within the document bundle.

        Returns:
            Path such as ``pages/page-0001/overlays/review_events.jsonl``.

        """
        return self.page_dir(page_number) / "overlays" / "review_events.jsonl"

    def overlay_state(self, page_number: int) -> Path:
        """
        Return the current overlay state artifact path.

        Args:
            page_number: 1-based page index within the document bundle.

        Returns:
            Path such as ``pages/page-0001/overlays/current_state.json``.

        """
        return self.page_dir(page_number) / "overlays" / "current_state.json"

    def page_export(self, page_number: int, name: str) -> Path:
        """
        Return one page export artifact path.

        Args:
            page_number: 1-based page index within the document bundle.
            name: Export basename such as ``page.md``.

        Returns:
            Path such as ``pages/page-0001/exports/page.md``.

        """
        return self.page_dir(page_number) / "exports" / name

    def document_evaluation_summary(self) -> Path:
        """
        Return the document-level evaluation summary path.

        Returns:
            Path to ``evaluation/summary.json``.

        """
        return self.root / "evaluation" / "summary.json"

    def document_exports_dir(self) -> Path:
        """
        Return the document-level exports directory.

        Returns:
            Path to the ``exports/`` directory.

        """
        return self.root / "exports"


class DocumentBundleManifest(SchemaModel):
    """On-disk document manifest for one Spec 0002 bundle."""

    #: Schema version for this manifest JSON document.
    schema_version: str
    #: Stable document identifier.
    document_id: str
    #: Source identity for the input artifact(s).
    source: SourceDescriptor
    #: Bibliographic metadata kept with the document.
    bibliographic_provenance: BibliographicProvenance
    #: Acquisition metadata kept with the document.
    acquisition_provenance: AcquisitionProvenance
    #: UTC timestamp describing when the bundle was produced.
    run_timestamp_utc: datetime
    #: Digest of the run configuration excluding secrets.
    config_digest: str
    #: Runners executed while producing this bundle.
    runner_set: list[RunnerReference]
    #: Number of pages materialized in the bundle.
    page_count: int = Field(gt=0)
    #: Bundle layout schema version.
    bundle_schema_version: str


class PageBundleManifest(SchemaModel):
    """On-disk page manifest for one Spec 0002 page bundle."""

    #: Schema version for this manifest JSON document.
    schema_version: str
    #: Stable page identifier.
    page_id: str
    #: 1-based page index within the source document.
    page_number: int = Field(gt=0)
    #: Relative path to the source page image.
    source_image_path: str
    #: Runners executed for this page.
    executed_passes: list[RunnerReference] = Field(default_factory=list)
    #: Raw witness artifacts generated for this page.
    witness_artifacts: list[WitnessReference] = Field(default_factory=list)
    #: Relative path to the normalized page graph artifact.
    graph_artifact_path: str
    #: Relative path to evaluation scores when present.
    evaluation_scores_path: str | None = None
    #: Relative path to evaluation flags when present.
    evaluation_flags_path: str | None = None
    #: Relative path to overlay state when present.
    overlay_state_path: str | None = None
    #: Relative path to the append-only review event log.
    review_events_path: str
