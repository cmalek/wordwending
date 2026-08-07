# Copyright (C) 2026 Chris Malek.
"""Persist runner execution batches, retries, and throughput summaries."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from pathlib import Path  # noqa: TC003
from typing import TYPE_CHECKING

from wordwending.exc import ConfigurationError, RunnerEndpointUnavailable
from wordwending.models.ocr import (
    BatchResultStatus,
    PreparedArtifactRef,
    RunnerExecutionBatch,
)
from wordwending.models.runner_execution import (
    HostedInvocationResult,
    PlannedRunnerBatch,
    RetryMode,
    RunnerThroughputSummary,
)
from wordwending.services.resume_ledger import ResumeLedgerService
from wordwending.services.runner_batching import RunnerBatchPlanner  # noqa: TC001
from wordwending.services.runner_packaging import RunnerInputPackager  # noqa: TC001

if TYPE_CHECKING:
    from wordwending.services.pass_runner import PassRunner

#: Persisted runner-batch schema version written under ``output_dir/batches/``.
RUNNER_BATCH_SCHEMA_VERSION = "1.0.0"
#: Retry strategy label persisted on failed-item retry batches.
FAILED_ITEMS_RETRY_STRATEGY = "failed-items"


def _retry_batch_id(original_batch_id: str, failure_item_ids: list[str]) -> str:
    """
    Derive a stable retry batch identifier from the source batch and failures.

    Args:
        original_batch_id: Persisted batch id for the initial invocation.
        failure_item_ids: Item ids that will be retried.

    Returns:
        Stable ``batch-<hex>`` retry identifier.

    """
    material = f"{original_batch_id}\nretry-1\n" + ",".join(sorted(failure_item_ids))
    return "batch-" + hashlib.sha256(material.encode("utf-8")).hexdigest()


def _derive_result_status(
    failure_item_ids: list[str],
    item_count: int,
) -> BatchResultStatus:
    """
    Map per-item failures to one batch result status.

    Args:
        failure_item_ids: Item ids that failed during invocation.
        item_count: Number of items submitted in the batch.

    Returns:
        Derived batch execution status.

    """
    if not failure_item_ids:
        return BatchResultStatus.SUCCEEDED
    if len(failure_item_ids) == item_count:
        return BatchResultStatus.FAILED
    return BatchResultStatus.PARTIAL


def _atomic_write_text(path: Path, payload: str) -> None:
    """
    Atomically write ``payload`` to ``path`` via a sibling temporary file.

    Side Effects:
        Creates parent directories and replaces ``path`` on success.

    Args:
        path: Destination file path.
        payload: UTF-8 text to persist.

    """
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(path.suffix + ".tmp")
    try:
        temp_path.write_text(payload, encoding="utf-8")
        temp_path.replace(path)
    except Exception:
        if temp_path.exists():
            temp_path.unlink()
        raise


class RunnerExecutionOrchestrator:
    """
    Coordinate one runner execution run with mutable per-run state.

    Args:
        planner: Fixed-size batch planner.
        packager: Runner input packager.
        runner: Hosted runner used for health checks and invocations.
        run_id: Execution run identifier.
        document_id: Document identifier under processing.
        bundle_root: Bundle root containing prepared artifact bytes.
        output_dir: Output root for batches, inputs, and witnesses.
        force: When ``True``, bypass the resume ledger and re-run batches.
        ledger: Resume ledger collaborator for completed-batch skip/record.

    """

    def __init__(  # noqa: PLR0913
        self,
        *,
        planner: RunnerBatchPlanner,
        packager: RunnerInputPackager,
        runner: PassRunner,
        run_id: str,
        document_id: str,
        bundle_root: Path,
        output_dir: Path,
        force: bool = False,
        ledger: ResumeLedgerService | None = None,
    ) -> None:
        """
        Bind collaborators and run identifiers for one execution segment.

        Keyword Args:
            planner: Fixed-size batch planner.
            packager: Runner input packager.
            runner: Hosted runner used for health checks and invocations.
            run_id: Execution run identifier.
            document_id: Document identifier under processing.
            bundle_root: Bundle root containing prepared artifact bytes.
            output_dir: Output root for batches, inputs, and witnesses.
            force: When ``True``, bypass the resume ledger and re-run batches.
            ledger: Resume ledger collaborator for completed-batch skip/record.

        """
        #: Fixed-size batch planner.
        self._planner = planner
        #: Runner input packager.
        self._packager = packager
        #: Hosted runner used for health checks and invocations.
        self._runner = runner
        #: Execution run identifier.
        self._run_id = run_id
        #: Document identifier under processing.
        self._document_id = document_id
        #: Bundle root containing prepared artifact bytes.
        self._bundle_root = bundle_root
        #: Output root for batches, inputs, and witnesses.
        self._output_dir = output_dir
        #: When ``True``, ignore completed batches already recorded in the ledger.
        self._force = force
        #: Resume ledger used to skip and record successfully completed batches.
        self._ledger = ledger
        #: Frozen execution policy for the run.
        self._policy = runner.policy
        #: Runner identity persisted on each batch record.
        self._runner_ref = runner.runner_ref
        #: Declared capability contract for the run.
        self._capability = runner.capability
        #: Persisted batch records emitted during the run.
        self._batches: list[RunnerExecutionBatch] = []
        #: Final failed item ids among measured non-warmup original items.
        self._failed_item_ids: set[str] = set()
        #: Measured non-warmup original item ids tracked for throughput.
        self._measured_item_ids: set[str] = set()
        #: Accumulated measured wall-clock duration in seconds.
        self._measured_duration_seconds = 0.0

    def run(
        self,
        artifacts: list[PreparedArtifactRef],
    ) -> tuple[list[RunnerExecutionBatch], RunnerThroughputSummary]:
        """
        Execute planned batches, optional retries, and throughput persistence.

        Args:
            artifacts: Ordered prepared artifacts ready for runner execution.

        Returns:
            Persisted runner execution batches and measured throughput summary.

        Raises:
            ConfigurationError: If the execution policy requests unsupported retry.

        """
        if self._policy.retry_mode is RetryMode.WHOLE_BATCH:
            msg = "whole-batch retry is not supported"
            raise ConfigurationError(msg)
        planned_batches = self._planner.plan(
            artifacts,
            self._capability,
            self._policy,
        )
        try:
            self._runner.health_check()
        except RunnerEndpointUnavailable as exc:
            return self._persist_health_failure(planned_batches, str(exc))
        for planned in planned_batches:
            if self._should_skip_planned_batch(planned):
                continue
            self._execute_planned_batch(planned)
        summary = self._build_throughput()
        self._persist_throughput(summary)
        return self._batches, summary

    def _should_skip_planned_batch(self, planned: PlannedRunnerBatch) -> bool:
        """
        Return whether ``planned`` should be skipped from a prior resume ledger.

        Args:
            planned: One planned batch from the fixed-size planner.

        Returns:
            ``True`` when the batch is already recorded and ``force`` is off.

        """
        if self._force or self._ledger is None:
            return False
        return self._ledger.contains(planned.batch_id)

    def _persist_health_failure(
        self,
        planned_batches: list[PlannedRunnerBatch],
        warning: str,
    ) -> tuple[list[RunnerExecutionBatch], RunnerThroughputSummary]:
        """
        Persist failed batch records when the hosted endpoint is unavailable.

        Args:
            planned_batches: Batches planned before the health check failed.
            warning: Health-check warning to attach to every persisted batch.

        Returns:
            Failed batch records and measured throughput summary.

        """
        timestamp = datetime.now(tz=UTC)
        for planned in planned_batches:
            item_ids = [item.item_id for item in planned.items]
            if not planned.warmup:
                self._measured_item_ids.update(item_ids)
                self._failed_item_ids.update(item_ids)
            batch = self._build_batch_record(
                planned=planned,
                started_at=timestamp,
                finished_at=timestamp,
                result_status=BatchResultStatus.FAILED,
                failure_item_ids=item_ids,
                invocation=HostedInvocationResult(
                    failure_item_ids=item_ids,
                    output_artifacts=[],
                    request_ids=[],
                    warnings=[warning],
                ),
                packaging_artifact_id=None,
            )
            self._persist_batch(batch)
            self._batches.append(batch)
        summary = self._build_throughput()
        self._persist_throughput(summary)
        return self._batches, summary

    def _execute_planned_batch(self, planned: PlannedRunnerBatch) -> None:
        """
        Package, invoke, persist, and optionally retry one planned batch.

        Args:
            planned: One planned batch from the fixed-size planner.

        """
        if not planned.warmup:
            self._measured_item_ids.update(item.item_id for item in planned.items)
        batch = self._invoke_and_persist(planned)
        self._batches.append(batch)
        self._record_batch_outcomes(batch)
        if self._should_retry(batch):
            retry_planned = self._retry_planned_batch(planned, batch.failure_item_ids)
            retry_batch = self._invoke_and_persist(
                retry_planned,
                retry_of_batch_id=batch.batch_id,
                retry_strategy=FAILED_ITEMS_RETRY_STRATEGY,
            )
            self._batches.append(retry_batch)
            self._apply_retry_outcomes(batch, retry_batch)
        self._record_ledger_success(planned)

    def _record_ledger_success(self, planned: PlannedRunnerBatch) -> None:
        """
        Record ``planned`` in the resume ledger when every item finally succeeded.

        Side Effects:
            Updates ``bundle_root/runner-resume-ledger.json`` when recording.

        Args:
            planned: Planned batch whose final item outcomes were just tracked.

        """
        if self._ledger is None:
            return
        item_ids = {item.item_id for item in planned.items}
        if planned.warmup:
            succeeded = any(
                batch.batch_id == planned.batch_id
                and batch.result_status is BatchResultStatus.SUCCEEDED
                for batch in self._batches
            )
        else:
            succeeded = not (item_ids & self._failed_item_ids)
        if not succeeded:
            return
        self._ledger.record_completed(
            batch_id=planned.batch_id,
            run_id=self._run_id,
            document_id=self._document_id,
            source_page_ids=[item.source_page_id for item in planned.items],
        )

    def _invoke_and_persist(
        self,
        planned: PlannedRunnerBatch,
        *,
        retry_of_batch_id: str | None = None,
        retry_strategy: str | None = None,
    ) -> RunnerExecutionBatch:
        """
        Package and invoke one batch, then persist the execution record.

        Args:
            planned: Planned batch to package and invoke.

        Keyword Args:
            retry_of_batch_id: Source batch id when this is a retry invocation.
            retry_strategy: Persisted retry strategy label.

        Returns:
            Persisted runner execution batch for the invocation.

        """
        started_at = datetime.now(tz=UTC)
        packaged = self._packager.package(
            planned,
            self._capability.packaging_strategy,
            self._bundle_root,
            self._output_dir,
        )
        invocation = self._runner.invoke(planned, packaged, self._output_dir)
        finished_at = datetime.now(tz=UTC)
        if not planned.warmup:
            self._measured_duration_seconds += (
                finished_at - started_at
            ).total_seconds()
        batch = self._build_batch_record(
            planned=planned,
            started_at=started_at,
            finished_at=finished_at,
            result_status=_derive_result_status(
                invocation.failure_item_ids,
                len(planned.items),
            ),
            failure_item_ids=list(invocation.failure_item_ids),
            invocation=invocation,
            packaging_artifact_id=packaged.artifact_id,
            retry_of_batch_id=retry_of_batch_id,
            retry_strategy=retry_strategy,
        )
        self._persist_batch(batch)
        return batch

    def _build_batch_record(  # noqa: PLR0913
        self,
        *,
        planned: PlannedRunnerBatch,
        started_at: datetime,
        finished_at: datetime,
        result_status: BatchResultStatus,
        failure_item_ids: list[str],
        invocation: HostedInvocationResult,
        packaging_artifact_id: str | None,
        retry_of_batch_id: str | None = None,
        retry_strategy: str | None = None,
    ) -> RunnerExecutionBatch:
        """
        Build one validated runner execution batch model.

        Keyword Args:
            planned: Planned batch metadata for ids and items.
            started_at: UTC timestamp when invocation started.
            finished_at: UTC timestamp when invocation finished.
            result_status: Derived batch execution status.
            failure_item_ids: Item ids that failed during invocation.
            invocation: Raw hosted invocation result.
            packaging_artifact_id: Packaged input artifact id when created.
            retry_of_batch_id: Source batch id when this is a retry invocation.
            retry_strategy: Persisted retry strategy label.

        Returns:
            Validated runner execution batch ready for persistence.

        """
        return RunnerExecutionBatch(
            schema_version=RUNNER_BATCH_SCHEMA_VERSION,
            batch_id=planned.batch_id,
            run_id=self._run_id,
            document_id=self._document_id,
            execution_policy_id=self._policy.policy_id,
            runner=self._runner_ref,
            capability=self._capability,
            packaging_artifact_id=packaging_artifact_id,
            batch_size=len(planned.items),
            items=list(planned.items),
            started_at_utc=started_at,
            finished_at_utc=finished_at,
            retry_of_batch_id=retry_of_batch_id,
            retry_strategy=retry_strategy,
            result_status=result_status,
            failure_item_ids=failure_item_ids,
            output_artifacts=list(invocation.output_artifacts),
            warnings=list(invocation.warnings),
            warmup=planned.warmup,
            request_ids=list(invocation.request_ids),
        )

    def _persist_batch(self, batch: RunnerExecutionBatch) -> None:
        """
        Atomically persist one runner execution batch JSON record.

        Side Effects:
            Writes ``output_dir/batches/<batch-id>.json``.

        Args:
            batch: Runner execution batch to persist.

        """
        destination = self._output_dir / "batches" / f"{batch.batch_id}.json"
        _atomic_write_text(destination, batch.model_dump_json(indent=2))

    def _should_retry(self, batch: RunnerExecutionBatch) -> bool:
        """
        Return whether one failed-item retry should run for ``batch``.

        Args:
            batch: Persisted batch record from the initial invocation.

        Returns:
            ``True`` when a single failed-item retry is configured and needed.

        """
        if batch.warmup or not batch.failure_item_ids:
            return False
        if self._policy.retry_mode is not RetryMode.FAILED_ITEMS:
            return False
        if self._policy.max_retries < 1:
            return False
        return batch.result_status in {
            BatchResultStatus.PARTIAL,
            BatchResultStatus.FAILED,
        }

    def _retry_planned_batch(
        self,
        original: PlannedRunnerBatch,
        failure_item_ids: list[str],
    ) -> PlannedRunnerBatch:
        """
        Build a retry planned batch containing only failed items.

        Args:
            original: Source planned batch from the initial invocation.
            failure_item_ids: Item ids to include in the retry batch.

        Returns:
            Planned batch for the single failed-item retry invocation.

        """
        failed = set(failure_item_ids)
        items = [item for item in original.items if item.item_id in failed]
        artifacts = [
            artifact
            for item, artifact in zip(original.items, original.artifacts, strict=True)
            if item.item_id in failed
        ]
        return PlannedRunnerBatch(
            batch_id=_retry_batch_id(original.batch_id, failure_item_ids),
            items=items,
            artifacts=artifacts,
            warmup=False,
        )

    def _record_batch_outcomes(self, batch: RunnerExecutionBatch) -> None:
        """
        Track final item failures for one non-warmup original batch.

        Args:
            batch: Persisted batch record from the initial invocation.

        """
        if batch.warmup:
            return
        self._failed_item_ids.update(batch.failure_item_ids)

    def _apply_retry_outcomes(
        self,
        original: RunnerExecutionBatch,
        retry: RunnerExecutionBatch,
    ) -> None:
        """
        Update final failures after one failed-item retry completes.

        Args:
            original: Initial batch record that triggered the retry.
            retry: Retry batch record for the failed items.

        """
        if original.warmup:
            return
        retried = {item.item_id for item in retry.items}
        self._failed_item_ids -= retried
        self._failed_item_ids.update(retry.failure_item_ids)

    def _build_throughput(self) -> RunnerThroughputSummary:
        """
        Build the measured throughput summary for the completed run.

        Returns:
            Throughput summary for non-warmup original item outcomes.

        """
        measured_item_count = len(self._measured_item_ids)
        failed_item_count = len(self._failed_item_ids & self._measured_item_ids)
        duration = self._measured_duration_seconds
        if duration > 0 and measured_item_count > 0:
            items_per_second = measured_item_count / duration
        else:
            items_per_second = 0.0
        return RunnerThroughputSummary(
            measured_item_count=measured_item_count,
            failed_item_count=failed_item_count,
            measured_duration_seconds=duration,
            items_per_second=items_per_second,
        )

    def _persist_throughput(self, summary: RunnerThroughputSummary) -> None:
        """
        Persist the measured throughput summary for the run.

        Side Effects:
            Writes ``output_dir/throughput.json``.

        Args:
            summary: Measured throughput summary to persist.

        """
        destination = self._output_dir / "throughput.json"
        _atomic_write_text(destination, summary.model_dump_json(indent=2))


class RunnerExecutionService:
    """
    Thin facade that delegates one run to ``RunnerExecutionOrchestrator``.

    Args:
        planner: Fixed-size batch planner.
        packager: Runner input packager.
        runner: Hosted runner used for health checks and invocations.

    """

    def __init__(
        self,
        planner: RunnerBatchPlanner,
        packager: RunnerInputPackager,
        runner: PassRunner,
    ) -> None:
        """
        Bind batch planning, packaging, and hosted runner collaborators.

        Args:
            planner: Fixed-size batch planner.
            packager: Runner input packager.
            runner: Hosted runner used for health checks and invocations.

        """
        #: Fixed-size batch planner.
        self._planner = planner
        #: Runner input packager.
        self._packager = packager
        #: Hosted runner used for health checks and invocations.
        self._runner = runner

    def run(  # noqa: PLR0913
        self,
        run_id: str,
        document_id: str,
        artifacts: list[PreparedArtifactRef],
        bundle_root: Path,
        output_dir: Path,
        *,
        force: bool = False,
    ) -> tuple[list[RunnerExecutionBatch], RunnerThroughputSummary]:
        """
        Execute one runner segment and persist batches plus throughput.

        Args:
            run_id: Execution run identifier.
            document_id: Document identifier under processing.
            artifacts: Ordered prepared artifacts ready for runner execution.
            bundle_root: Bundle root containing prepared artifact bytes.
            output_dir: Output root for batches, inputs, and witnesses.

        Keyword Args:
            force: When ``True``, bypass the resume ledger and re-run batches.

        Returns:
            Persisted batch records and the measured throughput summary.

        """
        orchestrator = RunnerExecutionOrchestrator(
            planner=self._planner,
            packager=self._packager,
            runner=self._runner,
            run_id=run_id,
            document_id=document_id,
            bundle_root=bundle_root,
            output_dir=output_dir,
            force=force,
            ledger=ResumeLedgerService(bundle_root),
        )
        batches, summary = orchestrator.run(artifacts)
        return batches, summary
