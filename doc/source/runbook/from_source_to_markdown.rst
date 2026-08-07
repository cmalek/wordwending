================================
From Source Material to Markdown
================================

Purpose
=======

This guide is the operator walkthrough from scanned source material toward
evidence-preserving Markdown. It states what ``wordwending`` can do today, what
remains manual or deferred, and where human correction fits.

.. note::

   ``wordwending`` is early, evolving software. Commands and bundle assembly paths
   described here are honest for the current release; gaps are called out
   explicitly rather than papered over.

Inputs
======

Supported source shapes:

- scanned PDFs
- directories of page images (for example ``.jp2``, ``.png``, ``.tif``)
- zip archives containing page images

Treat inputs as immutable provenance. Do not hand-edit source PDFs or source
images in place.

Stage Map
=========

The intended end-to-end spine:

1. **prepare** (``wordwending prepare``) — render stable page images and record
   preparation recipe
2. **run** (``wordwending run``) — execute OCR runner passes; preserve raw witness
   artifacts
3. **assemble** (``wordwending assemble``) — adapt raw witnesses, merge, and
   write a ``DocumentBundle`` tree from an operator manifest
4. **export** (``wordwending export``) — derive bundle JSON, RAG JSONL, and Markdown
   from an accepted ``DocumentBundle``

Supporting commands:

- ``wordwending prepare`` — stage 1: PDF or page images to prepared page images
- ``wordwending run`` — stage 2: OCR runner passes and raw witness artifacts
- ``wordwending assemble`` — stage 3: manifest-driven bundle assembly
- ``wordwending inspect-bundle`` — summarize an assembled bundle on disk
- ``wordwending review apply`` — append overlay review events to a bundle page
- ``wordwending review materialize`` — replay overlay history into current state
- ``wordwending version`` — confirm installed CLI
- ``wordwending settings`` — inspect effective configuration
- ``wordwending eval`` — score one page against gold
- ``wordwending eval-cohorts`` — batch evaluation across held-out slices

For stage theory and engineering detail, see :doc:`/runbook/ocr_process`.

Stage 3: Assemble from Prepare/Run Outputs
============================================

After ``run`` completes, raw witness artifacts live under the bundle root
(typically ``witnesses/...`` relative paths recorded in the run manifest).
Assemble does **not** auto-scan the tree: the operator writes an
``AssembleManifest`` JSON listing each page's prepared image and relative
witness paths, then runs:

.. code-block:: bash

   wordwending assemble --bundle-root path/to/bundle-root --manifest path/to/manifest.json

