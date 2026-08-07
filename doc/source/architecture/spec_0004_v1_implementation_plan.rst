=====================================
Spec 0004: Ordered V1 Implementation
=====================================

Purpose
=======

Provide a build order that reduces irreversible architecture and model choices.
Each phase must leave one executable check and evidence for the next decision.

Phase 1: Interoperability Spike
===============================

- round-trip one Bosworth-Toller dictionary page and one prose/note page through
  OCR-D/PAGE-compatible geometry and eScriptorium review
- prove source, prepared-image, coordinate-transform, and object-id provenance
- record which existing processors and interfaces can be reused

Exit: corrected PAGE-compatible evidence can return to a valid ``wordwending``
bundle without losing text, typography, geometry, reading order, or note links.

Phase 2: Gold Protocol and Evaluator
====================================

- publish annotation and adjudication guidelines
- create calibration examples for diplomatic text, structure, typography, and
  note linkage
- annotate explicit coverage/exclusion regions
- reserve held-out test slices before comparing engines
- implement metric semantics from :doc:`spec_0003_evaluation_schema`

Exit: the same valid prediction can be scored repeatedly with fixed
denominators, and an operator can reproduce one gold annotation from the docs.

Phase 3: Acquisition and Preparation
====================================

- accept a PDF, one image, or an ordered folder/archive of page images
- extract or render PDF pages when source images are unavailable
- assess skew, gutter shadow, resolution, markings, artifacts, and effective
  font size before expensive OCR
- preserve source-to-prepared transform chains and checksums
- choose full-page or per-page subdivision, including mixed document policies

Exit: each source page has a reproducible prepared image, quality decision,
coordinate identity, warnings, and optional prepared units.

Phase 4: One Vertical Slice
===========================

- execute one provisional text runner and one coordinate-rich runner
- preserve raw witnesses and exact model/runtime/config identity
- build one ``region/line/span/note`` page graph
- score it, issue dimension-specific review tasks, apply an overlay, and export
  JSON plus Markdown

Exit: one representative page travels end to end without manual file surgery.

Phase 5: Candidate Model Bake-Off
=================================

- run ``olmocr``, ``kraken``, and licensed alternative candidates against the
  same prepared inputs and held-out gold using Hugging Face hosted endpoints
- measure quality by dimension and page class, plus latency, throughput, cost,
  failure rate, license, and Hugging Face operability
- measure batch sizes rather than adopting folklore defaults

Exit: recorded evidence selects the smallest useful runner set and page-class
policies. Losing or redundant candidates are not integrated further.

No phase adds local OCR-model inference. Unit tests use recorded fixtures or
mock endpoints; live integration and benchmark tests target pinned Hugging Face
deployments.

Phase 6: Runner Boundary
========================

**Status: COMPLETE** (Wave G). ``PassRunner`` Protocol extracted from the
``olmocr`` and ``kraken`` hosted adapters; ``PassRunnerRegistry`` resolves by
``runner_id``; execution spine and CLI are typed to the Protocol. Fake runners
remain test doubles only and are not exit evidence.

- extract the common pass-runner interface from two or three working adapters
- validate batch counts, item/output associations, retries, timestamps, and
  immutable model/runtime/config revisions
- persist raw artifacts before normalization

Exit: selected runners emit different witness families through one proven
contract without hiding runner-specific capabilities.

Phase 7: Alignment and Abstaining Merge
=======================================

- normalize PAGE-compatible boxes, polygons, and baselines through recorded
  coordinate transforms
- align independent text, structure, typography, and note-link evidence
- merge only above calibrated thresholds; otherwise retain disagreement and
  create a targeted review task

Exit: difficult pages produce an auditable graph or explicit abstention, never
silent guessed structure.

Phase 8: Human Review and Rebase
================================

- issue self-contained review task packets
- replay geometry, ordering, text, typography, note, flag, and illegibility
  events
- support adjudication and rebase/supersession when source runs or graphs change

Exit: every human certification names its dimensions, evidence, guidelines,
coverage, base run, and graph revision.

Phase 9: Exports and Retrieval
==============================

- emit canonical bundle JSON and human/agent Markdown
- emit provisional region and note RAG chunks with multi-page provenance
- keep dictionary-entry, grammar-section, and TEI-inspired semantic transforms
  in downstream packages until page-graph evidence justifies promotion

Exit: consumers can retrieve accepted content and trace every chunk to pages,
objects, witnesses, and a chunking recipe.

Phase 10: Operational Hardening
===============================

**Status: NOT COMPLETE** (Wave H). Ops skeleton only: ``run`` resume ledger for
completed batches and ``inspect-bundle`` verification of digests already
recorded in bundle-layout metadata. Spec exit is deferred.

- resumability, caching, artifact retention, and corruption checks
- Hugging Face endpoint deployment, health checks, secrets, quotas, cold starts,
  queueing, retries, and cost controls
- corpus expansion, regression gates, and operator calibration monitoring

**Shipped (ops skeleton):** resume ledger (``runner-resume-ledger.json`` /
``--force``); inspect checksum OK/FAIL/SKIPPED for recorded layout digests.

**Deferred (do not mark COMPLETE):** HF deploy/ops, quotas, cost controls,
corpus regression gates, operator calibration monitoring.

Exit: interrupted runs resume without data loss and deployed runners are
reproducible and observable.

Recommended Initial CLI
=======================

- ``wordwending prepare``
- ``wordwending run``
- ``wordwending eval``
- ``wordwending inspect-bundle``

Add review or endpoint-management commands only after the corresponding phase
proves a command-line workflow is the right boundary.
