===============================
Spec 0009: Merge and Alignment
===============================

Purpose
=======

Define how ``wordwending`` resolves competing pass outputs into one accepted derived
page graph.

Why This Matters
================

The architecture already depends on multi-pass evidence. Without an explicit
merge policy, graph-building becomes subjective and inconsistent.

Core Rule
=========

The accepted page graph stores one primary accepted interpretation per derived
object, while preserving competing evidence in provenance.

This means:

- one accepted text per accepted span
- one accepted value per typography facet and semantic role per accepted span
- one accepted note linkage per accepted note-marker relationship
- preserved alternate evidence in provenance, not as uncontrolled duplicate
  graph nodes

Merge Output Model
==================

Each accepted derived object should record:

- primary accepted value
- contributing evidence sources
- alternate candidate evidence, when material
- merge confidence
- current trust state

Primary value plus preserved alternatives is the v1 rule.
V1 should not store many equal-status competing graph values as first-class
canonical graph payload.

Merge Decision Order
====================

Recommended v1 merge sequence:

1. choose prepared page variant
2. normalize coordinate systems
3. align layout or line evidence
4. align text evidence to chosen structure scaffold
5. align typography and role evidence onto accepted text spans
6. resolve note linkage
7. emit graph with provenance and merge confidence

Structure Scaffold
==================

V1 should choose one structure scaffold per page during merge.

Recommended default:

- prefer the pass with strongest coordinate-rich line or layout output for the
  scaffold
- fit other evidence onto that scaffold

This avoids trying to merge two incompatible region hierarchies symmetrically.

Text Resolution Policy
======================

When text runners disagree:

- choose one primary text source for the accepted span
- preserve alternate candidate texts in provenance
- emit disagreement metadata when differences are material

Recommended default for v1:

- use a configured precedence order
- allow evaluation or heuristics to override when evidence is strong

Runner precedence is set only after corpus benchmark results. Before that,
candidate evidence remains equal-status raw witness input to an abstaining merge.

Typography Resolution Policy
============================

When typography evidence disagrees:

- resolve weight, slant, baseline shift, family, size, small capitals, and letter
  spacing independently
- preserve conflicting candidates and per-facet confidence in provenance
- keep semantic roles such as ``footnote-marker`` separate from visual facets
- lower confidence only for the facets in conflict

If evidence is too weak:

- emit ``unknown`` for that facet and a targeted review task when it matters
- do not convert missing evidence into regular/upright/baseline defaults

Note Linkage Policy
===================

Note linkage is a derived claim and must be explicit.

When marker-to-note mapping is unambiguous:

- accept the linkage

When ambiguous:

- preserve candidate linkages in provenance
- emit review flag
- do not over-assert one mapping unless merge policy has a clear deterministic
  basis

Confidence Model
================

Each accepted derived object should support:

- machine confidence from source runner, when available
- merge confidence from alignment or resolution logic
- trust state from human review lifecycle

These are different concepts and should not be collapsed.

Recommended meanings:

``machine_confidence``
    confidence emitted by originating model or heuristic

``merge_confidence``
    confidence that accepted graph value was resolved correctly from competing
    evidence

``trust_state``
    human review status: ``machine``, ``reviewed``, or ``corrected``

When To Flag Instead of Resolve
===============================

The merge policy should emit flags when:

- text disagreement is material and no clear primary source wins
- typography or semantic-role evidence conflicts strongly
- note linkage remains ambiguous
- structure scaffolds disagree in ways that break local reading order
- source evidence is insufficient for a trustworthy accepted object

Flags are better than false certainty.

Preparation Interaction
=======================

If multiple prepared page variants exist, merge policy must know whether it is
combining:

- multiple pass outputs from one prepared variant
- or outputs across multiple prepared variants

Recommended v1 policy:

- choose one prepared variant as the basis for one accepted page graph
- preserve other prepared-variant results as alternate run evidence

This avoids cross-variant coordinate confusion in the canonical graph.

Human Review Interaction
========================

Human review does not erase merge provenance.

After a human correction:

- accepted value changes
- trust state updates
- prior machine merge decision remains auditable in provenance and review event
  history

Non-Goals
=========

V1 does not need:

- fully probabilistic graph inference
- global joint optimization across whole document
- learned merge ranking models
