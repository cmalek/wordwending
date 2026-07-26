==================================
Spec 0005: Human Markup and Review
==================================

Purpose
=======

Define exactly what ``bochord`` asks a human to inspect, how the decision is
recorded, and what a completed review does and does not certify.

Core Rule
=========

Human markup is evidence-bound review, not freeform rewriting. Operators edit
append-only overlays or gold annotations; they never edit raw witnesses,
canonical graphs, Markdown, or RAG exports directly.

No task may simply say "review this page." Every task packet must identify:

- one concrete question
- review type and independent review dimensions
- exact page, region, line, note, or span ids in scope
- prepared image checksum, source run, and graph revision
- evidence views that must be inspected
- allowed actions
- an explicit abstain or needs-adjudication path
- completion criteria and coverage to certify
- guideline id/version and relevant calibration examples

Review Dimensions
=================

Review is certified independently for:

``source-quality``
    Whether the acquired scan is usable and which defects are present.

``preparation``
    Whether crop, rotation, enhancement, and page subdivision preserve evidence.

``structure``
    Regions, lines, boxes/polygons/baselines, reading order, and containment.

``text``
    Diplomatic transcription only. Normalized text is regenerated
    deterministically after a diplomatic correction.

``typography``
    Font-family candidates, size estimate, weight, slant, baseline shift, small
    capitals, and letter spacing. These are independent facets: bold italic
    superscript text is one valid combination.

``note-linkage``
    Marker role, note-body identity, and marker-to-note relationship.

"Upright" replaces the ambiguous typography label "roman." It means not italic
or oblique; it does not mean serif, Latin-language text, or ordinary body text.

Trust and Coverage
==================

``machine`` means no human certification. ``reviewed`` means a human accepted
the named dimensions unchanged. ``corrected`` means a human changed the named
dimensions. Trust on one dimension never upgrades another dimension or a wider
scope. A text-reviewed span may still have machine-only typography.

The task result must record the exact inspected object ids or image coverage.
Page-wide certification is valid only when the task required and the operator
actually inspected the whole page for the named dimensions.

Required Evidence Order
=======================

The interface must present evidence in this order unless the task packet names a
stricter sequence:

1. source or canonical prepared page image
2. visible task scope and coordinate overlay
3. raw witness for the dimension under review
4. other independent witnesses, without hiding disagreement
5. current accepted page graph
6. evaluation flags and prior review events
7. allowed decision controls and completion checklist

The operator must be able to zoom to source pixels and toggle overlays. Derived
text alone is never sufficient evidence for text, structure, or typography
acceptance.

Source-Triage Procedure
=======================

1. Inspect the whole page at fit-to-page scale for missing edges, folds, severe
   gutter loss, bleed-through, obstruction, and non-page material.
2. Inspect representative body text at pixel scale for focus, compression,
   halftone, thresholding, and effective character resolution.
3. Check machine measurements for skew, DPI estimate, gutter shadow, markings,
   clipping, and scan artifacts against the image.
4. Choose ``usable``, ``usable-with-warning``, ``reprepare``, ``reacquire``, or
   ``abstain``. Record every material defect and the affected image area.
5. Complete only after the whole page and at least one small-font area were
   inspected. ``reacquire`` blocks expensive OCR unless explicitly overridden
   with a reason.

Preparation and Subdivision Procedure
=====================================

1. Compare source and prepared images with crop and transform overlays visible.
2. Verify that no glyph, marker, running head, note, or marginal content was
   accidentally removed.
3. Check that deskew/dewarp did not distort baselines or join/split characters.
4. Inspect the smallest meaningful text. If its effective glyph height is below
   the configured runner threshold, compare full-page and subdivided previews.
5. For columns or tiles, verify complete coverage, intended overlap, stable
   reading order, and a reversible mapping to the prepared-page coordinates.
6. Choose full page or the smallest subdivision that improves recognition while
   retaining context. The choice is page-local; adjacent pages may differ.
7. Complete only after every prepared unit is accounted for and the transform
   chain, image checksum, recipe, and override reason are persisted.

Layout Procedure
================

1. Inspect region boundaries before line or span corrections.
2. Classify body, note, marginalia, header, footer, table, paratext, or unknown.
3. Verify that every line belongs to exactly one intended region and that note
   blocks were not absorbed into body text.
4. Inspect reading order across columns, continued entries, notes, and page
   boundaries. Do not infer order solely from coordinate sorting.
