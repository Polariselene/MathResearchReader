# MathResearchReader

源码版本：**v0.2.0**（早期预发布版本）。

面向具备相关本科基础、尚不熟悉论文专题的研一读者，提供教科书级论文精读与证明审查。由 Codex 阅读论文、重组数学逻辑并讲解，将成果保存为可编辑的 Markdown 知识库，再按任务生成中文 PDF。

本项目由工作流指令、参考规则、本地PDF文字缓存与PDF构建工具组成。论文理解依赖 Codex 及其可用工具；缓存只提取文字，`build_pdf.py` 的输入是已经写好的 Markdown，二者都不会自行完成论文理解。

## 解决什么问题

研究论文经常省略背景、计算和证明步骤，关键依赖也可能分散在正文、附录与其他文献中。直接翻译或按原文顺序复述，仍可能让读者不知道一个定义为什么出现、一个公式怎样得到、一个证明依赖哪些条件。

MathResearchReader 将全文对象登记与教学组织分开：先核对原文及依赖，再按由浅入深的数学逻辑讲解。新方法从当前困难和自然尝试引出，变量在使用处交代空间、维数与作用，证明保留必要的代入、计算和中间结论。覆盖清单用于防止遗漏，正文用连贯论述展开。

## 主要功能

| 任务 | 工作内容 | 默认交付 |
|---|---|---|
| 单篇完整精读 | 全文及附录逐项登记；逐项解释数学定义、公式、证明、算法和图表，按依赖安排详略 | Markdown 知识库 + 中文 PDF |
| 指定证明审查 | 检查假设、量词、推导、引用适用性、反例和退化边界，提供核查依据 | Markdown 审计报告；明确要求才导出 PDF |
| 局部追问 | 解释指定定义、公式或证明步骤，补充背景、计算与例子 | 回答；已有知识库保存实质更新 |
| 跨论文比较 | 对照定义、假设、结论和证据，核验直接引用与适用条件 | 比较笔记与来源记录 |
| 继续阅读 | 根据版本、哈希、状态和 checkpoint 恢复，检查变更影响 | 更新原知识库 |
| 从笔记导出 PDF | 按输入顺序或 `book.json` 清单构建中文数学文档，保留构建记录 | PDF + 日志与 manifest |

默认掌握相关专业本科基础，但没学过本文专题；必要的专门概念、标准方案和操作要在正文实际教会，再进入论文创新。适用纯数学、应用数学、密码学、AI 安全和含数学论证的计算机科学论文。直接外部依赖优先核验，深层缺口登记后按需追溯。

PDF 默认不收录阅读说明、整书导航、独立练习与集中解答、额外研究启发；必要说明放在交付消息中。正文保留完整教学算例、反例、证明、图表解释、结论边界和必要来源索引。

对包含多项核心结果、陌生背景与多阶段方法的几十页数学论文，默认按百页级教材规划，逐章补足背景、计算和完整证明，不以二三十页或单次生成作为预算。按每章的新对象、变换、构造和误差持续绘制并解释几何矢量图，不以全书已有若干幅图为止；流程框和原文截图不能代替数学图解。小例子须接回准确通式、变量对应、条件和简化边界。对象覆盖、教学深度、数学正确性与排版分别验收，未讲透就继续补写。页数还受下述硬门槛约束，不能靠空白、字号或重复凑页；专项任务按实际范围展开。

**完整精读有效教学正文至少90页，可见主章不超过10章。** 首次写作前设计体系完整的百页级专题课程，逐单元直接充分讲授，完整内容审阅后才首次导出整书，不先生成短版再反复补到门槛。90页是异常检查底线，不是目标值或各章的页数配额。该要求适用于所有论文，从零读取原文也能执行，不依赖某篇旧产物；不能以原论文短为由自行豁免。封面、目录、索引、空白和重复内容不计有效正文。专项审查、局部解释和单纯导出不套此下限，也不能冒充完整精读。详见[通用交付契约](skills/math-research-reader/references/delivery-contract.md)。

讲解按专题课展开：复杂公式先解释具体对象怎样变化，再给一般证明；陌生的伴随、投影和表示转换要实际教会。先用论文中真正承重的难单元校准，不能以基础小例通过推定整书可读。可读性自查检查正文能否回答具体理解问题，用户暴露的缺口补回正文。规则和自编完整示范见[讲解尺度](skills/math-research-reader/references/teaching-style.md)，它不是自动评分器或学习效果保证。

