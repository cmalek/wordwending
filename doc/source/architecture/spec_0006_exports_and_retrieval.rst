========================================
Spec 0006: Exports and Retrieval Views
========================================

Purpose
=======

Define the v1 consumer-facing export contracts for ``bochord``.

This spec covers:

- full-fidelity structured bundle JSON
- retrieval-oriented RAG JSON
- evidence-preserving Markdown
- footnote chunk behavior
- document-level stitched chunks
- provenance and trust-state propagation

Export Principles
=================

``bochord`` has two first-class consumer needs:

- human or agent reading
- deterministic software and retrieval pipelines

Therefore v1 exports split into three product views:

- ``bundle JSON``
- ``rag JSON``
- ``markdown``

Rules:

- ``bundle JSON`` is the primary consumer contract.
- ``rag JSON`` is a derived retrieval contract.
- ``markdown`` is a derived evidence-preserving reading view.
- No consumer should treat Markdown as source of truth.

Export Family 1: Bundle JSON
============================

Purpose
-------

``bundle JSON`` is the canonical software-facing export for one document run.

It should preserve enough structure and provenance for:

- deterministic downstream software
- audit and replay
- exact linking back to page graph and witness artifacts
- later regeneration of simpler exports

Required Top-Level Sections
---------------------------

The v1 document bundle JSON should include:

- document metadata
- run metadata
- page list
- evaluation summary
- export summary

Minimum top-level fields:

- ``document_id``
- ``bundle_schema_version``
- ``source``
- ``run``
- ``pages``
- ``evaluation_summary``
- ``exports``

Document Metadata
-----------------

Document metadata should include:

- stable ``document_id``
- source filename or source label
- source type such as ``pdf`` or ``image-set``
- page count
- optional source checksum or source identity digest
- bibliographic provenance
- acquisition provenance

Run Metadata
------------

Run metadata should include:

- stable ``run_id``
- run timestamp
- preparation recipe identity
- pass runner set and versions where available
- bundle schema version

Page Objects
------------

Each page object should include:

- ``page_id``
- page number
- prepared image metadata
- ``regions``
- ``lines``
- ``spans``
- ``notes``
- page-local evaluation summary
- page-local review summary
- links to raw witness artifacts

Graph Objects
-------------

Each graph object must carry:

- stable id
- trust state
- optional review scope summary
- provenance pointers

``region`` minimum fields:

- ``region_id``
- ``region_kind``
- bounding box
- reading-order index
- trust state
- provenance references

``line`` minimum fields:

- ``line_id``
- parent ``region_id``
- bounding box
- line order in region
- trust state
- provenance references

``span`` minimum fields:

- ``span_id``
- parent ``line_id``
- text
- style class
- bounding box
- trust state
- provenance references

``note`` minimum fields:

- ``note_id``
- ``note_kind`` such as ``footnote-block``
- note text or ordered note span refs
- linked marker span ids
- parent region id where applicable
- trust state
- provenance references

Provenance Contract
-------------------

Every exportable graph object must be traceable back to evidence.

Minimum provenance pointers:

- contributing raw witness artifact ids
- contributing pass runner ids
- source page id
- optional confidence or disagreement metadata

Review and Trust Contract
-------------------------

Bundle JSON must expose:

- current trust state per object
- review events affecting that object
- review-scope summaries where useful

This allows downstream consumers to filter for:

- machine-only content
- human-reviewed accepted content
- human-corrected content

Evaluation Contract
-------------------

Bundle JSON should include both:

- page-local evaluation outputs
- document-level summary outputs

Do not collapse separate score families into one opaque number.

Export Family 2: RAG JSON
=========================

Purpose
-------

``rag JSON`` is the retrieval-oriented derived view. It is flatter and easier to
index than full graph JSON, but must preserve links back to bundle truth.

Design Rules
------------

- Region-first chunking is mandatory.
- Footnotes are first-class retrievable chunks.
- Fixed token windows are not primary chunk boundaries.
- Document-level stitched chunks derive only from accepted page graph order.

Two RAG Tiers
-------------

V1 should emit two retrieval views:

- page-local chunks
- document-level stitched chunks

Each chunk must remain linked back to page-local truth.

Page-Local Chunk Types
----------------------

Required v1 page-local chunk types:

- ``region_chunk``
- ``footnote_chunk``

Optional later:

- ``table_chunk``

``region_chunk`` rules:

- derived from one region at a time
- may summarize contained line and span content
- may include structured style summary

