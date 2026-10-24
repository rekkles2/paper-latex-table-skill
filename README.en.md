# Paper LaTeX Table Skill

**Generate, refine and reconstruct scientific LaTeX tables while preserving data and comparison semantics.**

A Codex Skill for experimental data, existing TeX and table screenshots. Deliver editable source, dependency notes and separate data, compilation and visual checks. Reference-driven layouts cover grouped comparisons, rotated headers, component ablations, aligned panels and paired gains; useful examples and repairs become reviewable design records.

[简体中文](README.md) · [Guide in Chinese](docs/guide.zh-CN.md) · [Skill contract](SKILL.md) · [Design principles](references/table-design-principles.md)

## Table Examples

Each comparison table presents the original reference figure on the left (with an explicit disclosure when the original image is unavailable) and the compiled, editable LaTeX reconstruction on the right; click any image to inspect it at full resolution, and use the TeX row links to access the corresponding source files.

### Benchmark Comparison

#### Public Benchmark Comparison

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| Not provided; this is a project-authored synthetic example. | ![Skill Reconstruction](examples/public/public-benchmark/reconstruction.png) |
| **TeX:** Missing (no original TeX provided) | **TeX:** [Reconstruction TeX](examples/public/public-benchmark/reconstruction.tex) |

#### Public Wide-Table Comparison

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| Not provided; this is a project-authored synthetic example. | ![Skill Reconstruction](examples/public/public-wide/reconstruction.png) |
| **TeX:** Missing (no original TeX provided) | **TeX:** [Reconstruction TeX](examples/public/public-wide/reconstruction.tex) |

#### Main-Table Showcase

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| Not provided; this is a project-authored synthetic example. | ![Skill Reconstruction](examples/public/showcase-main/reconstruction.png) |
| **TeX:** Missing (no original TeX provided) | **TeX:** [Reconstruction TeX](examples/public/showcase-main/reconstruction.tex) |

#### Paired-Generation Showcase

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| Not provided; this is a project-authored synthetic example. | ![Skill Reconstruction](examples/public/showcase-paired/reconstruction.png) |
| **TeX:** Missing (no original TeX provided) | **TeX:** [Reconstruction TeX](examples/public/showcase-paired/reconstruction.tex) |

<!-- LOCAL-ONLY:BEGIN -->
#### Main Table Example 1

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| ![Original Image](examples/references/main_table-example1/original.png) | ![Skill Reconstruction](examples/references/main_table-example1/reconstruction.png) |
| **TeX:** [Original TeX](examples/references/main_table-example1/original.tex) | **TeX:** [Reconstruction TeX](examples/references/main_table-example1/reconstruction.tex) |

<!-- LOCAL-ONLY:END -->

<!-- LOCAL-ONLY:BEGIN -->
#### Main Table Example 2

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| ![Original Image](examples/references/main_table-example2/original.png) | ![Skill Reconstruction](examples/references/main_table-example2/reconstruction.png) |
| **TeX:** [Original TeX](examples/references/main_table-example2/original.tex) | **TeX:** [Reconstruction TeX](examples/references/main_table-example2/reconstruction.tex) |

<!-- LOCAL-ONLY:END -->

<!-- LOCAL-ONLY:BEGIN -->
#### Main Table Example 3

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| ![Original Image](examples/references/main_table-example3/original.png) | ![Skill Reconstruction](examples/references/main_table-example3/reconstruction.png) |
| **TeX:** [Original TeX](examples/references/main_table-example3/original.tex) | **TeX:** [Reconstruction TeX](examples/references/main_table-example3/reconstruction.tex) |

<!-- LOCAL-ONLY:END -->

<!-- LOCAL-ONLY:BEGIN -->
#### Main Table: 25-Column Source Branch

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| No matching original image was supplied for this 25-column TeX branch; the preserved screenshot belongs to the separate Image-23 branch below. | ![Skill Reconstruction](examples/references/main_table-example4/reconstruction.png) |
| **TeX:** [Original TeX](examples/references/main_table-example4/original.tex) | **TeX:** [Reconstruction TeX](examples/references/main_table-example4/reconstruction.tex) |

