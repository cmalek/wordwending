==================
Hugging Face Setup
==================

Purpose
=======

This runbook explains how to prepare ``bochord`` to use models hosted on
Hugging Face.

This assumes a local ``bochord`` checkout and its repo-local virtual
environment.

Step 1: Activate the Project Environment
========================================

From the repo root:

.. code-block:: bash

   source .venv/bin/activate

This ensures Python, Sphinx, and model-related packages come from the project
environment, not the global interpreter.

Step 2: Install Hugging Face Client Tools
=========================================

The official Hub quickstart recommends ``huggingface_hub`` and the ``hf`` CLI.

.. code-block:: bash

   pip install --upgrade huggingface_hub

Official docs:

- `Hugging Face Hub Quickstart <https://huggingface.co/docs/huggingface_hub/quick-start>`_
- `Hugging Face CLI Guide <https://huggingface.co/docs/huggingface_hub/en/guides/cli>`_

Step 3: Authenticate
====================

Login with the official CLI flow:

.. code-block:: bash

   hf auth login

This opens a browser flow and stores a token locally for later downloads.

Use this when you need:

- gated model access
- private model access
- authenticated downloads

Step 4: Choose a Cache Policy
=============================

Model files are large. Decide early where they should live.

Useful environment variables and options from the official docs include:

- ``HF_HOME``
- ``--cache-dir`` on download commands
- ``HF_HUB_DOWNLOAD_TIMEOUT`` for slow links

Example:

.. code-block:: bash

   export HF_HOME="$PWD/.hf-home"
   export HF_HUB_DOWNLOAD_TIMEOUT=30

Step 5: Test Model Access
=========================

Use the CLI or Python client to confirm model availability before wiring it into
``bochord`` runners.

CLI example:

.. code-block:: bash

   hf download gpt2 config.json --quiet

Python example:

.. code-block:: python

   from huggingface_hub import hf_hub_download
   hf_hub_download(repo_id="gpt2", filename="config.json")

Step 6: Record Runtime Provenance
=================================

For every model-backed pass runner, record enough provenance to reproduce the
run later.

Minimum recommended provenance:

- model repo id
- revision, tag, or commit when pinned
- local runtime backend
- cache location policy
- authenticated or gated access expectation

Step 7: Separate Model Access from OCR Policy
=============================================

Hugging Face is a model distribution channel, not the OCR policy itself.

``bochord`` should keep separate:

- model acquisition and authentication
- runner configuration
- preparation and batching strategy
- evaluation and model comparison

Operator Notes
==============

- Prefer pinned revisions for reproducibility.
- Do not assume network availability during every run.
- Expect some model repos to be gated.
- Test access before long OCR jobs.

Current Official References
===========================

- `Hugging Face Hub Quickstart <https://huggingface.co/docs/huggingface_hub/quick-start>`_
- `Hugging Face CLI Guide <https://huggingface.co/docs/huggingface_hub/en/guides/cli>`_
