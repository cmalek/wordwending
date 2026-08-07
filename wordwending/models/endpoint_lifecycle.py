# Copyright (C) 2026 Chris Malek.
"""Hugging Face Inference Endpoint catalog, ledger, and lifecycle result models."""

from __future__ import annotations

from datetime import datetime  # noqa: TC003
from enum import StrEnum

from pydantic import Field, field_validator

from wordwending.models.ocr import SchemaModel

#: On-disk session ledger schema version.
ENDPOINT_SESSION_LEDGER_SCHEMA_VERSION = "1.0.0"

#: Placeholder immutable revision for the default olmocr catalog entry.
DEFAULT_OLMOCR_REVISION = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef0001"
#: Placeholder immutable revision for the default kraken catalog entry.
DEFAULT_KRAKEN_REVISION = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef0002"

#: Mutable Hub revision labels that must not be used as catalog identity.
_MUTABLE_REVISION_LABELS = frozenset({"main", "master", "latest", "head"})


def mutable_revision_rejected(revision: str) -> bool:
    """
    Return whether a Hub revision label must be rejected as mutable.

    Args:
        revision: Hub revision string from catalog input.

    Returns:
        ``True`` when the revision is a forbidden mutable label.

    """
    return revision.strip().lower() in _MUTABLE_REVISION_LABELS


class EndpointLastAction(StrEnum):
    """Last lifecycle action recorded for one endpoint session."""

    #: Endpoint was ensured up and ready for inference.
    UP = "up"
    #: Endpoint was paused or scaled down.
    DOWN = "down"
    #: Endpoint was explicitly paused without deletion.
    PAUSE = "pause"


class EndpointCatalogEntry(SchemaModel):
    """
    Catalog pin for one hosted runner's Inference Endpoint.

    Operators must replace placeholder repository and revision values before
    calling live Hugging Face APIs.
    """

    #: Stable runner identifier matching ``PassRunnerRegistry`` keys.
    runner_id: str
    #: Hub model repository (``owner/model``).
    repository: str
    #: Immutable Hub revision (commit hash); mutable labels are rejected.
    revision: str
    #: Inference Endpoint name in the hosting provider.
    endpoint_name: str
    #: Hugging Face namespace for the endpoint.
    namespace: str
    #: Accelerator class required by the HF create API.
    accelerator: str
    #: Cloud vendor for endpoint hardware.
    vendor: str
    #: Cloud region for endpoint hardware.
    region: str
    #: Instance type identifier (for example ``nvidia-a10g``).
    instance_type: str
    #: Instance size identifier (for example ``x1``).
    instance_size: str
    #: Serving framework (for example ``pytorch``).
    framework: str
    #: HF task type for the deployed model.
    task: str
    #: HF endpoint visibility/type (for example ``protected``).
    endpoint_type: str
    #: Whether HF scale-to-zero is enabled for idle cost control.
    scale_to_zero: bool = True

    @field_validator("revision")
    @classmethod
    def reject_mutable_revision(cls, revision: str) -> str:
        """
        Reject mutable Hub revision labels.

        Args:
            revision: Catalog revision string.

        Returns:
            The validated revision string.

        Raises:
            ValueError: When the revision is a forbidden mutable label.

        """
        if mutable_revision_rejected(revision):
            msg = (
                "endpoint catalog revision must be an immutable commit hash; "
                f"mutable label {revision!r} is rejected"
            )
            raise ValueError(msg)
        return revision


class EndpointLedgerEntry(SchemaModel):
    """One persisted endpoint session row without secrets."""

    #: Stable runner identifier for the session row.
    runner_id: str
    #: Inference Endpoint name in the hosting provider.
    endpoint_name: str
    #: Hugging Face namespace for the endpoint.
    namespace: str
    #: Last known HTTPS endpoint URL.
    endpoint_url: str
    #: UTC timestamp when the endpoint was last used for inference.
    last_used_at_utc: datetime
    #: Last recorded lifecycle action for the session row.
    last_action: EndpointLastAction

    @property
    def url(self) -> str:
        """
        Return the last known HTTPS endpoint URL.

        Returns:
            Stored endpoint URL for dict-style ledger access.

        """
        return self.endpoint_url


