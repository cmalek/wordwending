Using the Command Line Interface
================================

The ``wordwending`` CLI prepares source pages, runs hosted OCR, evaluates
predictions, and exports derived views from an accepted ``DocumentBundle``.
Deep workflow narrative lives in :doc:`/runbook/from_source_to_markdown`.

Getting help
------------

.. code-block:: bash

   wordwending --help
   wordwending prepare --help
   wordwending run --help
   wordwending assemble --help
   wordwending review --help
   wordwending endpoints --help
   wordwending export --help

Command structure
-----------------

.. code-block:: bash

   wordwending [global-options] <command> [options] [args]

Global options
--------------

``-v`` / ``--verbose``
    Extra diagnostic output.

``-q`` / ``--quiet``
    Suppress non-error output.

``--config-file PATH``
    Load a specific TOML settings file (highest file precedence).

``--output {json,table,text}``
    Format for commands that print structured results (for example
    ``settings``). Default comes from settings (``table``).

Commands
--------

version
^^^^^^^

Print package and dependency versions.

.. code-block:: bash

   wordwending version

settings
^^^^^^^^

Print effective settings (not a subcommand group).

.. code-block:: bash

   wordwending settings
   wordwending --output json settings

prepare
^^^^^^^

Acquire and prepare source pages (PDF, image, image folder, or ZIP of images)
into a reproducible output bundle.

.. code-block:: bash

   wordwending prepare SOURCE \
     --recipe recipe.json \
     --output-dir ./out \
     [--mode full-page|columns|fixed-tiles] \
     [--page-class ordinary-prose|dense-dictionary|note-heavy|table-heavy|mixed-complex] \
     [--override-reason "..."] \
     [--overrides overrides.json]

``--recipe`` and ``--output-dir`` are required. Operator overrides for
``--mode`` / ``--page-class`` require ``--override-reason``.

run
^^^

Execute prepared artifacts against one hosted olmOCR or kraken runner. Requires
``huggingface_api_key`` and a matching entry in
``huggingface_model_endpoints`` (see :doc:`/overview/configuration`).

Successful batches are recorded under
``<bundle-root>/runner-resume-ledger.json``. A later ``run`` against the same
bundle skips those batch ids unless ``--force`` is set. Missing or corrupt
ledger files are treated as empty. Together with ``inspect-bundle`` checksum
verification, this is the Wave H **ops skeleton only** — Spec 0004 **Phase 10
is NOT COMPLETE** (HF deploy/ops, quotas, cost controls, corpus regression
gates, and operator calibration monitoring remain deferred).

.. code-block:: bash

   wordwending run PREPARED_INPUTS.json \
     --policy policy.json \
     --runner runner.json \
     --bundle-root ./bundle \
     --output-dir ./run-out \
     --run-id RUN_ID \
     --document-id DOC_ID \
     [--force]

eval
^^^^

Score one predicted page against gold annotations; writes a
``PageEvaluationSummary`` JSON.

.. code-block:: bash

   wordwending eval \
     --prediction page.json \
     --gold gold.json \
     --profile profile.json \
     --output-json summary.json

eval-cohorts
^^^^^^^^^^^^

Summarize a JSON array of page evaluation records into fixed cohort views.

.. code-block:: bash

   wordwending eval-cohorts records.json --output-json cohorts.json

assemble
^^^^^^^^

Adapt raw witness artifacts, merge (single- or multi-witness), and write a
``DocumentBundle`` tree from an operator ``AssembleManifest`` JSON.

.. code-block:: bash

   wordwending assemble \
     --bundle-root ./bundle-root \
     --manifest manifest.json

Paths inside the manifest are relative posix strings resolved against
``--bundle-root``. Multi-witness pages list olmOCR and kraken (or other
supported runner) artifact paths; merge flags persist as dimension-specific
evaluation flags (``evaluation/flags.json``) for ``inspect-bundle`` and
operator review prep—not auto-emitted Spec 0005 ``ReviewTask`` packets.

inspect-bundle
^^^^^^^^^^^^^^

