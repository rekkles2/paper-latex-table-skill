# Paper LaTeX Table Skill

**paper-latex-table-skill** is a local Codex Agent Skill that turns experimental results into clean, publication-ready LaTeX tables. It covers `booktabs` styling, grouped headers, multi-dataset comparisons and ablation studies, with deterministic highlighting rules (bold best, underline second best), checks for numerical fidelity, and a controlled learning loop so the skill can improve from real usage without touching model weights.

It is designed for researchers using Codex who want consistent, defensible tables rather than hand-tuned LaTeX battles. The local helper tools require no additional model account, embedding service or network call; Codex supplies the host agent.

[简体中文使用指南（Guide in Chinese）](docs/guide.zh-CN.md)

## Example output

All figures below were compiled from the bundled example sources using **independently authored synthetic data**; they are not real experimental measurements and not automatically scored visual benchmarks.

![Compiled LaTeX grouped multi-dataset comparison table showing accuracy and latency tradeoffs across synthetic datasets.](docs/images/benchmark.png)

AUC denotes area under the receiver operating characteristic curve; F1 denotes the F1 score.

*A multi-dataset comparison with grouped headers: accuracy versus latency tradeoffs. Editable source and spec: [docs/examples/benchmark.json](docs/examples/benchmark.json). All values synthetic.*

![Compiled LaTeX component ablation table reporting mean and standard deviation for each configuration.](docs/images/ablation.png)

*A component ablation with mean ± std display. Editable spec: [docs/examples/ablation.json](docs/examples/ablation.json). All values synthetic.*

![Before-and-after comparison of a synthetic grid-rule table and its booktabs refinement where all body cells are identical.](docs/images/refinement.png)

*A refinement example: same data, from grid rules to booktabs. Editable sources: [before](docs/examples/refinement-before.tex) / [after](docs/examples/refinement-after.tex).*

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
Copy-Item -LiteralPath $source -Destination $destination -Recurse
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

Optional: regenerate the documentation preview images (requires TeX, Poppler and Pillow):

```text
python docs/render_previews.py --build-root build/readme-previews
```

## Scope & limits

- A passing compile is **not** a visual pass. Static checks are heuristic; test against the actual official conference template you are targeting before submission. Compatibility with any specific venue is not claimed.
- The public bundle contains eight original **synthetic** example cases. Private development references, if present, have separate provenance and redistribution rights and are excluded from the public export.
- Structured generation supports one grouped-header level. More complex refinement is agent-assisted and uses a reviewed ledger rather than a general LaTeX parser.
- Every preview figure in this README uses synthetic data.

## Publishing a clean copy

Local-only cases (`assets/cases/local/`) and private learning state must never be published. The root `.gitignore` excludes them. If `index_cases` output is absent after cloning, run `python scripts/index_cases.py`.

To export only public material:

```text
python scripts/export_public.py ../dist/paper-latex-table-skill.zip
```

Publish the extracted `paper-latex-table-skill` subfolder from that archive — it contains the README, figures, sources and public cases only.

## License

See [LICENSE](LICENSE). License selection is still pending; nothing here grants rights to relicense user-provided examples or local references.
