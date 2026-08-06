# Copyright (C) 2026 Chris Malek.
"""Tests for fixed runner batch planning."""

from __future__ import annotations

from decimal import Decimal

import pytest

from tests.test_ocr_models import runner_policy_payload
from wordwending.models.ocr import (
    BatchUnitKind,
    BoundingBox,
    InputKind,
    PackagingStrategy,
    PreparedArtifactRef,
    RunnerCapability,
)
from wordwending.models.runner_execution import (
    HostedEndpointPolicy,
    RunnerExecutionPolicy,
)
from wordwending.services.runner_batching import RunnerBatchPlanner


def capability(**overrides: object) -> RunnerCapability:
    """Return a default multi-item runner capability with optional overrides."""
    payload: dict[str, object] = {
        "accepted_input_kinds": [
            InputKind.IMAGE,
            InputKind.PREPARED_UNIT,
            InputKind.PDF,
        ],
        "preferred_input_kind": InputKind.PDF,
        "supports_multi_item_batching": True,
        "batch_unit_kind": BatchUnitKind.PREPARED_UNIT,
        "packaging_strategy": PackagingStrategy.UNIT_TO_PDF_BATCH,
    }
    payload.update(overrides)
    return RunnerCapability.model_validate(payload)


def policy(**overrides: object) -> RunnerExecutionPolicy:
    """Return a default runner execution policy with optional overrides."""
    return RunnerExecutionPolicy.model_validate(runner_policy_payload(**overrides))


def _prepared_unit(
    *,
    artifact_id: str,
    page_id: str,
    prepared_unit_id: str,
    artifact_path: str,
    order: int,
) -> PreparedArtifactRef:
    return PreparedArtifactRef(
        artifact_id=artifact_id,
        kind=InputKind.PREPARED_UNIT,
        page_id=page_id,
        prepared_unit_id=prepared_unit_id,
        artifact_path=artifact_path,
        parent_prepared_page_id=f"prepared-{page_id}",
        checksum=f"sha256:{artifact_id}",
        order=order,
        bounding_box=BoundingBox(x0=0, y0=0, x1=100, y1=100),
    )


def artifacts(count: int, *, kind: InputKind = InputKind.PREPARED_UNIT) -> list[PreparedArtifactRef]:
    """Build ``count`` sequential prepared artifacts on one page."""
    if kind is not InputKind.PREPARED_UNIT:
        return [
            PreparedArtifactRef(
                artifact_id=f"artifact-{index:03d}",
                kind=kind,
                page_id="page-0001",
                artifact_path=f"prepared/page-0001/artifact-{index:03d}.pdf",
            )
            for index in range(1, count + 1)
        ]
    return [
        _prepared_unit(
            artifact_id=f"artifact-{index:03d}",
            page_id="page-0001",
            prepared_unit_id=f"unit-{index:03d}",
            artifact_path=f"prepared/page-0001/units/unit-{index:03d}.png",
            order=index,
        )
        for index in range(1, count + 1)
    ]


def units(page_counts: dict[str, int]) -> list[PreparedArtifactRef]:
    """Build prepared-unit artifacts grouped by page id."""
    refs: list[PreparedArtifactRef] = []
    for page_id, count in page_counts.items():
        refs.extend(
            _prepared_unit(
                artifact_id=f"{page_id}-unit-{index:03d}",
                page_id=page_id,
                prepared_unit_id=f"{page_id}-unit-{index:03d}",
                artifact_path=f"prepared/{page_id}/units/unit-{index:03d}.png",
                order=index,
            )
            for index in range(1, count + 1)
        )
    return refs


def test_non_batching_runner_gets_one_item_batches() -> None:
    batches = RunnerBatchPlanner().plan(
        artifacts(3),
        capability(supports_multi_item_batching=False),
        policy(batch_size=4),
    )
    assert [len(batch.items) for batch in batches] == [1, 1, 1]


