# Spec 0012 Runner Execution and Batching Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Execute prepared pages/units through one pinned Hugging Face-hosted olmOCR path with explicit fixed batching, preserved inputs/raw responses, retries, and batch provenance.

**Architecture:** Add strict execution-policy models, one stateless batch planner, one Pillow packager, and one concrete hosted olmOCR runner. A per-run orchestrator persists every batch before moving on; no speculative multi-runner plugin interface is extracted.

**Tech Stack:** Python 3.13, Pydantic 2, Pillow 12, `olmocr==0.4.27`, `httpx>=0.28.1`, stdlib hashing/time/JSON, Click, pytest.

**Sequence:** 4 of 4. Start only after the Spec 0010 plan passes final review.

## Global Constraints

- Runner policy is explicit, versioned, and persisted.
- V1 batching is fixed-size only; batch size `1` means no batching.
- Preserve page-local grouping when possible.
- Every batch item maps back to exact source page, prepared unit, and artifact.
- Preserve packaged inputs when packaging strategy is not `direct`.
- Persist raw endpoint responses before normalization.
- Record model repository/revision, endpoint/runtime/container revision, hardware class, config digest, and prompt digest.
- Model inference runs only on Hugging Face hosted endpoints.
- Never download weights or fall back to local inference.
- Endpoint failure persists failed/retryable batch; never silently changes model.
- Hugging Face credentials and per-model endpoint URLs resolve through `bochord.settings.Settings`; secrets never enter config digests, logs, command arguments, or bundle provenance.
- Health readiness is operational only; it is not OCR quality evidence.
- Warm-up batches are marked and excluded from measured throughput.
- Batch experiments reuse same prepared ids and immutable model revision.
- Requires Spec 0007 completion plan before Task 2.
- Follow repository Napoleon docstrings and `#:` attribute comments on all non-test Python.
- Before Python commands: `source .venv/bin/activate`.
- After Python edits: touched-file `ruff`, touched-file `mypy`, `make napoleon-gate`, then focused/full pytest.

## Subagent Model Policy

- Dispatch each implementer with **Composer 2.5 fast**.
- Dispatch every task reviewer and final whole-plan reviewer with **Cursor Grok 4.5**.
- Fix rounds 1-3 resume Composer 2.5 fast; rounds 4-5 use fresh Cursor Grok 4.5 implementer.
- Use no other model.
- Give each implementer only generated task brief, prior-task interface decisions, and listed files.

For every task, use this serial Superpowers loop:

1. Composer 2.5 fast implements, runs the listed checks, self-reviews, and commits.
2. Cursor Grok 4.5 reviews spec compliance without editing.
3. Composer fixes rounds 1-3; if still failing, fresh Grok implementers handle
   rounds 4-5. The same Grok reviewer rechecks each round.
4. A fresh Cursor Grok 4.5 reviewer checks code quality without editing.
5. Apply the same fix-round policy to quality findings; that reviewer rechecks.

After the last task, a fresh Cursor Grok 4.5 reviewer audits the whole plan.
Do not start the next task or plan while either review has open findings.

## Dependency Decision

Use pinned `olmocr==0.4.27` only for its maintained v4 prompt builder; do not
copy its prompt text or invoke its local pipeline. Release is current,
Apache-2.0, Python 3.13-compatible by metadata, actively maintained, and has
remote OpenAI-compatible server support. Pinning is required because prompt
builder is not yet a stable public API.

Use direct `httpx>=0.28.1` for timeout, headers, status, and raw-response control.
Do not use `huggingface_hub.InferenceClient.image_to_text`: its public method is
single-image/task-shaped and does not express olmOCR PDF page queries or exact
raw-response retention.

Do not add a generic runner protocol in this plan. ADR 0007 requires two or
three working adapters before extracting that boundary.

## Existing Baseline

- Canonical `RunnerReference`, `RunnerCapability`, `BatchItemRef`,
  `RunnerOutputArtifact`, and `RunnerExecutionBatch` already exist and validate
  counts, item ids, status, timestamps, output associations, and hosted runtime
  identity.
- No execution-policy model, batch planner, packager, hosted runner, run
  orchestrator, or `bochord run` command exists.

---

## File Map

