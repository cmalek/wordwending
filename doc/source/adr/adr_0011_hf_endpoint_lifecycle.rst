======================================================
ADR 0011: Hugging Face Endpoint Lifecycle
======================================================

:Status: Accepted
:Date: 2026-08-07

Context
=======

``wordwending run`` and bake-off consume HTTPS URLs from
``Settings.huggingface_model_endpoints``, but operators previously had to
create, resume, pause, and delete Hugging Face Inference Endpoints outside the
product. Spec 0004 Phase 10 requires operational hardening for hosted runners
(deploy, health, cost controls). Waves A–H shipped an ops skeleton (resume
ledger + inspect checksums) without endpoint lifecycle automation. Live Phase 5
bake-off evidence is fragile without a repeatable hosted workflow.

Design detail lives in
``docs/superpowers/specs/2026-08-07-hf-endpoint-lifecycle-design.md``.
Implementation plan:
``docs/superpowers/plans/2026-08-07-hf-endpoint-lifecycle.md``.

Decision
========

V1 manages Inference Endpoints **inside** ``wordwending`` via a catalog-driven
``EndpointLifecycleService`` over the official ``huggingface_hub`` Inference
Endpoints API (not shell wrappers around ``hf`` as the primary path).

Locked choices:

- **CLI and ensure:** explicit ``wordwending endpoints up|down|status`` **and**
  optional ``--ensure-endpoints`` on ``run`` / ``bakeoff``.
- **Spin-down:** **pause** by default; **delete** only with an explicit flag.
- **Idle cost control:** configure HF **scale-to-zero** when creating/updating,
  **and** a local session ledger + idle watchdog that **pauses** (never
  auto-deletes).
- **Catalog:** keyed by ``runner_id`` from the start; first entries ``olmocr``
  and ``kraken``; Hub ``repository`` + immutable ``revision`` (reject
  ``main`` / ``master`` / ``latest`` / ``head``).
- **Secrets:** only ``Settings.huggingface_api_key``; never in catalog, ledger,
  or git.
- **URLs:** in-process overlay into ``huggingface_model_endpoints`` for runners;
  do not commit ephemeral endpoint URLs.
- **Layering:** models in ``wordwending.models``; service + thin HF client in
  ``wordwending.services``; thin Click in ``wordwending.cli``.

Non-decisions (deferred / forbidden under this ADR alone):

- Claiming Spec 0004 Phase 10 COMPLETE (quotas UX, full cost accounting, corpus
  regression gates, operator calibration monitoring remain deferred).
- Local GPU inference or downloading full model weights to the laptop.
- FakePassRunner or fake endpoints as Phase 10 exit evidence.
- Terraform / external IaC as the daily operator loop (``hf endpoints`` may
  remain a documented escape hatch).

Consequences
============

- Operators can bring up pinned endpoints for catalogued runners, run work, then
  pause or delete without leaving the product CLI.
- Live bake-off and ``run`` can use ``--ensure-endpoints`` fail-closed against
  real hosted URLs.
- Phase 10 documentation must keep **NOT COMPLETE** honesty while describing
  this lifecycle slice as preferred ops path.
- Default tests mock the HF client; live create/pause/delete stays behind
  ``pytest.mark.integration``.
