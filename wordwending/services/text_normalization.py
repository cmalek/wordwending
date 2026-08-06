# Copyright (C) 2026 Chris Malek.
"""Deterministic diplomatic-to-normalized text transformation."""

from __future__ import annotations

import re
import unicodedata

from wordwending.models import (
    BundlePage,
    LineJoinKind,
    LineJoinRecord,
    NoteMarkerNormalizedForm,
    NoteRecord,
    SpanRecord,
    SuperscriptNormalizedForm,
    TextNormalizationPolicy,
)

#: Default v1 normalization policy for page-graph regeneration.
DEFAULT_TEXT_NORMALIZATION_POLICY = TextNormalizationPolicy(
    policy_id="text-norm-v1",
    version="1",
)

#: Inline note-marker codepoints replaced under ``PLACEHOLDER`` policy.
_NOTE_MARKER_CODEPOINTS = frozenset("*†‡¹²³")

#: Unicode superscript digits and letters mapped to baseline equivalents.
_SUPERSCRIPT_TRANSLATION = str.maketrans(
    {
        "⁰": "0",
        "¹": "1",
        "²": "2",
        "³": "3",
        "⁴": "4",
        "⁵": "5",
        "⁶": "6",
        "⁷": "7",
        "⁸": "8",
        "⁹": "9",
        "⁺": "+",
        "⁻": "-",
        "⁼": "=",
        "⁽": "(",
        "⁾": ")",
        "ⁿ": "n",
        "ⁱ": "i",
        "ᵃ": "a",
        "ᵇ": "b",
        "ᶜ": "c",
        "ᵈ": "d",
        "ᵉ": "e",
        "ᶠ": "f",
        "ᵍ": "g",
        "ʰ": "h",
        "ʲ": "j",
        "ᵏ": "k",
        "ˡ": "l",
        "ᵐ": "m",
        "ᵒ": "o",
        "ᵖ": "p",
        "ʳ": "r",
        "ˢ": "s",
        "ᵗ": "t",
        "ᵘ": "u",
        "ᵛ": "v",
        "ʷ": "w",
        "ˣ": "x",
        "ʸ": "y",
        "ᶻ": "z",
    }
)

#: Trailing hyphen codepoints removed during explicit hyphen joins.
_HYPHEN_JOIN_SUFFIXES = ("-", "\u00ad")


