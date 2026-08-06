# Rename `bochord` → `wordwending` Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename the project identity from `bochord` to `wordwending` (package, CLI, env/config names, live docs, GitHub) so the package can publish on PyPI under a free name.

**Architecture:** Big-bang rename on one branch: `git mv` the package tree, mechanical string replace on in-scope paths, hand-fix identity files (including config basenames and napoleon baseline), reinstall, verify with an allowlisted `rg` gate plus the full test suite, then `gh repo rename`. No compatibility shims.

**Tech Stack:** Python package (`pyproject.toml` / uv), Click CLI, pydantic-settings, Sphinx docs, GitHub (`gh`), pytest.

**Spec:** `docs/superpowers/specs/2026-08-06-wordwending-rename-design.md`

---

## File map

| Path | Role after rename |
|---|---|
| `bochord/` → `wordwending/` | Import package (git mv) |
| `pyproject.toml` | name, scripts, urls, vulture paths |
| `.bumpversion.cfg` | version file paths under `wordwending/` |
| `Makefile` | `PACKAGE = wordwending` |
| `MANIFEST.in` | `include wordwending/py.typed` |
| `wordwending/settings.py` | `env_prefix`, `app_name`, config basenames, `WORDWENDING_CONFIG_FILE` |
| `bin/check_napoleon_gate.py` | default target package name |
| `doc/quality/napoleon_gate_baseline.json` | absolute paths containing old package segment |
| `doc/source/**`, `README.md`, `AGENTS.md`, `CONTEXT.md` | live docs / agent contract |
| `tests/**` | imports + asserts for old name / env / config files |
| `uv.lock` | refreshed via `uv sync` (do not hand-edit) |
| `docs/superpowers/plans/**`, `docs/superpowers/specs/**` | **do not rewrite** (allowlist) |
| `graphify-out/**` | regenerate with `graphify update .` only |

**Config basename map (extends spec identity map):**

| Old | New |
|---|---|
| `.bochord.toml` | `.wordwending.toml` |
| `bochord.toml` (ProgramData) | `wordwending.toml` |
| `/etc/bochord/config.toml` | `/etc/wordwending/config.toml` |
| XDG/app dir `bochord` if any | `wordwending` |

**README gloss:** Replace *bōchord* etymology with a short neutral line, e.g. `` `wordwending` is a Python CLI for high-fidelity OCR of Old English / Anglo-Saxon source material. `` Drop the PyPI collision warning block.

---

### Task 1: Branch

**Files:** none

- [ ] **Step 1: Create feature branch**

```bash
source .venv/bin/activate
/usr/bin/cd /Users/cmalek/src/workspace/bochord
git checkout -b rename/wordwending
```

Expected: on `rename/wordwending`.

---

### Task 2: Move package directory

**Files:**
- Rename: `bochord/` → `wordwending/`

- [ ] **Step 1: git mv package tree**

```bash
git mv bochord wordwending
```

Expected: `wordwending/` exists; `bochord/` gone from tree (egg-info may still say bochord until reinstall).

- [ ] **Step 2: Confirm**

```bash
test -d wordwending && test ! -d bochord && ls wordwending/main.py
```

Expected: exit 0.

---

### Task 3: Mechanical replace (in-scope only)

**Files:** all in-scope paths that still contain `bochord` / `BOCHORD_` (see `rg` command in Task 7). Do **not** edit `docs/superpowers/plans/**` or rewrite other historical specs for branding.

- [ ] **Step 1: Bulk replace with ripgrep-driven sed (macOS)**

From repo root, replace in tracked in-scope files only. Prefer a careful loop over `rg -l` with the same exclusions as the verification gate:

```bash
source .venv/bin/activate
/usr/bin/cd /Users/cmalek/src/workspace/bochord

RG_EXCLUDES=(
  --glob '!docs/superpowers/plans/**'
  --glob '!docs/superpowers/specs/**'
  --glob '!graphify-out/**'
  --glob '!.venv/**'
  --glob '!*.egg-info/**'
  --glob '!.git/**'
  --glob '!.mypy_cache/**'
  --glob '!.pytest_cache/**'
  --glob '!.ruff_cache/**'
  --glob '!.worktrees/**'
  --glob '!doc/quality/napoleon_gate_baseline.json'
)

# Order matters: longer / uppercase tokens first
while IFS= read -r f; do
  sed -i '' \
    -e 's/BOCHORD_/WORDWENDING_/g' \
    -e 's/\.bochord\.toml/.wordwending.toml/g' \
    -e 's/bochord\.toml/wordwending.toml/g' \
    -e 's/bochord/wordwending/g' \
    "$f"
done < <(rg -l 'bochord|BOCHORD' "${RG_EXCLUDES[@]}")
```

**Important:** Exclude `doc/quality/napoleon_gate_baseline.json` from this loop. Bulk `s/bochord/wordwending/g` would rewrite both workspace and package path segments (`…/bochord/bochord/…` → `…/wordwending/wordwending/…`), which breaks Task 4 Step 3 and `make napoleon-gate` while the local folder is still named `bochord`. Hand-patch that file in Task 4.
- [ ] **Step 2: Spot-check critical files**

