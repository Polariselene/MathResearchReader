# 开发架构与 Codex 使用

## 1. 三层边界

开源仓库负责开发、测试和分发；Skill 安装包负责可执行工作流；用户论文工作区负责来源、知识、证据与进度。三者分离，升级 Skill 不覆盖论文笔记，论文数据不默认进入开源仓库。

采用一个对外主 Skill，内部按需读取 references。内部模块不是必须安装的一组独立 Skill，也不意味着需要多个 agent。当前设计无需额外服务、API 密钥或专用 MCP；联网检索使用宿主可用能力，不写死某个宿主的工具名。

## 2. 建议的开源仓库结构

以下是逐步开发的目标结构，不要求第一天创建所有空目录。

```text
MathResearchReader/
├── README.md                         # 开源项目定位、安装、使用、能力限制
├── LICENSE                           # 许可证，待用户选择
├── CONTRIBUTING.md                   # 贡献与数学审查标准
├── THIRD_PARTY_NOTICES.md             # 仅实际复用内容的声明
├── pyproject.toml                    # Python 依赖与可选功能组
├── .gitignore                        # 排除用户论文、构建缓存、私人配置
├── skills/
│   └── math-research-reader/          # 可独立安装的完整目录
│       ├── SKILL.md                  # 入口、路由、硬约束、完成条件
│       ├── agents/
│       │   └── openai.yaml           # UI 元数据、默认提示与调用策略
│       ├── references/
│       │   ├── evidence-policy.md    # 来源分离、定位、版本、引用核验
│       │   ├── workflows/
│       │   │   ├── deep-read.md      # 八阶段与阶段交付
│       │   │   ├── proof-audit.md    # 专项审查与结论等级
│       │   │   ├── explain.md        # 局部解释、反复推导、多轮追问
│       │   │   ├── resume.md         # 断点恢复与失效检查
│       │   │   └── compare.md        # 定义/假设/约定对照与文献关系
│       │   ├── mathematics/
│       │   │   ├── definitions-and-notation.md
│       │   │   ├── equation-reconstruction.md
│       │   │   ├── theorem-and-proof.md
│       │   │   └── counterexamples.md
│       │   ├── profiles/
│       │   │   ├── pure-math.md
│       │   │   ├── applied-security.md
│       │   │   └── empirical-cs-ai.md
│       │   ├── knowledge-base.md     # 文件所有权、编号、链接、内容源
│       │   ├── visualization.md      # 图示选型、数学检查、来源
│       │   ├── pdf-publishing.md     # 排版、构建、逐页视觉检查
│       │   ├── quality-gates.md      # 完成判据与失败报告
│       │   └── formal-verification.md # 可选 Lean，后续按需实现
│       ├── scripts/
│       │   ├── mrr.py               # 唯一薄 CLI；下面的子命令入口
│       │   └── mrr/                 # 随 Skill 一起分发的 Python 实现
│       │       ├── doctor.py        # 环境、字体、工具、版本检查
│       │       ├── sources.py       # 文件检查、哈希、安全解包与来源登记
│       │       ├── extract_pdf.py   # 逐页文本、坐标、裁图与渲染
│       │       ├── scan_tex.py      # 主文件/includes/宏/label 扫描
│       │       ├── index.py         # 统一对象索引，模型复核状态
│       │       ├── state.py         # checkpoint、恢复、失效传播
│       │       ├── validate.py      # 覆盖率、证据链接与结构一致性
│       │       └── publish.py       # 合并 Markdown、图转换、PDF、QA
│       ├── schemas/                 # 本项目约定，不是 Codex 特殊目录
│       │   ├── config.schema.json
│       │   ├── paper.schema.json
│       │   ├── object-index.schema.json
│       │   ├── audit.schema.json
│       │   ├── state.schema.json
│       │   └── quality.schema.json
│       └── assets/
│           ├── templates/
│           │   ├── report-outline.md
│           │   ├── theorem-card.md
│           │   ├── equation-card.md
│           │   └── audit-finding.md
│           ├── pandoc/
│           │   ├── defaults.yaml
│           │   ├── zh-math.tex
│           │   └── filters/          # 仅实际需要的链接/交叉引用处理
│           └── config-defaults.yaml
├── tests/                            # 开发测试，不随最小 Skill 包分发
│   ├── unit/                        # 脚本真实行为测试
│   ├── integration/                 # 提取/恢复/构建链
│   └── fixtures/                    # 自编或许可允许的小样例
├── evals/
│   ├── cases.yaml                   # 四类论文与带缺陷证明的案例清单
│   ├── rubric.md                    # A/B/C/D 验收，数学审查依据
│   └── results/                     # 有版本的测试结果与限制
├── examples/
│   └── prompts.md                   # 精读、审查、解释、恢复、比较、导出
└── docs/
    ├── design/                      # 本次设计文档
    ├── installation.md              # Windows 优先，其他环境说明
    └── provenance.md                # 上游链接、审阅范围、实际借鉴记录
```

