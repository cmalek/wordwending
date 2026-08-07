# Hugging Face Endpoint Lifecycle Design

**Date:** 2026-08-07  
**Status:** Approved; implementation plan at
``docs/superpowers/plans/2026-08-07-hf-endpoint-lifecycle.md``  
**Branch context:** Phase 10 ops slice after Waves A–H spine  
**Approach:** In-repo `EndpointLifecycleService` over `huggingface_hub` Inference Endpoints API (Approach A)

## Problem

`wordwending run` and bake-off consume HTTPS URLs from `Settings.huggingface_model_endpoints`, but nothing in-repo creates, resumes, pauses, or deletes Hugging Face Inference Endpoints. Operators must provision endpoints manually (see runbook), which blocks a reliable Phase 10 workflow and trustworthy live Phase 5 bake-offs.

## Goals

1. Catalog-driven lifecycle for Inference Endpoints keyed by `runner_id` (olmocr + kraken first).
2. Explicit CLI: `endpoints up` / `down` / `status`.
3. Optional `--ensure-endpoints` on `run` and `bakeoff` so a single command can bring up what it needs.
4. Cost control: **pause by default**; **delete only on explicit flag**.
5. Idle control: configure HF **scale-to-zero** when creating/updating, **and** a local idle ledger + watchdog that pauses (never auto-deletes) after idle.
6. Pin Hub repository + immutable revision (no `main` / floating tags as identity).
7. Keep secrets in `Settings.huggingface_api_key` only; never embed tokens in catalogs, ledgers, or git.

## Non-goals

- Local GPU inference or downloading full model weights to the laptop.
- Claiming Spec 0004 Phase 10 COMPLETE (quotas dashboards, cost accounting, corpus regression gates, operator calibration monitoring remain deferred).
- FakePassRunner / fake endpoints as Phase 10 exit evidence.
- Replacing runners’ invoke path; runners continue to POST to HTTPS endpoint URLs.
- Terraform / external IaC as the daily operator loop (escape-hatch docs may still mention `hf endpoints` CLI).

## Decisions (locked in brainstorming)

| Topic | Choice |
| --- | --- |
| When endpoints come up/down | Both: explicit CLI **and** optional `--ensure-endpoints` on `run` / `bakeoff` |
| Spin-down default | Pause; delete only with explicit flag |
| Idle enforcement | Both: HF scale-to-zero **and** local idle timer / explicit `down` |
| Scope | Catalog-driven from the start; olmocr + kraken as first entries |
| Implementation shape | Service + models in wordwending over `huggingface_hub` (not shell wrappers) |

## Architecture

```text
CLI (endpoints up|down|status, run/bakeoff --ensure-endpoints)
        │
        ▼
EndpointLifecycleService
        │
        ├── EndpointCatalog (runner_id → pin + hardware + scale policy)
        ├── HfEndpointClient (huggingface_hub Inference Endpoints API)
        ├── EndpointSessionLedger (last-used, names, URLs; no secrets)
        └── Settings (huggingface_api_key; in-process URL overlay for runners)
                │
                ▼
        PassRunner invoke (existing olmocr / kraken runners)
```

### Layering (AGENTS.md)

| Concern | Location |
| --- | --- |
| Catalog / ledger / request-result models | `wordwending.models` |
| Lifecycle orchestration | `wordwending.services` (`EndpointLifecycleService` + thin HF client collaborator) |
| Click commands / flags | `wordwending.cli` only (thin) |
| API token + any user-provided endpoint URL map | `wordwending.settings.Settings` |

## Catalog

Per `runner_id` entry (defaults ship for `olmocr` and `kraken`; overridable via settings/TOML as needed):

- `runner_id` (stable; matches `PassRunnerRegistry`)
- Hub `repository` (e.g. `owner/model`)
- Immutable `revision` (commit hash)
- Endpoint `name` and HF `namespace`
- Hardware / deploy fields required by HF create API (accelerator, vendor, region, instance type/size, framework, task, type)
- Scale policy: enable scale-to-zero; optional HF idle seconds / replica bounds when supported

Reject catalog entries whose `revision` is a mutable label (`main`, `master`, `latest`, `head`) — same spirit as runner reproducibility elsewhere in the project.

