# Spec 0013 Pass-Runner Interface Schema Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Freeze the persisted pass-runner capability and batch-execution schema exactly as Spec 0013 requires, with invariant tests and golden fixtures, without extracting a speculative plugin framework.

**Architecture:** Keep the six Spec 0013 models in `bochord.models.ocr`. Close the one missing reproducibility gap (reject mutable revisions such as `main`). Add focused invariant tests plus golden JSON fixtures. Do not invent a runtime `Protocol` or plugin registry; ADR 0007 / Spec 0013 require two or three real adapters first (only olmOCR exists today).

**Tech Stack:** Python 3.13, Pydantic 2, pytest, stdlib `json`/`datetime`.

**Sequence:** 1 of 5 in this series. Finish before Spec 0008.

**Governing ADR:** ADR 0006 (pass-runner interfaces). Extraction timing bound by ADR 0007.

## Global Constraints

- Canonical models stay in `bochord.models.ocr`: `RunnerReference`, `RunnerCapability`, `PreparedArtifactRef`, `BatchItemRef`, `RunnerOutputArtifact`, `RunnerExecutionBatch`.
- Do not move these models into a new module in this plan.
- Do not add a generic runner protocol, registry, or plugin loader.
- Persist runner-specific raw artifacts as-is; do not flatten capabilities to invent a common runtime shape.
- Spec 0012 extras already on `RunnerExecutionBatch` (`execution_policy_id`, `warmup`, `request_ids`) may remain; they do not contradict Spec 0013.
- Follow Napoleon docstrings and `#:` attribute comments on all non-test Python.
- Before Python commands: `source .venv/bin/activate`.
- After Python edits: touched-file `ruff`, touched-file `mypy`, `make napoleon-gate`, then focused pytest.

## Subagent Model Policy

- Implementation tasks may use only **Cursor Grok 4.5** (`cursor-grok-4.5`) or **Composer 2.5 Fast** (`composer-2.5-fast`). No other implementer models.
- Prefer Composer 2.5 Fast for mechanical TDD; use Cursor Grok 4.5 when stuck or judgment is required.
- Review steps (spec compliance, code quality, final whole-plan) may use any appropriate model.
- Give each implementer only the generated task brief, prior-task interface decisions, and listed files.

For every task, use this serial Superpowers loop:

1. Implementer (Composer 2.5 Fast or Cursor Grok 4.5) implements, runs listed checks, self-reviews, and commits.
2. Spec-compliance reviewer (any appropriate model) reviews without editing.
3. Same implementer fixes; re-review until approved.
4. Fresh code-quality reviewer (any appropriate model) reviews without editing.
5. Same fix/re-review loop for quality findings.

After the last task, a fresh reviewer audits the whole plan.
Do not start the next task or plan while either review has open findings.

## Existing Baseline

- Spec 0012 already implemented the six Spec 0013 models plus validators for preferred-input membership, batch size/uniqueness, failure-id/status rules, finish-before-start, output-item association, and model-backed HF reproducibility fields.
- Concrete hosted olmOCR runner exists; no second adapter yet.
- Missing vs Spec 0013: explicit rejection of mutable revisions such as `main`; dedicated golden fixtures that freeze the Spec 0013 JSON shape.

---

## File Map

- Modify: `bochord/models/ocr.py` — reject mutable model revisions on `RunnerReference`.
- Modify: `tests/test_ocr_models.py` — Spec 0013 invariant matrix.
- Create: `tests/fixtures/runner/capability-v1.json` — frozen `RunnerCapability`.
- Create: `tests/fixtures/runner/execution-batch-succeeded-v1.json` — frozen succeeded batch.
- Create: `tests/fixtures/runner/execution-batch-partial-v1.json` — frozen partial batch.
- Create: `tests/fixtures/runner/execution-batch-failed-v1.json` — frozen failed batch.
- Modify: `tests/test_olmocr_runner.py` only if a fixture helper needs the mutable-revision rejection (prefer not).

### Task 1: Reject Mutable Model Revisions

**Files:**

- Modify: `bochord/models/ocr.py`
- Modify: `tests/test_ocr_models.py`

**Interfaces:**

Extend `RunnerReference.validate_model_reproducibility` so that when `model_name` is set, `model_revision` is not a mutable label:

```python
_MUTABLE_MODEL_REVISIONS = frozenset({"main", "master", "latest", "HEAD"})
```

Reject case-insensitively after strip. Keep existing required-field and `huggingface*` runtime checks.

- [x] **Step 1: Write failing tests**

```python
def test_runner_reference_rejects_mutable_model_revision() -> None:
    with pytest.raises(ValidationError, match="mutable"):
        RunnerReference(
            runner_id="olmocr",
            model_name="allenai/olmOCR-7B",
            model_revision="main",
            hardware_class="nvidia-l40s",
            runtime_name="huggingface-endpoint",
            runtime_revision="ep-rev-1",
            config_digest="cfg",
            prompt_digest="prompt",
        )


def test_runner_reference_accepts_immutable_digest_revision() -> None:
    ref = RunnerReference(
        runner_id="olmocr",
        model_name="allenai/olmOCR-7B",
        model_revision="abcdef0123456789",
        hardware_class="nvidia-l40s",
        runtime_name="huggingface-endpoint",
        runtime_revision="ep-rev-1",
        config_digest="cfg",
        prompt_digest="prompt",
    )
    assert ref.model_revision == "abcdef0123456789"
```

- [x] **Step 2: Run tests to verify they fail**

