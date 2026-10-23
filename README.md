# Paper LaTeX Table Skill

**让实验结果拥有论文主表的表达力。**

面向 Codex 的科研 LaTeX 表格 Skill：从数据生成、已有 TeX 精修，到截图重建与参考设计复用。用分层表头、分组字体、克制配色和有依据的数值强调，建立清晰的阅读层次，同时保留原始数据与比较语义。

[English](README.en.md) · [中文教程](docs/guide.zh-CN.md) · [Skill 入口](SKILL.md) · [参考布局](references/reference-catalog.md)

**数据 → 表格 · 代码 + 图片 → 保真重建 · 图片 → 可编辑 TeX · 好案例 → 可复用的设计经验**

## 看见表格的表达力

以下三张表均由随仓库提供的 **可编辑 LaTeX 源码实际编译**。模型、数据集、数值和覆盖关系均为原创合成示例，不是真实实验结果。复杂布局由 Codex 辅助编写，不代表 JSON 生成器能一键生成任意表格。

### 01 / 综合主表：密集，但不拥挤

![综合主表：分层表头、模型家族分区、淡紫方法行及最优次优强调](docs/images/showcase-main.png)

**三个基准 × 两种设置**，先看清比较结构，再读数值。粗斜体区分模型家族，淡紫色定位重点方法；最优/次优在全部可比行中计算，延迟按更低更好独立强调。

[可编辑 TeX](docs/examples/showcase/showcase-main.tex) · [合成数据](docs/examples/showcase/data.json)

### 02 / 组件消融：把“为什么有效”排清楚

![组件消融：开关、小号灰色标准差、基线增益与完整方法强调](docs/images/showcase-ablation.png)

**组件开关 → 指标变化 → 平均增益**，一行读完。标准差用小号灰字退后一级；增益明确比较基线与百分点单位，均值排名不被解释为统计显著性。

[可编辑 TeX](docs/examples/showcase/showcase-ablation.tex) · [合成数据](docs/examples/showcase/data.json)

### 03 / 能力矩阵：覆盖与空缺，都可见

![能力矩阵：感知、时间、定义三组表头及三态覆盖符号](docs/images/showcase-coverage.png)

**实心 / 半实心 / 空心** 分别表达完整、部分与未覆盖，附带规模、评估单位和图例。符号形状承载语义，颜色只是辅助。

[可编辑 TeX](docs/examples/showcase/showcase-coverage.tex) · [重建预览脚本](docs/render_showcase.py)

## 不止是换一个 booktabs 样式

| 特点 | 实际工作方式 |
| --- | --- |
| **参考设计复用** | 检索相近布局，拆解表头、分组、字体与强调角色，再适配自己的数据；原始参考单独保存。 |
| **数据保真精修** | 核对单元格身份、数值字符串、精度、不确定性和引用；代码与图片冲突时保留独立版本。 |
| **有依据的强调** | 按指标方向、比较范围和并列规则标记最优/次优，不把所有参数列都当成绩。 |
| **可编辑重建** | 恢复宏与依赖；图片先逐格转写，看不清的值标为 [?]，不猜数字。 |
| **可追溯的学习** | 保存案例与失败修复的私有待审记录，供后续检索；稳定规则更新另经回归与审核。 |
| **分层验证** | 数据核对、静态检查、实际编译和渲染审阅分别报告，保留源码与证据。 |

<details>
<summary>更多示例：同数据精修与基础生成</summary>

![同一组合成数据从网格表到 booktabs 的排版对比](docs/images/refinement.png)

[优化前](docs/examples/refinement-before.tex) · [优化后](docs/examples/refinement-after.tex)。原始单元格内容保持不变。

[基础主表规格](docs/examples/benchmark.json) · [基础消融规格](docs/examples/ablation.json)

</details>

## 三种输入方式

| 输入 | 工作方式 | 交付 |
| --- | --- | --- |
| 代码 + 图片 | 对照代码与原图，恢复宏和依赖，检查行列、数值、字体、粗斜体及强调标记 | TeX、依赖说明、冲突记录、实际编译与原图对比 |
| 仅代码 / 数据 | 保留原始字符串与精度，按目标版心生成或精修 | 可编辑 TeX、数据核对记录、PDF/PNG |
| 仅图片 | 先建立逐格转写记录；模糊字符保留 `[?]`，再重建表格 | TeX、图片哈希、转写状态及待确认清单 |

