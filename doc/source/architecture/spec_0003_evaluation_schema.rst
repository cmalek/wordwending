================================
Spec 0003: V1 Evaluation Schema
================================

Purpose
=======

Define the v1 evaluation contract so every pass set can be measured
consistently.

Score Families
==============

Every evaluated page reports three first-class score families:

``text``
    OCR character and token fidelity

``structure``
    Reading order, line joins, region coverage, note linkage, and similar
    structural correctness

``style``
    Per-facet retention of typography, plus independently scored note-marker roles

Text Metrics
============

Minimum v1 text metrics:

- character error rate
- word error rate
- exact-match rate for watchlist characters
- macron recall
- ligature preservation rate
- thorn and eth preservation rate

Structure Metrics
=================

Minimum v1 structure metrics:

- line ordering correctness
- region coverage
- note marker to note block linkage success
- line-join fidelity where gold data exists
- table-region detection presence or absence where gold data exists

Style Metrics
=============

Minimum v1 typography and role metrics:

- italic span retention
- bold span retention
- superscript span retention
- footnote marker retention
- footnote block detection or linkage correctness

Flags and Gates
===============

Scores are not enough. The schema should also emit review flags such as:

- missing watchlist character family
- style-family collapse
- ambiguous note linkage
- low-confidence merged graph region
- raw pass disagreement above threshold

The v1 schema should avoid one blended score. Summary output may present grouped
status, but underlying families remain separate.

Gold Data Expectations
======================

Gold slices may be partial and page-local.

V1 gold data should support:

- reference text spans
- watchlist character spans
- style-labeled spans
- note marker and note block annotations
- optional structure annotations for reading order or table regions