def test_page_local_policy_does_not_mix_units_until_needed() -> None:
    batches = RunnerBatchPlanner().plan(
        units(page_counts={"page-1": 3, "page-2": 3}),
        capability(),
        policy(batch_size=4, preserve_page_local_groups=True),
    )
    assert [[item.source_page_id for item in batch.items] for batch in batches] == [
        ["page-1", "page-1", "page-1"],
        ["page-2", "page-2", "page-2"],
    ]


def test_rejects_unaccepted_input_kind() -> None:
    with pytest.raises(ValueError, match="accepted_input_kinds"):
        RunnerBatchPlanner().plan(
            artifacts(1, kind=InputKind.PDF),
            capability(accepted_input_kinds=[InputKind.IMAGE, InputKind.PREPARED_UNIT]),
            policy(),
        )


def test_planning_preserves_stable_batch_ids() -> None:
    refs = artifacts(5)
    cap = capability()
    pol = policy(batch_size=2, warmup_batch_count=0)
    first = RunnerBatchPlanner().plan(refs, cap, pol)
    second = RunnerBatchPlanner().plan(refs, cap, pol)
    assert [batch.batch_id for batch in first] == [batch.batch_id for batch in second]


def test_warmup_batches_are_marked() -> None:
    batches = RunnerBatchPlanner().plan(
        artifacts(8),
        capability(),
        policy(batch_size=2, warmup_batch_count=2),
    )
    assert [batch.warmup for batch in batches] == [True, True, False, False]


def test_rejects_run_exceeding_item_cap() -> None:
    with pytest.raises(ValueError, match="max_items_per_run"):
        RunnerBatchPlanner().plan(
            artifacts(5),
            capability(),
            policy(
                batch_size=2,
                endpoint={
                    **runner_policy_payload()["endpoint"],  # type: ignore[index]
                    "max_items_per_run": 4,
                    "estimated_cost_per_item_usd": Decimal("0.01"),
                    "max_run_cost_usd": Decimal("1.00"),
                },
            ),
        )


def test_rejects_run_exceeding_cost_cap() -> None:
    base = policy(batch_size=5)
    invalid_endpoint = HostedEndpointPolicy.model_construct(
        endpoint_name=base.endpoint.endpoint_name,
        endpoint_key=base.endpoint.endpoint_key,
        hardware_class=base.endpoint.hardware_class,
        cold_start_timeout_seconds=base.endpoint.cold_start_timeout_seconds,
        request_timeout_seconds=base.endpoint.request_timeout_seconds,
        retryable_status_codes=base.endpoint.retryable_status_codes,
        scale_to_zero=base.endpoint.scale_to_zero,
        max_items_per_run=10,
        estimated_cost_per_item_usd=Decimal("0.25"),
        max_run_cost_usd=Decimal("1.00"),
        artifact_retention_days=base.endpoint.artifact_retention_days,
    )
    run_policy = RunnerExecutionPolicy.model_construct(
        policy_id=base.policy_id,
        version=base.version,
        batch_size=base.batch_size,
        target_longest_image_dim=base.target_longest_image_dim,
        preserve_page_local_groups=base.preserve_page_local_groups,
        packaging_strategy=base.packaging_strategy,
        warmup_batch_count=base.warmup_batch_count,
        retry_mode=base.retry_mode,
        max_retries=base.max_retries,
        endpoint=invalid_endpoint,
    )
    with pytest.raises(ValueError, match="max_run_cost_usd"):
        RunnerBatchPlanner().plan(artifacts(5), capability(), run_policy)


def test_direct_packaging_strategy_chunks_one_item() -> None:
    batches = RunnerBatchPlanner().plan(
        artifacts(3),
        capability(),
        policy(batch_size=4, packaging_strategy=PackagingStrategy.DIRECT),
    )
    assert [len(batch.items) for batch in batches] == [1, 1, 1]
