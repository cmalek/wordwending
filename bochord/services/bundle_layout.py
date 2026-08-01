# Copyright (C) 2026 Chris Malek.
"""Spec 0002 document bundle tree writer and reader."""

from __future__ import annotations

import json
import shutil
from collections.abc import Mapping  # noqa: TC003
from itertools import chain
from pathlib import Path  # noqa: TC003

from bochord.models import (
    BUNDLE_SCHEMA_VERSION,
    BundlePage,
    BundlePaths,
    DocumentBundle,
    DocumentBundleManifest,
    PageBundleManifest,
    PageEvaluationSummary,
    RunnerReference,
    WitnessReference,
)

#: Witness families that receive empty on-disk directories per page.
_WITNESS_FAMILIES = ("text", "layout", "style", "table")


def _atomic_write_text(path: Path, payload: str) -> None:
    """
    Atomically write ``payload`` to ``path`` via a sibling temporary file.

    Side Effects:
        Creates parent directories and replaces ``path`` on success.

    Args:
        path: Destination file path.
        payload: UTF-8 text to persist.

    """
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(path.suffix + ".tmp")
    try:
        temp_path.write_text(payload, encoding="utf-8")
        temp_path.replace(path)
    except Exception:
        if temp_path.exists():
            temp_path.unlink()
        raise


def _atomic_write_json(path: Path, payload: object) -> None:
    """
    Atomically write one JSON document to ``path``.

    Side Effects:
        Creates parent directories and replaces ``path`` on success.

    Args:
        path: Destination file path.
        payload: JSON-serializable object to persist.

    """
    _atomic_write_text(path, json.dumps(payload, indent=2))


def _relative_path(root: Path, path: Path) -> str:
    """
    Return ``path`` relative to ``root`` without a leading ``./``.

    Args:
        root: Bundle root directory.
        path: Absolute or root-relative path.

    Returns:
        POSIX-style relative path string.

    """
    return path.relative_to(root).as_posix()


def _collect_page_flags(summary: PageEvaluationSummary) -> list[dict[str, object]]:
    """
    Gather evaluation flags from all page summary families.

    Args:
        summary: Per-page evaluation summary.

    Returns:
        Combined flag payloads suitable for ``evaluation/flags.json``.

    """
    flags: list[dict[str, object]] = [
        flag.model_dump(mode="json")
        for flag in chain(
            summary.text.flags,
            summary.structure.flags,
            summary.style.typography.flags,
            summary.style.note_linkage.flags,
        )
    ]
    return flags


def _executed_passes(
    page: BundlePage,
    runner_set: list[RunnerReference],
) -> list[RunnerReference]:
    """
    Derive unique runner references for witnesses emitted on one page.

    Args:
        page: Accepted page graph.
        runner_set: Document-level runner references.

    Returns:
        Runners from ``runner_set`` whose ``runner_id`` appears on page witnesses.

    """
    witness_runner_ids = {witness.runner_id for witness in page.witnesses}
    seen: set[str] = set()
    executed: list[RunnerReference] = []
    for runner in runner_set:
        if runner.runner_id in witness_runner_ids and runner.runner_id not in seen:
            seen.add(runner.runner_id)
            executed.append(runner)
    return executed


