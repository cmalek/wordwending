===========================================
Spec 0010: Page Classification and Cohorts
===========================================

Purpose
=======

Define how ``bochord`` classifies pages for preparation, evaluation, and
benchmark cohorting.

Why This Matters
================

Different page types need different preparation and OCR strategies.

Examples:

- an ordinary prose page may work well as one full-page OCR target
- a dense dictionary page may need column subdivision
- a note-heavy page may need stronger note-linkage review
- a table-heavy page may need structural caution even when text OCR looks good

If all pages share one undifferentiated evaluation pool, averages will hide the
very failures ``bochord`` exists to surface.

Core Rule
=========

Page class is a per-page property.

Page class must be:

- auto-suggested during assessment
- human-overridable
- stored in provenance
- available to preparation and evaluation logic

Suggested V1 Page Classes
=========================

V1 should support this page-class taxonomy:

- ``ordinary-prose``
- ``dense-dictionary``
- ``note-heavy``
- ``table-heavy``
- ``mixed-complex``

These classes are operational, not philosophical. They exist to drive better
preparation, better evaluation, and clearer review expectations.

Class Meanings
==============

``ordinary-prose``
    Mostly continuous running text with no dominant dense-column or heavy-note
    behavior.

``dense-dictionary``
    Small-font, tightly packed lexical material, often multi-column, where
    full-page OCR may underperform badly without subdivision.

``note-heavy``
    Pages where note markers and note bodies are significant enough that note
    linkage and note isolation are first-class concerns.

``table-heavy``
    Pages where tables or paradigmatic structures dominate layout and reading
    order cannot be treated like ordinary prose.

``mixed-complex``
    Pages combining multiple difficult traits without one dominant class, such
    as prose plus dense notes plus tabular regions.

Suggested Assessment Heuristics
===============================

V1 assessment may suggest page class from heuristic signals such as:

- apparent font size
- column count
- region density
- line density
- note-marker frequency
- size and count of note-like lower-page regions
- table-region detection
- mixed layout complexity

V1 need not use learned classification models.
Deterministic heuristics are acceptable and easier to audit.

Required Provenance Fields
==========================

Each page should record at least:

- ``page_class_suggested``
- ``page_class_final``
- ``page_class_source`` with values such as ``auto`` or ``operator``
- optional operator override reason

Preparation Interaction
=======================

Page class should influence preparation defaults.

Recommended v1 implications:

``ordinary-prose``
    prefer full-page first unless quality assessment says otherwise

``dense-dictionary``
    prefer stronger consideration of column subdivision and overlap

``note-heavy``
    preserve note regions carefully and warn on linkage risk

``table-heavy``
    preserve table regions explicitly and avoid prose-biased flattening

``mixed-complex``
    prefer conservative preservation and stronger review flags

Page class should guide defaults, not become an unoverrideable law.

Evaluation Cohorts
==================

Evaluation must support cohorting by page class.

At minimum, the system should support:

- per-page-class summaries within one document
- cross-document summaries by page class
- comparison of preparation modes within one page class
- comparison of OCR runners within one page class

Baseline Rules
==============

Recommended evaluation order:

1. compare within same page class and same preparation mode
2. compare within same page class across preparation modes when running
   experiments
3. only then compute broader aggregated summaries

This keeps dense dictionary pages from disappearing inside easier prose-page
averages.

Operator Override
=================

Operators may override auto-suggested page class when the page's function is
clearer to a human than to heuristics.

Override guidance:

- use override when page role is obvious and materially affects preparation or
  evaluation
- record a reason when overriding
- do not casually relabel pages only to make metrics look better

Review Interaction
==================

Page class should affect review expectations.

Examples:

- ``dense-dictionary`` pages should trigger stronger suspicion of full-page OCR
  failures
- ``note-heavy`` pages should trigger stronger note-linkage review
- ``table-heavy`` pages should trigger stronger structural caution

Non-Goals
=========

V1 does not need:

- hierarchical page ontology
- automatic section-level semantic labeling
- one perfect class for every page in ambiguous books
