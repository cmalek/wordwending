=========================================
Spec 0013: Pass-Runner Interface Schema
=========================================

Purpose
=======

Define the exact persisted schema for pass-runner capability declarations and
runner batch execution records.

Canonical Models
================

The exact v1 Pydantic models live in ``bochord.models.ocr``:

- ``RunnerReference``
- ``RunnerCapability``
- ``PreparedArtifactRef``
- ``BatchItemRef``
- ``RunnerOutputArtifact``
- ``RunnerExecutionBatch``

Contract
========

``RunnerCapability`` is the runner's stable declaration of what the orchestrator
may send.

Required fields:

- ``accepted_input_kinds``
- ``preferred_input_kind``
- ``supports_multi_item_batching``
- ``batch_unit_kind``
- ``packaging_strategy``

Accepted enums are intentionally small and come from the shared model module:

- ``InputKind``: ``image``, ``prepared-unit``, ``pdf``
- ``BatchUnitKind``: ``page``, ``prepared-unit``, ``pdf-document``
- ``PackagingStrategy``: ``direct``, ``image-to-pdf``, ``unit-to-pdf-batch``

``RunnerExecutionBatch`` is the exact JSON shape for one invocation record.

Required persisted fields:

- ``schema_version``
- ``batch_id``
- ``run_id``
- ``document_id``
- ``runner``
- ``capability``
- ``batch_size``
- ``items``
- ``started_at_utc``
- ``result_status``

Optional but expected in normal runs:

- ``packaging_artifact_id``
- ``finished_at_utc``
- ``retry_of_batch_id``
- ``retry_strategy``
- ``failure_item_ids``
- ``output_artifacts``
- ``warnings``

Validation Invariants
=====================

- ``preferred_input_kind`` appears in non-empty ``accepted_input_kinds``.
- ``batch_size`` equals the number of unique ordered ``items``.
- failure ids are submitted item ids; succeeded has none, partial has some but
  not all, and failed names all submitted ids.
- finish time does not precede start time.
- every output artifact names the batch items it represents.
- a model-backed ``RunnerReference`` records model revision, hosting/runtime
  identity and revision, configuration digest, and prompt digest when prompting
  is used. Mutable model names such as ``main`` are not reproducible revisions.

Interface Extraction Rule
=========================

Do not implement a speculative plugin framework from this persistence schema.
First build two or three real candidate adapters. Extract the smallest common
runtime protocol only after their differing input, output, and failure behavior
is observed. Persist runner-specific raw artifacts rather than flattening useful
capabilities to fit an invented interface.

Why This Shape
==============

This schema is the minimum needed to answer the operational questions that will
actually matter in this corpus:

- what exact runner and model revision produced this witness
- whether the page ran full-page or as prepared units
- whether ``olmocr`` or a future runner consumed images directly or batched PDFs
- what batch size was used
- what failed and what was retried

Operator Notes
==============

- Preserve one ``RunnerExecutionBatch`` record per invocation, even when the
  invocation produced no usable witness output.
- Treat batch size as measured policy, not folklore.
- Dense dictionary pages and subdivided pages may need different defaults from
  ordinary prose pages.
