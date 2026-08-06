# README, Operator Docs, and Thin Export CLI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give operators an honest path from PDF/page images/zip toward evidence-preserving Markdown, with a thin `export` CLI, fleshed-out user/runbook docs (no API section), and a marketing README that matches reality.

**Architecture:** Keep assembly of `DocumentBundle` from prepare/run/merge out of scope (later `B*` slice). This plan only wraps existing `BundleLayoutService.write_document_exports(bundle, root)` behind `bochord export <document-bundle.json> --bundle-root <dir>`, then documents provisional export vs human-corrected overlay path, then rewrites overview docs and README. Markdown remains a derived reading view, not source of truth (Spec 0006).

**Tech Stack:** Python 3.13, Click CLI, Pydantic models, Sphinx RST docs, pytest, existing `BundleLayoutService` / `DocumentExportService`.

## Locked Decisions (from grilling)

| Topic | Decision |
| --- | --- |
| Audience | Scholar-first; RAG as payoff |
| Problem | OCR that “works” still loses philological signal **and** agent evidence |
| Solution spine | Multi-pass image-first OCR → witness-preserving bundles → structured + RAG + Markdown exports |
| Why | Fidelity before cleverness; rebuildable evidence; agent-citable scholarship |
| Tone | Elevated scholarly; etymology once; early/evolving banner; **no Caltech** |
| Docs URL | `https://bochord.readthedocs.io` |
| Install | Source / `uv` only; note **not** the PyPI Books-backup `bochord` |
| Quick Start | Minimal honest real CLI (`version` / `--help`); deep path in runbook |
| Docs scope | User guides + operator runbooks; **remove API** toctree/section |
| Inputs | PDF / page images / zip of page images |
| E2E promise | Provisional machine markdown **and** corrected overlay path; mark CLI gaps |
| Export CLI | Thin: `bochord export <document-bundle.json> --bundle-root <dir>` |
| Assemble | **Deferred** (later `B*`: merge → `DocumentBundle` → materialize) |
| Review in e2e | Medium conceptual (overlay/task concepts + service names; no fake review CLI) |
| Delivery order | Export CLI → e2e runbook → overview docs → README last |

## Global Constraints

- Before Python: `/usr/bin/cd` into repo; `source .venv/bin/activate`; use `.venv` tools.
- Bare `cd` is a broken bash function — always `/usr/bin/cd`.
- Preserve unrelated dirty worktree (`AGENTS.md`, `graphify-out/`, etc.).
- No Spec 0004 Phase 5/6/10, no table/TEI/search, no PyPI publish, no rename decision in this plan.
- Do not invent a full assemble/merge CLI here.
- After Python edits: `ruff`, `mypy`, `make napoleon-gate`, focused pytest.
- Prefer graphify before broad exploration; update graphify after code changes.
- TDD for the export CLI.

## File Map

| File | Role |
| --- | --- |
| `bochord/cli/cli.py` | Add `export` command |
| `tests/test_cli_commands.py` | CLI tests for `export` |
| `doc/source/runbook/from_source_to_markdown.rst` | **New** hero e2e guide |
| `doc/source/index.rst` | Marketing-aligned intro; toctree: add e2e, drop API; Python ≥3.13 |
| `doc/source/overview/installation.rst` | Source/`uv` only; collision note; Python 3.13 |
| `doc/source/overview/quickstart.rst` | Real commands; link e2e guide |
| `doc/source/overview/usage.rst` | Document real CLI including `export` |
| `doc/source/overview/configuration.rst` | Truth from `Settings` / HF keys (no FILL_ME_IN) |
| `doc/source/overview/faq.rst` | Collision, markdown-not-SoT, assemble TBD, early status |
| `doc/source/runbook/ocr_process.rst` | Keep as stage theory; link e2e guide |
| `doc/source/runbook/huggingface_setup.rst` | Ensure install path matches (no PyPI lie) |
| `doc/source/runbook/operator_notes.rst` | Cross-link e2e; keep short rules |
| `doc/source/api/models.rst` | Remove from toctree (file may remain unlinked or delete if unused) |
| `README.md` | Full marketing rewrite last |

