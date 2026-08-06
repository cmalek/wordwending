===================================================
ADR 0008: Stable IDs and Append-Only Review History
===================================================

:Status: Accepted
:Date: 2026-07-25

Context
=======

``wordwending`` outputs will be consumed by deterministic software, review
workflows, and RAG systems. Human markup must remain auditable over time.

Decision
========

Every graph object and exportable chunk must have a stable id that survives
rebuilds when underlying evidence has not materially changed.

Human review history is append-only. ``wordwending`` does not collapse review into a
single mutable latest-state blob.

Trust states are:

- ``machine``
- ``reviewed``
- ``corrected``

Trust is always qualified by reviewed dimensions. Text, structure, typography,
source quality, preparation, and note linkage are certified independently; no
single ``reviewed`` bit certifies them all.

Review scope may apply at:

- page
- region
- line
- note
- span

Initial review verbs are:

- ``accept``
- ``correct_text``
- ``correct_style``
- ``correct_geometry``
- ``reorder``
- ``reclassify_region``
- ``mark_illegible``
- ``link_note``
- ``unlink_note``
- ``split_region``
- ``merge_region``
- ``flag``
- ``resolve_flag``

Every event binds to a review task, source run, graph revision, prepared image,
and guideline revision through its overlay. Structural events carry complete
replayable replacement definitions. A changed base creates a successor/rebased
overlay rather than silently reusing stale decisions.

Consequences
============

- Overlays can point to stable objects instead of brittle positional guesses.
- Audit, diff, rollback, and retraining workflows become feasible.
- Downstream consumers can filter by trust state and review scope precisely.
