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
    NoteKind,
    NoteRecord,
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
    WitnessReference,
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


def _page_provenance(
    page_id: str,
    *,
    witness_id: str = "wit-1",
) -> ObjectProvenance:
    """Return provenance for one accepted page graph."""
    return ObjectProvenance(
        source_page_id=page_id,
        witness_ids=[witness_id],
        runner_ids=["olmocr"],
    )


def _prepared_page(page_id: str, page_number: int) -> PreparedPage:
    """Return a minimal prepared page shell for programmatic bundles."""
    return PreparedPage(
        prepared_page_id=f"prepared-{page_id}",
        preparation_mode=PreparationMode.FULL_PAGE,
        page_class=PageClass.ORDINARY_PROSE,
        image_path=f"pages/{page_id}/image/page.png",
        source_artifact_id=f"source-{page_id}",
        image_checksum="sha256:prepared",
        preparation_recipe_id="prep-v1",
        preparation_recipe_digest="digest-prep-v1",
        coordinate_space=CoordinateSpace(
            space_id=f"prepared-{page_id}",
            width_px=100,
            height_px=100,
        ),
    )


def _body_region_page(  # noqa: PLR0913
    *,
    page_id: str,
    page_number: int,
    region_id: str,
    text: str,
    reading_order_index: int,
    trust_state: TrustState = TrustState.MACHINE,
    witness_id: str = "wit-1",
) -> BundlePage:
    """Build one accepted page with a single body region and witness metadata."""
    provenance = _page_provenance(page_id, witness_id=witness_id)
    line_id = f"line-{region_id}"
    span_id = f"span-{region_id}"
    return BundlePage(
        page_id=page_id,
        page_number=page_number,
        prepared_page=_prepared_page(page_id, page_number),
        witnesses=[
            WitnessReference(
                witness_id=witness_id,
                witness_kind="text",
                artifact_path=f"pages/{page_id}/witnesses/text/{witness_id}.json",
                runner_id="olmocr",
                page_id=page_id,
            )
        ],
        regions=[
            RegionRecord(
                region_id=region_id,
                region_kind=RegionKind.BODY,
                reading_order_index=reading_order_index,
                line_ids=[line_id],
                trust_state=trust_state,
                provenance=provenance,
            )
        ],
        lines=[
            LineRecord(
                line_id=line_id,
                region_id=region_id,
                line_order=1,
                span_ids=[span_id],
                trust_state=trust_state,
                provenance=provenance,
            )
        ],
        spans=[
            SpanRecord(
                span_id=span_id,
                line_id=line_id,
                text_diplomatic=text,
                text_normalized=text,
                trust_state=trust_state,
                provenance=provenance,
            )
        ],
    )


def _document_bundle(
    pages: list[BundlePage],
    *,
    document_id: str = "stitch-doc",
) -> DocumentBundle:
    """Wrap accepted pages in a valid multi-page document bundle."""
    timestamp = datetime(2026, 8, 3, tzinfo=UTC)
    return DocumentBundle(
        document_id=document_id,
        bundle_schema_version="1.0.0",
        source=SourceDescriptor(
            source_id=f"src-{document_id}",
            source_type=SourceType.PDF,
            source_label=f"{document_id}.pdf",
            original_path=f"sources/{document_id}.pdf",
            page_count=len(pages),
        ),
        bibliographic_provenance=BibliographicProvenance(
            title="Stitch Test",
            authors=["Fixture Author"],
        ),
        acquisition_provenance=AcquisitionProvenance(
            acquisition_kind="local-scan",
            acquired_from="local",
        ),
        run=RunMetadata(
            run_id=f"run-{document_id}",
            run_timestamp_utc=timestamp,
            preparation_recipe_id="prep-v1",
            config_digest="sha256:config",
            runner_set=[],
            bundle_schema_version="1.0.0",
        ),
        pages=pages,
        evaluation_summary=DocumentEvaluationSummary(),
        exports=ExportSummary(bundle_json_path="exports/bundle.json"),
    )


def _minimal_document_bundle(page: BundlePage) -> DocumentBundle:
    """Wrap one accepted page in a valid document bundle."""
    return _document_bundle([page], document_id="collision-doc")


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


