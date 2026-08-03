# Copyright (C) 2026 Chris Malek.
"""Derive retrieval chunks from accepted document bundles."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from bochord.models import (
    BaselineShift,
    BundlePage,
    ChunkType,
    DocumentBundle,
    FontSlant,
    FontWeight,
    LineRecord,
    NoteRecord,
    RagChunk,
    RagDocument,
    RegionKind,
    RegionRecord,
    RetrievalMetadata,
    RetrievalProvenance,
    SpanRecord,
    StitchedChunk,
    TrustState,
    Typography,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

#: Persisted retrieval schema version for page-local chunk exports.
RAG_SCHEMA_VERSION = "1.0.0"

#: Reproducible recipe identifier for page-local region and footnote chunking.
PAGE_REGIONS_CHUNKING_RECIPE_ID = "page-regions-v1"

#: Minimum distinct pages required before emitting a stitched chunk.
MIN_STITCHED_PAGE_COUNT = 2


@dataclass(frozen=True)
class PageGraphIndex:
    """Typed page-graph lookups keyed by object kind."""

    #: Accepted regions indexed by ``region_id``.
    regions: dict[str, RegionRecord]
    #: Accepted lines indexed by ``line_id``.
    lines: dict[str, LineRecord]
    #: Accepted spans indexed by ``span_id``.
    spans: dict[str, SpanRecord]


class DocumentExportService:
    """Pure renderer that derives retrieval exports from accepted page graphs."""

    def build_rag_document(self, bundle: DocumentBundle) -> RagDocument:
        """
        Derive page-local region and footnote chunks from an accepted bundle.

        Args:
            bundle: Canonical document bundle whose page graphs supply chunk text.

        Returns:
            Retrieval document with region and footnote chunks in graph order.

        """
        chunks: list[RagChunk] = []
        for page in bundle.pages:
            page_index = self._build_page_indexes(page)
            chunks.extend(
                self._build_region_chunk(
                    bundle.document_id,
                    page,
                    region,
                    page_index,
                )
                for region in sorted(
                    page.regions,
                    key=lambda record: record.reading_order_index,
                )
            )
            chunks.extend(
                self._build_footnote_chunk(
                    bundle.document_id,
                    page,
                    note,
                    page_index,
                )
                for note in page.notes
            )
        region_chunks = [
            chunk for chunk in chunks if chunk.chunk_type == ChunkType.REGION
        ]
        stitched_chunks = self._build_stitched_chunks(
            bundle.document_id,
            bundle.pages,
            region_chunks,
        )
        return RagDocument(
            schema_version=RAG_SCHEMA_VERSION,
            chunking_recipe_id=PAGE_REGIONS_CHUNKING_RECIPE_ID,
            document_id=bundle.document_id,
            chunks=chunks,
            stitched_chunks=stitched_chunks,
        )

    def _build_stitched_chunks(
        self,
        document_id: str,
        pages: Sequence[BundlePage],
        region_chunks: list[RagChunk],
    ) -> list[StitchedChunk]:
        """
        Build cross-page stitched chunks from contiguous region-kind runs.

        Args:
            document_id: Owning document identifier.
            pages: Accepted pages in canonical bundle order.
            region_chunks: Page-local region chunks keyed by region graph order.

        Returns:
            Stitched chunks for same-kind runs spanning at least two pages.

        """
        chunks_by_region = {
            chunk.chunk_id.removeprefix("region-"): chunk
            for chunk in region_chunks
        }
        ordered_region_chunks: list[RagChunk] = []
        for page in pages:
            for region in sorted(
                page.regions,
                key=lambda record: record.reading_order_index,
            ):
                chunk = chunks_by_region.get(region.region_id)
                if chunk is not None:
                    ordered_region_chunks.append(chunk)

        stitched_chunks: list[StitchedChunk] = []
        current_run: list[RagChunk] = []
        current_kind: RegionKind | None = None
        for chunk in ordered_region_chunks:
            region_kind = chunk.retrieval_metadata.region_kind
            if (
                current_run
                and region_kind is not None
                and region_kind != current_kind
            ):
                stitched = self._finalize_stitched_run(document_id, current_run)
                if stitched is not None:
                    stitched_chunks.append(stitched)
                current_run = []
            current_kind = region_kind
            current_run.append(chunk)
        stitched = self._finalize_stitched_run(document_id, current_run)
        if stitched is not None:
            stitched_chunks.append(stitched)
        return stitched_chunks

    def _finalize_stitched_run(
        self,
        document_id: str,
        run: list[RagChunk],
    ) -> StitchedChunk | None:
        """
        Emit one stitched chunk when a region-kind run spans multiple pages.

        Args:
            document_id: Owning document identifier.
            run: Contiguous same-kind region chunks in accepted graph order.

        Returns:
            Stitched chunk when the run spans at least two distinct pages.

        """
        if not run:
            return None
        page_ids: list[str] = []
        seen_pages: set[str] = set()
        for chunk in run:
            for page_id in chunk.page_ids:
                if page_id not in seen_pages:
                    seen_pages.add(page_id)
                    page_ids.append(page_id)
        if len(page_ids) < MIN_STITCHED_PAGE_COUNT:
            return None

        component_chunk_ids = [chunk.chunk_id for chunk in run]
        source_object_ids: list[str] = []
        seen_objects: set[str] = set()
        provenance_pages: list[str] = []
        provenance_witnesses: list[str] = []
        provenance_runners: list[str] = []
        seen_provenance_pages: set[str] = set()
        seen_provenance_witnesses: set[str] = set()
        seen_provenance_runners: set[str] = set()
        for chunk in run:
            for object_id in chunk.source_object_ids:
                if object_id not in seen_objects:
                    seen_objects.add(object_id)
                    source_object_ids.append(object_id)
            self._extend_unique(
                provenance_pages,
                seen_provenance_pages,
                chunk.provenance.source_page_ids,
            )
            self._extend_unique(
                provenance_witnesses,
                seen_provenance_witnesses,
                chunk.provenance.witness_ids,
            )
            self._extend_unique(
                provenance_runners,
                seen_provenance_runners,
                chunk.provenance.runner_ids,
            )

        first_id = component_chunk_ids[0]
        last_id = component_chunk_ids[-1]
        return StitchedChunk(
            stitched_chunk_id=f"stitched-{first_id}-{last_id}",
            document_id=document_id,
            component_chunk_ids=component_chunk_ids,
            page_ids=page_ids,
            text="\n".join(chunk.text for chunk in run),
            trust_state=self._aggregate_chunk_trust(run),
            source_object_ids=source_object_ids,
            provenance=RetrievalProvenance(
                source_page_ids=provenance_pages,
                witness_ids=provenance_witnesses,
                runner_ids=provenance_runners,
            ),
        )

    def _aggregate_chunk_trust(self, chunks: Sequence[RagChunk]) -> TrustState:
        """
        Aggregate trust for stitched component chunks.

        Args:
            chunks: Region chunks whose trust states contribute to the stitch.

        Returns:
            Corrected when any chunk is corrected, else reviewed when all are
            reviewed, else machine.

        """
        trust_states = [chunk.trust_state for chunk in chunks]
        if any(state == TrustState.CORRECTED for state in trust_states):
            return TrustState.CORRECTED
        if trust_states and all(
            state == TrustState.REVIEWED for state in trust_states
        ):
            return TrustState.REVIEWED
        return TrustState.MACHINE

    def _build_page_indexes(self, page: BundlePage) -> PageGraphIndex:
        """
        Index page graph objects in separate typed lookup tables.

        Args:
            page: Accepted page graph whose objects will be resolved by id.

        Returns:
            Typed lookup tables for regions, lines, and spans.

        """
        return PageGraphIndex(
            regions={region.region_id: region for region in page.regions},
            lines={line.line_id: line for line in page.lines},
            spans={span.span_id: span for span in page.spans},
        )

    def _build_region_chunk(
        self,
        document_id: str,
        page: BundlePage,
        region: RegionRecord,
        page_index: PageGraphIndex,
    ) -> RagChunk:
        """
        Build one region retrieval chunk from accepted graph order.

        Args:
            document_id: Owning document identifier.
            page: Page containing the region graph.
            region: Accepted region whose lines and spans supply chunk text.
            page_index: Typed page graph lookups.

        Returns:
            Page-local region chunk with aggregated provenance and trust.

        """
        lines = self._ordered_region_lines(region, page_index)
        spans = self._ordered_region_spans(lines, page_index)
        included: list[RegionRecord | LineRecord | SpanRecord] = [
            region,
            *lines,
            *spans,
        ]
        typography_summary = self._typography_summary(spans)
        return RagChunk(
            chunk_id=f"region-{region.region_id}",
            chunk_type=ChunkType.REGION,
            document_id=document_id,
            page_ids=[page.page_id],
            text=self._join_region_text(lines, page_index),
            trust_state=self._aggregate_trust(included),
            source_object_ids=self._source_object_ids(included),
            provenance=self._aggregate_provenance(included),
            typography_summary=typography_summary,
            retrieval_metadata=RetrievalMetadata(
                reading_order_index=region.reading_order_index,
                page_number=page.page_number,
                region_kind=region.region_kind,
                contains_reviewed_content=self._contains_reviewed(included),
                contains_corrected_content=self._contains_corrected(included),
                typography_signals=typography_summary,
            ),
        )

    def _build_footnote_chunk(
        self,
        document_id: str,
        page: BundlePage,
        note: NoteRecord,
        page_index: PageGraphIndex,
    ) -> RagChunk:
        """
        Build one footnote retrieval chunk from an accepted note object.

        Args:
            document_id: Owning document identifier.
            page: Page containing the note graph.
            note: Accepted note whose diplomatic text becomes chunk text.
            page_index: Typed page graph lookups.

        Returns:
            Page-local footnote chunk with marker and region linkage retained.

        """
        marker_span_records = [
            page_index.spans[span_id]
            for span_id in note.linked_marker_span_ids
            if span_id in page_index.spans
        ]
        trust_objects: list[NoteRecord | SpanRecord] = [note, *marker_span_records]
        provenance_objects: list[
            NoteRecord | SpanRecord | RegionRecord
        ] = list(trust_objects)
        region: RegionRecord | None = None
        if note.region_id is not None:
            region = page_index.regions.get(note.region_id)
            if region is not None:
                provenance_objects.append(region)
        typography_summary = self._typography_summary(marker_span_records)
        return RagChunk(
            chunk_id=f"footnote-{note.note_id}",
            chunk_type=ChunkType.FOOTNOTE,
            document_id=document_id,
            page_ids=[page.page_id],
            text=note.text_diplomatic,
            trust_state=self._aggregate_trust(trust_objects),
            source_object_ids=self._footnote_source_object_ids(note, region),
            provenance=self._aggregate_provenance(provenance_objects),
            typography_summary=typography_summary,
            note_summary=self._footnote_note_summary(note),
            retrieval_metadata=RetrievalMetadata(
                page_number=page.page_number,
                contains_reviewed_content=self._contains_reviewed(trust_objects),
                contains_corrected_content=self._contains_corrected(trust_objects),
                typography_signals=typography_summary,
            ),
        )

    def _ordered_region_lines(
        self,
        region: RegionRecord,
        page_index: PageGraphIndex,
    ) -> list[LineRecord]:
        """
        Resolve region line ids in accepted line_order sequence.

        Args:
            region: Region whose ``line_ids`` identify member lines.
            page_index: Typed page graph lookups.

        Returns:
            Lines belonging to the region sorted by ``line_order``.

        """
        lines = [
            page_index.lines[line_id]
            for line_id in region.line_ids
            if line_id in page_index.lines
        ]
        return sorted(lines, key=lambda line: line.line_order)

    def _ordered_region_spans(
        self,
        lines: list[LineRecord],
        page_index: PageGraphIndex,
    ) -> list[SpanRecord]:
        """
        Resolve span ids for region lines in graph order.

        Args:
            lines: Region lines ordered by ``line_order``.
            page_index: Typed page graph lookups.

        Returns:
            Spans referenced by the lines in line and span order.

        """
        spans: list[SpanRecord] = []
        for line in lines:
            spans.extend(
                page_index.spans[span_id]
                for span_id in line.span_ids
                if span_id in page_index.spans
            )
        return spans

    def _join_region_text(
        self,
        lines: list[LineRecord],
        page_index: PageGraphIndex,
    ) -> str:
        """
        Join diplomatic span text for one region in graph order.

        Args:
            lines: Region lines ordered by ``line_order``.
            page_index: Typed page graph lookups.

        Returns:
            Region text with one line per newline-separated segment.

        """
        line_texts: list[str] = []
        for line in lines:
            span_texts = [
                page_index.spans[span_id].text_diplomatic
                for span_id in line.span_ids
                if span_id in page_index.spans
            ]
            line_texts.append("".join(span_texts))
        return "\n".join(line_texts)

    def _aggregate_trust(
        self,
        objects: Sequence[
            RegionRecord | LineRecord | SpanRecord | NoteRecord
        ],
    ) -> TrustState:
        """
        Aggregate trust for included graph objects.

        Args:
            objects: Graph objects whose trust states contribute to the chunk.

        Returns:
            Corrected when any object is corrected, else reviewed when all are
            reviewed or corrected, else machine.

        """
        trust_states = [obj.trust_state for obj in objects]
        if any(state == TrustState.CORRECTED for state in trust_states):
            return TrustState.CORRECTED
        if trust_states and all(
            state == TrustState.REVIEWED for state in trust_states
        ):
            return TrustState.REVIEWED
        return TrustState.MACHINE

    def _contains_reviewed(
        self,
        objects: Sequence[
            RegionRecord | LineRecord | SpanRecord | NoteRecord
        ],
    ) -> bool:
        """
        Report whether any included object has human-reviewed trust.

        Args:
            objects: Graph objects contributing to the chunk.

        Returns:
            ``True`` when at least one object is reviewed or corrected.

        """
        return any(
            obj.trust_state in {TrustState.REVIEWED, TrustState.CORRECTED}
            for obj in objects
        )

    def _contains_corrected(
        self,
        objects: Sequence[
            RegionRecord | LineRecord | SpanRecord | NoteRecord
        ],
    ) -> bool:
        """
        Report whether any included object has human-corrected trust.

        Args:
            objects: Graph objects contributing to the chunk.

        Returns:
            ``True`` when at least one object is corrected.

        """
        return any(obj.trust_state == TrustState.CORRECTED for obj in objects)

    def _aggregate_provenance(
        self,
        objects: Sequence[
            RegionRecord | LineRecord | SpanRecord | NoteRecord
        ],
    ) -> RetrievalProvenance:
        """
        Union provenance pointers from included graph objects.

        Args:
            objects: Graph objects whose provenance contributes to the chunk.

        Returns:
            Deduplicated page, witness, and runner pointers in first-seen order.

        """
        source_page_ids: list[str] = []
        witness_ids: list[str] = []
        runner_ids: list[str] = []
        seen_pages: set[str] = set()
        seen_witnesses: set[str] = set()
        seen_runners: set[str] = set()
        for obj in objects:
            provenance = obj.provenance
            self._extend_unique(
                source_page_ids,
                seen_pages,
                [provenance.source_page_id],
            )
            self._extend_unique(
                witness_ids,
                seen_witnesses,
                provenance.witness_ids,
            )
            self._extend_unique(
                runner_ids,
                seen_runners,
                provenance.runner_ids,
            )
        return RetrievalProvenance(
            source_page_ids=source_page_ids,
            witness_ids=witness_ids,
            runner_ids=runner_ids,
        )

    def _extend_unique(
        self,
        target: list[str],
        seen: set[str],
        values: list[str],
    ) -> None:
        """
        Append unseen string values to a list in first-seen order.

        Args:
            target: Destination list receiving unique values.
            seen: Values already present in ``target``.
            values: Candidate values to append.

        """
        for value in values:
            if value not in seen:
                seen.add(value)
                target.append(value)

    def _source_object_ids(
        self,
        objects: Sequence[
            RegionRecord | LineRecord | SpanRecord | NoteRecord
        ],
    ) -> list[str]:
        """
        Collect stable graph object ids included in a region chunk.

        Args:
            objects: Graph objects contributing to the chunk.

        Returns:
            Object ids in inclusion order without duplicates.

        """
        object_ids: list[str] = []
        seen: set[str] = set()
        for obj in objects:
            object_id = self._object_id(obj)
            if object_id not in seen:
                seen.add(object_id)
                object_ids.append(object_id)
        return object_ids

    def _footnote_note_summary(self, note: NoteRecord) -> list[str]:
        """
        Build ordered note linkage ids for footnote retrieval consumers.

        Args:
            note: Accepted note whose linkage ids should be summarized.

        Returns:
            ``note_id``, linked marker span ids, then parent ``region_id`` when
            the note is region-scoped.

        """
        summary = [note.note_id, *note.linked_marker_span_ids]
        if note.region_id is not None:
            summary.append(note.region_id)
        return summary

    def _footnote_source_object_ids(
        self,
        note: NoteRecord,
        region: RegionRecord | None,
    ) -> list[str]:
        """
        Collect graph ids referenced by a footnote chunk.

        Args:
            note: Accepted note object for the chunk.
            region: Parent region when the note is region-scoped.

        Returns:
            Note, region, and marker ids in stable inclusion order.

        """
        object_ids: list[str] = [note.note_id]
        seen = {note.note_id}
        for span_id in note.linked_marker_span_ids:
            if span_id not in seen:
                seen.add(span_id)
                object_ids.append(span_id)
        if region is not None and region.region_id not in seen:
            object_ids.append(region.region_id)
        return object_ids

    def _typography_summary(self, spans: list[SpanRecord]) -> list[Typography]:
        """
        Collect distinct known typography signals from included spans.

        Args:
            spans: Spans whose typography may contribute retrieval facets.

        Returns:
            Unique non-default typography records in first-seen order.

        """
        summary: list[Typography] = []
        seen: set[str] = set()
        for span in spans:
            if not self._has_known_typography(span.typography):
                continue
            key = span.typography.model_dump_json()
            if key not in seen:
                seen.add(key)
                summary.append(span.typography)
        return summary

    def _has_known_typography(self, typography: Typography) -> bool:
        """
        Report whether typography carries at least one known facet.

        Args:
            typography: Span typography candidate for retrieval export.

        Returns:
            ``True`` when any facet is materially known rather than default.

        """
        if typography.font_families:
            return True
        if typography.font_size_points is not None:
            return True
        if typography.small_caps is not None:
            return True
        if typography.letter_spaced is not None:
            return True
        return any(
            facet != unknown
            for facet, unknown in (
                (typography.weight, FontWeight.UNKNOWN),
                (typography.slant, FontSlant.UNKNOWN),
                (typography.baseline_shift, BaselineShift.UNKNOWN),
            )
        )

    def _object_id(
        self,
        obj: RegionRecord | LineRecord | SpanRecord | NoteRecord,
    ) -> str:
        """
        Resolve the stable identifier for one graph object.

        Args:
            obj: Graph object whose id field should be returned.

        Returns:
            Stable object identifier for the given record type.

        """
        if isinstance(obj, RegionRecord):
            return obj.region_id
        if isinstance(obj, LineRecord):
            return obj.line_id
        if isinstance(obj, SpanRecord):
            return obj.span_id
        return obj.note_id
