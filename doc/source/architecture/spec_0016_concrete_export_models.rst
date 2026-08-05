==========================================
Spec 0016: Concrete Bundle and RAG Models
==========================================

Purpose
=======

Define canonical Pydantic JSON shapes while keeping normative architecture in
ADRs and specs.

Bundle Contract
===============

``DocumentBundle`` records schema version, source, bibliographic and acquisition
provenance, immutable run metadata, pages, evaluation, and export paths. The
bundle and run schema versions must match; page ids are unique and source page
count must match exported pages when known.

``PreparedPage`` binds the canonical image to source artifact id, checksum,
preparation recipe, raster dimensions/DPI, coordinate-space id, ordered transform
chain, and optional prepared units. Boxes, polygons, and baselines always name a
coordinate space so source, prepared-page, and subdivision geometry cannot be
silently mixed.

Each page graph has unique region, line, span, and note ids. Parent/child,
containment, marker-link, and reading-order references must resolve during model
validation. Machine and merge confidence are bounded from zero through one.

Text spans carry diplomatic and deterministic normalized text, orthogonal
``Typography``, independent semantic roles, provenance, trust, and
dimension-specific review summaries.

RAG Contract
============

``RagDocument`` records schema version and chunking recipe. Page-local
``RagChunk`` and cross-page ``StitchedChunk`` carry ordered page ids, source
object ids, text, trust, and ``RetrievalProvenance`` with source pages,
witnesses, and runners. Page-local chunks declare exactly one page id and
``RetrievalProvenance.source_page_ids`` must be that same singleton in the same
order. Stitched chunks declare two or more distinct page ids in first-seen order
and ``RetrievalProvenance.source_page_ids`` must list those same ids in that
same order. ``RagDocument`` additionally requires each stitched chunk's
``page_ids`` to equal the ordered distinct union of its component chunks'
provenance page ids.

V1 retrieval chunks are provisional region, note, and table views. Dictionary
entries, grammar sections, parallel Old English/translation records, and
TEI-inspired semantic objects remain downstream transformations until their
boundaries can be derived and evaluated reliably. The canonical page graph is
not forced into one document-specific ontology.

Contract Governance
===================

Accepted ADRs and specs are normative. Pydantic models implement those
contracts; generated JSON Schema and contract tests prove parity. If prose and
code diverge, resolve the architecture decision first, then update both in the
same change. Code does not silently redefine an accepted spec.
