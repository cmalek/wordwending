# Copyright (C) 2026 Chris Malek.
"""Tests for Spec 0002 bundle path helpers and manifest models."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest
from pydantic import ValidationError

from bochord.models import (
    BUNDLE_SCHEMA_VERSION,
    AcquisitionProvenance,
    BibliographicProvenance,
    BundlePaths,
    DocumentBundle,
    DocumentBundleManifest,
    PageBundleManifest,
    RunnerReference,
    SourceDescriptor,
    SourceType,
    WitnessReference,
    page_dir_name,
)
from bochord.services.bundle_layout import BundleLayoutService

FIXTURE_PATH = (
    Path(__file__).parent / "fixtures" / "bundle_layout" / "minimal_document.json"
)


def load_minimal_bundle() -> DocumentBundle:
    """Load the minimal DocumentBundle fixture."""
    return DocumentBundle.model_validate_json(FIXTURE_PATH.read_text(encoding="utf-8"))


def _write_minimal_inputs(
    tmp_path: Path,
) -> tuple[
    dict[str, Path],
    dict[int, Path],
    dict[str, Path],
    dict[str, Path],
]:
    """Create input files referenced by bundle layout write tests."""
    inputs = tmp_path / "inputs"
    inputs.mkdir(parents=True, exist_ok=True)
    source_pdf = inputs / "sample.pdf"
    source_pdf.write_bytes(b"%PDF-1.4 minimal")
    source_page = inputs / "page1.jp2"
    source_page.write_bytes(b"fake-jp2-bytes")
    prepared_image = inputs / "prepared.jp2"
    prepared_image.write_bytes(b"fake-prepared-bytes")
    witness_src = inputs / "olmocr-response.json"
    witness_src.write_text('{"text": "hello"}', encoding="utf-8")
    return (
        {"sample.pdf": source_pdf},
        {1: source_page},
        {"page-0001": prepared_image},
        {"wit-1": witness_src},
    )


def test_page_dir_name_is_zero_padded() -> None:
    assert page_dir_name(1) == "page-0001"
    assert page_dir_name(12) == "page-0012"


def test_bundle_paths_match_spec_0002_layout(tmp_path) -> None:
    paths = BundlePaths(tmp_path / "doc")
    assert paths.document_manifest == paths.root / "manifest.json"
    assert paths.source_dir() == paths.root / "source"
    assert paths.source_provenance() == paths.root / "source/provenance.json"
    assert paths.source_pages_dir() == paths.root / "source/pages"
    assert paths.source_page_image(1, ".jp2") == paths.root / "source/pages/0001.jp2"
    assert paths.source_page_image(1, "jp2") == paths.root / "source/pages/0001.jp2"
    assert paths.page_dir(1) == paths.root / "pages/page-0001"
    assert paths.page_manifest(1) == paths.root / "pages/page-0001/manifest.json"
    assert paths.page_image_dir(1) == paths.root / "pages/page-0001/image"
    assert paths.witnesses_dir(1, "text") == (
        paths.root / "pages/page-0001/witnesses/text"
    )
    assert paths.page_graph(1) == paths.root / "pages/page-0001/graph/page_graph.json"
    assert paths.evaluation_scores(1) == (
        paths.root / "pages/page-0001/evaluation/scores.json"
    )
    assert paths.evaluation_flags(1) == (
        paths.root / "pages/page-0001/evaluation/flags.json"
    )
    assert paths.review_events(1) == (
        paths.root / "pages/page-0001/overlays/review_events.jsonl"
    )
    assert paths.overlay_state(1) == (
        paths.root / "pages/page-0001/overlays/current_state.json"
    )
    assert paths.page_export(1, "page.md") == (
        paths.root / "pages/page-0001/exports/page.md"
    )
    assert paths.document_evaluation_summary() == paths.root / "evaluation/summary.json"
    assert paths.document_exports_dir() == paths.root / "exports"


def test_document_bundle_manifest_round_trip() -> None:
    timestamp = datetime(2026, 7, 31, tzinfo=UTC)
    manifest = DocumentBundleManifest(
        schema_version="1.0.0",
        document_id="doc-1",
        source=SourceDescriptor(
            source_id="src-1",
            source_type=SourceType.PDF,
            source_label="sample.pdf",
            original_path="sources/sample.pdf",
        ),
        bibliographic_provenance=BibliographicProvenance(
            title="Sample Work",
            authors=["Author"],
        ),
        acquisition_provenance=AcquisitionProvenance(
            acquisition_kind="local-scan",
            acquired_from="local",
        ),
        run_timestamp_utc=timestamp,
        config_digest="sha256:config",
        runner_set=[RunnerReference(runner_id="fixture")],
        page_count=1,
        bundle_schema_version=BUNDLE_SCHEMA_VERSION,
    )
    restored = DocumentBundleManifest.model_validate(manifest.model_dump(mode="json"))
    assert restored == manifest


def test_page_bundle_manifest_round_trip() -> None:
    manifest = PageBundleManifest(
        schema_version="1.0.0",
        page_id="page-0001",
        page_number=1,
        source_image_path="source/pages/0001.jp2",
        graph_artifact_path="pages/page-0001/graph/page_graph.json",
        review_events_path="pages/page-0001/overlays/review_events.jsonl",
        witness_artifacts=[
            WitnessReference(
                witness_id="wit-1",
                witness_kind="text",
                artifact_path="pages/page-0001/witnesses/text/olmocr.json",
                runner_id="olmocr",
                page_id="page-0001",
            )
        ],
    )
    restored = PageBundleManifest.model_validate(manifest.model_dump(mode="json"))
    assert restored == manifest


def test_document_bundle_manifest_rejects_non_positive_page_count() -> None:
    timestamp = datetime(2026, 7, 31, tzinfo=UTC)
    with pytest.raises(ValidationError):
        DocumentBundleManifest(
            schema_version="1.0.0",
            document_id="doc-1",
            source=SourceDescriptor(
                source_id="src-1",
                source_type=SourceType.PDF,
                source_label="sample.pdf",
                original_path="sources/sample.pdf",
            ),
            bibliographic_provenance=BibliographicProvenance(
                title="Sample Work",
                authors=["Author"],
            ),
            acquisition_provenance=AcquisitionProvenance(
                acquisition_kind="local-scan",
                acquired_from="local",
            ),
            run_timestamp_utc=timestamp,
            config_digest="sha256:config",
            runner_set=[RunnerReference(runner_id="fixture")],
            page_count=0,
            bundle_schema_version=BUNDLE_SCHEMA_VERSION,
        )


def test_page_bundle_manifest_rejects_non_positive_page_number() -> None:
    with pytest.raises(ValidationError):
        PageBundleManifest(
            schema_version="1.0.0",
            page_id="page-0000",
            page_number=0,
            source_image_path="source/pages/0001.jp2",
            graph_artifact_path="pages/page-0000/graph/page_graph.json",
            review_events_path="pages/page-0000/overlays/review_events.jsonl",
        )


def test_source_page_image_rejects_empty_extension(tmp_path) -> None:
    paths = BundlePaths(tmp_path / "doc")
    with pytest.raises(ValueError, match="extension must not be empty"):
        paths.source_page_image(1, "   ")


def test_write_document_bundle_creates_spec_tree(tmp_path) -> None:
    """Materialized tree matches Spec 0002 layout and manifest fields."""
    bundle = load_minimal_bundle()
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    source_files, source_page_images, page_images, witness_files = _write_minimal_inputs(
        tmp_path
    )

    manifest = service.write_document_bundle(
        bundle,
        root,
        source_files=source_files,
        source_page_images=source_page_images,
        page_images=page_images,
        witness_files=witness_files,
    )

    assert manifest.page_count == 1
    assert len(manifest.runner_set) == 1
    assert manifest.runner_set[0].runner_id == "olmocr"
    assert (root / "manifest.json").exists()
    assert (root / "source" / "sample.pdf").exists()
    assert (root / "source" / "pages" / "0001.jp2").exists()
    assert (root / "pages" / "page-0001" / "image" / "prepared.jp2").exists()
    assert not (root / "pages" / "page-0001" / "image" / "page.png").exists()
    assert (
        root / "pages" / "page-0001" / "witnesses" / "text" / "olmocr-response.json"
    ).exists()
    for family in ("text", "layout", "style", "table"):
        assert (root / "pages" / "page-0001" / "witnesses" / family).is_dir()

    page_manifest = service.read_page_manifest(root, 1)
    assert page_manifest.source_image_path == "pages/page-0001/image/prepared.jp2"
    assert page_manifest.overlay_state_path is None
    assert len(page_manifest.executed_passes) == 1
    assert page_manifest.executed_passes[0].runner_id == "olmocr"
    assert page_manifest.witness_artifacts[0].artifact_path == (
        "pages/page-0001/witnesses/text/olmocr-response.json"
    )

    graph = service.read_page_graph(root, 1)
    assert len(graph.spans) == 1
    assert graph.spans[0].text_diplomatic == "hello"
    assert len(graph.notes) == 1
    assert graph.notes[0].text_diplomatic == "footnote text"
    assert graph.witnesses[0].artifact_path == (
        "pages/page-0001/witnesses/text/olmocr-response.json"
    )

    review_events_path = root / "pages" / "page-0001" / "overlays" / "review_events.jsonl"
    assert review_events_path.exists()
    assert review_events_path.read_text(encoding="utf-8") == ""

    scores = json.loads(
        (root / "pages" / "page-0001" / "evaluation" / "scores.json").read_text(
            encoding="utf-8"
        )
    )
    assert scores == bundle.pages[0].evaluation_summary.model_dump(mode="json")

    doc_eval = json.loads(
        (root / "evaluation" / "summary.json").read_text(encoding="utf-8")
    )
    assert doc_eval == bundle.evaluation_summary.model_dump(mode="json")

    flags = json.loads(
        (root / "pages" / "page-0001" / "evaluation" / "flags.json").read_text(
            encoding="utf-8"
        )
    )
    assert flags["flags"][0]["flag_id"] == "flag-text-1"


def test_write_document_bundle_refreshes_graph_on_rerun(tmp_path) -> None:
    """Second write overwrites recomputable graph content."""
    bundle = load_minimal_bundle()
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    source_files, source_page_images, page_images, witness_files = _write_minimal_inputs(
        tmp_path
    )

    service.write_document_bundle(
        bundle,
        root,
        source_files=source_files,
        source_page_images=source_page_images,
        page_images=page_images,
        witness_files=witness_files,
    )

    updated = bundle.model_copy(deep=True)
    updated.pages[0].spans[0].text_diplomatic = "updated text"
    service.write_document_bundle(
        updated,
        root,
        source_files=source_files,
        source_page_images=source_page_images,
        page_images=page_images,
        witness_files=witness_files,
    )

    graph = service.read_page_graph(root, 1)
    assert graph.spans[0].text_diplomatic == "updated text"


def test_write_document_bundle_preserves_review_events_jsonl(tmp_path) -> None:
    """Second write must not truncate a pre-seeded review_events.jsonl."""
    bundle = load_minimal_bundle()
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    source_files, source_page_images, page_images, witness_files = _write_minimal_inputs(
        tmp_path
    )
    review_path = root / "pages" / "page-0001" / "overlays" / "review_events.jsonl"
    seeded = b'{"event_id":"evt-seeded"}\n'

    service.write_document_bundle(
        bundle,
        root,
        source_files=source_files,
        source_page_images=source_page_images,
        page_images=page_images,
        witness_files=witness_files,
    )
    review_path.parent.mkdir(parents=True, exist_ok=True)
    review_path.write_bytes(seeded)

    service.write_document_bundle(
        bundle,
        root,
        source_files=source_files,
        source_page_images=source_page_images,
        page_images=page_images,
        witness_files=witness_files,
    )

    assert review_path.read_bytes() == seeded


def test_read_document_manifest_round_trip(tmp_path) -> None:
    """Written document manifest round-trips through the reader."""
    bundle = load_minimal_bundle()
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    source_files, source_page_images, page_images, witness_files = _write_minimal_inputs(
        tmp_path
    )

    written = service.write_document_bundle(
        bundle,
        root,
        source_files=source_files,
        source_page_images=source_page_images,
        page_images=page_images,
        witness_files=witness_files,
    )
    restored = service.read_document_manifest(root)

    assert restored == written
    assert restored.schema_version == BUNDLE_SCHEMA_VERSION
    assert restored.bundle_schema_version == BUNDLE_SCHEMA_VERSION


def test_write_document_bundle_rewrites_witness_paths_without_files(tmp_path) -> None:
    """Page manifest rewrites witness paths even when no file is copied."""
    bundle = load_minimal_bundle()
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    source_files, source_page_images, page_images, _witness_files = _write_minimal_inputs(
        tmp_path
    )
    pre_write_path = bundle.pages[0].witnesses[0].artifact_path
    assert pre_write_path.endswith("olmocr-response.json")

    service.write_document_bundle(
        bundle,
        root,
        source_files=source_files,
        source_page_images=source_page_images,
        page_images=page_images,
        witness_files=None,
    )

    page_manifest = service.read_page_manifest(root, 1)
    assert page_manifest.witness_artifacts[0].artifact_path == (
        "pages/page-0001/witnesses/text/olmocr-response.json"
    )
    assert page_manifest.witness_artifacts[0].artifact_path.startswith("pages/")

    graph = service.read_page_graph(root, 1)
    assert graph.witnesses[0].artifact_path == (
        "pages/page-0001/witnesses/text/olmocr-response.json"
    )


def test_write_document_bundle_writes_page_exports(tmp_path) -> None:
    """Optional page export text files land under pages/page-NNNN/exports/."""
    bundle = load_minimal_bundle()
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    source_files, source_page_images, page_images, witness_files = _write_minimal_inputs(
        tmp_path
    )

    service.write_document_bundle(
        bundle,
        root,
        source_files=source_files,
        source_page_images=source_page_images,
        page_images=page_images,
        witness_files=witness_files,
        page_exports={"page-0001": {"reading.txt": "hello"}},
    )

    export_path = root / "pages" / "page-0001" / "exports" / "reading.txt"
    assert export_path.exists()
    assert export_path.read_text(encoding="utf-8") == "hello"
