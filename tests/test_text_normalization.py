# Copyright (C) 2026 Chris Malek.
"""Tests for text normalization policy models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from bochord.models import TextNormalizationPolicy, UnicodeNormalizationForm


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