```bash
rg -n 'name = |env_prefix|project.scripts|PACKAGE|app_name' pyproject.toml wordwending/settings.py Makefile | head -40
```

Expected: `wordwending` / `WORDWENDING_` only (no `bochord`).

---

### Task 4: Hand-fix identity leftovers

**Files:**
- Modify: `wordwending/settings.py` (config path helpers)
- Modify: `bin/check_napoleon_gate.py` (default target list)
- Modify: `doc/quality/napoleon_gate_baseline.json` (path segments)
- Modify: `README.md` (branding + drop PyPI warning)
- Verify: `.bumpversion.cfg`, `MANIFEST.in`, `doc/source/conf.py`

- [ ] **Step 1: Fix settings config paths + cookiecutter typo**

In `wordwending/settings.py`, ensure:

- `env_prefix="WORDWENDING_"`
- `app_name` default `"wordwending"`
- User/local files: `.wordwending.toml`
- Windows ProgramData file: `wordwending.toml`
- Unix global in `get_config_paths`: `/etc/wordwending/config.toml`
- In `settings_customise_sources`, replace the broken cookiecutter path
  `"/etc/cookiecutter.project_python_name}}.toml"` with
  `"/etc/wordwending.toml"` (align with Windows `…/wordwending.toml` in the same method)
- Env key: `WORDWENDING_CONFIG_FILE`

- [ ] **Step 2: Napoleon gate default target**

In `bin/check_napoleon_gate.py`, default package target must be `wordwending` (not `bochord`).

- [ ] **Step 3: Patch napoleon baseline paths**

Baseline keys embed absolute paths like
`/Users/cmalek/src/workspace/bochord/bochord/...`.
After package mv, package segment is `wordwending` but workspace folder may still be `bochord` until the operator renames it.

```bash
# package segment only (workspace folder unchanged for now)
python - <<'PY'
from pathlib import Path
p = Path("doc/quality/napoleon_gate_baseline.json")
text = p.read_text()
text2 = text.replace("/bochord/bochord/", "/bochord/wordwending/")
# also catch any remaining /bochord/ as package-relative if present in path field only via replace above
if text2 == text:
    raise SystemExit("no path replacements made — inspect baseline format")
p.write_text(text2)
print("ok", text.count("bochord"), "->", text2.count("bochord"))
PY
```

If `make napoleon-gate` later disagrees, regenerate baseline with the project’s documented napoleon workflow rather than inventing keys.

- [ ] **Step 4: README + Sphinx branding (incl. macron forms)**

- Title `# wordwending`
- One-line product gloss (no *bōchord* etymology)
- Remove PyPI collision warning block about unrelated Books-backup package
- Clone/install/CLI examples use `wordwending`
- Docs URLs → `https://wordwending.readthedocs.io`
- Also scrub macron / display forms that miss the ASCII `rg` gate:

```bash
rg -n 'bōchord|Bōchord|\*bōchord\*' README.md doc/source/
```

Update any hits in `doc/source/index.rst`, `doc/source/overview/faq.rst`, and elsewhere under `doc/source/` to the new product name / gloss.
- [ ] **Step 5: Confirm bumpversion / manifest / sphinx**

```bash
rg -n 'bochord|BOCHORD' .bumpversion.cfg MANIFEST.in doc/source/conf.py Makefile pyproject.toml
```

Expected: no matches.

---

### Task 5: Reinstall editable env

**Files:**
- Regenerate: `uv.lock`, `*.egg-info` (via tool; do not hand-edit egg-info)

- [ ] **Step 1: Sync / reinstall**

```bash
source .venv/bin/activate
/usr/bin/cd /Users/cmalek/src/workspace/bochord
uv sync
```

Expected: success; `wordwending.egg-info` or equivalent present; old `bochord.egg-info` removable if leftover:

```bash
rm -rf bochord.egg-info
```

- [ ] **Step 2: Smoke import + CLI**

```bash
.venv/bin/python -c "import wordwending; print(wordwending.__file__)"
.venv/bin/wordwending --help
```

Expected: import path under `…/wordwending/`; help text prints.

---

### Task 6: Tests

**Files:**
- Modify as needed: `tests/**` (should already be covered by Task 3 replace; fix any stragglers)
- Especially: `tests/test_configuration.py`, `tests/test_cli_commands.py`, `tests/test_main.py`, `tests/conftest.py`

- [ ] **Step 1: Fix any remaining test assertions**

Search tests for old tokens:

```bash
rg -n 'bochord|BOCHORD|\.bochord' tests/
```

Expected: no matches. If any remain (e.g. odd fixtures), update to `wordwending` / `WORDWENDING_` / `.wordwending.toml`.

- [ ] **Step 2: Run full test suite**

```bash
source .venv/bin/activate
.venv/bin/pytest -q
```

Expected: PASS (same failures as pre-rename baseline only if pre-existing and unrelated — new rename failures must be fixed).

**Note:** Full suite is the gate (not only “rename-sensitive” files). CLI/settings/main are the highest-signal files if you need a fast loop first:

