Frequently Asked Questions
==========================

General
-------

What is wordwending?
^^^^^^^^^^^^^^^^

``wordwending`` is an early, evolving Python CLI for high-fidelity, image-first
OCR of Old English / Anglo-Saxon
source material. It preserves raw witnesses, then derives structured, RAG, and
Markdown exports for scholars—with agent-usable evidence as a payoff, not the
starting point.

Is this production-ready?
^^^^^^^^^^^^^^^^^^^^^^^^^

No. Treat it as research software: commands and bundle-assembly paths change.
**Phase 6** (PassRunner Protocol + registry) is **COMPLETE**. **Phase 5**
(bake-off) and **Phase 10** (operational hardening) are **NOT COMPLETE**.
Wave H ships an **ops skeleton only** (``run`` resume ledger,
``inspect-bundle`` checksum verification, and ``wordwending endpoints``
``up``/``down``/``status`` lifecycle CLI with optional ``--ensure-endpoints``
on ``run``/``bakeoff``); Spec Phase 10 exit remains deferred. See
:doc:`/runbook/from_source_to_markdown`.

Installation
------------

How should I install it?
^^^^^^^^^^^^^^^^^^^^^^^^

From source with ``uv sync``. See :doc:`installation`.

Usage
-----

What commands exist?
^^^^^^^^^^^^^^^^^^^^

``version``, ``settings``, ``prepare``, ``run``, ``eval``, ``eval-cohorts``,
``assemble``, ``inspect-bundle``, ``bakeoff``, ``endpoints up``,
``endpoints down``, ``endpoints status``, ``review apply``,
``review materialize``, and ``export``. Details: :doc:`usage`.

Where is the end-to-end guide?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:doc:`/runbook/from_source_to_markdown`.

Is there an assemble / merge / review CLI?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Yes, with honest limits:

- ``assemble`` adapts raw witnesses, merges (including olmOCR + kraken multi-witness),
  and writes a ``DocumentBundle`` tree from an operator ``AssembleManifest``
- ``inspect-bundle`` summarizes the assembled tree, including merge flags as
  dimension-specific evaluation flags (``evaluation/flags.json``),
  ``checksum: … OK|FAIL|SKIPPED`` lines for digests already recorded in bundle
  layout metadata, and ``exports/*`` paths when derived exports exist on disk
- ``review apply`` and ``review materialize`` drive append-only overlay acceptance
  (operators hand-author ``PageOverlay`` JSON; Spec 0005 ``ReviewTask`` packets
  are not auto-emitted by assemble)

There is no standalone ``merge`` command (merge runs inside ``assemble``) and no
single orchestrated prepare→export run yet. Spec 0004 Phase 6 (PassRunner Protocol
+ registry) is COMPLETE; Phase 5 remains NOT COMPLETE; Phase 10 remains NOT
COMPLETE (**ops skeleton only**; Spec exit deferred). See
:doc:`/runbook/from_source_to_markdown`.

Is Markdown the source of truth?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

No. Markdown under ``exports/document.md`` is a **derived reading view**.
Structured bundle JSON and witness artifacts remain authoritative for
rebuildability and evidence.

How do I configure Hugging Face for ``run``?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Set ``huggingface_api_key`` and ``huggingface_model_endpoints`` in TOML or
``WORDWENDING_*`` env vars. See :doc:`configuration` and
:doc:`/runbook/huggingface_setup`.

How do I spin Hugging Face endpoints up and down?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Spec 0004 Phase 10 is NOT COMPLETE** — lifecycle CLI is ops scaffolding only.

Preferred path:

.. code-block:: bash

   wordwending endpoints up [--runner olmocr] [--runner kraken]
   wordwending endpoints status [--runner RUNNER]
   wordwending endpoints down [--runner RUNNER]            # pause (default)
   wordwending endpoints down [--runner RUNNER] --delete   # destroy remote

``up`` and ``status`` pause endpoints idle longer than
``huggingface_endpoint_idle_minutes`` before ensuring fresh sessions. Catalog
entries configure Hugging Face scale-to-zero; the local ledger at
``huggingface_endpoint_ledger_path`` (default
``~/.config/wordwending/endpoint-session-ledger.json``) tracks
``last_used_at_utc`` and the idle watchdog **pauses only** (never auto-deletes).

For a single ``run`` or ``bakeoff`` without a separate ``endpoints up``:

.. code-block:: bash

   wordwending run ... --ensure-endpoints
   wordwending bakeoff ... --ensure-endpoints

Replace default catalog placeholders (``repository``, immutable ``revision``,
``namespace``, hardware) before live deployment. Secrets live only in
``huggingface_api_key``. The Hugging Face ``hf endpoints`` CLI remains an
escape hatch — see :doc:`/runbook/huggingface_setup`.

How do I change output format?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   wordwending --output json settings
   wordwending --output table settings
   wordwending --output text settings

Troubleshooting
---------------

``command not found: wordwending``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Activate the project venv after ``uv sync``:

.. code-block:: bash

   source .venv/bin/activate
   command -v wordwending
   wordwending version

``run`` says missing ``huggingface_api_key`` or endpoint
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Configure settings, then verify:

.. code-block:: bash

   wordwending settings

The endpoint key in your runner policy must match a key in
``huggingface_model_endpoints``, and every URL must be ``https``.

Getting help
------------

1. ``wordwending --help`` / ``wordwending <command> --help``
2. Docs at https://wordwending.readthedocs.io
3. GitHub issues on the project repository

When reporting bugs, include the exact command, full error text, OS, Python
version (3.13+), ``wordwending version`` output, and ``--verbose`` logs when safe
(scrub tokens).