class TextNormalizer:
    """
    Deterministic diplomatic → normalized text transform.

    Args:
        policy: Normalization settings governing every transform.

    """

    def __init__(self, policy: TextNormalizationPolicy) -> None:
        """
        Initialize the normalizer with a versioned policy.

        Args:
            policy: Normalization settings governing every transform.

        """
        #: Normalization settings governing every transform.
        self.policy = policy

    def normalize_span_text(self, text_diplomatic: str) -> str:
        """
        Normalize span diplomatic text without note-marker rewriting.

        Args:
            text_diplomatic: Evidence-preserving span text.

        Returns:
            Deterministic normalized text for spans.

        """
        return self._normalize_text(text_diplomatic, apply_note_markers=False)

    def normalize_note_text(self, text_diplomatic: str) -> str:
        """
        Normalize note diplomatic text, including note-marker policy.

        Args:
            text_diplomatic: Evidence-preserving note text.

        Returns:
            Deterministic normalized text for notes.

        """
        return self._normalize_text(text_diplomatic, apply_note_markers=True)

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
        Join two line texts and return normalized output plus provenance.

        Hyphen-at-line-end removal applies only when ``join_hyphen_at_line_end``
        is enabled and ``join_kind`` is ``HYPHEN_JOIN`` or ``HUMAN_CORRECTED``,
        and the left line ends with ASCII hyphen-minus or soft hyphen.

        Args:
            left_diplomatic: Diplomatic text for the left line.
            right_diplomatic: Diplomatic text for the right line.

        Keyword Args:
            left_line_id: Stable identifier for the left line.
            right_line_id: Stable identifier for the right line.
            join_kind: Join strategy applied at the line boundary.

        Returns:
            Normalized joined text and a ``LineJoinRecord`` audit value.

        """
        left_text = left_diplomatic
        removed_hyphen = False
        if (
            self.policy.join_hyphen_at_line_end
            and join_kind in {LineJoinKind.HYPHEN_JOIN, LineJoinKind.HUMAN_CORRECTED}
        ):
            for suffix in _HYPHEN_JOIN_SUFFIXES:
                if left_text.endswith(suffix):
                    left_text = left_text[: -len(suffix)]
                    removed_hyphen = True
                    break

        joined = left_text + right_diplomatic
        normalized = self.normalize_span_text(joined)
        record = LineJoinRecord(
            left_line_id=left_line_id,
            right_line_id=right_line_id,
            join_kind=join_kind,
            removed_hyphen=removed_hyphen,
            policy_id=self.policy.policy_id,
        )
        return normalized, record

    def apply_to_span(self, span: SpanRecord) -> SpanRecord:
        """
        Return a span copy with ``text_normalized`` regenerated.

        Args:
            span: Accepted span whose diplomatic text is authoritative.

        Returns:
            Copy with normalized text filled from diplomatic text.

        """
        return span.model_copy(
            update={
                "text_normalized": self.normalize_span_text(span.text_diplomatic),
            }
        )

    def apply_to_note(self, note: NoteRecord) -> NoteRecord:
        """
        Return a note copy with ``text_normalized`` regenerated.

        Args:
            note: Accepted note whose diplomatic text is authoritative.

        Returns:
            Copy with normalized text filled from diplomatic text.

        """
        return note.model_copy(
            update={
                "text_normalized": self.normalize_note_text(note.text_diplomatic),
            }
        )

    def apply_to_page(self, page: BundlePage) -> BundlePage:
        """
        Normalize every span and note while leaving diplomatic text unchanged.

        Args:
            page: Accepted page graph to normalize in place logically.

        Returns:
            Copy with regenerated normalized text on spans and notes.

        """
        return page.model_copy(
            update={
                "spans": [self.apply_to_span(span) for span in page.spans],
                "notes": [self.apply_to_note(note) for note in page.notes],
            }
        )

    def _normalize_text(
        self,
        text_diplomatic: str,
        *,
        apply_note_markers: bool,
    ) -> str:
        """
        Apply policy-ordered Unicode, whitespace, and optional marker rules.

        Args:
            text_diplomatic: Evidence-preserving input text.

        Keyword Args:
            apply_note_markers: Whether to apply note-marker placeholder rules.

        Returns:
            Normalized text after the configured transforms.

        """
        text = unicodedata.normalize(self.policy.unicode_form.value, text_diplomatic)
        if self.policy.collapse_whitespace:
            text = re.sub(r"\s+", " ", text)
        if self.policy.strip:
            text = text.strip()
        text = self._apply_superscript(text)
        if apply_note_markers:
            text = self._apply_note_markers(text)
        return text

    def _apply_superscript(self, text: str) -> str:
        """
        Map known superscript codepoints when flattening is enabled.

        Args:
            text: Text after Unicode and whitespace normalization.

        Returns:
            Text with known superscript codepoints flattened when configured.

        """
        if self.policy.superscript_form is SuperscriptNormalizedForm.RETAIN:
            return text
        return text.translate(_SUPERSCRIPT_TRANSLATION)

    def _apply_note_markers(self, text: str) -> str:
        """
        Replace documented marker codepoints when placeholder mode is enabled.

        Args:
            text: Text after earlier normalization stages.

        Returns:
            Text with documented note markers replaced by ``[n]`` when configured.

        """
        if self.policy.note_marker_form is NoteMarkerNormalizedForm.RETAIN:
            return text
        return "".join(
            "[n]" if character in _NOTE_MARKER_CODEPOINTS else character
            for character in text
        )
