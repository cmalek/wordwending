# Copyright (C) 2026 Chris Malek.
from __future__ import annotations


class BochordError(Exception):
    """Base exception for all bochord errors."""


class ConfigurationError(BochordError):
    """Raised when settings or configuration fails."""


class FileError(BochordError):
    """Raised when file I/O operations fail."""


class RunnerEndpointUnavailable(BochordError):
    """Raised when a hosted runner endpoint is not ready for inference."""
