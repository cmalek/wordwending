=========================
Detailed OCR Process
=========================

Purpose
=======

This document explains the intended ``bochord`` process end to end in operator
and engineering terms.

The core rule is simple:

OCR produces evidence. ``bochord`` preserves that evidence, compares competing
passes, evaluates them against gold slices, and only then derives normalized
page graphs and exports.

Stage 1: Acquire Source
=======================

Inputs are expected to be image-based source materials:

- scanned PDFs
- page image directories
- single page images for focused experiments

This stage records source identity and run configuration, but does not yet make
claims about text.

Operator notes:

- Prefer immutable source inputs.
- Do not hand-edit source PDFs or source images in place.
- Treat source naming as provenance, not decoration.

Stage 2: PDF-to-Image Preparation
=================================

For scanned PDFs, ``bochord`` must prepare page images before any OCR pass runs.
This is a first-class stage, not a disposable helper.

Responsibilities:

- render one stable page image per page
- record render recipe and output dimensions
- preserve page ordering
- keep deterministic page identity
- avoid hidden image cleanup that cannot be reconstructed later

Preparation outputs feed every later pass, so they must be reproducible.

Operator notes:

- If a render recipe changes, treat resulting outputs as a new run.
- Record DPI or target resolution explicitly.
- Preserve the prepared image artifact; do not assume the source PDF alone is
  enough for later debugging.

Stage 3: Run Competing Passes
=============================

Each page may run one or more pass families:

- text recognition
- line or layout segmentation
- style extraction
- table-region detection
- evaluation helper passes

Each runner writes raw witness artifacts unchanged.

Initial v1 strategy:

- ``olmocr`` for difficult text recognition
- ``kraken`` for structured historical OCR evidence and coordinate-rich outputs

Operator notes:

- Never let a runner write directly into the canonical page graph.
- Preserve pass-local metadata such as model id, config, and confidence values.
- When comparing runners, keep both outputs in the same bundle when possible.

Stage 4: Align Evidence
=======================

Raw pass outputs use different formats and coordinate schemes. ``bochord`` must
normalize them into shared page space before graph construction.

Alignment work includes:

- normalizing coordinate frames
- grouping related regions, lines, and spans
- linking note markers to note blocks when possible
- recording disagreements between passes

Operator notes:

- Alignment is derived logic and may improve over time.
- Raw witness artifacts should make graph rebuilds possible without rerunning
  OCR engines.

Stage 5: Build Page Graph
=========================

The normalized page graph is the first canonical derived representation for one
page.

V1 node kinds:

- ``region``
- ``line``
- ``span``
- ``note``

V1 style classes:

- ``plain``
- ``italic``
- ``bold``
- ``superscript``
- ``subscript``
- ``footnote-marker``

``note`` is used for bodies such as ``footnote-block``.

Operator notes:

- The page graph is still evidence-rich and provenance-aware.
- It is not yet a philological interpretation layer.

Stage 6: Evaluate Against Gold and Watchlists
=============================================

Evaluation is mandatory architecture, not optional benchmarking.

Score families remain separate:

- text
- structure
- style

Typical watchlists:

- macrons
- ligatures
- thorn and eth
- note markers
- italic spans
- bold spans
- superscripts

Operator notes:

- Do not trust a blended score.
- Review pages that pass text but fail structure or style.
- Expand gold slices gradually, not all at once.

Stage 7: Apply Overlays
=======================

Human corrections belong in overlays, not in-place mutations of raw OCR text.

Overlay examples:

- corrected span text
- corrected style class
- corrected note linkage
- accepted or rejected region interpretation

Operator notes:

- Overlays should be small, explicit, and diffable.
- Avoid manual edits that bypass overlay storage.

Stage 8: Export
===============

Exports are downstream-friendly views derived from:

- raw witness artifacts
- normalized page graph
- overlays

Examples:

- page markdown
- page plain text
- document-level stitched text
- JSON exports for downstream consumers

Operator notes:

- Exports are convenience products, not source-of-truth artifacts.
- Rebuild exports when graph or overlay logic changes.
