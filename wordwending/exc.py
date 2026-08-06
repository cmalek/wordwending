# Copyright (C) 2026 Chris Malek.
from __future__ import annotations


class WordwendingError(Exception):
    """Base exception for all wordwending errors."""


class ConfigurationError(WordwendingError):
    """Raised when settings or configuration fails."""


class FileError(WordwendingError):
    """Raised when file I/O operations fail."""


class RunnerEndpointUnavailable(WordwendingError):
    """Raised when a hosted runner endpoint is not ready for inference."""
