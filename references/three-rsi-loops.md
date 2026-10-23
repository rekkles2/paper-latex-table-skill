# Three evidence-based RSI loops

RSI (recursive self-improvement) here means accumulating verified design knowledge and repairs, not model-weight training. Three learning modes share one immutable episode format. Ordinary generation, selecting a suitable layout and recording local observations remain within the current task; they do not require a new stable-rule approval.

## 1. Code plus reference figure: paired reconstruction

1. Snapshot the TeX, main.tex/macros, atomic assets and reference image; declare purpose, target width and minimum physical font size.
2. Compare source and image at row/column/cell level. Record exact strings, precision, uncertainty, missing markers, row/column presence, citations and caption. Default data authority is original code; a contradictory image version gets its own transcription and TeX branch.
3. Recover actual definitions before inferring typography. Create a role/cell style ledger: font family, regular/bold/italic/bold-italic, size, underline, rotation, subscript, color and alignment. Record inferred font identity explicitly.
4. Produce the source-preserving baseline and at most two justified design/reconstruction alternatives. Compile, inspect full view and readable crops, then inspect at the requested physical width. Save compile reports, actual PDF/PNG, macro-restoration notes and comparisons.
5. Review data, source conflicts, typography, compilation, visual correspondence, physical readability and user constraints independently. Failed/pending checks retain a repairable case; they do not enter the reviewed-local atom pool. An accepted local design can be reused without changing stable skill rules.
6. Extract only design parameters actually present in that reviewed candidate. A generalizable repair can separately enter the stable `rsi.py` proposal, regression and explicit promotion path.

## 2. Figure only: reconstruct editable code, then learn

1. Preserve the supplied image and its hash. Read the full table and enlarged regions; separate raster ambiguity from unknown experimental evidence.
2. Build the keyed transcription ledger before authoring TeX. Every cell is `read`, `ambiguous` or `illegible`; ambiguous alternatives are recorded, and unresolved content renders `[?]`. Never infer a digit from a trend, ranking or expected average.
3. Record visible hierarchy and per-cell bold/italic/underline separately from numerical values. `transcribe_table.py` escapes text and supports these style combinations; it is not OCR. More complex scripts, typography and nested headers use agent-authored editable TeX with the same ledger.
4. Compile and compare the new render with the original. If adjustbox scales the table, check the resulting physical font size; a configured source size is not the final size. Do not flatten the table into the original screenshot. Keep irreducible logo crops separate and documented.
5. Recheck every semantic cell and style mark. Unresolved semantic cells block reviewed-local reuse and stable promotion, but do not prevent delivering a clearly marked draft. Self-review is named as such; independent review is not assumed.
6. Save successful reconstruction, font/macro decisions and demonstrated failure/repair together. Learn a case-specific design recipe first; generalize only what the evidence supports. Reuse the layout with new data, never the old experimental values.

## 3. Existing designs: retrieve, compose, compare and retain

1. Freeze the user's data contract, comparison groups, metric directions and constraints. Inspect relevant case metadata, typography ledgers, prior failures and `rsi_episode.py atoms` before proposing designs.
2. Decompose relevant designs into roles: header hierarchy, row groups, typography, emphasis, numeric alignment, rules/spacing, caption/notes. Record parent case IDs/versions and which role each contributes.
3. Reject incompatible combinations: conflicting comparison groups, unsupported header depth, too many color meanings, rank marks borrowed from an unrelated dataset, or a layout needing fonts below the minimum size. A visual feature alone never establishes numerical or experimental compatibility.
4. Keep a baseline and at most two alternative compositions. Use one meaningful design hypothesis per candidate, rather than accumulating decoration. `compose_designs.py` currently automates column spacing, row spacing and italic/bold-italic group hierarchy for the existing one-layer JSON renderer. It can load up to two reviewed local atoms. Deeper headers, palette/line systems and arbitrary TeX are agent-authored; do not claim automatic support.
5. The automated compositions keep the same data contract, unit strings, uncertainty, grouping and ranking semantics. `verify` regenerates the exact candidate and checks hashes. It does not certify aesthetics or measured width.
6. Compile at the actual target width and compare with the baseline. Require zero semantic differences, no clipping/overflow and readable text. Prefer the simplest candidate that meets the stated need and shows a concrete improvement (e.g. group boundaries clearer without reducing font size). Do not assign an arbitrary beauty score or declare an automatic winner.
7. Save the choice, rejected alternatives and reasons. Extract only reviewed declarative parameters as a versioned local atom. Every later load rechecks origin selection/review/artifact hashes; stale atoms are excluded. New evidence may justify a linked repair episode, with the prior failure retained.