5. Use ``correct_geometry``, ``reclassify_region``, ``reorder``,
   ``split_region``, or ``merge_region``. Split/merge events must contain complete
   replacement definitions, including line assignments and reading order.
6. If boundaries remain ambiguous, use ``flag`` or abstain. Do not repair a
   structural error with many text edits.
7. Complete only when every object in task scope has resolved containment,
   geometry, and order or an explicit unresolved flag.

Diplomatic-Text Procedure
=========================

1. Read from the prepared image, not from normalized text or a modern edition.
2. Compare the accepted text and each raw text witness character by character.
3. Preserve original graphemes, accents, punctuation, capitalization,
   abbreviations, spacing evidence, and line-break evidence according to the
   current guideline.
4. Correct only ``text_diplomatic``. Never type ``text_normalized`` during human
   review; the normalization pipeline regenerates it after overlay replay.
5. Use ``mark_illegible`` when the source pixels cannot support a defensible
   reading. Never silently guess from linguistic context.
6. Complete only after every grapheme in scope was inspected and all uncertainty
   is represented by an illegibility decision, flag, or abstention.

Typography Procedure
====================

1. Compare the target with neighboring text from the same page before deciding
   what counts as the local ordinary face.
2. Decide weight: ``regular``, ``bold``, or ``unknown``.
3. Decide slant: ``upright``, ``italic``, or ``unknown``.
4. Decide baseline shift: ``baseline``, ``superscript``, ``subscript``, or
   ``unknown``.
5. Record font-family candidates and font-size estimate only when the evidence
   supports them; preserve confidence and multiple candidates rather than
   inventing certainty.
6. Decide small capitals and letter spacing independently when material.
7. Assign semantic role separately. ``footnote-marker`` is a role, not a font
   style, and may itself be upright, italic, bold, or superscript.
8. Complete only when each required facet is selected, explicitly ``unknown``,
   or covered by an abstention. Do not collapse combinations into one style.

Note-Linkage Procedure
======================

1. Verify marker text/shape and its semantic ``footnote-marker`` role.
2. Inspect the candidate note body and surrounding notes in source reading order.
3. Confirm the marker-to-note mapping from visible numbering, symbols, placement,
   and sequence; linguistic plausibility alone is insufficient.
4. Use ``link_note`` only for a defensible mapping and ``unlink_note`` to remove
   an existing wrong mapping.
5. Flag or abstain if the marker or note body is missing, repeated ambiguously,
   clipped, or illegible.
6. Complete only after marker and note body were reviewed separately and every
   asserted link resolves to existing object ids.

Gold Annotation Procedure
=========================

1. Choose the benchmark split before annotation; final test slices stay held out
   during model and threshold selection.
2. Declare page, graph-object, or image-region coverage and the dimensions that
   are exhaustive inside it.
3. Annotate against the prepared image and current guideline, using graph ids
   when stable or image boxes/polygons while structure is under revision.
4. Mark illegible and ``do_not_score`` separately. Every exclusion requires a
   reason and remains visible in denominator reports.
5. A second annotator independently marks calibration and sampled production
   slices. Disagreements are preserved until adjudication; one annotation must
   not silently overwrite another.
6. Complete only when every in-coverage instance is annotated or explicitly
   excluded and the guideline version, annotators, image checksum, run, graph
   revision, and coverage are persisted.

Adjudication Procedure
======================

1. Show each independent decision and its evidence without presenting one as the
   default truth.
2. Re-inspect the source image and applicable calibration examples.
3. Choose one supported decision, enter a new adjudicated decision, or retain
   unresolved/illegible status.
4. Record adjudicator id, resolution, superseded event or annotation ids, and
   guideline version. Never erase the original decisions.

Task Completion and Rebase
==========================

A task may be marked ``completed`` only when all completion criteria are checked
and certified coverage is recorded. ``abstained`` and ``needs-adjudication`` are
valid outcomes, not incomplete work disguised as machine acceptance.

If the prepared image checksum, source run, graph revision, target ids, or
guideline changes, the old task cannot be applied silently. Create a successor
overlay, retain the predecessor id, rebase events whose targets still resolve,
and send conflicts back as explicit review tasks.

Prohibited Practices
====================

- editing exports or raw witnesses
- supplying normalized text in a human correction
- certifying typography after checking only transcription
- bulk-accepting a page after sampling one region
- guessing illegible text from context without marking uncertainty
- using text edits to hide structural errors
- treating a footnote marker as a mutually exclusive font style
- applying an overlay to a different image or graph revision without rebase
