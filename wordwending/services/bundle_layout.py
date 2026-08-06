# Copyright (C) 2026 Chris Malek.
"""Spec 0002 document bundle tree writer and reader."""

from __future__ import annotations

import json
import shutil
from collections.abc import Mapping  # noqa: TC003
from itertools import chain
from pathlib import Path
from typing import Any

from wordwending.models import (
    BUNDLE_SCHEMA_VERSION,
    BundlePage,
    BundlePaths,
    DocumentBundle,
    DocumentBundleManifest,
    ExportSummary,
    OverlayState,
    PageBundleManifest,
    PageEvaluationSummary,
    ReviewEvent,
    RunnerReference,
    WitnessReference,
    page_dir_name,
)
from wordwending.services.document_export import DocumentExportService

#: Witness families that receive empty on-disk directories per page.
_WITNESS_FAMILIES = ("text", "layout", "style", "table")


def _safe_basename(value: str, *, label: str) -> str:
    """
    Reject path segments that are not bare basenames.

    Args:
        value: Caller-supplied path segment.

    Keyword Args:
        label: Field name used in error messages.

    Returns:
        The validated basename.

    Raises:
        ValueError: If ``value`` is empty, ``.`` / ``..``, or contains path
            separators.

    """
    if not value or value in {".", ".."} or "/" in value or "\\" in value:
        msg = f"unsafe {label} basename {value!r}: must be a bare filename"
        raise ValueError(msg)
    return value


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


def _needs_trailing_newline(path: Path) -> bool:
    r"""
    Return True when ``path`` exists, is non-empty, and does not end with ``\n``.

    Args:
        path: JSONL file path.

    Returns:
        Whether a separator newline should be written before appending.

    """
    if not path.exists() or path.stat().st_size == 0:
        return False
    with path.open("rb") as handle:
        handle.seek(-1, 2)
        return handle.read(1) != b"\n"


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


def _resolve_source_image_path(
    root: Path,
    paths: BundlePaths,
    page_number: int,
    source_page_image_path: str | None,
    prepared_image_path: str | None,
) -> str:
    """
    Choose the page manifest source image path.

    Prefer ``source/pages/`` when a source page image was copied or already
    exists on disk; otherwise fall back to the prepared image path.

    Args:
        root: Bundle root directory.
        paths: Path helpers for the bundle root.
        page_number: 1-based page index within the document bundle.
        source_page_image_path: Bundle-relative source page image when copied.
        prepared_image_path: Bundle-relative prepared image when copied or known.

    Returns:
        Bundle-relative path for ``PageBundleManifest.source_image_path``.

    Raises:
        ValueError: If multiple ``source/pages/{page:04d}.*`` files exist, or
            if no source or prepared image path can be resolved.

    """
    if source_page_image_path:
        return source_page_image_path
    pages_dir = paths.source_pages_dir()
    if pages_dir.is_dir():
        prefix = f"{page_number:04d}."
        matches = sorted(
            candidate
            for candidate in pages_dir.iterdir()
            if candidate.is_file() and candidate.name.startswith(prefix)
        )
        if len(matches) > 1:
            names = ", ".join(path.name for path in matches)
            msg = (
                f"ambiguous source page image for page {page_number}: "
                f"multiple files match {prefix}* ({names})"
            )
            raise ValueError(msg)
        if len(matches) == 1:
            return _relative_path(root, matches[0])
    if prepared_image_path:
        return prepared_image_path
    msg = (
        f"source_image_path required for page {page_number}: "
        "no source/pages image and no prepared image path"
    )
    raise ValueError(msg)


def _resolve_overlay_state_path(
    root: Path,
    paths: BundlePaths,
    page_number: int,
) -> str | None:
    """
    Return the overlay state manifest pointer when the artifact exists.

    Args:
        root: Bundle root directory.
        paths: Path helpers for the bundle root.
        page_number: 1-based page index within the document bundle.

    Returns:
        Bundle-relative path to ``current_state.json`` when present.

    """
    overlay_path = paths.overlay_state(page_number)
    if overlay_path.exists():
        return _relative_path(root, overlay_path)
    return None


