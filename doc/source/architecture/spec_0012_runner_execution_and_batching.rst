===========================================
Spec 0012: Runner Execution and Batch Policy
===========================================

Purpose
=======

Define how ``bochord`` executes OCR-related runners with respect to input
packaging, batching, throughput experiments, and model-specific runtime policy.

Why This Matters
================

The orchestration layer must remain model-agnostic, but actual OCR throughput
and quality depend heavily on:

- how inputs are packaged
- how many pages or units are grouped into one runner invocation
- whether a runner expects PDF-native flow or image-native flow
- whether dense small-font pages are executed full-page or as subdivided units

If these choices remain ad hoc, performance comparisons and quality comparisons
will be misleading.

Core Rules
==========

- Runner execution policy is explicit, versioned, and recorded in provenance.
- Input packaging policy is runner-specific, not assumed globally.
- Batch size is an experimental parameter, not folklore.
- ``bochord`` may package images into PDFs for a runner when that improves
  compatibility or throughput, but that choice must be explicit and measurable.

Runner Input Contract
=====================

Every pass runner should declare its execution input contract.

At minimum, a runner should specify whether it prefers or accepts:

- prepared images
- prepared units
- packaged PDFs
- one item per invocation
- multi-item batches per invocation

Suggested runner capability fields:

- ``accepted_input_kinds``
- ``preferred_input_kind``
- ``supports_multi_item_batching``
- ``batch_unit_kind``
- ``packaging_strategy``

Suggested values:

``accepted_input_kinds``
    ``image``, ``prepared-unit``, ``pdf``

``batch_unit_kind``
    ``page``, ``prepared-unit``, ``pdf-document``

``packaging_strategy``
    ``direct``, ``image-to-pdf``, ``unit-to-pdf-batch``

olmOCR-Specific V1 Policy
=========================

Current ``olmocr`` usage is successful enough to justify first-class support,
but it remains one runner, not the architecture.

Important current fact:

- current ``olmocr`` tooling accepts PDF inputs and also image-file inputs via
  its ``--pdfs`` path

V1 ``bochord`` should still support packaging prepared images or prepared units
into small batched PDFs for ``olmocr`` when that improves throughput or runtime
stability.

This is a ``bochord`` execution policy choice, not a false claim that ``olmocr``
cannot consume images directly.

Image-to-PDF Packaging
======================

``bochord`` should support converting prepared images or prepared units into PDF
artifacts before runner execution when a runner benefits from PDF-native flow.

Use cases:

- runner prefers PDF semantics
- local batching is easier with PDF packaging
- throughput improves when multiple items are grouped into one packaged batch

Packaging outputs should be preserved as runner-input artifacts when they are
material to later audit or benchmarking.

Batching Policy
===============

Batching is first-class execution policy.

Batching choices should be explicit for each runner:

- no batching
- fixed-size batching
- adaptive batching

V1 should begin with fixed-size batching and benchmarking rather than adaptive
policies.

Suggested batch concepts:

- ``batch_id``
- ``runner_id``
- ``batch_size``
- ``batch_item_kind``
- ``batch_packaging_artifact``

Batch Size Research
===================

Optimal batch size should be measured, not guessed.

The system should support controlled throughput experiments over:

- full pages
- prepared units
- packaged PDF batches
- different batch sizes for the same runner and same page class

The initial goal is not one universal batch size. The goal is evidence about
which batch sizes work best for:

- ordinary prose pages
- dense dictionary pages
- note-heavy pages
- different subdivision strategies

Recommended v1 approach:

- choose one conservative default batch size per runner
- support explicit experiment runs varying batch size
- record throughput and failure behavior in run metadata

Prepared Units and Batching
===========================

When subdivision exists, the execution policy must decide whether a batch is
made of:

- whole prepared pages
- prepared units from one page
- prepared units across multiple pages

Recommended v1 policy:

- preserve page-local grouping when possible
- allow batching multiple prepared units together only when ordering and
  provenance remain explicit
- never lose mapping from one batch item back to its source page and unit

Throughput and Quality Tradeoff
===============================

Batching is not only a throughput concern.

The system should assume batch policy may affect:

- throughput
- failure rates
- memory pressure
- OCR quality stability
- ordering or output parsing complexity

Therefore runner execution metadata should record:

- batch size
- execution duration
- per-batch failures
- retry behavior
- packaging mode
- input item list

Retries and Failures
====================

Runner execution policy should support explicit retry metadata.

At minimum, record:

- whether batch failed
- which items failed
- whether retry occurred
- whether retry used same batch or smaller replacement batch

V1 need not implement sophisticated adaptive retry splitting immediately, but it
should leave room for:

- whole-batch retry
- item-level retry
- reduced-size retry batch

Model Openness
==============

``bochord`` is not locked to ``olmocr``.

Execution policy must stay open to other runners that may:

- perform better on the corpus
- prefer image-native execution
- require different batching patterns
- expose different throughput-quality tradeoffs

This is why input packaging and batch policy belong to runner execution spec,
not to a global one-model assumption.

Required Provenance
===================

Each execution batch should record:

- ``batch_id``
- runner identity
- model identity and revision where applicable
- input packaging mode
- input artifact ids
- batch size
- start and end timestamps or duration
- retry metadata
- execution result summary

Operator Notes
==============

- Benchmark batch size on real page classes, especially dense dictionary pages.
- Do not assume the best full-page batch size is also the best subdivided-unit
  batch size.
- Preserve packaged batch artifacts when they materially affect runner behavior.
- Treat throughput benchmarks as runner-policy evidence, not timeless truths.

Non-Goals
=========

V1 does not need:

- cluster scheduling
- dynamic autoscaling
- learned batch-size optimization
- one universal batch policy across all runners