- Create: `bochord/models/runner_execution.py` — policy, plans, packaged inputs, invocation/throughput results.
- Modify: `bochord/models/ocr.py` — missing batch provenance fields.
- Modify: `bochord/models/__init__.py` — export execution contracts.
- Modify: `bochord/settings.py` — Hugging Face API key plus per-model hosted endpoint settings.
- Modify: `pyproject.toml`, `uv.lock` — pinned olmOCR and direct httpx dependency.
- Create: `bochord/services/runner_batching.py` — fixed batch planning only.
- Create: `bochord/services/runner_packaging.py` — direct/PDF input preservation only.
- Create: `bochord/services/olmocr_runner.py` — concrete Hugging Face-hosted olmOCR calls only.
- Create: `bochord/services/runner_execution.py` — per-run orchestration and batch-record persistence.
- Modify: `bochord/cli/cli.py` — thin `run` command.
- Create: `tests/test_runner_batching.py`
- Create: `tests/test_runner_packaging.py`
- Create: `tests/test_olmocr_runner.py`
- Create: `tests/test_runner_execution.py`
- Modify: `tests/test_ocr_models.py`
- Modify: `tests/test_configuration.py`
- Modify: `tests/test_cli_commands.py`
- Create: `tests/fixtures/runner/olmocr-policy-v1.json`
- Create: `tests/fixtures/runner/prepared-inputs.json`

### Task 1: Freeze Execution Policy and Missing Provenance

**Files:**

- Create: `bochord/models/runner_execution.py`
- Modify: `bochord/models/ocr.py`
- Modify: `bochord/models/__init__.py`
- Modify: `bochord/settings.py`
- Modify: `tests/test_ocr_models.py`
- Modify: `tests/test_configuration.py`
- Create: `tests/fixtures/runner/olmocr-policy-v1.json`
- Modify: `pyproject.toml`
- Modify: `uv.lock`

**Interfaces:**

```python
class RetryMode(StrEnum):
    NONE = "none"
    WHOLE_BATCH = "whole-batch"
    FAILED_ITEMS = "failed-items"


class Settings(BaseSettings):
    huggingface_api_key: str | None = None
    huggingface_model_endpoints: dict[str, AnyHttpUrl] = Field(
        default_factory=dict
    )


class HostedEndpointPolicy(SchemaModel):
    endpoint_name: str
    endpoint_key: str
    hardware_class: str
    cold_start_timeout_seconds: float = Field(gt=0)
    request_timeout_seconds: float = Field(gt=0)
    retryable_status_codes: list[int]
    scale_to_zero: bool
    max_items_per_run: int = Field(gt=0)
    estimated_cost_per_item_usd: Decimal = Field(ge=0)
    max_run_cost_usd: Decimal = Field(ge=0)
    artifact_retention_days: int = Field(gt=0)


class RunnerExecutionPolicy(SchemaModel):
    policy_id: str
    version: str
    batch_size: int = Field(gt=0)
    target_longest_image_dim: int = Field(gt=0)
    preserve_page_local_groups: bool = True
    packaging_strategy: PackagingStrategy
    warmup_batch_count: int = Field(default=0, ge=0)
    retry_mode: RetryMode = RetryMode.FAILED_ITEMS
    max_retries: int = Field(default=1, ge=0)
    endpoint: HostedEndpointPolicy


class PlannedRunnerBatch(SchemaModel):
    batch_id: str
    items: list[BatchItemRef] = Field(min_length=1)
    artifacts: list[PreparedArtifactRef] = Field(min_length=1)
    warmup: bool = False


class PackagedRunnerInput(SchemaModel):
    artifact_id: str
    artifact_path: str
    checksum: str
    kind: InputKind
    batch_item_ids: list[str] = Field(min_length=1)
    page_numbers: list[int] = Field(min_length=1)


class HostedInvocationResult(SchemaModel):
    failure_item_ids: list[str]
    output_artifacts: list[RunnerOutputArtifact]
    request_ids: list[str]
    warnings: list[str]


class RunnerThroughputSummary(SchemaModel):
    measured_item_count: int = Field(ge=0)
    failed_item_count: int = Field(ge=0)
    measured_duration_seconds: float = Field(ge=0)
    items_per_second: float = Field(ge=0)
```

`RunnerReference` gains:

```python
hardware_class: str | None = None
```

Require it when `model_name` is set.

`RunnerExecutionBatch` gains:

```python
execution_policy_id: str
warmup: bool = False
request_ids: list[str] = Field(default_factory=list)
```

- [ ] **Step 1: Write failing strict contract tests**

