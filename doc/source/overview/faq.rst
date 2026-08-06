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
Gaps (especially assemble/merge and review) are documented rather than hidden.
See :doc:`/runbook/from_source_to_markdown`.

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
and ``export``. Details: :doc:`usage`.

Where is the end-to-end guide?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:doc:`/runbook/from_source_to_markdown`.

Is there an assemble / merge / review CLI?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Not yet. Assembling a ``DocumentBundle`` from prepare/run outputs and accepting
overlays remains deferred. Do not expect ``wordwending assemble`` or similar today.
``export`` assumes you already have a valid ``DocumentBundle`` JSON.

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
