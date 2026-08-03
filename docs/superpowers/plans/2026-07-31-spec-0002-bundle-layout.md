# Spec 0002 V1 Bundle Layout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Persist one document run as the Spec 0002 on-disk bundle layout with deterministic page ids, layered artifacts, and append-only review history.

**Architecture:** Add a stateless `BundleLayoutService` that writes/reads the filesystem tree from existing in-memory models (`DocumentBundle`, `BundlePage`, witnesses, evaluation, overlays). Keep ADR 0004 layers split on disk: raw witnesses, derived `graph/page_graph.json`, overlays, exports. Do not invent new graph semantics here — only layout + manifests.

**Tech Stack:** Python 3.13, Pydantic 2, stdlib `pathlib`/`json`/`hashlib`, pytest. No new dependency.

**Sequence:** 4 of 4. Start only after Spec 0009 plan passes final review.

**Governing ADR:** ADR 0002 (document bundle per run), ADR 0004 (layered artifacts), ADR 0008 (stable ids + append-only review history).

## Global Constraints

- On-disk tree matches Spec 0002 top-level layout.
- Page identities deterministic and stable across reruns (`page-0001`, …).
- Pass artifacts record pass name + instance identity.
- Recomputable files overwrite deterministically; human overlays stay separate; review history append-only.
- Source page-image filenames keep the real input extension (`.jp2` not required). Spec's illustrative `page.png` under `pages/page-NNNN/image/` is an example only — never force that basename.
- Document + page manifests carry Spec 0002 required fields.
- Tree includes Spec `source/pages/` (raw source page images) distinct from prepared `pages/page-NNNN/image/`.
- Minimum graph payload already defined by models; writer serializes `BundlePage` graph nodes to `graph/page_graph.json`.
- Typography/role vocabulary already in models — do not redefine.
- Allowed v1 note kind remains `footnote-block` (`NoteKind` already).
- Follow Napoleon docstrings and `#:` attribute comments on all non-test Python.
- Before Python commands: `source .venv/bin/activate`.
- After Python edits: touched-file `ruff`, touched-file `mypy`, `make napoleon-gate`, then focused pytest.
- Caller/model strings used as path segments (`witness_kind`, `witness_id`,
  `source_files` keys, export basenames) must be basename-safe; writes must not
  escape the intended Spec 0002 directories.
- JSONL trailing-newline heal must be codepoint-agnostic (inspect last byte).

## Subagent Model Policy

- Implementation tasks may use only **Cursor Grok** (`cursor-grok-4.5-medium`) or **Composer 2.5 Fast** (`composer-2.5-fast`). No other implementer models.
- Prefer Composer 2.5 Fast for mechanical TDD; use Cursor Grok when stuck or judgment is required.
- Review steps (spec compliance, code quality, final whole-plan) may use any appropriate model.
- Give each implementer only the generated task brief, prior-task interface decisions, and listed files.

For every task, use this serial Superpowers loop:

1. Implementer (Composer 2.5 Fast or Cursor Grok) implements, runs listed checks, self-reviews, and commits.
2. Spec-compliance reviewer (any appropriate model) reviews without editing.
3. Same implementer fixes; re-review until approved.
4. Fresh code-quality reviewer (any appropriate model) reviews without editing.
5. Same fix/re-review loop for quality findings.

After the last task, a fresh reviewer audits the whole plan.
Do not start the next task or plan while either review has open findings.

## Existing Baseline

- Tasks 1–3 shipped on master (`BundlePaths`, manifests, `BundleLayoutService` write/read/append).
- Follow-up hardening already on branch `verify/spec-0002-bundle-layout`: prepared-image rewrite in graph, duplicate `page_number` reject, `witness_kind` whitelist, `_safe_basename` for `source_files`/`page_exports`, ASCII trailing-newline heal, contextual JSONL read errors.
- Residual blockers from final re-review (Tasks 4–5 below):
  - `witness_id` interpolated into destination filename without basename validation → path escape.
  - JSONL trailing-newline heal uses text-mode `seek(tell()-1)` → `UnicodeDecodeError` on multi-byte last char.
