========================
Gold Annotation Protocol
========================

Purpose
=======

This runbook defines the reproducible user workflow for creating gold
annotations and verifying that two users produce byte-identical score
files. Follow it before comparing OCR runners or model revisions on held-out
pages.

Prerequisites
=============

- An accepted ``BundlePage`` graph for each page under review
- A frozen ``MetricProfile`` (for example
  ``tests/fixtures/evaluation/metric-profile-v1.json``)
- The annotation guideline id and version recorded in every gold file

Annotation Sequence
===================

Complete these steps in order for each document slice entering the benchmark
corpus.

1. **Assign the dataset split before any model work.**
   Record ``train``, ``development``, or ``test`` in the gold document header.
   Do not change the split after a runner has been tuned against the page.

2. **Record the guideline id and version.**
   Set ``guideline_id`` and ``guideline_version`` on the ``GoldDocument``.
   Every downstream score file must cite the same pair.

3. **Annotate coverage before object-level annotations.**
   For each page, write one or more ``GoldCoverage`` records that declare which
   review dimensions are exhaustive and which object ids they cover. Coverage
   gates denominators; without it, metrics silently exclude spans.

4. **Annotate diplomatic text and independent facets.**
   For each scored object:

   - ``GoldTextSpan`` — diplomatic Unicode, illegibility, and exclusions
   - ``GoldStyleSpan`` — each typography facet separately (weight, slant,
     baseline shift, size class)
   - ``GoldRegionAnnotation`` — region kind, order, and geometry anchors
   - ``GoldLineJoin`` — when a gold line spans multiple predicted lines
   - ``GoldNoteLink`` — marker-to-note edges and note roles

5. **Record exclusions and illegibility separately.**
   Use ``do_not_score`` with an ``exclusion_reason`` on spans or coverage when
   the annotator abstains. Use ``illegible`` on text spans when the ink is
   unreadable. Do not fold either case into diplomatic text.

6. **Second-annotate sampled slices.**
   A second annotator repeats steps 3–5 on a stratified sample (dictionary
   headword pages, note-heavy pages, ordinary prose). Retain both originals.

7. **Retain both originals.**
   Store each annotator's file under distinct ids. Do not overwrite the first
   pass when the second pass arrives.

8. **Adjudicator writes resolution plus superseded ids.**
   When annotations disagree, an adjudicator produces one resolved
   ``GoldPageAnnotation`` per page and records which annotation ids were
   superseded in operator notes or adjudication metadata.

9. **Run the CLI twice and compare output bytes.**
   Two operators (or one operator on two machines) run the same command.
   Identical inputs must yield byte-identical ``PageEvaluationSummary`` JSON.

   .. code-block:: bash

      wordwending eval --prediction PAGE.json --gold GOLD.json \
        --profile tests/fixtures/evaluation/metric-profile-v1.json \
        --output-json SCORES.json

   Compare with ``cmp SCORES-a.json SCORES-b.json``. Any difference indicates
   non-reproducible inputs, profile drift, or toolchain skew — not model quality.

Calibration Examples
====================

Use the Phase 1 PAGE interoperability fixtures as concrete calibration targets.
These pages exercised the dictionary and footnote review boundaries before gold
evaluation existed.

Dictionary headword page (``page-0100``)
----------------------------------------

From ``tests/fixtures/interchange/dictionary-page.base.json``:

- **Page class:** ``dense-dictionary``
- **Regions:** body column plus marginal structure
- **Coverage:** declare ``text`` and ``structure`` exhaustive over body span
  ids; typography coverage only where italic or small caps are legible
- **Text:** diplomatic headword and gloss lines (for example the corrected
  ``drēorig sorrow`` line from Spike 0001)
- **Typography:** score weight and slant facets independently when the runner
  emits style witnesses

Note-heavy page (``page-0010``)
-------------------------------

From ``tests/fixtures/interchange/note-page.base.json``:

- **Regions:** separate ``body`` and ``footnote`` regions with distinct reading
  order
- **Coverage:** exhaustive ``note_linkage`` over marker and footnote-block ids
- **Text:** body deletion markers and footnote body diplomatic strings
- **Note edges:** ``GoldNoteLink`` from inline marker spans to footnote-block
  regions; record exclusions when a marker is illegible

Dictionary and footnote pages stress different evaluation families. Calibrate
annotators on one page of each kind before scoring a full development split.

Gold File Shape
===============

A document-level gold file wraps page slices:

.. code-block:: json

   {
     "schema_version": "1.0.0",
     "document_id": "doc-example",
     "guideline_id": "diplomatic-v1",
     "guideline_version": "1.0.0",
     "dataset_split": "development",
     "pages": [
       {
         "page_id": "page-1",
         "coverage": [ ... ],
         "text_spans": [ ... ]
       }
     ]
   }

The CLI selects the page whose ``page_id`` matches the prediction file.

Operator Checklist
==================

Before declaring a gold slice ready for benchmark use:

- [ ] Dataset split assigned and frozen
- [ ] Guideline id/version recorded
- [ ] Coverage written before span annotations
- [ ] Exclusions and illegibility marked explicitly
- [ ] Second pass retained or adjudication recorded
- [ ] ``wordwending eval`` run twice with byte-identical output
