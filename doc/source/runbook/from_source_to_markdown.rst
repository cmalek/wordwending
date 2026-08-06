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
3. **merge / assemble** — combine passes into a ``DocumentBundle`` (not yet a
   CLI; see :ref:`what-is-missing`)
4. **export** (``wordwending export``) — derive bundle JSON, RAG JSONL, and Markdown
   from an accepted ``DocumentBundle``

Supporting commands:

- ``wordwending prepare`` — stage 1: PDF or page images to prepared page images
- ``wordwending run`` — stage 2: OCR runner passes and raw witness artifacts
- ``wordwending version`` — confirm installed CLI
- ``wordwending settings`` — inspect effective configuration
- ``wordwending eval`` — score one page against gold
- ``wordwending eval-cohorts`` — batch evaluation across held-out slices

For stage theory and engineering detail, see :doc:`/runbook/ocr_process`.

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

Corrected Path (Conceptual)
===========================

Philological work continues after the first machine bundle. Human corrections
belong in overlays and review tasks, not in-place edits to raw OCR text.

Conceptual workflow (no dedicated review CLI yet):

1. Inspect prepared images and raw witnesses first (:doc:`/runbook/operator_notes`).
2. Apply review concepts from :doc:`/architecture/spec_0005_human_markup`
   (diplomatic text, typography, note linkage, trust states).
3. Record accepted changes through overlay services
   ``wordwending.services.review_markup`` and ``wordwending.services.review_overlay``.
4. Rebuild the page graph and ``DocumentBundle`` with accepted overlay updates.
5. Run ``wordwending export`` again to regenerate ``exports/document.md``.

Until review and assemble commands ship, overlay application and bundle
rebuild may require library-level or manual steps.

What Markdown Is and Is Not
===========================

Per :doc:`/architecture/spec_0006_exports_and_retrieval`:

- Markdown is a **derived**, evidence-preserving reading view for humans and
  agents.
- Markdown is **not** source of truth. The canonical software contract is
  bundle JSON plus preserved witness artifacts and overlays.
- Rebuild Markdown whenever graph logic, overlays, or export rules change.

.. _what-is-missing:

What Is Missing
===============

These pieces are planned but **not** available as operator CLI today:

- **Assemble ``B*``** — orchestration from prepare/run outputs to a materialized
  ``DocumentBundle`` on disk
- **Merge CLI** — combining competing runner passes into one bundle graph
- **Review CLI** — driving ``review_markup`` / ``review_overlay`` tasks from the
  shell

When assemble and review CLIs land, this guide will be updated; until then, use
the provisional export path above and treat corrected output as a conceptual
target.

Related Runbooks
================

- :doc:`/overview/installation` — clone, environment, and editable install
- :doc:`/runbook/huggingface_setup` — model endpoint access for ``run``
- :doc:`/runbook/ocr_process` — full stage-by-stage OCR architecture
- :doc:`/runbook/operator_notes` — short preservation and triage rules
- :doc:`/runbook/gold_annotation` — gold slice protocol for ``eval`` /
  ``eval-cohorts``
