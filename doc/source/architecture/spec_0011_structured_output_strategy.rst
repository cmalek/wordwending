===================================
Spec 0011: Structured Output Strategy
===================================

Purpose
=======

Define how ``bochord`` should relate its standard OCR output to
document-specific downstream structures such as dictionaries, grammars, readers,
or source texts with translation.

Core Rule
=========

``bochord`` should standardize first on its own evidence-preserving OCR
intermediate structure, not on one downstream document ontology.

That standard intermediate structure is:

- prepared source artifacts
- raw witness artifacts
- accepted page graph
- review and evaluation metadata
- standard export families

Downstream packages should transform that standard output into
document-specific structures.

Those downstream transformations should preserve bibliographic and acquisition
provenance so target-domain models retain source identity and citation context.

Why This Matters
================

The user cares about many structurally different targets:

- dictionary entries such as Bosworth-Toller
- grammar sections such as Wright and Wright
- grammar sections such as Mitchell
- readers and source texts with translation

These should not all be forced into one immediate OCR output ontology.

TEI P5 as Structural Reference
==============================

TEI P5 dictionary guidance is a strong reference model for downstream lexical
structure.

Current official TEI guidelines include a dedicated dictionaries chapter:

- `TEI P5 Guidelines Index <https://www.tei-c.org/release/doc/tei-p5-doc/en/html/index.html>`_
- `TEI Dictionaries Chapter <https://www.tei-c.org/release/doc/tei-p5-doc/en/html/DI.html>`_

For dictionary-focused downstream work, ``bochord`` should allow a
TEI-inspired structured target model expressed as Python or Pydantic data, even
when XML output is not desired.

Recommended Strategy
====================

V1 should distinguish three layers:

1. ``bochord`` standard OCR structure
2. optional downstream transformation profiles
3. target-domain consumer models

Layer 1 belongs in ``bochord``.
Layers 2 and 3 usually belong in downstream packages.

Dictionary Recommendation
=========================

For dictionaries, especially Bosworth-Toller-like material, a TEI-inspired
intermediate target is a good idea.

Recommended use:

- treat TEI P5 as a modeling reference, not as a requirement to emit XML
- define Python or Pydantic models that mirror useful TEI-like concepts
- keep those models in a downstream dictionary-focused package unless they are
  needed broadly across multiple ``bochord`` users

This works well because TEI already distinguishes:

- entry structure
- form information
- grammatical information
- sense information
- examples
- notes
- related or grouped entries
- editorial versus lexical view

Why Not Make TEI the Primary bochord Output
===========================================

OCR orchestration and evidence preservation happen before many domain-specific
structural commitments are safe.

If ``bochord`` standardizes too early on one structured document model:

- non-dictionary texts get distorted
- review becomes biased toward one output ontology
- graph and provenance layers risk being flattened too soon

Therefore:

- use TEI-inspired models downstream where they fit
- keep ``bochord`` itself standardized on evidence-rich OCR structure

Downstream Package Responsibility
=================================

Yes: downstream packages should generally transform ``bochord`` standard output
into desired document-specific structures.

Examples:

- dictionary package turns page graph plus review outputs into TEI-inspired
  lexical entry models
- grammar package turns page graph plus review outputs into structured section,
  example, and note models
- reader package turns page graph plus review outputs into text plus translation
  structures

This keeps ``bochord`` reusable while still enabling strong domain models.

When bochord May Grow a Shared Target Profile
=============================================

If one downstream structure proves broadly reusable across many OCR tasks,
``bochord`` may later define a shared optional transformation profile.

Examples that might qualify later:

- generic dictionary-entry profile
- generic scholarly-note profile
- generic bilingual text profile

But these should be added only after real repeated use, not speculative design.

Non-Goals
=========

V1 should not attempt:

- one universal downstream schema for every document genre
- direct XML-first workflow
- forcing all consumers into TEI vocabulary when their target is not lexical