```python
def test_model_backed_runner_requires_hardware_class() -> None:
    payload = model_runner_payload(hardware_class=None)
    with pytest.raises(ValidationError):
        RunnerReference.model_validate(payload)


def test_endpoint_policy_rejects_estimate_above_run_cap() -> None:
    policy = runner_policy_payload(
        max_items_per_run=10,
        estimated_cost_per_item_usd="0.20",
        max_run_cost_usd="1.00",
    )
    with pytest.raises(ValidationError):
        RunnerExecutionPolicy.model_validate(policy)


def test_settings_accept_huggingface_api_key_and_endpoint_map() -> None:
    settings = Settings(
        huggingface_api_key="hf_test_token",
        huggingface_model_endpoints={
            "olmocr-production":
                "https://example.endpoints.huggingface.cloud/v1",
        },
    )
    assert settings.huggingface_api_key == "hf_test_token"
    assert str(
        settings.huggingface_model_endpoints["olmocr-production"]
    ) == "https://example.endpoints.huggingface.cloud/v1"
```

`RunnerExecutionPolicy` validator rejects
`max_items_per_run * estimated_cost_per_item_usd > max_run_cost_usd`.
`PackagedRunnerInput` validator requires equal lengths for item ids/page numbers.

- [ ] **Step 2: Run model tests and verify missing imports**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_ocr_models.py -k "runner or endpoint or packaged"
```

- [ ] **Step 3: Add dependencies**

```bash
source .venv/bin/activate
rtk uv add "olmocr==0.4.27" "httpx>=0.28.1"
```

Do not install olmOCR GPU extras.

- [ ] **Step 4: Implement bare models and validators**

Keep behavior out of models. `Settings` owns the Hugging Face token and endpoint
map; execution policy stores only `endpoint_key`, never a secret. Endpoint URLs
must use `https`. Retryable defaults in fixture:

```json
[408, 429, 502, 503, 504]
```

Fixture values:

```json
{
  "policy_id": "olmocr-hf-fixed-v1",
  "version": "1",
  "batch_size": 4,
  "target_longest_image_dim": 1024,
  "preserve_page_local_groups": true,
  "packaging_strategy": "unit-to-pdf-batch",
  "warmup_batch_count": 1,
  "retry_mode": "failed-items",
  "max_retries": 1,
  "endpoint": {
    "endpoint_name": "olmocr-production",
    "endpoint_key": "olmocr-production",
    "hardware_class": "nvidia-l40s",
    "cold_start_timeout_seconds": 600,
    "request_timeout_seconds": 180,
    "retryable_status_codes": [408, 429, 502, 503, 504],
    "scale_to_zero": true,
    "max_items_per_run": 100,
    "estimated_cost_per_item_usd": "0.01",
    "max_run_cost_usd": "1.00",
    "artifact_retention_days": 30
  }
}
```

- [ ] **Step 5: Run model tests and commit**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_ocr_models.py
rtk git add bochord/models/runner_execution.py bochord/models/ocr.py \
  bochord/models/__init__.py tests/test_ocr_models.py \
  tests/fixtures/runner/olmocr-policy-v1.json pyproject.toml uv.lock
rtk git commit -m "feat: define runner execution policy"
```

### Task 2: Plan Fixed Batches and Preserve Packaged Inputs

**Files:**

- Create: `bochord/services/runner_batching.py`
- Create: `bochord/services/runner_packaging.py`
- Create: `tests/test_runner_batching.py`
- Create: `tests/test_runner_packaging.py`
- Create: `tests/fixtures/runner/prepared-inputs.json`

**Interfaces:**

```python
class RunnerBatchPlanner:
    def plan(
        self,
        artifacts: list[PreparedArtifactRef],
        capability: RunnerCapability,
        policy: RunnerExecutionPolicy,
    ) -> list[PlannedRunnerBatch]: ...


class RunnerInputPackager:
    def package(
        self,
        batch: PlannedRunnerBatch,
        strategy: PackagingStrategy,
        bundle_root: Path,
        output_dir: Path,
    ) -> PackagedRunnerInput: ...
```

Batch item ids:

```text
<batch-id>-item-001
<batch-id>-item-002
```

Batch id is SHA-256 over ordered artifact ids, policy id, and batch ordinal:

```text
batch-<64 lowercase hex>
```

- [ ] **Step 1: Write failing planning tests**

```python
def test_non_batching_runner_gets_one_item_batches() -> None:
    capability = capability(supports_multi_item_batching=False)
    batches = RunnerBatchPlanner().plan(artifacts(3), capability, policy(4))
    assert [len(batch.items) for batch in batches] == [1, 1, 1]


def test_page_local_policy_does_not_mix_units_until_needed() -> None:
    batches = RunnerBatchPlanner().plan(
        units(page_counts={"page-1": 3, "page-2": 3}),
        capability(),
        policy(batch_size=4, preserve_page_local_groups=True),
    )
    assert [[item.source_page_id for item in batch.items] for batch in batches] == [
        ["page-1", "page-1", "page-1"],
        ["page-2", "page-2", "page-2"],
    ]
```