Provenance: Unresolved citation keys: aircraft, basic, cars, cheng_2017_resisc, coca, coco, dfn, eva18b, flickr, flower102, food101, imagenet, imagenet-a, imagenet-r, imagenet-sketch, imagenetv2, internvl, objectnet, pali, pets, siglip, siglip2, sun397, thomee2016yfcc100m, vit, vit22b; Unresolved cross-reference labels: appx:zeroshot_settings; Source TeX is from the 25-column branch; image-23 is a separate image branch and must not be represented as its matching source image.

<!-- LOCAL-ONLY:END -->

<!-- LOCAL-ONLY:BEGIN -->
#### Main Table: Image-23 Branch

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| ![Original Image](examples/references/main_table-example4-image-23/original.png) | ![Skill Reconstruction](examples/references/main_table-example4-image-23/reconstruction.png) |
| **TeX:** Missing (no original TeX provided) | **TeX:** [Reconstruction TeX](examples/references/main_table-example4-image-23/reconstruction.tex) |

Provenance: The 23-column count includes metadata columns such as model, parameters, resolution and data. This image-authoritative branch is separate from the 25-column source branch and from the 13 benchmark metric columns in the Cambrian-S table.

<!-- LOCAL-ONLY:END -->

<!-- LOCAL-ONLY:BEGIN -->
#### Diffusion Benchmark Comparison

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| ![Original Image](examples/references/diffusion-main/original.png) | ![Skill Reconstruction](examples/references/diffusion-main/reconstruction.png) |
| **TeX:** Missing (no original TeX provided) | **TeX:** [Reconstruction TeX](examples/references/diffusion-main/reconstruction.tex) |

<!-- LOCAL-ONLY:END -->

<!-- LOCAL-ONLY:BEGIN -->
#### Paired-Generation Comparison

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| ![Original Image](examples/references/paired-generation/original.png) | ![Skill Reconstruction](examples/references/paired-generation/reconstruction.png) |
| **TeX:** Missing (no original TeX provided) | **TeX:** [Reconstruction TeX](examples/references/paired-generation/reconstruction.tex) |

<!-- LOCAL-ONLY:END -->

<!-- LOCAL-ONLY:BEGIN -->
#### Guidance Comparison

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| ![Original Image](examples/references/guidance-comparison/original.png) | ![Skill Reconstruction](examples/references/guidance-comparison/reconstruction.png) |
| **TeX:** Missing (no original TeX provided) | **TeX:** [Reconstruction TeX](examples/references/guidance-comparison/reconstruction.tex) |

Provenance: Unresolved citation keys: 10, 18, 2, 24, 29, 34, 36, 38, 50, 54, 6, 68

<!-- LOCAL-ONLY:END -->

<!-- LOCAL-ONLY:BEGIN -->
#### Multimodal Benchmark Comparison

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| ![Original Image](examples/references/multimodal-main/original.png) | ![Skill Reconstruction](examples/references/multimodal-main/reconstruction.png) |
| **TeX:** Missing (no original TeX provided) | **TeX:** [Reconstruction TeX](examples/references/multimodal-main/reconstruction.tex) |

<!-- LOCAL-ONLY:END -->

### Ablation Study

#### Public Ablation Example

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| Not provided; this is a project-authored synthetic example. | ![Skill Reconstruction](examples/public/public-ablation/reconstruction.png) |
| **TeX:** Missing (no original TeX provided) | **TeX:** [Reconstruction TeX](examples/public/public-ablation/reconstruction.tex) |

#### Sensitivity-Analysis Showcase

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| Not provided; this is a project-authored synthetic example. | ![Skill Reconstruction](examples/public/showcase-sensitivity/reconstruction.png) |
| **TeX:** Missing (no original TeX provided) | **TeX:** [Reconstruction TeX](examples/public/showcase-sensitivity/reconstruction.tex) |

#### Ablation-Study Showcase

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| Not provided; this is a project-authored synthetic example. | ![Skill Reconstruction](examples/public/showcase-ablation/reconstruction.png) |
| **TeX:** Missing (no original TeX provided) | **TeX:** [Reconstruction TeX](examples/public/showcase-ablation/reconstruction.tex) |