README/贡献说明属于用户明确希望开源所需的仓库文档，不重复塞入 Skill 执行上下文。只安装 `skills/math-research-reader/` 就必须具备所需脚本、schema、模板和 references；不能依赖仓库根目录未随安装分发的 Python 源码。可选功能缺失应有明确提示。

## 3. 主 SKILL.md 的职责与大小

建议最初控制在约 150–250 行以内，作为维护目标而非 Codex 限制。只保留：能力边界；任务和 Profile 路由；输入及来源检查；共用证据原则；工作区与状态；各阶段需要加载的 references；完成/失败判据；最终回复要求。

主文件不承载全部数学教程、TeX 宏知识、字体安装说明、表单和全部专业 Profile。每份长 reference 有短目录，规则只维护一处。

加载示例：

| 请求 | 加载 |
|---|---|
| 完整数学精读 | 共用证据 + deep-read + pure-math；到公式/证明阶段再读相应数学模块；导出时才读 PDF 规则 |
| Theorem 3.2 审查 | 共用证据 + proof-audit + theorem-and-proof + counterexamples + 相关 Profile；不默认载入整套实证分析 |
| 解释式 (7) | 共用证据 + explain + equation-reconstruction，以及式 (7) 的定义/假设/上下文 |
| 继续阅读 | resume + 状态文件 + 当前阶段必要模块 |
| 重新导出 | knowledge-base + pdf-publishing + 构建状态；内容变更时回到受影响检查 |

八阶段是依赖和验收框架，允许迭代回到前阶段。专项任务仍检查目标依赖，不能为节省范围删去目标定理必要的前提。

## 4. 主 Skill 元数据

项目展示名：MathResearchReader。目录与 `name`：math-research-reader。用户显式调用：`$math-research-reader`。

SKILL.md 顶部建议只使用必要字段：

```yaml
---
name: math-research-reader
description: >-
  对数学为主的论文执行教学级精读、公式逐步推导、定理与证明重建及严格证明审查，
  兼顾应用数学、密码学、AI 安全和计算机科学。适用于精读论文、解释公式、审查指定定理、
  继续已有阅读；维护可追溯的 Markdown 知识库，并按任务导出中文 PDF。
---
```

description 说明“做什么、何时用”；工作流细节不放在元数据。不要虚构 `commands`、`modes`、`model`、`pip_dependencies` 等 Codex frontmatter 字段。Python 与系统依赖放 pyproject.toml 和环境诊断；发布版本放仓库标签/包配置，数据版本放 schema_version。

agents/openai.yaml 建议：

```yaml
interface:
  display_name: "MathResearchReader"
  short_description: "数学论文教学级精读、公式推导、严格证明审查与中文知识库及 PDF 交付"
  default_prompt: "使用 $math-research-reader 对我提供的论文执行完整教学级精读，建立可追溯的 Markdown 知识库并生成中文 PDF。"
policy:
  allow_implicit_invocation: true
```

保留自动匹配，并支持显式 `$` 调用；目前没有要求“只能手动调用”。如果用户后续明确要求仅显式启用，再改为 false。暂不声明特定 MCP 依赖，因为核心流程无需固定连接器。`dependencies.tools` 不是安装 Pandoc、ctex 或 Python 包的字段。

正式实现时使用 skill-creator 的生成器生成/校验 UI 元数据和 frontmatter，并运行 quick_validate；这类校验只确认包结构，不证明数学流程有效。

