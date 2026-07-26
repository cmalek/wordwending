============================================================
ADR 0005: Gold-Set Evaluation Is First-Class, Not Optional
============================================================

:Status: Accepted
:Date: 2026-07-25

Context
=======

This problem domain cannot be managed by intuition alone. Difficult pages need
multiple passes and targeted review. A single aggregate score hides damaging
failure modes.

Decision
========

Evaluation is a first-class pipeline stage from v1.

Evaluation score families remain separate:

- text accuracy
- structure accuracy
- typography accuracy by independent facet
- note-linkage accuracy

V1 style scope is intentionally narrow and useful:

- plain
- italic
- bold
- superscript
- subscript
- footnote marker
- footnote block

Evaluation must support gold slices and watchlist metrics for:

- macrons and ligatures
- thorn and eth
- other difficult characters or symbols
- reading order and line-join fidelity
- footnote handling
- style retention

Consequences
============

- Review gates can say ``text pass, style fail`` instead of hiding failure in an
  average.
- New passes can be judged against corpus-relevant criteria from day one.
- Benchmarking is part of the product architecture, not later research debt.