#### Basic Ablation Example

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| Not provided; this is a project-authored synthetic example. | ![Skill Reconstruction](examples/public/basic-ablation/reconstruction.png) |
| **TeX:** Missing (no original TeX provided) | **TeX:** [Reconstruction TeX](examples/public/basic-ablation/reconstruction.tex) |

<!-- LOCAL-ONLY:BEGIN -->
#### Ablation Table Example 1

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| ![Original Image](examples/references/ablation_table-example1/original.png) | ![Skill Reconstruction](examples/references/ablation_table-example1/reconstruction.png) |
| **TeX:** [Original TeX](examples/references/ablation_table-example1/original.tex) | **TeX:** [Reconstruction TeX](examples/references/ablation_table-example1/reconstruction.tex) |

<!-- LOCAL-ONLY:END -->

<!-- LOCAL-ONLY:BEGIN -->
#### Ablation Table Example 2

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| ![Original Image](examples/references/ablation_table-example2/original.png) | ![Skill Reconstruction](examples/references/ablation_table-example2/reconstruction.png) |
| **TeX:** [Original TeX](examples/references/ablation_table-example2/original.tex) | **TeX:** [Reconstruction TeX](examples/references/ablation_table-example2/reconstruction.tex) |

<!-- LOCAL-ONLY:END -->

<!-- LOCAL-ONLY:BEGIN -->
#### Representation Ablation

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| ![Original Image](examples/references/representation-ablation/original.png) | ![Skill Reconstruction](examples/references/representation-ablation/reconstruction.png) |
| **TeX:** Missing (no original TeX provided) | **TeX:** [Reconstruction TeX](examples/references/representation-ablation/reconstruction.tex) |

<!-- LOCAL-ONLY:END -->

<!-- LOCAL-ONLY:BEGIN -->
#### Data-Mixture Ablation

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| ![Original Image](examples/references/data-mixture/original.png) | ![Skill Reconstruction](examples/references/data-mixture/reconstruction.png) |
| **TeX:** Missing (no original TeX provided) | **TeX:** [Reconstruction TeX](examples/references/data-mixture/reconstruction.tex) |

<!-- LOCAL-ONLY:END -->

### Dataset Comparison & Capability Matrix

#### Public Cross-Dataset Example

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| Not provided; this is a project-authored synthetic example. | ![Skill Reconstruction](examples/public/public-cross-dataset/reconstruction.png) |
| **TeX:** Missing (no original TeX provided) | **TeX:** [Reconstruction TeX](examples/public/public-cross-dataset/reconstruction.tex) |

#### Public Multi-Dataset Example

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| Not provided; this is a project-authored synthetic example. | ![Skill Reconstruction](examples/public/public-multi-dataset/reconstruction.png) |
| **TeX:** Missing (no original TeX provided) | **TeX:** [Reconstruction TeX](examples/public/public-multi-dataset/reconstruction.tex) |

#### Dataset Capability Matrix

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| Not provided; this is a project-authored synthetic example. | ![Skill Reconstruction](examples/public/showcase-coverage/reconstruction.png) |
| **TeX:** Missing (no original TeX provided) | **TeX:** [Reconstruction TeX](examples/public/showcase-coverage/reconstruction.tex) |

<!-- LOCAL-ONLY:BEGIN -->
#### Dataset Benchmark Table

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| ![Original Image](examples/references/dataset_benchmark_table/original.png) | ![Skill Reconstruction](examples/references/dataset_benchmark_table/reconstruction.png) |
| **TeX:** [Original TeX](examples/references/dataset_benchmark_table/original.tex) | **TeX:** [Reconstruction TeX](examples/references/dataset_benchmark_table/reconstruction.tex) |

<!-- LOCAL-ONLY:END -->