Paths inside the manifest are **relative posix strings** resolved against
``--bundle-root``. After assemble, ``document-bundle.json`` at the bundle root
is the loadable ``DocumentBundle`` input for ``wordwending export``; use
``inspect-bundle`` to verify the written tree (and, after ``export``, list
``exports/*`` paths):

.. code-block:: bash

   wordwending inspect-bundle --bundle-root path/to/bundle-root

Multi-witness merge (olmOCR + kraken) runs on the same assemble path: list
two or more witness artifact paths per page in the manifest. ``run`` supports
both ``olmocr`` and ``kraken`` hosted runners; assemble adapts each witness,
merges through ``AbstainingMergeService``, and persists merge flags. Use
``inspect-bundle`` to inspect disagreement flags before review.

Provisional Path: Export When You Have a DocumentBundle
=======================================================

When a valid ``DocumentBundle`` JSON already exists (for example from tests,
fixtures, or manual assembly), export derived views with:

.. code-block:: bash

   wordwending export path/to/document-bundle.json --bundle-root path/to/bundle-root

Under ``bundle-root``, ``export`` writes at least:

- ``exports/document.md`` — evidence-preserving reading view
- ``exports/bundle.json`` — full-fidelity structured export
- ``exports/rag.jsonl`` — retrieval-oriented chunks
- ``exports/stitched_chunks.jsonl`` — document-level stitched chunks

This is the **provisional machine path**: Markdown reflects the bundle as
assembled, without human overlay acceptance.

Corrected Path: Review Overlays
===============================

Philological work continues after the first machine bundle. Human corrections
belong in overlays and review tasks, not in-place edits to raw OCR text.

Operator workflow:

1. Inspect prepared images, raw witnesses, and merge flags
   (:doc:`/runbook/operator_notes`, ``inspect-bundle``).
2. Apply review concepts from :doc:`/architecture/spec_0005_human_markup`
   (diplomatic text, typography, note linkage, trust states). Multi-witness
   assemble projects merge disagreements into dimension-specific **evaluation
   flags** (``evaluation/flags.json`` and the page evaluation summary)—use
   ``inspect-bundle`` to read them. Spec 0005 ``ReviewTask`` packets are **not**
   auto-emitted by ``assemble`` or the CLI; operators hand-author a
   ``PageOverlay`` JSON (library code exposes
   ``MergeFlagReviewService.build_review_tasks`` for separate workflows).
3. Prepare a ``PageOverlay`` JSON with review events (Spec 0014).
4. Append events and materialize overlay state:

.. code-block:: bash

   wordwending review apply \
     --bundle-root path/to/bundle-root \
     --overlay path/to/page-overlay.json \
     --page-id PAGE_ID

   wordwending review materialize \
     --bundle-root path/to/bundle-root \
     --page-id PAGE_ID

5. Overlay acceptance is persisted under the page tree. **Graph rebase**—applying
   accepted overlay corrections back onto the accepted page graph—is deferred
   (Spec 0004 Phase 8 exit). ``wordwending export`` reads ``DocumentBundle`` page
   graphs only; it does **not** consume ``overlays/review_events.jsonl`` or
   ``overlays/current_state.json`` until rebase lands. Re-running export after
   ``review apply`` does not regenerate Markdown from overlay edits.

Append-only overlay history is preserved under ``overlays/review_events.jsonl``;
``review materialize`` rebuilds ``overlays/current_state.json`` from that log.

What Markdown Is and Is Not
===========================

Per :doc:`/architecture/spec_0006_exports_and_retrieval`:

- Markdown is a **derived**, evidence-preserving reading view for humans and
  agents.
- Markdown is **not** source of truth. The canonical software contract is
  bundle JSON plus preserved witness artifacts and overlays.
- Rebuild Markdown when graph logic or export rules change, or after graph rebase
  incorporates accepted overlays into the bundle graph.

.. _what-is-missing:

Spec 0004 Phase 4 Status
==========================

On the current spine, the v1 plan **Phase 4 full bullets (Waves A+C+D)** are met
for a representative page traveling end to end without hand-edited
``DocumentBundle`` JSON:

- **Two real hosted runners on assemble** — olmOCR (provisional text) and kraken
  (``HuggingFaceKrakenRunner``) adapt through ``wordwending assemble`` with
  multi-witness merge and flag persistence
- **Raw witnesses preserved** — exact runner response bytes under the bundle tree
- **Derived page graph** — region/line/span/note scaffold via merge on assemble
  (provisional text-first geometry on both runners today)
- **Score, evaluation flags, overlay CLI, export** — ``eval`` / ``eval-cohorts``;
  merge flags → dimension-specific **evaluation flags**
  (``evaluation/flags.json``); operators hand-author ``PageOverlay`` for
  ``review apply`` / ``review materialize``; ``export`` for JSON and Markdown
  from bundle page graphs

**Phase 6 is COMPLETE**: ``PassRunner`` Protocol extracted from the olmOCR and
kraken hosted adapters, ``PassRunnerRegistry`` resolves by ``runner_id``, and the
execution spine / CLI are typed to the Protocol. Fake runners remain test
doubles only.

This is **not** a claim that Spec 0004 Phase 5 (candidate bake-off) or Phase 10
(operational hardening) are complete. **Phase 5 is explicitly NOT COMPLETE**:
the Wave F harness exists, but Spec exit criteria (cost/license/operability
scoring and full held-out corpus) remain deferred. **Phase 10 is explicitly
NOT COMPLETE**: Wave H ships an **ops skeleton only** (resume ledger +
inspect checksums + ``wordwending endpoints`` lifecycle CLI with optional
``--ensure-endpoints`` on ``run``/``bakeoff``); Spec exit remains deferred
(see below). Spec 0004 Phase 4's
**coordinate-rich second-runner** bullet remains **deferred**: kraken on the
spine uses conservative/text-first geometry until Phase 7 alignment exit
matures coordinate-rich merge.

What Is Missing
===============

These pieces are planned but **not** available or **not complete** today:

- **Standalone merge CLI** — merge runs inside ``assemble``; there is no separate
  ``wordwending merge`` command
- **Auto manifest** — assemble requires an operator-written ``AssembleManifest``;
  the CLI does not scan prepare/run output trees automatically
- **Full DocumentRunOrchestrator** — prepare → run → assemble → review → export
  is staged by separate commands, not one orchestrated run id
- **Phase 5 bake-off — NOT COMPLETE** — Wave F ships an offline harness
  (``BakeoffService`` / ``wordwending bakeoff``) that writes
  ``bakeoff-matrix-v1.json`` for real schema candidates (``olmocr`` +
  ``kraken``) using ``EvaluationService`` metrics plus latency/failure and
  license/cost/operability **placeholders**. Deferred before any Phase 5
  COMPLETE claim: cost/license/operability scoring, full corpus held-out
  slices, and live bake-off evidence beyond recorded fixtures
- **Graph rebase / overlay → export** — ``review apply`` persists overlays, but
  ``export`` reads bundle page graphs only until rebase lands
- **Phase 10 operations — NOT COMPLETE (ops skeleton only)** — Wave H ships:

  - ``run`` resume ledger (``runner-resume-ledger.json`` / ``--force``)
  - ``inspect-bundle`` verification of digests already recorded in bundle-layout
    metadata (``checksum: … OK|FAIL|SKIPPED``)
  - ``wordwending endpoints up|down|status`` lifecycle CLI (pause-default
    ``down``, ``--delete`` to destroy; HF scale-to-zero + local idle ledger
    that pauses only; catalog pins required before live HF)
  - ``--ensure-endpoints`` on ``run`` and ``bakeoff`` (fail-closed ensure +
    in-process URL overlay)

  **Deferred before any Phase 10 COMPLETE claim:** full Hugging Face deploy/ops
  beyond lifecycle scaffolding (health-check automation, queueing policy,
  quotas UX), cost controls, corpus regression gates, and operator calibration
  monitoring. Do **not** mark Spec 0004 Phase 10 COMPLETE.

Related Runbooks
================

- :doc:`/overview/installation` — clone, environment, and editable install
- :doc:`/runbook/huggingface_setup` — model endpoint access for ``run``
- :doc:`/runbook/ocr_process` — full stage-by-stage OCR architecture
- :doc:`/runbook/operator_notes` — short preservation and triage rules
- :doc:`/runbook/gold_annotation` — gold slice protocol for ``eval`` /
  ``eval-cohorts``