```bash
source .venv/bin/activate
pytest tests/test_ocr_models.py::test_runner_reference_rejects_mutable_model_revision \
  tests/test_ocr_models.py::test_runner_reference_accepts_immutable_digest_revision -v
```

Expected: FAIL because mutable revisions are still accepted.

- [x] **Step 3: Implement minimal rejection**

Inside `validate_model_reproducibility`, after required-field checks:

```python
if self.model_name is not None and self.model_revision is not None:
    revision = self.model_revision.strip()
    if revision.casefold() in {item.casefold() for item in _MUTABLE_MODEL_REVISIONS}:
        msg = "mutable model revisions such as main are not reproducible"
        raise ValueError(msg)
```

Module-level `#:` frozenset constant near other model constants.

- [x] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_ocr_models.py::test_runner_reference_rejects_mutable_model_revision \
  tests/test_ocr_models.py::test_runner_reference_accepts_immutable_digest_revision -v
```

Expected: PASS.

- [x] **Step 5: Quality gate + commit**

```bash
ruff check bochord/models/ocr.py tests/test_ocr_models.py
mypy bochord/models/ocr.py
make napoleon-gate
pytest tests/test_ocr_models.py -q
git add bochord/models/ocr.py tests/test_ocr_models.py
git commit -m "$(cat <<'EOF'
fix: reject mutable runner model revisions

EOF
)"
```

### Task 2: Freeze Spec 0013 Invariants and Golden Fixtures

**Files:**

- Create: `tests/fixtures/runner/capability-v1.json`
- Create: `tests/fixtures/runner/execution-batch-succeeded-v1.json`
- Create: `tests/fixtures/runner/execution-batch-partial-v1.json`
- Create: `tests/fixtures/runner/execution-batch-failed-v1.json`
- Modify: `tests/test_ocr_models.py`

**Interfaces:**

Golden fixtures must round-trip through the six Spec 0013 models. Tests must assert every Spec 0013 invariant:

| Invariant | Assertion |
|-----------|-----------|
| preferred in accepted | empty accepted / preferred-outside-accepted raise |
| batch_size == unique ordered items | mismatch and duplicate ids raise |
| succeeded has no failures | failures with SUCCEEDED raise |
| partial has some but not all | empty or all failures with PARTIAL raise |
| failed names all ids | incomplete FAILED raise |
| finish ≥ start | earlier finish raises |
| outputs name submitted items | unknown output item ids raise |
| model-backed revision fields | missing digest/runtime fields raise |
| mutable revision | covered in Task 1 |

Do not assert absence of Spec 0012 extras. Batch fixtures **must** include Spec 0012 fields still required by the live model: at least `execution_policy_id`. Prefer explicit `warmup` / `request_ids` in fixtures even when defaults would apply, so the frozen JSON shape is obvious to implementers.

Fixture `capability-v1.json` example:

```json
{
  "accepted_input_kinds": ["image", "pdf"],
  "preferred_input_kind": "pdf",
  "supports_multi_item_batching": true,
  "batch_unit_kind": "prepared-unit",
  "packaging_strategy": "unit-to-pdf-batch"
}
```

Each batch fixture includes required Spec 0013 fields, Spec 0012 `execution_policy_id` (plus `warmup` / `request_ids`), and a valid `RunnerReference` with immutable revision.

- [x] **Step 1: Write failing round-trip and invariant tests**

```python
def test_spec_0013_capability_fixture_round_trips() -> None:
    payload = json.loads(FIXTURES.joinpath("capability-v1.json").read_text())
    capability = RunnerCapability.model_validate(payload)
    assert capability.model_dump(mode="json") == payload


def test_spec_0013_batch_fixtures_round_trip_by_status() -> None:
    for name in (
        "execution-batch-succeeded-v1.json",
        "execution-batch-partial-v1.json",
        "execution-batch-failed-v1.json",
    ):
        payload = json.loads(FIXTURES.joinpath(name).read_text())
        batch = RunnerExecutionBatch.model_validate(payload)
        assert batch.model_dump(mode="json") == payload
        assert batch.batch_size == len(batch.items)
```

Add one parametrized negative test covering the invariant table rows not already covered by existing tests. Reuse helpers from `tests/test_ocr_models.py` where present; do not duplicate identical assertions.

- [x] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_ocr_models.py -k spec_0013 -v
```

Expected: FAIL on missing fixtures / missing tests.

- [x] **Step 3: Add fixtures (and finish any remaining negative cases)**

Write the four JSON fixtures. Keep timestamps UTC ISO-8601. Keep paths relative. No secrets.

- [x] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_ocr_models.py -k "spec_0013 or runner_reference or RunnerCapability or RunnerExecutionBatch" -q
```

Expected: PASS.

- [x] **Step 5: Quality gate + commit**

```bash
ruff check tests/test_ocr_models.py
make napoleon-gate
pytest tests/test_ocr_models.py -q
git add tests/fixtures/runner tests/test_ocr_models.py
git commit -m "$(cat <<'EOF'
test: freeze Spec 0013 runner schema fixtures

EOF
)"
```

## Final Review Focus

Whole-plan reviewer must verify:

- all Spec 0013 required fields and invariants are tested;
- mutable revisions rejected;
- no `Protocol`/plugin registry/`typing.Protocol` runner abstraction introduced;
- models remain in `bochord.models.ocr`;
- ADR 0006 contract preserved: runners emit raw witnesses, never write the page graph.

## Cost Stop

Stop after schema freeze + invariant fixtures. No second adapter, no common runtime protocol, no normalization, no merge, no bundle writer.
