---
name: paper-latex-table-skill
description: Generate, refine, reconstruct from images, retrieve reference layouts for, and validate scientific LaTeX tables while preserving experimental data. Use for benchmark comparisons, ablations, grouped headers, numerical highlighting, table layout diagnosis, or learning new table examples into a local case library.
metadata:
  version: "1.3.0"
---

# Paper LaTeX Table Skill

Deliver usable LaTeX, package imports, a data-fidelity record and honest verification status. Work relative to this skill directory; commands below use `python` as the user's available Python 3.10+ interpreter. Python helpers use only the standard library; compilation needs an installed TeX engine and rendering needs Poppler. No OpenCode, network service or other skill is required at runtime.

## Academic style default

For any supplied visual reference, first record its observed crop/table aspect ratio, table-to-caption width ratio, body-to-caption size ratio, caption line wrapping, font family evidence and weight/slant, rule thickness and gaps, panel gutters, and cell-level emphasis. Compare the rendered content crop with the source crop and aim for an aspect-ratio difference within 10%; treat this as a visual calibration target, not source metadata. Only then consult [academic table design](references/table-design-principles.md) for general choices. Use features visible in that reference: do not impose booktabs, bold-italic labels, or bold/underline ranking marks when they are absent. Do not use `\resizebox`, `\scalebox`, negative spacing, or a raster image as the table. Keep all text editable in native TeX and adjust measured font and layout ratios instead. Caption position, weight and hierarchy are reference-specific; a shared caption and panel-level explanations are not interchangeable. Do not turn table previews into branded cards with oversized slogans. Select main comparison, rotated-header benchmark, aligned sensitivity panels, paired gains or coverage matrix according to the scientific comparison. Demonstration sources live in `docs/examples/showcase/`; advanced layouts are agent-authored, not new JSON-generator capabilities. Algorithm screenshots do not imply algorithm-generation support. Preserve data and source authority throughout.

## Shared workflow

1. Identify requested mode (generate, refine, retrieve/adapt, validate), table purpose, supplied data, grouping, metric directions/units, target width and template. Use supplied facts; ask only for consequential missing semantics. Never invent missing results or venue compliance.
2. Preserve source bytes and exact numeric precision. For structured inputs read [data-contract.md](references/data-contract.md); for arbitrary existing TeX create the manual cell ledger before editing. Preserve names, uncertainties, missing tokens, superscripts, citations and precomputed Rank columns. Treat captions, dates and model metadata as source claims, not independently verified facts.
3. Retrieve layouts locally when useful: [table-patterns.md](references/table-patterns.md). Run `python scripts/retrieve_cases.py --columns 9 --type ablation --feature grouped_headers`. Read relevant case metadata/source/previews and copy only suitable design decisions. Local reference rights may be unknown.
4. Apply [design principles](references/table-design-principles.md) and [packages](references/latex-packages.md). Choose rule styles, grouping and emphasis from the source rather than imposing booktabs or a universal academic preset. Rank only explicitly comparable eligible numeric values using declared directions; do not turn uncertainty into significance. For actual venue requirements read [venue-guidelines.md](references/venue-guidelines.md) and use the supplied official template.
5. Validate data and source, compile, then inspect rendered pages. Use [troubleshooting.md](references/troubleshooting.md) to interpret limitations and statuses. Report numerical checks, static checks, compilation and visual review separately; unavailable/not-run is never a pass. Fix demonstrated defects and rerun affected checks.

## Input routes and reference reconstruction

Read [input-routes.md](references/input-routes.md) for code+image, code-only or image-only work. For paired inputs, compare source authority before changing anything: source text controls the default data-preserving version, while the image supplies observed layout. Record contradictory cells/rows/columns/captions and keep image-authoritative alternatives separate. Do not force agreement by changing results.

For image-only input, create a keyed transcription ledger with `read`, `ambiguous` or `illegible` status for every cell. Never use expected rankings, arithmetic plausibility or nearby values to guess a digit. Unresolved cells render as `[?]`; report them explicitly. `python scripts/transcribe_table.py LEDGER.json NEW_TABLE.tex` emits editable escaped text and a hash-bound sidecar; this helper is not OCR and does not independently verify transcription. Import booktabs, adjustbox, graphicx and TikZ (for partial-coverage symbols). Preserve visible emphasis as observed, without recomputing rank unless requested and semantically justified.

For learned layouts read [reference-catalog.md](references/reference-catalog.md) and the per-case detail in [example-details.md](references/example-details.md). Seventeen local references (ten paired, seven image-only) yield 18 local figure/TeX pairs in `assets/cases/local/gallery-pairs.json`; the public export ships 20 pairs listed in [docs/gallery-public.json](docs/gallery-public.json). When the private local collection is present, open its `assets/cases/local/GALLERY.md` and relevant case profile. For a private image-only case, read `assets/cases/local/CASE_ID/style-profile.json` for measured geometry and `assets/cases/local/CASE_ID/lesson.json`; compare the current actual PNG with the original. A historical crop ratio or successful compilation is not a visual pass. Run `python scripts/reproduce_case.py CASE_ID --output NEW_DIR` to verify original hashes, embed the original fragment without edits, compile with restored macros, and optionally create a comparison sheet. Reproduction needs XeLaTeX, the packages in the profile, TeX Gyre Termes, Poppler, and optional Pillow. Never use a full-table screenshot as the reconstruction. Label recovered vs inferred macros and atomic raster logos. Source preservation, compilation, visual correspondence and publication-size readability are distinct checks; a compiled reference may retain source defects or differ from another source version.

