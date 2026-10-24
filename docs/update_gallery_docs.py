import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BEGIN, END = "<!-- GALLERY:BEGIN -->", "<!-- GALLERY:END -->"
LSTART, LEND = "<!-- LOCAL-ONLY:BEGIN -->", "<!-- LOCAL-ONLY:END -->"
FILES = {"README.md": ("zh", ["核心特点"]), "README.en.md": ("en", ["Capabilities", "Core Features"])}

L = {
    "zh": {
        "title": "## 示例对照画廊",
        "pub": "公开示例", "loc": "本地参考（私有）",
        "orig": "原图", "recon": "重建",
        "origtex": "原始 TeX", "recontex": "重建 TeX", "tex": "TeX 源码",
        "review": "审阅记录", "lesson": "要点记录",
        "warn": "以下本地参考含私有图片与源码；公共导出会移除本标记块。",
        "loccounts": "本地共 {loc} 对私有参考，另有 {pub} 对公开示例。",
        "locremaining": "其余本地参考（{count}）",
        "kind": {"structured-synthetic": "结构化合成示例", "advanced-synthetic": "进阶合成示例",
                 "documentation-synthetic": "文档合成示例", "refinement-synthetic": "精修合成示例",
                 "design-reuse-synthetic": "设计复用合成示例"},
        "public-titles": {
            "public-ablation": "组件消融", "public-benchmark": "分组基准比较",
            "public-cross-dataset": "跨数据集比较", "public-decimal": "小数点对齐",
            "public-multi-dataset": "多数据集分组表头", "public-ties-missing": "并列与缺失值",
            "public-uncertainty": "均值与不确定性", "public-wide": "宽基准表",
            "showcase-main": "分组主表展示", "showcase-sensitivity": "并排敏感性面板",
            "showcase-paired": "成对比较与增益", "showcase-ablation": "组件开关消融",
            "showcase-coverage": "覆盖能力矩阵", "basic-benchmark": "基础基准表示例",
            "basic-ablation": "基础消融表示例", "refinement-before": "精修前：完整网格",
            "refinement-after": "精修后：分组横线", "reuse-baseline": "复用基线",
            "reuse-grouped": "分组复用方案", "reuse-compact": "紧凑复用方案",
        },
        "authority-zh": {
            "source-preserving style branch; source/image differences remain recorded":
                "保留源码的样式分支；源码/图片差异仍单独记录",
            "23-column image branch, separate from 25-column code branch":
                "23 列图片分支，与 25 列代码分支分开保存",
            "manual image transcription; inferred macros/fonts":
                "手动逐格转写图片；宏与字体为推断",
        },
        "local-notes": {
            "diffusion-main": "结构：分组扩散基准主表，表下注释。可见匹配点：预训练双层表头、跨正文的语义竖线、灰色分组带和粗体 roman JiT 名称。原图中 latent 标签为常规斜体，pixel 标签为粗斜体；caption 三行，表格下方无底线。",
            "representation-ablation": "结构：共享说明加四个并排消融面板。可见匹配点：灰色默认行、局部加粗值和各面板短说明；原图共享 caption 五行，面板表格窄且居中、表体小于 caption。",
            "paired-generation": "结构：按模型配对的 baseline/RCG 增益表。可见匹配点：多行方法标识、细分隔线、改进值粗体及括号内绿色增益；原图表格居中紧凑，caption 在表上方。",
            "guidance-comparison": "结构：无/有 guidance 的双层指标表头。可见匹配点：类别人群整行灰字、块边界竖线和斜体组名；灰色表示人群，不表示排名。本例作为布局控制，不需无证据的风格改动。",
            "meanflow-algorithm": "结构：带标题、注释和语法着色的算法伪代码。可见匹配点：窄横线、青色注释、洋红关键字/可调用项；函数名不加下划线，等号为黑色，Note 正文为小号常规衬线字。",
            "multimodal-main": "结构：视频/图像指标分块的宽主表。可见匹配点：65° 旋转表头、分组底色、浅绿目标行及独立的细分隔线；缩短表头应匹配字号与间距，不改变角度。",
            "data-mixture": "结构：图像与视频指标分块的数据配比表。可见匹配点：旋转表头、斜体类别带、竖向块边界和浅绿 Full Mix 行；Full Mix 的标签与视频单元格加粗，图像单元格保持常规；baseline 数字字形倾斜度不确定，不据此设定统一规则。",
        },
        "counts": "公开示例统计：公共索引共 {pub} 对；本节直接显示 {shown} 对。",
        "above": "另有 {skip} 对公开示例已在上方“表格示例”小节直接显示，此处不重复：{ids}",
    },
    "en": {
        "title": "## Paired example gallery",
        "pub": "Public pairs", "loc": "Local reference (private)",
        "orig": "Original figure", "recon": "Reconstruction",
        "origtex": "Original TeX", "recontex": "Reconstruction TeX", "tex": "TeX source",
        "review": "Review", "lesson": "Lesson",
        "warn": "Local reference images and source links below are private; public export strips this marked block.",
        "loccounts": "There are {loc} private local pairs, separate from {pub} public examples.",
        "locremaining": "Other local references ({count})",
        "kind": {"structured-synthetic": "structured synthetic", "advanced-synthetic": "advanced synthetic",
                 "documentation-synthetic": "documentation synthetic", "refinement-synthetic": "refinement synthetic",
                 "design-reuse-synthetic": "design-reuse synthetic"},
        "public-titles": {
            "public-ablation": "Component ablation", "public-benchmark": "Grouped benchmark",
            "public-cross-dataset": "Cross-dataset comparison", "public-decimal": "Decimal alignment",
            "public-multi-dataset": "Grouped multi-dataset table", "public-ties-missing": "Ties and missing values",
            "public-uncertainty": "Mean and uncertainty", "public-wide": "Wide benchmark",
            "showcase-main": "Grouped comparison showcase", "showcase-sensitivity": "Aligned sensitivity panels",
            "showcase-paired": "Paired comparisons and gains", "showcase-ablation": "Component-switch ablation",
            "showcase-coverage": "Coverage matrix", "basic-benchmark": "Basic benchmark example",
            "basic-ablation": "Basic ablation example", "refinement-before": "Before refinement: full grid",
            "refinement-after": "After refinement: sparse rules", "reuse-baseline": "Reuse baseline",
            "reuse-grouped": "Grouped reuse variant", "reuse-compact": "Compact reuse variant",
        },
        "counts": "Public count: {pub} pairs in the public index; {shown} displayed directly in this section.",
        "above": "The remaining {skip} public pairs are already displayed directly in the sections above: {ids}",
        "local-notes": {
            "diffusion-main": "Role: grouped diffusion benchmark with a caption below. Visible matches: two-tier pre-training header, semantic vertical boundaries through the body, gray bands and bold roman JiT names. In the source, the latent label is italic (not bold) and the pixel label bold italic; the caption is three lines and there is no bottom rule.",
            "representation-ablation": "Role: one shared explanation above four side-by-side ablation panels. Visible matches: gray default rows, selective bold values and short panel notes; the source caption spans five lines and the panel tables are narrow/centered, with smaller body type than caption type.",
            "paired-generation": "Role: paired baseline/RCG gain comparison. Visible matches: multirow method labels, thin pair separators, bold improved values and green signed gains in parentheses; the source table is compact and centered with its caption above.",
            "guidance-comparison": "Role: two-tier metric comparison with and without guidance. Visible matches: gray text for the class-conditional population, block-boundary rules and italic group labels. Gray encodes population, not rank; keep this case as a control unless a mismatch is demonstrated.",
            "meanflow-algorithm": "Role: pseudocode listing with title, note and syntax colors. Visible matches: narrow rules, teal comments and magenta keywords/callables. Function names are not underlined, equals signs are black, and the Note is small plain serif text.",
            "multimodal-main": "Role: wide main table split into video and image metrics. Visible matches: 65-degree rotated headers, category bands, pale-green target rows and separate thin block rules; shorten the header through matched type size/spacing, not a new angle.",
            "data-mixture": "Role: image/video metric blocks for a data-mixture comparison. Visible matches: rotated headers, italic category bands, vertical block boundaries and a pale-green Full Mix row. The Full Mix label and video cells are bold while image cells remain regular; baseline value slant is uncertain, so do not encode a universal roman/italic rule.",
        },
    },
}


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)["examples"]