**Out of scope files:** `bochord/services/merge.py` assemble orchestration, PyPI rename, review CLI, architecture ADR/spec rewrites except cross-links.

### Task 1: Thin `export` CLI (TDD)

**Files:** Modify `bochord/cli/cli.py`; Modify `tests/test_cli_commands.py`.

**Consumes:** `BundleLayoutService.write_document_exports`, frozen fixture `tests/fixtures/export_models/document-bundle-v1.json` (or `load_frozen_document_bundle_v1` helpers in tests).

**Produces:** Runnable `bochord export <document-bundle.json> --bundle-root <dir>` writing `exports/document.md` (and sibling export artifacts).

- [ ] **Step 1: Write failing CLI tests**

  Follow patterns in `tests/test_cli_commands.py` (Click `CliRunner`). Prefer loading
  `tests/fixtures/export_models/document-bundle-v1.json` directly (do not import
  helpers from `tests/test_bundle_layout.py`). Cover at least:

  ```python
  def test_export_writes_document_markdown(tmp_path: Path) -> None:
      # Arrange: copy fixture document-bundle-v1.json into tmp_path
      # Act: invoke ["export", str(bundle_json), "--bundle-root", str(root)]
      # Assert: exit 0; (root / "exports" / "document.md").exists()
      # Assert: exports/bundle.json, rag.jsonl, stitched_chunks.jsonl exist

  def test_export_rejects_invalid_bundle_json(tmp_path: Path) -> None:
      # Act with malformed JSON
      # Assert: non-zero exit; ClickException / stderr mentions validation

  def test_export_requires_bundle_root(tmp_path: Path) -> None:
      # Missing --bundle-root → usage error
  ```

- [ ] **Step 2: Confirm RED**

  ```bash
  /usr/bin/cd /Users/cmalek/src/workspace/bochord && source .venv/bin/activate
  pytest tests/test_cli_commands.py -k "export" -q
  ```

  Expected: fail (command missing or incomplete).

- [ ] **Step 3: Implement minimal `export` command**

  In `bochord/cli/cli.py`, add Click command (Napoleon docs per AGENTS.md):

  ```python
  @cli.command("export")
  @click.argument(
      "document_bundle",
      type=click.Path(exists=True, dir_okay=False, path_type=Path),
  )
  @click.option(
      "--bundle-root",
      required=True,
      type=click.Path(file_okay=False, path_type=Path),
      help="Filesystem root that receives exports/ artifacts.",
  )
  def export_document(document_bundle: Path, bundle_root: Path) -> None:
      """Write derived bundle/RAG/Markdown exports from a DocumentBundle JSON."""
      try:
          bundle = DocumentBundle.model_validate_json(
              document_bundle.read_text(encoding="utf-8")
          )
          exported = BundleLayoutService().write_document_exports(
              bundle, bundle_root
          )
      except (OSError, ValidationError, ValueError) as exc:
          raise click.ClickException(str(exc)) from exc
      click.echo(f"markdown: {bundle_root / exported.exports.document_markdown_path}")
      click.echo(f"bundle_json: {bundle_root / exported.exports.bundle_json_path}")
  ```

  Import `DocumentBundle` and `BundleLayoutService` as needed. No assemble/merge logic.
  Expand the docstring to the repo Napoleon shape used by sibling commands
  (`Args` / `Side Effects` / `Raises`) — a one-line docstring will fail
  `napoleon-gate`.

- [ ] **Step 4: Confirm GREEN + quality gates**

  ```bash
  /usr/bin/cd /Users/cmalek/src/workspace/bochord && source .venv/bin/activate
  pytest tests/test_cli_commands.py -k "export" -q
  .venv/bin/ruff check bochord/cli/cli.py tests/test_cli_commands.py
  .venv/bin/mypy bochord/cli/cli.py
  make napoleon-gate
  ```

