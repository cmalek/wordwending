# Assemble eval fixtures

Wave A / Wave B fixtures for assemble → eval → export. Object ids follow
ADR 0008 / A2 adapt formula so gold annotations pair to adapted `BundlePage`
(and provisional `PassWitnessPage`) spans.

## ID formula (locked)

Given `prepared_page_id` from the assemble manifest:

```text
region_id = f"{prepared_page_id}:r0"
line_id   = f"{prepared_page_id}:l{line_index}"
span_id   = f"{prepared_page_id}:s{line_index}"
```

`line_index` is 0-based over newline-split diplomatic lines from the olmOCR
`chat.completion` assistant content.

## Fixture pairing (`page-0001`)

| Role | Value |
|------|--------|
| Bundle / eval `page_id` | `page-0001` |
| Manifest `prepared_page_id` | `prepared-page-1` |
| Adapted region | `prepared-page-1:r0` |
| Adapted lines | `prepared-page-1:l0`, `prepared-page-1:l1` |
| Adapted spans | `prepared-page-1:s0`, `prepared-page-1:s1` |

Gold (`gold-v1.json`) pairs to those span ids:

| Gold field | Values |
|------------|--------|
| `coverage[0].target_object_ids` | `prepared-page-1:s0`, `prepared-page-1:s1` |
| `text_spans[].target_object_id` | `prepared-page-1:s0`, `prepared-page-1:s1` |
| `text_spans[].text_diplomatic` | Same strings as olmOCR fixture lines |

`page_id` (`page-0001`) identifies the page in the bundle tree and gold
document. Stable graph object ids are prefixed by `prepared_page_id`, not
`page_id`. Eval matches gold `target_object_id` to prediction span ids after
assemble writes `pages/page-0001/graph/page_graph.json`.

## Files

| File | Role |
|------|------|
| `manifest-v1.json` | Assemble input: one page, one olmOCR raw witness |
| `manifest-multi-witness-v1.json` | Assemble input: one page, olmOCR + kraken with intentional text disagreement |
| `olmocr-chat-completion-v1.json` | Raw witness bytes (exact `chat.completion` shape) |
| `kraken-chat-completion-v1.json` | Second-runner raw witness with disagreeing diplomatic lines |
| `gold-v1.json` | Partial text gold keyed to adapted span ids |
| `metric-profile-v1.json` | Eval profile for Wave A exit |

Manifest `prepared_page.image_checksum` may use a placeholder (`sha256:image`);
assemble reseals it from on-disk prepared image bytes when writing the bundle.

## Consumers

- `tests/test_witness_adaptation.py` — adapt identity + gold span pairing
- `tests/test_assemble.py` — multi-witness disagreement → `evaluation/flags.json`
- `tests/test_assemble_wave_a_exit.py` — assemble → eval → export exit path
- `tests/test_cli_commands.py` — assemble / inspect-bundle including merge flags