- Parked (out of Spec 0002 / this plan’s manifest interface): adding `run_id` to `DocumentBundleManifest` (ADR 0008 overlay rebasing later).
- No CLI for bundle layout (Spec 0004 lists `inspect-bundle` later).

---

## File Map

- Exists: `bochord/models/bundle_layout.py` — document/page manifest models + path constants.
- Exists: `bochord/services/bundle_layout.py` — `BundleLayoutService` (+ `_safe_basename`, `_WITNESS_FAMILIES`).
- Exists: `tests/test_bundle_layout.py`, `tests/fixtures/bundle_layout/minimal_document.json`.
- Tasks 4–5 modify only the service + tests. **No CLI.**

### Task 1: Manifest Models and Path Helpers

**Files:**

- Create: `bochord/models/bundle_layout.py`
- Modify: `bochord/models/__init__.py`
- Create: `tests/test_bundle_layout.py`

**Interfaces:**

```python
BUNDLE_SCHEMA_VERSION = "bochord-bundle-v1"


class BundlePaths:
    """Relative path helpers for one document bundle root."""

    def __init__(self, root: Path) -> None:
        self.root = root

    @property
    def document_manifest(self) -> Path: ...  # manifest.json

    def source_dir(self) -> Path: ...  # source/
    def source_provenance(self) -> Path: ...  # source/provenance.json
    def source_pages_dir(self) -> Path: ...  # source/pages/
    def source_page_image(self, page_number: int, extension: str) -> Path:
        ...  # source/pages/0001.jp2 (zero-pad page number; keep real extension)

    def page_dir(self, page_number: int) -> Path: ...  # pages/page-0001/
    def page_manifest(self, page_number: int) -> Path: ...
    def page_image_dir(self, page_number: int) -> Path: ...  # pages/page-0001/image/
    def witnesses_dir(self, page_number: int, family: str) -> Path: ...
    def page_graph(self, page_number: int) -> Path: ...
    def evaluation_scores(self, page_number: int) -> Path: ...
    def evaluation_flags(self, page_number: int) -> Path: ...
    def review_events(self, page_number: int) -> Path: ...
    def overlay_state(self, page_number: int) -> Path: ...
    def page_export(self, page_number: int, name: str) -> Path: ...
    def document_evaluation_summary(self) -> Path: ...  # evaluation/summary.json
    def document_exports_dir(self) -> Path: ...


def page_dir_name(page_number: int) -> str:
    return f"page-{page_number:04d}"


class DocumentBundleManifest(SchemaModel):
    schema_version: str
    document_id: str
    source: SourceDescriptor
    bibliographic_provenance: BibliographicProvenance
    acquisition_provenance: AcquisitionProvenance
    run_timestamp_utc: datetime
    config_digest: str
    runner_set: list[RunnerReference]
    page_count: int = Field(gt=0)
    bundle_schema_version: str


class PageBundleManifest(SchemaModel):
    schema_version: str
    page_id: str
    page_number: int = Field(gt=0)
    source_image_path: str
    executed_passes: list[RunnerReference] = Field(default_factory=list)
    witness_artifacts: list[WitnessReference] = Field(default_factory=list)
    graph_artifact_path: str
    evaluation_scores_path: str | None = None
    evaluation_flags_path: str | None = None
    overlay_state_path: str | None = None
    review_events_path: str
```

- [x] **Step 1: Write failing path + manifest tests**

```python
def test_page_dir_name_is_zero_padded() -> None:
    assert page_dir_name(1) == "page-0001"
    assert page_dir_name(12) == "page-0012"


def test_bundle_paths_match_spec_0002_layout(tmp_path: Path) -> None:
    paths = BundlePaths(tmp_path / "doc")
    assert paths.source_pages_dir() == paths.root / "source/pages"
    assert paths.source_page_image(1, ".jp2") == paths.root / "source/pages/0001.jp2"
    assert paths.page_graph(1) == paths.root / "pages/page-0001/graph/page_graph.json"
    assert paths.review_events(1) == (
        paths.root / "pages/page-0001/overlays/review_events.jsonl"
    )
```

