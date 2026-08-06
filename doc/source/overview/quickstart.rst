Quickstart Guide
================

Confirm the CLI, inspect settings, then follow the operator walkthrough for
real preparation, OCR, and export work.

Prerequisites
-------------

- Python **3.13+**
- :doc:`/overview/installation` completed (source + ``uv sync``)
- For hosted OCR: Hugging Face credentials and endpoints
  (:doc:`/overview/configuration`, :doc:`/runbook/huggingface_setup`)

Smoke check
-----------

.. code-block:: bash

   source .venv/bin/activate
   wordwending --help
   wordwending version
   wordwending settings

Commands available today
------------------------

=================  ===========================================================
Command            Role
=================  ===========================================================
``version``        Installed package and dependency versions
``settings``       Effective configuration (table / json / text)
``prepare``        Acquire and prepare source pages into a bundle layout
``run``            Execute prepared artifacts against one hosted olmOCR runner
``eval``           Score one predicted page against gold annotations
``eval-cohorts``   Summarize page evaluations into fixed cohort views
``export``         Derive bundle / RAG / Markdown exports from a DocumentBundle
=================  ===========================================================

There is no assemble/merge or review CLI yet. Building a ``DocumentBundle`` from
prepare/run outputs remains manual or deferred; see the e2e guide.

Minimal export (when you already have a DocumentBundle)
-------------------------------------------------------

.. code-block:: bash

   wordwending export path/to/document-bundle.json --bundle-root path/to/bundle-root

Writes under ``bundle-root/exports/`` at least ``document.md``, ``bundle.json``,
``rag.jsonl``, and ``stitched_chunks.jsonl``. Markdown is a **derived reading
view**, not the source of truth.

Deep walkthrough
----------------

For the full spine (prepare → run → provisional export, plus what is still
missing), use:

:doc:`/runbook/from_source_to_markdown`

Next steps
----------

1. :doc:`/overview/usage` — command reference and global options
2. :doc:`/overview/configuration` — ``huggingface_api_key`` and endpoints
3. :doc:`/overview/faq` — early status and known gaps
