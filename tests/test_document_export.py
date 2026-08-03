# Copyright (C) 2026 Chris Malek.
"""Tests for document export and retrieval chunk derivation."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from bochord.models import (
    AcquisitionProvenance,
    BaselineShift,
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
    TextRole,
    TrustState,
    Typography,
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


def _region_page(  # noqa: PLR0913
    *,
    page_id: str,
    page_number: int,
    region_id: str,
    text: str,
    reading_order_index: int,
    region_kind: RegionKind = RegionKind.BODY,
    trust_state: TrustState = TrustState.MACHINE,
    witness_id: str = "wit-1",
) -> BundlePage:
    """Build one accepted page with a single region and witness metadata."""
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
                region_kind=region_kind,
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
    return _region_page(
        page_id=page_id,
        page_number=page_number,
        region_id=region_id,
        text=text,
        reading_order_index=reading_order_index,
        region_kind=RegionKind.BODY,
        trust_state=trust_state,
        witness_id=witness_id,
    )


def _merge_page_regions(base: BundlePage, extra: BundlePage) -> BundlePage:
    """Combine region graph objects from two pages sharing the same page id."""
    return base.model_copy(
        update={
            "regions": [*base.regions, *extra.regions],
            "lines": [*base.lines, *extra.lines],
            "spans": [*base.spans, *extra.spans],
        }
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


def test_stitching_is_body_main_text_only() -> None:
    """Only BODY main-text regions stitch; other region kinds stay page-local."""
    footnote_one = _region_page(
        page_id="page-0001",
        page_number=1,
        region_id="region-footnote-one",
        text="footnote one",
        reading_order_index=1,
        region_kind=RegionKind.FOOTNOTE,
    )
    footnote_two = _region_page(
        page_id="page-0002",
        page_number=2,
        region_id="region-footnote-two",
        text="footnote two",
        reading_order_index=1,
        region_kind=RegionKind.FOOTNOTE,
    )
    header_one = _region_page(
        page_id="page-0001",
        page_number=1,
        region_id="region-header-one",
        text="header one",
        reading_order_index=1,
        region_kind=RegionKind.HEADER,
    )
    header_two = _region_page(
        page_id="page-0002",
        page_number=2,
        region_id="region-header-two",
        text="header two",
        reading_order_index=1,
        region_kind=RegionKind.HEADER,
    )

    assert (
        DocumentExportService()
        .build_rag_document(_document_bundle([footnote_one, footnote_two]))
        .stitched_chunks
        == []
    )
    assert (
        DocumentExportService()
        .build_rag_document(_document_bundle([header_one, header_two]))
        .stitched_chunks
        == []
    )

    body_one = _body_region_page(
        page_id="page-0001",
        page_number=1,
        region_id="region-body-one",
        text="body one",
        reading_order_index=2,
    )
    body_two = _body_region_page(
        page_id="page-0002",
        page_number=2,
        region_id="region-body-two",
        text="body two",
        reading_order_index=1,
    )
    mixed_page_one = _merge_page_regions(
        body_one,
        _region_page(
            page_id="page-0001",
            page_number=1,
            region_id="region-header-mixed",
            text="mixed header",
            reading_order_index=1,
            region_kind=RegionKind.HEADER,
        ),
    )
    mixed_page_two = _merge_page_regions(
        body_two,
        _region_page(
            page_id="page-0002",
            page_number=2,
            region_id="region-footnote-mixed",
            text="mixed footnote",
            reading_order_index=2,
            region_kind=RegionKind.FOOTNOTE,
        ),
    )

    rag = DocumentExportService().build_rag_document(
        _document_bundle([mixed_page_one, mixed_page_two])
    )

    assert len(rag.stitched_chunks) == 1
    stitched = rag.stitched_chunks[0]
    assert stitched.component_chunk_ids == [
        "region-region-body-one",
        "region-region-body-two",
    ]
    assert stitched.text == "body one\nbody two"
    stitched_components = [
        chunk
        for chunk in rag.chunks
        if chunk.chunk_id in stitched.component_chunk_ids
    ]
    assert all(
        chunk.retrieval_metadata.region_kind == RegionKind.BODY
        for chunk in stitched_components
    )


def _markdown_style_page() -> BundlePage:
    """Build one page exercising markdown style, regions, and footnote linkage."""
    page_id = "page-md-0001"
    provenance = _page_provenance(page_id)
    witness_only_phrase = "WITNESS-ONLY-ARTIFACT-TEXT"
    body_region_id = "region-body-md"
    table_region_id = "region-table-md"
    marginal_region_id = "region-marginal-md"
    unknown_region_id = "region-unknown-md"
    line_id = "line-body-md"
    return BundlePage(
        page_id=page_id,
        page_number=1,
        prepared_page=_prepared_page(page_id, 1),
        witnesses=[
            WitnessReference(
                witness_id="wit-witness-only",
                witness_kind="text",
                artifact_path=f"pages/{page_id}/witnesses/text/{witness_only_phrase}.json",
                runner_id="olmocr",
                page_id=page_id,
            )
        ],
        regions=[
            RegionRecord(
                region_id=body_region_id,
                region_kind=RegionKind.BODY,
                reading_order_index=1,
                line_ids=[line_id],
                trust_state=TrustState.MACHINE,
                provenance=provenance,
            ),
            RegionRecord(
                region_id=table_region_id,
                region_kind=RegionKind.TABLE,
                reading_order_index=2,
                line_ids=["line-table-md"],
                trust_state=TrustState.MACHINE,
                provenance=provenance,
            ),
            RegionRecord(
                region_id=marginal_region_id,
                region_kind=RegionKind.MARGINALIA,
                reading_order_index=3,
                line_ids=["line-marginal-md"],
                trust_state=TrustState.MACHINE,
                provenance=provenance,
            ),
            RegionRecord(
                region_id=unknown_region_id,
                region_kind=RegionKind.UNKNOWN,
                reading_order_index=4,
                line_ids=["line-unknown-md"],
                trust_state=TrustState.MACHINE,
                provenance=provenance,
            ),
        ],
        lines=[
            LineRecord(
                line_id=line_id,
                region_id=body_region_id,
                line_order=1,
                span_ids=[
                    "span-bold",
                    "span-italic",
                    "span-super",
                    "span-marker",
                    "span-escape",
                ],
                trust_state=TrustState.MACHINE,
                provenance=provenance,
            ),
            LineRecord(
                line_id="line-table-md",
                region_id=table_region_id,
                line_order=1,
                span_ids=["span-table-md"],
                trust_state=TrustState.MACHINE,
                provenance=provenance,
            ),
            LineRecord(
                line_id="line-marginal-md",
                region_id=marginal_region_id,
                line_order=1,
                span_ids=["span-marginal-md"],
                trust_state=TrustState.MACHINE,
                provenance=provenance,
            ),
            LineRecord(
                line_id="line-unknown-md",
                region_id=unknown_region_id,
                line_order=1,
                span_ids=["span-unknown-md"],
                trust_state=TrustState.MACHINE,
                provenance=provenance,
            ),
        ],
        spans=[
            SpanRecord(
                span_id="span-bold",
                line_id=line_id,
                text_diplomatic="bold",
                text_normalized="bold",
                typography=Typography(weight=FontWeight.BOLD, slant=FontSlant.UPRIGHT),
                trust_state=TrustState.MACHINE,
                provenance=provenance,
            ),
            SpanRecord(
                span_id="span-italic",
                line_id=line_id,
                text_diplomatic="italic",
                text_normalized="italic",
                typography=Typography(
                    weight=FontWeight.REGULAR,
                    slant=FontSlant.ITALIC,
                ),
                trust_state=TrustState.MACHINE,
                provenance=provenance,
            ),
            SpanRecord(
                span_id="span-super",
                line_id=line_id,
                text_diplomatic="super",
                text_normalized="super",
                typography=Typography(
                    weight=FontWeight.REGULAR,
                    slant=FontSlant.UPRIGHT,
                    baseline_shift=BaselineShift.SUPERSCRIPT,
                ),
                trust_state=TrustState.MACHINE,
                provenance=provenance,
            ),
            SpanRecord(
                span_id="span-marker",
                line_id=line_id,
                text_diplomatic="marker",
                text_normalized="marker",
                roles=[TextRole.FOOTNOTE_MARKER],
                trust_state=TrustState.REVIEWED,
                provenance=provenance,
            ),
            SpanRecord(
                span_id="span-escape",
                line_id=line_id,
                text_diplomatic="*stars*",
                text_normalized="*stars*",
                trust_state=TrustState.MACHINE,
                provenance=provenance,
            ),
            SpanRecord(
                span_id="span-table-md",
                line_id="line-table-md",
                text_diplomatic="table witness prose",
                text_normalized="table witness prose",
                trust_state=TrustState.MACHINE,
                provenance=provenance,
            ),
            SpanRecord(
                span_id="span-marginal-md",
                line_id="line-marginal-md",
                text_diplomatic="margin witness prose",
                text_normalized="margin witness prose",
                trust_state=TrustState.MACHINE,
                provenance=provenance,
            ),
            SpanRecord(
                span_id="span-unknown-md",
                line_id="line-unknown-md",
                text_diplomatic="unknown witness prose",
                text_normalized="unknown witness prose",
                trust_state=TrustState.MACHINE,
                provenance=provenance,
            ),
        ],
        notes=[
            NoteRecord(
                note_id="note-md-1",
                note_kind=NoteKind.FOOTNOTE_BLOCK,
                region_id=body_region_id,
                text_diplomatic="Accepted note body for marker.",
                linked_marker_span_ids=["span-marker"],
                trust_state=TrustState.REVIEWED,
                provenance=provenance,
            )
        ],
    )


def test_markdown_preserves_style_regions_and_note_linkage() -> None:
    """Markdown follows accepted graph order, styles, placeholders, and notes."""
    minimal = _load_minimal_bundle()
    style_page = _markdown_style_page()
    bundle = minimal.model_copy(
        update={"pages": [*minimal.pages, style_page]},
    )
    markdown = DocumentExportService().render_markdown(bundle)

    witness_only_phrase = "WITNESS-ONLY-ARTIFACT-TEXT"
    assert witness_only_phrase not in markdown
    assert "table witness prose" not in markdown
    assert "margin witness prose" not in markdown
    assert "unknown witness prose" not in markdown

    page_one_idx = markdown.index("<!-- page page-0001 -->")
    page_two_idx = markdown.index("<!-- page page-md-0001 -->")
    assert page_one_idx < page_two_idx

    body_region_idx = markdown.index("<!-- region region-body kind=body -->")
    corrected_region_idx = markdown.index(
        "<!-- region region-corrected kind=body -->"
    )
    table_region_idx = markdown.index("<!-- region region-table-md kind=table -->")
    marginal_region_idx = markdown.index(
        "<!-- region region-marginal-md kind=marginalia -->"
    )
    unknown_region_idx = markdown.index(
        "<!-- region region-unknown-md kind=unknown -->"
    )
    assert body_region_idx < corrected_region_idx < page_two_idx
    assert (
        table_region_idx
        < marginal_region_idx
        < unknown_region_idx
    )

    assert "and*git*[^note-1]" in markdown
    assert "more" in markdown
    assert "**corrected**" in markdown

    assert "**bold**" in markdown
    assert "*italic*" in markdown
    assert "<sup>super</sup>" in markdown
    assert "*marker*[^note-md-1]" not in markdown
    assert "marker[^note-md-1]" in markdown
    assert r"\*stars\*" in markdown

    assert "[table region: region-table-md]" in markdown
    assert "[marginalia region: region-marginal-md]" in markdown
    assert "[unknown region: region-unknown-md]" in markdown

    notes_idx = markdown.index("## Notes")
    assert notes_idx > unknown_region_idx
    assert "[^note-1]: See also the entry under git." in markdown
    assert "[^note-md-1]: Accepted note body for marker." in markdown


def _single_span_body_page(
    *,
    page_id: str,
    span_id: str,
    text: str,
    typography: Typography | None = None,
) -> BundlePage:
    """Build one body region page with a single styled span."""
    provenance = _page_provenance(page_id)
    region_id = f"region-{span_id}"
    line_id = f"line-{span_id}"
    span = SpanRecord(
        span_id=span_id,
        line_id=line_id,
        text_diplomatic=text,
        text_normalized=text,
        typography=typography or Typography(),
        trust_state=TrustState.MACHINE,
        provenance=provenance,
    )
    return BundlePage(
        page_id=page_id,
        page_number=1,
        prepared_page=_prepared_page(page_id, 1),
        regions=[
            RegionRecord(
                region_id=region_id,
                region_kind=RegionKind.BODY,
                reading_order_index=1,
                line_ids=[line_id],
                trust_state=TrustState.MACHINE,
                provenance=provenance,
            )
        ],
        lines=[
            LineRecord(
                line_id=line_id,
                region_id=region_id,
                line_order=1,
                span_ids=[span_id],
                trust_state=TrustState.MACHINE,
                provenance=provenance,
            )
        ],
        spans=[span],
    )


def test_markdown_html_escapes_superscript_content() -> None:
    """Superscript diplomatic text must HTML-escape <, >, and & inside <sup>."""
    page = _single_span_body_page(
        page_id="page-html-esc",
        span_id="span-html-super",
        text="a<b&c>",
        typography=Typography(
            weight=FontWeight.REGULAR,
            slant=FontSlant.UPRIGHT,
            baseline_shift=BaselineShift.SUPERSCRIPT,
        ),
    )
    markdown = DocumentExportService().render_markdown(
        _document_bundle([page], document_id="html-esc-doc")
    )

    assert "<sup>a&lt;b&amp;c&gt;</sup>" in markdown
    assert "<sup>a<b&c></sup>" not in markdown


def test_markdown_renders_combined_bold_italic() -> None:
    """Bold+italic spans use ***text*** with bold outside italic."""
    page = _single_span_body_page(
        page_id="page-bold-italic",
        span_id="span-bold-italic",
        text="both",
        typography=Typography(
            weight=FontWeight.BOLD,
            slant=FontSlant.ITALIC,
        ),
    )
    markdown = DocumentExportService().render_markdown(
        _document_bundle([page], document_id="bold-italic-doc")
    )

    assert "***both***" in markdown
    assert "**\\*both\\***" not in markdown
    assert "*\\**both*\\***" not in markdown


def test_markdown_includes_orphan_note_without_region() -> None:
    """Notes without a parent region still appear in the Notes section."""
    page = _body_region_page(
        page_id="page-orphan-note",
        page_number=1,
        region_id="region-orphan-body",
        text="main text",
        reading_order_index=1,
    )
    page = page.model_copy(
        update={
            "notes": [
                NoteRecord(
                    note_id="note-orphan",
                    note_kind=NoteKind.FOOTNOTE_BLOCK,
                    region_id=None,
                    text_diplomatic="Orphan note without region scope.",
                    linked_marker_span_ids=[],
                    trust_state=TrustState.REVIEWED,
                    provenance=_page_provenance("page-orphan-note"),
                )
            ]
        }
    )
    markdown = DocumentExportService().render_markdown(
        _document_bundle([page], document_id="orphan-note-doc")
    )

    assert "## Notes" in markdown
    assert "[^note-orphan]: Orphan note without region scope." in markdown