- [x] **Step 2: Run tests to verify they fail**

- [x] **Step 3: Implement models + path helpers**

- [x] **Step 4: Run tests to verify they pass**

- [x] **Step 5: Quality gate + commit**

```bash
git commit -m "$(cat <<'EOF'
feat: add document bundle path and manifest models

EOF
)"
```

### Task 2: Write Bundle Tree from DocumentBundle

**Files:**

- Create: `bochord/services/bundle_layout.py`
- Modify: `tests/test_bundle_layout.py`
- Create: `tests/fixtures/bundle_layout/minimal_document.json`

**Interfaces:**

```python
class BundleLayoutService:
    """Write and read Spec 0002 document bundle trees."""

    def write_document_bundle(
        self,
        bundle: DocumentBundle,
        root: Path,
        *,
        # Keys = destination basenames under source/ (e.g. "source.pdf").
        source_files: Mapping[str, Path] | None = None,
        # Keys = 1-based page_number → source/pages/{page:04d}{ext}.
        source_page_images: Mapping[int, Path] | None = None,
        # Keys = page_id → pages/page-NNNN/image/<src.name> (basename preserved).
        page_images: Mapping[str, Path] | None = None,
        # Keys = witness_id → copied to witnesses/{family}/<src.name>.
        witness_files: Mapping[str, Path] | None = None,
        # Keys = page_id → {export_basename: text content}.
        page_exports: Mapping[str, Mapping[str, str]] | None = None,
    ) -> DocumentBundleManifest:
        """
        Materialize the on-disk tree (recomputable layers only).

        Side Effects:
            Creates directories and writes JSON/text/image copies under ``root``.
            Creates empty ``overlays/review_events.jsonl`` if missing; never
            truncates an existing events file. Does not write overlay state
            or review event payloads (Task 3 owns those).
        """

    def read_document_manifest(self, root: Path) -> DocumentBundleManifest: ...

    def read_page_manifest(self, root: Path, page_number: int) -> PageBundleManifest: ...

    def read_page_graph(self, root: Path, page_number: int) -> BundlePage: ...
```

Writer rules:

