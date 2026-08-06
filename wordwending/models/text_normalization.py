# Copyright (C) 2026 Chris Malek.
"""Text normalization policy and line-join contract models."""

from __future__ import annotations

from enum import StrEnum

from pydantic import model_validator

from wordwending.models.ocr import SchemaModel


class UnicodeNormalizationForm(StrEnum):
    """Unicode normalization form applied to diplomatic text."""

    #: Canonical composition; v1 ships NFC only.
    NFC = "NFC"


class NoteMarkerNormalizedForm(StrEnum):
    """How inline note markers appear in normalized text."""

    #: Keep marker graphemes in normalized text.
    RETAIN = "retain"
    #: Replace markers with a documented placeholder token, e.g. ``[n]``.
    PLACEHOLDER = "placeholder"


class SuperscriptNormalizedForm(StrEnum):
    """How superscript characters appear in normalized text."""

    #: Keep superscript characters as-is.
    RETAIN = "retain"
    #: Map known superscript digits and letters to baseline equivalents.
    FLATTEN = "flatten"


class LineJoinKind(StrEnum):
    """How adjacent lines were joined when building normalized text."""

    #: Lines were concatenated without heuristic repair.
    DIRECT = "direct"
    #: A trailing hyphen on the left line was removed during join.
    HYPHEN_JOIN = "hyphen-join"
    #: A heuristic join rule selected the join boundary.
    HEURISTIC = "heuristic"
    #: A human corrected the join decision.
    HUMAN_CORRECTED = "human-corrected"


class LineJoinRecord(SchemaModel):
    """Audit record for one line join applied under a normalization policy."""

    #: Identifier of the left line in the join pair.
    left_line_id: str
    #: Identifier of the right line in the join pair.
    right_line_id: str
    #: Join strategy that produced the normalized boundary.
    join_kind: LineJoinKind
    #: Whether a trailing hyphen was removed from the left line.
    removed_hyphen: bool = False
    #: Normalization policy identifier governing this join.
    policy_id: str


class TextNormalizationPolicy(SchemaModel):
    """Versioned, deterministic text normalization policy."""

    #: Stable policy identifier for persisted normalization settings.
    policy_id: str
    #: Semantic version of the normalization contract.
    version: str
    #: Unicode normalization form applied to diplomatic text.
    unicode_form: UnicodeNormalizationForm = UnicodeNormalizationForm.NFC
    #: Collapse internal whitespace runs to single spaces.
    collapse_whitespace: bool = True
    #: Strip leading and trailing whitespace from normalized text.
    strip: bool = True
    #: How inline note markers appear in normalized output.
    note_marker_form: NoteMarkerNormalizedForm = NoteMarkerNormalizedForm.RETAIN
    #: How superscript characters appear in normalized output.
    superscript_form: SuperscriptNormalizedForm = SuperscriptNormalizedForm.RETAIN
    #: Join words split across a line-ending hyphen.
    join_hyphen_at_line_end: bool = True
    #: Preserve historical character forms rather than modernizing them.
    preserve_historical_characters: bool = True

    @model_validator(mode="after")
    def reject_historical_modernization(self) -> TextNormalizationPolicy:
        """
        Reject v1 policies that disable historical character preservation.

        Returns:
            The validated normalization policy.

        Raises:
            ValueError: If ``preserve_historical_characters`` is ``False``.

        """
        if not self.preserve_historical_characters:
            msg = "preserve_historical_characters=False is not supported in v1"
            raise ValueError(msg)
        return self
