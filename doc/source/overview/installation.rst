Installation
============

Install ``wordwending`` from source. This project is early and evolving; the
documented path is clone + ``uv``, not a published package for this tool.

Prerequisites
-------------

- Python **3.13** or later (matches ``requires-python`` in ``pyproject.toml``)
- `uv <https://docs.astral.sh/uv/>`_
- ``git``

.. warning::

   ``wordwending`` is not yet published as an installable package for this OCR
   tool. Do not ``pip install wordwending`` (or ``uv tool install wordwending`` /
   ``pipx install wordwending``) expecting this repository; install from source
   as below.

From Source with ``uv``
-----------------------

.. code-block:: bash

   git clone https://github.com/cmalek/wordwending.git
   /usr/bin/cd wordwending
   # Install uv if needed: https://docs.astral.sh/uv/getting-started/installation/
   uv sync
   source .venv/bin/activate
   wordwending --help

``uv sync`` creates ``.venv`` and installs the project in editable form with
declared dependencies. Always activate that environment before Python or docs
work in this repository.

Verification
------------

.. code-block:: bash

   source .venv/bin/activate
   wordwending version
   wordwending --help

Next steps
----------

- :doc:`/overview/quickstart` — minimal CLI smoke check
- :doc:`/runbook/from_source_to_markdown` — end-to-end operator walkthrough
- :doc:`/overview/configuration` — Hugging Face and other settings
- :doc:`/runbook/huggingface_setup` — hosted endpoint operations
