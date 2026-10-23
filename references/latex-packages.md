# Packages: use only what the table needs

Official references verified during development (2026-10-23): [booktabs](https://ctan.org/pkg/booktabs), [siunitx](https://ctan.org/pkg/siunitx/), [tabularx manual](https://texdoc.org/serve/tabularx.pdf/0). Additional package entry points: [multirow](https://ctan.org/pkg/multirow), [adjustbox](https://ctan.org/pkg/adjustbox).

| Need | Package / check |
|---|---|
| Top/mid/bottom rules, cmidrule | booktabs |
| Decimal alignment, units | siunitx; S headers/missing markers protected with braces or multicolumn; inspect installed version using kpsewhich and compile log `\\listfiles` |
| Merged row labels | multirow; check vertical placement across group rules |
| Wrapped headers | makecell; do not copy unavailable custom macros |
| Text wrapping at given width | tabularx + array; X columns may re-evaluate content |
| Bounded maximum width | adjustbox; inspect actual scaling |
| Row/cell colors | xcolor with table option (colortbl) |
| Dashed rules | arydshln; avoid loading unless required |

Current CTAN and installed TeX versions may differ. Keep syntax compatible with the installed version; do not upgrade TeX silently. A generic compilation wrapper loads the common packages for diagnosis, so it does not establish a minimal dependency set. Provide final imports explicitly and compile in the actual paper preamble. Omit wrapper geometry/caption changes from official templates. Undefined private macros or absent icon assets are blockers to source-faithful compilation; do not invent invisible stubs.
