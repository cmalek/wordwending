# Copyright (C) 2026 Chris Malek.
"""Derive retrieval chunks and Markdown from accepted document bundles."""

from __future__ import annotations

from typing import TYPE_CHECKING

from bochord.models import (
    BundlePage,
    ChunkType,
    DocumentBundle,
    LineRecord,
    NoteRecord,
    RagChunk,
    RagDocument,
    RegionRecord,
    RetrievalMetadata,
    RetrievalProvenance,
    SpanRecord,
    TrustState,
    Typography,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

#: Persisted retrieval schema version for page-local chunk exports.
RAG_SCHEMA_VERSION = "1.0.0"

#: Reproducible recipe identifier for page-local region and footnote chunking.
PAGE_REGIONS_CHUNKING_RECIPE_ID = "page-regions-v1"


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
        return RagDocument(
            schema_version=RAG_SCHEMA_VERSION,
            chunking_recipe_id=PAGE_REGIONS_CHUNKING_RECIPE_ID,
            document_id=bundle.document_id,
            chunks=chunks,
            stitched_chunks=[],
        )

    def _build_page_indexes(
        self,
        page: BundlePage,
    ) -> dict[str, LineRecord | SpanRecord | RegionRecord]:
        """
        Index page graph objects by stable identifier.

        Args:
            page: Accepted page graph whose objects will be resolved by id.

        Returns:
            Lookup table mapping graph ids to their accepted records.

        """
        index: dict[str, LineRecord | SpanRecord | RegionRecord] = {}
        for region in page.regions:
            index[region.region_id] = region
        for line in page.lines:
            index[line.line_id] = line
        for span in page.spans:
            index[span.span_id] = span
        return index

    def _build_region_chunk(
        self,
        document_id: str,
        page: BundlePage,
        region: RegionRecord,
        page_index: dict[str, LineRecord | SpanRecord | RegionRecord],
    ) -> RagChunk:
        """
        Build one region retrieval chunk from accepted graph order.

        Args:
            document_id: Owning document identifier.
            page: Page containing the region graph.
            region: Accepted region whose lines and spans supply chunk text.
            page_index: Page graph lookup keyed by object id.

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
        return RagChunk(
            chunk_id=f"region-{region.region_id}",
            chunk_type=ChunkType.REGION,
            document_id=document_id,
            page_ids=[page.page_id],
            text=self._join_region_text(lines, page_index),
            trust_state=self._aggregate_trust(included),
            source_object_ids=self._source_object_ids(included),
            provenance=self._aggregate_provenance(included),
            typography_summary=self._typography_summary(spans),
            retrieval_metadata=RetrievalMetadata(
                reading_order_index=region.reading_order_index,
                page_number=page.page_number,
                region_kind=region.region_kind,
                contains_reviewed_content=self._contains_reviewed(included),
                contains_corrected_content=self._contains_corrected(included),
                typography_signals=self._typography_summary(spans),
            ),
        )

    def _build_footnote_chunk(
        self,
        document_id: str,
        page: BundlePage,
        note: NoteRecord,
        page_index: dict[str, LineRecord | SpanRecord | RegionRecord],
    ) -> RagChunk:
        """
        Build one footnote retrieval chunk from an accepted note object.

        Args:
            document_id: Owning document identifier.
            page: Page containing the note graph.
            note: Accepted note whose diplomatic text becomes chunk text.
            page_index: Page graph lookup keyed by object id.

        Returns:
            Page-local footnote chunk with marker and region linkage retained.

        """
        marker_spans = [
            page_index[span_id]
            for span_id in note.linked_marker_span_ids
            if span_id in page_index
        ]
        trust_objects: list[NoteRecord | SpanRecord] = [note]
        trust_objects.extend(
            span for span in marker_spans if isinstance(span, SpanRecord)
        )
        provenance_objects: list[
            NoteRecord | SpanRecord | RegionRecord
        ] = list(trust_objects)
        region: RegionRecord | None = None
        if note.region_id is not None and note.region_id in page_index:
            candidate = page_index[note.region_id]
            if isinstance(candidate, RegionRecord):
                region = candidate
                provenance_objects.append(region)
        return RagChunk(
            chunk_id=f"footnote-{note.note_id}",
            chunk_type=ChunkType.FOOTNOTE,
            document_id=document_id,
            page_ids=[page.page_id],
            text=note.text_diplomatic,
            trust_state=self._aggregate_trust(trust_objects),
            source_object_ids=self._footnote_source_object_ids(note, region),
            provenance=self._aggregate_provenance(provenance_objects),
            note_summary=[note.note_id, *note.linked_marker_span_ids],
        )

    def _ordered_region_lines(
        self,
        region: RegionRecord,
        page_index: dict[str, LineRecord | SpanRecord | RegionRecord],
    ) -> list[LineRecord]:
        """
        Resolve region line ids in accepted line_order sequence.

        Args:
            region: Region whose ``line_ids`` identify member lines.
            page_index: Page graph lookup keyed by object id.

        Returns:
            Lines belonging to the region sorted by ``line_order``.

        """
        lines: list[LineRecord] = []
        for line_id in region.line_ids:
            record = page_index.get(line_id)
            if isinstance(record, LineRecord):
                lines.append(record)
        return sorted(lines, key=lambda line: line.line_order)

    def _ordered_region_spans(
        self,
        lines: list[LineRecord],
        page_index: dict[str, LineRecord | SpanRecord | RegionRecord],
    ) -> list[SpanRecord]:
        """
        Resolve span ids for region lines in graph order.

        Args:
            lines: Region lines ordered by ``line_order``.
            page_index: Page graph lookup keyed by object id.

        Returns:
            Spans referenced by the lines in line and span order.

        """
        spans: list[SpanRecord] = []
        for line in lines:
            for span_id in line.span_ids:
                record = page_index.get(span_id)
                if isinstance(record, SpanRecord):
                    spans.append(record)
        return spans

    def _join_region_text(
        self,
        lines: list[LineRecord],
        page_index: dict[str, LineRecord | SpanRecord | RegionRecord],
    ) -> str:
        """
        Join diplomatic span text for one region in graph order.

        Args:
            lines: Region lines ordered by ``line_order``.
            page_index: Page graph lookup keyed by object id.

        Returns:
            Region text with one line per newline-separated segment.

        """
        line_texts: list[str] = []
        for line in lines:
            span_texts: list[str] = []
            for span_id in line.span_ids:
                record = page_index.get(span_id)
                if isinstance(record, SpanRecord):
                    span_texts.append(record.text_diplomatic)
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
            state in {TrustState.REVIEWED, TrustState.CORRECTED}
            for state in trust_states
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
        Collect distinct typography signals from included spans.

        Args:
            spans: Spans whose typography may contribute retrieval facets.

        Returns:
            Unique typography records in first-seen order.

        """
        summary: list[Typography] = []
        seen: set[str] = set()
        for span in spans:
            key = span.typography.model_dump_json()
            if key not in seen:
                seen.add(key)
                summary.append(span.typography)
        return summary

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
