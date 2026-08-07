# Copyright (C) 2026 Chris Malek.
"""Pass-runner runtime Protocol extracted from real hosted adapter call sites."""

from __future__ import annotations

from pathlib import Path  # noqa: TC003
from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from wordwending.models.ocr import RunnerCapability, RunnerReference
    from wordwending.models.runner_execution import (
        HostedInvocationResult,
        PackagedRunnerInput,
        PlannedRunnerBatch,
        RunnerExecutionPolicy,
    )


@runtime_checkable
class PassRunner(Protocol):
    """
    Common runtime contract for hosted pass runners.

    Extracted from ``HuggingFaceOlmocrRunner`` and ``HuggingFaceKrakenRunner``
    call sites (ADR 0007 / Spec 0013). The execution spine reads ``policy``,
    ``runner_ref``, and ``capability`` for batch persistence, calls
    ``health_check`` before invocations, and invokes batches via::

        invocation = runner.invoke(planned, packaged, output_dir)

    Fake doubles may satisfy this Protocol in unit tests only; they do not
    close Spec 0004 Phase 6 by themselves.
    """

    @property
    def policy(self) -> RunnerExecutionPolicy:
        """Frozen execution policy for hosted invocations."""

    @property
    def runner_ref(self) -> RunnerReference:
        """Model-backed runner identity persisted on batch records."""

    @property
    def capability(self) -> RunnerCapability:
        """Declared input and batching contract for the orchestrator."""

    def health_check(self) -> None:
        """
        Verify the hosted endpoint is ready for invocations.

        Raises:
            RunnerEndpointUnavailable: If the endpoint is unreachable or not ready.

        """

    def invoke(
        self,
        batch: PlannedRunnerBatch,
        packaged: PackagedRunnerInput,
        output_dir: Path,
    ) -> HostedInvocationResult:
        """
        Execute one packaged batch against the hosted endpoint.

        Side Effects:
            Writes raw witness bytes under ``output_dir`` when items succeed.

        Args:
            batch: Planned batch whose items will be invoked.
            packaged: Packaged input artifact metadata and page mapping.
            output_dir: Output root containing packaged inputs and witnesses.

        Returns:
            Hosted invocation result with per-item failures and artifacts.

        """
