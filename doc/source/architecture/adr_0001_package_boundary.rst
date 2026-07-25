===============================================
ADR 0001: Package Boundary Is OCR Orchestration
===============================================

:Status: Accepted
:Date: 2026-07-25

Context
=======

``bochord`` exists to support difficult Old English OCR work on image-based
documents. The core problem is not a single recognizer choice. The core problem
is orchestrating multiple passes that preserve evidence needed for later
philological interpretation:

- difficult characters and diacritics
- reading order and layout
- style signals such as italic, bold, superscript, and footnotes
- later human review against gold examples

Decision
========

``bochord`` owns image-first OCR orchestration and witness production.

``bochord`` does not own downstream philological semantics such as:

- Old English morphology
- dictionary parsing
- lexicographic normalization
- product-specific interpretation of witness content

The package boundary is the generic workflow:

``acquire -> pdf-to-image prepare -> run passes -> align -> evaluate -> review -> export``

Consequences
============

- ``bochord`` may be reused by multiple downstream Old English products.
- OCR output remains evidence, not canonical semantic truth.
- Architecture should optimize for workflow clarity and rebuildability, not for
  one model-specific happy path.
- Downstream packages should consume exported witness bundles or normalized
  derived views instead of reaching into raw runner internals.