``footnote_chunk`` rules:

- derived from one note object
- searchable independently
- linked to marker span ids
- linked to owning page and, when possible, parent region

Required RAG Chunk Fields
-------------------------

Every RAG chunk should include at least:

- ``chunk_id``
- ``chunk_type``
- ``document_id``
- ``page_id`` or page reference list
- ``text``
- ``trust_state``
- ``source_object_ids``
- ``provenance``
- ``style_summary``
- ``note_summary``
- ``retrieval_metadata``

Suggested retrieval metadata fields:

- reading-order position
- page number
- region kind
- whether chunk contains reviewed or corrected content
- whether chunk is note-derived
- whether chunk contains style signals such as italic or bold

Footnote Retrieval Contract
---------------------------

Footnotes must be separately retrievable and also recoverable in context.

Each footnote chunk must link to:

- its ``note_id``
- one or more marker ``span_id`` values
- page id
- parent region id when available

This allows an agent to:

- find the note directly
- recover the local main-text context later

Document-Level Stitched Chunks
------------------------------

Purpose:

- support retrieval across page breaks and section flow
- avoid forcing cross-page questions to depend on page-local chunk searches only

Rules:

- stitched chunks derive only from accepted page graph order
- never derive stitched chunks from raw OCR text streams
- stitched chunks must preserve references back to component page-local chunks

Each stitched chunk should include:

- ``stitched_chunk_id``
- ordered list of component ``chunk_id`` values
- ordered page references
- stitched text
- aggregated trust state
- provenance pointers back to component bundle objects

Trust Propagation for Retrieval
-------------------------------

Chunk trust must be explicit.

Suggested rule:

- if any included object is ``corrected``, chunk trust is at least
  ``corrected``
- else if all included reviewed objects are accepted and no machine-only content
  remains, chunk trust may be ``reviewed``
- otherwise chunk trust remains ``machine``

The implementation may also expose finer trust summaries, but the three core
states must remain visible.

Export Family 3: Markdown
=========================

Purpose
-------

Markdown is the human and agent reading view.

It should be easy to read while still preserving important evidence.

Markdown Design Rules
---------------------

- Preserve note markers explicitly.
- Preserve note bodies explicitly.
- Preserve italic, bold, and superscript where recoverable.
- Preserve important region boundaries when flattening would hide meaning.
- Avoid pretty reflow that destroys evidence boundaries.

Markdown should be produced from the accepted structured layer, not from raw OCR
text streams.

Required Markdown Behaviors
---------------------------

Main-text rendering:

- render region content in accepted reading order
- keep meaningful paragraph or region boundaries
- render italic and bold with normal Markdown emphasis when safe
- render superscript in a consistent explicit convention

Footnote rendering:

- preserve inline note markers in main text
- render note bodies in separate note section or page-local note section
- keep stable linkage between marker and note body

Style rendering:

- use lightweight readable markup
- do not invent visually fancy formatting that loses source alignment

Region rendering:

- for ordinary prose, natural Markdown paragraphs are acceptable
- for special regions such as tables or marginalia, prefer explicit markers or
  placeholders over misleading prose flattening

What Markdown Must Not Do
-------------------------

Markdown must not:

- silently merge footnotes into main prose
- silently drop style signals that later parsing or reading depends on
- rewrite text to improve readability at the cost of evidence
- become the only preserved representation of a page

ID and Reference Stability
==========================

All export families must preserve stable referenceability.

Required stable ids:

- ``document_id``
- ``page_id``
- ``region_id``
- ``line_id``
- ``span_id``
- ``note_id``
- ``chunk_id``
- ``stitched_chunk_id`` where applicable

The stable id contract exists to support:

- overlays
- audit and review history
- retrieval provenance
- deterministic downstream joins
- diffing between runs

Recommended File Outputs
========================

V1 should write, at minimum:

- one full document ``bundle.json``
- one document ``rag.jsonl`` or equivalent chunk stream
- one document ``stitched_chunks.jsonl`` or equivalent
- one document ``document.md``
- optional page-local Markdown views for inspection

Non-Goals
=========

V1 export work should not attempt:

- perfect typography reproduction
- lossless round-trip from Markdown back to graph
- table cell semantics beyond region-level placeholders
- generic search-engine schema support for every downstream system

Future Extension Points
=======================

Likely later extensions:

- table-specific retrieval chunks
- richer style summaries
- entity or citation overlays on top of graph chunks
- multiple Markdown rendering styles for different operator audiences