- [ ] **Step 5: Commit**

  ```bash
  git add bochord/cli/cli.py tests/test_cli_commands.py
  git commit -m "$(cat <<'EOF'
  feat: add thin document export CLI

  EOF
  )"
  ```

### Task 2: Hero e2e runbook `from_source_to_markdown`

**Files:** Create `doc/source/runbook/from_source_to_markdown.rst`; Modify `doc/source/index.rst` (toctree); Modify `doc/source/runbook/ocr_process.rst` and `doc/source/runbook/operator_notes.rst` (one-line links each).

**Produces:** Start→markdown narrative with provisional vs corrected paths and explicit gaps.

- [ ] **Step 1: Draft RST structure**

  Required sections:

  1. Purpose / early-software banner
  2. Inputs (PDF, page images, zip of images)
  3. Stage map: prepare → run → **(merge/assemble TBD)** → export
  4. **Provisional path:** when you already have valid `DocumentBundle` JSON → `bochord export …` → `exports/document.md`
  5. **Corrected path (conceptual):** review overlays / Spec 0005 concepts; services `review_markup` / `review_overlay`; re-export after accepted graph updates; **no review CLI yet**
  6. What Markdown is / is not (Spec 0006: derived view, not SoT)
  7. What is missing (assemble `B*`, merge CLI, review CLI)
  8. Links: installation, HF setup, `ocr_process`, operator_notes, gold_annotation

  Use real command names only. Include example:

  ```bash
  bochord export path/to/document-bundle.json --bundle-root path/to/bundle-root
  ```

- [ ] **Step 2: Wire toctree**

  In `doc/source/index.rst` Development or Getting Started toctree, add:

  ```rst
  runbook/from_source_to_markdown
  ```

  Prefer Getting Started (near quickstart) or User Guide — pick Getting Started so the hero path is obvious. Add a one-line pointer in `ocr_process.rst` Purpose and in `operator_notes.rst` Purpose to the new guide.

- [ ] **Step 3: Sphinx build smoke**

  ```bash
  /usr/bin/cd /Users/cmalek/src/workspace/bochord && source .venv/bin/activate
  make -C doc html  # or project’s usual docs build target
  ```

  Expected: build succeeds; no broken toctree refs.

- [ ] **Step 4: Commit**

  ```bash
  git add doc/source/runbook/from_source_to_markdown.rst doc/source/index.rst doc/source/runbook/ocr_process.rst doc/source/runbook/operator_notes.rst
  git commit -m "$(cat <<'EOF'
  docs: add source-to-markdown operator guide

  EOF
  )"
  ```

### Task 3: Fulfill overview docs + drop API

**Files:** Modify `doc/source/overview/{installation,quickstart,usage,configuration,faq}.rst`; Modify `doc/source/index.rst`; Modify `doc/source/runbook/huggingface_setup.rst` as needed; Remove API from toctree (and delete `doc/source/api/models.rst` only if nothing else references it).

**Produces:** No `__FILL_ME_IN__` / `group1` stubs in user-facing overview pages; Python 3.13; honest install.

- [ ] **Step 1: Inventory stubs**

  ```bash
  /usr/bin/cd /Users/cmalek/src/workspace/bochord
  rg -n "FILL_ME_IN|group1|group2|PyPI|3\\.10|3\\.11" doc/source/overview doc/source/index.rst doc/source/runbook/huggingface_setup.rst
  ```

- [ ] **Step 2: Rewrite installation**

  - Require Python **3.13+** (match `pyproject.toml` `requires-python`)
  - Primary: clone + `uv sync` / editable install from source
  - Explicit warning: PyPI name `bochord` may refer to an unrelated Books-backup project — do **not** `pip install bochord` for this tool until packaging story changes
  - Remove or demote PyPI install sections

- [ ] **Step 3: Rewrite quickstart + usage**

  - Real commands: `version`, `settings`, `prepare`, `run`, `eval`, `eval-cohorts`, `export`
  - Point deep walkthrough to `:doc:`/runbook/from_source_to_markdown``
  - Drop all `group1` examples