## Service API (contract)

`EndpointLifecycleService`:

- `ensure_up(runner_ids: Sequence[str]) -> EndpointEnsureResult`  
  Create if missing; resume if paused or scaled-to-zero; wait until ready (with timeout); update session ledger; return HTTPS URLs keyed by `runner_id`.
- `down(runner_ids: Sequence[str], *, delete: bool = False) -> EndpointDownResult`  
  Default pause; if `delete=True`, destroy endpoint. Clear or mark ledger entries accordingly.
- `status(runner_ids: Sequence[str] | None = None) -> EndpointStatusReport`  
  Report HF status + ledger last-used for catalogued (or selected) runners.
- Idle watchdog helper (invoked by CLI or a small internal check): if last-used older than configured idle minutes, **pause** (never delete).

Collaborator `HfEndpointClient` wraps `huggingface_hub` (`create_inference_endpoint`, pause/resume/scale_to_zero/delete, wait/describe). Unit tests mock this collaborator; no live HF in default pytest.

## Session ledger

Persist under a local ops path (not inside document bundles), e.g. configurable directory under the user’s wordwending data/config area:

- endpoint name, namespace, runner_id
- last known URL (HTTPS)
- last-used UTC timestamp
- last desired action (up/down/pause)

No API tokens in the ledger. Safe to wipe; `ensure_up` rediscovers/recreates from catalog + HF API.

## CLI

- `wordwending endpoints up [--runner ID]...` — ensure listed runners (default: all catalogued)
- `wordwending endpoints down [--runner ID]... [--delete]` — pause default; delete if flagged
- `wordwending endpoints status [--runner ID]...`
- `wordwending run ... --ensure-endpoints` — ensure runners needed for this run, overlay URLs for the process, touch ledger
- `wordwending bakeoff ... --ensure-endpoints` — same for bake-off candidates

Idle timeout and scale-to-zero knobs live in Settings (pydantic-settings), not ad-hoc env reads in services.

## Runner URL wiring

After `ensure_up`, apply an **in-process overlay** of `huggingface_model_endpoints` (and/or a session file that Settings can load for the operator machine). Do not commit live endpoint URLs into the git repo. Existing runners keep resolving URLs from Settings as today.

## Error handling

- Missing/invalid token → `ConfigurationError`
- Endpoint create/wait failure → typed ops error (new or existing wordwending exception); do not pretend invoke succeeded
- Unknown `runner_id` → clear error listing catalogued ids
- Partial multi-runner `ensure_up` failure → report which succeeded/failed; do not silently continue as if all were ready unless explicitly documented (prefer fail-closed for `--ensure-endpoints`)

## Testing

- Unit: mock `HfEndpointClient` — create, resume, pause, delete, scale-to-zero config recorded, ledger idle pause, ensure overlays URLs
- CLI: up/down/status smoke with doubles; `--ensure-endpoints` wiring
- Integration (`pytest.mark.integration`): optional live create/pause/delete against a cheap/dev endpoint when credentials present — skipped by default

## Docs / honesty

Update HF setup runbook: lifecycle CLI is the preferred path; Phase 10 still **NOT COMPLETE**; deferred list unchanged (quotas UX, cost controls beyond pause/scale-to-zero, corpus gates, calibration monitoring).

## Success criteria

1. Operator can `endpoints up` for olmocr + kraken from catalog pins and get ready HTTPS URLs without Hub UI.
2. `endpoints down` pauses; `down --delete` removes.
3. HF scale-to-zero configured on ensure; local idle path pauses after configured idle.
4. `run --ensure-endpoints` / `bakeoff --ensure-endpoints` bring up needed endpoints then invoke as today.
5. Default test suite never hits live HF; Phase 10 not marked COMPLETE.

## Open points for implementation plan (not blockers)

- Exact Settings field names for catalog overrides and idle minutes
- Whether session ledger path is under XDG config vs an explicit Settings path
- Wait/poll timeout defaults for cold start
- Whether bakeoff `--ensure-endpoints` should refuse Fake/plumbing candidates (yes — only catalogued real runners)
