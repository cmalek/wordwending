=====================================================
ADR 0007: V1 Starts with olmOCR Plus Kraken, Not More
=====================================================

:Status: Accepted
:Date: 2026-07-25

Context
=======

The package needs a practical v1 engine strategy. More engines can be added
later, but v1 needs one strong text-first path and one historical OCR ecosystem
with structured outputs.

Decision
========

V1 starts with:

- ``olmocr`` as primary difficult-text recognizer candidate
- ``kraken`` as the first structured historical OCR ecosystem for line, layout,
  coordinate-rich, and fallback text evidence

Other framework judgments for now:

- ``Docling`` is a strong secondary research target and a good source of ideas
  for layout, OCR, and table passes, but not the first orchestration spine.
- ``OCRmyPDF`` is mature and useful for preprocessing ideas, but is not the
  central architecture for image-first multi-witness research bundles.
- ``python-doctr`` is a model toolkit, not the first orchestration boundary.

Consequences
============

- Early implementation stays small enough to ship.
- ``bochord`` still leaves room for future runners such as Docling-based or
  custom style passes.
- Evaluation schema must be engine-agnostic so later replacements remain cheap.
