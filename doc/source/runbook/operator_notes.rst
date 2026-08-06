=====================
Operator Notes
=====================

Purpose
=======

This page is the short practical runbook for humans operating ``wordwending`` on
difficult documents.

For the end-to-end source-to-Markdown operator path, see
:doc:`/runbook/from_source_to_markdown`.

Non-Negotiable Rules
====================

- Treat OCR output as evidence, not final truth.
- Keep raw pass artifacts.
- Keep prepared page images.
- Compare source quality, preparation, structure, text, typography, and note
  linkage separately.
- Use overlays for corrections.
- Rebuild derived outputs rather than hand-editing machine outputs in place.

What To Preserve
================

For every serious run, preserve:

- source PDF or source images
- prepared page images
- raw artifacts from every executed runner
- page graph outputs
- evaluation outputs
- overlays
- run manifests

If one of these is missing, future debugging gets harder fast.

What To Review First
====================

When triaging a page, inspect in this order:

1. prepared page image
2. raw text witness
3. line or layout witness
4. style witness
5. page graph
6. evaluation flags
7. overlay candidates

This keeps review grounded in evidence instead of derived claims.

When To Rerun
=============

Rerun the whole document or page set when:

- PDF-to-image recipe changes
- page dimensions or DPI changes
- OCR runner config changes
- runner version changes
- alignment logic changes and raw witness is missing needed fields

Do not pretend outputs are comparable when preparation inputs changed.

When To Avoid Reruns
====================

You should usually avoid expensive OCR reruns when only these changed:

- graph-building logic
- note-linking heuristics
- evaluation thresholds
- export formatting
- overlay application

Those should rebuild from preserved raw witness artifacts.

Practical Review Heuristics
===========================

Check these first on hard philological pages:

- macrons dropped or replaced
- ligatures expanded
- thorn or eth substituted
- italic glosses flattened into plain text
- bold headwords lost
- superscripts flattened
- footnote markers detached from note bodies
- note bodies absorbed into main text
- table regions treated as ordinary prose

Common Failure Shapes
=====================

Good text, bad style
    Often looks acceptable in plain text exports but destroys later parsing.

Good text, bad note linkage
    Creates subtle downstream citation or gloss errors.

Good CER, bad reading order
    Dangerous on multi-column or note-heavy pages.

Bad text from one runner, good structure from another
    This is normal. Merge later. Do not force one winner too early.

Before Starting Any Review Task
===============================

Refuse a task as malformed rather than guessing its intent when the interface
does not show:

- one exact question and target scope
- prepared image plus checksum
- required raw evidence views
- review dimensions being certified
- allowed actions including flag/abstain where applicable
- completion checklist and coverage
- guideline version and base run/graph revision

At completion, check that the event names only dimensions actually inspected.
For example, accepting text does not accept typography, and accepting one span
does not accept a region or page. Use ``unknown``, ``mark_illegible``, ``flag``,
``abstained``, or ``needs-adjudication`` rather than a plausible guess.

If Evidence Changed
===================

Stop review when the visible prepared-image checksum, source run, graph revision,
or target ids differ from the task packet. Request/rebuild a successor task and
overlay. Do not apply a stale correction by visual position alone.

Research Discipline
===================

- Change one major variable at a time when benchmarking.
- Expand gold slices gradually across difficulty classes.
- Prefer a smaller number of pages with high-quality annotations over a large
  low-trust pseudo-gold set.
- Keep operator notes near bundle outputs when a page has unusual failure modes.

Human Markup
============

Detailed human markup rules live in:

- :doc:`/architecture/spec_0005_human_markup`

Operators should treat that document as normative for:

- what can be edited
- what review verbs mean
- how trust states change
- how note and style corrections must be recorded
- exactly how source, preparation, layout, text, typography, note, gold, and
  adjudication tasks are completed
