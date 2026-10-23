# Venue compatibility is evidence, not a preset

CVPR, ICCV, NeurIPS, ICML, ICLR and IEEE Transactions may differ in class options, caption handling, font size, float placement and permitted packages. Version 1 ships no official class files and verifies none of these venues. Do not advertise a venue-specific pass from generic article output.

Ask for or locate the actual submission-year official template when venue compliance matters. Use its documentclass and preamble unchanged; respect columnwidth vs textwidth, use table* only where supported, and keep bibliography/ref resolution inside that project. `compile_table.py` accepts a full document containing documentclass and does not inject its generic wrapper into it. Run with explicit engine if required by the template, and ensure support files are resolvable relative to the source directory. Some full projects require latexmk/bibtex or custom build steps beyond the two-pass convenience wrapper; use their existing build command and record it.

Record template URL, year/version, class hash, engine, package versions and actual tested document. Unknown provenance or a caption containing 'CVPR' is not proof of venue identity. Never modify official style files to make a table fit.