def test_stitching_uses_accepted_graph_order_not_witness_order() -> None:
    """Stitched chunks follow bundle page order and accepted region reading order."""
    page_one = _body_region_page(
        page_id="page-0001",
        page_number=1,
        region_id="region-page-one",
        text="page one body",
        reading_order_index=1,
        witness_id="wit-z-last",
    )
    page_two = _body_region_page(
        page_id="page-0002",
        page_number=2,
        region_id="region-page-two",
        text="page two body",
        reading_order_index=1,
        witness_id="wit-a-first",
    )
    bundle = _document_bundle([page_one, page_two])

    rag = DocumentExportService().build_rag_document(bundle)

    assert len(rag.stitched_chunks) == 1
    stitched = rag.stitched_chunks[0]
    assert stitched.component_chunk_ids == [
        "region-region-page-one",
        "region-region-page-two",
    ]
    assert stitched.page_ids == ["page-0001", "page-0002"]
    assert len(set(stitched.page_ids)) >= 2
    assert stitched.text == "page one body\npage two body"
    assert stitched.stitched_chunk_id == (
        "stitched-region-region-page-one-region-region-page-two"
    )
    assert stitched.document_id == "stitch-doc"

    region_chunks = [c for c in rag.chunks if c.chunk_type == ChunkType.REGION]
    assert {chunk.chunk_id for chunk in region_chunks} == set(
        stitched.component_chunk_ids
    )
    assert all(
        chunk_id.startswith("region-")
        for chunk_id in stitched.component_chunk_ids
    )
    assert not any(
        chunk_id.startswith("footnote-")
        for chunk_id in stitched.component_chunk_ids
    )

    union_object_ids: list[str] = []
    union_pages: list[str] = []
    union_witnesses: list[str] = []
    union_runners: list[str] = []
    for chunk_id in stitched.component_chunk_ids:
        component = next(c for c in rag.chunks if c.chunk_id == chunk_id)
        union_object_ids.extend(component.source_object_ids)
        union_pages.extend(component.provenance.source_page_ids)
        union_witnesses.extend(component.provenance.witness_ids)
        union_runners.extend(component.provenance.runner_ids)

    assert stitched.source_object_ids == list(dict.fromkeys(union_object_ids))
    assert stitched.provenance.source_page_ids == list(dict.fromkeys(union_pages))
    assert stitched.provenance.witness_ids == list(dict.fromkeys(union_witnesses))
    assert stitched.provenance.runner_ids == list(dict.fromkeys(union_runners))
    assert stitched.trust_state == TrustState.MACHINE


def test_stitching_skips_one_page_runs_and_footnotes() -> None:
    """Single-page body runs and footnote chunks never produce stitched chunks."""
    page = _body_region_page(
        page_id="page-0001",
        page_number=1,
        region_id="region-only",
        text="single page",
        reading_order_index=1,
    )
    page = page.model_copy(
        update={
            "notes": [
                NoteRecord(
                    note_id="note-1",
                    note_kind=NoteKind.FOOTNOTE_BLOCK,
                    region_id="region-only",
                    text_diplomatic="Footnote body.",
                    linked_marker_span_ids=["span-region-only"],
                    trust_state=TrustState.REVIEWED,
                    provenance=_page_provenance("page-0001"),
                )
            ]
        }
    )
    bundle = _document_bundle([page])

    rag = DocumentExportService().build_rag_document(bundle)

    assert rag.stitched_chunks == []
    assert any(chunk.chunk_type == ChunkType.FOOTNOTE for chunk in rag.chunks)


def test_stitching_aggregates_corrected_trust_across_components() -> None:
    """Stitched trust follows the same corrected-over-reviewed-over-machine rule."""
    page_one = _body_region_page(
        page_id="page-0001",
        page_number=1,
        region_id="region-trust-one",
        text="trusted one",
        reading_order_index=1,
        trust_state=TrustState.REVIEWED,
    )
    page_two = _body_region_page(
        page_id="page-0002",
        page_number=2,
        region_id="region-trust-two",
        text="trusted two",
        reading_order_index=1,
        trust_state=TrustState.CORRECTED,
    )
    bundle = _document_bundle([page_one, page_two])

    rag = DocumentExportService().build_rag_document(bundle)

    assert len(rag.stitched_chunks) == 1
    assert rag.stitched_chunks[0].trust_state == TrustState.CORRECTED
