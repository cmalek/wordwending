# Copyright (C) 2026 Chris Malek.
"""Tests for Spec 0002 bundle path helpers and manifest models."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from bochord.models import (
    BUNDLE_SCHEMA_VERSION,
    AcquisitionProvenance,
    BibliographicProvenance,
    BundlePaths,
    DocumentBundleManifest,
    PageBundleManifest,
    RunnerReference,
    SourceDescriptor,
    SourceType,
    WitnessReference,
    page_dir_name,
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
