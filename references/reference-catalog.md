# Learned reference layouts

Ten user-supplied local cases were studied with their original code and images. The original 23 source files are hash checked. This catalog records layout observations, not external verification of the papers, results or venue provenance. Full local snapshots, restored macros, compilations and comparison images live together in `assets/cases/local/`; that private collection is omitted from the public export. Eight original synthetic cases remain public and can be retrieved after a fresh index build.

| Local case ID | Observed structure | Reusable lesson | Fidelity risk |
| --- | --- | --- | --- |
| ablation_table-example1 | 9 columns; three binary components; three paired-shot datasets; two backbone bands | Align component switches with metric blocks; retain backbone boundaries | Mean/std plus colored deltas have separate semantics; Unicode ± needs the correct font |
| ablation_table-example2 | 11 columns; three component switches; six datasets and an average; global/local groups | Pale section bands and narrow delta annotations separate variants without a dense grid | Supplied main.tex is truncated; recover complete macros rather than loading it wholesale |
| dataset_benchmark_table | 14 columns; metadata plus a ten-capability coverage matrix | Full/half/empty symbols express categorical coverage compactly | A partial symbol is not a numeric half score; moving captions need robust macros |
| main_table-example1 | 12 columns; rotated task headings; three metric blocks; human/closed/open groups | Rotate labels and use group bands to make wide comparisons navigable | Preserve provided Rank, scope and gray marks rather than globally reranking |
| main_table-example2 | 15 columns; category and difficulty headers; proprietary/open bands; brand icons | Separate comparison populations and distinguish a method family with a light band | Missing icons need declared crops; Params strings such as 30B-A3B are not scalar metrics |
| main_table-example3 | 13 columns; four capability icons; benchmark/domain groups; uncertainty; two shaded deltas | Keep uncertainty subordinate and delta columns visually distinct | Do not reconstruct reported deltas from rounded means or turn uncertainty into significance |
| main_table-example4 | Code: 25 columns; image: 23; rotated headers; three zero-shot task families | Use task-family headings and average columns to navigate many benchmarks | Two versions disagree in rows, columns, averages and caption; keep source/image branches separate |
| others-example1 | 8 columns; centralized baseline and two federated groups | Gray reference baselines and pale group bands distinguish comparison roles | The screenshot omits the code caption; delta baselines differ from other ECG tables |
| others-example2 | 6 columns; paired local/global comparisons; distribution blocks and multirow settings | Treat paired FedAvg/TDFL columns as repeated experimental structure | Preserve alpha, participant count and multirow identities; gains are percentage points |
| others-example3 | 5 columns; model groups; dates/resolution/source/long URLs | Group metadata catalogs by family; keep source URLs editable | Dates and links are source claims; typographic reproduction does not establish currency |

## Choose a pattern

Retrieve by task, column count and features; then read the actual case rather than applying a style name blindly. Reuse grouping, spacing and hierarchy with the user's own data. The structured JSON generator handles one header-group level; arbitrary multirow, deeper headers, bespoke macro grammars and original reference reproduction use agent-authored TeX with a keyed ledger.

For each local case, `reproduction/profile.json` records the wrapper settings and dependency-restoration notes; `reproduction/reproduction-report.json` binds source/macro/profile hashes to the actual compilation. `reproduction/comparison.png` places the original and TeX reconstruction side by side. `reproduction/REVIEW.md` records observed residual differences. These are source-preserving reconstructions, not a claim of pixel identity or publisher-template compliance.

## Provenance and organization

README organization and the original/reproduction gallery pattern were inspired by [Trae1ounG/paper-plot-skills](https://github.com/Trae1ounG/paper-plot-skills), inspected during this revision. Plotting code and numeric evidence were not imported from it. OpenCode supplied a completed documentation/input-route review; its proposed confidence scores and most-likely digit selection were deliberately rejected in favor of explicit transcription states and unresolved placeholders. A second optional case-lesson request timed out and is not treated as completed analysis.
