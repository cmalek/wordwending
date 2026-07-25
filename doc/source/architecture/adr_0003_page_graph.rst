=========================================
ADR 0003: Shared Page Graph Is Core Model
=========================================

:Status: Accepted
:Date: 2026-07-25

Context
=======

``bochord`` will run competing or complementary passes on the same page.
Different engines may be strong at different things:

- text recognition
- line segmentation
- reading order
- style cues
- table region detection

Decision
========

The canonical derived page model is a shared page graph anchored to page
coordinates.

V1 graph node kinds are intentionally small:

- ``region``
- ``line``
- ``span``
- ``note``

V1 semantics:

- ``region`` covers layout areas such as paragraph, table area, marginalia, or
  footnote area.
- ``line`` records ordered textual lines inside a region.
- ``span`` records aligned styled runs such as plain, italic, bold,
  superscript, subscript, or footnote marker.
- ``note`` records note bodies linked from marker spans.

Tables remain lazy in v1: a table is a ``region(kind=table)`` plus optional raw
table witness, not a full cell graph.

Consequences
============

- All pass outputs must be alignable into shared page coordinates.
- Merge logic can combine best text from one engine with best structure or style
  from another.
- V1 avoids ontology explosion while still modeling the signals this corpus
  actually needs.