Also test input-kind rejection, stable ordering, warm-up batch marking, and cost
cap before any output write.

- [ ] **Step 2: Write failing packaging tests**

```python
def test_pdf_batch_preserves_item_page_mapping(tmp_path: Path) -> None:
    packaged = RunnerInputPackager().package(
        planned_batch(3),
        PackagingStrategy.UNIT_TO_PDF_BATCH,
        fixture_root(),
        tmp_path,
    )
    assert packaged.kind is InputKind.PDF
    assert packaged.page_numbers == [1, 2, 3]
    assert packaged.batch_item_ids == [
        item.item_id for item in planned_batch(3).items
    ]
    assert Path(tmp_path, packaged.artifact_path).exists()
    assert packaged.checksum
```

- [ ] **Step 3: Run tests and verify imports fail**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_runner_batching.py tests/test_runner_packaging.py
```

- [ ] **Step 4: Implement planner**

Rules:

1. validate each artifact kind is accepted;
2. preserve input order;
3. if runner cannot batch or packaging strategy is `direct`, chunk at one;
4. otherwise group by source page when page-local policy is true, then fixed-size
   chunk each group;
5. otherwise fixed-size chunk whole sequence;
6. mark first `warmup_batch_count` batches;
7. never adapt size based on runtime observation.

Use stdlib slicing; no queue framework.

- [ ] **Step 5: Implement direct and PDF packaging**

- `direct`: one-item batch only; reference original artifact bytes without copy.
- `image-to-pdf`: write ordered images into one PDF.
- `unit-to-pdf-batch`: same PDF operation, preserving unit/item mapping.

Use Pillow:

```python
images = [Image.open(path).convert("RGB") for path in paths]
try:
    images[0].save(
        destination,
        "PDF",
        save_all=True,
        append_images=images[1:],
        resolution=300.0,
    )
finally:
    for image in images:
        image.close()
```

Write under `runner-inputs/<batch-id>.pdf`; hash saved bytes. No temporary file
survives failed packaging.

- [ ] **Step 6: Run tests and commit**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_runner_batching.py tests/test_runner_packaging.py
rtk git add bochord/services/runner_batching.py \
  bochord/services/runner_packaging.py tests/test_runner_batching.py \
  tests/test_runner_packaging.py tests/fixtures/runner/prepared-inputs.json
rtk git commit -m "feat: plan and package runner batches"
```

### Task 3: Execute Concrete Hosted olmOCR Batches

**Files:**

- Create: `bochord/services/olmocr_runner.py`
- Create: `tests/test_olmocr_runner.py`

**Interfaces:**

```python
class HuggingFaceOlmocrRunner:
    def __init__(
        self,
        runner: RunnerReference,
        policy: RunnerExecutionPolicy,
        endpoint_url: str,
        token: str,
        client: httpx.Client,
    ) -> None: ...

    def health_check(self) -> None: ...

    def invoke(
        self,
        batch: PlannedRunnerBatch,
        packaged: PackagedRunnerInput,
        output_dir: Path,
    ) -> HostedInvocationResult: ...
```

Runner capability is fixed in module:

```python
OLMOCR_CAPABILITY = RunnerCapability(
    accepted_input_kinds=[
        InputKind.IMAGE,
        InputKind.PREPARED_UNIT,
        InputKind.PDF,
    ],
    preferred_input_kind=InputKind.PDF,
    supports_multi_item_batching=True,
    batch_unit_kind=BatchUnitKind.PREPARED_UNIT,
    packaging_strategy=PackagingStrategy.UNIT_TO_PDF_BATCH,
)
```

- [ ] **Step 1: Write mocked endpoint tests**

```python
def test_health_check_requires_models_readiness(tmp_path: Path) -> None:
    client = mock_client(get_status=503)
    with pytest.raises(RunnerEndpointUnavailable):
        hosted_runner(client).health_check()


def test_raw_response_is_saved_and_mapped_before_parsing(tmp_path: Path) -> None:
    client = mock_client(
        post_responses=[httpx.Response(200, json=olmocr_response("þā"))]
    )
    result = hosted_runner(client).invoke(
        planned_batch(1),
        packaged_input(1),
        tmp_path,
    )
    assert result.failure_item_ids == []
    artifact = result.output_artifacts[0]
    assert artifact.batch_item_ids == [planned_batch(1).items[0].item_id]
    assert Path(tmp_path, artifact.artifact_path).read_text(encoding="utf-8")
```

