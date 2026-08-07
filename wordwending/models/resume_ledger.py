# Copyright (C) 2026 Chris Malek.
"""Resume ledger contracts for completed runner batches."""

from __future__ import annotations

from datetime import datetime  # noqa: TC003

from pydantic import Field

from wordwending.models.ocr import SchemaModel

#: On-disk ledger filename under ``bundle_root``.
RESUME_LEDGER_FILENAME = "runner-resume-ledger.json"
#: Schema version persisted with every ledger document.
RESUME_LEDGER_SCHEMA_VERSION = "1.0.0"


class ResumeLedgerEntry(SchemaModel):
    """One successfully completed runner batch recorded for resume."""

    #: Stable planned batch identifier (matches ``PlannedRunnerBatch.batch_id``).
    batch_id: str
    #: Execution run identifier that completed the batch.
    run_id: str
    #: Document identifier under processing when the batch completed.
    document_id: str
    #: Source page ids included in the completed batch.
    source_page_ids: list[str] = Field(min_length=1)
    #: UTC timestamp when the batch was recorded as complete.
    completed_at_utc: datetime


class ResumeLedger(SchemaModel):
    """Persisted set of successfully completed runner batches under a bundle."""

    #: Ledger schema version.
    schema_version: str = RESUME_LEDGER_SCHEMA_VERSION
    #: Completed batch entries keyed by stable batch identity at load time.
    completed_batches: list[ResumeLedgerEntry] = Field(default_factory=list)
