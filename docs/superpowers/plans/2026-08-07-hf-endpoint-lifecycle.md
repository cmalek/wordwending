# HF Endpoint Lifecycle Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship catalog-driven Hugging Face Inference Endpoint lifecycle (`up` / pause-default `down` / `status`, optional `--ensure-endpoints` on `run`/`bakeoff`, HF scale-to-zero + local idle pause) so operators have a real hosted workflow before Phase 5 live bake-off — without marking Spec 0004 Phase 10 COMPLETE.

**Architecture:** Thin Click CLI delegates to `EndpointLifecycleService`, which orchestrates an `EndpointCatalog`, `HfEndpointClient` (`huggingface_hub`), and an on-disk `EndpointSessionLedger` (no secrets). After `ensure_up`, an in-process Settings URL overlay feeds existing olmocr/kraken runners. Docs stay honest: ops slice only; Phase 10 NOT COMPLETE.

**Tech Stack:** Python 3.13, Click, Pydantic 2, pydantic-settings, `huggingface_hub` (add via `uv add`), pytest, existing `wordwending.settings.Settings` / `wordwending.exc`.

**Spec:** `docs/superpowers/specs/2026-08-07-hf-endpoint-lifecycle-design.md`

## Subagent Model Policy (locked)

| Role | Model slug |
| --- | --- |
| Mechanical TDD (1–2 files, clear steps) | `composer-2.5-fast` |
| Multi-file integration / stuck | `cursor-grok-4.5-medium` |
| Spec/ADR-compliance reviewer | `cursor-grok-4.5-medium` |
| Code-quality reviewer | `composer-2.5-fast` |
| Wave / plan-exit audit | `cursor-grok-4.5-medium` |

**No other models.** Per task (serial Superpowers loop):

1. Implementer implements, runs listed checks, self-reviews, commits (product/docs/tests only; leave `graphify-out/` unstaged).
2. Spec/ADR reviewer (`cursor-grok-4.5-medium`) reviews without editing.
3. Same implementer fixes; re-review until approved.
4. Fresh code-quality reviewer (`composer-2.5-fast`) reviews without editing.
5. Same fix/re-review loop for quality findings.

After all tasks: fresh `cursor-grok-4.5-medium` plan-exit audit vs design spec + Phase 10 honesty.

Include in **every** subagent prompt:

- Workspace: `/Users/cmalek/src/workspace/wordwending`
- Before explore: `graphify query/path/explain`; `user-code-index` after `GetMcpTools` / `set_project_path`
- Python: `source .venv/bin/activate`; `/usr/bin/cd` only (never bare `cd`)
- After Python edits: `.venv/bin/ruff`, `.venv/bin/mypy` on touched files, `make napoleon-gate`, focused pytest
- After code edits: `graphify update .` (leave `graphify-out/` **unstaged**)
- Prefer 3rd-party via `context7` + `package-registry-mcp` before inventing
- Never mark Spec 0004 Phase 10 COMPLETE
- Never use FakePassRunner as ops exit evidence
- No local GPU / weight download
- Secrets only via `Settings.huggingface_api_key`

## Global Constraints

- AGENTS.md layering: models → services → thin CLI; settings only through `wordwending.settings.Settings`.
- Napoleon class/method docs + `#:` on attributes; methods ≤ 60 lines; no god classes.
- Mutable Hub revisions forbidden in catalog: reject `main` / `master` / `latest` / `head` (case-insensitive).
- Pause by default; delete only with explicit `delete=True` / `--delete`.
- Local idle watchdog **pauses** only — never auto-deletes.
- Default pytest suite must never call live HF; live smoke behind `@pytest.mark.integration` (already registered in `tests/conftest.py`).
- Documentation tasks are required (runbook, usage, FAQ, README honesty).

## File Map