```bash
.venv/bin/pytest -q tests/test_main.py tests/test_configuration.py tests/test_cli_commands.py tests/test_cli_utils.py
```

Then run full suite before claiming done.

---

### Task 7: `rg` verification gate

**Files:** none (read-only check)

- [ ] **Step 1: Run allowlisted search (ASCII tokens)**

```bash
source .venv/bin/activate
/usr/bin/cd /Users/cmalek/src/workspace/bochord

rg -n 'bochord|BOCHORD' \
  --glob '!docs/superpowers/plans/**' \
  --glob '!docs/superpowers/specs/**' \
  --glob '!graphify-out/**' \
  --glob '!.venv/**' \
  --glob '!*.egg-info/**' \
  --glob '!.git/**' \
  --glob '!.mypy_cache/**' \
  --glob '!.pytest_cache/**' \
  --glob '!.ruff_cache/**' \
  --glob '!.worktrees/**' \
  --glob '!doc/quality/napoleon_gate_baseline.json'
```

Expected: **no output** (exit code 1 from rg = no matches = success).

**Note:** Exclude the napoleon baseline here. After Task 4 Step 3 it still contains workspace-folder `…/bochord/wordwending/…` paths until the operator renames the local folder (Task 11 Step 3). Scrubbing those early breaks `make napoleon-gate`.
- [ ] **Step 2: Macron / display-name sweep**

```bash
rg -n 'bōchord|Bōchord' \
  --glob '!docs/superpowers/plans/**' \
  --glob '!docs/superpowers/specs/**' \
  --glob '!graphify-out/**'
```

Expected: no matches.

If matches remain, fix them before continuing.
---

### Task 8: Quality gate + graphify

**Files:**
- Touch as needed for ruff/mypy/napoleon on Python sources
- Update: `graphify-out/` via tool

- [ ] **Step 1: ruff + mypy on package**

```bash
source .venv/bin/activate
.venv/bin/ruff check wordwending tests
.venv/bin/mypy wordwending
```

Expected: clean or only pre-existing unrelated issues (fix rename-caused ones).

- [ ] **Step 2: napoleon gate**

```bash
make napoleon-gate
```

Expected: pass vs updated baseline.

- [ ] **Step 3: graphify update**

```bash
graphify update .
```

Expected: graph refreshes under `graphify-out/` with `wordwending` paths.

---

### Task 9: Commit in-repo rename

**Files:** all in-repo rename changes

- [ ] **Step 1: Commit**

```bash
git status
git add -A
# review: do not stage secrets; skip unrelated dirty graphify noise if policy says so — prefer including graphify update from Task 8
git commit -m "$(cat <<'EOF'
rename: bochord → wordwending across package and docs

EOF
)"
```

Expected: commit succeeds; hooks pass (fix and new commit if hooks fail — do not `--no-verify`).

- [ ] **Step 2: Push branch before GitHub rename**

```bash
git push -u origin HEAD
```

Expected: remote branch exists under current repo name `bochord`. **Push before `gh repo rename`** so tracking survives the rename.

---

### Task 10: GitHub rename + URL sweep

**Files:**
- Possibly Modify: `pyproject.toml`, `README.md`, docs URLs if any still point at `github.com/cmalek/bochord`

- [ ] **Step 1: Rename GitHub repo**

```bash
gh repo rename wordwending --yes
```

Expected: repo becomes `cmalek/wordwending`; git remote URL updates or needs:

```bash
git remote -v
# if still old:
git remote set-url origin git@github.com:cmalek/wordwending.git
```

- [ ] **Step 2: Confirm no live GitHub old URLs in-scope**

```bash
rg -n 'github.com/cmalek/bochord|bochord.readthedocs' \
  --glob '!docs/superpowers/plans/**' \
  --glob '!docs/superpowers/specs/**' \
  --glob '!graphify-out/**'
```

Expected: no matches. If any, fix + commit:

```bash
git commit -am "$(cat <<'EOF'
docs: point URLs at wordwending GitHub/RTD hosts

EOF
)"
git push
```

---

### Task 11: Operator checklist (human)

Not agent-owned beyond documenting:

- [ ] **Step 1: ReadTheDocs** — rename project to `wordwending` so `https://wordwending.readthedocs.io` resolves; trigger a docs build.
- [ ] **Step 2: Local folder** — rename `…/workspace/bochord` → `…/workspace/wordwending`; reopen Cursor root.
- [ ] **Step 3: After local folder rename** — if napoleon baseline still embeds `/workspace/bochord/`, regenerate or sed workspace segment; re-run `make napoleon-gate`.
- [ ] **Step 4: Local config** — rename any `~/.bochord.toml` / `.bochord.toml` to `.wordwending.toml`; update shell env `BOCHORD_*` → `WORDWENDING_*`.

---

## Done criteria (from spec)

- `import wordwending` works
- `wordwending --help` works
- Task 7 `rg` gate clean
- Full pytest green for rename
- GitHub repo is `cmalek/wordwending`
- Operator items in Task 11 open until human completes them
