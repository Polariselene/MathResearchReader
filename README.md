# MathResearchReader

面向数学研究生的教科书级论文精读与证明审查 Skill。由 Codex 阅读论文、重组数学逻辑并讲解，将成果保存为可编辑的 Markdown 知识库，再按任务生成中文 PDF。

本项目由工作流指令、参考规则和一个 PDF 构建脚本组成。论文理解依赖 Codex 及其可用工具；`build_pdf.py` 的输入是已经写好的 Markdown，不会自行读取论文并完成精读。

## 解决什么问题

研究论文经常省略背景、计算和证明步骤，关键依赖也可能分散在正文、附录与其他文献中。直接翻译或按原文顺序复述，仍可能让读者不知道一个定义为什么出现、一个公式怎样得到、一个证明依赖哪些条件。

MathResearchReader 将全文对象登记与教学组织分开：先核对原文及依赖，再按由浅入深的数学逻辑讲解。新方法从当前困难和自然尝试引出，变量在使用处交代空间、维数与作用，证明保留必要的代入、计算和中间结论。覆盖清单用于防止遗漏，正文用连贯论述展开。

## 主要功能

| 任务 | 工作内容 | 默认交付 |
|---|---|---|
| 单篇完整精读 | 全文及附录逐项登记；核心定义、公式、证明、算法和图表完整展开，其他内容说明作用与取舍 | Markdown 知识库 + 中文 PDF |
| 指定证明审查 | 检查假设、量词、推导、引用适用性、反例和退化边界，提供核查依据 | Markdown 审计报告；明确要求才导出 PDF |
| 局部追问 | 解释指定定义、公式或证明步骤，补充背景、计算与例子 | 回答；已有知识库保存实质更新 |
| 跨论文比较 | 对照定义、假设、结论和证据，核验直接引用与适用条件 | 比较笔记与来源记录 |
| 继续阅读 | 根据版本、哈希、状态和 checkpoint 恢复，检查变更影响 | 更新原知识库 |
| 从笔记导出 PDF | 按输入顺序或 `book.json` 清单构建中文数学文档，保留构建记录 | PDF + 日志与 manifest |

默认以数学研究生基础为起点，补齐子领域背景。适用纯数学、应用数学、密码学、AI 安全和含数学论证的计算机科学论文。直接外部依赖优先核验，深层缺口登记后按需追溯。

PDF 默认不收录阅读说明、整书导航、独立练习与集中解答、额外研究启发；必要说明放在交付消息中。正文的完整教学算例、反例、证明、图表解释、结论边界和必要来源索引保留。长篇按实际理解需要展开，不设页数上限，也不保证每篇都达到百页。

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
讲清核心定义、公式、定理和证明，保留必要计算及教学算例。
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
├── figures/                    # 有来源的原图与教学图
├── .mrr/
│   ├── objects.json            # 原文对象到正文的定位
│   ├── dependencies.json      # 依赖与适用条件
│   ├── state.json             # 当前进度、版本与下一步
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

安装 Skill 目录不要求 Python；执行附带的 PDF 构建脚本需要：

| 依赖 | 用途 |
|---|---|
| Python 3.10+ | 运行 `build_pdf.py`，脚本仅使用标准库 |
| Pandoc | 解析 Markdown、组装章节并调用排版引擎 |
| XeLaTeX、ctex 与 `kpsewhich` | 中文 LaTeX 排版及依赖检查 |
| Fandol 中文字体、STIX Two Math | 默认中文和数学字体 |

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

## 验证状态与限制

本地命令验证环境为 Windows、PowerShell、Python 3.14、Pandoc 3.9、TeX Live 2026。其他操作系统的安装命令未验证，因此这里仅给出 PowerShell 版本。命令、运行结果与检查范围见 [README 命令验证记录](evals/results/readme-validation.md)。

在项目根目录可运行现有脚本单元测试，不需要 Pandoc：

```powershell
python -m unittest discover -s tests -v
```

当前结果为 22 项中 21 项通过、1 项因系统不允许创建符号链接而跳过。官方 `quick_validate.py` 的包结构校验通过；这些检查均不认证数学正确性。

| 已有验证 | 范围 |
|---|---|
| [真实论文完整精读测试](evals/results/full-read-2609.14379v2.md) | 39 页论文生成 83 页教材，逐页检查；这是最新教学反馈之前的基线 |
| [教学修订局部验证](evals/results/narrative-teaching-validation.md) | 两段改写、数学复算与正文清单组装；尚未重新验收修订后的完整长篇 |
| [不同类型论文的定向测试](evals/results/validation.md) | 纯数学、应用数学、密码学及实证 AI 的限定范围案例，不是四篇全文精读 |

检查来自同一上下文自查，没有独立数学认证或读者学习效果测量。尚未验证百页整书教学效果、复杂 OCR/TeX 输入的全面兼容性和跨平台运行。Lean 仅有按需使用规则，没有捆绑形式化工具链或已完成形式化验证的承诺。作者代码运行与真实实验复现不属于默认精读流程。

## 项目结构与设计来源

```text
skills/math-research-reader/
├── SKILL.md                    # 入口与任务路由
├── agents/openai.yaml          # 展示信息、默认提示、调用策略
├── references/                 # 按需加载的阅读、数学、审计与质量规则
├── assets/pdf-header.tex       # 中文数学版式
├── scripts/build_pdf.py        # 唯一随包运行脚本
└── LICENSE
tests/                          # 构建器行为测试
evals/                          # 测试材料、结果及限制
docs/                           # 产品需求、设计和来源审阅记录
```

从现有项目吸收机制后重新编写工作流，具体采纳与取舍见[六项目机制对照](docs/upstream-review/README.md)、[需求适配表](docs/upstream-review/product-fit.md)和[最新教学反馈对照](docs/design/05-teaching-feedback.md)。运行时无需安装这些上游项目。

采用 [MIT License](LICENSE)，仅覆盖本项目有权授权的原创部分。上游参考项目、字体和外部论文的范围与许可见
[第三方材料说明](THIRD_PARTY.md)；未知授权材料不随项目发布。私人原始需求、参考讲义、下载论文、
本地知识库和依赖缓存不分发。公开构建记录中的脱敏路径是历史展示值，不是可执行命令。

公开前检查与本轮修复结果见[发布前检查记录](docs/release-readiness.md)。`.gitignore`用于排除本地文件，
直接压缩整个工作目录不会自动遵守它；分发时应采用该记录中的公开文件清单。