Add tests for 429/502 failure capture, timeout, missing token, idempotency header,
and no local fallback/subprocess call.

- [ ] **Step 2: Run tests and verify import failure**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_olmocr_runner.py
```

- [ ] **Step 3: Build olmOCR queries without copying upstream prompt**

Import pinned helper:

```python
from olmocr.prompts import build_no_anchoring_v4_yaml_prompt

# ponytail: pinned upstream helper avoids owning olmOCR prompt text;
# replace only when upstream exposes a public builder or pinned upgrade breaks.
query = {
    "model": self._runner.model_name,
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": build_no_anchoring_v4_yaml_prompt()},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{image_base64}"},
                },
            ],
        }
    ],
    "max_tokens": 8000,
    "temperature": 0.0,
}
```

For packaged PDF, zip `batch_item_ids` with `page_numbers`. For direct image,
page number is `1`. Render a selected packaged-PDF page with already-installed
`pypdfium2`; load direct images with Pillow. Resize proportionally only when
longest edge exceeds `target_longest_image_dim`, encode deterministic PNG bytes,
then Base64 them. Do not call olmOCR pipeline code, Poppler, or local model code.

- [ ] **Step 4: Call only hosted OpenAI-compatible endpoint**

Health URL: `<endpoint_url>/models`.
Completion URL: `<endpoint_url>/chat/completions`.

Headers:

```python
{
    "Authorization": f"Bearer {token}",
    "Idempotency-Key": f"{batch.batch_id}:{item_id}",
    "X-Scale-Up-Timeout": str(
        int(policy.endpoint.cold_start_timeout_seconds)
    ),
}
```

Use configured request timeout. Save response bytes under
`witnesses/<batch-id>/<item-id>.json` before JSON interpretation. Never log
headers/token. Record response `x-request-id` when present.

Classify configured retryable status codes as failed items with warnings; raise
only for local filesystem/config programming errors. One bad item must not erase
successful item artifacts.

- [ ] **Step 5: Run tests and commit**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_olmocr_runner.py
rtk git add bochord/services/olmocr_runner.py tests/test_olmocr_runner.py
rtk git commit -m "feat: execute hosted olmocr batches"
```

### Task 4: Persist Runs, Retries, Throughput, and CLI

**Files:**

- Create: `bochord/services/runner_execution.py`
- Create: `tests/test_runner_execution.py`
- Modify: `bochord/cli/cli.py`
- Modify: `tests/test_cli_commands.py`

**Interfaces:**

```python
class RunnerExecutionService:
    def __init__(
        self,
        planner: RunnerBatchPlanner,
        packager: RunnerInputPackager,
        runner: HuggingFaceOlmocrRunner,
    ) -> None: ...

    def run(
        self,
        run_id: str,
        document_id: str,
        artifacts: list[PreparedArtifactRef],
        bundle_root: Path,
        output_dir: Path,
    ) -> tuple[list[RunnerExecutionBatch], RunnerThroughputSummary]: ...
```

Per-run mutable state lives in private `RunnerExecutionOrchestrator`; facade
constructs it per `run` call.

CLI:

```text
bochord run PREPARED-INPUTS.json
  --policy OLMOCR-POLICY.json
  --runner RUNNER-REFERENCE.json
  --bundle-root BUNDLE
  --output-dir OUTPUT
  --run-id RUN-ID
  --document-id DOCUMENT-ID
```

Output:

```text
OUTPUT/
  runner-inputs/...
  witnesses/<batch-id>/...
  batches/<batch-id>.json
  throughput.json
```

- [ ] **Step 1: Write failing orchestration tests**

```python
def test_partial_batch_persists_before_failed_item_retry(tmp_path: Path) -> None:
    service = execution_service(
        first_result=hosted_result(failed=["item-2"]),
        retry_result=hosted_result(failed=[]),
    )
    batches, summary = service.run(
        "run-1",
        "bt",
        prepared_artifacts(2),
        fixture_root(),
        tmp_path,
    )
    assert [batch.result_status for batch in batches] == [
        BatchResultStatus.PARTIAL,
        BatchResultStatus.SUCCEEDED,
    ]
    assert batches[1].retry_of_batch_id == batches[0].batch_id
    assert batches[1].retry_strategy == "failed-items"
    assert len(list((tmp_path / "batches").glob("*.json"))) == 2
    assert summary.failed_item_count == 0


def test_warmup_batch_is_excluded_from_throughput(tmp_path: Path) -> None:
    _, summary = execution_service(warmup_batch_count=1).run(
        "run-1",
        "bt",
        prepared_artifacts(8),
        fixture_root(),
        tmp_path,
    )
    assert summary.measured_item_count == 4
```

