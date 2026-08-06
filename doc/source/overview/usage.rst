Using the Command Line Interface
================================

The ``bochord`` CLI prepares source pages, runs hosted OCR, evaluates
predictions, and exports derived views from an accepted ``DocumentBundle``.
Deep workflow narrative lives in :doc:`/runbook/from_source_to_markdown`.

Getting help
------------

.. code-block:: bash

   bochord --help
   bochord prepare --help
   bochord run --help
   bochord export --help

Command structure
-----------------

.. code-block:: bash

   bochord [global-options] <command> [options] [args]

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

   bochord version

settings
^^^^^^^^

Print effective settings (not a subcommand group).

.. code-block:: bash

   bochord settings
   bochord --output json settings

prepare
^^^^^^^

Acquire and prepare source pages (PDF, image, image folder, or ZIP of images)
into a reproducible output bundle.

.. code-block:: bash

   bochord prepare SOURCE \
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

   bochord run PREPARED_INPUTS.json \
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

   bochord eval \
     --prediction page.json \
     --gold gold.json \
     --profile profile.json \
     --output-json summary.json

eval-cohorts
^^^^^^^^^^^^

Summarize a JSON array of page evaluation records into fixed cohort views.

.. code-block:: bash

   bochord eval-cohorts records.json --output-json cohorts.json

export
^^^^^^

Write derived exports from a ``DocumentBundle`` JSON into
``<bundle-root>/exports/``.

.. code-block:: bash

   bochord export document-bundle.json --bundle-root ./bundle-root

Artifacts include ``exports/document.md``, ``exports/bundle.json``,
``exports/rag.jsonl``, and ``exports/stitched_chunks.jsonl``.

What is not a CLI yet
---------------------

- Assembling / merging prepare+run outputs into a ``DocumentBundle``
- Review / overlay acceptance workflows

Those gaps are documented in :doc:`/runbook/from_source_to_markdown`. Do not
invent assemble or review commands; use fixtures or manual assembly when you
need ``export`` today.

Configuration
-------------

See :doc:`/overview/configuration`. For hosted endpoints, also
:doc:`/runbook/huggingface_setup`.
