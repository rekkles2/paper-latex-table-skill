# Paper LaTeX Table Skill

**Generate, refine and reconstruct scientific LaTeX tables while preserving data and comparison semantics.**

A Codex Skill for experimental data, existing TeX and table screenshots. Deliver editable source, dependency notes and separate data, compilation and visual checks. Reference-driven layouts cover grouped comparisons, rotated headers, component ablations, aligned panels and paired gains; useful examples and repairs become reviewable design records.

[简体中文](README.md) · [Guide in Chinese](docs/guide.zh-CN.md) · [Skill contract](SKILL.md) · [Design principles](references/table-design-principles.md)

<!-- LOCAL-ONLY:BEGIN -->
**Private local reference index:** [Diffusion benchmark](#diffusion-main) · [Four-panel ablation](#representation-ablation) · [Paired gains](#paired-generation) · [Guidance control](#guidance-comparison) · [Algorithm listing](#meanflow-algorithm) · [Multimodal wide table](#multimodal-main) · [Data mixture](#data-mixture)
<!-- LOCAL-ONLY:END -->

## Table examples

These are compiled LaTeX tables with compact serif typography, restrained rules, and gray bands or pale row shading only where they carry a stated role. Caption position, weight and hierarchy follow each table or panel's explanatory role rather than one imposed template; the previews avoid card-like decoration. **All names, values and coverage assignments are synthetic, not experimental results.** Advanced layouts are agent-authored with checked records; they are not arbitrary-layout capabilities of the JSON generator.

### Grouped comparison with rotated headers

![Paper-style comparison with rotated metric labels, gray category bands and pale green featured rows](docs/images/showcase-main.png)

Italic gray bands separate families. Rotated labels fit long headings; bold and underline follow a declared comparison scope. Featured-row shading is separate from ranking.

[Editable TeX](docs/examples/showcase/showcase-main.tex) · [Original synthetic data](docs/examples/showcase/data.json)

### Aligned sensitivity panels

![Four aligned ablation subtables with gray default settings](docs/images/showcase-sensitivity.png)

One shared caption, four factors. Gray marks defaults; bold marks the best value within each panel and column.

[Editable TeX](docs/examples/showcase/showcase-sensitivity.tex) · [Synthetic data and cell ledger](docs/examples/showcase/academic-ledger.json)

### Paired comparisons with explicit gains

![Paired baseline and improved methods with gains relative to each encoder baseline](docs/images/showcase-paired.png)

Keep each baseline beside its improved variant. Accuracy gains use percentage points; increased latency remains a black cost annotation.

[Editable TeX](docs/examples/showcase/showcase-paired.tex)

### Component ablation

![Compact component ablation with uncertainty and baseline-relative gains](docs/images/showcase-ablation.png)

Preserve mean precision and standard deviations. State component meanings and delta baselines; ranking means does not establish significance.

[Editable TeX](docs/examples/showcase/showcase-ablation.tex)

### Coverage matrix

![Monochrome full, partial and empty coverage symbols with a legend](docs/images/showcase-coverage.png)

Shapes encode coverage without relying on color. Sizes, evaluation units and symbol meanings remain explicit.

[Editable TeX](docs/examples/showcase/showcase-coverage.tex) · [Rebuild previews](docs/render_showcase.py)

<!-- GALLERY:BEGIN -->

## Paired example gallery

Public count: 20 pairs in the public index; 15 displayed directly in this section.

The remaining 5 public pairs are already displayed directly in the sections above: showcase-main, showcase-sensitivity, showcase-paired, showcase-ablation, showcase-coverage

<!-- LOCAL-ONLY:BEGIN -->

Local reference images and source links below are private; public export strips this marked block.

### Local reference (private) (18)

There are 18 private local pairs, separate from 20 public examples.

### diffusion-main

| Original figure | Reconstruction |
| --- | --- |
| ![Original figure](assets/cases/local/diffusion-main/figure.png) | ![Reconstruction](assets/cases/local/diffusion-main/reproduced.png) |

[Reconstruction TeX](assets/cases/local/diffusion-main/table.tex) · [Review](assets/cases/local/diffusion-main/STYLE-REVIEW.json) · [Lesson](assets/cases/local/diffusion-main/lesson.json)

Role: grouped diffusion benchmark with a caption below. Visible matches: two-tier pre-training header, semantic vertical boundaries through the body, gray bands and bold roman JiT names. In the source, the latent label is italic (not bold) and the pixel label bold italic; the caption is three lines and there is no bottom rule.

### representation-ablation

| Original figure | Reconstruction |
| --- | --- |
| ![Original figure](assets/cases/local/representation-ablation/figure.png) | ![Reconstruction](assets/cases/local/representation-ablation/reproduced.png) |

[Reconstruction TeX](assets/cases/local/representation-ablation/table.tex) · [Review](assets/cases/local/representation-ablation/STYLE-REVIEW.json) · [Lesson](assets/cases/local/representation-ablation/lesson.json)

Role: one shared explanation above four side-by-side ablation panels. Visible matches: gray default rows, selective bold values and short panel notes; the source caption spans five lines and the panel tables are narrow/centered, with smaller body type than caption type.

### paired-generation

| Original figure | Reconstruction |
| --- | --- |
| ![Original figure](assets/cases/local/paired-generation/figure.png) | ![Reconstruction](assets/cases/local/paired-generation/reproduced.png) |

[Reconstruction TeX](assets/cases/local/paired-generation/table.tex) · [Review](assets/cases/local/paired-generation/STYLE-REVIEW.json) · [Lesson](assets/cases/local/paired-generation/lesson.json)

Role: paired baseline/RCG gain comparison. Visible matches: multirow method labels, thin pair separators, bold improved values and green signed gains in parentheses; the source table is compact and centered with its caption above.

### guidance-comparison

| Original figure | Reconstruction |
| --- | --- |
| ![Original figure](assets/cases/local/guidance-comparison/figure.png) | ![Reconstruction](assets/cases/local/guidance-comparison/reproduced.png) |

[Reconstruction TeX](assets/cases/local/guidance-comparison/table.tex) · [Review](assets/cases/local/guidance-comparison/STYLE-REVIEW.json) · [Lesson](assets/cases/local/guidance-comparison/lesson.json)

Role: two-tier metric comparison with and without guidance. Visible matches: gray text for the class-conditional population, block-boundary rules and italic group labels. Gray encodes population, not rank; keep this case as a control unless a mismatch is demonstrated.

### meanflow-algorithm

| Original figure | Reconstruction |
| --- | --- |
| ![Original figure](assets/cases/local/meanflow-algorithm/figure.png) | ![Reconstruction](assets/cases/local/meanflow-algorithm/reproduced.png) |

[Reconstruction TeX](assets/cases/local/meanflow-algorithm/table.tex) · [Review](assets/cases/local/meanflow-algorithm/STYLE-REVIEW.json) · [Lesson](assets/cases/local/meanflow-algorithm/lesson.json)

Role: pseudocode listing with title, note and syntax colors. Visible matches: narrow rules, teal comments and magenta keywords/callables. Function names are not underlined, equals signs are black, and the Note is small plain serif text.

### multimodal-main

| Original figure | Reconstruction |
| --- | --- |
| ![Original figure](assets/cases/local/multimodal-main/figure.png) | ![Reconstruction](assets/cases/local/multimodal-main/reproduced.png) |

[Reconstruction TeX](assets/cases/local/multimodal-main/table.tex) · [Review](assets/cases/local/multimodal-main/STYLE-REVIEW.json) · [Lesson](assets/cases/local/multimodal-main/lesson.json)

Role: wide main table split into video and image metrics. Visible matches: 65-degree rotated headers, category bands, pale-green target rows and separate thin block rules; shorten the header through matched type size/spacing, not a new angle.

### data-mixture

| Original figure | Reconstruction |
| --- | --- |
| ![Original figure](assets/cases/local/data-mixture/figure.png) | ![Reconstruction](assets/cases/local/data-mixture/reproduced.png) |

[Reconstruction TeX](assets/cases/local/data-mixture/table.tex) · [Review](assets/cases/local/data-mixture/STYLE-REVIEW.json) · [Lesson](assets/cases/local/data-mixture/lesson.json)

Role: image/video metric blocks for a data-mixture comparison. Visible matches: rotated headers, italic category bands, vertical block boundaries and a pale-green Full Mix row. The Full Mix label and video cells are bold while image cells remain regular; baseline value slant is uncertain, so do not encode a universal roman/italic rule.

<!-- LOCAL-ONLY:END -->

### Public pairs (15)

### Component ablation (structured synthetic)

![Component ablation](docs/images/public/ablation.png)

[TeX source](assets/cases/public/ablation/table.tex)

### Grouped benchmark (structured synthetic)

![Grouped benchmark](docs/images/public/benchmark.png)

[TeX source](assets/cases/public/benchmark/table.tex)

### Cross-dataset comparison (structured synthetic)

![Cross-dataset comparison](docs/images/public/cross-dataset.png)

[TeX source](assets/cases/public/cross-dataset/table.tex)

### Decimal alignment (structured synthetic)

![Decimal alignment](docs/images/public/decimal.png)

[TeX source](assets/cases/public/decimal/table.tex)

### Grouped multi-dataset table (structured synthetic)

![Grouped multi-dataset table](docs/images/public/multi-dataset.png)

[TeX source](assets/cases/public/multi-dataset/table.tex)

### Ties and missing values (structured synthetic)

![Ties and missing values](docs/images/public/ties-missing.png)

[TeX source](assets/cases/public/ties-missing/table.tex)

### Mean and uncertainty (structured synthetic)

![Mean and uncertainty](docs/images/public/uncertainty.png)

[TeX source](assets/cases/public/uncertainty/table.tex)

### Wide benchmark (structured synthetic)

![Wide benchmark](docs/images/public/wide.png)

[TeX source](assets/cases/public/wide/table.tex)

### Basic benchmark example (documentation synthetic)

![Basic benchmark example](docs/images/benchmark.png)

[TeX source](docs/examples/benchmark.tex)

### Basic ablation example (documentation synthetic)

![Basic ablation example](docs/images/ablation.png)

[TeX source](docs/examples/ablation.tex)

### Before refinement: full grid (refinement synthetic)

![Before refinement: full grid](docs/images/refinement-before.png)

[TeX source](docs/examples/refinement-before.tex)

### After refinement: sparse rules (refinement synthetic)

![After refinement: sparse rules](docs/images/refinement-after.png)

[TeX source](docs/examples/refinement-after.tex)

### Reuse baseline (design-reuse synthetic)

![Reuse baseline](docs/images/reuse-baseline.png)

[TeX source](docs/examples/design-reuse/baseline.tex)

### Grouped reuse variant (design-reuse synthetic)

![Grouped reuse variant](docs/images/reuse-grouped.png)

[TeX source](docs/examples/design-reuse/grouped-readable.tex)

### Compact reuse variant (design-reuse synthetic)

![Compact reuse variant](docs/images/reuse-compact.png)

[TeX source](docs/examples/design-reuse/compact-readable.tex)

<!-- LOCAL-ONLY:BEGIN -->

Local reference images and source links below are private; public export strips this marked block.

### Other local references (11)

### ablation_table-example1

| Original figure | Reconstruction |
| --- | --- |
| ![Original figure](assets/cases/local/ablation_table-example1/figure.png) | ![Reconstruction](assets/cases/local/ablation_table-example1/reproduction/image-style/reproduced.png) |

[Original TeX](assets/cases/local/ablation_table-example1/table.tex) · [Reconstruction TeX](assets/cases/local/ablation_table-example1/reproduction/image-style/run-style-3/build/table-build.tex) · [Review](assets/cases/local/ablation_table-example1/reproduction/REVIEW.md)

source-preserving style branch; source/image differences remain recorded

### ablation_table-example2

| Original figure | Reconstruction |
| --- | --- |
| ![Original figure](assets/cases/local/ablation_table-example2/figure.png) | ![Reconstruction](assets/cases/local/ablation_table-example2/reproduction/image-style/reproduced.png) |

[Original TeX](assets/cases/local/ablation_table-example2/table.tex) · [Reconstruction TeX](assets/cases/local/ablation_table-example2/reproduction/image-style/run-style-4/build/table-build.tex) · [Review](assets/cases/local/ablation_table-example2/reproduction/REVIEW.md)

source-preserving style branch; source/image differences remain recorded

### dataset_benchmark_table

| Original figure | Reconstruction |
| --- | --- |
| ![Original figure](assets/cases/local/dataset_benchmark_table/figure.png) | ![Reconstruction](assets/cases/local/dataset_benchmark_table/reproduction/image-style/reproduced.png) |

[Original TeX](assets/cases/local/dataset_benchmark_table/table.tex) · [Reconstruction TeX](assets/cases/local/dataset_benchmark_table/reproduction/image-style/run-style-3/build/table-build.tex) · [Review](assets/cases/local/dataset_benchmark_table/reproduction/REVIEW.md)

source-preserving style branch; source/image differences remain recorded

### main_table-example1

| Original figure | Reconstruction |
| --- | --- |
| ![Original figure](assets/cases/local/main_table-example1/figure.png) | ![Reconstruction](assets/cases/local/main_table-example1/reproduction/image-style/reproduced.png) |

[Original TeX](assets/cases/local/main_table-example1/table.tex) · [Reconstruction TeX](assets/cases/local/main_table-example1/reproduction/image-style/run-style-3/build/table-build.tex) · [Review](assets/cases/local/main_table-example1/reproduction/REVIEW.md)

source-preserving style branch; source/image differences remain recorded

### main_table-example2

| Original figure | Reconstruction |
| --- | --- |
| ![Original figure](assets/cases/local/main_table-example2/figure.png) | ![Reconstruction](assets/cases/local/main_table-example2/reproduction/image-style/reproduced.png) |

[Original TeX](assets/cases/local/main_table-example2/table.tex) · [Reconstruction TeX](assets/cases/local/main_table-example2/reproduction/image-style/run-style-4/build/table-build.tex) · [Review](assets/cases/local/main_table-example2/reproduction/REVIEW.md)

source-preserving style branch; source/image differences remain recorded

### main_table-example3

| Original figure | Reconstruction |
| --- | --- |
| ![Original figure](assets/cases/local/main_table-example3/figure.png) | ![Reconstruction](assets/cases/local/main_table-example3/reproduction/image-style/reproduced.png) |

[Original TeX](assets/cases/local/main_table-example3/table.tex) · [Reconstruction TeX](assets/cases/local/main_table-example3/reproduction/image-style/run-style-3/build/table-build.tex) · [Review](assets/cases/local/main_table-example3/reproduction/REVIEW.md)

source-preserving style branch; source/image differences remain recorded

### main_table-example4

| Original figure | Reconstruction |
| --- | --- |
| ![Original figure](assets/cases/local/main_table-example4/figure.png) | ![Reconstruction](assets/cases/local/main_table-example4/reproduction/image-style/reproduced.png) |

[Original TeX](assets/cases/local/main_table-example4/table.tex) · [Reconstruction TeX](assets/cases/local/main_table-example4/reproduction/image-style/run-style-3/build/table-build.tex) · [Review](assets/cases/local/main_table-example4/reproduction/REVIEW.md)

source-preserving style branch; source/image differences remain recorded

### others-example1

| Original figure | Reconstruction |
| --- | --- |
| ![Original figure](assets/cases/local/others-example1/figure.png) | ![Reconstruction](assets/cases/local/others-example1/reproduction/image-style/reproduced.png) |

[Original TeX](assets/cases/local/others-example1/table.tex) · [Reconstruction TeX](assets/cases/local/others-example1/reproduction/image-style/run-style-3/build/table-build.tex) · [Review](assets/cases/local/others-example1/reproduction/REVIEW.md)

source-preserving style branch; source/image differences remain recorded

### others-example2

| Original figure | Reconstruction |
| --- | --- |
| ![Original figure](assets/cases/local/others-example2/figure.png) | ![Reconstruction](assets/cases/local/others-example2/reproduction/image-style/reproduced.png) |

[Original TeX](assets/cases/local/others-example2/table.tex) · [Reconstruction TeX](assets/cases/local/others-example2/reproduction/image-style/run-style-3/build/table-build.tex) · [Review](assets/cases/local/others-example2/reproduction/REVIEW.md)

source-preserving style branch; source/image differences remain recorded

### others-example3

| Original figure | Reconstruction |
| --- | --- |
| ![Original figure](assets/cases/local/others-example3/figure.png) | ![Reconstruction](assets/cases/local/others-example3/reproduction/image-style/reproduced.png) |

[Original TeX](assets/cases/local/others-example3/table.tex) · [Reconstruction TeX](assets/cases/local/others-example3/reproduction/image-style/run-style-3/build/table-build.tex) · [Review](assets/cases/local/others-example3/reproduction/REVIEW.md)

source-preserving style branch; source/image differences remain recorded

### main_table-example4-image-23

| Original figure | Reconstruction |
| --- | --- |
| ![Original figure](assets/cases/local/main_table-example4/figure.png) | ![Reconstruction](assets/cases/local/main_table-example4/reproduction/image-only/styled-reproduced-v2.png) |

[Reconstruction TeX](assets/cases/local/main_table-example4/reproduction/image-only/styled-document-v2.tex)

23-column image branch, separate from 25-column code branch

<!-- LOCAL-ONLY:END -->

<!-- GALLERY:END -->

## Capabilities

| Capability | What it does |
| --- | --- |
| Table generation | Produce LaTeX tables from a JSON spec: `booktabs` rules, one grouped-header level, multiple datasets, ablation layouts. |
| Ranking & emphasis | Explicit higher/lower/none direction per column; **bold** best, <u>underline</u> distinct second best; shared marks for ties; missing values excluded; parameters unranked unless you ask. |
| Numeric fidelity | Explicit numeric source strings and precision are preserved in the data contract; no silent re-rounding. |
| Uncertainty display | Explicit mean/std or confidence intervals shown as configured; no significance inference is drawn for you. |
| Agent-assisted refinement | Complex or macro-heavy tables are refined via an agent-reviewed cell ledger, not blind LaTeX parsing. |
| Case retrieval | Deterministic local retrieval of similar public example cases. |
| Validation & preview | Static heuristic checks, TeX compilation and PDF rendering/inspection helpers. |
| Controlled learning | Records useful real examples or failure feedback as private candidates for later review. |

See [SKILL.md](SKILL.md) for the full contract.

## Installation

Easiest path: open Codex and ask —

> Install this local paper-latex-table-skill folder into my configured Codex skill directory, preserve existing skills, and verify discovery.

Manual installation (Windows PowerShell, run from this repository root):

```powershell
$source = (Resolve-Path .).Path
if (-not (Test-Path (Join-Path $source 'SKILL.md'))) { throw 'Run from the skill repository root.' }
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$destination = Join-Path $codexHome 'skills/paper-latex-table-skill'
if (Test-Path $destination) { throw 'Already installed; compare changes before updating.' }
New-Item -ItemType Directory -Force -Path (Split-Path $destination) | Out-Null
New-Item -ItemType Directory -Force -Path $destination | Out-Null
Get-ChildItem -LiteralPath $source -Force |
    Where-Object { $_.Name -notin @('.git', '.local', 'build', 'state', 'skill-state', '__pycache__') } |
    ForEach-Object { Copy-Item -LiteralPath $_.FullName -Destination $destination -Recurse }
```

After copying, confirm the skill is discovered and enabled in your Codex client; if the skill picker looks stale, restart Codex. Next turn, invoke `$paper-latex-table-skill`. These paths follow the current local Codex installation convention — adjust for your configured skill directory if it differs. User-directory installation normally requires no administrator privileges.

## Requirements

- Python 3.10+ (stdlib only for the helpers)
- An installed TeX engine (for `compile_table.py`)
- `pdftoppm`/Poppler (for PDF previews)
- Pillow, optionally, only if you regenerate the documentation preview images

## Quick start

Tell Codex what you want, naming the skill explicitly:

```text
$paper-latex-table-skill Create a grouped-header multi-dataset comparison from results/data.json.
$paper-latex-table-skill Improve the LaTeX in draft.tex to booktabs style without changing any data.
$paper-latex-table-skill Record the table in my_note.tex as a learning example; type is ablation, 9 columns, grouped headers.
$paper-latex-table-skill Check this table for overflow risk and verify the ranking marks are correct.
```

You can also drive the helpers directly from the repository root:

```text
python scripts/index_cases.py
python scripts/generate_table.py docs/examples/benchmark.json build/demo.tex
python scripts/validate_table.py build/demo.tex --spec docs/examples/benchmark.json
python scripts/compile_table.py build/demo.tex --output build/demo-compile
python scripts/inspect_render.py build/demo-compile/table-build.pdf --output build/demo-render
python scripts/retrieve_cases.py --columns 9 --type ablation --feature grouped_headers
```

Generation and compilation refuse existing outputs; use fresh filenames/directories when repeating these commands. Open the rendered PNGs to inspect the final table.

## Learning loop

The skill implements **controlled self-improvement**. When you supply a genuinely reusable example or report a real failure, `learning.py` records it as a pending private candidate with observed source hashes and evidence, stored outside the installed tree (default `$CODEX_HOME/skill-state/paper-latex-table-skill`, or `~/.codex/skill-state/...`), so it survives skill upgrades.

During authorized table tasks, useful observations can be captured as candidates. Stable promotion requires regression tests, compilation/visual/provenance review, explicit approval recorded with `rsi.py`, and manual integration. There is no background process, no autonomous rewrite of stable files, and no training of any model weights. Details: [references/continuous-learning.md](references/continuous-learning.md) and [rsi/improvement-policy.md](rsi/improvement-policy.md).

Record an example manually:

```text
python scripts/learning.py --kind case --source path/to/table.tex --reason "Reusable grouped-header pattern" --type ablation --columns 9 --feature grouped_headers
```

## Reproducibility & testing

Run the regression suite against your copy:

```text
python tests/test_tables.py
```

Regenerate the showcase (requires XeLaTeX, TeX Gyre fonts, Poppler and Pillow; choose a fresh build directory):

```text
python docs/render_showcase.py --build-root build/readme-showcase
```

## Scope & limits

- A passing compile is **not** a visual pass. Static checks are heuristic; test against the actual official conference template you are targeting before submission. Compatibility with any specific venue is not claimed.
- The public gallery contains twenty **synthetic** example pairs: eight structured cases plus showcase, basic, refinement and design-reuse variants. Private development references, if present, have separate provenance and redistribution rights and are excluded from the public export.
- Structured generation supports one grouped-header level. More complex refinement is agent-assisted and uses a reviewed ledger rather than a general LaTeX parser.
- Public demonstration previews use synthetic data; optional private references reproduce user-supplied sources, whose claims are not independently verified.

## Glossary

- **AUC**: area under the ROC curve — a threshold-independent single-number summary of classifier quality.
- **ROC**: receiver operating characteristic — true-positive rate plotted against false-positive rate across decision thresholds.
- **F1 score**: harmonic mean of precision and recall — rewards balanced performance instead of optimizing either one alone.

## Publishing a clean copy

Local-only cases (`assets/cases/local/`) and private learning state must never be published. The root `.gitignore` excludes them. If `index_cases` output is absent after cloning, run `python scripts/index_cases.py`.

To export only public material:

```text
python scripts/export_public.py ../dist/paper-latex-table-skill.zip
```

Publish the extracted `paper-latex-table-skill` subfolder from that archive — it contains the README, figures, sources and public cases only.

## License

See [LICENSE](LICENSE). License selection is still pending; nothing here grants rights to relicense user-provided examples or local references.

## Reference reconstruction and image input

Version 1.2.0 adds source-preserving local reproduction, explicit typography profiles, image transcription ledgers and separate code/image authority. The 10 paired code-and-figure cases support source-preserving compile comparisons; seven image-only references are manual transcriptions and reconstructions, not source-preserving reproductions. The original 23-file hash check covers only the initial 10 paired cases. See [input routes](references/input-routes.md) and [learned layout catalog](references/reference-catalog.md). Local case images and reconstruction evidence stay inside `assets/cases/local/`, excluded from public export. The local gallery documents residual differences rather than claiming pixel identity.

See [three RSI loops](references/three-rsi-loops.md) for paired/image-only learning, evidence-bound episodes and reviewed design recombination. Local design reuse and stable rule promotion are separate.

### Design reuse: one data contract, three candidates

![Three actual compiled layout candidates using the same synthetic data and 10pt body text](docs/images/design-reuse.png)

[Baseline TeX](docs/examples/design-reuse/baseline.tex) · [Grouped variant](docs/examples/design-reuse/grouped-readable.tex) · [Compact variant](docs/examples/design-reuse/compact-readable.tex). Synthetic data only; these are alternatives to inspect, not an automatically ranked aesthetic result.