def strip_region(text):
    return re.sub(re.escape(BEGIN) + r"\n.*?" + re.escape(END) + r"\n*", "", text, flags=re.S)


def is_displayed(text, figure):
    return re.search(r"!\[[^\]]*\]\(" + re.escape(figure) + r"\)", text) is not None


def picture(p, lab):
    original, rebuilt = p.get("original_figure"), p.get("figure")
    if original and rebuilt:
        return ("| %s | %s |\n| --- | --- |\n| ![%s](%s) | ![%s](%s) |"
                % (lab["orig"], lab["recon"], lab["orig"], original, lab["recon"], rebuilt))
    figure = original or rebuilt
    return "![%s](%s)" % (lab["recon"] if rebuilt else lab["orig"], figure)


def entry_links(p, lab):
    out = []
    for key, label in (("original_tex", "origtex"), ("tex", "recontex"), ("review", "review"), ("lesson", "lesson")):
        if p.get(key):
            out.append("[%s](%s)" % (lab[label], p[key]))
    return " · ".join(out)


def local_block(p, lab, tr=None):
    parts = ["### " + p["id"], picture(p, lab)]
    links = entry_links(p, lab)
    if links:
        parts.append(links)
    if p.get("authority") and p.get("kind") != "image-only-reference":
        parts.append(tr.get(p["authority"], p["authority"]) if tr else p["authority"])
    note = lab.get("local-notes", {}).get(p["id"])
    if note:
        parts.append(note)
    return "\n\n".join(parts)