- [ ] **Step 4: Configuration + FAQ**

  - Configuration: document real Settings keys operators need (at least HF API key / endpoint mapping as used by `run`)
  - FAQ: early status; PyPI collision; Markdown not SoT; assemble/merge not yet CLI; link e2e guide

- [ ] **Step 5: Index + API removal**

  - Align index intro with problem/how/why (scholar-first)
  - Requirements: Python 3.13+
  - Getting Started list includes e2e guide
  - Remove `api/models` from Reference toctree; keep `changelog`
  - If `api/models.rst` orphaned, delete it in this commit

- [ ] **Step 6: Docs build + commit**

  ```bash
  make -C doc html
  git add doc/source/
  git commit -m "$(cat <<'EOF'
  docs: rewrite user guides and drop API reference

  EOF
  )"
  ```

### Task 4: Marketing README

**Files:** Modify `README.md`.

**Produces:** Full rewrite matching locked decisions; shop window for RTD.

- [ ] **Step 1: Replace README content**

  Structure:

  1. Title + one-line etymology (*bōchord*, book treasure-hoard)
  2. Early/evolving banner
  3. Problem (dual failure)
  4. How (solution spine)
  5. Why (fidelity / rebuildable / agents)
  6. Core features (3 bullets aligned with index)
  7. Documentation link: `https://bochord.readthedocs.io`
  8. Requirements: Python 3.13+
  9. Installation from source / `uv` + PyPI collision note
  10. Quick Start: `bochord --help`, `bochord version`; link e2e guide on RTD
  11. Commands table (real names only)
  12. Common use cases (research passes; reviewable exports; provisional markdown)
  13. No Caltech / institutional affiliation

- [ ] **Step 2: Sanity check**

  - No `pip install bochord` without collision warning
  - No placeholder Feature 1 / group1
  - Docs URL is `.io`

- [ ] **Step 3: Commit**

  ```bash
  git add README.md
  git commit -m "$(cat <<'EOF'
  docs: rewrite README for operator-facing product story

  EOF
  )"
  ```

### Task 5: Graphify + final verification

**Files:** none intentional (graphify-out may dirty; leave unstaged unless project normally commits it).

- [ ] **Step 1: Update code graph**

  ```bash
  /usr/bin/cd /Users/cmalek/src/workspace/bochord && graphify update .
  ```

- [ ] **Step 2: Final gates**

  ```bash
  source .venv/bin/activate
  pytest tests/test_cli_commands.py -k "export" -q
  .venv/bin/ruff check bochord/cli/cli.py tests/test_cli_commands.py
  .venv/bin/mypy bochord/cli/cli.py
  make napoleon-gate
  make -C doc html
  ```

- [ ] **Step 3: Report**

  Summarize commits, docs URL, remaining deferred work (`B*` assemble, review CLI, PyPI rename).

## Deferred (explicitly not this plan)

- **`B*`:** Assemble `DocumentBundle` from prepare/run/merge outputs + optional `bundle` CLI
- Review / overlay CLI
- PyPI name claim or package rename
- Spec 0004 Phases 5/6/10
- Filling every architecture ADR with tutorial prose

## Acceptance Checks

- `bochord export <valid DocumentBundle JSON> --bundle-root <dir>` writes `exports/document.md` and sibling Spec 0006 artifacts
- Invalid JSON fails with non-zero exit
- `from_source_to_markdown` documents provisional + conceptual corrected paths and lists assemble/review gaps
- Overview pages have no `FILL_ME_IN` / `group1` stubs
- API reference removed from published toctree
- README matches marketing locks; links `https://bochord.readthedocs.io`; warns about PyPI collision
- No Caltech mention in README/user docs touched here

## Plan Self-Review

- Spec coverage: Spec 0006 export families + Markdown-not-SoT preserved; Spec 0002 layout only via existing writers
- No duplicate assemble definition: deferred `B*` named once
- CLI thinness: export only wraps `write_document_exports`
- Docs-first operator need: hero runbook before README shop window
