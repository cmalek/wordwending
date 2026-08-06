======================================================
Spike 0001: PAGE / eScriptorium Interoperability
======================================================

:Status: Closed
:Date: 2026-07-26
:Decision: reject

Context
=======

ADR 0009 requires a bounded spike before committing to OCR-D/PAGE and
eScriptorium as the human-review boundary. Phase 1 exports two representative
``wordwending`` review packages (dictionary headword page and note-heavy page),
imports them into eScriptorium, applies operator text corrections, and records
the native PAGE XML export without post-processing.

The implementation plan hard-stops when any required stable id — including
``Word``/``span-*`` ids — fails to survive the round trip. Fuzzy matching or
recovery merges are out of scope for Phase 1.

Environment
===========

- **Image:** ``registry.gitlab.com/scripta/escriptorium@sha256:997e6f4e668ec65a3a0ae108f8ff1aa56e01c0eee16369b2fe8204d9a908ee68``
  (locally created ``2026-05-18T16:37:48.658854589Z``; application reported
  ``VERSION_DATE`` ``v1.0.0``)
- **Instance date:** 2026-07-26
- **Recorded fixtures:**
  ``tests/fixtures/interchange/dictionary-page.corrected.xml``,
  ``tests/fixtures/interchange/note-page.corrected.xml``

Procedure
=========

1. Export review ZIP + ``*.wordwending.json`` sidecar from ``PageXmlInterchangeService``.
2. Export PAGE directly with the canonical prepared-image filename, canonical
   width/height, importer-friendly integer coordinates, and explicit line
   geometry for the representative fixtures.
3. Import into eScriptorium, apply line-level transcription corrections
   (``drēorig sorrow`` on the dictionary page; ``Deletion 10`` on the note page).
4. Export native PAGE XML via ``PageXMLExporter`` with no ``merge_word_structure``
   or other reconstruction.

Fields preserved by native PAGE export
======================================

Observed directly in recorded exports:

- **Region ids** — ``region-0100-a``, ``region-0100-b``,
  ``region-0010-body``, ``region-0010-footnote``
- **Line ids** — ``line-0100-1``, ``line-0100-2``, ``line-0010-body-1``,
  ``line-0010-footnote-1``
- **Line-level text** — corrected ``Unicode`` at ``TextLine/TextEquiv``
  (``drēorig sorrow``, ``Deletion 10``, footnote body text)
- **Region/line geometry** — ``Coords`` and ``Baseline`` on imported lines
- **Region typing** — encoded as eScriptorium ``custom="structure {type:…;}"``
  rather than wordwending's ``type="…"`` attribute

Fields not preserved
====================

Native export **drops** the ``Word`` subtree entirely:

- No ``Word`` elements
- No stable ``span-*`` ids (``span-0100-headword``, ``span-note-marker-10``, etc.)
- No word-level ``TextStyle`` (italic, superscript) in export
- No ``ReadingOrder`` block (wordwending sidecar retains canonical order)

``import_corrected_page`` correctly raises ``ValueError: missing word ids: …``
when paired with the canonical sidecar.

Fields restored only from sidecar
=================================

The ``*.wordwending.json`` sidecar remains the honest source for wordwending-only
evidence that PAGE/eScriptorium never carried:

- Preparation provenance, transforms, checksums, coordinate-space ids
- Witness/runner ids and review state
- Note linkage (``note-10`` → ``span-note-marker-10``)
- Span-level typography facets (italic, superscript, baseline shift)
- Diplomatic vs normalized text split at span granularity

Re-merging Words from the export sidecar or source PAGE after native export
would invent span ids and violate the spike's id-survival rule. That approach
was used in an earlier commit and is explicitly disallowed.

Reusable processors and interfaces
==================================

The spike identified a narrow reuse boundary worth keeping:

- **Reuse directly:** eScriptorium's PAGE import/export workflow for region and
  line review, plus PAGE 2019-07-15 geometry, reading-order, and line-text
  conventions.
- **Keep wordwending-owned:** prepared-image provenance, transform chains,
  checksums, stable span/note ids, note linkage, and span-level typography.
- **Do not adopt yet:** OCR-D workspace management or ``ocrd-models`` for this
  slice; the bounded stdlib serializer/importer is enough for Phase 1 and
  avoids taking on a Python-version mismatch before the real round-trip earns
  it.

Unsupported correction actions
==============================

- **Word-stable round-trip through eScriptorium PAGE export** — required for
  wordwending span-level gold, typography, and note-marker linkage under ADR 0008.

Secondary findings
==================

- **Canonical package identity matters** — native exports drift from the
  canonical prepared-image binding recorded in the sidecar
  (``imageFilename``/dimensions differ from the reviewed package), so
  ``import_corrected_page`` now rejects them before any coordinate-space relabel.
- **Integer PAGE coordinates are enough for the bounded exporter** — the
  direct review package can emit importer-friendly integers without adding OCR-D
  dependencies or a second preprocessing tool.
- **Representative fixture coverage now includes formula + note linkage** — the
  note-page sidecar still carries prose, a formula token, a superscript marker,
  and a linked footnote even though native PAGE export only preserves line text.

Decision
========

**reject**

eScriptorium native PAGE export preserves region and line structure plus
line-level corrected text, but it drifts from wordwending's canonical prepared-image
identity and does not round-trip the required stable ``Word``/``span-*`` ids.
The canonical JSON sidecar cannot honestly restore those ids after export
without forbidden merge logic.

Phase 1 stops here per the plan cost gate. Do not build OCR-D workspace
management, production review UI, or fuzzy object matching on this evidence.

Evidence tests
==============

``tests/test_page_interchange.py`` records the failure mode:

- ``test_native_escriptorium_export_preserves_region_line_ids_and_text``
- ``test_native_escriptorium_export_lacks_stable_word_ids``
- ``test_native_escriptorium_export_rejects_import``

References
==========

- :doc:`adr_0009_ocrd_page_escriptorium`
- :doc:`adr_0008_stable_ids_and_review_history`
- Phase 1 plan: ``docs/superpowers/plans/2026-07-25-phase-1-page-interoperability-spike.md``