<!-- LOCAL-ONLY:BEGIN -->
#### Related-Datasets Table

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| ![Original Image](examples/references/related-datasets/original.png) | ![Skill Reconstruction](examples/references/related-datasets/reconstruction.png) |
| **TeX:** Missing (no original TeX provided) | **TeX:** [Reconstruction TeX](examples/references/related-datasets/reconstruction.tex) |

Provenance: Original TeX not provided; caption claims not independently verified.

<!-- LOCAL-ONLY:END -->

### Human–Judge Evaluation

<!-- LOCAL-ONLY:BEGIN -->
#### Human-Judge Evaluation

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| ![Original Image](examples/references/human-judge/original.png) | ![Skill Reconstruction](examples/references/human-judge/reconstruction.png) |
| **TeX:** Missing (no original TeX provided) | **TeX:** [Reconstruction TeX](examples/references/human-judge/reconstruction.tex) |

Provenance: Original TeX not provided; caption claims not independently verified.

<!-- LOCAL-ONLY:END -->

### Qualitative VQA

<!-- LOCAL-ONLY:BEGIN -->
#### Behavioral VQA Examples

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| ![Original Image](examples/references/behavior-vqa/original.png) | ![Skill Reconstruction](examples/references/behavior-vqa/reconstruction.png) |
| **TeX:** Missing (no original TeX provided) | **TeX:** [Reconstruction TeX](examples/references/behavior-vqa/reconstruction.tex) |

Provenance: Original TeX not provided; caption claims not independently verified.

<!-- LOCAL-ONLY:END -->

### Algorithms & Protocols

<!-- LOCAL-ONLY:BEGIN -->
#### Protocol Example 1

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| ![Original Image](examples/references/others-example1/original.png) | ![Skill Reconstruction](examples/references/others-example1/reconstruction.png) |
| **TeX:** [Original TeX](examples/references/others-example1/original.tex) | **TeX:** [Reconstruction TeX](examples/references/others-example1/reconstruction.tex) |

<!-- LOCAL-ONLY:END -->

<!-- LOCAL-ONLY:BEGIN -->
#### Protocol Example 2

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| ![Original Image](examples/references/others-example2/original.png) | ![Skill Reconstruction](examples/references/others-example2/reconstruction.png) |
| **TeX:** [Original TeX](examples/references/others-example2/original.tex) | **TeX:** [Reconstruction TeX](examples/references/others-example2/reconstruction.tex) |

<!-- LOCAL-ONLY:END -->

<!-- LOCAL-ONLY:BEGIN -->
#### Protocol Example 3

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| ![Original Image](examples/references/others-example3/original.png) | ![Skill Reconstruction](examples/references/others-example3/reconstruction.png) |
| **TeX:** [Original TeX](examples/references/others-example3/original.tex) | **TeX:** [Reconstruction TeX](examples/references/others-example3/reconstruction.tex) |

<!-- LOCAL-ONLY:END -->

<!-- LOCAL-ONLY:BEGIN -->
#### MeanFlow Algorithm

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| ![Original Image](examples/references/meanflow-algorithm/original.png) | ![Skill Reconstruction](examples/references/meanflow-algorithm/reconstruction.png) |
| **TeX:** Missing (no original TeX provided) | **TeX:** [Reconstruction TeX](examples/references/meanflow-algorithm/reconstruction.tex) |

<!-- LOCAL-ONLY:END -->

### Numerical Reporting & Refinement

#### Public Decimal-Reporting Example

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| Not provided; this is a project-authored synthetic example. | ![Skill Reconstruction](examples/public/public-decimal/reconstruction.png) |
| **TeX:** Missing (no original TeX provided) | **TeX:** [Reconstruction TeX](examples/public/public-decimal/reconstruction.tex) |

#### Public Ties and Missing-Values Example

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| Not provided; this is a project-authored synthetic example. | ![Skill Reconstruction](examples/public/public-ties-missing/reconstruction.png) |
| **TeX:** Missing (no original TeX provided) | **TeX:** [Reconstruction TeX](examples/public/public-ties-missing/reconstruction.tex) |

#### Public Uncertainty-Reporting Example

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| Not provided; this is a project-authored synthetic example. | ![Skill Reconstruction](examples/public/public-uncertainty/reconstruction.png) |
| **TeX:** Missing (no original TeX provided) | **TeX:** [Reconstruction TeX](examples/public/public-uncertainty/reconstruction.tex) |

