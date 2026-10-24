# Coverage Symbols

Coverage cells use `symbol` values `full`, `half`, or `empty` in the public ledger passed to `generate(ledger)`. The ledger contains `columns` (`id`, `label`), `rows` (`id`, `cells` keyed by column id), and `caption`; each cell has a `status` and `symbol`. `generate` returns `(tex_string, unresolved_list)`. Unknown symbols raise `ValueError`.

All three TikZ marks share the same `(-.89ex,-.89ex)` to `(.89ex,.89ex)` bounding box, baseline, and `.78ex` outer radius. `full` is solid, `half` fills the left semicircle and draws the circular outline, and `empty` draws an unfilled outline. The half mark has no center divider.