# Copyright (C) 2026 Chris Malek.
"""Checksum verification report models for Spec 0002 bundle inspection."""

from __future__ import annotations

from enum import StrEnum

from wordwending.models.ocr import SchemaModel


class ChecksumVerificationStatus(StrEnum):
    """Outcome for one recorded checksum field verified against on-disk bytes."""

    #: On-disk bytes match the recorded digest label.
    OK = "OK"
    #: Recorded digest does not match on-disk bytes or the file is missing.
    FAIL = "FAIL"
    #: No digest was recorded for this artifact path.
    SKIPPED = "SKIPPED"


class ChecksumVerificationResult(SchemaModel):
    """One bundle-relative path checked against a recorded digest label."""

    #: Bundle-relative artifact path that was inspected.
    artifact_path: str
    #: Recorded digest label from bundle layout metadata, when present.
    recorded_checksum: str | None = None
    #: Digest label computed from on-disk bytes when verification ran.
    computed_checksum: str | None = None
    #: Verification outcome for this artifact.
    status: ChecksumVerificationStatus
    #: Operator-visible detail for skips and failures.
    detail: str | None = None


class BundleChecksumReport(SchemaModel):
    """Aggregate checksum verification results for one bundle root."""

    #: Per-artifact verification outcomes in stable inspection order.
    results: list[ChecksumVerificationResult]

    @property
    def all_ok(self) -> bool:
        """
        Return whether every non-skipped verification succeeded.

        Returns:
            ``True`` when no result has ``FAIL`` status.

        """
        return all(
            result.status != ChecksumVerificationStatus.FAIL for result in self.results
        )