优先最少的必要主章，同一大问题用连贯段落讲完，默认不使用三级及以下标题；内部知识点或分批文件不自动成为PDF小节。新内容由当前困难、自然尝试及其局限引出，再讲本文实际方法与效果。篇幅不足时在原论证的首次需要处补背景、推导和图例，并重写衔接，不能在书末追加补课章节凑页。

图示随课程蓝图规划并在对应推导处绘制，几十幅或更多均可，只要真实帮助理解；十章不是十图上限。每个核心公式都在使用处交代变量的类型、空间/维数、范围和作用，提供承重中间推导；保持正常字号，长式按数学步骤换行，图中参数与通式对齐。

完整精读按[导师式执行流程](skills/math-research-reader/references/deep-read.md)展开每个必要知识点的先修、操作、推导、证明和图解。写作队列持续推进，checkpoint不等于结束；默认先完成正文再集中导出，不主动把几十页阶段PDF/压缩包作为任务终点。精简入口并按动作加载规则，缓存同版本来源，批量定位并合并取页，共享已写背景，合并同单元检查，只复查变更依赖。运行工具按用法调用，不默认把脚本源码读入上下文。保留全部教学与逐页检查要求，不承诺固定额度或省额比例。

## 安装

安装的是整个 `skills/math-research-reader/` 目录，包含 `references/`、`assets/`、`scripts/` 和 `agents/`，不能只复制 `SKILL.md`。

取得项目文件后，在项目根目录打开 **PowerShell**，执行下面的项目级安装命令：

```powershell
$skillSource = (Resolve-Path -LiteralPath '.\skills\math-research-reader').Path
$skillTarget = Join-Path (Get-Location).Path '.agents\skills\math-research-reader'
if (Test-Path -LiteralPath $skillTarget) {
    throw '目标已存在，请先检查版本和本地修改，不要直接覆盖。'
}
New-Item -ItemType Directory -Path (Split-Path -Parent $skillTarget) -Force | Out-Null
Copy-Item -LiteralPath $skillSource -Destination $skillTarget -Recurse -ErrorAction Stop
Test-Path -LiteralPath (Join-Path $skillTarget 'SKILL.md')
```

最后应输出 `True`。在该项目目录启动或打开 Codex，即可使用此 Skill。仅将源码保留在 `skills/` 下不等于安装。

