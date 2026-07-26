=========================================
Spec 0014: Review Task and Overlay Schema
=========================================

Purpose
=======

Define exact self-contained task packets, append-only events, and materialized
overlay JSON in ``bochord.models.ocr``.

Review Task Contract
====================

``ReviewTask`` is the instruction boundary between orchestration and a human.
It requires ``task_id``, ``task_type``, non-empty ``dimensions``,
``target_scope``, non-empty ``target_object_ids``, one concrete ``question``,
non-empty ``required_evidence``, ``allowed_actions``, and
``completion_criteria``, plus ``guideline_id``, ``guideline_version``,
``base_run_id``, and ``base_graph_revision``.

It also records calibration examples, whether abstention is allowed, lifecycle
status, and coverage ids certified at completion. Task types are source triage,
preparation, layout, text, typography, note linkage, gold, and adjudication.
The interface must render these fields as instructions and controls; it must not
replace them with a generic review screen.

Event Base Contract
===================

Every review event requires:

- event and task ids
- target object id and scope
- non-empty review dimensions
- base run id and graph revision
- guideline version
- prior and new trust state
- operator id and UTC timestamp
- fixed ``action`` discriminator

An event is invalid for an overlay when its task is missing, its action is not
allowed by that task, its dimensions exceed the task dimensions, or its run and
graph revisions do not match the overlay/task binding.

Event Payloads
==============

``correct_text`` carries replacement ``text_diplomatic`` only. Normalized text
is regenerated deterministically and is never operator input.

``correct_style`` carries a complete orthogonal ``Typography`` value and
semantic text roles. Weight, slant, baseline shift, family, size, small capitals,
and letter spacing do not exclude one another. ``footnote-marker`` is a role.

``correct_geometry`` carries a box and/or polygon in an identified coordinate
space. ``reorder`` carries the complete ordered child-id list.
``reclassify_region`` carries the accepted region kind. ``mark_illegible``
carries the reason source pixels do not support a transcription.

``link_note`` and ``unlink_note`` carry marker span ids and note id.
``split_region`` and ``merge_region`` carry complete ``RegionRevision``
definitions: ids, classes, geometry, reading order, and line assignments. Id-only
structural events are not replayable and are invalid.

``flag`` creates a stable ``flag_id``. ``resolve_flag`` closes that exact id with
an auditable resolution. Flags never upgrade trust by themselves.

Materialized State
==================

``OverlayState`` is a replay cache, not truth. It records object/scope, trust,
reviewed and corrected dimensions, active flag ids, applied event ids,
diplomatic-text, typography, role, geometry, region-kind, note-link, and
illegibility overrides. There is no normalized-text override.

Page Overlay Contract
=====================

``PageOverlay`` requires schema and overlay ids, page id, source run id, base
graph revision, prepared-image checksum, review tasks, events, and materialized
state. ``predecessor_overlay_id`` links a superseding or rebased overlay.

Replay and Rebase Rules
=======================

The event log is append-only truth; materialized state may always be rebuilt.
Events apply in recorded order. Duplicate event ids, unresolved task ids,
dangling flag resolutions, or mismatched base revisions are hard validation
errors.

When the image, run, graph, or guideline changes, create a successor overlay.
Reapply only events whose targets and coordinate spaces still resolve; issue
adjudication tasks for conflicts. Never mutate the predecessor to make it appear
compatible.