1. Create exact Spec 0002 directories, including `source/pages/` and empty witness family dirs (`text`/`layout`/`style`/`table`).
2. Copy top-level source artifact into `source/` retaining extension; write `source/provenance.json` from acquisition+bibliographic subset.
3. Copy each raw source page image into `source/pages/{page:04d}{ext}` via `source_page_images` (extension from the supplied path, not forced to `.jp2`).
4. For each page under `pages/page-NNNN/`:
   - copy prepared image into `image/` keeping the **real filename/extension** (ignore Spec's illustrative `page.png` basename);
   - write `graph/page_graph.json` as `BundlePage.model_dump(mode="json")`;
   - evaluation mapping:
     - `evaluation/scores.json` ← `PageEvaluationSummary.model_dump(mode="json")` when present;
     - `evaluation/flags.json` ← `{"flags": [...]}` collected from summary family flag lists when any flags exist, else omit or write `{"flags": []}`;
   - exports if provided.
5. Witness files copy into `witnesses/{family}/` using artifact filename; family from `witness_kind`. When writing the page manifest, rewrite each `WitnessReference.artifact_path` to the in-bundle relative path under `pages/page-NNNN/witnesses/{family}/<filename>` (do not leave pre-write absolute/ad-hoc paths).
6. Page manifest `executed_passes`: unique `RunnerReference` values derived from runners present on that page's `witnesses` (match `runner_id` against `bundle.run.runner_set`); not a blind copy of the full document `runner_set` unless every runner actually emitted a witness on that page.
7. Document `evaluation/summary.json` ← `DocumentEvaluationSummary.model_dump(mode="json")` + `exports/` when present.
8. Atomic writes: temp file + `Path.replace` for JSON (not for append-only JSONL).
9. Re-run overwrite set: manifests, graph, scores, flags, exports, source/prepared images, witnesses. **Never truncate or rewrite** existing `overlays/review_events.jsonl`. If missing, create empty file and point page manifest at it. Overlay `current_state.json` is Task 3 only — Task 2 neither takes nor writes overlay payloads.

`page_graph.json` payload = `BundlePage.model_dump(mode="json")` (YAGNI wrapper).

- [x] **Step 1: Write failing write/read tests** asserting tree shape with `tmp_path.rglob` and manifest fields.

Required assertions:

- `manifest.json` exists with page_count and runner_set
- `source/pages/0001.jp2` (or `.png`) exists from `source_page_images`
- `pages/page-0001/graph/page_graph.json` round-trips spans/notes
- prepared `image/` keeps real extension/basename (not forced to `page.png`)
- `evaluation/scores.json` matches page summary dump; document `evaluation/summary.json` matches document summary
- witness lands under `witnesses/text/`
- second write refreshes graph content
- second write leaves a pre-seeded `review_events.jsonl` byte-identical (append-only guard before Task 3 API exists)

- [x] **Step 2: Run tests to verify they fail**

- [x] **Step 3: Implement writer/reader**

- [x] **Step 4: Run tests to verify they pass**

- [x] **Step 5: Quality gate + commit**

```bash
git commit -m "$(cat <<'EOF'
feat: write Spec 0002 document bundle layout

EOF
)"
```

### Task 3: Append-Only Review Overlays

**Files:**

- Modify: `bochord/services/bundle_layout.py`
- Modify: `tests/test_bundle_layout.py`

**Interfaces:**

```python
class BundleLayoutService:
    def append_review_events(
        self,
        root: Path,
        page_number: int,
        events: list[ReviewEvent],  # discriminated union, not ReviewEventBase
    ) -> None:
        """
        Append JSONL review events; never rewrite prior lines.

        Side Effects:
            Creates/appends ``overlays/review_events.jsonl``.
        """

    def write_overlay_state(
        self,
        root: Path,
        page_number: int,
        states: list[OverlayState],
    ) -> None:
        """Overwrite ``overlays/current_state.json`` deterministically."""

    def read_review_events(
        self,
        root: Path,
        page_number: int,
    ) -> list[dict[str, Any]]: ...
```

Rules:

- `append_review_events` opens in append mode; refuses truncate.
- Test: write events A, append B, read back A then B in order; file size only grows.
- Also test: `write_document_bundle` after append does not shrink or rewrite JSONL (ADR 0008).
- `current_state.json` may overwrite (derived current view); history stays in JSONL.
- Page manifest always points at review_events path (empty file ok from Task 2).

- [x] **Step 1: Write failing append-only tests**

- [x] **Step 2: Run tests to verify they fail**

- [x] **Step 3: Implement append + state write**

- [x] **Step 4: Run full bundle suite**

```bash
pytest tests/test_bundle_layout.py -q
```

- [x] **Step 5: Quality gate + commit**

```bash
git commit -m "$(cat <<'EOF'
feat: append-only bundle review event logs

EOF
)"
```

### Task 4: Sanitize `witness_id` in Witness Destination Filenames

**Why:** Residual from final re-review (extends I-4). `_copy_witnesses` builds
`filename = f"{witness.witness_id}_{basename}"` without validating `witness_id`.
A value like `"../../../../"` writes outside `pages/page-NNNN/witnesses/<family>/`.

**Files:**

- Modify: `bochord/services/bundle_layout.py` (`_copy_witnesses`)
- Modify: `tests/test_bundle_layout.py`

**Interfaces:**

- Consumes: existing `_safe_basename(value: str, *, label: str) -> str`
- Produces: destination filename uses only validated basename segments; unsafe
  `witness_id` raises `ValueError` before any copy

**Rules:**

1. Before interpolating `witness.witness_id` into the destination filename, run
   `safe_id = _safe_basename(witness.witness_id, label="witness_id")`.
2. Keep collision-avoidance prefix: `filename = f"{safe_id}_{basename}"` where
   `basename` is still `source_path.name` (already a filesystem basename).
3. Do **not** change `WitnessReference.witness_id` on the rewritten model — only
   the on-disk filename segment is sanitized. Manifest/graph keep the original id.
4. Reject must happen even when `witness_files` is omitted (path is still written
   into the rewritten `artifact_path`).

- [x] **Step 1: Write failing test**

```python
def test_write_document_bundle_rejects_unsafe_witness_id(tmp_path) -> None:
    """Path-traversal witness_id must not become a destination filename segment."""
    bundle = load_minimal_bundle()
    page = bundle.pages[0]
    unsafe_id = "../../../../"
    bad_witness = page.witnesses[0].model_copy(update={"witness_id": unsafe_id})
    bundle = bundle.model_copy(
        update={"pages": [page.model_copy(update={"witnesses": [bad_witness]})]}
    )
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    source_files, source_page_images, page_images, _ = _write_minimal_inputs(tmp_path)
    witness_src = tmp_path / "inputs" / "olmocr-response.json"

    with pytest.raises(ValueError, match="witness_id"):
        service.write_document_bundle(
            bundle,
            root,
            source_files=source_files,
            source_page_images=source_page_images,
            page_images=page_images,
            witness_files={unsafe_id: witness_src},
        )
    assert not (root / "_olmocr-response.json").exists()
    assert not (tmp_path / "_olmocr-response.json").exists()
```

Existing `test_write_document_bundle_keeps_same_basename_witnesses` remains the
regression guard for safe ids (`wit-a` / `wit-b`).

- [x] **Step 2: Run test to verify it fails**

```bash
source .venv/bin/activate
pytest tests/test_bundle_layout.py::test_write_document_bundle_rejects_unsafe_witness_id -q
```

Expected: FAIL (unsafe id currently accepted / file escapes to bundle root).

- [x] **Step 3: Minimal implementation**

In `_copy_witnesses`, validate before building `filename`:

```python
safe_id = _safe_basename(witness.witness_id, label="witness_id")
if witness_files and witness.witness_id in witness_files:
    source_path = witness_files[witness.witness_id]
    basename = source_path.name
else:
    basename = Path(witness.artifact_path).name
filename = f"{safe_id}_{basename}"
```

Keep `witness.witness_id` unchanged on the rewritten `WitnessReference`.
Raise via `_safe_basename` before `destination_dir.mkdir` / `shutil.copy2`.
Update the method `Raises:` docstring to mention unsafe `witness_id`.

- [x] **Step 4: Run focused suite**

```bash
pytest tests/test_bundle_layout.py -q
```

Expected: all prior tests still pass; new reject test passes.

- [x] **Step 5: Quality gate + commit**

```bash
source .venv/bin/activate
ruff check bochord/services/bundle_layout.py tests/test_bundle_layout.py
mypy bochord/services/bundle_layout.py
make napoleon-gate
pytest tests/test_bundle_layout.py -q
graphify update .
git commit -m "$(cat <<'EOF'
fix: sanitize witness_id in bundle witness filenames

EOF
)"
```

### Task 5: Binary-Safe JSONL Trailing-Newline Heal

**Why:** Residual from final re-review (extends I-5). `append_review_events`
opens UTF-8 text mode and does `handle.seek(handle.tell() - 1)` to inspect the
last character. When the file ends on a multi-byte UTF-8 codepoint (e.g. `é`)
without a trailing newline, seek lands mid-codepoint → `UnicodeDecodeError`
instead of healing.

**Files:**

- Modify: `bochord/services/bundle_layout.py` (`append_review_events`)
- Modify: `tests/test_bundle_layout.py`

**Interfaces:**

- Consumes: existing `append_review_events` / `read_review_events` contracts
- Produces: heal check that inspects the last **byte** (`b"\n"`) without
  text-mode character arithmetic; append behavior otherwise unchanged

**Rules:**

1. Peek last byte with a short binary open (`"rb"`) or `handle.buffer` — do not
   subtract 1 from a text-mode position and re-read as UTF-8.
2. If file non-empty and last byte ≠ `0x0A`, write `"\n"` then append events.
3. Never truncate or rewrite prior JSONL lines (ADR 0008).
4. Keep contextual `ValueError` on corrupt lines in `read_review_events` (already shipped).

- [x] **Step 1: Write failing test**

```python
def test_append_review_events_heals_missing_newline_after_multibyte_utf8(
    tmp_path,
) -> None:
    """Heal must not UnicodeDecodeError when prior JSONL ends on multi-byte UTF-8."""
    bundle = load_minimal_bundle()
    service = BundleLayoutService()
    root = tmp_path / "bundle"
    source_files, source_page_images, page_images, witness_files = (
        _write_minimal_inputs(tmp_path)
    )
    service.write_document_bundle(
        bundle,
        root,
        source_files=source_files,
        source_page_images=source_page_images,
        page_images=page_images,
        witness_files=witness_files,
    )

    review_path = root / "pages" / "page-0001" / "overlays" / "review_events.jsonl"
    # Ends on multi-byte UTF-8 'é' (U+00E9 → c3 a9), no trailing newline
    review_path.write_bytes(b'{"event_id":"partial","note":"caf\xc3\xa9')

    service.append_review_events(root, 1, [_accept_review_event("evt-1")])

    raw = review_path.read_bytes()
    assert raw.endswith(b"\n")
    assert b'"event_id":"evt-1"' in raw or b'"event_id": "evt-1"' in raw
    # Damaged first line may still be unreadable; append itself must succeed.
```

- [x] **Step 2: Run test to verify it fails**

```bash
source .venv/bin/activate
pytest tests/test_bundle_layout.py::test_append_review_events_heals_missing_newline_after_multibyte_utf8 -q
```

Expected: FAIL with `UnicodeDecodeError` (current text-mode seek).

- [x] **Step 3: Minimal implementation**

Replace text-mode last-char peek with a module helper that peeks the last byte:

```python
def _needs_trailing_newline(path: Path) -> bool:
    """
    Return True when ``path`` exists, is non-empty, and does not end with ``\\n``.

    Args:
        path: JSONL file path.

    Returns:
        Whether a separator newline should be written before appending.

    """
    if not path.exists() or path.stat().st_size == 0:
        return False
    with path.open("rb") as handle:
        handle.seek(-1, 2)
        return handle.read(1) != b"\n"
```

In `append_review_events`:

```python
review_events_path.parent.mkdir(parents=True, exist_ok=True)
needs_newline = _needs_trailing_newline(review_events_path)
with review_events_path.open("a", encoding="utf-8") as handle:
    if needs_newline:
        handle.write("\n")
    handle.write("\n".join(lines) + "\n")
```

Prefer `"a"` once binary peek is separate — do not `seek` on the text handle.

- [x] **Step 4: Run focused suite**

```bash
pytest tests/test_bundle_layout.py -q
```

Expected: new test passes; existing
`test_append_review_events_heals_missing_trailing_newline` still passes.

- [x] **Step 5: Quality gate + commit**

```bash
source .venv/bin/activate
ruff check bochord/services/bundle_layout.py tests/test_bundle_layout.py
mypy bochord/services/bundle_layout.py
make napoleon-gate
pytest tests/test_bundle_layout.py -q
graphify update .
git commit -m "$(cat <<'EOF'
fix: heal JSONL trailing newline with binary peek

EOF
)"
```

## Final Review Focus

- Disk tree matches Spec 0002 (names + layer split).
- Manifests include required document/page fields.
- Source extensions preserved.
- Graph minimum model serialized (regions/lines/spans/notes + provenance).
- Review JSONL append-only; overlays separate from witnesses/graph.
- ADR 0002/0004/0008 respected.
- No merge/normalization logic reimplemented inside writer.
- All path segments derived from caller/model strings (`witness_kind`,
  `witness_id`, `source_files` keys, export names) are basename-safe; writes
  cannot escape `pages/page-NNNN/witnesses/<family>/` or the bundle root.
- JSONL trailing-newline heal is codepoint-agnostic (byte peek, not text seek).

## Cost Stop

Stop after Tasks 4–5 harden the shipped layout service. No `run_id` on
`DocumentBundleManifest` (parked), no full orchestrator wiring, no RAG/TEI
export generation, no CLI, no resumability/caching (Phase 10).
