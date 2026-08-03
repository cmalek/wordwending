# Copyright (C) 2026 Chris Malek.
"""Tests for document export and retrieval chunk derivation."""

from __future__ import annotations

import json
from pathlib import Path

from bochord.models import (
    ChunkType,
    DocumentBundle,
    FontSlant,
    FontWeight,
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
