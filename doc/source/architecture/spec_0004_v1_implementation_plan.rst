=====================================
Spec 0004: Ordered V1 Implementation
=====================================

Purpose
=======

Provide a build order that follows the ADR chain and minimizes wasted work.

Phase 1: Contracts and Skeleton
===============================

Ship first:

- package-level architecture docs
- run config models
- page classification models
- bundle manifest models
- page graph models
- pass runner protocol or abstract base
- empty orchestrator skeleton

Exit criteria:

- type-stable models exist
- one fake pass runner can execute through the orchestrator
- bundle skeleton can be written to disk

Phase 2: Raw Witness Infrastructure
===================================

Ship next:

- page preparation service
- page assessment and page classification
- witness artifact storage rules
- pass runner registry
- deterministic page bundle writing

Exit criteria:

- one input document produces page folders and raw witness artifacts
- page-level preparation and classification metadata are persisted
- rerun behavior is deterministic

Phase 3: First Engines
======================

Ship next:

- ``olmocr`` runner
- ``kraken`` runner
- shared runner result normalization

Exit criteria:

- both runners can emit raw witness artifacts for the same page
- page manifests record both passes correctly

Phase 4: Alignment and Graph Build
==================================

Ship next:

- shared coordinate normalization
- evidence alignment logic
- graph builder for ``region/line/span/note``

Exit criteria:

- one page with two runners yields one derived page graph
- footnote marker and note block representation works

Phase 5: Evaluation
===================

Ship next:

- gold slice schema
- family-specific scoring
- review flags
- run summaries

Exit criteria:

- same page graph can be scored against supplied gold data
- review flags are emitted separately from scores

Phase 6: Overlay and Export
===========================

Ship next:

- overlay schema
- overlay application service
- page and document export views

Exit criteria:

- human corrections can be layered without mutating raw witness data
- downstream consumers can read stable normalized exports

Phase 7: Retrieval Views
========================

Ship next:

- page-local RAG chunk generation
- footnote chunk generation
- document-level stitched chunk generation from accepted page graph order

Exit criteria:

- page-local chunks link back to graph truth
- footnotes are independently retrievable
- stitched chunks exist without reading raw OCR streams directly

Phase 8: Hardening
==================

Only after earlier phases work:

- richer table handling
- additional engines or runners
- packaging and CLI ergonomics
- benchmark corpus growth

Recommended Initial CLI
=======================

Keep CLI small:

- ``bochord run``
- ``bochord eval``
- ``bochord inspect-bundle``
- ``bochord version``

Avoid v1 CLI sprawl. Most complexity belongs in config and services.
