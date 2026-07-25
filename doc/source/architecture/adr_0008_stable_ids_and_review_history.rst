===================================================
ADR 0008: Stable IDs and Append-Only Review History
===================================================

:Status: Accepted
:Date: 2026-07-25

Context
=======

``bochord`` outputs will be consumed by deterministic software, review
workflows, and RAG systems. Human markup must remain auditable over time.

Decision
========

Every graph object and exportable chunk must have a stable id that survives
rebuilds when underlying evidence has not materially changed.

Human review history is append-only. ``bochord`` does not collapse review into a
single mutable latest-state blob.

Trust states are:

- ``machine``
- ``reviewed``
- ``corrected``

Review scope may apply at:

- page
- region
- note
- span

Initial review verbs are:

- ``accept``
- ``correct_text``
- ``correct_style``
- ``link_note``
- ``unlink_note``
- ``split_region``
- ``merge_region``
- ``flag``

Consequences
============

- Overlays can point to stable objects instead of brittle positional guesses.
- Audit, diff, rollback, and retraining workflows become feasible.
- Downstream consumers can filter by trust state and review scope precisely.