代码与图片可能来自不同版本。默认保留代码数据；如果需要按图复现，建立独立版本，不用修改数字来掩盖冲突。辅助脚本不是 OCR，也不能凭图片确认实验真实性。

## 已学习的布局

本地完整版包含 **10 个用户提供的代码 + 图片案例**，原始 23 个文件保留哈希；每案提供恢复宏、源码保真编译及原图对比。另有 **8 个公开合成案例**供生成与回归使用。

| 布局 | 主要设计 | 关注细节 |
| --- | --- | --- |
| Few-shot 组件消融 | 9 列、3 个组件、两种 backbone、成对 shot 列 | 均值 ± 标准差、粗体最优行、斜体分组、增益箭头 |
| 多数据集组件消融 | 11 列、Global/Local 分组、淡色区块 | 粗体/下划线作用域、紫色完整方法、细字号注释 |
| 数据集能力矩阵 | 14 列、分层表头、覆盖圆点 | 实心/半实心/空心、图例与字号比例 |
| 空间能力主表 | 12 列、旋转列名、3 类指标 | Rank 原值、分组斜体、深浅灰强调 |
| Omni 模型主表 | 15 列、类别与难度分组 | 分组粗斜体、品牌图标、参数字符串 |
| 多领域工具主表 | 13 列、能力图标、标准差、双 Δ 列 | 小号灰色不确定性、下标、平均行 |
| Zero-shot 综合表 | 25 列源码 / 23 列图片 | 旋转彩色表头、平均列、版本冲突隔离 |
| 编码器比较 | 8 列、中心化/全局/局部分组 | 灰色基线、粗体正文、不同增益基准 |
| 联邦数据划分 | 6 列、Local/Global 成对比较 | 多行 setting、希腊字母、百分点变化 |
| 模型资源目录 | 5 列、按家族分组、长 URL | 粗斜体家族名、正文粗体、可编辑链接 |

详细经验见[参考目录](references/reference-catalog.md)。原始参考材料的再分发权尚未确认，因此本地原图、复现图及逐案审核放在 `assets/cases/local/GALLERY.md`；公开 GitHub 包不包含该私有目录。本地画廊展示的是实际重建与残差，不宣称像素完全一致。

## 安装到 Codex

在 Codex 中打开本仓库，发送：

```text
请将当前 paper-latex-table-skill 安装到我已配置的 Codex skills 目录。
如已存在，请先比较和备份，保留已有学习记录，安装后验证技能可发现。
```

手动安装（Windows PowerShell；从包含 SKILL.md 的仓库根目录执行）：

```powershell
$skillSource = (Resolve-Path .).Path
if (-not (Test-Path (Join-Path $skillSource 'SKILL.md'))) { throw '请在技能仓库根目录执行' }
$skillHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$skillTarget = Join-Path $skillHome 'skills/paper-latex-table-skill'
if (Test-Path $skillTarget) { throw '目标已存在，请先比较并备份再更新' }
New-Item -ItemType Directory -Force -Path $skillTarget | Out-Null
Get-ChildItem -LiteralPath $skillSource -Force |
    Where-Object { $_.Name -notin @('.git', '.local', 'build', 'state', 'skill-state', '__pycache__') } |
    ForEach-Object { Copy-Item -LiteralPath $_.FullName -Destination $skillTarget -Recurse }
```

安装后检查 Codex 的技能列表。若列表未刷新，重启客户端后在新一轮对话中输入 `$paper-latex-table-skill`。无需启用 OpenCode；它仅用于开发评审。

## 使用示例

```text
$paper-latex-table-skill 用 results.json 生成双栏论文通栏表；accuracy 越高越好，latency 越低越好。
$paper-latex-table-skill 按 figure.png 复现 table.tex，对齐字体、字号、粗体、斜体、下划线与间距，保留全部数值。
$paper-latex-table-skill 只有这张截图，请先逐格转写，再重建可编辑 LaTeX；看不清的值不要猜。
$paper-latex-table-skill 学习这份新表格，保存源代码/图片、设计参数与核对记录，作为待审阅参考。
```

