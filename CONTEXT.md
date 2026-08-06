# wordwending Context

## Mission

`wordwending` is an image-first OCR orchestration toolkit for difficult Old English
and Anglo-Saxon source documents.

Its job is to turn scanned PDFs and source images into evidence-preserving OCR
bundles that humans, deterministic software, and AI systems can inspect, review,
and reuse.

Primary goals:

- prepare page images for OCR from scanned inputs
- run and compare multiple OCR-related passes on difficult pages
- preserve raw witness artifacts instead of collapsing early to plain text
- build a normalized, provenance-aware page graph
- evaluate OCR quality against gold slices and targeted watchlists
- support explicit human review and correction
- preserve bibliographic context and source provenance alongside OCR artifacts
- export structured JSON, retrieval-oriented JSON, and evidence-preserving
  Markdown views

## Boundary

This repo is one product context: OCR orchestration and witness production for
difficult historical source documents.

In scope:

- scanned PDF and source-image preparation
- source-page folders such as `.jp2` or other page-image sets
- source-quality assessment and operator warnings
- page classification for preparation and evaluation cohorts
- OCR pass orchestration
- layout, line, style, note, and table-region evidence capture
- evidence alignment and merge policy
- review overlays and trust-state tracking
- structured and retrieval-oriented export generation

Out of scope:

- Old English morphology
- dictionary semantics
- lexicographic normalization as a product domain
- downstream philological interpretation beyond OCR witness production
- full document-semantic knowledge extraction
- document-specific structured transforms (dictionary, grammar, reader,
  translation, or TEI-inspired targets); those belong in downstream packages
- acting as a general structured-data transformer rather than an OCR framework
  for faithful evidence-preserving output
- generic training-platform work

## Canonical Terms

- source document: immutable scanned PDF, page-image set, or single page image
  used as input to one `wordwending` run
- source image set: folder of individual page images representing one logical
  source document, such as `.jp2` page files from archive.org or operator-made
  scan folders
- bibliographic provenance: citation-oriented source metadata describing what
  document a run came from, where it was obtained, which edition or scan it
  represents, and any other identifying source context needed for later
  scholarly or software reuse
- acquisition provenance: operational source metadata describing how input was
  obtained, such as local scan folder, archive.org derivative set, manual
  download, or other concrete acquisition path
- source page: one logical page from a source document before any preparation
  variants or OCR-target subdivision
- document bundle: top-level run artifact containing source metadata, prepared
  pages, page bundles, manifests, evaluation outputs, overlays, and exports
- page bundle: page-local artifact package containing raw witness artifacts,
  derived graph data, evaluation outputs, overlays, and page-level exports
- raw witness artifact: exact unchanged output from one pass runner, preserved
  for audit, comparison, and rebuildability
- witness production: workflow that creates preserved OCR-related evidence
  artifacts rather than jumping directly to flattened final text
- pass runner: pluggable engine adapter that accepts page-local input plus run
  config and emits raw witness artifacts plus metadata without writing directly
  into the canonical page graph
- pass family: broad kind of runner such as text, line/layout, style, table, or
  evaluation helper
- page preparation: first-class stage that turns source PDFs or source images
  into deterministic prepared page images for downstream OCR and analysis
- preparation recipe: named, serializable configuration describing one
  preparation strategy, including render and cleanup choices
- preparation assessment: source-quality evaluation performed during preparation
  to identify likely OCR risks, unusable inputs, and subdivision needs
- prepared page: one prepared image variant of one source page produced by one
  preparation recipe
- prepared page variant: another term for a prepared page used when multiple
  preparation recipes exist for the same source page
- prepared page id: stable identity for one prepared page variant
- prepared unit: one OCR-target subdivision of a prepared page, such as a
  column or fixed tile
- prepared unit id: stable identity for one prepared unit
- source page id: stable identity for one logical source page
- input quality warning: operator-facing signal that a page or document may not
  be suitable for trustworthy OCR without intervention
- unusable input: source material whose assessed quality is too poor for
  trustworthy OCR without manual intervention or alternate acquisition
- page subdivision: preparation-time splitting of one logical page into smaller
  OCR-target units when full-page OCR is likely to underperform
- subdivision mode: strategy for prepared-unit generation, such as `full-page`,
  `columns`, or `fixed-tiles`
- overlap: intentional pixel overlap between adjacent prepared units to prevent
  boundary loss of words, note markers, or fine features
- column-major order: stable prepared-unit ordering that walks one column before
  moving to the next column
- page class: operational classification assigned per page to guide preparation,
  evaluation, and review expectations
- ordinary-prose page: page dominated by running prose and usually suitable for
  full-page OCR unless assessment suggests otherwise
- dense-dictionary page: small-font, tightly packed lexical page where
  subdivision is often required for reliable OCR
- note-heavy page: page where note markers and note bodies materially affect OCR
  structure and review
- table-heavy page: page where table-like layout dominates and ordinary prose
  assumptions are unsafe
- mixed-complex page: page combining multiple difficult traits without one
  single dominant class
- page graph: normalized shared-coordinate representation for one page built
  from aligned pass outputs
- shared page coordinates: one common coordinate system used to align evidence
  from multiple pass runners on the same page
- coordinate space: stable identity plus raster dimensions for the image in
  which a box, polygon, or baseline is expressed
- transform chain: ordered, replayable source-to-prepared mappings such as crop,
  scale, rotation, deskew, or dewarp; non-linear mappings retain an artifact
- polygon: non-rectangular geometry used when an axis-aligned box would lose
  region or line shape
