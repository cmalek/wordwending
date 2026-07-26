# Phase 1 PAGE/eScriptorium Interoperability Spike Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove that two representative pages can pass through PAGE XML and eScriptorium correction, then return to validated `bochord` page bundles without losing required evidence.

**Architecture:** Keep `BundlePage` JSON canonical. A small `PageXmlInterchangeService` writes PAGE XML plus an untouched `BundlePage` sidecar, then merges corrected PAGE fields back into that sidecar by stable object id. eScriptorium remains a manual external gate; no review UI or OCR engine is built.

**Tech Stack:** Python 3.13, Pydantic 2, `xml.etree.ElementTree`, `zipfile`, pytest, eScriptorium PAGE import/export.

## Global Constraints

- Use PDF page 100 from `sources/anglo_saxon_dictionary_concise.pdf` as dense dictionary fixture.
- Use PDF page 10 from `sources/Kiparsky-PhonologyOldEnglish-1976.pdf` as prose, formula, superscript marker, and footnote fixture.
- Public truth remains validated JSON; PAGE XML is interchange only.
- Preserve stable ids, source/prepared coordinate identity, text, typography, geometry, reading order, and note links.
- Never run OCR models locally.
- Do not add `ocrd`, `ocrd-models`, XML framework, review UI, CLI command, or generic plugin interface in this spike.
- Stop after decision record. Phase 4 work starts only if exit gate passes.
- Follow repository Napoleon docstrings and `#:` attribute comments on all non-test Python.
- Give Cursor one task section at a time plus only its listed files.

## Dependency Decision

`ocrd-models` latest registry release is `2.67.1` from 2024, while OCR-D's
published support matrix only claims partial core support through Python
3.11/3.12 and this repo requires Python 3.13. Use stdlib XML for this bounded
subset. Reconsider OCR-D core only after the real round trip proves a workspace
API would replace maintained code.

---

## File Map

- Create: `bochord/services/__init__.py` — service package marker.
- Create: `bochord/services/page_interchange.py` — PAGE XML export/import boundary.
- Create: `tests/test_page_interchange.py` — pure round-trip and recorded-export checks.
- Create: `tests/fixtures/interchange/dictionary-page.base.json` — canonical dictionary `BundlePage`.
- Create: `tests/fixtures/interchange/note-page.base.json` — canonical note `BundlePage`.
- Create after eScriptorium export: `tests/fixtures/interchange/dictionary-page.corrected.xml`.
- Create after eScriptorium export: `tests/fixtures/interchange/note-page.corrected.xml`.
- Create: `doc/source/architecture/spike_0001_page_escriptorium.rst` — evidence and adopt/reject decision.
- Modify: `doc/source/architecture/index.rst` — include spike decision record.

### Task 1: Canonical PAGE XML Boundary

**Files:**

- Create: `bochord/services/__init__.py`
- Create: `bochord/services/page_interchange.py`
- Create: `tests/test_page_interchange.py`
- Create: `tests/fixtures/interchange/dictionary-page.base.json`
- Create: `tests/fixtures/interchange/note-page.base.json`

**Interfaces:**

- Consumes: `BundlePage`, `BoundingBox`, `LineRecord`, `NoteRecord`, `Polygon`, `RegionRecord`, `SpanRecord`, `Typography`.
- Produces:

```python
class PageXmlInterchangeService:
    def export_review_package(
        self,
        page: BundlePage,
        image_path: Path,
        output_dir: Path,
    ) -> Path: ...

    def import_corrected_page(
        self,
        page_xml_path: Path,
        sidecar_path: Path,
    ) -> BundlePage: ...
```

- Package layout:

```text
<output_dir>/
  <page_id>.review.zip       # image + PAGE XML for eScriptorium
  <page_id>.bochord.json     # canonical sidecar; never sent through XML
```

- PAGE mapping:

