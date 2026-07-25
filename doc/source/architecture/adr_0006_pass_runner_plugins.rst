==========================================================
ADR 0006: Engines Integrate Through Pass-Runner Interfaces
==========================================================

:Status: Accepted
:Date: 2026-07-25

Context
=======

``bochord`` must compare and combine multiple engines over time. Hard-coding
one engine into the orchestration spine would make later evaluation and
replacement expensive.

Decision
========

Engines integrate as pass runners behind a common interface.

Each pass runner:

- receives page-local input and run config
- produces one raw witness artifact set plus metadata
- never writes directly into the canonical page graph

Typical pass families include:

- text pass
- line or layout pass
- style pass
- table pass
- evaluation pass

Consequences
============

- The orchestration spine remains stable while engines change.
- Competing pass outputs can coexist in one bundle.
- Merge and graph-building logic stays centralized instead of spreading
  model-specific glue throughout the codebase.
