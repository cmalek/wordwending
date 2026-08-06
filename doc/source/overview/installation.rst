Installation
============

Install ``bochord`` from source. This project is early and evolving; the
documented path is clone + ``uv``, not a published package for this tool.

Prerequisites
-------------

- Python **3.13** or later (matches ``requires-python`` in ``pyproject.toml``)
- `uv <https://docs.astral.sh/uv/>`_
- ``git``

.. warning::

   The PyPI project name ``bochord`` may refer to an **unrelated** Books-backup
   package. Do **not** ``pip install bochord`` (or ``uv tool install bochord`` /
   ``pipx install bochord``) expecting this OCR tool until this project's own
   packaging story changes. Install from source as below.

From Source with ``uv``
-----------------------

.. code-block:: bash

   git clone https://github.com/cmalek/bochord.git
   /usr/bin/cd bochord
   # Install uv if needed: https://docs.astral.sh/uv/getting-started/installation/
   uv sync
   source .venv/bin/activate
   bochord --help

``uv sync`` creates ``.venv`` and installs the project in editable form with
declared dependencies. Always activate that environment before Python or docs
work in this repository.

Verification
------------

.. code-block:: bash

   source .venv/bin/activate
   bochord version
   bochord --help

Next steps
----------

- :doc:`/overview/quickstart` — minimal CLI smoke check
- :doc:`/runbook/from_source_to_markdown` — end-to-end operator walkthrough
- :doc:`/overview/configuration` — Hugging Face and other settings
- :doc:`/runbook/huggingface_setup` — hosted endpoint operations
