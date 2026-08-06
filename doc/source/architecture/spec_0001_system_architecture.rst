=================================
Spec 0001: V1 System Architecture
=================================

Purpose
=======

Define the minimal v1 architecture that satisfies the accepted ADR chain.

Core Services
=============

The v1 codebase should model real workflow boundaries as cohesive service
classes:

- ``DocumentRunOrchestrator``
- ``PagePreparationService``
- ``PassRunnerRegistry``
- ``PageAlignmentService``
- ``PageGraphBuilder``
- ``EvaluationService``
- ``OverlayService``
- ``BundleWriter``

Recommended execution flow:

1. Load run config and source document
2. Record bibliographic and acquisition provenance for the source document
3. Prepare deterministic page images from source PDF or source image set
4. For each page, execute configured pass runners
5. Persist raw witness artifacts
6. Align evidence into shared coordinates
7. Build derived page graph
8. Evaluate against gold data or watchlists when configured
9. Apply overlays when present
10. Write page bundle and document manifests

Suggested Python package layout:

- ``wordwending.models`` for dataclasses or Pydantic models
- ``wordwending.services`` for orchestration and business logic
- ``wordwending.cli`` for user-facing command surfaces

Service Boundaries
==================

``DocumentRunOrchestrator``
    Thin public facade for one document run. Owns run sequencing and delegates
    page-local work.

``PagePreparationService``
    Responsible for deterministic page image materialization from PDF or source
    image inputs, including page identity, render recipe provenance, and stable
    output dimensions.

``PassRunnerRegistry``
    Resolves configured pass runners and their order.

``PageAlignmentService``
    Normalizes raw pass coordinates into shared page space and computes evidence
    relationships.

``PageGraphBuilder``
    Converts aligned evidence into normalized ``region/line/span/note`` graph
    data.

``EvaluationService``
    Computes score families, watchlist metrics, and review flags.

``OverlayService``
    Applies human corrections as explicit overlays without mutating raw witness
    inputs.

``BundleWriter``
    Writes deterministic bundle files and manifests.

``SourceProvenanceService``
    Captures bibliographic and acquisition provenance for source documents and
    attaches it to bundle outputs.

Non-Goals for V1
================

V1 should not attempt:

- full document-semantic interpretation
- general table cell reconstruction
- automatic full-corpus style taxonomy discovery
- model training platform work
- distributed workflow scheduling
