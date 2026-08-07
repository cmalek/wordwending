# Copyright (C) 2026 Chris Malek.
"""Optional live Hugging Face endpoint lifecycle integration tests."""

from __future__ import annotations

import pytest


@pytest.mark.integration
def test_live_endpoint_lifecycle_smoke() -> None:
    pytest.skip("Live HF Inference Endpoint create/pause/delete — enable with credentials")