class BundleLayoutService:
    """Write and read Spec 0002 document bundle trees."""

    def write_document_bundle(  # noqa: PLR0913
        self,
        bundle: DocumentBundle,
        root: Path,
        *,
        source_files: Mapping[str, Path] | None = None,
        source_page_images: Mapping[int, Path] | None = None,
        page_images: Mapping[str, Path] | None = None,
        witness_files: Mapping[str, Path] | None = None,
        page_exports: Mapping[str, Mapping[str, str]] | None = None,
    ) -> DocumentBundleManifest:
        """
        Materialize the on-disk tree (recomputable layers only).

        Side Effects:
            Creates directories and writes JSON/text/image copies under ``root``.
            Creates empty ``overlays/review_events.jsonl`` if missing; never
            truncates an existing events file. Does not write overlay state
            or review event payloads (Task 3 owns those).

        Args:
            bundle: Canonical in-memory document export.
            root: Filesystem root for the bundle tree.

        Keyword Args:
            source_files: Destination basenames under ``source/`` mapped to
                local source artifact paths.
            source_page_images: 1-based page numbers mapped to raw source page
                image paths copied into ``source/pages/``.
            page_images: Page ids mapped to prepared image paths copied into
                ``pages/page-NNNN/image/`` preserving basename and extension.
            witness_files: Witness ids mapped to raw witness artifact paths.
            page_exports: Page ids mapped to export basenames and text content.

        Returns:
            The written document manifest.

        """
        paths = BundlePaths(root)
        root.mkdir(parents=True, exist_ok=True)
        paths.source_dir().mkdir(parents=True, exist_ok=True)
        paths.source_pages_dir().mkdir(parents=True, exist_ok=True)

        if source_files:
            for basename, source_path in source_files.items():
                shutil.copy2(source_path, paths.source_dir() / basename)

        provenance_payload = {
            "bibliographic_provenance": bundle.bibliographic_provenance.model_dump(
                mode="json"
            ),
            "acquisition_provenance": bundle.acquisition_provenance.model_dump(
                mode="json"
            ),
        }
        _atomic_write_json(paths.source_provenance(), provenance_payload)

        if source_page_images:
            for page_number, source_path in source_page_images.items():
                destination = paths.source_page_image(page_number, source_path.suffix)
                shutil.copy2(source_path, destination)

        for page in bundle.pages:
            self._write_page_bundle(
                page=page,
                root=root,
                paths=paths,
                runner_set=bundle.run.runner_set,
                page_images=page_images,
                witness_files=witness_files,
                page_exports=page_exports,
            )

        paths.document_exports_dir().mkdir(parents=True, exist_ok=True)
        _atomic_write_json(
            paths.document_evaluation_summary(),
            bundle.evaluation_summary.model_dump(mode="json"),
        )

        document_manifest = DocumentBundleManifest(
            schema_version=BUNDLE_SCHEMA_VERSION,
            document_id=bundle.document_id,
            source=bundle.source,
            bibliographic_provenance=bundle.bibliographic_provenance,
            acquisition_provenance=bundle.acquisition_provenance,
            run_timestamp_utc=bundle.run.run_timestamp_utc,
            config_digest=bundle.run.config_digest,
            runner_set=bundle.run.runner_set,
            page_count=len(bundle.pages),
            bundle_schema_version=BUNDLE_SCHEMA_VERSION,
        )
        _atomic_write_json(
            paths.document_manifest,
            document_manifest.model_dump(mode="json"),
        )
        return document_manifest

    def _write_page_bundle(  # noqa: PLR0913
        self,
        *,
        page: BundlePage,
        root: Path,
        paths: BundlePaths,
        runner_set: list[RunnerReference],
        page_images: Mapping[str, Path] | None,
        witness_files: Mapping[str, Path] | None,
        page_exports: Mapping[str, Mapping[str, str]] | None,
    ) -> None:
        """
        Write one page bundle subtree.

        Side Effects:
            Creates directories and writes page artifacts under ``root``.

        Keyword Args:
            page: Accepted page graph to persist.
            root: Bundle root directory.
            paths: Path helpers for the bundle root.
            runner_set: Document-level runner references.
            page_images: Prepared image paths keyed by page id.
            witness_files: Witness artifact paths keyed by witness id.
            page_exports: Optional page export text keyed by page id.

        """
        page_number = page.page_number
        paths.page_dir(page_number).mkdir(parents=True, exist_ok=True)
        for family in _WITNESS_FAMILIES:
            paths.witnesses_dir(page_number, family).mkdir(parents=True, exist_ok=True)

        prepared_image_path: str | None = None
        if page_images and page.page_id in page_images:
            source_path = page_images[page.page_id]
            image_dir = paths.page_image_dir(page_number)
            image_dir.mkdir(parents=True, exist_ok=True)
            destination = image_dir / source_path.name
            shutil.copy2(source_path, destination)
            prepared_image_path = _relative_path(root, destination)

        rewritten_witnesses = self._copy_witnesses(
            page=page,
            root=root,
            paths=paths,
            witness_files=witness_files,
        )

        graph_path = paths.page_graph(page_number)
        _atomic_write_json(graph_path, page.model_dump(mode="json"))

        scores_path = paths.evaluation_scores(page_number)
        _atomic_write_json(
            scores_path,
            page.evaluation_summary.model_dump(mode="json"),
        )

        flags_path = paths.evaluation_flags(page_number)
        _atomic_write_json(
            flags_path,
            {"flags": _collect_page_flags(page.evaluation_summary)},
        )

        if page_exports and page.page_id in page_exports:
            for export_name, content in page_exports[page.page_id].items():
                _atomic_write_text(paths.page_export(page_number, export_name), content)

        review_events_path = paths.review_events(page_number)
        review_events_path.parent.mkdir(parents=True, exist_ok=True)
        if not review_events_path.exists():
            review_events_path.write_text("", encoding="utf-8")

        page_manifest = PageBundleManifest(
            schema_version=BUNDLE_SCHEMA_VERSION,
            page_id=page.page_id,
            page_number=page.page_number,
            source_image_path=prepared_image_path or "",
            executed_passes=_executed_passes(page, runner_set),
            witness_artifacts=rewritten_witnesses,
            graph_artifact_path=_relative_path(root, graph_path),
            evaluation_scores_path=_relative_path(root, scores_path),
            evaluation_flags_path=_relative_path(root, flags_path),
            overlay_state_path=None,
            review_events_path=_relative_path(root, review_events_path),
        )
        _atomic_write_json(
            paths.page_manifest(page_number),
            page_manifest.model_dump(mode="json"),
        )

    def _copy_witnesses(
        self,
        *,
        page: BundlePage,
        root: Path,
        paths: BundlePaths,
        witness_files: Mapping[str, Path] | None,
    ) -> list[WitnessReference]:
        """
        Copy witness artifacts and rewrite in-bundle relative paths.

        Keyword Args:
            page: Accepted page graph containing witness references.
            root: Bundle root directory.
            paths: Path helpers for the bundle root.
            witness_files: Witness artifact paths keyed by witness id.

        Returns:
            Witness references with bundle-relative ``artifact_path`` values.

        """
        rewritten: list[WitnessReference] = []
        for witness in page.witnesses:
            relative_path = witness.artifact_path
            if witness_files and witness.witness_id in witness_files:
                source_path = witness_files[witness.witness_id]
                destination_dir = paths.witnesses_dir(
                    page.page_number,
                    witness.witness_kind,
                )
                destination_dir.mkdir(parents=True, exist_ok=True)
                destination = destination_dir / source_path.name
                shutil.copy2(source_path, destination)
                relative_path = _relative_path(root, destination)
            rewritten.append(
                witness.model_copy(update={"artifact_path": relative_path})
            )
        return rewritten

    def read_document_manifest(self, root: Path) -> DocumentBundleManifest:
        """
        Read the document-level manifest from one bundle root.

        Args:
            root: Filesystem root for one document bundle tree.

        Returns:
            Parsed document manifest.

        """
        paths = BundlePaths(root)
        return DocumentBundleManifest.model_validate_json(
            paths.document_manifest.read_text(encoding="utf-8")
        )

    def read_page_manifest(self, root: Path, page_number: int) -> PageBundleManifest:
        """
        Read one page manifest from a bundle root.

        Args:
            root: Filesystem root for one document bundle tree.
            page_number: 1-based page index within the document bundle.

        Returns:
            Parsed page manifest.

        """
        paths = BundlePaths(root)
        return PageBundleManifest.model_validate_json(
            paths.page_manifest(page_number).read_text(encoding="utf-8")
        )

    def read_page_graph(self, root: Path, page_number: int) -> BundlePage:
        """
        Read one normalized page graph artifact.

        Args:
            root: Filesystem root for one document bundle tree.
            page_number: 1-based page index within the document bundle.

        Returns:
            Parsed page graph.

        """
        paths = BundlePaths(root)
        return BundlePage.model_validate_json(
            paths.page_graph(page_number).read_text(encoding="utf-8")
        )
