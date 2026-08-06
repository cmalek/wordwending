==============================================================
ADR 0004: Raw Witness, Graph, Overlay, and Export Stay Split
==============================================================

:Status: Accepted
:Date: 2026-07-25

Context
=======

Hard OCR research work needs auditability. If graph-building or merge logic is
wrong, the team must be able to rebuild derived outputs from preserved raw
artifacts.

Decision
========

``wordwending`` stores four distinct layers:

1. Raw witness layer
2. Derived graph layer
3. Overlay layer
4. Export layer

The raw witness layer stores exact outputs from each pass unchanged.

The derived graph layer stores normalized page graph data built from those raw
artifacts.

The overlay layer stores human-authored corrections or adjudications without
destroying underlying machine output.

The export layer stores consumer-friendly outputs derived from graph plus
overlays.

Consequences
============

- Expensive OCR or layout passes do not need reruns when graph merge logic
  changes.
- Model comparisons remain possible after the fact.
- Human corrections remain explicit and diffable instead of silently mutating
  raw OCR output.