class EndpointSessionLedger(SchemaModel):
    """Persisted endpoint session ledger without API tokens."""

    #: Ledger schema version.
    schema_version: str = ENDPOINT_SESSION_LEDGER_SCHEMA_VERSION
    #: Session rows keyed by ``runner_id``.
    entries: dict[str, EndpointLedgerEntry] = Field(default_factory=dict)


class EndpointRemoteState(SchemaModel):
    """Remote Inference Endpoint snapshot from Hugging Face Hub."""

    #: Inference Endpoint name in the hosting provider.
    name: str
    #: Remote HF endpoint status string.
    status: str
    #: HTTPS endpoint URL when deployed or scaled to zero.
    url: str | None = None


class EndpointEnsureResult(SchemaModel):
    """Result of ensuring catalogued endpoints are ready."""

    #: Ready HTTPS URLs keyed by ``runner_id``.
    urls_by_runner_id: dict[str, str] = Field(default_factory=dict)
    #: Runner identifiers that were already ready without changes.
    already_ready_runner_ids: list[str] = Field(default_factory=list)
    #: Runner identifiers resumed from paused or scaled-to-zero state.
    resumed_runner_ids: list[str] = Field(default_factory=list)
    #: Runner identifiers created during ensure.
    created_runner_ids: list[str] = Field(default_factory=list)


class EndpointDownResult(SchemaModel):
    """Result of pausing or deleting catalogued endpoints."""

    #: Runner identifiers paused during down.
    paused_runner_ids: list[str] = Field(default_factory=list)
    #: Runner identifiers deleted during down.
    deleted_runner_ids: list[str] = Field(default_factory=list)


class EndpointStatusRow(SchemaModel):
    """Status for one catalogued runner endpoint."""

    #: Stable runner identifier.
    runner_id: str
    #: Inference Endpoint name in the hosting provider.
    endpoint_name: str
    #: Remote HF endpoint status string.
    hf_status: str
    #: Last known HTTPS endpoint URL, when available.
    endpoint_url: str | None = None
    #: UTC timestamp from the session ledger, when recorded.
    last_used_at_utc: datetime | None = None


class EndpointStatusReport(SchemaModel):
    """Aggregated endpoint status for selected catalog runners."""

    #: Per-runner status rows in request order.
    rows: list[EndpointStatusRow] = Field(default_factory=list)


def default_endpoint_catalog() -> list[EndpointCatalogEntry]:
    """
    Return built-in catalog entries for olmocr and kraken.

    Placeholder repository and revision values are immutable for unit tests.
    Operators must replace them before live Hugging Face deployment.

    Returns:
        Default catalog entries for supported hosted runners.

    """
    return [
        EndpointCatalogEntry(
            runner_id="olmocr",
            repository="allenai/olmOCR-7B-0225-preview",
            revision=DEFAULT_OLMOCR_REVISION,
            endpoint_name="ww-olmocr",
            namespace="operator-namespace-required",
            accelerator="gpu",
            vendor="aws",
            region="us-east-1",
            instance_type="nvidia-a10g",
            instance_size="x1",
            framework="pytorch",
            task="image-text-to-text",
            endpoint_type="protected",
            scale_to_zero=True,
        ),
        EndpointCatalogEntry(
            runner_id="kraken",
            repository="wordwending/kraken-hosted-placeholder",
            revision=DEFAULT_KRAKEN_REVISION,
            endpoint_name="ww-kraken",
            namespace="operator-namespace-required",
            accelerator="gpu",
            vendor="aws",
            region="us-east-1",
            instance_type="nvidia-a10g",
            instance_size="x1",
            framework="pytorch",
            task="image-to-text",
            endpoint_type="protected",
            scale_to_zero=True,
        ),
    ]
