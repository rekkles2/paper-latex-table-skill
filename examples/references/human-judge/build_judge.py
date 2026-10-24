#!/usr/bin/env python3
"""Standalone XeLaTeX generator for Table 1 (Human and MLLM-as-a-Judge scores)."""

import argparse
import json
import re
from pathlib import Path

EXPECTED_COLUMNS = [
    "Add", "Remove", "Replace", "Action", "Counting", "Relation", "All Edits"
]

GROUPS = [
    ("Image Preserv.", "grpPreserv", [
        "Unchanged Regions", "Global Consistency", "Identity Preservation"
    ]),
    ("Edit Quality", "grpQuality", [
        "Scale Realism", "Spatial Relationship", "Texture and Detail",
        "Image Quality", "Color and Lighting", "Seamlessness"
    ]),
    ("Instruct. Fidel.", "grpFidel", [
        "Alignment", "Completeness", "Plausibility"
    ]),
]

EXPECTED_FACTORS = [f for _, _, factors in GROUPS for f in factors] + ["Overall Average"]
MEAN_RE = re.compile(r"^\d+\.\d{3}$")
STD_RE = re.compile(r"^\d+\.\d{2}$")
VALID_HIGHLIGHTS = {"none", "light", "dark"}


def load_ledger(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        for line in raw.splitlines():
            s = line.strip()
            if s.startswith("{") and s.endswith("}"):
                return json.loads(s)
        start, end = raw.find("{"), raw.rfind("}")
        if start != -1 and end > start:
            return json.loads(raw[start:end + 1])
        raise


def validate_ledger(data: dict) -> list:
    if "columns" in data and data["columns"] != EXPECTED_COLUMNS:
        raise ValueError(f"Unexpected columns: {data['columns']}")
    rows = data.get("rows")
    if not isinstance(rows, list) or len(rows) != 26:
        raise ValueError(f"Expected exactly 26 rows, got {len(rows) if isinstance(rows, list) else type(rows)}")

    mean_count = 0
    std_count = 0
    for idx, row in enumerate(rows):
        exp_factor = EXPECTED_FACTORS[idx // 2]
        exp_pop = "Human" if idx % 2 == 0 else "Our Judge"
        if row.get("factor") != exp_factor:
            raise ValueError(f"Row {idx}: expected factor '{exp_factor}', got '{row.get('factor')}'")
        if row.get("population") != exp_pop:
            raise ValueError(f"Row {idx}: expected population '{exp_pop}', got '{row.get('population')}'")

        means = row.get("means")
        stds = row.get("std")
        highlights = row.get("highlight")
        if not (isinstance(means, list) and isinstance(stds, list) and isinstance(highlights, list)):
            raise ValueError(f"Row {idx}: means/std/highlight must be lists")
        if not (len(means) == len(stds) == len(highlights) == 7):
            raise ValueError(f"Row {idx}: expected 7 entries for means/std/highlight")

        for j in range(7):
            m, s, h = means[j], stds[j], highlights[j]
            if not isinstance(m, str) or not MEAN_RE.match(m):
                raise ValueError(f"Row {idx} col {j}: invalid mean literal '{m}'")
            if not isinstance(s, str) or not STD_RE.match(s):
                raise ValueError(f"Row {idx} col {j}: invalid std literal '{s}'")
            if h not in VALID_HIGHLIGHTS:
                raise ValueError(f"Row {idx} col {j}: invalid highlight '{h}'")
            if exp_pop == "Human" and h != "none":
                raise ValueError(f"Row {idx} col {j}: Human row cannot have highlight '{h}'")
            mean_count += 1
            std_count += 1

    if mean_count != 182 or std_count != 182:
        raise ValueError("Total means and std counts must both equal 182")
    return rows


def format_cell(mean_str: str, std_str: str, highlight: str) -> str:
    std_part = f"{{\\fontsize{{7.2pt}}{{8.6pt}}\\selectfont\\textcolor{{stdgray}}{{({std_str})}}}}"
    if highlight == "dark":
        return f"\\cellcolor{{greendark}}\\textbf{{{mean_str}}} {std_part}"
    if highlight == "light":
        return f"\\cellcolor{{greenlight}}\\textbf{{{mean_str}}} {std_part}"
    return f"{mean_str} {std_part}"


def render_tex(rows: list) -> str:
    lines = [
        r"\documentclass{article}",
        r"\usepackage[paperwidth=230mm,paperheight=185mm,margin=2mm]{geometry}",
        r"\usepackage{fontspec}",
        r"\usepackage{type1cm}",
        r"\setmainfont{TeX Gyre Termes}",
        r"\usepackage{booktabs}",
        r"\usepackage{array}",
        r"\usepackage{multirow}",
        r"\usepackage{graphicx}",
        r"\usepackage[table]{xcolor}",
        r"\pagestyle{empty}",
        r"\definecolor{greenlight}{RGB}{204,255,204}",
        r"\definecolor{greendark}{RGB}{178,255,178}",
        r"\definecolor{grpPreserv}{RGB}{34,153,84}",
        r"\definecolor{grpQuality}{RGB}{46,117,211}",
        r"\definecolor{grpFidel}{RGB}{211,63,46}",
        r"\definecolor{stdgray}{RGB}{120,120,120}",
        r"\setlength{\parindent}{0pt}",
        r"\setlength{\tabcolsep}{3.8pt}",
        r"\renewcommand{\arraystretch}{1.20}",
        r"\setlength{\aboverulesep}{1.7pt}",
        r"\setlength{\belowrulesep}{1.9pt}",
        r"\begin{document}",
        r"{\fontsize{14.5pt}{17.2pt}\selectfont",
        r"Table 1: \textbf{Human and our MLLM-as-a-Judge scores for all factors and across all edit types.} "
        r"We report the average score over all image edit types in the last column and over all factors in the last row. "
        r"When the difference between our judge score and human evaluation is closer than 0.5, its background is dark green. "
        r"When the difference is closer than 1.0, its background is light green. "
        r"The gray text is the standard deviation of the scores from which the average is computed.\par}",
        r"\vspace{3.5mm}",
        r"\begin{center}",
        r"{\fontsize{8.5pt}{10.2pt}\selectfont",
        r"\begin{tabular}{@{}c c l c c c c c c c@{}}",
        r"\toprule",
        r" & & & \multicolumn{6}{c}{\textsc{Image Edit Types}} & \\",
        r"\cmidrule(lr){4-9}",
        r" & \textbf{Factor} & & \textbf{Add} & \textbf{Remove} & \textbf{Replace} & "
        r"\textbf{Action} & \textbf{Counting} & \textbf{Relation} & \textbf{All Edits} \\",
        r"\midrule",
    ]

    row_cursor = 0
    for grp_title, grp_color, grp_factors in GROUPS:
        span_rows = len(grp_factors) * 2
        fixup = "-3pt" if span_rows == 6 else "-7pt"
        for f_idx, factor in enumerate(grp_factors):
            human_row = rows[row_cursor]
            judge_row = rows[row_cursor + 1]
            row_cursor += 2

            if f_idx == 0:
                col1 = (
                    f"\\multirow{{{span_rows}}}{{*}}[{fixup}]"
                    f"{{\\rotatebox[origin=c]{{90}}{{\\textcolor{{{grp_color}}}{{\\textbf{{\\textsc{{{grp_title}}}}}}}}}}}"
                )
            else:
                col1 = ""

            col2 = f"\\multirow{{2}}{{*}}{{\\textcolor{{{grp_color}}}{{\\textbf{{{factor}}}}}}}"
            h_cells = " & ".join(
                format_cell(human_row["means"][j], human_row["std"][j], human_row["highlight"][j])
                for j in range(7)
            )
            j_cells = " & ".join(
                format_cell(judge_row["means"][j], judge_row["std"][j], judge_row["highlight"][j])
                for j in range(7)
            )
            lines.append(f"{col1} & {col2} & Human & {h_cells} \\\\")
            lines.append(f" & & Our Judge & {j_cells} \\\\")
            if f_idx < len(grp_factors) - 1:
                lines.append(r"\cmidrule{2-10}")
        lines.append(r"\midrule")

    human_oa = rows[row_cursor]
    judge_oa = rows[row_cursor + 1]
    h_oa_cells = " & ".join(
        format_cell(human_oa["means"][j], human_oa["std"][j], human_oa["highlight"][j])
        for j in range(7)
    )
    j_oa_cells = " & ".join(
        format_cell(judge_oa["means"][j], judge_oa["std"][j], judge_oa["highlight"][j])
        for j in range(7)
    )
    lines.append(f" & \\multirow{{2}}{{*}}{{\\textbf{{Overall Average}}}} & Human & {h_oa_cells} \\\\")
    lines.append(f" & & Our Judge & {j_oa_cells} \\\\")
    lines.extend([
        r"\bottomrule",
        r"\end{tabular}}",
        r"\end{center}",
        r"\end{document}",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Table 1 XeLaTeX from Gemini ledger.")
    parser.add_argument("--ledger", required=True, type=Path, help="Path to input ledger JSON/MD")
    parser.add_argument("--output", required=True, type=Path, help="Path to output .tex file")
    args = parser.parse_args()

    ledger = load_ledger(args.ledger)
    rows = validate_ledger(ledger)
    tex = render_tex(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(tex, encoding="utf-8")


if __name__ == "__main__":
    main()
