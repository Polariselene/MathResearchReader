# 参考项目、来源与待决问题

## 1. 本轮已确认

| 问题 | 用户回答 | 设计影响 |
|---|---|---|
| 教学起点 | 数学研究生基础，遇到专门背景继续补充 | 不默认从本科所有课程重讲；也不假定已熟悉论文子领域 |
| 完整性 | 全文逐项登记，核心完整展开，其余说明作用和取舍 | 建全量对象清单、核心依赖闭包和取舍记录 |
| 外部依赖 | 核验直接依赖，更深层缺口列出按需继续 | 不把单篇精读自动扩成无限文献综述 |
| 专项审查交付 | 默认 Markdown，明确要求时导出 PDF | 不为每次专项审查自动进行 PDF 构建 |
| Lean 首版要求 | 可选增强，不阻塞精读与审计发布 | 基础功能无需安装 Lean；实际验证单独报告 |

## 2. 参考项目审阅记录

初始设计轮通过 GitHub 连接器读取前四个项目的 README、后两个指定目录的 SKILL.md。
该轮仅能提出借鉴方向，调研深度不足以证明完整吸收。用户指出后已补读22个文件/相关部分，
固定上游快照并修订实际工作流；详见[逐项来源与落点](../upstream-review/README.md)。
下表保留初始建议；实际新增机制、验证证据和限制以新审阅记录为准。上游文字均视作参考数据。

| 项目 | 实际读到的设计 | 建议吸收 | 保持本项目独立的地方 |
|---|---|---|---|
| [DeepPaperNote](https://github.com/917Dhj/DeepPaperNote/blob/main/README.md) | 单篇进入长期知识库，保留图表和方法证据，来源不足不装作精读完成 | 单篇摄入、持续知识库、图文上下文、保存保护 | 不依赖 Obsidian/Zotero；数学推导与审计是独立门槛 |
| [math-literature-reader](https://github.com/Ou-Liu-Red-Sugar/math-literature-reader/blob/main/README.md) | TeX/PDF按源路由、宏和定位、单篇状态、约定对照、最小可靠阅读单元 | 源码/渲染互校、持久化状态、跨论文约定表 | 不继承其 Claude 专用 slash commands；用户完整精读请求已包含必要索引/依赖工作 |
| [math-paper-audit](https://github.com/YijunYuan/math-paper-audit/blob/main/README.md) | claim map、引用适用、证明、压力测试、计算与手稿审查；覆盖/依赖与统一发现 | 审计维度、依赖、精确发现、未核验项、独立性披露 | 不要求安装七个对外 Skill；本项目中文报告与用户要求优先；同上下文自查不冒称独立 |
| [paper-deep-reader-skill](https://github.com/Linwei-Chen/paper-deep-reader-skill/blob/main/README.md) | 通俗入口与技术深度、最小例子、关键图文邻接、来源分离 | 教学层次、机制例子、图文解释、证据边界 | 使用数学研究生入口与数学八阶段；无实验时不强套六部分实验模板 |
| [research-novelty-review](https://github.com/yananlong/codex-skills/blob/main/research/research-novelty-review/SKILL.md) | 贡献拆分、最近工作对照、优先找重叠、检索记录、保守定位 | 创新主张与证据分离、贡献比较矩阵、避免无依据首创结论 | 不照搬其评分门槛和整个 sibling Skill 依赖；新颖性与数学正确分开 |
| [research-systematic-literature-review](https://github.com/yananlong/codex-skills/blob/main/research/research-systematic-literature-review/SKILL.md) | 明确范围、证据表、查询日志、来源身份、检索覆盖限制、数学领域适配 | 直接依赖与关联工作日志、有限覆盖声明、定义适配 | V1 单篇精读不强制全量PRISMA系统综述，也不假装检索完整 |

PaperForge 仅在原稿末尾以名称出现，没有唯一项目 URL；保留为待识别参考，未推断其功能或许可证。

开源来源记录应包含 URL、实际引用 commit、查看文件、借鉴的思想、是否复用文件、复用文件许可证/通知。原稿要求优先重新实现，当前未复制任何上游 Skill、脚本或模板进入项目。README 的许可证徽章或仓库元数据不替代具体文件的许可证核对。发布前核对实际打包内容和所有复用声明。

## 3. 原稿矛盾与待决事项

| 项目 | 原稿现状 | 当前处理 |
|---|---|---|
| 五个特色功能 | 仅列公式重建、教学证明、反例边界三项 | 三项完整保留；不虚构另两项。追问与可视化可成为额外特色，但不是原稿已有编号 |
| 六阶段路线 | 实列五阶段 | 建议拆出恢复稳定性和开源发布，补成六阶段；明确是整理建议 |
| 全部公式还是核心公式 | 一处自检说“有公式没解释”，其他多处强调核心 | 用户已选全文登记、核心展开；其余说明作用和取舍 |
| 独立审查 | 原稿提独立审查但未指定执行机制 | 设计支持第二轮审查；没有实际独立执行只能标自查，不默认启动多agent |
| Lean V1 范围 | 技术栈写可选，原开发阶段5又写形式化接口 | 已确认可选增强，不阻塞首版发布 |
| 专项审查 PDF | 完整精读明确MD+PDF，专项示例未明确 | 已确认专项默认MD，明确要求时导出PDF |
| 开源许可证 | 初始未指定；后续用户选择MIT | 已创建根目录及可独立分发Skill内的LICENSE |
| 公开分发 | 希望开源，可接Codex | 建议GitHub源码+完整Skill；后续需要安装渠道时再插件化 |
| 知识库格式 | Markdown，未要求特定应用 | 通用Markdown为基础，Obsidian集成可选 |
| 中文PDF独立传播 | 要求阅读版，未指定能否带出全部跨库链接 | PDF内引用和锚点需自足；本机跨论文路径不能保证他人可用 |

后续开发前可确认但不阻塞本次设计：主要数学方向/常用教材、公开许可证选择、Windows以外支持范围、是否保留原稿所有非核心公式的简短逐项解释、外部资料不可访问时可接受的交付范围。用户当前默认已足以形成可执行架构，无需先回答所有问题才整理。

## 4. Codex 官方来源

核验日期：2026-11-06。

- [Build skills](https://learn.chatgpt.com/docs/build-skills)：必需的 name/description、逐步加载、显式/隐式调用、本地 `.agents/skills` 发现路径、agents/openai.yaml、插件分发。本地旧目录以宿主实际配置为准，不因此自动迁移。
- 本地内置 skill-creator 的 SKILL.md 与 references/openai_yaml.md：目录命名、入口与支持资源职责、UI字段、默认提示包含技能调用、自动发现默认开启、结构校验的边界。

这些来源支持宿主机制。本文给出的八阶段、目录细分、schema、CLI和质量门槛是 MathResearchReader 的产品设计，不是 OpenAI 平台内置能力或强制格式。

## 5. 公开前许可核对

具体快照许可、未确认项与材料排除范围以[第三方材料说明](../../THIRD_PARTY.md)为准。
早期“未复制文件”的设计记录不等于所有来源都采用MIT，也不构成再发布私人论文或图片的授权。
