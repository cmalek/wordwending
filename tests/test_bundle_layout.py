# Copyright (C) 2026 Chris Malek.
"""Tests for Spec 0002 bundle path helpers and manifest models."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest
from pydantic import ValidationError

from wordwending.models import (
    BUNDLE_SCHEMA_VERSION,
    AcceptReviewEvent,
    AcquisitionProvenance,
    BibliographicProvenance,
    BundlePaths,
    DocumentBundle,
    DocumentBundleManifest,
    OverlayState,
    PageBundleManifest,
    PageOverlay,
    RagChunk,
    ReviewDimension,
    ReviewScope,
    RunnerReference,
    SourceDescriptor,
    SourceType,
    StitchedChunk,
    TrustState,
    WitnessReference,
    page_dir_name,
)
from wordwending.services.bundle_layout import (
    BundleLayoutService,
    _resolve_source_image_path,
)
from wordwending.services.document_export import DocumentExportService

FIXTURE_PATH = (
    Path(__file__).parent / "fixtures" / "bundle_layout" / "minimal_document.json"
)
EXPORT_FIXTURE_PATH = (
    Path(__file__).parent / "fixtures" / "exports" / "minimal-bundle.json"
)
OVERLAY_V1_FIXTURE = (
    Path(__file__).parent / "fixtures" / "review_overlay" / "page-overlay-v1.json"
)
EXPORT_MODELS_FIXTURES = Path(__file__).parent / "fixtures" / "export_models"
DOCUMENT_BUNDLE_V1_FIXTURE = EXPORT_MODELS_FIXTURES / "document-bundle-v1.json"


def load_minimal_bundle() -> DocumentBundle:
    """Load the minimal DocumentBundle fixture."""
    return DocumentBundle.model_validate_json(FIXTURE_PATH.read_text(encoding="utf-8"))


def load_export_minimal_bundle() -> DocumentBundle:
    """Load the compact export-fixture DocumentBundle."""
    return DocumentBundle.model_validate_json(
        EXPORT_FIXTURE_PATH.read_text(encoding="utf-8")
    )


def load_frozen_document_bundle_v1() -> DocumentBundle:
    """Load the frozen document-bundle-v1 contract fixture."""
    return DocumentBundle.model_validate_json(
        DOCUMENT_BUNDLE_V1_FIXTURE.read_text(encoding="utf-8")
    )


def _accept_review_event(event_id: str) -> AcceptReviewEvent:
    """Build one minimal accept review event for bundle overlay tests."""
    return AcceptReviewEvent(
        event_id=event_id,
        task_id="task-1",
        target_object_id="note-1",
        target_scope=ReviewScope.NOTE,
        review_dimensions=[ReviewDimension.NOTE_LINKAGE],
        base_run_id="run-1",
        base_graph_revision="graph-1",
        guideline_version="review-v1",
        prior_trust_state=TrustState.MACHINE,
        new_trust_state=TrustState.REVIEWED,
        operator_id="editor-1",
        timestamp_utc=datetime(2026, 7, 26, tzinfo=UTC),
    )


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
    assert paths.pending_tasks_path(1) == (
        paths.root / "pages/page-0001/overlays/pending_tasks.json"
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
    source_files, source_page_images, page_images, witness_files = (
        _write_minimal_inputs(tmp_path)
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
        root
        / "pages"
        / "page-0001"
        / "witnesses"
        / "text"
        / "wit-1_olmocr-response.json"
    ).exists()
    for family in ("text", "layout", "style", "table"):
        assert (root / "pages" / "page-0001" / "witnesses" / family).is_dir()

    page_manifest = service.read_page_manifest(root, 1)
    assert page_manifest.source_image_path == "source/pages/0001.jp2"
    assert page_manifest.overlay_state_path is None
    assert len(page_manifest.executed_passes) == 1
    assert page_manifest.executed_passes[0].runner_id == "olmocr"
    assert page_manifest.witness_artifacts[0].artifact_path == (
        "pages/page-0001/witnesses/text/wit-1_olmocr-response.json"
    )

    graph = service.read_page_graph(root, 1)
    assert len(graph.spans) == 1
    assert graph.spans[0].text_diplomatic == "hello"
    assert len(graph.notes) == 1
    assert graph.notes[0].text_diplomatic == "footnote text"
    assert graph.prepared_page.image_path == "pages/page-0001/image/prepared.jp2"
    assert graph.witnesses[0].artifact_path == (
        "pages/page-0001/witnesses/text/wit-1_olmocr-response.json"
    )

    review_events_path = (
        root / "pages" / "page-0001" / "overlays" / "review_events.jsonl"
    )
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
    source_files, source_page_images, page_images, witness_files = (
        _write_minimal_inputs(tmp_path)
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
    source_files, source_page_images, page_images, witness_files = (
        _write_minimal_inputs(tmp_path)
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
    source_files, source_page_images, page_images, witness_files = (
        _write_minimal_inputs(tmp_path)
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
    source_files, source_page_images, page_images, _witness_files = (
        _write_minimal_inputs(tmp_path)
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
        "pages/page-0001/witnesses/text/wit-1_olmocr-response.json"
    )
    assert page_manifest.witness_artifacts[0].artifact_path.startswith("pages/")

    graph = service.read_page_graph(root, 1)
    assert graph.witnesses[0].artifact_path == (
        "pages/page-0001/witnesses/text/wit-1_olmocr-response.json"
    )


def test_write_document_bundle_writes_page_exports(tmp_path) -> None:
    """Optional page export text files land under pages/page-NNNN/exports/."""
    bundle = load_minimal_bundle()
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    source_files, source_page_images, page_images, witness_files = (
        _write_minimal_inputs(tmp_path)
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


def test_append_review_events_preserves_order_and_grows_file(tmp_path) -> None:
    """Append-only JSONL keeps prior lines and grows monotonically."""
    bundle = load_minimal_bundle()
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    source_files, source_page_images, page_images, witness_files = (
        _write_minimal_inputs(tmp_path)
    )
    service.write_document_bundle(
        bundle,
        root,
        source_files=source_files,
        source_page_images=source_page_images,
        page_images=page_images,
        witness_files=witness_files,
    )

    event_a = _accept_review_event("evt-a")
    event_b = _accept_review_event("evt-b")
    review_path = root / "pages" / "page-0001" / "overlays" / "review_events.jsonl"

    service.append_review_events(root, 1, [event_a])
    size_after_a = review_path.stat().st_size
    assert size_after_a > 0

    service.append_review_events(root, 1, [event_b])
    size_after_b = review_path.stat().st_size
    assert size_after_b > size_after_a

    events = service.read_review_events(root, 1)
    assert [event["event_id"] for event in events] == ["evt-a", "evt-b"]


def test_write_document_bundle_after_append_does_not_rewrite_jsonl(tmp_path) -> None:
    """Recomputing the bundle must not truncate appended review history."""
    bundle = load_minimal_bundle()
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    source_files, source_page_images, page_images, witness_files = (
        _write_minimal_inputs(tmp_path)
    )
    service.write_document_bundle(
        bundle,
        root,
        source_files=source_files,
        source_page_images=source_page_images,
        page_images=page_images,
        witness_files=witness_files,
    )

    event = _accept_review_event("evt-append")
    service.append_review_events(root, 1, [event])
    review_path = root / "pages" / "page-0001" / "overlays" / "review_events.jsonl"
    bytes_after_append = review_path.read_bytes()

    service.write_document_bundle(
        bundle,
        root,
        source_files=source_files,
        source_page_images=source_page_images,
        page_images=page_images,
        witness_files=witness_files,
    )

    assert review_path.read_bytes() == bytes_after_append
    assert service.read_review_events(root, 1)[0]["event_id"] == "evt-append"


def test_overlay_v1_bundle_rerun_preserves_review_events_and_state(
    tmp_path,
) -> None:
    """Rewriting bundle after overlay_v1 write keeps JSONL and state intact."""
    overlay = PageOverlay.model_validate_json(
        OVERLAY_V1_FIXTURE.read_text(encoding="utf-8")
    )
    bundle = load_minimal_bundle()
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    source_files, source_page_images, page_images, witness_files = (
        _write_minimal_inputs(tmp_path)
    )
    service.write_document_bundle(
        bundle,
        root,
        source_files=source_files,
        source_page_images=source_page_images,
        page_images=page_images,
        witness_files=witness_files,
    )

    service.append_review_events(root, 1, overlay.review_events)
    service.write_overlay_state(root, 1, overlay.current_state)
    review_path = root / "pages" / "page-0001" / "overlays" / "review_events.jsonl"
    state_path = root / "pages" / "page-0001" / "overlays" / "current_state.json"
    review_bytes = review_path.read_bytes()
    state_bytes = state_path.read_bytes()

    service.write_document_bundle(
        bundle,
        root,
        source_files=source_files,
        source_page_images=source_page_images,
        page_images=page_images,
        witness_files=witness_files,
    )

    page_manifest = service.read_page_manifest(root, 1)
    assert review_path.read_bytes() == review_bytes
    assert state_path.read_bytes() == state_bytes
    assert page_manifest.overlay_state_path == (
        "pages/page-0001/overlays/current_state.json"
    )
    assert page_manifest.review_events_path == (
        "pages/page-0001/overlays/review_events.jsonl"
    )


def test_write_overlay_state_updates_page_manifest_pointer(tmp_path) -> None:
    """After write_overlay_state, page manifest points at current_state.json."""
    bundle = load_minimal_bundle()
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    source_files, source_page_images, page_images, witness_files = (
        _write_minimal_inputs(tmp_path)
    )
    service.write_document_bundle(
        bundle,
        root,
        source_files=source_files,
        source_page_images=source_page_images,
        page_images=page_images,
        witness_files=witness_files,
    )

    states = [
        OverlayState(
            object_id="note-1",
            scope=ReviewScope.NOTE,
            trust_state=TrustState.REVIEWED,
            reviewed_dimensions=[ReviewDimension.NOTE_LINKAGE],
            applied_event_ids=["evt-a"],
        )
    ]
    service.write_overlay_state(root, 1, states)

    page_manifest = service.read_page_manifest(root, 1)
    assert page_manifest.overlay_state_path == (
        "pages/page-0001/overlays/current_state.json"
    )


def test_write_document_bundle_preserves_overlay_state_pointer(tmp_path) -> None:
    """Rewriting the bundle keeps overlay state file and manifest pointer."""
    bundle = load_minimal_bundle()
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    source_files, source_page_images, page_images, witness_files = (
        _write_minimal_inputs(tmp_path)
    )
    service.write_document_bundle(
        bundle,
        root,
        source_files=source_files,
        source_page_images=source_page_images,
        page_images=page_images,
        witness_files=witness_files,
    )

    states = [
        OverlayState(
            object_id="note-1",
            scope=ReviewScope.NOTE,
            trust_state=TrustState.REVIEWED,
            reviewed_dimensions=[ReviewDimension.NOTE_LINKAGE],
            applied_event_ids=["evt-a"],
        )
    ]
    service.write_overlay_state(root, 1, states)
    state_path = root / "pages" / "page-0001" / "overlays" / "current_state.json"
    bytes_after_overlay = state_path.read_bytes()

    service.write_document_bundle(
        bundle,
        root,
        source_files=source_files,
        source_page_images=source_page_images,
        page_images=page_images,
        witness_files=witness_files,
    )

    page_manifest = service.read_page_manifest(root, 1)
    assert state_path.read_bytes() == bytes_after_overlay
    assert page_manifest.overlay_state_path == (
        "pages/page-0001/overlays/current_state.json"
    )


def test_write_overlay_state_writes_json_array(tmp_path) -> None:
    """Derived overlay state overwrites current_state.json as a JSON array."""
    bundle = load_minimal_bundle()
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    source_files, source_page_images, page_images, witness_files = (
        _write_minimal_inputs(tmp_path)
    )
    service.write_document_bundle(
        bundle,
        root,
        source_files=source_files,
        source_page_images=source_page_images,
        page_images=page_images,
        witness_files=witness_files,
    )

    states = [
        OverlayState(
            object_id="note-1",
            scope=ReviewScope.NOTE,
            trust_state=TrustState.REVIEWED,
            reviewed_dimensions=[ReviewDimension.NOTE_LINKAGE],
            applied_event_ids=["evt-a"],
        )
    ]
    service.write_overlay_state(root, 1, states)

    state_path = root / "pages" / "page-0001" / "overlays" / "current_state.json"
    assert state_path.exists()
    payload = json.loads(state_path.read_text(encoding="utf-8"))
    assert payload == [state.model_dump(mode="json") for state in states]


def test_read_review_events_skips_blank_lines(tmp_path) -> None:
    """Blank JSONL lines are ignored when reading review events."""
    bundle = load_minimal_bundle()
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    source_files, source_page_images, page_images, witness_files = (
        _write_minimal_inputs(tmp_path)
    )
    service.write_document_bundle(
        bundle,
        root,
        source_files=source_files,
        source_page_images=source_page_images,
        page_images=page_images,
        witness_files=witness_files,
    )

    event = _accept_review_event("evt-only")
    review_path = root / "pages" / "page-0001" / "overlays" / "review_events.jsonl"
    review_path.write_text(
        "\n" + json.dumps(event.model_dump(mode="json")) + "\n\n",
        encoding="utf-8",
    )

    events = service.read_review_events(root, 1)
    assert len(events) == 1
    assert events[0]["event_id"] == "evt-only"


def test_write_overlay_state_creates_manifest_when_missing(tmp_path) -> None:
    """Overlay write before bundle write still records overlay presence."""
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    states = [
        OverlayState(
            object_id="note-1",
            scope=ReviewScope.NOTE,
            trust_state=TrustState.REVIEWED,
            reviewed_dimensions=[ReviewDimension.NOTE_LINKAGE],
            applied_event_ids=["evt-a"],
        )
    ]

    service.write_overlay_state(root, 1, states)

    state_path = root / "pages" / "page-0001" / "overlays" / "current_state.json"
    assert state_path.exists()
    page_manifest = service.read_page_manifest(root, 1)
    assert page_manifest.page_id == "page-0001"
    assert page_manifest.overlay_state_path == (
        "pages/page-0001/overlays/current_state.json"
    )
    assert page_manifest.review_events_path == (
        "pages/page-0001/overlays/review_events.jsonl"
    )
    review_path = root / "pages" / "page-0001" / "overlays" / "review_events.jsonl"
    assert review_path.exists()


def test_resolve_source_image_path_rejects_ambiguous_extensions(tmp_path) -> None:
    """Multiple source/pages/NNNN.* files must not silently pick one."""
    root = tmp_path / "bundle"
    paths = BundlePaths(root)
    pages_dir = paths.source_pages_dir()
    pages_dir.mkdir(parents=True)
    (pages_dir / "0001.jp2").write_bytes(b"a")
    (pages_dir / "0001.png").write_bytes(b"b")

    with pytest.raises(ValueError, match="ambiguous source page image"):
        _resolve_source_image_path(root, paths, 1, None, None)


def test_write_document_bundle_uses_prepared_image_path_fallback(tmp_path) -> None:
    """Without source/prepared copies, fall back to BundlePage prepared path."""
    bundle = load_minimal_bundle()
    service = BundleLayoutService()
    root = tmp_path / "bundle"

    service.write_document_bundle(bundle, root)

    page_manifest = service.read_page_manifest(root, 1)
    assert page_manifest.source_image_path == "/opt/wordwending-work/prepared_0001.tif"
    graph = service.read_page_graph(root, 1)
    assert graph.prepared_page.image_path == "/opt/wordwending-work/prepared_0001.tif"


def test_write_document_bundle_rejects_missing_source_image_path(tmp_path) -> None:
    """Raise when no source page image and no prepared image path exist."""
    bundle = load_minimal_bundle()
    page = bundle.pages[0]
    cleared = page.model_copy(
        update={
            "prepared_page": page.prepared_page.model_copy(update={"image_path": ""}),
        }
    )
    bundle = bundle.model_copy(update={"pages": [cleared]})
    service = BundleLayoutService()
    root = tmp_path / "bundle"

    with pytest.raises(ValueError, match="source_image_path"):
        service.write_document_bundle(bundle, root)


def test_write_document_bundle_rejects_unknown_witness_kind(tmp_path) -> None:
    """witness_kind outside Spec 0002 families must not become path segments."""
    bundle = load_minimal_bundle()
    page = bundle.pages[0]
    bad_witness = page.witnesses[0].model_copy(update={"witness_kind": "handwriting"})
    bundle = bundle.model_copy(
        update={"pages": [page.model_copy(update={"witnesses": [bad_witness]})]}
    )
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    source_files, source_page_images, page_images, witness_files = (
        _write_minimal_inputs(tmp_path)
    )

    with pytest.raises(ValueError, match="witness_kind"):
        service.write_document_bundle(
            bundle,
            root,
            source_files=source_files,
            source_page_images=source_page_images,
            page_images=page_images,
            witness_files=witness_files,
        )


def test_write_document_bundle_rejects_traversing_witness_kind(tmp_path) -> None:
    """Path-traversal witness_kind values must be rejected before copy."""
    bundle = load_minimal_bundle()
    page = bundle.pages[0]
    bad_witness = page.witnesses[0].model_copy(
        update={"witness_kind": "../../../../escaped"}
    )
    bundle = bundle.model_copy(
        update={"pages": [page.model_copy(update={"witnesses": [bad_witness]})]}
    )
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    source_files, source_page_images, page_images, witness_files = (
        _write_minimal_inputs(tmp_path)
    )

    with pytest.raises(ValueError, match="witness_kind"):
        service.write_document_bundle(
            bundle,
            root,
            source_files=source_files,
            source_page_images=source_page_images,
            page_images=page_images,
            witness_files=witness_files,
        )
    assert not (tmp_path / "escaped").exists()


def test_write_document_bundle_rejects_unsafe_witness_id(tmp_path) -> None:
    """Path-traversal witness_id must not become a destination filename segment."""
    bundle = load_minimal_bundle()
    page = bundle.pages[0]
    unsafe_id = "../../../../"
    bad_witness = page.witnesses[0].model_copy(update={"witness_id": unsafe_id})
    bundle = bundle.model_copy(
        update={"pages": [page.model_copy(update={"witnesses": [bad_witness]})]}
    )
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    source_files, source_page_images, page_images, _ = _write_minimal_inputs(tmp_path)
    witness_src = tmp_path / "inputs" / "olmocr-response.json"

    with pytest.raises(ValueError, match="witness_id"):
        service.write_document_bundle(
            bundle,
            root,
            source_files=source_files,
            source_page_images=source_page_images,
            page_images=page_images,
            witness_files={unsafe_id: witness_src},
        )
    assert not (root / "_olmocr-response.json").exists()
    assert not (tmp_path / "_olmocr-response.json").exists()


def test_write_document_bundle_keeps_same_basename_witnesses(tmp_path) -> None:
    """Two text witnesses sharing a basename must both survive under unique names."""
    bundle = load_minimal_bundle()
    page = bundle.pages[0]
    wit_a = page.witnesses[0].model_copy(update={"witness_id": "wit-a"})
    wit_b = page.witnesses[0].model_copy(update={"witness_id": "wit-b"})
    witness_ids = ["wit-a", "wit-b"]

    def _retarget_provenance(record):
        return record.model_copy(
            update={
                "provenance": record.provenance.model_copy(
                    update={"witness_ids": list(witness_ids)}
                )
            }
        )

    page = page.model_copy(
        update={
            "witnesses": [wit_a, wit_b],
            "regions": [_retarget_provenance(region) for region in page.regions],
            "lines": [_retarget_provenance(line) for line in page.lines],
            "spans": [_retarget_provenance(span) for span in page.spans],
            "notes": [_retarget_provenance(note) for note in page.notes],
        }
    )
    bundle = bundle.model_copy(update={"pages": [page]})
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    source_files, source_page_images, page_images, _ = _write_minimal_inputs(tmp_path)
    inputs = tmp_path / "inputs"
    witness_a = inputs / "dir-a" / "response.json"
    witness_b = inputs / "dir-b" / "response.json"
    witness_a.parent.mkdir(parents=True)
    witness_b.parent.mkdir(parents=True)
    witness_a.write_text('{"text": "alpha"}', encoding="utf-8")
    witness_b.write_text('{"text": "beta"}', encoding="utf-8")

    service.write_document_bundle(
        bundle,
        root,
        source_files=source_files,
        source_page_images=source_page_images,
        page_images=page_images,
        witness_files={"wit-a": witness_a, "wit-b": witness_b},
    )

    text_dir = root / "pages" / "page-0001" / "witnesses" / "text"
    path_a = text_dir / "wit-a_response.json"
    path_b = text_dir / "wit-b_response.json"
    assert path_a.read_text(encoding="utf-8") == '{"text": "alpha"}'
    assert path_b.read_text(encoding="utf-8") == '{"text": "beta"}'
    assert not (text_dir / "response.json").exists()

    page_manifest = service.read_page_manifest(root, 1)
    artifact_paths = {
        ref.witness_id: ref.artifact_path for ref in page_manifest.witness_artifacts
    }
    assert artifact_paths["wit-a"] == (
        "pages/page-0001/witnesses/text/wit-a_response.json"
    )
    assert artifact_paths["wit-b"] == (
        "pages/page-0001/witnesses/text/wit-b_response.json"
    )

    graph = service.read_page_graph(root, 1)
    graph_paths = {ref.witness_id: ref.artifact_path for ref in graph.witnesses}
    assert graph_paths == artifact_paths


def test_write_document_bundle_rewrites_prepared_image_path_in_graph(tmp_path) -> None:
    """Copied prepared images rewrite page_graph prepared_page.image_path."""
    bundle = load_minimal_bundle()
    assert bundle.pages[0].prepared_page.image_path.startswith("/")
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    source_files, source_page_images, page_images, witness_files = (
        _write_minimal_inputs(tmp_path)
    )
    prepared = tmp_path / "inputs" / "prepared_0001.tif"
    prepared.write_bytes(b"fake-tif-bytes")
    page_images = {"page-0001": prepared}

    service.write_document_bundle(
        bundle,
        root,
        source_files=source_files,
        source_page_images=source_page_images,
        page_images=page_images,
        witness_files=witness_files,
    )

    graph = service.read_page_graph(root, 1)
    assert graph.prepared_page.image_path == (
        "pages/page-0001/image/prepared_0001.tif"
    )
    assert (root / "pages" / "page-0001" / "image" / "prepared_0001.tif").exists()


def test_write_document_bundle_rejects_duplicate_page_numbers(tmp_path) -> None:
    """Duplicate page_number values must fail before silent page overwrite."""
    bundle = load_minimal_bundle()
    first = bundle.pages[0]
    second = first.model_copy(
        update={
            "page_id": "page-0001-dup",
            "spans": [
                first.spans[0].model_copy(
                    update={"span_id": "span-2", "text_diplomatic": "SECOND PAGE TEXT"}
                )
            ],
        }
    )
    bundle = bundle.model_copy(update={"pages": [first, second]})
    service = BundleLayoutService()
    root = tmp_path / "bundle"

    with pytest.raises(ValueError, match="duplicate page_number"):
        service.write_document_bundle(bundle, root)


def test_write_document_bundle_rejects_unsafe_source_basename(tmp_path) -> None:
    """source_files keys must be bare basenames, not path segments."""
    bundle = load_minimal_bundle()
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    source_pdf = tmp_path / "inputs" / "sample.pdf"
    source_pdf.parent.mkdir(parents=True, exist_ok=True)
    source_pdf.write_bytes(b"%PDF-1.4 minimal")

    with pytest.raises(ValueError, match="basename"):
        service.write_document_bundle(
            bundle,
            root,
            source_files={"../escaped.pdf": source_pdf},
        )


def test_write_document_bundle_rejects_unsafe_page_export_name(tmp_path) -> None:
    """page_exports basenames must not escape the page exports directory."""
    bundle = load_minimal_bundle()
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    source_files, source_page_images, page_images, witness_files = (
        _write_minimal_inputs(tmp_path)
    )

    with pytest.raises(ValueError, match="basename"):
        service.write_document_bundle(
            bundle,
            root,
            source_files=source_files,
            source_page_images=source_page_images,
            page_images=page_images,
            witness_files=witness_files,
            page_exports={"page-0001": {"../escaped.txt": "nope"}},
        )


def test_append_review_events_heals_missing_trailing_newline(tmp_path) -> None:
    """Append inserts a separator when prior JSONL lacks a trailing newline."""
    bundle = load_minimal_bundle()
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    source_files, source_page_images, page_images, witness_files = (
        _write_minimal_inputs(tmp_path)
    )
    service.write_document_bundle(
        bundle,
        root,
        source_files=source_files,
        source_page_images=source_page_images,
        page_images=page_images,
        witness_files=witness_files,
    )

    review_path = root / "pages" / "page-0001" / "overlays" / "review_events.jsonl"
    review_path.write_bytes(b'{"event_id":"partial"}')
    service.append_review_events(root, 1, [_accept_review_event("evt-1")])

    events = service.read_review_events(root, 1)
    assert [event["event_id"] for event in events] == ["partial", "evt-1"]


def test_append_review_events_heals_missing_newline_after_multibyte_utf8(
    tmp_path,
) -> None:
    """Heal must not UnicodeDecodeError when prior JSONL ends on multi-byte UTF-8."""
    bundle = load_minimal_bundle()
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    source_files, source_page_images, page_images, witness_files = (
        _write_minimal_inputs(tmp_path)
    )
    service.write_document_bundle(
        bundle,
        root,
        source_files=source_files,
        source_page_images=source_page_images,
        page_images=page_images,
        witness_files=witness_files,
    )

    review_path = root / "pages" / "page-0001" / "overlays" / "review_events.jsonl"
    # Ends on multi-byte UTF-8 'é' (U+00E9 → c3 a9), no trailing newline
    review_path.write_bytes(b'{"event_id":"partial","note":"caf\xc3\xa9')

    service.append_review_events(root, 1, [_accept_review_event("evt-1")])

    raw = review_path.read_bytes()
    assert raw.endswith(b"\n")
    assert b'"event_id":"evt-1"' in raw or b'"event_id": "evt-1"' in raw
    # Damaged first line may still be unreadable; append itself must succeed.


def test_read_review_events_reports_corrupt_line(tmp_path) -> None:
    """Corrupt JSONL lines name the file and line number."""
    bundle = load_minimal_bundle()
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    source_files, source_page_images, page_images, witness_files = (
        _write_minimal_inputs(tmp_path)
    )
    service.write_document_bundle(
        bundle,
        root,
        source_files=source_files,
        source_page_images=source_page_images,
        page_images=page_images,
        witness_files=witness_files,
    )

    review_path = root / "pages" / "page-0001" / "overlays" / "review_events.jsonl"
    review_path.write_text('{"ok":true}\n{not-json}\n', encoding="utf-8")

    with pytest.raises(ValueError, match=r"review_events\.jsonl.*line 2"):
        service.read_review_events(root, 1)


def test_write_document_exports_writes_derived_views(tmp_path) -> None:
    """Persisted document exports match renderer output and preserve overlays."""
    bundle = load_export_minimal_bundle()
    original_exports = bundle.exports.model_copy(deep=True)
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    source_files, source_page_images, page_images, witness_files = (
        _write_minimal_inputs(tmp_path)
    )
    service.write_document_bundle(
        bundle,
        root,
        source_files=source_files,
        source_page_images=source_page_images,
        page_images=page_images,
        witness_files=witness_files,
    )

    review_path = root / "pages" / "page-0001" / "overlays" / "review_events.jsonl"
    seeded_events = b'{"event_id":"evt-export-seed"}\n'
    review_path.write_bytes(seeded_events)

    exporter = DocumentExportService()
    expected_rag = exporter.build_rag_document(bundle)
    expected_markdown = exporter.render_markdown(bundle)

    written = service.write_document_exports(bundle, root)

    assert bundle.exports == original_exports
    assert written.exports.bundle_json_path == "exports/bundle.json"
    assert written.exports.rag_jsonl_path == "exports/rag.jsonl"
    assert written.exports.stitched_chunks_jsonl_path == "exports/stitched_chunks.jsonl"
    assert written.exports.document_markdown_path == "exports/document.md"

    bundle_json_path = root / written.exports.bundle_json_path
    rag_jsonl_path = root / written.exports.rag_jsonl_path
    stitched_jsonl_path = root / written.exports.stitched_chunks_jsonl_path
    markdown_path = root / written.exports.document_markdown_path

    restored = DocumentBundle.model_validate_json(
        bundle_json_path.read_text(encoding="utf-8")
    )
    assert restored == written
    assert restored.exports == written.exports

    rag_lines = [
        line
        for line in rag_jsonl_path.read_text(encoding="utf-8").splitlines()
        if line
    ]
    assert len(rag_lines) == len(expected_rag.chunks)
    for line, chunk in zip(rag_lines, expected_rag.chunks, strict=True):
        assert json.loads(line) == chunk.model_dump(mode="json")
    if expected_rag.chunks:
        assert rag_jsonl_path.read_text(encoding="utf-8").endswith("\n")

    stitched_lines = [
        line
        for line in stitched_jsonl_path.read_text(encoding="utf-8").splitlines()
        if line
    ]
    assert len(stitched_lines) == len(expected_rag.stitched_chunks)
    for line, chunk in zip(
        stitched_lines,
        expected_rag.stitched_chunks,
        strict=True,
    ):
        assert json.loads(line) == chunk.model_dump(mode="json")
    if expected_rag.stitched_chunks:
        assert stitched_jsonl_path.read_text(encoding="utf-8").endswith("\n")

    assert markdown_path.read_text(encoding="utf-8") == expected_markdown

    stale_marker = "stale-export-marker"
    rag_jsonl_path.write_text(f"{stale_marker}\n", encoding="utf-8")
    markdown_path.write_text(stale_marker, encoding="utf-8")

    rewritten = service.write_document_exports(bundle, root)

    assert rewritten.exports == written.exports
    assert stale_marker not in rag_jsonl_path.read_text(encoding="utf-8")
    assert markdown_path.read_text(encoding="utf-8") == expected_markdown
    assert review_path.read_bytes() == seeded_events


def test_write_document_exports_frozen_contract_jsonl_validates(tmp_path) -> None:
    """Layout exports from document-bundle-v1 keep stable ids and model-valid JSONL."""
    bundle = load_frozen_document_bundle_v1()
    original_document_id = bundle.document_id
    original_exports = bundle.exports.model_copy(deep=True)
    root = tmp_path / "frozen-bundle"
    root.mkdir(parents=True, exist_ok=True)

    expected_rag = DocumentExportService().build_rag_document(bundle)
    written = BundleLayoutService().write_document_exports(bundle, root)

    assert bundle.exports == original_exports
    assert written.document_id == original_document_id
    assert written.exports.bundle_json_path == "exports/bundle.json"
    assert written.exports.rag_jsonl_path == "exports/rag.jsonl"
    assert written.exports.stitched_chunks_jsonl_path == "exports/stitched_chunks.jsonl"
    assert written.exports.document_markdown_path == "exports/document.md"

    restored_bundle = DocumentBundle.model_validate_json(
        (root / written.exports.bundle_json_path).read_text(encoding="utf-8")
    )
    assert restored_bundle.document_id == original_document_id
    assert restored_bundle.exports == written.exports

    rag_lines = [
        line
        for line in (root / written.exports.rag_jsonl_path)
        .read_text(encoding="utf-8")
        .splitlines()
        if line
    ]
    assert len(rag_lines) == len(expected_rag.chunks)
    for line, expected in zip(rag_lines, expected_rag.chunks, strict=True):
        chunk = RagChunk.model_validate_json(line)
        assert chunk == expected
        assert chunk.document_id == original_document_id
        assert chunk.chunk_id

    stitched_lines = [
        line
        for line in (root / written.exports.stitched_chunks_jsonl_path)
        .read_text(encoding="utf-8")
        .splitlines()
        if line
    ]
    assert len(stitched_lines) == len(expected_rag.stitched_chunks)
    assert stitched_lines, "frozen bundle must persist a multi-page stitched chunk"
    for line, expected in zip(
        stitched_lines,
        expected_rag.stitched_chunks,
        strict=True,
    ):
        chunk = StitchedChunk.model_validate_json(line)
        assert chunk == expected
        assert chunk.document_id == original_document_id
        assert chunk.stitched_chunk_id
        assert len(chunk.page_ids) >= 2