| Path | Responsibility |
| --- | --- |
| `pyproject.toml` / `uv.lock` | Add `huggingface_hub` dependency |
| `wordwending/models/endpoint_lifecycle.py` | Catalog entry, ledger, ensure/down/status result models |
| `wordwending/models/__init__.py` | Re-export new models as needed |
| `wordwending/settings.py` | Idle minutes, wait timeout, ledger path, namespace, catalog overrides, URL overlay helper |
| `wordwending/exc.py` | `EndpointLifecycleError` (ops failures distinct from `RunnerEndpointUnavailable`) |
| `wordwending/services/hf_endpoint_client.py` | Thin wrapper around `huggingface_hub` Inference Endpoint APIs |
| `wordwending/services/endpoint_session_ledger.py` | Load/save session ledger JSON (no secrets) |
| `wordwending/services/endpoint_lifecycle.py` | `EndpointLifecycleService` orchestration |
| `wordwending/cli/endpoints.py` or commands in `wordwending/cli/cli.py` | Thin `endpoints` Click group |
| `wordwending/cli/cli.py` | Wire group; add `--ensure-endpoints` to `run` / `bakeoff` |
| `tests/test_endpoint_lifecycle.py` | Unit tests with fake client |
| `tests/test_cli_endpoints.py` or extend `tests/test_cli_commands.py` | CLI + ensure-endpoints wiring |
| `doc/source/runbook/huggingface_setup.rst` | Preferred lifecycle CLI path; Phase 10 NOT COMPLETE |
| `doc/source/overview/usage.rst` | Document `endpoints` + `--ensure-endpoints` |
| `doc/source/overview/faq.rst` | Ops honesty |
| `README.md` | Short pointer to endpoint lifecycle |
| `doc/source/architecture/spec_0004_v1_implementation_plan.rst` | Phase 10 status: still NOT COMPLETE; note lifecycle slice shipped |

## Locked Settings Names

```python
# On Settings (WORDWENDING_* env / TOML):
huggingface_endpoint_namespace: str | None = None
huggingface_endpoint_idle_minutes: int = 30
huggingface_endpoint_wait_timeout_seconds: int = 900
huggingface_endpoint_ledger_path: Path | None = None
# default when None: Path.home() / ".config" / "wordwending" / "endpoint-session-ledger.json"
huggingface_endpoint_catalog: list[EndpointCatalogEntry] = Field(default_factory=list)
# empty list → use built-in default_catalog() for olmocr + kraken
```

URL overlay for a process: mutate a copy of settings / pass updated `huggingface_model_endpoints` into runner construction (prefer explicit overlay dict returned by `ensure_up`, applied in CLI before building runners — do not write secrets or ephemeral URLs into git-tracked files).

## Built-in Catalog Policy

- Ship `default_endpoint_catalog()` returning entries for `runner_id` `olmocr` and `kraken`.
- **Hardware / Hub pins:** use clearly named fields; if production Hub commit is not yet chosen, put **operator-required** pins in Settings/TOML examples and ship **test catalog fixtures** with fake-but-immutable revisions (`deadbeef…` hex) for unit tests. Do **not** ship `revision="main"`.
- Document in runbook that operators must set real `repository` + `revision` + hardware before `endpoints up` against live HF.

---

### Task 1: Dependency + models + settings + exception

**Model:** `composer-2.5-fast`

**Files:**
- Modify: `pyproject.toml` (via `uv add huggingface_hub`)
- Create: `wordwending/models/endpoint_lifecycle.py`
- Modify: `wordwending/models/__init__.py`
- Modify: `wordwending/settings.py`
- Modify: `wordwending/exc.py`
- Test: `tests/test_endpoint_lifecycle_models.py`

**Interfaces:**
- Produces: `EndpointCatalogEntry`, `EndpointLedgerEntry`, `EndpointSessionLedger`, `EndpointEnsureResult`, `EndpointDownResult`, `EndpointStatusRow`, `EndpointStatusReport`, `default_endpoint_catalog()`, `EndpointLifecycleError`, Settings fields listed above, `mutable_revision_rejected(revision: str) -> bool`

- [ ] **Step 1: Add dependency**

```bash
source .venv/bin/activate
uv add huggingface_hub
```

- [ ] **Step 2: Write failing model/settings tests**

```python
# tests/test_endpoint_lifecycle_models.py
import pytest
from pydantic import ValidationError

from wordwending.models.endpoint_lifecycle import (
    EndpointCatalogEntry,
    default_endpoint_catalog,
    reject_mutable_revision,
)
from wordwending.settings import Settings


def test_default_catalog_includes_olmocr_and_kraken() -> None:
    ids = {entry.runner_id for entry in default_endpoint_catalog()}
    assert ids == {"olmocr", "kraken"}


def test_catalog_entry_rejects_mutable_revision() -> None:
    with pytest.raises(ValidationError):
        EndpointCatalogEntry(
            runner_id="olmocr",
            repository="org/model",
            revision="main",
            endpoint_name="ww-olmocr",
            namespace="ns",
            accelerator="gpu",
            vendor="aws",
            region="us-east-1",
            instance_type="nvidia-a10g",
            instance_size="x1",
            framework="pytorch",
            task="image-text-to-text",
            endpoint_type="protected",
            scale_to_zero=True,
        )


def test_settings_idle_and_ledger_defaults(tmp_path, monkeypatch) -> None:
    monkeypatch.delenv("WORDWENDING_HUGGINGFACE_ENDPOINT_IDLE_MINUTES", raising=False)
    settings = Settings()
    assert settings.huggingface_endpoint_idle_minutes == 30
    assert settings.huggingface_endpoint_wait_timeout_seconds == 900
```