## Executable episode workflow

Commands run from the skill root. State defaults outside the installed skill, under `$CODEX_HOME/skill-state/paper-latex-table-skill`, so updates preserve history. Source/reference packages remain self-contained in the skill; operational episodes are private and are not exported.

```text
python scripts/rsi_episode.py start --mode paired --source table.tex --source figure.png --requirements rsi/templates/rsi-requirements.json
python scripts/rsi_episode.py start --mode image-only --source figure.png --requirements rsi/templates/rsi-requirements.json
python scripts/rsi_episode.py start --mode reuse --source results.json --requirements rsi/templates/rsi-requirements.json
python scripts/rsi_episode.py candidate EPISODE --tex OUTPUT.tex --recipe RECIPE.json --artifact COMPILE_REPORT.json --artifact PREVIEW.png --artifact DATA_LEDGER.json --artifact TYPOGRAPHY.json
python scripts/rsi_episode.py review EPISODE CANDIDATE_ID --review REVIEW.json
python scripts/rsi_episode.py select EPISODE CANDIDATE_ID --reason "Why this candidate meets the constraints better than the baseline"
python scripts/rsi_episode.py extract EPISODE --design REVIEWED_DESIGN_CONFIG.json
python scripts/rsi_episode.py atoms
```

`start` prints the actual episode path; `candidate` prints its ID/path. Use those returned values, not the placeholders above. Review artifact paths refer to immutable numbered snapshots in `candidate.json`. Supply its `candidate_hash` and the episode's `input_hash`; declare the actual reviewer and exposure (`self_review` or `independent_review`). Each check has a status (`passed`, `failed`, `pending`) and nonempty artifact references. Image-only requires a `transcription` check; paired mode requires `source_conflicts`. Declare `unresolved_semantic_cells` explicitly. Reuse selection also requires a `baseline_comparison` explanation.

The template [rsi-review.json](../rsi/templates/rsi-review.json) deliberately starts with pending checks. Edit it only after real inspection. Review is an attestation checked for binding and completeness, not an automatic image grader. Failed/pending review stays in the episode as failure memory. Selecting a candidate does not copy it into stable skill files or make a paper claim true.

```text
python scripts/compose_designs.py generate docs/examples/benchmark.json --requirements rsi/templates/rsi-requirements.json --output build/layout-options
python scripts/compose_designs.py verify build/layout-options/grouped-readable
python scripts/compose_designs.py generate results.json --requirements my-requirements.json --atom PATH_TO_REVIEWED_ATOM.json --output build/reused-layout
```

`extract` accepts only the three supported style fields and checks they equal the reviewed recipe; changing parameters requires a new candidate and review. Atoms contain no arbitrary executable TeX. A local accepted style is useful evidence, not a universal rule.

## Promotion, stop rules and rollback

Stop when a candidate meets the actual task constraints and the required checks pass; stop after three independent candidates if none does, report the limiting constraint and keep the best clearly qualified draft. Repairs use a linked new episode rather than overwriting evidence. Avoid repeated external model retries; permission failures, service errors and timeouts are separate execution outcomes.

Promote stable instructions/scripts only for a demonstrated transferable benefit, using [improvement-policy.md](../rsi/improvement-policy.md). The maintained complete test harness runs against the candidate's modules and binds the full test-tree hash, not just one old test file. Snapshot creation excludes `.git` and `.local` so history does not recursively enter the baseline. Public redistribution additionally needs a rights review. Unknown rights permit private use, not public export.

No runner restores old files automatically. For rollback, inspect the baseline snapshot or a prior version and restore only the intended files after checking for newer changes. Original inputs, episode evidence and accepted prior recipes remain recoverable. Global promotion is explicit; routine design reuse is local and task-scoped.

The design was reviewed through OpenCode GLM-5.3 and independently checked by a Codex reviewer. Suggestions that incorrectly described automatic stable copying, mandatory human-only review or arbitrary selection scores were rejected. The implemented tracker and tests define actual behavior.
