=================================
Spec 0008: Text and Normalization
=================================

Purpose
=======

Define the v1 text contract for evidence-preserving OCR output and downstream
normalized views.

Why This Matters
================

These documents require both:

- philologically faithful text preservation
- deterministic normalized text for software and retrieval

If the system keeps only one text field, either evidence or usability will be
damaged.

Core Rule
=========

Every text-bearing derived object should support both:

- exact or diplomatic text
- normalized text

Suggested field names:

- ``text_diplomatic``
- ``text_normalized``

Scope
=====

This dual-text rule applies where text is meaningful on:

- ``span``
- ``note``
- ``region_chunk``
- ``footnote_chunk``
- ``stitched_chunk``

It may also apply to lines and regions when a direct text payload is stored.

Diplomatic Text
===============

``text_diplomatic`` is the evidence-preserving text closest to accepted page
graph truth.

Rules:

- preserve accepted grapheme identity
- preserve macrons and ligatures
- preserve thorn and eth
- preserve superscript content where text-bearing
- do not silently expand ligatures
- do not silently modernize forms
- do not silently flatten uncertain characters into normalized substitutes

``text_diplomatic`` may still be derived from corrected graph content after
human review, but it remains the philologically faithful field.

Normalized Text
===============

``text_normalized`` is the deterministic downstream convenience field.

It may support:

- normalized Unicode composition policy
- deterministic whitespace normalization
- deterministic line-join handling
- optional retrieval-friendly substitutions where explicitly defined

Normalization must be rule-based and documented.
It must never silently replace diplomatic truth.

Required Normalization Policy Areas
===================================

V1 must define explicit rules for:

- Unicode normalization form
- whitespace normalization
- line-break joining
- hyphen-at-line-end handling
- note marker retention or representation
- superscript retention or flattening strategy in normalized text

Ligature and Historical Character Policy
========================================

V1 should default to preserving historical characters in both diplomatic and
normalized text unless a derived retrieval field explicitly says otherwise.

Recommended default:

- ``æ`` stays ``æ``
- ``ǣ`` stays ``ǣ``
- ``þ`` stays ``þ``
- ``ð`` stays ``ð``

If retrieval systems want alternate forms such as ``ae`` or plain-vowel forms,
those belong in retrieval-oriented fields, not in primary normalized text.

Line Joining Policy
===================

V1 must be explicit about line joins.

Recommended model:

- page graph preserves line structure
- ``text_diplomatic`` at span or note level does not erase line provenance
- region or chunk level normalized text may join lines for readability
- joined text should record whether a join was direct, heuristic, or human
  corrected

Hyphenation Policy
==================

Do not silently remove all end-line hyphens.

Recommended approach:

- preserve source-observed hyphenation in diplomatic layer when relevant
- allow normalized or chunk text to join words only under explicit rule or human
  correction
- record join provenance where a significant textual decision occurred

Human Correction Semantics
==========================

``correct_text`` in review events should target accepted diplomatic text.

Normalized text is then regenerated from corrected diplomatic text by the
normalization pipeline.

Operators should not independently edit both diplomatic and normalized text.

Retrieval Fields
================

RAG outputs may include additional retrieval fields such as:

- ``text_search``
- ``text_ascii_fallback``
- ``text_query_normalized``

These are downstream convenience fields and must never replace:

- ``text_diplomatic``
- ``text_normalized``

Non-Goals
=========

V1 does not need:

- full linguistic normalization
- lemma-level normalization
- automatic orthographic modernization
- language-model rewriting for readability
