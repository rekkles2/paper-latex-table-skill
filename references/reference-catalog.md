# Learned reference layouts

Seventeen local references were studied with their original code, images or both: ten paired references (original TeX and figure) and seven image-only references (reconstruction only). This catalog records layout observations, not external verification of the papers, results or venue provenance. Full local snapshots, restored macros, compilations and comparison images live together in `assets/cases/local/`; that private collection is omitted from the public export. Eight original synthetic cases remain public and can be retrieved after a fresh index build.

Per-case typography, group scope, macro/package roles, ranking/delta semantics, fidelity pitfalls and reuse notes: [example-details.md](example-details.md).

## Figure/TeX pair indices

- Public pairs (20): [docs/gallery-public.json](../docs/gallery-public.json)
- Optional local pairs (18): `assets/cases/local/gallery-pairs.json` — private, absent from the public export

## Ten paired references

| Local case ID | Observed structure | Reusable lesson | Fidelity risk |
| --- | --- | --- | --- |
| ablation_table-example1 | 9 columns; three binary components; three paired-shot datasets; two backbone bands | Align component switches with metric blocks; retain backbone boundaries | Mean/std plus colored deltas have separate semantics; Unicode ± needs the correct font |
| ablation_table-example2 | 11 columns; three component switches; six datasets and an average; global/local groups | Pale section bands and narrow delta annotations separate variants without a dense grid | Supplied main.tex exists and is truncated; recover complete macros rather than loading it wholesale |
| dataset_benchmark_table | 14 columns; metadata plus a ten-capability coverage matrix | Full/half/empty symbols express categorical coverage compactly | A partial symbol is not a numeric half score; moving captions need robust macros |
| main_table-example1 | 12 columns; rotated task headings; three metric blocks; human/closed/open groups | Rotate labels and use group bands to make wide comparisons navigable | Preserve provided Rank, scope and gray marks rather than globally reranking |
| main_table-example2 | 15 columns; category and difficulty headers; proprietary/open bands; brand icons | Separate comparison populations and distinguish a method family with a light band | Missing icons need declared crops; Params strings such as 30B-A3B are not scalar metrics |
| main_table-example3 | 13 columns; four capability icons; benchmark/domain groups; uncertainty; two shaded deltas | Keep uncertainty subordinate and delta columns visually distinct | Do not reconstruct reported deltas from rounded means or turn uncertainty into significance |
| main_table-example4 | Code: 25 columns; image: 23; rotated headers; three zero-shot task families | Use task-family headings and average columns to navigate many benchmarks | Two versions disagree in rows, columns, averages and caption; keep source/image branches separate |
| others-example1 | 8 columns; centralized baseline and two federated groups | Gray reference baselines and pale group bands distinguish comparison roles | The screenshot omits the code caption; delta baselines differ from other ECG tables |
| others-example2 | 6 columns; paired local/global comparisons; distribution blocks and multirow settings | Treat paired FedAvg/TDFL columns as repeated experimental structure | Preserve alpha, participant count and multirow identities; gains are percentage points |
| others-example3 | 5 columns; model groups; dates/resolution/source/long URLs | Group metadata catalogs by family; keep source URLs editable | Dates and links are source claims; typographic reproduction does not establish currency |

## Seven image-only references

| Case ID | Observed structure | Reusable lesson | Fidelity risk |
| --- | --- | --- | --- |
| diffusion-main | Two-row header; three real pretraining columns (token/perc./self-sup.); latent/pixel gray bands; JiT family rows; caption below the block | Keep pretraining as a header-level fact and the caption below the tabular block | Parameter strings such as 675+49M and 700 M are identity strings; never synthesize a missing IS value |
| representation-ablation | Four aligned panels; FID, IS and rep FD only; gray default markers | Repeat the default-marker convention per factor and align panel baselines | Gray marks the default, not the best result; no significance inference |
| paired-generation | Multirow method identifiers; baseline/RCG pairs split by thin rules; bold improved value with small green signed delta | Bind each delta to its own baseline; keep citation numbers as literal source text | Pictured deltas are claims, not recomputed evidence |
| guidance-comparison | Two-tier w/o and w/ Guidance header; gray class-conditional population; vertical block boundaries; bold caption lead | Gray population tint retained inside bold values encodes population, not rank | Do not treat gray rows as worse or average across populations |
| meanflow-algorithm | Algorithm 1 pseudocode block; serif title/note; colored monospace body; no line numbers | One verified compile-only pseudocode reconstruction; layout only | No execution, no algorithm semantics, no universal algorithm generation |
| multimodal-main | 15 columns; 65-degree rotated metric labels; lavender population bands; pale green target rows; model-size blocks | Keep evaluation populations distinct and model-size blocks as explicit scopes | Size blocks are not a ranking; missing tokens and base-LM identities stay literal |
| data-mixture | Image/video column blocks; rotated labels; italic data-source bands; pale green full-mixture row | Band rows by data-source mixture so each recipe change reads as a group | Bands describe composition only; no significance or trend implication |

## Cross-cutting conventions

Gray carries three distinct meanings and they are never merged: **default/selected baseline** (representation-ablation, others-example1), **best/second-best standing** (main_table-example1), **population membership** (guidance-comparison). Caption weight and position are reference-specific — bold lead, bold first sentence, fully regular serif and centered sans-serif all occur; do not impose one universal rule. Limited vertical rules are allowed at source-observed semantic block boundaries; booktabs-first, no full grid. Preserve source-provided deltas and ranks; never silently recompute a reported source delta from rounded means. New synthetic or user-authorized calculations are allowed with explicit baseline and units. Image-only transcription states are `read`, `ambiguous` and `illegible`; unresolved cells render `[?]` and style ambiguity stays in prose notes.

## Choose a pattern

Retrieve by task, column count and features; then read the actual case rather than applying a style name blindly. Reuse grouping, spacing and hierarchy with the user's own data. The structured JSON generator handles one header-group level; arbitrary multirow, deeper headers, bespoke macro grammars and original reference reproduction use agent-authored TeX with a keyed ledger.

For each paired local case, `reproduction/profile.json` records the wrapper settings and dependency-restoration notes; `reproduction/reproduction-report.json` binds source/macro/profile hashes to the actual compilation. `reproduction/comparison.png` places the original and TeX reconstruction side by side. `reproduction/REVIEW.md` records observed residual differences. These are source-preserving reconstructions, not a claim of pixel identity or publisher-template compliance.

## Provenance and organization

README organization and the original/reproduction gallery pattern were inspired by [Trae1ounG/paper-plot-skills](https://github.com/Trae1ounG/paper-plot-skills), inspected during this revision. Plotting code and numeric evidence were not imported from it. OpenCode supplied a completed documentation/input-route review; its proposed confidence scores and most-likely digit selection were deliberately rejected in favor of explicit transcription states and unresolved placeholders.
