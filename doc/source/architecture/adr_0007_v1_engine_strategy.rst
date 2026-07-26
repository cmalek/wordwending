===============================================
ADR 0007: Select V1 Engines by Corpus Benchmark
===============================================

:Status: Accepted
:Date: 2026-07-25

Context
=======

The package needs a practical v1 engine strategy. More engines can be added
later, but v1 needs one strong text-first path and one historical OCR ecosystem
with structured outputs.

The current leading candidate is ``olmocr`` because it has already performed
well on difficult material, but the architecture must remain open to other
models when they perform as well or better on the real corpus.

Decision
========

V1 starts with a bake-off, not an engine commitment. The first candidate set is:

- ``olmocr`` because it has already handled difficult Old English characters well
- ``kraken`` for trainable historical text recognition and coordinate-rich output
- ``PaddleOCR-VL`` as an Apache-licensed document-understanding candidate
- ``Chandra OCR`` as a high-quality candidate only after its model license is
  confirmed acceptable for the intended deployment
- ``Surya`` or ``Docling`` when they provide a materially distinct layout or
  recognition baseline rather than duplicating another pass

Every candidate runs on the same prepared images and held-out gold slices.
Selection uses text, structure, typography, note-linkage, throughput, failure,
cost, and licensing results. A model is not adopted because it wins one easy
page or one aggregate score.

All candidate model inference runs on Hugging Face hosted endpoints. Local
execution is not a fallback because the operator laptop cannot support these
models. Hugging Face deployability, hardware availability, endpoint stability,
and hosted cost are therefore required bake-off criteria.

Other framework judgments for now:

- ``Docling`` is a strong secondary research target and a good source of ideas
  for layout, OCR, and table passes, but not the first orchestration spine.
- ``OCRmyPDF`` is mature and useful for preprocessing ideas, but is not the
  central architecture for image-first multi-witness research bundles.
- ``python-doctr`` is a model toolkit, not the first orchestration boundary.

Consequences
============

- The first vertical slice may use ``olmocr`` and ``kraken``, but their adapters
  remain provisional until the bake-off is complete.
- Runner interfaces are extracted only after two or three real adapters expose
  the common boundary; no speculative plugin framework is built first.
- Evaluation schema must be engine-agnostic so later replacements remain cheap.
- License and hosting constraints are scored alongside recognition quality.
