# Copyright (C) 2026 Chris Malek.
"""Runner execution policy, packaging, and hosted-invocation contracts."""

from __future__ import annotations

import math
from decimal import Decimal
from enum import StrEnum

from pydantic import Field, model_validator

from bochord.models.ocr import (
    BatchItemRef,
    InputKind,
    PackagingStrategy,
    PreparedArtifactRef,
    RunnerOutputArtifact,
    SchemaModel,
)


class RetryMode(StrEnum):
    """Retry strategy for failed runner invocations."""

    #: Do not retry failed invocations.
    NONE = "none"
    #: Retry the entire batch as one unit.
    WHOLE_BATCH = "whole-batch"
    #: Retry only the items that failed.
    FAILED_ITEMS = "failed-items"


class HostedEndpointPolicy(SchemaModel):
    """Hosted inference endpoint contract without secrets."""

    #: Human-readable endpoint name in the hosting provider.
    endpoint_name: str
    #: Settings key used to resolve the endpoint URL at runtime.
    endpoint_key: str
    #: Hardware class required for reproducible execution.
    hardware_class: str
    #: Maximum seconds to wait for a cold-started endpoint.
    cold_start_timeout_seconds: float = Field(gt=0)
    #: Maximum seconds to wait for one inference request.
    request_timeout_seconds: float = Field(gt=0)
    #: HTTP status codes that may be retried.
    retryable_status_codes: list[int]
    #: Whether the endpoint scales to zero when idle.
    scale_to_zero: bool
    #: Maximum items allowed in one hosted run.
    max_items_per_run: int = Field(gt=0)
    #: Estimated hosted cost per item in USD.
    estimated_cost_per_item_usd: Decimal = Field(ge=0)
    #: Maximum allowed cost for one hosted run in USD.
    max_run_cost_usd: Decimal = Field(ge=0)
    #: Days to retain hosted-side artifacts.
    artifact_retention_days: int = Field(gt=0)


class RunnerExecutionPolicy(SchemaModel):
    """Frozen execution policy for one runner and hosting boundary."""

    #: Stable policy identifier referenced by execution batches.
    policy_id: str
    #: Policy schema version.
    version: str
    #: Fixed number of items per invocation batch.
    batch_size: int = Field(gt=0)
    #: Longest image dimension sent to the hosted runner.
    target_longest_image_dim: int = Field(gt=0)
    #: Whether page-local item groups must stay together in one batch.
    preserve_page_local_groups: bool = True
    #: Packaging policy applied before hosted invocation.
    packaging_strategy: PackagingStrategy
    #: Number of warmup batches to run before measured throughput.
    warmup_batch_count: int = Field(default=0, ge=0)
    #: Retry strategy for failed invocations.
    retry_mode: RetryMode = RetryMode.FAILED_ITEMS
    #: Maximum retry attempts after the initial invocation.
    max_retries: int = Field(default=1, ge=0, le=1)
    #: Hosted endpoint contract for this policy.
    endpoint: HostedEndpointPolicy

    @model_validator(mode="after")
    def validate_run_cost_cap(self) -> RunnerExecutionPolicy:
        """
        Reject endpoint estimates that exceed the configured run cost cap.

        Returns:
            The validated execution policy.

        Raises:
            ValueError: If estimated per-run cost exceeds ``max_run_cost_usd``.

        """
        estimated_run_cost = (
            Decimal(self.endpoint.max_items_per_run)
            * self.endpoint.estimated_cost_per_item_usd
        )
        if estimated_run_cost > self.endpoint.max_run_cost_usd:
            msg = (
                "max_items_per_run * estimated_cost_per_item_usd "
                "must not exceed max_run_cost_usd"
            )
            raise ValueError(msg)
        return self


class PlannedRunnerBatch(SchemaModel):
    """One planned invocation batch before packaging and submission."""

    #: Stable batch identifier within the run.
    batch_id: str
    #: Source items included in this batch.
    items: list[BatchItemRef] = Field(min_length=1)
    #: Prepared artifacts that will be packaged for this batch.
    artifacts: list[PreparedArtifactRef] = Field(min_length=1)
    #: Whether this batch is a warmup invocation excluded from throughput.
    warmup: bool = False


class PackagedRunnerInput(SchemaModel):
    """Packaged artifact ready for hosted runner submission."""

    #: Stable packaged-input artifact identifier.
    artifact_id: str
    #: Filesystem-relative path to the packaged input artifact.
    artifact_path: str
    #: Digest binding the packaged input bytes.
    checksum: str
    #: Concrete packaged input kind.
    kind: InputKind
    #: Batch item ids represented by this packaged input.
    batch_item_ids: list[str] = Field(min_length=1)
    #: Source page numbers aligned with ``batch_item_ids``.
    page_numbers: list[int] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_item_page_alignment(self) -> PackagedRunnerInput:
        """
        Require one page number for every packaged batch item.

        Returns:
            The validated packaged runner input.

        Raises:
            ValueError: If item ids and page numbers differ in length.

        """
        if len(self.batch_item_ids) != len(self.page_numbers):
            msg = "batch_item_ids and page_numbers must have equal length"
            raise ValueError(msg)
        return self


class HostedInvocationResult(SchemaModel):
    """Raw result returned from one hosted runner invocation."""

    #: Batch item ids that failed during hosted execution.
    failure_item_ids: list[str]
    #: Output witness artifacts produced by the hosted runner.
    output_artifacts: list[RunnerOutputArtifact]
    #: Hosted request identifiers for audit and support.
    request_ids: list[str]
    #: Non-fatal warnings emitted by the hosted runner.
    warnings: list[str]


class RunnerThroughputSummary(SchemaModel):
    """Measured throughput for one runner execution segment."""

    #: Number of items included in the measured segment.
    measured_item_count: int = Field(ge=0)
    #: Number of items that failed in the measured segment.
    failed_item_count: int = Field(ge=0)
    #: Wall-clock duration of the measured segment in seconds.
    measured_duration_seconds: float = Field(ge=0)
    #: Derived throughput in items per second.
    items_per_second: float = Field(ge=0)

    @model_validator(mode="after")
    def validate_throughput_coherence(self) -> RunnerThroughputSummary:
        """
        Keep failure counts and derived throughput internally coherent.

        Returns:
            The validated throughput summary.

        Raises:
            ValueError: If counts or throughput disagree with measured facts.

        """
        if self.failed_item_count > self.measured_item_count:
            msg = "failed_item_count must not exceed measured_item_count"
            raise ValueError(msg)
        if (
            self.measured_duration_seconds > 0
            and self.measured_item_count > 0
            and not math.isclose(
                self.items_per_second,
                self.measured_item_count / self.measured_duration_seconds,
                rel_tol=1e-9,
                abs_tol=1e-9,
            )
        ):
            msg = (
                "items_per_second must equal measured_item_count / "
                "measured_duration_seconds"
            )
            raise ValueError(msg)
        return self
