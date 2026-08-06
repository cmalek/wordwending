Configuration
=============

``bochord`` loads cascading TOML settings plus ``BOCHORD_*`` environment
variables. Operators running ``bochord run`` must supply a Hugging Face API
token and named endpoint URLs.

Configuration methods
---------------------

Highest priority wins:

1. Command-line options (``--config-file``, ``--output``, ``--verbose``, ``--quiet``)
2. Environment variables (``BOCHORD_*``)
3. TOML configuration files (most specific file among those found)
4. Built-in defaults

File locations
--------------

Settings search (later / more specific wins when multiple exist; an explicit
``--config-file`` or ``BOCHORD_CONFIG_FILE`` path is preferred when set):

1. Global: ``/etc/bochord.toml`` (Unix) or ``C:/ProgramData/bochord.toml`` (Windows)
2. User: ``~/.bochord.toml``
3. Local: ``./.bochord.toml`` (current working directory)
4. Explicit: ``BOCHORD_CONFIG_FILE`` or ``--config-file``

Inspect what the process actually loaded:

.. code-block:: bash

   bochord settings
   bochord --output json settings

Settings operators need
-----------------------

Values mirror ``bochord.settings.Settings``:

**Identity (read-only)**

- ``app_name`` — always ``bochord``
- ``app_version`` — package version string

**CLI / logging**

- ``default_output_format`` — ``table`` | ``json`` | ``text`` (default ``table``)
- ``enable_colors`` — boolean (default ``true``)
- ``quiet_mode`` — boolean (default ``false``)
- ``log_level`` — ``DEBUG`` | ``INFO`` | ``WARNING`` | ``ERROR`` (default ``INFO``)
- ``log_file`` — optional path, or omit / ``null``

**Hugging Face (required for ``bochord run``)**

- ``huggingface_api_key`` — API token (secret). Missing or empty → ``run`` fails.
- ``huggingface_model_endpoints`` — map of endpoint key → **HTTPS** URL.
  ``run`` resolves ``execution_policy.endpoint.endpoint_key`` against this map.

Example ``~/.bochord.toml``:

.. code-block:: toml

   default_output_format = "table"
   enable_colors = true
   log_level = "INFO"

   huggingface_api_key = "hf_..."

   [huggingface_model_endpoints]
   olmocr-primary = "https://xxxxxxxx.us-east-1.aws.endpoints.huggingface.cloud"

Environment variables use the ``BOCHORD_`` prefix, for example:

.. code-block:: bash

   export BOCHORD_HUGGINGFACE_API_KEY="hf_..."
   export BOCHORD_LOG_LEVEL="DEBUG"
   export BOCHORD_DEFAULT_OUTPUT_FORMAT="json"

Prefer environment variables or a mode-``600`` user TOML for secrets. Do not
commit tokens or put them in bundle provenance.

Endpoint URLs must use ``https``. Non-HTTPS values are rejected at settings
validation.

Global CLI options
------------------

.. code-block:: bash

   bochord --verbose settings
   bochord --quiet version
   bochord --config-file ./my-bochord.toml settings
   bochord --output json settings

See also
--------

- :doc:`/runbook/huggingface_setup` — endpoint provisioning and laptop boundary
- :doc:`/overview/usage` — command reference
- :doc:`/runbook/from_source_to_markdown` — end-to-end operator path