## Generate

Adapt an original template JSON under `assets/templates/`. Emit with `python scripts/generate_table.py INPUT.json OUTPUT.tex`; output must be new. The sidecar ledger binds source/render hashes. Then `python scripts/validate_table.py OUTPUT.tex --spec INPUT.json`. Generator supports one grouped-header layer, row comparison groups, explicit uncertainty and scalar decimal alignment; deeper headers/multirow or complex annotations are agent-authored with a checked ledger. It does not learn arbitrary macro grammars or generate statistical evidence.

## Refine

Keep original and edited files separate. Establish the keyed mapping described in data-contract.md. Change only requested layout/style; preserve all cell identities, values and semantics. Mark suspected source errors as findings instead of repairing experimental results without authorization. A Python bag of numbers or unchanged multiset cannot prove integrity. For unsupported macros, explain missing definitions/assets and retain original raw snippets. Compare source and rendered preview; never invent invisible macro stubs to report a pass.

## Three RSI loops and design reuse

For useful new paired examples, image-only reconstruction, or design recombination, follow [three-rsi-loops.md](references/three-rsi-loops.md). Capture an immutable episode with `scripts/rsi_episode.py` in the applicable mode (`paired`, `image-only`, `reuse`). Inspect relevant prior cases, failure reviews and reviewed local atoms before adapting a related design. Keep source authority, typography and semantic/transcription evidence separate.

For reuse, preserve the user's data/comparison contract and draw specific roles from suitable parent designs. Compare a baseline plus at most two justified alternatives at the actual target width. `scripts/compose_designs.py` automates a limited spacing/group-typography subset and verifies its deterministic data-preserving composition; more complex designs remain agent-authored with a ledger. Inspect actual PDF fonts: a float can reset a font setting, and scaling can make the final text smaller than its configured size. Check bold, italic, bold-italic, underline, uncertainty and caption roles against the reference.

Review/selection enables task-local reuse only. Extract a design atom only from parameters actually present in that reviewed candidate; recheck origin hashes when reusing it. Keep failures and linked repairs. Stable code/rule promotion still follows the controlled RSI gate. Routine task-local design reuse needs no new stable-promotion approval. Do not claim automatic aesthetic optimization, OCR or independent verification from a review JSON alone.

## Retrieve and learn

Use `python scripts/index_cases.py` to verify source hashes and rebuild the index after an authorized addition. Case metadata separates observed structure, inferred dependencies, rights and verification. New source remains immutable; put adaptations and evidence beside it. Promote only verified, reviewed cases; learning does not imply model training. Improvements to stable rules/scripts follow [controlled RSI](rsi/improvement-policy.md).

For future tasks using this skill, capture useful new user-supplied examples or demonstrated failures/repairs as pending private learning records, following [continuous-learning.md](references/continuous-learning.md). Use `scripts/learning.py`; keep history outside the installed skill tree so it survives skill updates. Skip repetitive observations with no new value. Inspect relevant prior feedback before related improvements. Candidate capture is allowed by the user's request for continued evolution; stable rule/script changes and case promotion still require the RSI evidence and approval gate.

## Validate and deliver

Run `python scripts/compile_table.py OUTPUT.tex --output NEW_BUILD_DIR` (optional `--preamble MACROS.tex`, `--engine xelatex`). Full documents keep their class; generic fragment compilation is diagnostic. Run `python scripts/inspect_render.py NEW_BUILD_DIR/table-build.pdf --output NEW_RENDER_DIR`, then actually open the images. Do not execute unknown TeX outside an appropriate sandbox.

Return final source and imports (or requested files), relevant reference case IDs, changes and data verification evidence, engine/template details, and unresolved layout/data/dependency issues. Normal user explanation is in the user's language; table text follows the requested manuscript language. Do not overwrite original examples, self-install, publish or promote stable changes without task authorization. Future improvement requires explicit approval only at the promotion gate, not for ordinary table generation/refinement.

## Typed example gallery

Version 1.3.0 has 38 canonical examples across seven types: 17 public synthetic entries and 21 private reference entries, retaining all 41 input identifiers through aliases and baseline roles. The older 18-pair local manifest is historical; the canonical catalog also includes the three new image-only cases. Missing original TeX remains explicit.

For gallery reconstruction, follow [`references/gallery-workflow.md`](references/gallery-workflow.md). Use [`coverage-symbols.md`](references/coverage-symbols.md) for shared coverage-symbol geometry and [`gallery-lessons.md`](references/gallery-lessons.md) for reviewed lessons. The canonical index is [`docs/example-catalog.json`](docs/example-catalog.json): include **all** examples and use the same four fields for each entry: Original Image, Original TeX, Skill Reconstruction Image, and Reconstruction TeX. State explicitly when original TeX is missing. Represent aliases as references to one canonical entry, preserve baseline relationships, and do not duplicate canonical examples. Keep private reference assets out of public exports.