Adjust `EndpointCatalogEntry` field names to match HF create API needs; keep them explicit.

- [ ] **Step 3: Run tests — expect FAIL (modules missing)**

```bash
.venv/bin/pytest tests/test_endpoint_lifecycle_models.py -q
```

- [ ] **Step 4: Implement models, Settings fields, `EndpointLifecycleError`**

Napoleon docs; `#:` on attributes; export from `models/__init__.py` as needed.

- [ ] **Step 5: Run tests — expect PASS; ruff/mypy/napoleon-gate**

```bash
.venv/bin/pytest tests/test_endpoint_lifecycle_models.py -q
.venv/bin/ruff check wordwending/models/endpoint_lifecycle.py wordwending/settings.py wordwending/exc.py tests/test_endpoint_lifecycle_models.py
.venv/bin/mypy wordwending/models/endpoint_lifecycle.py wordwending/settings.py wordwending/exc.py
make napoleon-gate
```

- [ ] **Step 6: Commit** (no `graphify-out/`)

```bash
git add pyproject.toml uv.lock wordwending/models/endpoint_lifecycle.py wordwending/models/__init__.py wordwending/settings.py wordwending/exc.py tests/test_endpoint_lifecycle_models.py
git commit -m "$(cat <<'EOF'
feat(endpoints): add catalog models and lifecycle settings

EOF
)"
```

---

### Task 2: `HfEndpointClient` + session ledger

**Model:** `composer-2.5-fast`

**Files:**
- Create: `wordwending/services/hf_endpoint_client.py`
- Create: `wordwending/services/endpoint_session_ledger.py`
- Test: `tests/test_hf_endpoint_client.py`, `tests/test_endpoint_session_ledger.py`

**Interfaces:**
- Consumes: `EndpointCatalogEntry`, Settings token
- Produces:
  - `HfEndpointClient` with methods:
    - `describe(name: str, *, namespace: str | None) -> EndpointRemoteState`
    - `create(entry: EndpointCatalogEntry) -> EndpointRemoteState`
    - `resume(name: str, *, namespace: str | None) -> EndpointRemoteState`
    - `pause(name: str, *, namespace: str | None) -> EndpointRemoteState`
    - `scale_to_zero(name: str, *, namespace: str | None) -> EndpointRemoteState`
    - `delete(name: str, *, namespace: str | None) -> None`
    - `wait_ready(name: str, *, namespace: str | None, timeout_seconds: int) -> EndpointRemoteState`
  - `EndpointRemoteState` (name, status, url: str | None) in models or client module models
  - `EndpointSessionLedgerStore.load/save/touch/mark_down` on path

- [ ] **Step 1: Failing tests for ledger round-trip and client method surface via Protocol/fake**

```python
def test_ledger_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "ledger.json"
    store = EndpointSessionLedgerStore(path)
    store.touch(
        runner_id="olmocr",
        endpoint_name="ww-olmocr",
        namespace="ns",
        url="https://example.huggingface.cloud",
        action="up",
    )
    loaded = store.load()
    assert loaded.entries["olmocr"].url.startswith("https://")
```

Client tests use a fake/recording double implementing the same methods; real `huggingface_hub` calls only inside `HfEndpointClient` implementation (integration later).

- [ ] **Step 2: Run — FAIL**

- [ ] **Step 3: Implement client + ledger** (methods ≤ 60 lines; inject token; map hub errors → `EndpointLifecycleError` / `ConfigurationError` for missing token)

- [ ] **Step 4: PASS + gates**

- [ ] **Step 5: Commit**

```bash
git commit -m "$(cat <<'EOF'
feat(endpoints): add HF client wrapper and session ledger

EOF
)"
```

---

### Task 3: `EndpointLifecycleService` (ensure / down / status / idle pause)

**Model:** `cursor-grok-4.5-medium`

**Files:**
- Create: `wordwending/services/endpoint_lifecycle.py`
- Test: `tests/test_endpoint_lifecycle.py`

