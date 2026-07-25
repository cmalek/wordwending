========================================================
ADR 0002: Top-Level Artifact Is Document Bundle Per Run
========================================================

:Status: Accepted
:Date: 2026-07-25

Context
=======

Plain OCR text is too lossy for these documents. ``bochord`` must preserve
multiple evidence layers and allow later recomputation without rerunning every
model.

Decision
========

The top-level artifact is a document bundle containing page bundles.

Each document bundle records one run over one source document and contains:

- source document metadata
- rendered page images
- one page bundle per processed page
- run-level metrics and manifests
- optional overlays and exports

Each page bundle is the unit of page-local truth and stores:

- raw witness artifacts from each pass
- derived normalized page graph
- evaluation outputs
- human overlay edits
- page-level exports

Consequences
============

- v1 can optimize for page-local correctness without pretending to solve
  whole-book reasoning up front.
- Document-level reconciliation can be added later as a stitching step.
- Storage layout must support deterministic rebuilds from raw pass artifacts.