| `bochord` | PAGE 2019-07-15 |
|---|---|
| prepared image | `Page@imageFilename`, width, height |
| `RegionRecord` | `TextRegion@id`, `@type`, `Coords` |
| region order | `ReadingOrder/OrderedGroup/RegionRefIndexed@index` |
| `LineRecord` | `TextLine@id`, `Coords`, `Baseline` |
| `SpanRecord` | `Word@id`, `Coords`, `TextStyle`, `TextEquiv/Unicode` |
| `NoteRecord` | points to footnote `RegionRecord`; full linkage retained in JSON sidecar |
| transform/checksum/provenance/review | JSON sidecar only |

- Import rule: PAGE may update text, PAGE-supported typography, geometry, and reading order. Sidecar-only provenance, review state, note linkage, transforms, checksums, and alternate evidence remain byte-for-byte semantically unchanged.

- [ ] **Step 1: Write failing export/import tests**

```python
from pathlib import Path

from bochord.models import BundlePage, FontSlant
from bochord.services.page_interchange import PageXmlInterchangeService


def test_page_xml_round_trip_keeps_page_contract(tmp_path: Path) -> None:
    base = BundlePage.model_validate_json(
        Path("tests/fixtures/interchange/note-page.base.json").read_text()
    )
    image = tmp_path / "note-page.png"
    image.write_bytes(b"fixture-image")
    service = PageXmlInterchangeService()

    package = service.export_review_package(base, image, tmp_path)
    returned = service.import_corrected_page(
        tmp_path / "page-0010.xml",
        tmp_path / "page-0010.bochord.json",
    )

    assert package.name == "page-0010.review.zip"
    assert returned.page_id == base.page_id
    assert returned.prepared_page == base.prepared_page
    assert returned.notes[0].linked_marker_span_ids == ["span-note-marker-10"]
    assert returned.spans[0].typography.slant is FontSlant.ITALIC
```

```python
def test_corrected_page_xml_updates_only_page_fields(tmp_path: Path) -> None:
    base = BundlePage.model_validate_json(
        Path("tests/fixtures/interchange/dictionary-page.base.json").read_text()
    )
    service = PageXmlInterchangeService()
    package = service.export_review_package(base, Path("page.png"), tmp_path)
    page_xml = tmp_path / "page-0100.xml"
    xml = page_xml.read_text().replace("dreorig", "drēorig")
    page_xml.write_text(xml, encoding="utf-8")

    returned = service.import_corrected_page(
        page_xml,
        tmp_path / "page-0100.bochord.json",
    )

    assert returned.spans[0].text_diplomatic == "drēorig"
    assert returned.spans[0].provenance == base.spans[0].provenance
    assert returned.prepared_page.transforms == base.prepared_page.transforms
```

- [ ] **Step 2: Run tests and verify missing service failure**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_page_interchange.py
```

Expected: collection fails with `ModuleNotFoundError: No module named 'bochord.services'`.

- [ ] **Step 3: Create two minimal canonical fixture bundles**

Dictionary fixture must contain:

- `page_id="page-0100"`, `page_number=100`, two ordered regions.
- At least one line baseline and one polygon.
- Spans `dreorig` and `sorrow`; `sorrow` is italic.
- Prepared image checksum, coordinate space, and one source-to-prepared transform.

Note fixture must contain:

- `page_id="page-0010"`, `page_number=10`.
- Main region plus `footnote-block` region.
- Superscript marker span `span-note-marker-10`.
- Note `note-10` linked to that marker.
- At least one italic span and one baseline.

Validate both files during creation:

```bash
source .venv/bin/activate
rtk python -c 'from pathlib import Path; from bochord.models import BundlePage; [BundlePage.model_validate_json(path.read_text()) for path in Path("tests/fixtures/interchange").glob("*.base.json")]'
```

Expected: exit 0.

- [ ] **Step 4: Implement minimal stdlib serializer and importer**

Use one namespace constant and strict id lookup:

```python
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
import xml.etree.ElementTree as ET

from bochord.models import BundlePage

PAGE_NS = "http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15"
NS = {"pc": PAGE_NS}
ET.register_namespace("", PAGE_NS)


