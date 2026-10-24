# Visual Fidelity Lessons

- Match the source's font character, weight, and rule continuity; do not substitute a merely similar overall style.
- Use native glyphs with matching stroke weight. Reproduce visible source glyphs with `pifont` when appropriate.
- Preserve highlighted cells as literal source annotations. Do not recompute rankings or move highlights based on derived values.
- Keep means and standard deviations in their source fields, with their source colors and formatting.
- When a requested color applies to text in a quoted prompt, color exactly the requested word span and exclude adjacent punctuation.
- If reviewers or models disagree about a visual detail, inspect the source and reconstruction closely at enlarged scale before deciding.
- When source code and a source image conflict, preserve and document the discrepancy. Do not invent a reconciliation.
- Record visual review status honestly; do not claim pixel identity or that every model check is complete without evidence.

- For wide tables, verify each value against both its row label and its column header; a visually plausible row can still contain shifted values.
- Scope boldface to the exact source highlights; a declaration before a tabular can accidentally bold its entire body.
- Check full-span section rows with vertical rules after rendering. If a rule-patching package is unnecessary and disrupts spans, omit it from the standalone reconstruction.