官方机制说明：Skill 先暴露 name/description，使用时读取正文和相关资源；本设计按需加载结构与此一致。[OpenAI：Build skills](https://learn.chatgpt.com/docs/build-skills)

## 5. 独立论文知识库

```text
<用户选择的知识库>/
├── index.md                         # 论文导航，可重建
├── concepts/                        # 跨论文复用的概念，保存来源和约定
├── comparisons/                     # 定义/假设/结论转换表
└── papers/
    └── <稳定-paper-id>/
        ├── paper.yaml               # 身份、版本、来源、原件哈希
        ├── source/                  # 原始 PDF/TeX/附录，只读保留
        ├── notes/
        │   ├── overview.md
        │   ├── research-logic.md
        │   ├── prerequisites.md
        │   ├── method.md
        │   ├── contributions.md
        │   ├── research-directions.md
        │   └── followups.md          # 多轮追问产生的新内容
        ├── notation.md
        ├── equations/<object-id>.md
        ├── theorems/<object-id>.md
        ├── audits/
        │   ├── report.md
        │   └── findings/<finding-id>.md
        ├── references.md
        ├── figures/                 # 原图提取与自绘分开并记来源
        ├── report.yaml              # 章节/卡片装配顺序，不放第二份正文
        ├── .mrr/
        │   ├── config.resolved.yaml
        │   ├── source-map.json
        │   ├── object-index.json
        │   ├── dependencies.json
        │   ├── state.json
        │   ├── quality.json
        │   ├── checkpoints/
        │   └── extracted/           # 可重建文本、页面与扫描缓存
        ├── build/                   # 派生 Markdown、TeX、图示转换与日志
        └── exports/
            ├── report.zh-CN.pdf
            └── build-manifest.json
```

这是建议的持久化布局。用户可以指定根目录；默认用当前工作区的独立 `MathResearchReader-Library/`，不得静默写入个人 Vault。源文件可用受保护副本并保留原路径；“只读”至少由写入逻辑和哈希检查保证。

报告构建从 report.yaml 指定顺序装配 Markdown 卡片；同一定理不能在主报告和卡片内各维护一份独立正文。build 下的合并稿标明自动生成。JSON 保存卡片路径、状态和关系，必要短摘录视作可重建缓存。

普通 Markdown 相对链接为基础，避免默认依赖 Obsidian 的 Wikilinks。PDF 构建将内部链接转换成文档锚点，图片路径按知识库根解析；跨论文的外部文件链接在 PDF 中说明用途和可访问性，不能假设离开本机仍可用。

## 6. 数据契约与恢复

| 文件 | 最小字段与用途 |
|---|---|
| paper.yaml | schema_version、paper_id、title、authors、DOI/arXiv、version、source_files、hashes、canonical URL、来源取得时间 |
| object-index.json | id、type、原编号、准确定位、所属章节、核心性及理由、card_path、提取/阅读/解释/审查状态 |
| source-map.json | source_id、文件与哈希、PDF 页序/纸面页码/章节/编号，或 TeX 文件/label/行；定位的核验状态 |
| dependencies.json | 依赖边、所需结论与假设映射、原文依据、外部来源、未解决依赖及影响；模型复核状态 |
| state.json | task_id、mode、scope、profiles、stage、已完成对象、下一行动、未决项、checkpoint、输入与内容哈希 |
| quality.json | check_id、scope、applicable、pass/fail/unverified、依据/执行者/时间、阻塞影响 |
| build-manifest.json | 所有输入 Markdown/图示/模板哈希、工具与字体版本、构建命令、退出码、PDF 哈希、QA 状态 |

状态更新使用原子写入，保留上个 checkpoint；损坏时依据来源和记录恢复，不能直接删除所有证据。用户手改笔记必须保留；重生成前检测差异。

恢复时检查源文版本和笔记变动；定义、假设或引理更改后，让依赖的证明与报告检查失效；只因 PDF 模板修改通常只重跑构建与排版 QA。哈希一致允许复用既有检查，但不证明首次检查就是正确的。

建议状态区分：draft、in-progress、blocked、reviewed-with-open-issues、complete-for-declared-scope。审查发现真实漏洞可以成功交付审查报告，不能同时声称目标定理已验证。完整精读未覆盖范围或 PDF 失败时，整项精读交付仍不完整。

配置优先级建议为：本次用户明确要求 → 单篇配置 → 用户项目偏好 → 包默认值；每次保存解析后的配置。不通过任务默认值覆盖本次用户明确限定的范围。

## 7. 代码与模型分工

| 任务 | 执行方 | 限制 |
|---|---|---|
| 文件检查、哈希、解包、环境诊断 | Python | 结果明确、错误可定位 |
| PDF 提取、渲染、坐标和图表裁剪 | PyMuPDF；pdftotext 备选 | 提取文本不等于已视觉核对 |
| TeX includes/宏/章节/label 扫描 | 结构扫描辅助 | 编号、宏语义、依赖须模型核查 |
| 定义与符号统一、研究逻辑 | 模型 | 保存来源与歧义 |
| 公式、教学证明、漏洞审查 | 模型；可选计算/Lean | 工具检验范围与一般证明区分 |
| 引文身份 | 检索 + 脚本 | 适用性还要读取原结果 |
| Markdown 内容 | 模型 | 唯一人工维护正文 |
| 覆盖账目、链接、依赖一致性 | Python + 模型 | 自动校验不证明数学正确 |
| PDF | Pandoc + XeLaTeX + ctex | 渲染后视觉验收 |

薄 CLI 建议支持 doctor、init-paper、extract、index、checkpoint、validate、build-pdf；这些是未来 `python scripts/mrr.py <子命令>`，当前没有实现，也不是 `$math-research-reader` 后的强制参数。脚本应提供稳定参数、明确输出路径、机器可读结果与非零失败码。

## 8. 在 Codex 中安装与使用

仓库的 `skills/` 目录是源码组织位置，不是自动发现路径。开发时可将完整 Skill 目录复制或链接到：

- 当前项目：`<项目根目录>/.agents/skills/math-research-reader/`。
- 当前用户通用：`~/.agents/skills/math-research-reader/`。

正式使用时选一个作用域，避免同名的多份安装混淆版本。当前宿主已有 `.codex/skills` 中的技能，不需要迁移或删除；新安装优先采用当前官方文档的 `.agents/skills` 目录。只把源码放进 `skills/math-research-reader`，不会自动安装它。

Codex 支持显式 `$skill-name`，也可按 description 自动匹配；CLI/IDE 可使用技能选择器。不同客户端 UI 可能不同；若桌面输入框不提供 `$` 选择，可通过 Skills 界面选择并使用同样的任务文本。更新未出现时重新加载/重启确认。[OpenAI：技能发现、调用和目录](https://learn.chatgpt.com/docs/build-skills)

单篇精读：

```text
$math-research-reader

请对我提供的论文执行完整教学级精读。
重点讲清楚所有核心定义、公式、定理和证明。
全文逐项登记，核心内容完整展开，其他内容说明作用和取舍。
以相关本科基础、研一且不熟悉论文专题为起点，实际补齐专门背景。
展开中间计算和完整证明，绘制多幅数学矢量图，不压缩成摘要。
建立 Markdown 知识库，并生成中文 PDF。
论文：<附加 PDF、TeX，或给出实际文件路径>
```

专项证明审查：

```text
$math-research-reader

请对论文的 Theorem 3.2 进行严格数学审查。
逐项检查假设、量词、推导和边界情况。
核验相关引理及外部结果的准确陈述与适用条件。
不要只给出结论，要提供完整审查依据。
区分原文证明、教学补全、发现的问题与尚未验证的部分。
论文：<实际文件或已有 paper-id>
```

其他入口：

```text
$math-research-reader
继续 <paper-id>，从上次 checkpoint 的未完成证明开始，保留所有既有符号约定。

$math-research-reader
解释 <paper-id> 的式 (7)：给最小数值例子和一般符号推导，说明每一步的条件。

$math-research-reader
比较 <paper-A> 与 <paper-B> 中紧性条件的定义、量词和定理强度，给来源位置。

$math-research-reader
从现有 Markdown 重新生成 <paper-id> 的中文 PDF，并完成逐页排版检查。
```

调用文字不是 shell 命令；Skill 本身不会因 `$` 获得额外执行权限。缺少论文、版本或定理定位且无法唯一推断时才询问所需信息。

## 9. 开发路线与发布

原稿声称“六阶段”，实际只有五阶段。建议保留其所有工作，并显式拆出第六阶段：

| 阶段 | 范围 | 交付与门槛 |
|---|---|---|
| 1 核心与证据 | 主入口、来源/版本、基础检查、模板、对象/状态 schema | 能为单篇建立准确档案与计划，失败透明 |
| 2 教学精读 | 研究逻辑、预备知识、公式、定理、证明、图示、Markdown | 一篇数学样例完成可追溯教学报告 |
| 3 证明审计 | 引用适用性、量词、缺口、反例、边界、依赖传播 | 能发现已知缺陷并给出数学依据 |
| 4 中文 PDF | 模板、图表、目录、链接、自动与视觉 QA | 同源 Markdown/PDF 通过交付检查 |
| 5 恢复与稳定性 | 原稿的异常处理、测试、稳定性，加明确断点恢复验收 | 四类论文、变更失效、保护原稿和重建通过 |
| 6 开源发布与可选形式化 | 原稿的安装文档与正式版本；Lean 最小接口可选 | 完整独立 Skill 包、许可证/来源、安装测试、限制说明 |

原稿时间估计分别为 1–2、2–3、1–2、1、1–2 周；这是原始设想，不是本次承诺。第 5 阶段同时混入 Lean、测试和发布，建议以验收推进，不把“接上 Lean”当成 V1 数学正确的必要条件。用户已确认 Lean 为可选增强，不阻塞首版发布。

V1 先发布 GitHub 源码与可独立安装 Skill；希望进入官方插件分发渠道时再包装 plugin，保持核心目录可复用。当前官方建议可复用分发采用插件，但不需要为了本次架构设计立刻创建 MCP 服务。[OpenAI：技能与插件分发](https://learn.chatgpt.com/docs/build-skills)

开源前检查所有实际打包文件的依赖、许可证、署名及字体/论文样例分发条件；不把私人论文和整个个人知识库默认打包。清楚标明实际验证过的操作系统、宿主和工具版本。