Summarize an assembled bundle: manifests, pages, witnesses, merge flags,
overlay paths, and ``exports/*`` artifact paths when export has run. Also
prints ``checksum: <path> OK|FAIL|SKIPPED`` for digests already recorded in
bundle-layout metadata (source / prepared-page / prepared-unit). This is
corruption-check scaffolding only — Spec 0004 **Phase 10 is NOT COMPLETE**.

.. code-block:: bash

   wordwending inspect-bundle --bundle-root ./bundle-root

bakeoff
^^^^^^^

Score **recorded** candidate predictions into ``bakeoff-matrix-v1.json`` using
``EvaluationService`` metrics. Schema targets real candidates (``olmocr`` +
``kraken``). Spec 0004 **Phase 5 is NOT COMPLETE** — cost/license/operability
scoring and full held-out corpus remain deferred.

.. code-block:: bash

   wordwending bakeoff \
     --bundle-root ./bakeoff-root \
     --manifest bakeoff-manifest.json \
     --profile metric-profile-v1.json \
     --output-dir ./bakeoff-out

review apply
^^^^^^^^^^^^

Append ``PageOverlay`` review events to a bundle page and materialize overlay
state from the full append-only history.

.. code-block:: bash

   wordwending review apply \
     --bundle-root ./bundle-root \
     --overlay page-overlay.json \
     --page-id PAGE_ID

review materialize
^^^^^^^^^^^^^^^^^^

Replay ``overlays/review_events.jsonl`` into ``overlays/current_state.json``
for one page.

.. code-block:: bash

   wordwending review materialize \
     --bundle-root ./bundle-root \
     --page-id PAGE_ID

endpoints up
^^^^^^^^^^^^

Ensure catalogued Hugging Face Inference Endpoints are ready and print HTTPS
URLs. Requires ``huggingface_api_key`` (see :doc:`/overview/configuration`).
``--runner`` may be repeated; omit it to target every catalogued runner
(``olmocr``, ``kraken`` by default).

Before ensuring endpoints, ``up`` calls the idle watchdog (``pause_idle``) as
a safety net: runners idle longer than
``huggingface_endpoint_idle_minutes`` are paused so stale sessions do not
block fresh ensure operations. Spec 0004 **Phase 10 is NOT COMPLETE** — this
is lifecycle CLI scaffolding only; full HF deploy/ops, quotas, cost controls,
and corpus regression gates remain deferred.

.. code-block:: bash

   wordwending endpoints up [--runner olmocr] [--runner kraken]

endpoints down
^^^^^^^^^^^^^^

Pause or delete catalogued endpoints and update the session ledger at
``huggingface_endpoint_ledger_path`` (default
``~/.config/wordwending/endpoint-session-ledger.json``). Pausing is the
default; pass ``--delete`` to destroy remote endpoints instead.

.. code-block:: bash

   wordwending endpoints down [--runner RUNNER] [--delete]

endpoints status
^^^^^^^^^^^^^^^^

Report remote Hugging Face status and ledger ``last_used_at_utc`` for
catalogued runners. Like ``up``, ``status`` calls ``pause_idle`` first as a
safety net for stale idle sessions.

.. code-block:: bash

   wordwending endpoints status [--runner RUNNER]

export
^^^^^^

Write derived exports from a ``DocumentBundle`` JSON into
``<bundle-root>/exports/``. Export reads accepted page graphs only; overlay
files (``overlays/review_events.jsonl``, ``overlays/current_state.json``) are
not consumed until graph rebase lands.

.. code-block:: bash

   wordwending export document-bundle.json --bundle-root ./bundle-root

Artifacts include ``exports/document.md``, ``exports/bundle.json``,
``exports/rag.jsonl``, and ``exports/stitched_chunks.jsonl``.

What is not a CLI yet
---------------------

- Standalone ``merge`` (merge runs inside ``assemble``)
- Auto-generated ``AssembleManifest`` from prepare/run output trees
- Single orchestrated prepare → run → assemble → review → export run
- Spec 0004 **Phase 5 NOT COMPLETE** (``bakeoff`` harness writes
  ``bakeoff-matrix-v1.json`` from recorded predictions; cost/license/
  operability scoring and full held-out corpus remain deferred)
- Spec 0004 **Phase 10 NOT COMPLETE** — **ops skeleton only** (``run`` resume
  ledger + ``inspect-bundle`` checksum verification). Deferred Spec exit:
  HF deploy/ops, quotas, cost controls, corpus regression gates, operator
  calibration monitoring. (Phase 6 PassRunner Protocol + registry is COMPLETE.)

Those gaps are documented in :doc:`/runbook/from_source_to_markdown`.

Configuration
-------------

See :doc:`/overview/configuration`. For hosted endpoints, also
:doc:`/runbook/huggingface_setup`.
