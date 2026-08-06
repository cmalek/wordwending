# Rename `bochord` → `wordwending` Design

Date: 2026-08-06
Repo: `/Users/cmalek/src/workspace/bochord`
Focus: One-shot project identity rename so the package can publish on PyPI
under a free name.

## Purpose

PyPI already has an unrelated package named `bochord` (iCloud Books backup).
This OCR project must rename to `wordwending` everywhere that defines product
identity, then rename the GitHub repository. ReadTheDocs is a manual follow-up
by the operator.

Target outcome:

- installable / importable as `wordwending`
- CLI entry point `wordwending`
- settings env prefix `WORDWENDING_`
- GitHub repo `cmalek/wordwending`
- live docs and ADRs use the new name
- no compatibility shims for the old name

## Locked Decisions

| Decision | Choice |
|---|---|
| New name | `wordwending` (confirmed free on PyPI at design time) |
| Scope | Full rename: package dir, imports, PyPI name, CLI, env prefix, GitHub, RTD (operator), local folder (operator) |
| Env prefix | Clean break: `BOCHORD_` → `WORDWENDING_` (no alias) |
| Docs churn | Rewrite live surface + Sphinx `doc/` (incl. ADRs/architecture). Leave `docs/superpowers/plans/` frozen |
| External services | Agent runs `gh repo rename` + in-repo URL updates. Operator renames RTD project in the UI |
| Approach | Big-bang on one branch (no phased dual-name state, no one-off rename script) |
| Compat | None: no dual CLI, no leftover `bochord` package, no env alias |

## Identity Map

| Kind | Old | New |
|---|---|---|
| PyPI / `[project].name` | `bochord` | `wordwending` |
| Import package directory | `bochord/` | `wordwending/` |
| CLI `[project.scripts]` | `bochord = "bochord.main:main"` | `wordwending = "wordwending.main:main"` |
| Settings `env_prefix` | `BOCHORD_` | `WORDWENDING_` |
| GitHub | `cmalek/bochord` | `cmalek/wordwending` |
| ReadTheDocs host | `bochord.readthedocs.io` | `wordwending.readthedocs.io` |
| Local workspace folder | `.../bochord` | `.../wordwending` |

## In Scope

- Package tree rename via `git mv bochord wordwending`
- Imports and string references in code, tests, fixtures
- `pyproject.toml` (name, scripts, urls, package/coverage lists)
- `uv.lock` refresh via sync/reinstall
- `.bumpversion.cfg` file paths
- `Makefile` `PACKAGE=`
- `MANIFEST.in`, `.readthedocs.yaml` if they name the package
- `AGENTS.md`, `CONTEXT.md`, `README.md` (drop PyPI collision warning; note new name)
- Sphinx tree under `doc/` including ADRs and architecture docs
- CI / GitHub workflow files under `.github/` if they mention the old name
- `graphify update .` after Python tree move
- `gh repo rename wordwending` and remaining GitHub URL fixes

## Out of Scope

- `docs/superpowers/plans/*` (historical archives; leave as-is)
- Rewriting other `docs/superpowers/specs/*` for the old name (this rename spec itself keeps historical `bochord` references; see `rg` allowlist)
- Publishing to PyPI (separate later task)
- Compatibility / migration layer for old name
- Rewriting or deleting `graphify-out/` by hand (regenerate with `graphify update`)
- Committing `.venv` / caches; operator reinstalls editable env after rename
- Operator’s local folder rename and Cursor workspace reopen (checklist item)

## Execution Order

1. Create feature branch from current HEAD.
2. `git mv bochord wordwending` (preserve history).
3. Mechanical replace on in-scope paths only:
   - `bochord` → `wordwending`
   - `BOCHORD_` → `WORDWENDING_`
   - GitHub and ReadTheDocs URLs to the new hosts
4. Hand-fix identity files that need more than blind replace:
   - `pyproject.toml`, `.bumpversion.cfg`, `Makefile`, `doc/source/conf.py`
   - README branding / install / CLI examples
5. Reinstall editable package (`uv sync` or equivalent) so CLI and imports resolve.
6. Verification gate (after reinstall, before `graphify update`):
   - `rg` for leftover `bochord` / `BOCHORD_` with the allowlist below
   - `wordwending --help`
   - rename-sensitive tests (CLI, settings/config, main) via project pytest
7. `graphify update .` (graph artifacts may temporarily still mention old paths until update; not part of step-6 gate)
8. Commit in-repo rename.
9. `gh repo rename wordwending`, push, fix any remaining GitHub URLs.
10. Operator checklist: rename RTD project; rename local workspace folder; reopen IDE root if needed.

## `rg` Allowlist (verification exclusions)

Matches of `bochord` / `BOCHORD_` are **allowed** only under:

- `docs/superpowers/plans/**` — frozen historical plans
- `docs/superpowers/specs/**` — design specs that document the rename (including this file)
- `graphify-out/**` — generated; refreshed by `graphify update .`
- `.venv/**`, `*.egg-info/**`, `.mypy_cache/**`, `.pytest_cache/**`, `.ruff_cache/**` — local/generated

Everything else in the repo must be clean. Search case-sensitive for `bochord` and `BOCHORD_`; title-case `Bochord` is not expected and is not a separate requirement.

## Risks

| Risk | Mitigation |
|---|---|
| Missed fixture / path string still says `bochord` | `rg` allowlist gate before merge |
| Editable install stale after `git mv` | Reinstall before tests |
| GitHub rename breaks old clone URLs | Expected; remotes update via `gh`; document in cutover |
| RTD 404 until operator renames | README points at new host; checklist item explicit |
| Local folder still named `bochord` | Harmless until operator renames; package name independent |

## Done Criteria

- `import wordwending` succeeds
- `wordwending --help` succeeds
- No `bochord` / `BOCHORD_` outside the `rg` allowlist above
- Rename-sensitive tests pass
- GitHub repository is `cmalek/wordwending`
- Open operator items: RTD rename, local folder rename

## Non-Goals (Ponytail)

- No rename script artifact
- No two-phase “package renamed, repo still bochord” PR pair
- No env/CLI aliases “for one release”
- No mass rewrite of historical superpowers plans
