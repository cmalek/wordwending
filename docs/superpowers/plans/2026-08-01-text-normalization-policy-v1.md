# Text Normalization Policy v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish the exact, deterministic `text-norm-v1` behavior implemented by `TextNormalizer`, so downstream users never treat normalized text as independently editable evidence.

**Architecture:** This is a documentation-only contract stage after Spec 0008. Derive every rule from `TextNormalizationPolicy` and `TextNormalizer`; do not add behavior, dependencies, a second normalizer, or retrieval fields. `text_diplomatic` stays authoritative and `text_normalized` remains a derived view.

**Tech Stack:** reStructuredText, Sphinx, existing pytest normalization fixture. No new dependency.

**Sequence:** 3 of 5. Start only after Spec 0008 plan passes final review; finish before Spec 0009.

**Governing Specs:** Spec 0008 (dual-text contract) and `doc/source/architecture/text_normalization_policy_v1.rst` (normative v1 rules).

## Global Constraints

- Document policy id `text-norm-v1`, version `1`, Unicode NFC, whitespace collapse, stripping, retained note markers and superscripts, and historical-character preservation.
- Historical characters (`æ`, `ǣ`, `þ`, `ð`, `œ`, macron vowels) must never be modernized or expanded in v1.
- Document `PLACEHOLDER` only for `*`, `†`, `‡`, `¹`, `²`, `³`; replacement is `[n]` and applies only to note normalization.
- Document transform order exactly: Unicode, whitespace, strip, superscript flattening, then note-marker replacement.
- Document line-join removal only for ASCII hyphen-minus or U+00AD, enabled policy, and `hyphen-join` or `human-corrected` join kind.
- State that joins return `LineJoinRecord` and are not persisted on page-graph objects in v1.
- `correct_text` edits diplomatic text only; normalized text is regenerated.
- No new Python behavior, retrieval fields, lemma normalization, linguistic modernization, or LLM rewriting.
- Before Python commands: `source .venv/bin/activate`.

## Subagent Model Policy

- Implementation tasks may use only **Cursor Grok 4.5** (`cursor-grok-4.5`) or **Composer 2.5 Fast** (`composer-2.5-fast`). No other implementer models.
- Use Composer 2.5 Fast for this mechanical documentation task; use Cursor Grok 4.5 only if code-to-contract reconciliation needs judgment.
- Reviews may use any appropriate model; use a fresh reviewer for Spec compliance and a final Sphinx/content review.
- Give implementers only generated task brief, listed files, and prior-stage interface decisions.

For every task, use this serial Superpowers loop:

1. Implementer (Composer 2.5 Fast or Cursor Grok 4.5) implements, runs listed checks, self-reviews, and commits.
2. Spec-compliance reviewer (any appropriate model) reviews without editing.
3. Same implementer fixes; re-review until approved.
4. Fresh code-quality reviewer (any appropriate model) reviews without editing.
5. Same fix/re-review loop for quality findings.

After the last task, a fresh reviewer audits this plan. Do not begin Spec 0009 while either review has open findings.

## Existing Baseline

- Spec 0008 provides `TextNormalizationPolicy`, `TextNormalizer`, fixture cases, and `DEFAULT_TEXT_NORMALIZATION_POLICY`.
- `doc/source/architecture/index.rst` already includes `text_normalization_policy_v1`.
- This stage records the code contract; it does not change normalization behavior.

---

## File Map

- Modify: `doc/source/architecture/text_normalization_policy_v1.rst` — normative human-readable v1 policy.

### Task 1: Publish and Freeze `text-norm-v1`

**Files:**

- Modify: `doc/source/architecture/text_normalization_policy_v1.rst`

**Interfaces:**

```python
DEFAULT_TEXT_NORMALIZATION_POLICY = TextNormalizationPolicy(
    policy_id="text-norm-v1",
    version="1",
)

TextNormalizer.normalize_span_text(text_diplomatic: str) -> str
TextNormalizer.normalize_note_text(text_diplomatic: str) -> str
TextNormalizer.join_line_texts(...) -> tuple[str, LineJoinRecord]
```

- [x] **Step 1: Confirm existing policy identity test**

```bash
source .venv/bin/activate
pytest tests/test_text_normalization.py::test_default_text_normalization_policy_matches_v1_contract -v
```

Expected: PASS. The test is established by Spec 0008 and anchors the document's policy id, version, NFC, and preservation contract.

- [x] **Step 2: Write normative policy document**

Maintain these sections with these exact rules:

```rst
Default Policy
==============

``DEFAULT_TEXT_NORMALIZATION_POLICY`` uses ``policy_id`` ``text-norm-v1``,
``version`` ``1``, NFC, whitespace collapse, stripping, retained note markers,
retained superscripts, and historical-character preservation.

Transform Order
===============

Apply NFC, collapse whitespace, strip, flatten superscripts when configured,
then replace note markers when configured. ``x¹*`` therefore becomes
``x1[n]`` under both flattening and placeholder modes.
```

Add sections named `Unicode Normalization`, `Whitespace`, `Historical Characters`,
`Note Markers`, `Superscript`, `Line Joins`, and `Dual Text Contract`. State exact
marker and line-join limits from Global Constraints. Do not list the full
implementation superscript table; document its fixed-table behavior instead.

- [x] **Step 3: Verify fixture behavior and Sphinx build**

```bash
source .venv/bin/activate
pytest tests/test_text_normalization.py -q
make docs
```

Expected: PASS; documentation builds without warnings treated as errors by project configuration.

- [x] **Step 4: Commit**

```bash
git add doc/source/architecture/text_normalization_policy_v1.rst
git commit -m "docs: define text normalization policy v1"
```

## Final Review Focus

- Every documented transformation matches `TextNormalizer` and fixture cases.
- Transform order explains superscript marker overlap correctly.
- Document never implies operators may edit normalized text independently.
- No behavior or scope from Spec 0009 merge is introduced.

## Cost Stop

Stop after policy documentation and one identity regression test. No code refactor, retrieval normalization, persisted join provenance, or additional policy versions.