- baseline: ordered points describing where a text line sits, especially useful
  for curved or skewed historical print
- region: page-graph node representing one layout area such as paragraph, table
  area, marginalia area, or footnote area
- line: page-graph node representing one ordered textual line inside a region
- span: page-graph node representing one aligned styled text run inside a line
- note: page-graph node representing one note body linked to one or more marker
  spans
- footnote marker: semantic span role marking inline note-reference text or a
  symbol; independent of visual font properties
- footnote block: note-kind for a note body rendered separately from main text
- table region: region whose dominant role is tabular or paradigmatic layout;
  v1 does not require full cell modeling
- typography: orthogonal visual facets on a span: font-family candidates, font
  size estimate, weight, slant, baseline shift, small capitals, and letter
  spacing
- font weight: `regular`, `bold`, or `unknown`, independent of slant and role
- font slant: `upright`, `italic`, or `unknown`; upright means not italic or
  oblique and replaces the ambiguous label `roman`
- baseline shift: `baseline`, `superscript`, `subscript`, or `unknown`
- text role: semantic role such as `text` or `footnote-marker`, kept separate
  from typography
- PAGE interchange: OCR-D PAGE-compatible internal representation used when it
  reduces custom orchestration or review work; public output remains JSON and
  Markdown rather than requiring XML
- structure scaffold: chosen coordinate-rich structural basis used during merge
  so other pass evidence can be aligned onto one accepted page layout
- merge policy: deterministic rules for resolving competing pass outputs into
  one accepted derived page graph while preserving alternate evidence in
  provenance
- accepted page graph: current canonical derived page graph for one page after
  merge and any later human review
- primary accepted value: chosen text, style, or linkage carried in the
  accepted graph object
- alternate evidence: preserved non-primary candidate output retained in
  provenance for audit and comparison
- provenance: traceable record of where a derived object came from, including
  contributing raw witnesses, pass runners, preparation variant, source page,
  and source-document provenance
- machine confidence: confidence emitted by an originating model or heuristic
- merge confidence: confidence that the accepted graph value was resolved
  correctly from competing evidence
- trust state: human-review state on named evidence dimensions of a derived
  object or exportable chunk: `machine`, `reviewed`, or `corrected`
- review dimension: independently certifiable evidence family: source quality,
  preparation, structure, text, typography, or note linkage
- review scope: granularity at which trust or review applies, such as page,
  region, line, note, or span
- machine state: trust state meaning no human acceptance yet
- reviewed state: trust state meaning a human checked and accepted output
  unchanged
- corrected state: trust state meaning a human changed machine-derived output
- review event: one append-only human markup record describing acceptance,
  correction, linkage, split/merge, or flagging activity
- review task: self-contained operator packet naming one question, dimensions,
  targets, required evidence, allowed actions, abstention, completion criteria,
  guideline version, source run, and graph revision
- abstention: explicit outcome stating that available evidence does not support
  a defensible decision; it is not machine acceptance or task failure
- adjudication: review of independent conflicting decisions that preserves the
  originals and records a new resolution
- overlay rebase: explicit transfer of still-valid events to a successor image,
  run, or graph revision while routing unresolved targets back to review
- overlay: review layer applied on top of derived graph outputs without
  mutating raw witness artifacts
- append-only review history: review model where events are accumulated rather
  than replaced by one mutable latest-state blob
- gold slice: manually verified annotation slice used as trusted reference for
  evaluation on a page or page fragment
- gold coverage: explicit page, graph-object, or image region and dimensions
  that define what was annotated exhaustively and therefore define metric
  denominators
- held-out split: gold examples reserved before model selection and not used to
  tune prompts, preparation, merge thresholds, or engine choices
- watchlist metric: targeted evaluation metric focused on one failure family
  such as macrons, ligatures, thorn/eth, or style retention
- text accuracy: evaluation family covering OCR character and word fidelity
- structure accuracy: evaluation family covering reading order, linkage,
  coverage, and similar structural correctness
- typography accuracy: evaluation family scored per independent visual facet
- note-linkage accuracy: evaluation family covering marker roles and
  marker-to-note edges within explicit gold coverage
- evidence-preserving text: text kept in a form that does not discard important
  graphemes, style signals, or uncertainty too early
- diplomatic text: exact or philologically faithful text field derived from the
  accepted graph and intended to preserve evidence
- normalized text: deterministic downstream convenience text field derived from
  diplomatic text by explicit normalization rules
- retrieval field: auxiliary text field optimized for search or indexing rather
  than philological truth
- bundle JSON: primary structured export contract carrying full-fidelity bundle,
  graph, provenance, review, and evaluation information
- RAG JSON: derived retrieval-oriented export contract carrying flattened,
  indexable chunks with links back to bundle truth
- Markdown export: derived evidence-preserving reading view for humans or
  agents; not canonical truth
- region chunk: retrieval chunk derived from one region
- footnote chunk: retrieval chunk derived from one note and linked back to its
  marker spans and page context
- stitched chunk: document-level retrieval chunk derived from accepted
  page-graph order across page boundaries
- chunking recipe: versioned deterministic policy that produced RAG chunk
  boundaries and text
- hosted inference boundary: all OCR model inference runs on pinned Hugging Face
  endpoints; the local laptop prepares inputs, orchestrates requests, validates
  and stores witnesses, evaluates outputs, and supports review, but never runs
  OCR models or silently falls back to local weights
- page-local truth: design principle that correctness is established first at
  the page level before broader document stitching
