======================================================
ADR 0009: Adapt OCR-D/PAGE and eScriptorium Boundaries
======================================================

:Status: Accepted
:Date: 2026-07-25

Context
=======

``wordwending`` needs multi-stage image preparation, coordinate-rich OCR evidence,
evaluation, and human correction. OCR-D already defines reproducible OCR
workflows and PAGE XML conventions. eScriptorium already provides mature human
segmentation, transcription, training-data, and import/export workflows.
Rebuilding those capabilities before testing interoperability would add risk
without improving Old English recognition.

Decision
========

Before implementing a custom orchestrator or review UI, build one bounded spike
that round-trips a representative page through:

1. ``wordwending`` prepared-image and transform provenance
2. OCR-D workspace conventions and PAGE-compatible regions, lines, baselines,
   reading order, text, and typography
3. eScriptorium import, operator correction, and export
4. ``wordwending`` Pydantic bundle, overlay, and gold contracts

PAGE is an internal interchange option, not the public output requirement.
Public software contracts remain validated JSON and Markdown. XML is not forced
on downstream users.

Adopt existing OCR-D processors or eScriptorium workflows where they satisfy a
stage. Write a ``wordwending`` adapter only where corpus-specific provenance,
evaluation, or model integration is missing.

OCR-D/eScriptorium interoperability does not authorize local OCR-model
execution. Local tools may prepare, annotate, transform, and evaluate images;
model inference remains on Hugging Face and returns importable witness artifacts.

References
==========

- `OCR-D workflows <https://ocr-d.de/en/workflows>`_
- `OCR-D PAGE conventions <https://ocr-d.de/en/spec/page>`_
- `OCR-D evaluation conventions <https://ocr-d.de/en/spec/ocrd_eval>`_
- `eScriptorium <https://escriptorium.eu/about/>`_

Consequences
============

- Coordinate and typography models remain compatible with mature interchange
  concepts without exposing XML as the canonical API.
- Human correction uses eScriptorium first unless the spike proves it cannot
  express a required review action safely.
- The spike is an implementation gate, not a commitment to use all of OCR-D.
