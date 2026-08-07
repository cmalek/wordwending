# Copyright (C) 2026 Chris Malek.
"""Resolve hosted PassRunner adapter classes by stable runner_id."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeAlias

from wordwending.services.kraken_runner import HuggingFaceKrakenRunner
from wordwending.services.olmocr_runner import HuggingFaceOlmocrRunner

if TYPE_CHECKING:
    from collections.abc import Mapping

#: Constructable hosted adapter class whose instances satisfy ``PassRunner``.
#: Not ``type[PassRunner]``: Protocol types are not constructable under mypy.
PassRunnerClass: TypeAlias = type[Any]


class UnknownPassRunnerError(LookupError):
    """Raised when ``runner_id`` is not registered with the registry."""


class PassRunnerRegistry:
    """
    Resolve hosted ``PassRunner`` adapter classes by stable ``runner_id``.

    Defaults register the two real hosted adapters (``olmocr``, ``kraken``).
    Fake doubles may be registered in tests only; they are not Phase 6 exit
    evidence.

    Args:
        runners: Optional mapping of ``runner_id`` to a constructable
            ``PassRunner`` class. When omitted, registers ``olmocr`` and
            ``kraken``.

    """

    def __init__(self, runners: Mapping[str, PassRunnerClass] | None = None) -> None:
        """
        Bind known runner classes for resolution.

        Args:
            runners: Optional mapping of ``runner_id`` to a constructable
                ``PassRunner`` class. When omitted, registers ``olmocr`` and
                ``kraken``.

        """
        if runners is None:
            runners = {
                "olmocr": HuggingFaceOlmocrRunner,
                "kraken": HuggingFaceKrakenRunner,
            }
        #: Registered constructable PassRunner classes keyed by runner_id.
        self._runners: dict[str, PassRunnerClass] = dict(runners)

    @property
    def known_ids(self) -> frozenset[str]:
        """
        Stable runner ids currently registered.

        Returns:
            Frozen set of registered ``runner_id`` values.

        """
        return frozenset(self._runners)

    def register(self, runner_id: str, runner_cls: PassRunnerClass) -> None:
        """
        Register or replace one constructable ``PassRunner`` class.

        Args:
            runner_id: Stable logical runner id.
            runner_cls: Constructable class whose instances satisfy
                ``PassRunner``.

        """
        self._runners[runner_id] = runner_cls

    def resolve(self, runner_id: str) -> PassRunnerClass:
        """
        Return the constructable ``PassRunner`` class for ``runner_id``.

        Args:
            runner_id: Stable logical runner id from ``RunnerReference``.

        Returns:
            Constructable class whose instances satisfy ``PassRunner``.

        Raises:
            UnknownPassRunnerError: If ``runner_id`` is not registered.

        """
        runner_cls = self._runners.get(runner_id)
        if runner_cls is None:
            supported = ", ".join(sorted(self._runners)) or "(none)"
            msg = f"unsupported runner_id {runner_id!r}; supported: {supported}"
            raise UnknownPassRunnerError(msg)
        return runner_cls