命令行（输出应使用新文件/目录）：

```text
python scripts/index_cases.py
python scripts/generate_table.py docs/examples/benchmark.json build/demo.tex
python scripts/validate_table.py build/demo.tex --spec docs/examples/benchmark.json
python scripts/compile_table.py build/demo.tex --output build/demo-compile
python scripts/inspect_render.py build/demo-compile/table-build.pdf --output build/demo-render
python scripts/retrieve_cases.py --columns 9 --type ablation --feature grouped_headers
```

本地参考复现与图片转写的命令、格式和依赖见[输入流程](references/input-routes.md)。JSON 生成器支持一层分组表头；复杂 multirow、深层表头和专用宏由代理结合核对记录编写。

## 持续学习

新案例或真实修复经验会保存为私有 pending 记录，默认位于 `$CODEX_HOME/skill-state/paper-latex-table-skill`，不随技能更新覆盖。后续相关任务可以检索这些记录，复用经过核对的布局与修复方法。

稳定规则、脚本和案例晋升需经过回归、来源检查、实际渲染审阅及明确批准。这里的“自我进化”是可追溯的经验积累与受控改进，不是模型权重训练或后台自行改写。见[学习流程](references/continuous-learning.md)和[改进政策](rsi/improvement-policy.md)。

## 依赖与验证

- Python 3.10+；核心生成、校验、转写脚本仅用标准库。
- TeX 引擎与所需宏包；本地恢复案例使用 XeLaTeX、fontspec、TikZ 等。
- Poppler `pdftoppm` 用于 PDF 转 PNG；Pillow 为对比图/文档预览的可选依赖。
- 字体对齐分支优先使用本机 Times New Roman，缺少时回退 TeX Gyre Termes；截图无法提供确切字体元数据，推断和替代会写入记录。

数据核对、编译成功、视觉对应与投稿尺寸可读性分别报告。编译成功不等于视觉通过，也不代表符合任一会议官方模板。

## 公开打包

```text
python scripts/export_public.py .local/releases/paper-latex-table-skill-1.2.0.zip
```

导出排除私有参考、构建日志、学习状态、Git 历史与内部备份，保留公开示例、README 图片及可运行工具。项目许可证状态见 [LICENSE](LICENSE)；第三方参考不会自动继承项目许可。

README 目录与原图/复现画廊的组织参考了 [Trae1ounG/paper-plot-skills](https://github.com/Trae1ounG/paper-plot-skills)。开发中使用本机 OpenCode API 完成了一份文档与流程评审；运行本技能不依赖它。

## 三条 RSI 学习与复用流程

| 模式 | 如何学习 | 如何复用 |
| --- | --- | --- |
| Code + Figure | 原件快照 → 行列/数值/样式冲突核对 → 宏与字体恢复 → 编译对比 | 从已审阅版本提取布局参数；代码版与图片版分开 |
| Figure Only | 逐格转写 → 模糊值 `[?]` → 可编辑 TeX → 字体与粗斜体对照 | 保存图片哈希、转写与恢复经验；未确认值阻止晋升 |
| 设计复用 | 检索相近案例/历史失败 → 分解设计角色 → 基线 + 最多两个组合候选 | 同数据、同最小字号下比较；只保留经核对的参数组合 |

新增 `rsi_episode.py` 记录实际学习过程，`compose_designs.py` 生成并核对设计候选。当前自动组合范围为列间距、行距、分组斜体/粗斜体；复杂表头、配色和线型由 Codex 基于参考与核对记录编写。日常复用不需额外的全局升级批准；稳定规则与脚本晋升单独管理。详见[三模式教程与命令](references/three-rsi-loops.md)。

### 设计复用：一份数据，三种候选

![同一组合成数据与 10pt 正文字号的三种实际编译候选](docs/images/design-reuse.png)

[Baseline TeX](docs/examples/design-reuse/baseline.tex) · [Grouped variant](docs/examples/design-reuse/grouped-readable.tex) · [Compact variant](docs/examples/design-reuse/compact-readable.tex). 仅使用合成数据；候选用于人工比较，不代表自动审美排名。
