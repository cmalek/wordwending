# bochord

`bochord` (from *bōchord*, “book treasure-hoard”) is an early, evolving Python
CLI for high-fidelity OCR of Old English / Anglo-Saxon source material. It is
built for scholars first: preserve philological signal in the page image, keep
rebuildable witnesses, then derive structured and Markdown views. Agent-ready
RAG exports are a payoff of that fidelity, not a substitute for it.

> **Early software.** Commands, bundle layout, and export surfaces are still
> evolving. Prefer the published docs over informal notes when they diverge.

## Problem

OCR that “works” still fails twice: it drops typography, notes, and layout that
philologists need, and it leaves agents without citable evidence of what the
page actually showed.

## How

Multi-pass, image-first OCR → witness-preserving bundles → structured JSON, RAG
chunks, and evidence-preserving Markdown. Hosted runners do inference; the
laptop prepares, validates, stores, evaluates, and exports.

## Why

Fidelity before cleverness. Raw pass artifacts stay intact so derived graphs and
exports remain rebuildable. Humans correct via overlays and review tasks—not by
silently editing OCR text into a new “truth.”

## Core Features

**Image-first OCR orchestration**

- Multi-pass workflows for difficult historical PDFs and page images
- Separate text, structure, typography, note-linkage, and evaluation concerns

**Witness-preserving bundle outputs**

- Raw pass artifacts remain intact
- Derived page graphs, overlays, and exports remain rebuildable

**Reviewable structured exports**

- Full-fidelity JSON for deterministic software
- Evidence-preserving Markdown and RAG-oriented JSON for agents

## Documentation

Published docs: <https://bochord.readthedocs.io>

End-to-end operator walkthrough (prepare → run → provisional export, plus what
is still missing):
[From source to Markdown](https://bochord.readthedocs.io/en/latest/runbook/from_source_to_markdown.html)

## Requirements

- Python **3.13** or later
- [`uv`](https://docs.astral.sh/uv/)
- `git`

## Installation

Install from source. This project is early; the documented path is clone +
`uv`, not a published package for this tool.

> **Warning:** The PyPI project name `bochord` may refer to an **unrelated**
> Books-backup package. Do **not** `pip install bochord` (or
> `uv tool install bochord` / `pipx install bochord`) expecting this OCR tool
> until this project's own packaging story changes.

```bash
git clone https://github.com/cmalek/bochord.git
cd bochord
# Install uv if needed: https://docs.astral.sh/uv/getting-started/installation/
uv sync
source .venv/bin/activate
bochord --help
```

## Quick Start

```bash
source .venv/bin/activate
bochord --help
bochord version
```

For the full spine (inputs, prepare/run, provisional export when you already
have a `DocumentBundle`, and documented gaps), see the
[from source to Markdown](https://bochord.readthedocs.io/en/latest/runbook/from_source_to_markdown.html)
guide on Read the Docs.

## Commands

| Command | Role |
| --- | --- |
| `version` | Installed package and dependency versions |
| `settings` | Effective configuration (table / json / text) |
| `prepare` | Acquire and prepare source pages into a bundle layout |
| `run` | Execute prepared artifacts against one hosted olmOCR runner |
| `eval` | Score one predicted page against gold annotations |
| `eval-cohorts` | Summarize page evaluations into fixed cohort views |
| `export` | Derive bundle / RAG / Markdown exports from a DocumentBundle |

There is no assemble/merge or review CLI yet.

## Common Use Cases

**Research and compare OCR passes**

- Run competing hosted engines on difficult pages
- Evaluate text, structure, typography, and note linkage separately

**Produce reviewable bundle artifacts**

- Preserve footnotes, italic, bold, and superscript signals
- Hand off evidence-rich outputs to downstream Old English tooling

**Export provisional Markdown and RAG views**

- When a `DocumentBundle` exists, `bochord export` writes derived
  `document.md` and retrieval artifacts (Markdown is not the source of truth)
