# paper-latex-table-skill 使用指南（简体中文）

`paper-latex-table-skill` 是一个本地 Codex Agent Skill，用于把实验结果整理成投稿级别的 LaTeX 表格：支持 `booktabs` 三线表、分组表头（一级）、多数据集对比、消融实验布局，采用确定性的排序与强调规则（最优加粗、次优下划线、并列共享标记、缺失值不排序），并严格保留原始数字字符串与精度。运行时只需 Python 3.10+ 标准库；编译需要本机已安装 TeX 引擎，PDF 预览需要 Poppler（`pdftoppm`）。本地辅助脚本不需要额外模型账号、嵌入服务或联网调用；Codex 本身仍作为宿主代理运行。

中文版指南对应仓库根目录的 `docs/guide.zh-CN.md`，英文说明见 [README](../README.en.md)。

## 一、安装

最简单的方式是在 Codex 对话中直接说：

```text
Install this local paper-latex-table-skill folder into my configured Codex skill directory, preserve existing skills, and verify discovery.
```

也可以在仓库根目录用 PowerShell 手动安装：

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

注意：如果目标目录已存在，脚本会直接报错退出，请先比对差异再更新，不要盲目覆盖。安装完成后确认 Codex 已发现并启用该技能；若技能选择器没有刷新，重启 Codex 即可。下一轮对话中即可用 `$paper-latex-table-skill` 调用。以上路径遵循当前本地 Codex 的默认安装约定，如果你配置过其他技能目录，请相应调整。安装到自己的用户目录通常不需要管理员权限。

## 二、四种典型调用

以下示例都写在发给 Codex 的消息里，务必显式带上 `$paper-latex-table-skill`：

1. **由结果生成表格**

```text
$paper-latex-table-skill 请根据 results/data.json 生成一个带分组表头的多数据集对比表，accuracy 方向为 higher。
```

2. **改进已有表格（不动数据）**

```text
$paper-latex-table-skill 把 draft.tex 改成 booktabs 风格，但任何数值和精度都不允许改变。
```

3. **登记学习示例**

```text
$paper-latex-table-skill 把 my_note.tex 记为学习案例：类型 ablation，9 列，带分组表头，理由是"可复用的分组表头排版模式"。
```

4. **检查溢出与排序**

```text
$paper-latex-table-skill 检查 table.tex 是否有溢出风险，并核对加粗/下划线标记是否符合方向定义。
```

## 三、命令行工具

（以下命令均在仓库根目录执行，构建目录需为全新目录）

建立公共案例索引：

```text
python scripts/index_cases.py
```

由示例 spec 生成表格：

```text
python scripts/generate_table.py docs/examples/benchmark.json build/demo.tex
```

对照 spec 做静态校验：

```text
python scripts/validate_table.py build/demo.tex --spec docs/examples/benchmark.json
```

编译并渲染预览：

```text
python scripts/compile_table.py build/demo.tex --output build/demo-compile
python scripts/inspect_render.py build/demo-compile/table-build.pdf --output build/demo-render
```

按特征检索相似公共案例：

```text
python scripts/retrieve_cases.py --columns 9 --type ablation --feature grouped_headers
```

手动登记学习候选（也可通过 Codex 对话完成）：

```text
python scripts/learning.py --kind case --source path/to/table.tex --reason "Reusable grouped-header pattern" --type ablation --columns 9 --feature grouped_headers
```

运行当前副本的回归测试：

```text
python tests/test_tables.py
```

如需重新生成文档预览图（需已装 TeX、Poppler 与 Pillow，Pillow 仅此一步需要）：

```text
python docs/render_previews.py --build-root build/readme-previews
```

## 四、受控学习机制说明

当你提供真正可复用的示例或报告真实失败时，`learning.py` 会将其记录为待审私有候选，并附带观测到的源码哈希与证据，保存位置默认为 `$CODEX_HOME/skill-state/paper-latex-table-skill`（未设置环境变量时为 `~/.codex/skill-state/paper-latex-table-skill`），位于技能安装目录之外，升级技能不会丢失。

晋升为稳定案例必须经过回归测试、编译/视觉/来源审查、你的明确批准，通过 `rsi.py` 记录审批后，再人工整合。不存在任何后台自动进程、自主改写稳定文件或模型权重训练。

## 五、常见问题

- **编译命令报错找不到 TeX**：`compile_table.py` 依赖本机安装的 TeX 引擎，请先安装 TeX Live/MiKTeX 并确认命令行可用。
- **脚本提示输出目录已存在**：构建命令要求全新目录，换一个新的 build 目录（如 `build/demo2-render`）再执行。
- **技能没有被 Codex 发现**：确认安装到了你配置的技能目录、目录里有 `SKILL.md`；然后重启 Codex 让选择器刷新。
- **校验通过是否意味着排版合格**：静态检查是启发式的，"编译通过"不等于"视觉合格"。投稿前请用目标会议官方模板实际编译检查。
- **数值被改动了**：生成器按显式数据契约保留数值与精度，已有 LaTeX 还需要逐单元格核对；如发现改动请当作真实失败上报登记。
- **发布时注意**：`assets/cases/local/` 与私有学习状态绝不可上传。重新克隆后若索引缺失，先运行 `index_cases.py`；导出用 `python scripts/export_public.py ../dist/paper-latex-table-skill.zip`，只发布解压后的 `paper-latex-table-skill` 子目录。

## 七、按代码/图片复现与字体细节

参见[三种输入流程](../references/input-routes.md)和[布局参考目录](../references/reference-catalog.md)。本地十个案例的原始代码、图片、宏恢复、字体样式分支与实际编译均在 `assets/cases/local/`。可打开其中的 `GALLERY.md` 查看原图/源码保真/字体对齐对比。仅图片输入先用逐格 ledger 保存读取状态；`ambiguous` 和 `illegible` 输出 `[?]`，不猜数字。

```text
python scripts/reproduce_case.py main_table-example2 --output build/omni-source
python scripts/reproduce_case.py main_table-example2 --profile reproduction/image-style/profile.json --output build/omni-typography
python scripts/transcribe_table.py MY_LEDGER.json build/from-image.tex
```

字体对齐包括普通/粗体/斜体/粗斜体、旋转表头、下标、下划线、不确定性和 caption 的字号及字形。Times New Roman 是基于图像的推断；若目标机器缺少此字体，回退字体必须记录为差异，不能宣称完全相同。数值保真与样式对应分开核对。

## 三条 RSI 学习与复用流程

| 模式 | 如何学习 | 如何复用 |
| --- | --- | --- |
| Code + Figure | 原件快照 → 行列/数值/样式冲突核对 → 宏与字体恢复 → 编译对比 | 从已审阅版本提取布局参数；代码版与图片版分开 |
| Figure Only | 逐格转写 → 模糊值 `[?]` → 可编辑 TeX → 字体与粗斜体对照 | 保存图片哈希、转写与恢复经验；未确认值阻止晋升 |
| 设计复用 | 检索相近案例/历史失败 → 分解设计角色 → 基线 + 最多两个组合候选 | 同数据、同最小字号下比较；只保留经核对的参数组合 |

新增 `rsi_episode.py` 记录实际学习过程，`compose_designs.py` 生成并核对设计候选。当前自动组合范围为列间距、行距、分组斜体/粗斜体；复杂表头、配色和线型由 Codex 基于参考与核对记录编写。日常复用不需额外的全局升级批准；稳定规则与脚本晋升单独管理。详见[三模式教程与命令](../references/three-rsi-loops.md)。