**Interfaces:**
- Consumes: catalog, `HfEndpointClient`, ledger store, Settings timeouts/idle
- Produces:
  - `EndpointLifecycleService.ensure_up(runner_ids: Sequence[str]) -> EndpointEnsureResult`
  - `down(runner_ids: Sequence[str], *, delete: bool = False) -> EndpointDownResult`
  - `status(runner_ids: Sequence[str] | None = None) -> EndpointStatusReport`
  - `pause_idle(*, now: datetime | None = None) -> EndpointDownResult` — pause runners idle longer than `idle_minutes`; never delete
  - Fail-closed: unknown runner_id → error listing catalog ids; partial ensure failure → error naming failed ids (no silent success)

- [ ] **Step 1: Failing tests**

```python
def test_ensure_up_creates_missing_and_returns_https_url() -> None:
    client = FakeHfEndpointClient()
    service = EndpointLifecycleService(client=client, catalog=..., ledger=..., settings=...)
    result = service.ensure_up(["olmocr"])
    assert "olmocr" in result.urls
    assert str(result.urls["olmocr"]).startswith("https://")
    assert client.created == ["ww-olmocr"]  # or catalog endpoint_name


def test_down_pauses_by_default_delete_flag_destroys() -> None:
    ...


def test_pause_idle_pauses_only_stale_entries() -> None:
    ...


def test_ensure_up_unknown_runner_fails_closed() -> None:
    with pytest.raises(...):
        service.ensure_up(["nope"])
```

Cover: resume when paused/scaledToZero; scale_to_zero configured on create path when `entry.scale_to_zero`; wait_ready called; missing token → `ConfigurationError`.

- [ ] **Step 2: FAIL**

- [ ] **Step 3: Implement service** (constructor injection; no `os.environ`)

- [ ] **Step 4: PASS + gates + `graphify update .` (unstaged)**

- [ ] **Step 5: Commit**

```bash
git commit -m "$(cat <<'EOF'
feat(endpoints): add EndpointLifecycleService ensure/down/status

EOF
)"
```

---

### Task 4: CLI `endpoints` group + docs for commands

**Model:** `composer-2.5-fast`

**Files:**
- Create: `wordwending/cli/endpoints.py` (preferred) **or** add group in `cli.py` if small
- Modify: `wordwending/cli/cli.py` — register group
- Modify: `doc/source/overview/usage.rst` — document commands
- Test: `tests/test_cli_endpoints.py`

**Interfaces:**
- Consumes: `EndpointLifecycleService`
- Produces: Click group `endpoints` with `up`, `down`, `status`; `down --delete`; optional `--runner` multi-option; `up` may call `pause_idle` first or expose `endpoints idle-reap` — prefer calling `pause_idle` at start of `up`/`status` as safety net (document behavior)

- [ ] **Step 1: Failing CLI tests** (CliRunner + monkeypatched service / fake client)

```python
def test_endpoints_up_prints_urls(runner, monkeypatch) -> None:
    ...
    result = runner.invoke(cli, ["endpoints", "up", "--runner", "olmocr"])
    assert result.exit_code == 0
    assert "https://" in result.output
```

- [ ] **Step 2: FAIL**

- [ ] **Step 3: Implement thin CLI + usage.rst section**

- [ ] **Step 4: PASS + gates**

- [ ] **Step 5: Commit**

```bash
git commit -m "$(cat <<'EOF'
feat(cli): add endpoints up/down/status commands

EOF
)"
```

---

### Task 5: `--ensure-endpoints` on `run` and `bakeoff` + URL overlay

**Model:** `cursor-grok-4.5-medium`

**Files:**
- Modify: `wordwending/cli/cli.py` (`run_runner`, `bakeoff_matrix`)
- Test: extend `tests/test_cli_commands.py` / `tests/test_cli_endpoints.py`
- Helper: small function in `wordwending/services/endpoint_lifecycle.py` or `wordwending/cli/utils.py` — prefer service method `overlay_endpoints(settings, urls) -> Settings` or return dict applied when constructing runners

**Interfaces:**
- Consumes: `ensure_up`
- Produces: `--ensure-endpoints` flag; on success, runner construction sees HTTPS URLs for required `runner_id`s; fail-closed if ensure fails; bakeoff only ensures catalogued real candidates (olmocr/kraken), never Fake

- [ ] **Step 1: Failing tests**

```python
def test_run_ensure_endpoints_overlays_url_before_invoke(runner, monkeypatch) -> None:
    # mock ensure_up → urls; assert hosted runner constructed with overlay URL
    ...


def test_bakeoff_ensure_endpoints_fail_closed_on_lifecycle_error(runner, monkeypatch) -> None:
    ...
```

