# Spec 0008 Text and Normalization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a documented, deterministic dual-text normalization pipeline that fills `text_normalized` from `text_diplomatic` without silently damaging philological evidence.

**Architecture:** Add a versioned `TextNormalizationPolicy` model and one stateless `TextNormalizer` service using stdlib `unicodedata` only. Apply at span/note (and optional line/region) boundaries. Human `correct_text` edits diplomatic text; normalized text is regenerated, never independently edited. Defer retrieval-only fields (`text_search`, `text_ascii_fallback`) to Spec 0006 exports.

**Tech Stack:** Python 3.13, Pydantic 2, stdlib `unicodedata`/`re`, existing `regex` only if grapheme splits are needed, pytest. No new dependency (`unicodedata2` rejected; stdlib NFC is enough for v1).

**Sequence:** 2 of 4. Start only after Spec 0013 plan passes final review.

**Governing ADR:** ADR 0003 (page graph text objects) and ADR 0004 (derived layers stay rebuildable from evidence).

## Global Constraints

- Dual fields: `text_diplomatic` (evidence) and `text_normalized` (deterministic convenience).
- Never silently expand ligatures, modernize orthography, or flatten thorn/eth/macrons in either primary field.
- Default: `æ/ǣ/þ/ð` stay themselves in both diplomatic and normalized text.
- Normalization is rule-based and versioned via `policy_id` + `version` (no separate digest field in v1).
- `correct_text` targets diplomatic text only; regenerate normalized afterward.
- No LLM rewriting, lemma normalization, or automatic modernization.
- Retrieval fields are out of scope here.
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

- `SpanRecord` / `NoteRecord` / `GoldTextSpan` already have `text_diplomatic` + optional `text_normalized`.
- Evaluation already NFC-normalizes for scoring graphemes; that is scoring prep, not the Spec 0008 pipeline.
- `GoldLineJoin` exists for evaluation; accepted graph lines have `joins_to_line_id` but no join-provenance enum yet.
- No `TextNormalizer` service exists.

---

## File Map

- Create: `bochord/models/text_normalization.py` — policy + join provenance enums/models.
- Modify: `bochord/models/__init__.py` — export new contracts.
- Create: `bochord/services/text_normalization.py` — `TextNormalizer`.
- Modify: `bochord/services/page_interchange.py` — after diplomatic `correct_text` merge, regenerate `text_normalized`.
- Create: `tests/test_text_normalization.py`
- Modify: `tests/test_page_interchange.py` — regeneration after correction.
- Create: `tests/fixtures/text_normalization/cases.json` — deterministic cases.
- Create: `doc/source/architecture/text_normalization_policy_v1.rst` — human-readable rule table (docs-only; keep short).

### Task 1: Freeze Normalization Policy Models

**Files:**

- Create: `bochord/models/text_normalization.py`
- Modify: `bochord/models/__init__.py`
- Create: `tests/test_text_normalization.py`

**Interfaces:**

```python
class UnicodeNormalizationForm(StrEnum):
    NFC = "NFC"
    # v1 ships NFC only; enum documents the policy knob


class NoteMarkerNormalizedForm(StrEnum):
    RETAIN = "retain"          # keep marker graphemes in normalized text
    PLACEHOLDER = "placeholder"  # replace with documented token, e.g. "[n]"


class SuperscriptNormalizedForm(StrEnum):
    RETAIN = "retain"          # keep superscript characters as-is
    FLATTEN = "flatten"        # map known superscript digits/letters to baseline


class LineJoinKind(StrEnum):
    DIRECT = "direct"
    HYPHEN_JOIN = "hyphen-join"
    HEURISTIC = "heuristic"
    HUMAN_CORRECTED = "human-corrected"


class LineJoinRecord(SchemaModel):
    left_line_id: str
    right_line_id: str
    join_kind: LineJoinKind
    removed_hyphen: bool = False
    policy_id: str


class TextNormalizationPolicy(SchemaModel):
    policy_id: str
    version: str
    unicode_form: UnicodeNormalizationForm = UnicodeNormalizationForm.NFC
    collapse_whitespace: bool = True
    strip: bool = True
    note_marker_form: NoteMarkerNormalizedForm = NoteMarkerNormalizedForm.RETAIN
    superscript_form: SuperscriptNormalizedForm = SuperscriptNormalizedForm.RETAIN
    join_hyphen_at_line_end: bool = True
    preserve_historical_characters: bool = True  # must stay True in v1 defaults
```

