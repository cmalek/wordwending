====================================
Spec 0007: PDF-to-Image Preparation
====================================

Purpose
=======

Define the v1 preparation contract for turning source PDFs or source images
into page-image inputs for downstream OCR and layout passes.

Why This Matters
================

For difficult historical OCR, preparation is not a disposable helper. It is a
major quality lever and must be reproducible, inspectable, and comparable.

Preparation must also decide when source material is too poor for trustworthy
OCR without intervention, and when one full page should be split into smaller
OCR units to recover small text effectively.

Preparation Principles
======================

- Preparation is a first-class pipeline stage.
- Prepared images are preserved artifacts, not transient scratch files.
- A change in preparation recipe creates a meaningfully distinct run input.
- Preparation must be deterministic for a given recipe and source input.
- Competing preparation recipes are allowed in v1.
- Input quality assessment is part of preparation, not a separate optional
  report.
- Page subdivision into smaller OCR units is allowed when full-page OCR would be
  materially worse.

Preparation Inputs
==================

V1 accepts:

- scanned PDF source
- page image set
- single page image

Page image sets are first-class inputs, not fallback edge cases.

Important examples:

- archive.org `.jp2` page folders
- operator-generated scan folders
- other ordered page-image directories representing one logical document

``page image set`` is intentionally format-agnostic.

V1 must not assume that page-image inputs always arrive as ``.jp2`` bundles.
Common real inputs will also include ordered folders or archives of:

- ``.png``
- ``.jpg`` or ``.jpeg``
- ``.tif`` or ``.tiff``
- mixed image formats that still preserve stable page ordering

For scanned PDFs, the system must render one prepared page image per page before
any OCR runner executes.

More precisely, PDF-to-image preparation must support two page-image acquisition
paths:

- extract an embedded page raster directly when the PDF already contains one
  usable source image per page
- render the PDF page to an image when direct extraction is unavailable or
  produces materially worse OCR inputs

The chosen path should be recorded per page in preparation provenance.

For source image sets, the system must preserve source ordering, source
filenames, and source-image provenance before producing any prepared-page
variants.

Preparation Recipe
==================

Every prepared page image must record a preparation recipe identity.

The recipe should capture, at minimum:

- source type
- PDF page-image acquisition mode when source type is ``pdf``
- render backend or renderer identity
- target DPI or equivalent target resolution
- color mode
- deskew setting
- denoise setting
- crop policy
- binarization or thresholding policy, if used
- dewarp policy, if used

Preparation recipes must be stable, named, and serializable.

Preparation Assessment
======================

Preparation must include a source-quality assessment stage before OCR runners
execute.

This assessment exists to:

- identify pages likely to fail or underperform
- decide whether a page needs alternate preparation
- decide whether a page should be subdivided into smaller OCR units
- produce operator-facing warnings before expensive OCR work proceeds

The assessment is not only informational. It is part of preparation metadata
and may affect downstream execution.

Required V1 Quality Checks
==========================

V1 preparation assessment should support explicit checks for:

- skewness
- effective resolution or DPI adequacy
- gutter shadow severity
- border shadows or dark margin artifacts
- bleed-through or show-through where detectable
- handwritten or reader markings where detectable
- large speckle or dust artifact burden
- contrast weakness
- text-size risk, especially when font appears too small for reliable
  full-page OCR

These checks may begin as deterministic heuristics rather than learned models.

Preparation Assessment Outputs
==============================

Each prepared page assessment should emit:

- ``assessment_id``
- ``source_page_id``
- optional ``prepared_page_id``
- measured or estimated quality signals
- severity levels
- recommended actions
- operator-facing warnings
- machine-usable flags

Suggested machine flags:

- ``unusable_without_intervention``
- ``needs_alternate_preparation``
- ``needs_page_subdivision``
- ``low_confidence_dpi``
- ``heavy_gutter_shadow``
- ``heavy_markings``

Per-Page Preparation Choice
===========================

Preparation choice is per page, not per document.

One document run may legitimately contain mixed preparation modes across pages.

Examples:

- one page uses full-page OCR
- another page uses column subdivision
- another page uses fixed tiles
- another page uses forced operator override

This is expected behavior for heterogeneous historical books and must be
treated as normal, not exceptional.

Each source page should therefore record:

- assessment result
- chosen preparation mode
- whether the choice was automatic or forced
- operator override reason when forced
- overlap setting when subdivision applies
- ordering metadata when subdivision applies
- prepared unit list when subdivision applies

Unusable Input Warnings
=======================

``wordwending`` should warn operators when an input appears unlikely to yield
trustworthy OCR without intervention.

Examples:

- resolution too low for detected text size
- severe skew or curvature
- heavy gutter shadow across text columns
- dense marginal or handwritten markings through text
- extreme speckle or scan noise

V1 need not block execution automatically in every case, but it should surface
clear warnings and support configurable fail-fast thresholds later.

V1 Required Recipe Fields
=========================

The v1 recipe model should include explicit fields for:

- ``recipe_id``
- ``pdf_page_image_mode``
- ``render_dpi``
- ``color_mode``
- ``deskew``
- ``denoise``
- ``crop_mode``
- ``binarize_mode``
- ``dewarp_mode``
- optional freeform notes

Suggested v1 enumerations:

``pdf_page_image_mode``
    ``extract-embedded``, ``render-page``, ``auto``

``color_mode``
    ``grayscale``, ``rgb``, ``binary``

