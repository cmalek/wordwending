# Copyright (C) 2026 Chris Malek.
"""Fixed-size runner batch planning without runtime adaptation."""

from __future__ import annotations

import hashlib
from decimal import Decimal
from itertools import groupby

from wordwending.models.ocr import (
    BatchItemRef,
    PackagingStrategy,
    PreparedArtifactRef,
    RunnerCapability,
)
from wordwending.models.runner_execution import (
    PlannedRunnerBatch,
    RunnerExecutionPolicy,
)


def _batch_id(policy_id: str, artifact_ids: list[str], ordinal: int) -> str:
    """
    Derive a stable batch identifier from policy, artifacts, and ordinal.

    Args:
        policy_id: Execution policy identifier.
        artifact_ids: Ordered artifact ids included in the batch.
        ordinal: Zero-based batch ordinal within the run.

    Returns:
        Stable ``batch-<hex>`` identifier.

    """
    material = f"{policy_id}\n{ordinal}\n" + ",".join(artifact_ids)
    return "batch-" + hashlib.sha256(material.encode("utf-8")).hexdigest()


def _chunk_size(
    capability: RunnerCapability,
    policy: RunnerExecutionPolicy,
) -> int:
    """
    Resolve the fixed chunk size for one planned batch.

    Args:
        capability: Declared runner batching contract.
        policy: Frozen execution policy for the run.

    Returns:
        Maximum number of artifacts allowed in one batch.

    """
    if (
        not capability.supports_multi_item_batching
        or policy.packaging_strategy is PackagingStrategy.DIRECT
    ):
        return 1
    return policy.batch_size


def _grouped_artifacts(
    artifacts: list[PreparedArtifactRef],
    *,
    preserve_page_local_groups: bool,
) -> list[list[PreparedArtifactRef]]:
    """
    Group artifacts for page-local batching when required.

    Args:
        artifacts: Ordered prepared artifacts for the run.

    Keyword Args:
        preserve_page_local_groups: Whether page ids must stay isolated.

    Returns:
        Artifact groups to chunk independently.

    """
    if not preserve_page_local_groups:
        return [artifacts]
    return [
        list(group)
        for _, group in groupby(artifacts, key=lambda artifact: artifact.page_id)
    ]


def _fixed_chunks(
    artifacts: list[PreparedArtifactRef],
    chunk_size: int,
) -> list[list[PreparedArtifactRef]]:
    """
    Split artifacts into fixed-size chunks preserving order.

    Args:
        artifacts: Ordered artifacts for one grouping scope.
        chunk_size: Maximum items per batch chunk.

    Returns:
        Fixed-size artifact chunks.

    """
    return [
        artifacts[start : start + chunk_size]
        for start in range(0, len(artifacts), chunk_size)
    ]


class RunnerBatchPlanner:
    """Plan fixed runner batches from prepared artifacts and policy."""

    def plan(
        self,
        artifacts: list[PreparedArtifactRef],
        capability: RunnerCapability,
        policy: RunnerExecutionPolicy,
    ) -> list[PlannedRunnerBatch]:
        """
        Plan fixed-size runner batches without runtime adaptation.

        Args:
            artifacts: Ordered prepared artifacts ready for packaging.
            capability: Declared runner input and batching contract.
            policy: Frozen execution policy for the run.

        Returns:
            Planned batches with stable ids and optional warmup marking.

        Raises:
            ValueError: If inputs are rejected by capability or cost caps.

        """
        self._validate_cost_caps(artifacts, policy)
        accepted_kinds = set(capability.accepted_input_kinds)
        for artifact in artifacts:
            if artifact.kind not in accepted_kinds:
                msg = (
                    f"artifact {artifact.artifact_id} kind {artifact.kind.value} "
                    "is not in accepted_input_kinds"
                )
                raise ValueError(msg)

        chunk_size = _chunk_size(capability, policy)
        artifact_groups = _grouped_artifacts(
            artifacts,
            preserve_page_local_groups=policy.preserve_page_local_groups,
        )
        chunks: list[list[PreparedArtifactRef]] = []
        for group in artifact_groups:
            chunks.extend(_fixed_chunks(group, chunk_size))

        batches: list[PlannedRunnerBatch] = []
        for ordinal, chunk in enumerate(chunks):
            artifact_ids = [artifact.artifact_id for artifact in chunk]
            batch_id = _batch_id(policy.policy_id, artifact_ids, ordinal)
            items = [
                BatchItemRef(
                    item_id=f"{batch_id}-item-{index:03d}",
                    source_page_id=artifact.page_id,
                    prepared_unit_id=artifact.prepared_unit_id,
                    artifact_id=artifact.artifact_id,
                )
                for index, artifact in enumerate(chunk, start=1)
            ]
            batches.append(
                PlannedRunnerBatch(
                    batch_id=batch_id,
                    items=items,
                    artifacts=chunk,
                    warmup=ordinal < policy.warmup_batch_count,
                )
            )
        return batches

    def _validate_cost_caps(
        self,
        artifacts: list[PreparedArtifactRef],
        policy: RunnerExecutionPolicy,
    ) -> None:
        """
        Reject runs that exceed hosted item or cost caps before planning output.

        Args:
            artifacts: Ordered prepared artifacts for the run.
            policy: Frozen execution policy for the run.

        Raises:
            ValueError: If the run exceeds configured caps.

        """
        item_count = len(artifacts)
        if item_count > policy.endpoint.max_items_per_run:
            msg = (
                "artifact count exceeds endpoint max_items_per_run "
                f"({item_count} > {policy.endpoint.max_items_per_run})"
            )
            raise ValueError(msg)
        estimated_cost = (
            Decimal(item_count) * policy.endpoint.estimated_cost_per_item_usd
        )
        if estimated_cost > policy.endpoint.max_run_cost_usd:
            msg = (
                "estimated run cost exceeds endpoint max_run_cost_usd "
                f"({estimated_cost} > {policy.endpoint.max_run_cost_usd})"
            )
            raise ValueError(msg)
