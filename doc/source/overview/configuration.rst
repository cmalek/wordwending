Configuration
=============

``wordwending`` loads cascading TOML settings plus ``WORDWENDING_*`` environment
variables. Operators running ``wordwending run`` must supply a Hugging Face API
token and named endpoint URLs.

Settings field precedence
-------------------------

``Settings.settings_customise_sources`` returns sources in **highest-first**
order. When a TOML file is selected, field values resolve as:

1. Selected TOML file (wins over environment)
2. Environment variables (``WORDWENDING_*``)
3. Built-in field defaults

If no TOML file is found, environment variables win over defaults.

Important: only **one** TOML file is loaded (not a merge of several). Among
candidate paths that exist, the highest wins and the rest are ignored:

1. Explicit: ``--config-file`` (sets ``WORDWENDING_CONFIG_FILE`` before load) or
   ``WORDWENDING_CONFIG_FILE`` already in the environment
2. Local: ``./.wordwending.toml`` (current working directory)
3. User: ``~/.wordwending.toml``

System-wide global config (for example under ``/etc``) is **not** currently a
supported operator path—do not depend on it.

Runtime CLI flags (not Settings sources)
----------------------------------------

These affect the current invocation; they do **not** override TOML/env field
values inside ``Settings``:

- ``--output`` — format for commands that print results (for example ``settings``)
- ``--verbose`` / ``--quiet`` — console verbosity for that run

``--config-file`` is different: it selects which TOML file ``Settings`` loads
(via ``WORDWENDING_CONFIG_FILE``), and that TOML still beats ``WORDWENDING_*`` field
env vars.

Inspect what the process actually loaded:

.. code-block:: bash

   wordwending settings
   wordwending --output json settings

Settings operators need
-----------------------

Values mirror ``wordwending.settings.Settings``:

**Identity (read-only)**

- ``app_name`` — always ``wordwending``
- ``app_version`` — package version string

**CLI / logging**

- ``default_output_format`` — ``table`` | ``json`` | ``text`` (default ``table``)
- ``enable_colors`` — boolean (default ``true``)
- ``quiet_mode`` — boolean (default ``false``)
- ``log_level`` — ``DEBUG`` | ``INFO`` | ``WARNING`` | ``ERROR`` (default ``INFO``)
- ``log_file`` — optional path, or omit / ``null``

**Hugging Face (required for ``wordwending run``)**

- ``huggingface_api_key`` — API token (secret). Missing or empty → ``run`` fails.
- ``huggingface_model_endpoints`` — map of endpoint key → **HTTPS** URL.
  ``run`` resolves ``execution_policy.endpoint.endpoint_key`` against this map.

Example ``~/.wordwending.toml``:

.. code-block:: toml

   default_output_format = "table"
   enable_colors = true
   log_level = "INFO"

   huggingface_api_key = "hf_..."

   [huggingface_model_endpoints]
   olmocr-primary = "https://xxxxxxxx.us-east-1.aws.endpoints.huggingface.cloud"

Environment variables use the ``WORDWENDING_`` prefix, for example:

.. code-block:: bash

   export WORDWENDING_HUGGINGFACE_API_KEY="hf_..."
   export WORDWENDING_LOG_LEVEL="DEBUG"
   export WORDWENDING_DEFAULT_OUTPUT_FORMAT="json"

Prefer environment variables or a mode-``600`` user TOML for secrets. Do not
commit tokens or put them in bundle provenance.

Endpoint URLs must use ``https``. Non-HTTPS values are rejected at settings
validation.

Global CLI options
------------------

.. code-block:: bash

   wordwending --verbose settings
   wordwending --quiet version
   wordwending --config-file ./my-wordwending.toml settings
   wordwending --output json settings

See also
--------

- :doc:`/runbook/huggingface_setup` — endpoint provisioning and laptop boundary
- :doc:`/overview/usage` — command reference
- :doc:`/runbook/from_source_to_markdown` — end-to-end operator path