#### After Numerical Refinement

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| ![Original Image](examples/public/refinement-after/original.png) | ![Skill Reconstruction](examples/public/refinement-after/reconstruction.png) |
| **TeX:** [Original TeX](examples/public/refinement-after/original.tex) | **TeX:** [Reconstruction TeX](examples/public/refinement-after/reconstruction.tex) |

Provenance: Original image is a project-authored synthetic baseline, not an external source-paper image.

#### Grouped Design Reuse

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| ![Original Image](examples/public/reuse-grouped/original.png) | ![Skill Reconstruction](examples/public/reuse-grouped/reconstruction.png) |
| **TeX:** [Original TeX](examples/public/reuse-grouped/original.tex) | **TeX:** [Reconstruction TeX](examples/public/reuse-grouped/reconstruction.tex) |

Provenance: Original image is a project-authored synthetic baseline, not an external source-paper image.

#### Compact Design Reuse

| Original Reference Figure | Editable Skill Reconstruction |
| :--- | :--- |
| ![Original Image](examples/public/reuse-compact/original.png) | ![Skill Reconstruction](examples/public/reuse-compact/reconstruction.png) |
| **TeX:** [Original TeX](examples/public/reuse-compact/original.tex) | **TeX:** [Reconstruction TeX](examples/public/reuse-compact/reconstruction.tex) |

Provenance: Original image is a project-authored synthetic baseline, not an external source-paper image.

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
- The current gallery has **38 canonical examples** in seven categories: 17 public synthetic examples and 21 private reference reconstructions. All 41 input identifiers remain represented through canonical entries, aliases and baseline relationships. The 20 public input entries are consolidated into 17 canonical examples without deleting the original files. Private references have separate provenance and redistribution rights and are excluded from the public export.
- Structured generation supports one grouped-header level. More complex refinement is agent-assisted and uses a reviewed ledger rather than a general LaTeX parser.
- Public demonstration previews use synthetic data; optional private references reproduce user-supplied sources, whose claims are not independently verified.

## Glossary

- **AUC**: area under the ROC curve — a threshold-independent single-number summary of classifier quality.
- **ROC**: receiver operating characteristic — true-positive rate plotted against false-positive rate across decision thresholds.
- **F1 score**: harmonic mean of precision and recall — rewards balanced performance instead of optimizing either one alone.

## Publishing a clean copy

The full local gallery includes private reference assets in `examples/references/`; the current repository is private. Public exports exclude that directory, local-only cases (`assets/cases/local/`) and private learning state, and filter the README and catalog accordingly. The root `.gitignore` excludes the raw local cases. Review redistribution rights before changing repository visibility. If `index_cases` output is absent after cloning, run `python scripts/index_cases.py`.

To export only public material:

```text
python scripts/export_public.py ../dist/paper-latex-table-skill.zip
```

Publish the extracted `paper-latex-table-skill` subfolder from that archive — it contains the README, figures, sources and public cases only.

## License

See [LICENSE](LICENSE). License selection is still pending; nothing here grants rights to relicense user-provided examples or local references.

## Reference reconstruction and image input

Version 1.3.0 organizes the original 18 reference pairs and three new image-only cases into 21 private reference entries. Related Datasets, Human–Judge and Behavior VQA include standalone editable TeX; missing original TeX is stated explicitly. The historical 10 paired code-and-figure cases support source-preserving compile comparisons; image-only references use checked transcription and reconstruction. The original 23-file hash check covers only the initial 10 paired cases. See [input routes](references/input-routes.md), the historical [learned layout catalog](references/reference-catalog.md), and the current [example catalog](docs/example-catalog.json). Private assets and evidence are excluded from public exports. The gallery documents source conflicts and residual differences rather than claiming pixel identity.

See [three RSI loops](references/three-rsi-loops.md) for paired/image-only learning, evidence-bound episodes and reviewed design recombination. Local design reuse and stable rule promotion are separate.
