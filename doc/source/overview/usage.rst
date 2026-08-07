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

Execute prepared artifacts against one hosted olmOCR runner. Requires
``huggingface_api_key`` and a matching entry in
``huggingface_model_endpoints`` (see :doc:`/overview/configuration`).

.. code-block:: bash

   wordwending run PREPARED_INPUTS.json \
     --policy policy.json \
     --runner runner.json \
     --bundle-root ./bundle \
     --output-dir ./run-out \
     --run-id RUN_ID \
     --document-id DOC_ID

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
supported runner) artifact paths; merge flags persist for review.

inspect-bundle
^^^^^^^^^^^^^^

Summarize an assembled bundle: manifests, pages, witnesses, merge flags, and
overlay paths.

.. code-block:: bash

   wordwending inspect-bundle --bundle-root ./bundle-root

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

export
^^^^^^

Write derived exports from a ``DocumentBundle`` JSON into
``<bundle-root>/exports/``.

.. code-block:: bash

   wordwending export document-bundle.json --bundle-root ./bundle-root

Artifacts include ``exports/document.md``, ``exports/bundle.json``,
``exports/rag.jsonl``, and ``exports/stitched_chunks.jsonl``.

What is not a CLI yet
---------------------

- Standalone ``merge`` (merge runs inside ``assemble``)
- Auto-generated ``AssembleManifest`` from prepare/run output trees
- Single orchestrated prepare → run → assemble → review → export run
- Phase 5 bake-off, Phase 6 PassRunner Protocol, Phase 10 operational hardening

Those gaps are documented in :doc:`/runbook/from_source_to_markdown`.

Configuration
-------------

See :doc:`/overview/configuration`. For hosted endpoints, also
:doc:`/runbook/huggingface_setup`.