Reject `preserve_historical_characters=False` in v1 validator (YAGNI: no modernization path yet).

- [ ] **Step 1: Write failing model tests**

```python
def test_default_policy_preserves_historical_characters() -> None:
    policy = TextNormalizationPolicy(policy_id="text-norm-v1", version="1")
    assert policy.preserve_historical_characters is True
    assert policy.unicode_form is UnicodeNormalizationForm.NFC


def test_policy_rejects_historical_modernization_flag() -> None:
    with pytest.raises(ValidationError):
        TextNormalizationPolicy(
            policy_id="bad",
            version="1",
            preserve_historical_characters=False,
        )
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
source .venv/bin/activate
pytest tests/test_text_normalization.py -v
```

Expected: FAIL (module missing).

- [ ] **Step 3: Implement models + exports**

- [ ] **Step 4: Run tests to verify they pass**

- [ ] **Step 5: Quality gate + commit**

```bash
ruff check bochord/models/text_normalization.py bochord/models/__init__.py tests/test_text_normalization.py
mypy bochord/models/text_normalization.py
make napoleon-gate
pytest tests/test_text_normalization.py -q
git add bochord/models/text_normalization.py bochord/models/__init__.py tests/test_text_normalization.py
git commit -m "$(cat <<'EOF'
feat: add text normalization policy models

EOF
)"
```

### Task 2: Implement TextNormalizer

**Files:**

- Create: `bochord/services/text_normalization.py`
- Modify: `tests/test_text_normalization.py`
- Create: `tests/fixtures/text_normalization/cases.json`
- Create: `doc/source/architecture/text_normalization_policy_v1.rst`

**Interfaces:**

```python
# Module-level default lives in bochord/services/text_normalization.py
DEFAULT_TEXT_NORMALIZATION_POLICY = TextNormalizationPolicy(
    policy_id="text-norm-v1",
    version="1",
)


class TextNormalizer:
    """Deterministic diplomatic → normalized text transform."""

    def __init__(self, policy: TextNormalizationPolicy) -> None:
        self.policy = policy

    def normalize_span_text(self, text_diplomatic: str) -> str:
        """NFC + whitespace + optional superscript flatten. No note-marker rewrite."""

    def normalize_note_text(self, text_diplomatic: str) -> str:
        """Same as span, then apply ``note_marker_form`` (RETAIN/PLACEHOLDER)."""

    def join_line_texts(
        self,
        left_diplomatic: str,
        right_diplomatic: str,
        *,
        left_line_id: str,
        right_line_id: str,
        join_kind: LineJoinKind,
    ) -> tuple[str, LineJoinRecord]:
        """
        Return normalized joined text plus join provenance.

        Caller supplies line ids; record.policy_id comes from self.policy.
        Hyphen-at-line-end joins only when ``join_kind`` is HYPHEN_JOIN or
        HUMAN_CORRECTED and left ends with ASCII hyphen-minus or soft hyphen.
        """

    def apply_to_span(self, span: SpanRecord) -> SpanRecord:
        """Return copy with ``text_normalized`` filled from diplomatic."""

    def apply_to_note(self, note: NoteRecord) -> NoteRecord:
        ...

    def apply_to_page(self, page: BundlePage) -> BundlePage:
        """Normalize every span and note; leave diplomatic unchanged."""
```

`LineJoinRecord` is a return-value helper for chunk/region join callers. Do **not** persist it onto `BundlePage` / RAG chunks in this plan (deferred; Cost Stop).

Documented v1 rules (also in the rst doc):