- [ ] **Step 2: FAIL**

- [ ] **Step 3: Implement flag + overlay wiring** (CLI stays thin; call service)

- [ ] **Step 4: PASS + gates**

- [ ] **Step 5: Commit**

```bash
git commit -m "$(cat <<'EOF'
feat(cli): add --ensure-endpoints to run and bakeoff

EOF
)"
```

---

### Task 6: Documentation honesty pass (required)

**Model:** `composer-2.5-fast`

**Files:**
- Modify: `doc/source/runbook/huggingface_setup.rst` — lifecycle CLI as preferred path; `hf endpoints` as escape hatch; keep Phase 10 NOT COMPLETE banner; document pause vs `--delete`, scale-to-zero + local idle, catalog pins, ledger path
- Modify: `doc/source/overview/usage.rst` — `endpoints` + `--ensure-endpoints` examples
- Modify: `doc/source/overview/faq.rst` — how to spin endpoints up/down; Phase 10 still NOT COMPLETE
- Modify: `README.md` — short ops pointer
- Modify: `doc/source/architecture/spec_0004_v1_implementation_plan.rst` — Phase 10 Status remains NOT COMPLETE; note lifecycle slice shipped under deferred exit
- Modify: `doc/source/runbook/from_source_to_markdown.rst` — Phase 10 ops skeleton list includes endpoint lifecycle CLI (still NOT COMPLETE)

- [ ] **Step 1: Update docs** (no COMPLETE claims for Phase 5/10)

- [ ] **Step 2: Grep honesty**

```bash
rg -n "Phase 10" README.md doc/source/runbook doc/source/overview doc/source/architecture/spec_0004_v1_implementation_plan.rst
# Expect NOT COMPLETE / ops skeleton language; no Phase 10 COMPLETE
```

- [ ] **Step 3: Commit**

```bash
git commit -m "$(cat <<'EOF'
docs: document HF endpoint lifecycle CLI as Phase 10 ops slice

EOF
)"
```

---

### Task 7: Integration stub + plan-exit audit prep

**Model:** `composer-2.5-fast` (stub) then audit by `cursor-grok-4.5-medium` (dispatch separately)

**Files:**
- Modify: `tests/test_endpoint_lifecycle.py` or `tests/test_endpoint_lifecycle_integration.py`

- [ ] **Step 1: Add skipped integration test**

```python
@pytest.mark.integration
def test_live_endpoint_lifecycle_smoke() -> None:
    pytest.skip("Live HF Inference Endpoint create/pause/delete — enable with credentials")
```

- [ ] **Step 2: Commit**

```bash
git commit -m "$(cat <<'EOF'
test(endpoints): add skipped live HF lifecycle integration stub

EOF
)"
```

- [ ] **Step 3: Plan-exit audit** (dispatcher runs `cursor-grok-4.5-medium` reviewer — no edits)

Checklist for auditor:

1. Spec goals 1–7 covered  
2. Pause default / delete flag  
3. Scale-to-zero + local idle pause (no auto-delete)  
4. Catalog olmocr+kraken; mutable revision rejected  
5. CLI + `--ensure-endpoints`  
6. Docs updated; Phase 10 NOT COMPLETE  
7. No live HF in default suite  
8. `graphify-out` not in commits  

Write: `.superpowers/sdd/task-endpoint-lifecycle-audit.md`

---

## Spec Coverage (self-check)

| Spec requirement | Task |
| --- | --- |
| Catalog-driven olmocr+kraken | 1, 3 |
| CLI up/down/status | 4 |
| `--ensure-endpoints` on run/bakeoff | 5 |
| Pause default / delete flag | 3, 4 |
| HF scale-to-zero + local idle | 2, 3 |
| Pin revision / reject mutable | 1 |
| Secrets via Settings only | 1–5 |
| Docs / Phase 10 NOT COMPLETE | 6 |
| Unit mocks; integration skip | 2, 3, 7 |
| `huggingface_hub` client | 1–2 |

## Execution Handoff

Plan saved to `docs/superpowers/plans/2026-08-07-hf-endpoint-lifecycle.md`.

**Recommended:** Subagent-Driven Development with models **only** `composer-2.5-fast` and `cursor-grok-4.5-medium` as in the policy table above.

**Two execution options:**

1. **Subagent-Driven (recommended)** — fresh subagent per task + spec review + quality review  
2. **Inline Execution** — this session with executing-plans checkpoints  

Which approach?