def public_block(p, lab):
    title = lab["public-titles"].get(p["id"], p["id"])
    return "\n\n".join([
        "### %s (%s)" % (title, lab["kind"].get(p["kind"], p["kind"])),
        "![%s](%s)" % (title, p["figure"]),
        "[%s](%s)" % (lab["tex"], p["tex"]),
    ])


def build(public, fresh, skip, local, lang):
    lab = L[lang]
    featured_ids = ["diffusion-main", "representation-ablation", "paired-generation",
                    "guidance-comparison", "meanflow-algorithm", "multimodal-main", "data-mixture"]
    featured = [next(p for p in local if p["id"] == case_id) for case_id in featured_ids if any(p["id"] == case_id for p in local)]
    featured_set = {p["id"] for p in featured}
    remaining = [p for p in local if p["id"] not in featured_set]
    head = [BEGIN, lab["title"],
            lab["counts"].format(pub=len(public), shown=len(fresh))]
    if skip:
        head.append(lab["above"].format(skip=len(skip), ids=", ".join(p["id"] for p in skip)))
    if featured:
        head += [LSTART, lab["warn"], "### %s (%d)" % (lab["loc"], len(local)),
                 lab["loccounts"].format(loc=len(local), pub=len(public))]
        head += [local_block(p, lab, lab.get("authority-zh")) for p in featured]
        head.append(LEND)
    head.append("### %s (%d)" % (lab["pub"], len(fresh)))
    head += [public_block(p, lab) for p in fresh]
    if remaining:
        head += [LSTART, lab["warn"], "### %s" % lab["locremaining"].format(count=len(remaining))]
        head += [local_block(p, lab, lab.get("authority-zh")) for p in remaining]
        head.append(LEND)
    head.append(END)
    return "\n\n".join(head) + "\n\n"


def insert(text, region, headings):
    m = re.search(r"^## (%s)[ \t\r]*$" % "|".join(re.escape(h) for h in headings), text, re.M)
    if not m:
        raise SystemExit("gallery insertion heading not found")
    return text[:m.start()] + region + text[m.start():]


def main():
    public = load(ROOT / "docs" / "gallery-public.json")
    local_path = ROOT / "assets" / "cases" / "local" / "gallery-pairs.json"
    local = load(local_path) if local_path.exists() else []
    for name, (lang, headings) in FILES.items():
        path = ROOT / name
        text = strip_region(path.read_text(encoding="utf-8"))
        skip = [p for p in public if is_displayed(text, p["figure"])]
        fresh = [p for p in public if not is_displayed(text, p["figure"])]
        path.write_text(insert(text, build(public, fresh, skip, local, lang), headings), encoding="utf-8")
        print("updated", name, "public shown", len(fresh), "skipped", len(skip), "local", len(local))


if __name__ == "__main__":
    main()
