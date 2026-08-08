======================================
Wave B Architecture Notes (2026-08-07)
======================================

:Status: Accepted
:Date: 2026-08-07

These notes record two Wave B decisions that refine accepted architecture
without superseding the ADR chain. They are honest about what ships in Wave A/B
versus what remains deferred.

Spec 0001 Waive: PageAlignmentService and PageGraphBuilder
==========================================================

:Supersedes: nothing (temporary implementation waiver)
:Revisit: after Wave F bake-off if merge-locality or testability fails

Spec 0001 lists ``PageAlignmentService`` and ``PageGraphBuilder`` as separate
core services with distinct responsibilities for coordinate normalization,
evidence alignment, and derived page graph construction.

**Wave B waives extracting those services as separate modules.** For v1 spine
work through Wave C, ``wordwending.services.merge`` owns the full merge
pipeline:

- structure scaffold selection (Spec 0009)
- coordinate-space normalization and witness alignment
- text, typography, role, and note-link resolution onto the scaffold
- emission of the accepted derived page graph with provenance

The public facade is ``AbstainingMergeService``; per-page orchestration lives in
``MergeOrchestrator``. Assemble calls merge; it does not reimplement alignment
or graph build.

This waiver is **temporary**. If the Wave F bake-off shows that alignment or
graph construction must be split for locality, reuse, or independent testing,
extract ``PageAlignmentService`` and/or ``PageGraphBuilder`` then and update
Spec 0001 accordingly. Until that gate, treat Spec 0001's separate service
names as aspirational boundaries, not missing modules.

ADR 0009 Follow-up: Human Correction Boundary
==============================================

:Supersedes: ADR 0009 consequence "Human correction uses eScriptorium first"
:Related spike: :doc:`spike_0001_page_escriptorium` (closed, **reject**)

ADR 0009 required a bounded spike before committing to OCR-D/PAGE and
eScriptorium as the human-review boundary. Spike 0001 recorded that eScriptorium
native PAGE export preserves region and line structure plus line-level text, but
does **not** round-trip the stable ``Word``/``span-*`` ids required by ADR 0008.
Phase 1 stopped at that cost gate.

**Follow-up decision (Wave B):** the v1 human correction boundary is a custom
``wordwending review`` CLI, not eScriptorium. The CLI shipped in Wave D
(``review apply``, ``review materialize``); this note records the chosen
boundary.

Implications:

- Operators correct evidence through append-only review overlays (Spec 0014) and
  Spec 0005 review concepts. Assemble / ``review issue`` emit pending
  ``ReviewTask`` packets (``overlays/pending_tasks.json``); humans still
  hand-author review **events** / ``PageOverlay`` JSON for ``review apply``.
  ``review rebase`` applies accepted leaf overrides onto the page graph before
  export (ADR 0008 successor overlay; JSONL history stays append-only).
- eScriptorium is **not** the v1 review UI. Do not build production workflows
  that depend on eScriptorium round-tripping span-level identity.
- ``PageXmlInterchangeService`` remains for **optional** PAGE XML import and
  export (interchange with external tools, recorded fixtures, and spike evidence).
  PAGE is an interchange format, not the operator review surface.
- Public software contracts stay validated JSON and Markdown; XML is not forced
  on downstream users (unchanged from ADR 0009).

ADR 0009 itself stays **Accepted** — the spike gate worked as intended. This
follow-up replaces only the "eScriptorium first" consequence with the custom CLI
choice once spike evidence exists.

References
==========

- :doc:`spec_0001_system_architecture`
- :doc:`spec_0009_merge_policy`
- :doc:`adr_0009_ocrd_page_escriptorium`
- :doc:`spike_0001_page_escriptorium`
- :doc:`spec_0005_human_markup`
- :doc:`spec_0014_review_overlay_schema`
- Wave plan: ``docs/superpowers/plans/2026-08-07-v1-spine-and-phase-completion.md``

Spec 0004 Phase 4 Status (2026-08-07)
======================================

After Waves A, C, and D, the v1 plan **Phase 4 full bullets (Waves A+C+D)** are
met on the fixture-backed spine: olmOCR + kraken witnesses adapt through
``assemble``, multi-witness merge persists **evaluation flags**
(``evaluation/flags.json``), operators hand-author review **events** /
``PageOverlay`` and apply overlays via ``wordwending review``, and ``eval`` /
``export`` follow without hand-edited ``DocumentBundle`` JSON. Hands-off
operator path follow-up: ``assemble --from-run`` builds the manifest;
assemble / ``review issue`` persist Spec 0005 pending ``ReviewTask`` packets;
``review rebase`` applies accepted overlay leaf overrides onto page graphs
(ADR 0008 successor overlay) so ``export`` sees corrections.

**Phase 6 COMPLETE:** ``PassRunner`` Protocol + ``PassRunnerRegistry`` (``olmocr`` /
``kraken``) with the execution spine typed to the Protocol. Fake runners remain
test doubles only.

**Not claimed complete:** **Phase 5 NOT COMPLETE** (bake-off harness
only); **Phase 10 NOT COMPLETE** (operational hardening). Wave H ships an **ops
skeleton only** (``run`` resume ledger, ``inspect-bundle`` checksum
verification, ``wordwending endpoints up|down|status`` lifecycle CLI with
optional ``--ensure-endpoints`` on ``run``/``bakeoff``); Spec Phase 10 exit
remains deferred. Spec 0004 Phase 4's **coordinate-rich second-runner**
bullet is met on the **fixture-backed spine** when kraken emits
``wordwending.kraken_segmentation/v1`` JSON; the **live HF endpoint must emit
v1 JSON** for the same geometry in production. Plain-text kraken fallback and
olmOCR remain provisional (null line boxes).
