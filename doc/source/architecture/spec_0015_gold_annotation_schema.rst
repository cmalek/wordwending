====================================
Spec 0015: Gold Annotation Schema
====================================

Purpose
=======

Define scorable gold slices with explicit anchors, coverage, exclusions,
guideline revisions, held-out splits, and adjudication metadata.

Binding
=======

``GoldDocument`` records schema version, document id, guideline id/version,
dataset split, creation time, annotators, optional adjudicator, and pages.

Every ``GoldPageAnnotation`` binds to one page number, source run, graph revision,
and prepared-image checksum. Moving annotations to a changed image or graph
requires an explicit rebase.

Anchors
=======

Text, typography, and region annotations must contain at least one resolvable
anchor:

- a stable graph-object id
- a bounding box in an identified coordinate space
- a polygon in an identified coordinate space

Unanchored annotations are invalid. Image geometry is preferred while graph ids
are unstable; graph ids are preferred once a reviewed graph is stable.

Coverage and Exclusions
=======================

Every page has one or more ``GoldCoverage`` records. Each names the evaluated
dimensions, page/object/image scope, and whether annotation is exhaustive in
that scope. Partial gold is honest only when these scopes define the denominator.

``do_not_score`` is distinct from illegibility. Exclusions require a reason and
remain reportable. Illegible text may be a scored class or excluded according to
the metric profile, but the policy must be fixed before model comparison.

Annotation Families
===================

``GoldTextSpan`` stores diplomatic text, optional deterministically normalized
text, and illegibility. ``GoldStyleSpan`` stores orthogonal typography and
semantic roles. ``GoldRegionAnnotation`` stores region kind and optional reading
order. ``GoldNoteLink`` stores marker span ids and note target id.

Metric Semantics
================

Metric profiles are versioned and fixed before evaluation:

- compare Unicode NFC grapheme clusters for diplomatic character error rate
- publish whether whitespace, punctuation, case, and line breaks are significant
- derive word error rate from the documented tokenizer, never ambient locale
- score regions with class-aware polygon/box IoU and a documented threshold
- score reading order as ordered relations within covered structure
- score typography per facet; bold italic is not one mutually exclusive class
- score note linkage as marker-to-note edges within exhaustive coverage
- define empty prediction, empty gold, absent facet, unknown, illegible, and
  ``do_not_score`` cases explicitly; never divide by an implicit denominator

Gold Process
============

Annotators calibrate against guideline examples before production work. Sampled
slices receive independent second annotation. Agreement is reported by
dimension. Disagreements remain separate until an adjudicator records a new
decision and the superseded annotation ids; annotations are never overwritten.

Train/development/test assignment occurs before engine comparison. Test slices
remain hidden from prompt, threshold, preprocessing, and model-selection work.