Add health-failure persistence, all-failed status, no-retry policy, max one
retry, and timestamp ordering tests.

- [ ] **Step 2: Run tests and verify import failure**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_runner_execution.py
```

- [ ] **Step 3: Implement per-run orchestrator**

For each planned batch:

1. plan original batches, then run the endpoint health check once;
2. if health fails, atomically persist every planned batch as `FAILED`, attach
   every item id to `failed_item_ids`, add one health warning, and return without
   packaging or invoking;
3. capture UTC start;
4. package input;
5. invoke concrete runner;
6. capture UTC finish;
7. derive `SUCCEEDED`, `PARTIAL`, or `FAILED` from failed item ids;
8. build and atomically persist `RunnerExecutionBatch`;
9. if configured, create one retry batch from failed items only;
10. persist retry with `retry_of_batch_id` and `retry_strategy`;
11. continue next original batch.

Derive the single retry id without a new id service:

```python
retry_batch_id = "batch-" + sha256(
    (
        f"{original.batch_id}\nretry-1\n"
        + ",".join(sorted(original.failed_item_ids))
    ).encode("utf-8")
).hexdigest()
```

Use temporary sibling plus `Path.replace` for batch JSON so interrupted writes
never leave partial JSON. Do not normalize witnesses here.

Throughput uses finished-started duration for non-warmup batches only. Failure
rate counts final item outcome after allowed retry.

- [ ] **Step 4: Add thin CLI command**

Resolve settings only after strict file validation:

```python
token = settings.huggingface_api_key
if not token:
    raise click.ClickException(
        "missing settings value huggingface_api_key"
    )

endpoint_url = settings.huggingface_model_endpoints.get(
    policy.endpoint.endpoint_key
)
if endpoint_url is None:
    raise click.ClickException(
        "missing Hugging Face endpoint for "
        f"{policy.endpoint.endpoint_key}"
    )
```

Construct `httpx.Client`, concrete runner, collaborators, and service. Always
close client. Print batch count, final failure count, measured items/second, and
output path. Never print endpoint token or request headers.

- [ ] **Step 5: Run required quality gate**

```bash
source .venv/bin/activate
rtk ruff check bochord/models/runner_execution.py bochord/models/ocr.py \
  bochord/models/__init__.py bochord/services/runner_batching.py \
  bochord/services/runner_packaging.py bochord/services/olmocr_runner.py \
  bochord/services/runner_execution.py bochord/cli/cli.py \
  tests/test_ocr_models.py tests/test_runner_batching.py \
  tests/test_runner_packaging.py tests/test_olmocr_runner.py \
  tests/test_runner_execution.py tests/test_cli_commands.py
rtk .venv/bin/mypy bochord/models/runner_execution.py bochord/models/ocr.py \
  bochord/models/__init__.py bochord/services/runner_batching.py \
  bochord/services/runner_packaging.py bochord/services/olmocr_runner.py \
  bochord/services/runner_execution.py bochord/cli/cli.py
rtk make napoleon-gate
rtk pytest -q
```

Expected: all offline tests pass; no live endpoint required.

- [ ] **Step 6: Commit**

```bash
rtk git add bochord/services/runner_execution.py bochord/cli/cli.py \
  tests/test_runner_execution.py tests/test_cli_commands.py
rtk git commit -m "feat: persist runner execution and retries"
```

## Final Review Focus

Cursor Grok 4.5 final reviewer must verify:

- no local inference/download path exists;
- no token enters persisted models, logs, digests, or command arguments;
- every raw response and packaged input remains attributable to exact batch items;
- failed original batches remain persisted after successful retry;
- page-local batch grouping and warm-up exclusion match policy;
- no generic runner protocol/plugin registry was introduced.

## Cost Stop

Stop after one concrete hosted olmOCR path. No adaptive batching, concurrency
pool, cluster scheduler, endpoint provisioning, autoscaler control, generic
plugin registry, normalization, merge, or model bake-off ranking. Add common
runner interface only after second and third real adapters expose shared shape.