希望跨项目使用时，可将同一完整目录放到用户级的 `~/.agents/skills/math-research-reader/`。选择一个安装作用域，避免同名多份混淆。Codex 会检测技能变化；未出现时重启 Codex。安装路径与发现行为依据 [OpenAI 官方技能文档](https://learn.chatgpt.com/docs/build-skills)。

以上复制与重复安装保护已在隔离项目目录验证；没有为测试写入真实用户级技能目录，也没有执行 Git 初始化或上传。

## 使用方法与输入示例

安装后，在 Codex 对话中输入 `$math-research-reader` 并给出实际论文路径或附件。以下尖括号内容是占位符，需换成你自己的文件和目录；调用提示是对话内容，不是 PowerShell 命令。

### 单篇完整精读

```text
$math-research-reader

请对这篇论文执行完整教科书级精读。
先梳理全文数学依赖，再按由浅入深的逻辑讲解。
按具备相关本科基础、不了解本文专题的研一水平讲解。
先补专题基础，再拆解核心定义、公式、定理和证明，展开中间计算与贯穿算例，
首次就按完整专题课程充分写作，全书不超过10个主章，绘制并解释充分的数学矢量图。
有效教学正文至少90页，按需要展开至百页或更多，不压缩成摘要，不先做短版再补页。
建立 Markdown 知识库，并生成中文 PDF。
论文：<论文PDF路径>
输出目录：<论文知识库目录>
```

### 专项证明审查

```text
$math-research-reader

请严格审查论文的 Theorem 3.2。
逐项检查假设、量词、推导、引用与边界，给出完整数学依据。
输出 Markdown 审计报告。
论文：<论文PDF路径>
输出目录：<论文知识库目录>
```

编号不存在时应说明检索结果，不会为了完成提示而虚构定理。

### 局部追问与恢复

```text
$math-research-reader
请解释这份知识库中式(7)的推导，回顾变量的空间与维数，展开中间计算。
知识库：<论文知识库目录>

$math-research-reader
继续阅读 <论文知识库目录>，核对源文件和笔记版本，
从 checkpoint 的下一项工作继续，保留我的修改和已有符号约定。
```

优先提供完整 TeX 主文件、includes、宏、参考文献、附录、图表及对应 PDF，也可只提供可读 PDF。URL、DOI 或 arXiv 标识需要宿主能够联网取得全文；扫描件需要可用的 OCR。项目没有捆绑通用论文下载器、OCR 或 PDF 阅读引擎。缺工具或资料时会说明受影响范围，不用摘要代替全文。

## 输出示例

完整精读的目录可组织如下；只创建任务实际需要的文件：

```text
example-paper/
├── paper.json                  # 论文身份、版本、来源与哈希
├── source/                     # 原始资料副本
├── report.md                   # 短篇正文；长篇时为留在 Markdown 的导航
├── chapters/                   # 长篇唯一数学正文，按教学依赖组织
├── book.json                   # 实际进入 PDF 的有序正文清单
├── audit.md                    # 审计发现与依据
├── figures/                    # 原图、自绘矢量图及可编辑源
├── .mrr/
│   ├── objects.json            # 原文对象定位与逐项教学证据
│   ├── dependencies.json      # 依赖与适用条件
│   ├── state.json             # 当前进度、版本、教学欠缺与下一步
│   ├── quality.json           # 检查结果及对应文件哈希
│   └── checkpoints/           # 阶段恢复记录
├── build/                     # 构建日志与 manifest
└── exports/report.zh-CN.pdf
```

专项审查可只输出审计报告及必要索引。发现原论文错误不妨碍完成诚实的审计报告，但不能将相关命题记作验证通过。

审计内容示例（自编数学案例，不属于某篇真实论文）：

```text
待审主张：任意半正定矩阵 C 都有 C^(-1/2) C C^(-1/2) = I。
核查：取 C = diag(4, 0)，普通逆平方根不存在。
若改用伪逆平方根 diag(1/2, 0)，乘积为 diag(1, 0)，不是 I。
结论：全维表述不成立。
修补：增加正定条件，或将结论限定在 C 的值域子空间。
说明：修补后的命题与原主张分开记录。
```

## PDF 依赖与运行示例

需要减少重复PDF文字提取时，可使用随包的本地缓存工具。它额外需要已有Poppler `pdftotext`，
不自动安装；扫描件OCR和公式/图表核对仍由宿主完成。在单篇工作区已保存`source/paper.pdf`后，从项目根目录运行：

```powershell
python .\skills\math-research-reader\scripts\reading_cache.py prepare --root <论文工作区> --source source/paper.pdf
python .\skills\math-research-reader\scripts\reading_cache.py locate --root <论文工作区> --source source/paper.pdf --query "Theorem" --limit 8
python .\skills\math-research-reader\scripts\reading_cache.py locate --root <论文工作区> --source source/paper.pdf --query "Theorem" --query "Lemma" --limit 12
python .\skills\math-research-reader\scripts\reading_cache.py read --root <论文工作区> --source source/paper.pdf --pages 3-6,9
```

尖括号需换成实际路径。prepare只回传小型元数据；未变源和提取器复用缓存，read只回传指定页的完整文字，
不静默截断。页码是从1起的文件页序，必须按实际证明范围取齐。
locate用于定位，仅返回命中页码、行号和限长片段，明确报告省略结果；不能代替完整阅读和原页数学核对。
重复`--query`可一次定位至多16个相关词，合并重叠命中行，逐词报告命中及遗漏；limit限制整批返回行数。
已有页范围可直接read，相邻/重叠范围合并；同会话无变不在每次取页前重复prepare。
可传`prepare --pdftotext <已有工具路径>`。缓存损坏或源改变后重新prepare，原PDF保持只读；
缓存仅保存在单篇`.mrr/source-cache/`，不随项目分发。

安装 Skill 目录不要求 Python；执行附带的 PDF 构建脚本需要：

| 依赖 | 用途 |
|---|---|
| Python 3.10+ | 运行 `build_pdf.py`，脚本仅使用标准库 |
| Pandoc | 解析 Markdown、组装章节并调用排版引擎 |
| XeLaTeX、ctex 与 `kpsewhich` | 中文 LaTeX 排版及依赖检查 |
| Fandol 中文字体、STIX Two Math | 默认中文和数学字体 |
| Poppler `pdfinfo` | 完整精读发布前核实际PDF至少90页；普通导出不要求 |

工具须已安装并在 PATH 中；项目不会自动安装。Pandoc 或 XeLaTeX 不在 PATH 时，可用 `--pandoc`、`--xelatex` 指定本机已有可执行文件；`--cjk-font` 可指定已安装的中文字体。`--check` 只诊断工具与 ctex，字体和版式仍须实际构建检查。

以下为**导出命令的最小验证例**，不会执行论文精读。在项目根目录下新建 `.local-test/readme-demo/`，按下面内容保存两个文件。

`report.md`：

```markdown
# 二维线性响应 {#response}

设 $x\in\mathbb R^2$，观测为 $y=Ax$，其中
$$
A=\begin{pmatrix}1&0\\0&2\end{pmatrix}.
$$
取 $x=(2,3)^\top$，代入得到 $y=(2,6)^\top$。
```

`book.json`：

```json
{
  "schema_version": 1,
  "title": "中文数学导出验证例",
  "lang": "zh-CN",
  "chapters": [
    {"id": "response", "file": "report.md"}
  ]
}
```

在项目根目录执行：

```powershell
$paperRoot = (Resolve-Path -LiteralPath '.\.local-test\readme-demo').Path
python .\skills\math-research-reader\scripts\build_pdf.py --root $paperRoot --check
python .\skills\math-research-reader\scripts\build_pdf.py --root $paperRoot --input report.md --output exports/report.zh-CN.pdf
```

按清单构建，使用另一个输出文件：

```powershell
python .\skills\math-research-reader\scripts\build_pdf.py --root $paperRoot --book book.json --output exports/book.zh-CN.pdf
```

示例中的 `report.md` 是数学正文，因此可收入 PDF；若它是长篇导航，则从 `book.json` 排除。真实长篇将各正文文件按教学顺序列入清单。`--book` 与 `--input` 不能混用；前者会在派生 AST 中处理章节锚点、章间链接和相对图片路径，后者按指定顺序传入 Markdown。

输出已存在时，脚本会拒绝覆盖；检查后增加 `--replace` 才会替换。所有输入与输出均相对 `--root`，原始 `source/` 受保护。构建记录保存在 `build/pdf-*/manifest.json` 和日志中。构建成功仅表示 `built`，视觉状态仍为 `unverified`，完整交付还需检查每页 PDF。

上面的短样例是导出测试，不是完整精读。真实完整精读在`book.json`顶层写入`"task_mode": "deep-read"`，并使用：

```powershell
python .\skills\math-research-reader\scripts\build_pdf.py --root $paperRoot --book book.json --full-read --output exports/full-read.zh-CN.pdf
```

这是整书导出命令，不会自动补写内容；把它用于前述短样例应失败。任一`--full-read`或`task_mode=deep-read`都会启用90个物理页下限，不足或计数失败则不发布、不覆盖已有成稿。`pdfinfo`不在PATH时用`--pdfinfo`指定已有工具。脚本只检查物理页数；有效教学正文是否达到90页、数学与教学是否合格，仍需内容验收。

构建器还继承`.mrr/state.json`或`.mrr/reading-plan.json`中的全文任务标记或90页契约；因此改用`--input`、遗漏标志或更换输出名不能取消原任务门槛。状态损坏或在构建期间改变会停止发布。独立专项短报告使用独立任务工作区，保留原全文任务状态。

结构检查按真实Pandoc标题核至多10个可见主章，而非限制分批文件数；原始TeX章节命令不能用于绕过检查。书名放book元数据，主章用一级Markdown标题，最终目录还需人工核对。state首次记录`first_manuscript_status=planned`，写作为`composing`，整书内容与必要图示审阅后才设`content-reviewed`；前两阶段会在编译前被阻止，不用于反复制作短整书。未存该字段的历史工作区仍受90页与十章门槛约束。

## 验证状态与限制

本地命令验证环境为 Windows、PowerShell、Python 3.14、Pandoc 3.9、TeX Live 2026。其他操作系统的安装命令未验证，因此这里仅给出 PowerShell 版本。命令、运行结果与检查范围见 [README 命令验证记录](evals/results/readme-validation.md)。

在项目根目录可运行现有脚本单元测试，不需要 Pandoc：

```powershell
python -m unittest discover -s tests -v
```

当前结果为 56 项中 55 项通过、1 项因系统不允许创建符号链接而跳过。官方 `quick_validate.py` 的包结构校验通过；这些检查均不认证数学正确性。最新[多轮开销复核](evals/results/mentor-efficiency-validation.md#多轮复核与停止)记录规则去重、按节恢复、保留或撤回的优化及停止依据；[批量定位](evals/results/mentor-efficiency-validation.md#进一步精简与批量定位2026-11-08)、[90页与十章验证](evals/results/first-manuscript-90-validation.md)及[早期门槛](evals/results/full-read-contract-validation.md)保留历史范围。

| 已有验证 | 范围 |
|---|---|
| [真实论文完整精读测试](evals/results/full-read-2609.14379v2.md) | 39 页论文生成 83 页教材，逐页检查；这是最新教学反馈之前的基线 |
| [教学修订局部验证](evals/results/narrative-teaching-validation.md) | 两段改写、数学复算与正文清单组装；尚未重新验收修订后的完整长篇 |
| [研一背景与矢量图解验证](evals/results/first-year-depth-validation.md) | 自编教学单元的表示、完整推导、误差边界和四幅数学矢量图；局部验证不等于整篇精读验收 |
| [讲解可读性修订验证](evals/results/readability-validation.md) | 重新对照四份私人讲义的代表性教学段落，以陌生算符的完整自编单元检验讲解尺度；不是新整书验收 |
| [图解与通式修订验证](evals/results/visual-generalization-validation.md) | 在完整讲解示范中加入四幅矢量图，逐处对应通式，并复算一般列变换恢复；仍为限定单元验证 |
| [不同类型论文的定向测试](evals/results/validation.md) | 纯数学、应用数学、密码学及实证 AI 的限定范围案例，不是四篇全文精读 |

检查来自同一上下文自查，没有独立数学认证或读者学习效果测量。尚未验证百页整书教学效果、复杂 OCR/TeX 输入的全面兼容性和跨平台运行。Lean 仅有按需使用规则，没有捆绑形式化工具链或已完成形式化验证的承诺。作者代码运行与真实实验复现不属于默认精读流程。

## 项目结构与设计来源

```text
skills/math-research-reader/
├── SKILL.md                    # 入口与任务路由
├── agents/openai.yaml          # 展示信息、默认提示、调用策略
├── references/                 # 按需加载的阅读、数学、审计与质量规则
├── assets/pdf-header.tex       # 中文数学版式
├── scripts/build_pdf.py        # 中文PDF构建与完整精读页数门槛
├── scripts/reading_cache.py    # 本地PDF文字缓存与按页读取
└── LICENSE
tests/                          # 构建器行为测试
evals/                          # 测试材料、结果及限制
docs/                           # 产品需求、设计和来源审阅记录
```

从现有项目吸收机制后重新编写工作流，具体采纳与取舍见[六项目机制对照](docs/upstream-review/README.md)、[需求适配表](docs/upstream-review/product-fit.md)、[连续讲解反馈](docs/design/05-teaching-feedback.md)、[研一深度与矢量图反馈](docs/design/06-depth-feedback.md)和[最新可读性反馈](docs/design/07-readable-teaching-feedback.md)。运行时无需安装这些上游项目。

采用 [MIT License](LICENSE)，仅覆盖本项目有权授权的原创部分。上游参考项目、字体和外部论文的范围与许可见
[第三方材料说明](THIRD_PARTY.md)；未知授权材料不随项目发布。私人原始需求、参考讲义、下载论文、
本地知识库和依赖缓存不分发。公开构建记录中的脱敏路径是历史展示值，不是可执行命令。

公开前检查与本轮修复结果见[发布前检查记录](docs/release-readiness.md)。`.gitignore`用于排除本地文件，
直接压缩整个工作目录不会自动遵守它；分发时应采用该记录中的公开文件清单。