``crop_mode``
    ``none``, ``trim_margin``, ``content_bbox``

``binarize_mode``
    ``none``, ``otsu``, ``adaptive``

``dewarp_mode``
    ``none``, ``basic``

V1 need not implement every mode immediately, but the schema should reserve
them.

Text-Size and Page-Subdivision Policy
=====================================

Preparation must explicitly assess whether full-page OCR is appropriate for the
observed text size.

Some source material, such as dense dictionary pages, may require splitting one
logical page into smaller OCR units so text becomes large enough for reliable
recognition.

V1 should therefore support:

- assessing apparent text-size risk on a page
- deciding whether full-page OCR is inadequate
- generating subdivided prepared units for OCR when needed

Subdivision does not change the logical page identity. It creates OCR-target
subunits under the same source page.

Suggested identities:

- ``source_page_id`` for the logical page
- ``prepared_page_id`` for the prepared page variant
- ``prepared_unit_id`` for one OCR-target subdivision such as a column or tile

Subdivision Triggers
====================

V1 subdivision heuristics should consider:

- apparent text size too small at current full-page render scale
- multi-column dense pages
- dictionary-style narrow entries packed tightly on page
- evaluation history showing poor full-page OCR but better chunk-level OCR

The Bosworth-Toller pages are the motivating example for this capability, not
an exception outside the core model.

Subdivision Modes
=================

Recommended v1 preparation modes:

- ``full-page``
- ``columns``
- ``fixed-tiles``

Recommended v1 policy:

- automatic choice may select among these per page
- primary subdivision mode is ``columns``
- fallback subdivision mode is ``fixed-tiles``

Operator override may force any supported mode on a specific page.

Subdivision Outputs
===================

When subdivision occurs, preparation should preserve:

- mapping from ``prepared_unit_id`` back to ``prepared_page_id``
- bounding box of each unit in page coordinates
- ordering metadata for reconstructing page flow
- overlap in pixels between adjacent units when configured
- recipe and assessment metadata that justified subdivision

Coordinate and Image Provenance
===============================

Every source page, prepared page variant, and prepared unit has a stable
coordinate-space id, pixel width/height, optional effective DPI, artifact id,
and checksum. Boxes, polygons, and baselines name that id rather than a generic
``pixel`` label.

Preparation records the ordered mapping from source space to prepared space and
from prepared page to every unit. Crops, scales, rotations, and deskew operations
store numeric parameters. Dewarp or other non-linear operations retain the
mapping artifact needed to replay coordinates. OCR evidence is rejected during
alignment when its coordinate identity cannot be resolved through this chain.

Prepared-image checksums bind later review and gold image anchors to the pixels
the operator actually inspected. A changed checksum creates a new prepared page
identity and requires overlay/gold rebase; it never silently inherits old boxes.

Operator Rules for Subdivision
==============================

- Treat subdivision as preparation logic, not as a downstream OCR hack.
- Preserve page-level identity even when OCR runs on smaller units.
- Record why subdivision happened so later evaluation can compare full-page and
  subdivided strategies honestly.
- Record operator-forced choices explicitly in provenance, never as hidden CLI
  state.

Competing Preparation Recipes
=============================

V1 should support multiple preparation recipes for the same source page.

Reason:

- hard pages may benefit from different render or cleanup strategies
- one OCR runner may prefer a different preparation than another
- evaluation should compare preparation alternatives, not only OCR alternatives

Recommended model:

- one logical source page
- one or more prepared page variants
- each variant has a unique ``prepared_page_id``
- downstream pass outputs reference ``prepared_page_id``

Prepared Page Identity
======================

V1 should distinguish:

- ``source_page_id``: stable identity of the logical source page
- ``prepared_page_id``: stable identity of one prepared image variant

This is necessary when multiple preparation recipes exist for one page.

When subdivision exists, prepared units must remain children of one prepared
page variant rather than masquerading as independent source pages.

Prepared Image Metadata
=======================

Every prepared image should record:

- ``prepared_page_id``
- ``source_page_id``
- pixel width and height
- effective DPI or equivalent resolution metadata
- preparation recipe id
- checksum or content digest
- source artifact reference

Preservation Rules
==================

The prepared image itself must be preserved in the bundle.

Do not rely on being able to regenerate identical images later from the source
PDF without recipe and renderer provenance.

Evaluation and Preparation
==========================

Preparation is part of evaluation scope.

The system should support comparing:

- same OCR runner across multiple preparation recipes
- multiple OCR runners against one preparation recipe
- multiple OCR runners across multiple preparation recipes
- full-page OCR against subdivided-page OCR for the same logical page

This means evaluation metadata should always record which prepared image variant
or prepared unit fed which pass runner.

Evaluation baselines should compare pages first against other runs using the
same preparation mode, while still allowing explicit cross-mode experiments.

Reason:

- same-mode comparisons are cleaner operational baselines
- cross-mode comparisons are still necessary when testing whether subdivision or
  alternate preparation materially improves OCR quality

Operator Rules
==============

- If the recipe changes, treat outputs as a distinct run input.
- Do not compare results across changed preparation recipes as if they were same
  baseline.
- Preserve prepared images even when they look visually redundant.
- Heed unusable-input warnings before spending time on markup of obviously bad
  OCR.
- Compare full-page and subdivided preparation strategies on dense small-font
  pages before deciding one global policy.

Non-Goals
=========

V1 does not need:

- automatic recipe search over a large hyperparameter space
- learned preparation policy
- distributed preparation farm orchestration
