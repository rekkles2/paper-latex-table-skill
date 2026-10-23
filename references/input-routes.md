# Input routes and evidence

| Input | First artifact | Data authority | Output |
| --- | --- | --- | --- |
| Code + image | Immutable source snapshots and a conflict ledger | Original code for the default variant; image-observed version separate | Editable TeX, restored dependency notes, original/render comparison |
| Code only | Source snapshot; keyed row/column ledger for arbitrary macros | Original strings, units, precision and missing tokens | Compiled TeX if dependencies exist; exact unmet dependencies otherwise |
| Image only | Per-cell transcription ledger linked to source image hash | Visible pixels, with unresolved readings retained | Editable TeX and a separate transcription report |

## Code plus image

Record stable row/column keys, code tokens, image readings, observed emphasis, and discrepancy type. Include header/row presence and caption differences. Default to a code-preserving reconstruction while documenting conflicts; an explicitly requested image reconstruction is a separate branch. Do not block unrelated layout work while seeking a consequential missing value. A rendered image can show another paper version or a cropped region. Never overwrite either source to conceal a mismatch.

Recover macro definitions from supplied main.tex and package files first. If the supplied preamble is truncated, extract only complete necessary definitions and record their source. Infer missing visible typography only with an explicit restoration note. Missing bibliography must remain unresolved; do not manufacture citation identities. Unknown logos can be omitted with a visible note, supplied by the user, or tightly cropped from the reference when appropriate; record each atomic raster crop separately. The table itself must remain editable.

## Image transcription format

`transcribe_table.py` consumes JSON with `image` (relative to ledger), `image_sha256`, `columns` (unique `id`, `label`, optional `rotate`), and `rows` (unique `id`, `cells` keyed by every column ID). Each cell has `status`: `read`, `ambiguous`, or `illegible`. A read cell has `text` as an exact string, or `symbol`: `full` / `half` / `empty`. Optional boolean `bold`, `italic` and `underline` preserve visible emphasis in cells and headings. Ambiguous cells may carry `alternatives`; they render as `[?]`, never as an arbitrary most-likely value. Optional `header_groups` span all columns; `rule_before` separates row groups.

```json
{"image":"reference.png","image_sha256":"REPLACE_WITH_ACTUAL_SHA256","columns":[{"id":"model","label":"Model"},{"id":"acc","label":"Accuracy (%)"}],"rows":[{"id":"method-a","cells":{"model":{"status":"read","text":"Method A"},"acc":{"status":"ambiguous","alternatives":["81.3","87.3"]}}}]}
```

Inspect a readable crop before marking `read`; keep exact signs, decimal zeros, uncertainty, missing markers and superscripts in the ledger. Record the image crop/page location for nontrivial ambiguity. Separate unknown experimental evidence from unknown transcription. Ask for clarification only for consequential unresolved cells; a placeholder permits the rest of the reconstruction to proceed. Do not declare image-derived numbers independently verified merely because the same agent read them twice.

## Review sequence

1. Verify original hashes and scope, source authority and all visible row/column identities.
2. Compile the exact delivered file with its actual dependencies. Report engine, page size, warnings and missing glyphs.
3. Open the newly rendered table and compare at full view and readable detail. Compare rule structure, group spans, symbols, deltas, citations, emphasis, clipping, caption and crop.
4. Inspect at the intended physical publication width. A side-by-side sheet resized to equal width is a comparison aid, not proof of physical readability or numerical integrity.
5. Report source preservation, transcription, compilation, visual match and physical-size review separately as passed/failed/pending. Inferred font and absent template remain limitations even when the body looks close.

These review categories draw on Sivia's semantics/editability/geometry/render evidence discipline. The backend here remains native LaTeX; a PowerPoint or draw.io inspection is not evidence for a TeX artifact.

For learning from each input mode and recombining reviewed layouts, follow [three-rsi-loops.md](three-rsi-loops.md).
