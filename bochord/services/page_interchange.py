# Copyright (C) 2026 Chris Malek.
"""PAGE XML review-package interchange for canonical page bundles."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path  # noqa: TC003
from zipfile import ZIP_DEFLATED, ZipFile

from bochord.models import (
    BaselineShift,
    BoundingBox,
    BundlePage,
    FontSlant,
    LineRecord,
    Point,
    Polygon,
    RegionRecord,
    SpanRecord,
    Typography,
)

#: PAGE 2019-07-15 XML namespace used for review-package interchange.
PAGE_NS = "http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15"
#: ElementTree namespace map for PAGE XML parsing helpers.
NS = {"pc": PAGE_NS}
ET.register_namespace("", PAGE_NS)
#: Minimum vertex count required to reconstruct polygon geometry from PAGE.
_MIN_POLYGON_POINTS = 3


class PageXmlInterchangeService:
    """Round-trip canonical page evidence through PAGE review packages."""

    def export_review_package(
        self,
        page: BundlePage,
        image_path: Path,
        output_dir: Path,
    ) -> Path:
        """
        Write PAGE review ZIP and canonical JSON sidecar.

        Args:
            page: Canonical page bundle to export.
            image_path: Prepared page image included in the review ZIP.
            output_dir: Directory receiving XML, sidecar, and ZIP outputs.

        Returns:
            Path to the review ZIP written for eScriptorium import.

        """
        output_dir.mkdir(parents=True, exist_ok=True)
        xml_path = output_dir / f"{page.page_id}.xml"
        sidecar_path = output_dir / f"{page.page_id}.bochord.json"
        self._write_page_xml(page, image_path.name, xml_path)
        sidecar_path.write_text(
            page.model_dump_json(indent=2) + "\n",
            encoding="utf-8",
        )
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
        """
        Merge PAGE-supported corrections into canonical sidecar data.

        Args:
            page_xml_path: Corrected PAGE XML returned from review.
            sidecar_path: Canonical JSON sidecar written during export.

        Returns:
            Updated bundle page with PAGE corrections applied.

        Raises:
            ValueError: If the XML root or required stable ids are invalid.

        """
        base = BundlePage.model_validate_json(
            sidecar_path.read_text(encoding="utf-8"),
        )
        root = ET.parse(page_xml_path).getroot()  # noqa: S314
        if root.tag != f"{{{PAGE_NS}}}PcGts":
            msg = "expected PAGE 2019-07-15 PcGts root"
            raise ValueError(msg)
        return self._merge_page(root, base)

    def _write_page_xml(
        self,
        page: BundlePage,
        image_filename: str,
        xml_path: Path,
    ) -> None:
        """Serialize one bundle page to PAGE 2019-07-15 XML."""
        space = page.prepared_page.coordinate_space
        root = ET.Element(f"{{{PAGE_NS}}}PcGts")
        page_el = ET.SubElement(
            root,
            f"{{{PAGE_NS}}}Page",
            imageFilename=image_filename,
            imageWidth=str(space.width_px),
            imageHeight=str(space.height_px),
        )
        lines_by_id = {line.line_id: line for line in page.lines}
        spans_by_id = {span.span_id: span for span in page.spans}
        ordered_regions = sorted(
            page.regions,
            key=lambda region: region.reading_order_index,
        )
        for region in ordered_regions:
            region_el = self._region_element(region)
            for line_id in region.line_ids:
                line_el = self._line_element(lines_by_id[line_id])
                for span_id in lines_by_id[line_id].span_ids:
                    line_el.append(self._word_element(spans_by_id[span_id]))
                region_el.append(line_el)
            page_el.append(region_el)
        reading_order = ET.SubElement(page_el, f"{{{PAGE_NS}}}ReadingOrder")
        ordered_group = ET.SubElement(
            reading_order,
            f"{{{PAGE_NS}}}OrderedGroup",
            id="reading-order-1",
        )
        for index, region in enumerate(ordered_regions):
            ET.SubElement(
                ordered_group,
                f"{{{PAGE_NS}}}RegionRefIndexed",
                index=str(index),
                regionRef=region.region_id,
            )
        ET.ElementTree(root).write(
            xml_path,
            encoding="utf-8",
            xml_declaration=True,
        )

    def _merge_page(self, root: ET.Element, base: BundlePage) -> BundlePage:
        """Apply PAGE-supported field updates onto the canonical sidecar."""
        page_el = root.find(f"{{{PAGE_NS}}}Page")
        if page_el is None:
            msg = "PAGE document missing Page element"
            raise ValueError(msg)
        space_id = base.prepared_page.coordinate_space.space_id
        region_elements = self._indexed_children(page_el, "TextRegion")
        line_elements, word_elements = self._collect_line_and_word_elements(
            region_elements,
        )
        reading_order = self._reading_order_indices(page_el)
        regions = self._merge_regions(
            base.regions,
            region_elements,
            reading_order,
            space_id,
        )
        lines = self._merge_lines(base.lines, line_elements, space_id)
        spans = self._merge_spans(base.spans, word_elements, space_id)
        return base.model_copy(
            update={"regions": regions, "lines": lines, "spans": spans},
        )

    def _collect_line_and_word_elements(
        self,
        region_elements: dict[str, ET.Element],
    ) -> tuple[dict[str, ET.Element], dict[str, ET.Element]]:
        """Index TextLine and Word elements by stable id."""
        line_elements: dict[str, ET.Element] = {}
        word_elements: dict[str, ET.Element] = {}
        for region_el in region_elements.values():
            for line_el in region_el.findall(f"{{{PAGE_NS}}}TextLine"):
                line_id = line_el.get("id")
                if line_id is None:
                    msg = "TextLine missing stable id"
                    raise ValueError(msg)
                if line_id in line_elements:
                    msg = f"duplicate line id {line_id}"
                    raise ValueError(msg)
                line_elements[line_id] = line_el
                for word_el in line_el.findall(f"{{{PAGE_NS}}}Word"):
                    word_id = word_el.get("id")
                    if word_id is None:
                        msg = "Word missing stable id"
                        raise ValueError(msg)
                    if word_id in word_elements:
                        msg = f"duplicate word id {word_id}"
                        raise ValueError(msg)
                    word_elements[word_id] = word_el
        return line_elements, word_elements

    def _merge_regions(
        self,
        regions: list[RegionRecord],
        region_elements: dict[str, ET.Element],
        reading_order: dict[str, int],
        space_id: str,
    ) -> list[RegionRecord]:
        """Merge PAGE region geometry and reading order."""
        merged = [
            self._merge_region(
                region,
                region_elements[region.region_id],
                reading_order.get(region.region_id, region.reading_order_index),
                space_id,
            )
            for region in regions
            if region.region_id in region_elements
        ]
        if len(merged) != len(regions):
            missing = sorted(
                {region.region_id for region in regions} - set(region_elements),
            )
            msg = f"missing region ids: {', '.join(missing)}"
            raise ValueError(msg)
        return merged

    def _merge_lines(
        self,
        lines: list[LineRecord],
        line_elements: dict[str, ET.Element],
        space_id: str,
    ) -> list[LineRecord]:
        """Merge PAGE line geometry for every canonical line id."""
        merged = [
            self._merge_line(line, line_elements[line.line_id], space_id)
            for line in lines
            if line.line_id in line_elements
        ]
        if len(merged) != len(lines):
            missing = sorted(
                {line.line_id for line in lines} - set(line_elements),
            )
            msg = f"missing line ids: {', '.join(missing)}"
            raise ValueError(msg)
        return merged

    def _merge_spans(
        self,
        spans: list[SpanRecord],
        word_elements: dict[str, ET.Element],
        space_id: str,
    ) -> list[SpanRecord]:
        """Merge PAGE word text and typography for every canonical span id."""
        merged = [
            self._merge_span(span, word_elements[span.span_id], space_id)
            for span in spans
            if span.span_id in word_elements
        ]
        if len(merged) != len(spans):
            missing = sorted(
                {span.span_id for span in spans} - set(word_elements),
            )
            msg = f"missing word ids: {', '.join(missing)}"
            raise ValueError(msg)
        return merged

    def _region_element(self, region: RegionRecord) -> ET.Element:
        """Build one PAGE TextRegion from a canonical region record."""
        region_el = ET.Element(
            f"{{{PAGE_NS}}}TextRegion",
            id=region.region_id,
            type=region.region_kind.value,
        )
        if region.bounding_box is not None:
            region_el.append(self._coords(region.bounding_box))
        elif region.polygon is not None:
            region_el.append(self._coords_from_polygon(region.polygon))
        return region_el

    def _line_element(self, line: LineRecord) -> ET.Element:
        """Build one PAGE TextLine from a canonical line record."""
        line_el = ET.Element(f"{{{PAGE_NS}}}TextLine", id=line.line_id)
        if line.polygon is not None:
            line_el.append(self._coords_from_polygon(line.polygon))
        elif line.bounding_box is not None:
            line_el.append(self._coords(line.bounding_box))
        if line.baseline:
            line_el.append(self._baseline_element(line.baseline))
        return line_el

    def _word_element(self, span: SpanRecord) -> ET.Element:
        """Build one PAGE Word from a canonical span record."""
        word_el = ET.Element(f"{{{PAGE_NS}}}Word", id=span.span_id)
        if span.bounding_box is not None:
            word_el.append(self._coords(span.bounding_box))
        text_style = self._text_style(span.typography)
        if text_style is not None:
            word_el.append(text_style)
        text_equiv = ET.SubElement(word_el, f"{{{PAGE_NS}}}TextEquiv")
        unicode_el = ET.SubElement(text_equiv, f"{{{PAGE_NS}}}Unicode")
        unicode_el.text = span.text_diplomatic
        return word_el

    def _coords(self, bounding_box: BoundingBox) -> ET.Element:
        """Convert one axis-aligned box to PAGE Coords."""
        points = (
            f"{bounding_box.x0},{bounding_box.y0} "
            f"{bounding_box.x1},{bounding_box.y0} "
            f"{bounding_box.x1},{bounding_box.y1} "
            f"{bounding_box.x0},{bounding_box.y1}"
        )
        return ET.Element(f"{{{PAGE_NS}}}Coords", points=points)

    def _coords_from_polygon(self, polygon: Polygon) -> ET.Element:
        """Convert one polygon to PAGE Coords."""
        points = " ".join(f"{point.x},{point.y}" for point in polygon.points)
        return ET.Element(f"{{{PAGE_NS}}}Coords", points=points)

    def _baseline_element(self, baseline: list[Point]) -> ET.Element:
        """Convert one baseline polyline to PAGE Baseline."""
        points = " ".join(f"{point.x},{point.y}" for point in baseline)
        return ET.Element(f"{{{PAGE_NS}}}Baseline", points=points)

    def _text_style(self, typography: Typography) -> ET.Element | None:
        """Map supported typography facets to PAGE TextStyle."""
        attrs: dict[str, str] = {}
        if typography.slant is FontSlant.ITALIC:
            attrs["italic"] = "true"
        if typography.baseline_shift is BaselineShift.SUPERSCRIPT:
            attrs["superscript"] = "true"
        if not attrs:
            return None
        return ET.Element(f"{{{PAGE_NS}}}TextStyle", attrs)

    def _indexed_children(
        self,
        parent: ET.Element,
        tag_name: str,
    ) -> dict[str, ET.Element]:
        """Index direct child elements by stable id, rejecting duplicates."""
        indexed: dict[str, ET.Element] = {}
        for child in parent.findall(f"{{{PAGE_NS}}}{tag_name}"):
            child_id = child.get("id")
            if child_id is None:
                msg = f"{tag_name} missing stable id"
                raise ValueError(msg)
            if child_id in indexed:
                msg = f"duplicate {tag_name.lower()} id {child_id}"
                raise ValueError(msg)
            indexed[child_id] = child
        return indexed

    def _reading_order_indices(self, page_el: ET.Element) -> dict[str, int]:
        """Read region reading-order indices from PAGE ReadingOrder."""
        indices: dict[str, int] = {}
        reading_order = page_el.find(f"{{{PAGE_NS}}}ReadingOrder")
        if reading_order is None:
            return indices
        for ref in reading_order.iter(f"{{{PAGE_NS}}}RegionRefIndexed"):
            region_ref = ref.get("regionRef")
            if region_ref is None:
                continue
            indices[region_ref] = int(ref.get("index", "0")) + 1
        return indices

    def _merge_region(
        self,
        region: RegionRecord,
        region_el: ET.Element,
        reading_order_index: int,
        space_id: str,
    ) -> RegionRecord:
        """Merge PAGE geometry and reading order into one region record."""
        coords = region_el.find(f"{{{PAGE_NS}}}Coords")
        polygon = self._polygon_from_coords(coords, space_id)
        bounding_box = self._bbox_from_coords(coords, space_id)
        return region.model_copy(
            update={
                "reading_order_index": reading_order_index,
                "bounding_box": bounding_box or region.bounding_box,
                "polygon": polygon or region.polygon,
            },
        )

    def _merge_line(
        self,
        line: LineRecord,
        line_el: ET.Element,
        space_id: str,
    ) -> LineRecord:
        """Merge PAGE geometry into one line record."""
        coords = line_el.find(f"{{{PAGE_NS}}}Coords")
        baseline_el = line_el.find(f"{{{PAGE_NS}}}Baseline")
        polygon = self._polygon_from_coords(coords, space_id)
        bounding_box = self._bbox_from_coords(coords, space_id)
        baseline = self._points_from_coords(baseline_el)
        return line.model_copy(
            update={
                "bounding_box": bounding_box or line.bounding_box,
                "polygon": polygon or line.polygon,
                "baseline": baseline or line.baseline,
            },
        )

    def _merge_span(
        self,
        span: SpanRecord,
        word_el: ET.Element,
        space_id: str,
    ) -> SpanRecord:
        """Merge PAGE text, typography, and geometry into one span record."""
        coords = word_el.find(f"{{{PAGE_NS}}}Coords")
        unicode_el = word_el.find(f".//{{{PAGE_NS}}}Unicode")
        text_diplomatic = span.text_diplomatic
        if unicode_el is not None and unicode_el.text is not None:
            text_diplomatic = unicode_el.text
        typography = self._typography_from_text_style(
            word_el.find(f"{{{PAGE_NS}}}TextStyle"),
            span.typography,
        )
        bounding_box = self._bbox_from_coords(coords, space_id)
        return span.model_copy(
            update={
                "text_diplomatic": text_diplomatic,
                "typography": typography,
                "bounding_box": bounding_box or span.bounding_box,
            },
        )

    def _typography_from_text_style(
        self,
        text_style: ET.Element | None,
        base: Typography,
    ) -> Typography:
        """Apply PAGE TextStyle updates onto canonical typography."""
        if text_style is None:
            return base
        updates: dict[str, FontSlant | BaselineShift] = {}
        italic = text_style.get("italic")
        if italic == "true":
            updates["slant"] = FontSlant.ITALIC
        elif italic == "false":
            updates["slant"] = FontSlant.UPRIGHT
        superscript = text_style.get("superscript")
        if superscript == "true":
            updates["baseline_shift"] = BaselineShift.SUPERSCRIPT
        elif superscript == "false":
            updates["baseline_shift"] = BaselineShift.BASELINE
        return base.model_copy(update=updates)

    def _parse_points(self, points: str) -> list[tuple[float, float]]:
        """Parse PAGE point strings into coordinate pairs."""
        parsed: list[tuple[float, float]] = []
        for token in points.split():
            if not token:
                continue
            x_text, y_text = token.split(",", maxsplit=1)
            parsed.append((float(x_text), float(y_text)))
        return parsed

    def _bbox_from_coords(
        self,
        coords: ET.Element | None,
        space_id: str,
    ) -> BoundingBox | None:
        """Derive one axis-aligned box from PAGE Coords."""
        if coords is None:
            return None
        points = self._parse_points(coords.get("points", ""))
        if not points:
            return None
        xs = [point[0] for point in points]
        ys = [point[1] for point in points]
        return BoundingBox(
            x0=min(xs),
            y0=min(ys),
            x1=max(xs),
            y1=max(ys),
            coordinate_space_id=space_id,
        )

    def _polygon_from_coords(
        self,
        coords: ET.Element | None,
        space_id: str,
    ) -> Polygon | None:
        """Derive one polygon from PAGE Coords when enough points exist."""
        if coords is None:
            return None
        points = self._parse_points(coords.get("points", ""))
        if len(points) < _MIN_POLYGON_POINTS:
            return None
        return Polygon(
            coordinate_space_id=space_id,
            points=[Point(x=x, y=y) for x, y in points],
        )

    def _points_from_coords(self, element: ET.Element | None) -> list[Point]:
        """Derive one point list from PAGE Baseline or Coords."""
        if element is None:
            return []
        return [
            Point(x=x, y=y)
            for x, y in self._parse_points(element.get("points", ""))
        ]
