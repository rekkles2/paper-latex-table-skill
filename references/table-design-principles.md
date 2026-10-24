# Academic table design

## Default: a table that belongs in a paper

Use the supplied paper screenshot as the visual authority for style, not as evidence for experimental claims. A README preview should resemble a cropped paper table, not a promotional card. Do not add oversized titles, slogans, chapter numbers, branding colors, decorative frames or large padding inside the image. Keep README commentary outside the compiled table.

Before applying general style defaults, make a short reference record: content-crop width/height ratio; table width relative to caption width; body glyph size relative to caption glyph size; observed caption line count and wrapping; visible family evidence plus weight and slant; rule thickness, spacing around rules, and panel gutters; and each cell/row's emphasis role. Use the source crop, not page dimensions, as the comparison unit and aim for a rendered crop aspect within 10% of it. This tolerance is a working calibration goal, not a claim about original page or font metadata. Match these observations first, then make a separate readability adjustment only if needed.

Use visible source features rather than a universal house style. Compact serif type, sparse rules, a bold caption lead, booktabs rules, italic group bands, bold winners, or underlined runners-up are options only when the reference or task supports them. Preserve a shown vertical semantic boundary; do not replace source-specific rules with booktabs for consistency. A shared caption and panel-level explanations are not interchangeable. Table numbers in demonstrations are illustrative; real manuscript numbers must come from its counter. Preserve captions in grammar-only or typography-only work unless explicitly authorized.

## Select the structure from the question

- Main comparison: grouped metric columns, italic category bands on light gray, clear comparison scopes; an optional pale green featured row when supported by the reference.
- Wide benchmark: rotate long metric labels while keeping body values upright. Use thin vertical separators only between major semantic blocks when the reference uses them; do not turn this into a full grid.
- Sensitivity ablation: align two to four subtables, with one factor per panel and a shared caption. Gray marks a declared default, not automatically a best value. Keep panel labels and parameter units explicit.
- Paired improvement: place baseline and improved method together; separate pairs with thin rules. Compute deltas within each pair, state their units, and avoid coloring a latency increase as an improvement.
- Component ablation: align binary toggles, group results, de-emphasize uncertainty moderately, and identify the delta baseline.
- Coverage matrix: use full/partial/empty symbols plus a legend; shapes must carry meaning in grayscale.
- Algorithm screenshots are typography references only. Do not claim algorithm rendering or pseudocode support unless that separate route is implemented and verified.

## Data and emphasis

Declare metric direction and comparison scope before ranking. Bold best and underline distinct second only when requested or consistent with the reference; ties share marks, missing values are excluded. Default rows and featured methods have separate semantics from ranking. Keep names, citations, missing tokens, uncertainties, precision and precomputed ranks unchanged. Source and screenshot disagreements require separate versions.

Use limited color only for a functional role: neutral gray groups/defaults, a pale featured row, reference-matched citation links, or a signed gain. Never invent citations to imitate blue reference numbers. Favor black text over a global tinted palette; validate grayscale readability.

## Fit and inspect

Start at the target column/text width and measured source ratios. Adjust native TeX font size, column padding, row spacing, natural table width and panel gutters; reduce redundant labels, wrap headings or split panels only when content permits. Never use `\resizebox`, `\scalebox`, negative spacing, or a raster image in place of an editable table. Avoid automatic tiny text. Standalone previews should state their configured width and body size; they do not prove venue-template compliance. Do not infer original font metadata from a screenshot; report substitutions and fallbacks explicitly.

Check crop aspect, caption/table width and type-size ratios, caption wrapping, weight/slant, long rotated headings, rule gaps, rules through bands, panel gutters, cell-level marks, symbols and missing glyphs against the reference. Numerical fidelity, compilation, visual correspondence, final-size readability and reference rights are separate checks. Compile success alone is not visual acceptance; do not claim a new render passed until it has actually been opened and compared.
