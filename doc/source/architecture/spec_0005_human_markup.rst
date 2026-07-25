==================================
Spec 0005: Human Markup and Review
==================================

Purpose
=======

Define exactly how human markup must be performed in ``bochord``.

Design Rule
===========

Human markup is review over evidence, not freeform rewriting.

Operators work against:

- prepared page image
- raw witness artifacts
- derived page graph
- evaluation flags

Operators do not edit exports directly.
Operators do not edit raw OCR witness files directly.

Markup Targets
==============

Human markup may target these scope levels:

- page
- region
- note
- span

V1 should not allow arbitrary partial-coordinate edits outside one of those
scopes.

Stable ID Requirement
=====================

Every reviewable object must have a stable id.

Minimum reviewable ids:

- ``page_id``
- ``region_id``
- ``note_id``
- ``span_id``
- exportable ``chunk_id``

Without stable ids, markup history becomes fragile and non-replayable.

Markup State Model
==================

Trust states:

- ``machine``: no human acceptance yet
- ``reviewed``: human checked and accepted unchanged
- ``corrected``: human changed machine output

Review state should be explicit per scope object. A reviewed footnote does not
upgrade the whole page automatically.

Append-Only Event Model
=======================

Each markup action is one append-only review event.

Each event must record:

- event id
- target object id
- target scope
- prior trust state
- new trust state
- action verb
- operator id
- timestamp
- optional free-text note
- optional payload describing the correction

Required Review Verbs
=====================

``accept``
    Human checked target and accepts it unchanged.

``correct_text``
    Human replaces machine-derived text for one review target.

``correct_style``
    Human changes style classification such as ``plain`` to ``italic``.

``link_note``
    Human links a footnote marker to a note body.

``unlink_note``
    Human removes an incorrect note linkage.

``split_region``
    Human indicates one region should become multiple regions.

``merge_region``
    Human indicates multiple regions should be treated as one.

``flag``
    Human records a problem or unresolved ambiguity without asserting a final
    correction.

Payload Rules
=============

Payloads must stay small and verb-specific.

Examples:

``correct_text``
    new text value, optional reason

``correct_style``
    prior style, new style

``link_note``
    marker id, note id

``split_region``
    target region id plus resulting region definitions or split anchors

``flag``
    flag type, message, optional severity

V1 should not support arbitrary scriptable transformation payloads.

Required Operator Workflow
==========================

Operators should review in this order:

1. prepared page image
2. raw text witness
3. raw layout or line witness
4. raw style witness
5. derived page graph
6. evaluation flags
7. review event entry

This ordering reduces the risk of correcting a derived claim without checking
 evidence.

Span-Level Markup Rules
=======================

Use span-level review when:

- text is wrong but region and line are right
- style is wrong on a local run
- footnote marker classification is wrong

Do not use span-level review to mask region-level segmentation failures that
need ``split_region`` or ``merge_region``.

Region-Level Markup Rules
=========================

Use region-level review when:

- a note block was absorbed into prose
- a table region was misread as ordinary text block
- multiple logical blocks were merged
- one logical block was split incorrectly

If the error is structural, record a structural review event rather than many
tiny span edits.

Footnote Markup Rules
=====================

Footnotes are first-class review objects.

Required practice:

- review marker and note body separately
- preserve marker-to-note linkage explicitly
- do not flatten note text into main text during markup
- keep note body as retrievable chunk after review

If marker exists but note body is uncertain:

- mark linkage with ``flag`` first
- only use ``link_note`` when operator can assert the mapping

Style Markup Rules
==================

V1 style classes are intentionally small:

- ``plain``
- ``italic``
- ``bold``
- ``superscript``
- ``subscript``
- ``footnote-marker``

Operators should correct to these classes only.
Do not invent ad hoc new style names during review.

Acceptance Rules
================

Use ``accept`` only after checking target against source image and relevant raw
witnesses.

Do not bulk-accept a whole page unless operator truly reviewed whole page.
Prefer the narrowest honest scope.

Flagging Rules
==============

Use ``flag`` when:

- evidence is ambiguous
- two pass runners disagree materially
- note linkage is plausible but not certain
- style cannot be determined confidently
- region boundaries are unclear

Flags should not silently upgrade trust state.

Operator Notes
==============

Good markup is small, explicit, and replayable.

Bad markup patterns:

- editing Markdown export by hand
- overwriting raw OCR files
- applying page-wide trust after checking one note
- using text correction to hide structural segmentation failure
- inventing new freeform style labels