1. Unicode: `unicodedata.normalize("NFC", text)`.
2. Whitespace: collapse runs of Unicode whitespace to single ASCII space; optional strip.
3. Historical chars: never rewrite `æ ǣ þ ð œ` or macron vowels.
4. Note markers: `RETAIN` keeps text; `PLACEHOLDER` replaces only codepoints in a small documented set (e.g. `*†‡¹²³`) with `[n]` — do not invent linguistic analysis.
5. Superscript: `RETAIN` default; `FLATTEN` maps only a fixed table of Unicode superscript digits/letters.
6. Line joins: do not erase line provenance on spans; joining is only via `join_line_texts` for chunk/region convenience callers. Hyphen removal only under explicit join kind.

Fixture `cases.json` rows: input diplomatic, policy overrides, expected normalized.

- [ ] **Step 1: Write failing service tests from fixture cases**

Include at least:

- macron + thorn + eth + æ preserved under NFC + whitespace collapse
- multi-space / tab / newline collapsed
- soft hyphen + hyphen-join removes one end hyphen
- direct join keeps hyphen characters unchanged
- placeholder note-marker form
- flatten superscript digits
- `apply_to_page` leaves diplomatic identical

- [ ] **Step 2: Run tests to verify they fail**

- [ ] **Step 3: Implement `TextNormalizer` + short policy rst**

Add rst to architecture toctree if one already lists sibling policy docs; otherwise leave unlinked and note path in commit message (do not invent large docs scaffolding).

- [ ] **Step 4: Run tests to verify they pass**

- [ ] **Step 5: Quality gate + commit**

```bash
git commit -m "$(cat <<'EOF'
feat: add deterministic text normalizer

EOF
)"
```

### Task 3: Regenerate Normalized Text After Diplomatic Correction

**Files:**

- Modify: `bochord/services/page_interchange.py`
- Modify: `tests/test_page_interchange.py`

**Interfaces:**

When `_merge_span` (or equivalent) updates `text_diplomatic` from PAGE `Unicode`, call `TextNormalizer(...).apply_to_span` so `text_normalized` is regenerated. Do not accept independent normalized edits from interchange.

Import `DEFAULT_TEXT_NORMALIZATION_POLICY` from `bochord.services.text_normalization` (defined in Task 2). Do not redefine it in page_interchange.

- [ ] **Step 1: Write failing interchange test**

```python
def test_import_correct_text_regenerates_normalized() -> None:
    # export page, mutate PAGE Unicode for one span, import
    # assert span.text_diplomatic == corrected
    # assert span.text_normalized == TextNormalizer(
    #     DEFAULT_TEXT_NORMALIZATION_POLICY
    # ).normalize_span_text(corrected)
```

- [ ] **Step 2: Run test to verify it fails**

- [ ] **Step 3: Wire regenerator into merge path**

`PageXmlInterchangeService` currently has **no** `__init__`. Add a new optional constructor (not an extension of an existing one) for testability:

```python
from bochord.services.text_normalization import (
    DEFAULT_TEXT_NORMALIZATION_POLICY,
    TextNormalizer,
)

class PageXmlInterchangeService:
    def __init__(
        self,
        text_normalizer: TextNormalizer | None = None,
    ) -> None:
        self._text_normalizer = text_normalizer or TextNormalizer(
            DEFAULT_TEXT_NORMALIZATION_POLICY
        )
```

Keep existing call sites working: default ctor args mean `PageXmlInterchangeService()` still valid.

- [ ] **Step 4: Run tests to verify they pass**

- [ ] **Step 5: Quality gate + commit**

```bash
git commit -m "$(cat <<'EOF'
fix: regenerate normalized text after diplomatic correction

EOF
)"
```

## Final Review Focus

- Both primary fields exist and diplomatic is never overwritten by normalizer.
- All six Spec 0008 policy areas are explicit in code + rst.
- Historical characters preserved.
- No retrieval-only fields added to span/note.
- No linguistic/LLM modernization.
- ADR 0004: normalized layer remains regenerable from diplomatic + policy.

## Cost Stop

Stop after policy + normalizer + correction regeneration. No RAG `text_search` fields, no persisting `LineJoinRecord` onto the page graph/chunks, no merge service, no bundle writer, no lemma/modernization options.
