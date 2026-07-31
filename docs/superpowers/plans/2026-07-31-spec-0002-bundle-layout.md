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

- In-memory `DocumentBundle` / `BundlePage` / witnesses / evaluation / review events exist.
- Runner execution already writes raw responses under ad-hoc `witnesses/` paths.
- No Spec 0002 tree writer, document/page manifest models, or append-only overlay file API.
- Spec 0009 produces accepted graphs in memory; this plan persists them.

---

## File Map

- Create: `bochord/models/bundle_layout.py` — document/page manifest models + path constants.
- Modify: `bochord/models/__init__.py` — exports.
- Create: `bochord/services/bundle_layout.py` — `BundleLayoutService`.
- Create: `tests/test_bundle_layout.py`
- Create: `tests/fixtures/bundle_layout/minimal_document.json` — in-memory bundle seed.
- Modify: `bochord/cli/cli.py` — thin `inspect-bundle` only if needed for one executable check; prefer service-level API without CLI unless a 10-line command helps. **Default: no CLI** (Spec 0004 lists `inspect-bundle` later; YAGNI unless tests need it).

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

- [ ] **Step 1: Write failing path + manifest tests**

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

- [ ] **Step 2: Run tests to verify they fail**

- [ ] **Step 3: Implement models + path helpers**

- [ ] **Step 4: Run tests to verify they pass**

- [ ] **Step 5: Quality gate + commit**

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

- [ ] **Step 1: Write failing write/read tests** asserting tree shape with `tmp_path.rglob` and manifest fields.

Required assertions:

- `manifest.json` exists with page_count and runner_set
- `source/pages/0001.jp2` (or `.png`) exists from `source_page_images`
- `pages/page-0001/graph/page_graph.json` round-trips spans/notes
- prepared `image/` keeps real extension/basename (not forced to `page.png`)
- `evaluation/scores.json` matches page summary dump; document `evaluation/summary.json` matches document summary
- witness lands under `witnesses/text/`
- second write refreshes graph content
- second write leaves a pre-seeded `review_events.jsonl` byte-identical (append-only guard before Task 3 API exists)

- [ ] **Step 2: Run tests to verify they fail**

- [ ] **Step 3: Implement writer/reader**

- [ ] **Step 4: Run tests to verify they pass**

- [ ] **Step 5: Quality gate + commit**

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

- [ ] **Step 1: Write failing append-only tests**

- [ ] **Step 2: Run tests to verify they fail**

- [ ] **Step 3: Implement append + state write**

- [ ] **Step 4: Run full bundle suite**

```bash
pytest tests/test_bundle_layout.py -q
```

- [ ] **Step 5: Quality gate + commit**

```bash
git commit -m "$(cat <<'EOF'
feat: append-only bundle review event logs

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

## Cost Stop

Stop after layout service write/read/append. No full orchestrator wiring, no RAG export generation, no TEI, no CLI unless a test truly cannot call the service, no resumability/caching (Phase 10).
