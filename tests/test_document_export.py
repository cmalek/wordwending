# Copyright (C) 2026 Chris Malek.
"""Tests for document export and retrieval chunk derivation."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from bochord.models import (
    AcquisitionProvenance,
    BibliographicProvenance,
    BundlePage,
    ChunkType,
    CoordinateSpace,
    DocumentBundle,
    DocumentEvaluationSummary,
    ExportSummary,
    FontSlant,
    FontWeight,
    LineRecord,
    ObjectProvenance,
    PageClass,
    PreparationMode,
    PreparedPage,
    RegionKind,
    RegionRecord,
    RunMetadata,
    SourceDescriptor,
    SourceType,
    SpanRecord,
    TrustState,
)
from bochord.services.document_export import DocumentExportService

FIXTURES = Path(__file__).parent / "fixtures" / "exports"
MINIMAL_BUNDLE = FIXTURES / "minimal-bundle.json"


def _load_minimal_bundle() -> DocumentBundle:
    """Load and validate the compact export fixture bundle."""
    raw = json.loads(MINIMAL_BUNDLE.read_text(encoding="utf-8"))
    return DocumentBundle.model_validate(raw)


def test_build_rag_document_emits_region_and_footnote_chunks() -> None:
    """Page-local chunks follow graph order, provenance, metadata, and trust rules."""
    bundle = _load_minimal_bundle()
    service = DocumentExportService()
    rag = service.build_rag_document(bundle)

    assert rag.document_id == "export-minimal"
    assert rag.schema_version == "1.0.0"
    assert rag.chunking_recipe_id == "page-regions-v1"
    assert rag.stitched_chunks == []

    region_chunks = [c for c in rag.chunks if c.chunk_type == ChunkType.REGION]
    footnote_chunks = [c for c in rag.chunks if c.chunk_type == ChunkType.FOOTNOTE]

    assert len(region_chunks) == 2
    assert len(footnote_chunks) == 1
    assert [c.chunk_id for c in region_chunks] == [
        "region-region-body",
        "region-region-corrected",
    ]
    assert footnote_chunks[0].chunk_id == "footnote-note-1"

    body_chunk = region_chunks[0]
    corrected_chunk = region_chunks[1]
    footnote_chunk = footnote_chunks[0]

    assert body_chunk.text == "andgit\nmore"
    assert corrected_chunk.text == "corrected"

    assert footnote_chunk.text == "See also the entry under git."
    assert "note-1" in footnote_chunk.source_object_ids
    assert "span-git" in footnote_chunk.source_object_ids
    assert footnote_chunk.page_ids == ["page-0001"]
    assert "region-body" in footnote_chunk.source_object_ids

    assert footnote_chunk.note_summary == [
        "note-1",
        "span-git",
        "region-body",
    ]
    assert footnote_chunk.note_summary[0] == "note-1"
    assert "span-git" in footnote_chunk.note_summary
    assert "region-body" in footnote_chunk.note_summary

    assert footnote_chunk.retrieval_metadata.page_number == 1
    assert footnote_chunk.retrieval_metadata.region_kind is None
    assert footnote_chunk.retrieval_metadata.contains_reviewed_content is True
    assert footnote_chunk.retrieval_metadata.contains_corrected_content is False
    assert any(
        signal.slant == FontSlant.ITALIC
        for signal in footnote_chunk.retrieval_metadata.typography_signals
    )
    assert any(
        signal.slant == FontSlant.ITALIC
        for signal in footnote_chunk.typography_summary
    )

    assert len(body_chunk.typography_summary) == 1
    assert body_chunk.typography_summary[0].slant == FontSlant.ITALIC
    assert body_chunk.typography_summary == body_chunk.retrieval_metadata.typography_signals
    assert len(corrected_chunk.typography_summary) == 1
    assert corrected_chunk.typography_summary[0].weight == FontWeight.BOLD

    for chunk in rag.chunks:
        assert chunk.provenance.source_page_ids == ["page-0001"]
        assert chunk.provenance.witness_ids == ["wit-1"]
        assert chunk.provenance.runner_ids == ["olmocr"]

    assert body_chunk.retrieval_metadata.page_number == 1
    assert body_chunk.retrieval_metadata.region_kind == "body"
    assert body_chunk.retrieval_metadata.reading_order_index == 1
    assert body_chunk.retrieval_metadata.contains_reviewed_content is True
    assert body_chunk.retrieval_metadata.contains_corrected_content is False
    assert any(
        signal.slant == FontSlant.ITALIC
        for signal in body_chunk.retrieval_metadata.typography_signals
    )
    assert any(
        signal.weight == FontWeight.BOLD
        for signal in corrected_chunk.retrieval_metadata.typography_signals
    )

    assert corrected_chunk.retrieval_metadata.reading_order_index == 2
    assert corrected_chunk.retrieval_metadata.contains_corrected_content is True
    assert corrected_chunk.trust_state == TrustState.CORRECTED

    assert body_chunk.trust_state == TrustState.MACHINE
    assert footnote_chunk.trust_state == TrustState.REVIEWED


def _object_provenance() -> ObjectProvenance:
    """Return valid single-page provenance for programmatic graph tests."""
    return ObjectProvenance(
        source_page_id="page-0001",
        witness_ids=["wit-1"],
        runner_ids=["olmocr"],
    )


def _minimal_document_bundle(page: BundlePage) -> DocumentBundle:
    """Wrap one accepted page in a valid document bundle."""
    timestamp = datetime(2026, 8, 3, tzinfo=UTC)
    return DocumentBundle(
        document_id="collision-doc",
        bundle_schema_version="1.0.0",
        source=SourceDescriptor(
            source_id="src-collision",
            source_type=SourceType.PDF,
            source_label="collision.pdf",
            original_path="sources/collision.pdf",
            page_count=1,
        ),
        bibliographic_provenance=BibliographicProvenance(
            title="Collision Test",
            authors=["Fixture Author"],
        ),
        acquisition_provenance=AcquisitionProvenance(
            acquisition_kind="local-scan",
            acquired_from="local",
        ),
        run=RunMetadata(
            run_id="run-collision",
            run_timestamp_utc=timestamp,
            preparation_recipe_id="prep-v1",
            config_digest="sha256:config",
            runner_set=[],
            bundle_schema_version="1.0.0",
        ),
        pages=[page],
        evaluation_summary=DocumentEvaluationSummary(),
        exports=ExportSummary(bundle_json_path="exports/bundle.json"),
    )


def test_typed_page_indexes_resolve_colliding_ids_by_object_kind() -> None:
    """Separate region/line/span maps must not overwrite unlike graph records."""
    provenance = _object_provenance()
    shared_id = "shared-object-id"
    page = BundlePage(
        page_id="page-0001",
        page_number=1,
        prepared_page=PreparedPage(
            prepared_page_id="prepared-page-1",
            preparation_mode=PreparationMode.FULL_PAGE,
            page_class=PageClass.ORDINARY_PROSE,
            image_path="pages/page-0001/image/page.png",
            source_artifact_id="source-page-1",
            image_checksum="sha256:prepared",
            preparation_recipe_id="prep-v1",
            preparation_recipe_digest="digest-prep-v1",
            coordinate_space=CoordinateSpace(
                space_id="prepared-page-1",
                width_px=100,
                height_px=100,
            ),
        ),
        regions=[
            RegionRecord(
                region_id=shared_id,
                region_kind=RegionKind.BODY,
                reading_order_index=1,
                line_ids=["line-1"],
                provenance=provenance,
            )
        ],
        lines=[
            LineRecord(
                line_id="line-1",
                region_id=shared_id,
                line_order=1,
                span_ids=[shared_id],
                provenance=provenance,
            )
        ],
        spans=[
            SpanRecord(
                span_id=shared_id,
                line_id="line-1",
                text_diplomatic="span-wins",
                text_normalized="span-wins",
                provenance=provenance,
            )
        ],
    )
    bundle = _minimal_document_bundle(page)

    rag = DocumentExportService().build_rag_document(bundle)
    region_chunk = next(
        chunk for chunk in rag.chunks if chunk.chunk_type == ChunkType.REGION
    )

    assert region_chunk.text == "span-wins"