class PageXmlInterchangeService:
    """Round-trip canonical page evidence through PAGE review packages."""

    def export_review_package(
        self,
        page: BundlePage,
        image_path: Path,
        output_dir: Path,
    ) -> Path:
        """Write PAGE review ZIP and canonical JSON sidecar."""
        output_dir.mkdir(parents=True, exist_ok=True)
        xml_path = output_dir / f"{page.page_id}.xml"
        sidecar_path = output_dir / f"{page.page_id}.bochord.json"
        self._write_page_xml(page, image_path.name, xml_path)
        sidecar_path.write_text(page.model_dump_json(indent=2) + "\n", encoding="utf-8")
        zip_path = output_dir / f"{page.page_id}.review.zip"
        with ZipFile(zip_path, "w", ZIP_DEFLATED) as archive:
            archive.write(image_path, image_path.name)
            archive.write(xml_path, xml_path.name)
        return zip_path

    def import_corrected_page(
        self,
        page_xml_path: Path,
        sidecar_path: Path,
    ) -> BundlePage:
        """Merge PAGE-supported corrections into canonical sidecar data."""
        base = BundlePage.model_validate_json(sidecar_path.read_text(encoding="utf-8"))
        root = ET.parse(page_xml_path).getroot()
        if root.tag != f"{{{PAGE_NS}}}PcGts":
            raise ValueError("expected PAGE 2019-07-15 PcGts root")
        return self._merge_page(root, base)
```

Keep `_write_page_xml` and `_merge_page` under 60 lines each. Split element conversion into `_region_element`, `_line_element`, `_word_element`, `_coords`, and `_text_style`. Reject missing or duplicate stable ids instead of positional matching.

- [ ] **Step 5: Run targeted tests**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_page_interchange.py
```

Expected: all pass.

- [ ] **Step 6: Commit**

```bash
rtk git add bochord/services tests/test_page_interchange.py tests/fixtures/interchange
rtk git commit -m "feat: add PAGE interchange spike boundary"
```

### Task 2: Real eScriptorium Round Trip

**Files:**

- Create: `tests/fixtures/interchange/dictionary-page.corrected.xml`
- Create: `tests/fixtures/interchange/note-page.corrected.xml`

**Interfaces:**

- Consumes: Task 1 review ZIPs and sidecars.
- Produces: recorded PAGE exports from eScriptorium for permanent regression checks.

- [ ] **Step 1: Render exact source pages**

```bash
rtk mkdir -p /tmp/bochord-page-spike
rtk pdftoppm -f 100 -l 100 -r 300 -png \
  sources/anglo_saxon_dictionary_concise.pdf \
  /tmp/bochord-page-spike/dictionary
rtk pdftoppm -f 10 -l 10 -r 300 -png \
  sources/Kiparsky-PhonologyOldEnglish-1976.pdf \
  /tmp/bochord-page-spike/note
```

Expected files: `dictionary-100.png`, `note-10.png`.

- [ ] **Step 2: Export review packages**

```bash
source .venv/bin/activate
rtk python - <<'PY'
from pathlib import Path

from bochord.models import BundlePage
from bochord.services.page_interchange import PageXmlInterchangeService

root = Path("/tmp/bochord-page-spike")
cases = {
    "dictionary-page": root / "dictionary-100.png",
    "note-page": root / "note-10.png",
}
service = PageXmlInterchangeService()
for stem, image in cases.items():
    payload = Path(f"tests/fixtures/interchange/{stem}.base.json").read_text()
    service.export_review_package(BundlePage.model_validate_json(payload), image, root)
PY
```

Expected outputs:

```text
/tmp/bochord-page-spike/page-0100.review.zip
/tmp/bochord-page-spike/page-0100.bochord.json
/tmp/bochord-page-spike/page-0010.review.zip
/tmp/bochord-page-spike/page-0010.bochord.json
```

- [ ] **Step 3: Import and correct in eScriptorium**

For each ZIP:

1. Import image.
2. Import PAGE transcription with override enabled.
3. Dictionary page: change `dreorig` to `drēorig`; preserve italic `sorrow`.
4. Note page: change one main-text token; preserve marker `10`, footnote region, baselines, and region order.
5. Export PAGE without images.
6. Copy returned PAGE XML to the matching `tests/fixtures/interchange/*.corrected.xml` path.

- [ ] **Step 4: Verify stable ids survived**

```bash
rtk rg -n 'page-0100|region-|line-|span-' \
  tests/fixtures/interchange/dictionary-page.corrected.xml
rtk rg -n 'page-0010|region-|line-|span-note-marker-10' \
  tests/fixtures/interchange/note-page.corrected.xml
```

Expected: original region, line, and span ids remain. If eScriptorium replaces any required id, stop Task 2 and record Phase 1 as failed; do not add fuzzy coordinate matching.

- [ ] **Step 5: Commit recorded exports**

```bash
rtk git add tests/fixtures/interchange/*.corrected.xml
rtk git commit -m "test: record eScriptorium PAGE round trip"
```

### Task 3: Exit Gate and Decision Record

**Files:**

- Modify: `tests/test_page_interchange.py`
- Create: `doc/source/architecture/spike_0001_page_escriptorium.rst`
- Modify: `doc/source/architecture/index.rst`

**Interfaces:**

- Consumes: recorded corrected PAGE XML plus canonical sidecars.
- Produces: repeatable exit test and explicit `adopt`, `adopt-with-sidecar`, or `reject` decision.

- [ ] **Step 1: Add recorded-export regression test**

```python
import pytest


@pytest.mark.parametrize(
    ("stem", "corrected_text"),
    [
        ("dictionary-page", "drēorig"),
        ("note-page", "Deletion"),
    ],
)
def test_recorded_escriptorium_export_returns_to_bundle(
    stem: str,
    corrected_text: str,
) -> None:
    fixture_dir = Path("tests/fixtures/interchange")
    page = PageXmlInterchangeService().import_corrected_page(
        fixture_dir / f"{stem}.corrected.xml",
        fixture_dir / f"{stem}.base.json",
    )

    assert corrected_text in " ".join(span.text_diplomatic for span in page.spans)
    assert page.prepared_page.image_checksum
    assert page.prepared_page.transforms
    assert any(line.baseline for line in page.lines)
```

Add explicit assertions for:

- region reading order;
- italic and superscript facets;
- marker `span-note-marker-10` to `note-10` linkage;
- unchanged source page id, coordinate-space id, witness ids, runner ids, and review state.

- [ ] **Step 2: Run exit test**

```bash
source .venv/bin/activate
rtk pytest -q tests/test_page_interchange.py
```

Expected: all pass twice without fixture changes.

- [ ] **Step 3: Write decision record**

Record:

- exact eScriptorium version/instance date;
- fields preserved directly by PAGE;
- fields restored from canonical JSON sidecar;
- any unsupported correction action;
- final decision.

Decision rule:

- `adopt`: all required fields survive PAGE directly.
- `adopt-with-sidecar`: PAGE carries editable evidence and stable ids; sidecar safely retains `bochord`-only provenance/linkage.
- `reject`: stable ids or editable text/geometry cannot round-trip.

- [ ] **Step 4: Run final quality gate**

```bash
source .venv/bin/activate
rtk ruff check bochord/services/page_interchange.py tests/test_page_interchange.py
rtk .venv/bin/mypy bochord/services/page_interchange.py
rtk make napoleon-gate
rtk pytest -q
```

Expected: all pass.

- [ ] **Step 5: Commit**

```bash
rtk git add bochord/services/page_interchange.py tests/test_page_interchange.py \
  doc/source/architecture/spike_0001_page_escriptorium.rst \
  doc/source/architecture/index.rst
rtk git commit -m "docs: record PAGE interoperability decision"
```

## Cost Stop

Stop here. No OCR-D workspace manager, review UI, fuzzy object matcher, or production review workflow. Add one only when recorded Phase 1 evidence proves sidecar + stable ids insufficient.