def _rewrite_page_manifest(
    paths: BundlePaths,
    page_number: int,
    page_manifest: PageBundleManifest,
) -> None:
    """
    Atomically rewrite one page manifest.

    Side Effects:
        Replaces ``pages/page-NNNN/manifest.json``.

    Args:
        paths: Path helpers for the bundle root.
        page_number: 1-based page index within the document bundle.
        page_manifest: Manifest payload to persist.

    """
    _atomic_write_json(
        paths.page_manifest(page_number),
        page_manifest.model_dump(mode="json"),
    )


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

        Raises:
            ValueError: If ``bundle.pages`` contains duplicate ``page_number``
                values, or if a caller-supplied path segment is unsafe.

        """
        page_numbers = [page.page_number for page in bundle.pages]
        if len(page_numbers) != len(set(page_numbers)):
            msg = (
                "duplicate page_number values in document bundle: "
                f"{sorted(page_numbers)}"
            )
            raise ValueError(msg)

        paths = BundlePaths(root)
        root.mkdir(parents=True, exist_ok=True)
        paths.source_dir().mkdir(parents=True, exist_ok=True)
        paths.source_pages_dir().mkdir(parents=True, exist_ok=True)

        if source_files:
            for basename, source_path in source_files.items():
                safe_name = _safe_basename(basename, label="source_files")
                shutil.copy2(source_path, paths.source_dir() / safe_name)

        provenance_payload = {
            "bibliographic_provenance": bundle.bibliographic_provenance.model_dump(
                mode="json"
            ),
            "acquisition_provenance": bundle.acquisition_provenance.model_dump(
                mode="json"
            ),
        }
        _atomic_write_json(paths.source_provenance(), provenance_payload)

        source_page_image_paths: dict[int, str] = {}
        if source_page_images:
            for page_number, source_path in source_page_images.items():
                destination = paths.source_page_image(page_number, source_path.suffix)
                shutil.copy2(source_path, destination)
                source_page_image_paths[page_number] = _relative_path(root, destination)

        for page in bundle.pages:
            self._write_page_bundle(
                page=page,
                root=root,
                paths=paths,
                runner_set=bundle.run.runner_set,
                page_images=page_images,
                witness_files=witness_files,
                page_exports=page_exports,
                source_page_image_path=source_page_image_paths.get(page.page_number),
            )

        self._write_document_tail(bundle, paths)
        return self._build_document_manifest(bundle, paths)

    def write_document_exports(
        self,
        bundle: DocumentBundle,
        root: Path,
    ) -> DocumentBundle:
        """
        Write derived document export artifacts under ``exports/``.

        Side Effects:
            Atomically creates or replaces ``exports/bundle.json``,
            ``exports/rag.jsonl``, ``exports/stitched_chunks.jsonl``, and
            ``exports/document.md``. Does not modify overlay state or
            ``overlays/review_events.jsonl``.

        Args:
            bundle: Canonical accepted document export used as derivation input.
            root: Filesystem root for the document bundle tree.

        Returns:
            A copied ``DocumentBundle`` whose ``exports`` summary points at the
            four written artifact paths. The input ``bundle`` is not mutated.

        """
        paths = BundlePaths(root)
        paths.document_exports_dir().mkdir(parents=True, exist_ok=True)

        bundle_json_path = "exports/bundle.json"
        rag_jsonl_path = "exports/rag.jsonl"
        stitched_chunks_jsonl_path = "exports/stitched_chunks.jsonl"
        document_markdown_path = "exports/document.md"
        summary = ExportSummary(
            bundle_json_path=bundle_json_path,
            rag_jsonl_path=rag_jsonl_path,
            stitched_chunks_jsonl_path=stitched_chunks_jsonl_path,
            document_markdown_path=document_markdown_path,
        )
        exported = bundle.model_copy(update={"exports": summary})
        exporter = DocumentExportService()
        rag = exporter.build_rag_document(exported)
        markdown = exporter.render_markdown(exported)

        _atomic_write_json(
            root / bundle_json_path,
            exported.model_dump(mode="json"),
        )
        _atomic_write_text(
            root / rag_jsonl_path,
            self._jsonl_payload(
                [chunk.model_dump(mode="json") for chunk in rag.chunks]
            ),
        )
        _atomic_write_text(
            root / stitched_chunks_jsonl_path,
            self._jsonl_payload(
                [
                    chunk.model_dump(mode="json")
                    for chunk in rag.stitched_chunks
                ]
            ),
        )
        _atomic_write_text(
            root / document_markdown_path,
            markdown,
        )
        return exported

    @staticmethod
    def _jsonl_payload(records: list[dict[str, object]]) -> str:
        """
        Serialize JSON objects as JSONL with a trailing newline when nonempty.

        Args:
            records: JSON-serializable objects to emit one-per-line.

        Returns:
            Empty string when ``records`` is empty; otherwise newline-joined
            JSON lines ending with a trailing newline.

        """
        if not records:
            return ""
        return "".join(f"{json.dumps(record)}\n" for record in records)

    def _write_document_tail(
        self,
        bundle: DocumentBundle,
        paths: BundlePaths,
    ) -> None:
        """
        Write document-level evaluation and export scaffolding.

        Side Effects:
            Creates ``exports/`` and writes ``evaluation/summary.json``.

        Args:
            bundle: Canonical in-memory document export.
            paths: Path helpers for the bundle root.

        """
        paths.document_exports_dir().mkdir(parents=True, exist_ok=True)
        _atomic_write_json(
            paths.document_evaluation_summary(),
            bundle.evaluation_summary.model_dump(mode="json"),
        )

    def _build_document_manifest(
        self,
        bundle: DocumentBundle,
        paths: BundlePaths,
    ) -> DocumentBundleManifest:
        """
        Persist and return the document-level manifest.

        Side Effects:
            Writes ``manifest.json`` under the bundle root.

        Args:
            bundle: Canonical in-memory document export.
            paths: Path helpers for the bundle root.

        Returns:
            The written document manifest.

        """
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
        source_page_image_path: str | None = None,
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
            source_page_image_path: Bundle-relative source page image when copied.

        """
        page_number = page.page_number
        paths.page_dir(page_number).mkdir(parents=True, exist_ok=True)
        for family in _WITNESS_FAMILIES:
            paths.witnesses_dir(page_number, family).mkdir(parents=True, exist_ok=True)

        prepared_image_path = self._copy_prepared_page_image(
            page=page,
            root=root,
            paths=paths,
            page_images=page_images,
        )
        rewritten_witnesses = self._copy_witnesses(
            page=page,
            root=root,
            paths=paths,
            witness_files=witness_files,
        )
        graph_updates: dict[str, object] = {"witnesses": rewritten_witnesses}
        if prepared_image_path is not None:
            graph_updates["prepared_page"] = page.prepared_page.model_copy(
                update={"image_path": prepared_image_path}
            )
        page_for_graph = page.model_copy(update=graph_updates)
        graph_path = paths.page_graph(page_number)
        _atomic_write_json(graph_path, page_for_graph.model_dump(mode="json"))

        self._write_page_evaluation_and_manifest(
            page=page,
            root=root,
            paths=paths,
            runner_set=runner_set,
            rewritten_witnesses=rewritten_witnesses,
            prepared_image_path=prepared_image_path,
            source_page_image_path=source_page_image_path,
            graph_path=graph_path,
            page_exports=page_exports,
        )

    def _copy_prepared_page_image(
        self,
        *,
        page: BundlePage,
        root: Path,
        paths: BundlePaths,
        page_images: Mapping[str, Path] | None,
    ) -> str | None:
        """
        Copy one prepared page image when a source path is supplied.

        Keyword Args:
            page: Accepted page graph to persist.
            root: Bundle root directory.
            paths: Path helpers for the bundle root.
            page_images: Prepared image paths keyed by page id.

        Returns:
            Bundle-relative prepared image path when copied.

        """
        if not page_images or page.page_id not in page_images:
            return None
        source_path = page_images[page.page_id]
        image_dir = paths.page_image_dir(page.page_number)
        image_dir.mkdir(parents=True, exist_ok=True)
        destination = image_dir / source_path.name
        shutil.copy2(source_path, destination)
        return _relative_path(root, destination)

    def _write_page_evaluation_and_manifest(  # noqa: PLR0913
        self,
        *,
        page: BundlePage,
        root: Path,
        paths: BundlePaths,
        runner_set: list[RunnerReference],
        rewritten_witnesses: list[WitnessReference],
        prepared_image_path: str | None,
        source_page_image_path: str | None,
        graph_path: Path,
        page_exports: Mapping[str, Mapping[str, str]] | None,
    ) -> None:
        """
        Write page evaluation artifacts, exports, overlays, and manifest.

        Side Effects:
            Creates evaluation, export, overlay, and manifest files for one page.

        Keyword Args:
            page: Accepted page graph to persist.
            root: Bundle root directory.
            paths: Path helpers for the bundle root.
            runner_set: Document-level runner references.
            rewritten_witnesses: Witness references with bundle-relative paths.
            prepared_image_path: Bundle-relative prepared image path when present.
            source_page_image_path: Bundle-relative source page image when copied.
            graph_path: Absolute path to the page graph artifact.
            page_exports: Optional page export text keyed by page id.

        """
        page_number = page.page_number
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
                safe_name = _safe_basename(export_name, label="page_exports")
                _atomic_write_text(paths.page_export(page_number, safe_name), content)

        review_events_path = paths.review_events(page_number)
        review_events_path.parent.mkdir(parents=True, exist_ok=True)
        if not review_events_path.exists():
            review_events_path.write_text("", encoding="utf-8")

        prepared_fallback = prepared_image_path or page.prepared_page.image_path or None
        page_manifest = PageBundleManifest(
            schema_version=BUNDLE_SCHEMA_VERSION,
            page_id=page.page_id,
            page_number=page.page_number,
            source_image_path=_resolve_source_image_path(
                root,
                paths,
                page_number,
                source_page_image_path,
                prepared_fallback,
            ),
            executed_passes=_executed_passes(page, runner_set),
            witness_artifacts=rewritten_witnesses,
            graph_artifact_path=_relative_path(root, graph_path),
            evaluation_scores_path=_relative_path(root, scores_path),
            evaluation_flags_path=_relative_path(root, flags_path),
            overlay_state_path=_resolve_overlay_state_path(root, paths, page_number),
            review_events_path=_relative_path(root, review_events_path),
        )
        _rewrite_page_manifest(paths, page_number, page_manifest)

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

        Raises:
            ValueError: If ``witness_kind`` is not a Spec 0002 witness family,
                or if ``witness_id`` is not a bare basename.

        """
        rewritten: list[WitnessReference] = []
        for witness in page.witnesses:
            if witness.witness_kind not in _WITNESS_FAMILIES:
                msg = (
                    f"unsupported witness_kind {witness.witness_kind!r}; "
                    f"expected one of {_WITNESS_FAMILIES}"
                )
                raise ValueError(msg)
            safe_id = _safe_basename(witness.witness_id, label="witness_id")
            if witness_files and witness.witness_id in witness_files:
                source_path = witness_files[witness.witness_id]
                basename = source_path.name
            else:
                basename = Path(witness.artifact_path).name
            # Prefix with witness_id so same-basename artifacts cannot collide.
            filename = f"{safe_id}_{basename}"
            destination_dir = paths.witnesses_dir(
                page.page_number,
                witness.witness_kind,
            )
            relative_path = _relative_path(root, destination_dir / filename)
            if witness_files and witness.witness_id in witness_files:
                destination_dir.mkdir(parents=True, exist_ok=True)
                source_path = witness_files[witness.witness_id]
                shutil.copy2(source_path, destination_dir / filename)
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

    def append_review_events(
        self,
        root: Path,
        page_number: int,
        events: list[ReviewEvent],
    ) -> None:
        """
        Append JSONL review events; never rewrite prior lines.

        Side Effects:
            Creates/appends ``overlays/review_events.jsonl``. When an existing
            file is non-empty and lacks a trailing newline, writes one before
            appending so prior lines stay parseable.

        Args:
            root: Filesystem root for one document bundle tree.
            page_number: 1-based page index within the document bundle.
            events: Review events to append in order.

        """
        if not events:
            return
        paths = BundlePaths(root)
        review_events_path = paths.review_events(page_number)
        review_events_path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            json.dumps(event.model_dump(mode="json"), separators=(",", ":"))
            for event in events
        ]
        needs_newline = _needs_trailing_newline(review_events_path)
        with review_events_path.open("a", encoding="utf-8") as handle:
            if needs_newline:
                handle.write("\n")
            handle.write("\n".join(lines) + "\n")

    def write_overlay_state(
        self,
        root: Path,
        page_number: int,
        states: list[OverlayState],
    ) -> None:
        """
        Overwrite ``overlays/current_state.json`` deterministically.

        Side Effects:
            Atomically replaces ``overlays/current_state.json``. Updates the
            page ``manifest.json`` ``overlay_state_path`` pointer when a
            manifest exists, or creates a stub page manifest (plus empty
            ``review_events.jsonl``) when none exists yet.

        Args:
            root: Filesystem root for one document bundle tree.
            page_number: 1-based page index within the document bundle.
            states: Materialized overlay state for reviewed objects.

        """
        paths = BundlePaths(root)
        overlay_path = paths.overlay_state(page_number)
        payload = [state.model_dump(mode="json") for state in states]
        _atomic_write_json(overlay_path, payload)
        overlay_relative = _relative_path(root, overlay_path)

        review_events_path = paths.review_events(page_number)
        review_events_path.parent.mkdir(parents=True, exist_ok=True)
        if not review_events_path.exists():
            review_events_path.write_text("", encoding="utf-8")

        manifest_path = paths.page_manifest(page_number)
        if manifest_path.exists():
            page_manifest = PageBundleManifest.model_validate_json(
                manifest_path.read_text(encoding="utf-8")
            )
            updated = page_manifest.model_copy(
                update={"overlay_state_path": overlay_relative}
            )
        else:
            # Stub manifest so overlay presence is recorded before
            # write_document_bundle; full write replaces all other fields.
            updated = PageBundleManifest(
                schema_version=BUNDLE_SCHEMA_VERSION,
                page_id=page_dir_name(page_number),
                page_number=page_number,
                source_image_path="",
                graph_artifact_path=_relative_path(root, paths.page_graph(page_number)),
                overlay_state_path=overlay_relative,
                review_events_path=_relative_path(root, review_events_path),
            )
        _rewrite_page_manifest(paths, page_number, updated)

    def read_review_events(
        self,
        root: Path,
        page_number: int,
    ) -> list[dict[str, Any]]:
        """
        Read append-only review events for one page.

        Args:
            root: Filesystem root for one document bundle tree.
            page_number: 1-based page index within the document bundle.

        Returns:
            Parsed JSON objects for each non-blank JSONL line.

        Raises:
            ValueError: If a non-blank line is not valid JSON; the message
                names the review-events file and 1-based line number.

        """
        paths = BundlePaths(root)
        review_events_path = paths.review_events(page_number)
        if not review_events_path.exists():
            return []
        events: list[dict[str, Any]] = []
        for line_number, line in enumerate(
            review_events_path.read_text(encoding="utf-8").splitlines(),
            start=1,
        ):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                events.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                msg = (
                    f"invalid JSON in {review_events_path.name} "
                    f"line {line_number}: {exc.msg}"
                )
                raise ValueError(msg) from exc
        return events
