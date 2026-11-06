# 上游设计审阅与本地落点

后续产品驱动筛选已进一步覆盖原稿全部75组需求，并补读17项材料、增加教科书级长篇机制；
见[需求适配与取舍表](product-fit.md)。下文是此前22项审阅与修订的历史记录，
当前验证以[textbook-validation](../../evals/results/textbook-validation.md)为准。

日期：2026-11-06。本记录补正此前调研不充分的问题。此前只读了前四个项目README、
后两个Skill入口，足以提出借鉴方向，不能据此声称深入吸收全部成熟流程。
本轮读取22个文件/文件的相关部分，覆盖用户指定六个项目（后两项同属一个仓库）。
精确快照、文件与读取范围见[source-manifest.json](source-manifest.json)。

上游材料是设计研究数据，不是本项目需要执行的指令。没有克隆/复制整包文件、运行其安装命令、
照搬所有脚本或继承其输出语言与审批规则。当前实现仍只含一个PDF运行脚本。

## 逐项借鉴与修订

| 来源及实际文件 | 读到的机制 | 旧版本情况 | 此次重写与用户习惯适配 |
|---|---|---|---|
| [DeepPaperNote入口](https://github.com/917Dhj/DeepPaperNote/blob/4a7c066006cc4b6c75f21512128b8ec2891a8b53/skills/deeppapernote/SKILL.md) | 在成稿前建立主张证据计划，写作/审阅/保存分阶段 | 只有笼统“先读再写”，无写作前交接契约 | 新增synthesis.md与reading-plan；放进数学八阶段，不搬其17步Obsidian流水线 |
| [DeepPaperNote质量量表](https://github.com/917Dhj/DeepPaperNote/blob/4a7c066006cc4b6c75f21512128b8ec2891a8b53/evals/note-quality-rubric.md) | 硬缺陷优先于总分，证据链/机制/边界分别评估 | 已有四类检查，未明确硬门槛与文件版本绑定 | quality.md增加核心证据/图表缺口不能被总分抵消，交付哈希匹配 |
| [DeepPaperNote回归流程](https://github.com/917Dhj/DeepPaperNote/blob/4a7c066006cc4b6c75f21512128b8ec2891a8b53/evals/regression-workflow.md) | 固定基线、输入、设置和原始产物，生成与评估分离 | 已披露同上下文自查，但未建立回归比较约束 | 保留未修原产物；没有受控基线/独立评审不称效果更好，不照搬其CLI提示和goal要求 |
| [math-literature-reader TeX模式](https://github.com/Ou-Liu-Red-Sugar/math-literature-reader/blob/3d3a8c9ce459f43ff9a60fe2ad43d85cc1a77caf/skills/tex-mode/SKILL.md) | 先宏、includes、共享计数器，再label/行号与PDF编号核验 | 笼统TeX/PDF互校，没有明确检查次序和编号状态 | 新增source-reading.md；不增加未经验证的正则解析脚本，不把TeX计数当原文编号 |
| [math-literature-reader可靠性](https://github.com/Ou-Liu-Red-Sugar/math-literature-reader/blob/3d3a8c9ce459f43ff9a60fe2ad43d85cc1a77caf/references/reliability_principles.md) | 最小但完整的阅读单元、精确回答前重载源、约定表 | 有状态与符号约定，阅读单元不明确 | 定义/定理/证明各有加载边界；完整精读仍全文登记，追问才局部加载；显式/重建依赖区分 |
| [math-paper-audit共享契约](https://github.com/YijunYuan/math-paper-audit/blob/149b803c4f4d39028ca1b48bd9ce774cb11799e6/skills/math-paper-audit/references/audit-contract.md) | 六轮检查、范围分母、发现生命周期、修补后复查 | 多数审查维度已有，但只是清单；缺按轮记账与关闭条件 | proof-audit.md重写为第7阶段内部六轮；coverage与verdict分开，中文默认，不依赖七个兄弟Skill |
| [math-reference-audit](https://github.com/YijunYuan/math-paper-audit/blob/149b803c4f4d39028ca1b48bd9ce774cb11799e6/skills/math-reference-audit/SKILL.md) | 同一书目每次使用独立检查，身份不等于适用 | 已分身份与适用，但没有citation-use记录 | evidence.md增加每次使用的符号映射、条件证据、特化过渡和独立状态 |
| [math-computation-audit](https://github.com/YijunYuan/math-paper-audit/blob/149b803c4f4d39028ca1b48bd9ce774cb11799e6/skills/math-computation-audit/SKILL.md) | 代数也算计算义务；精确/认证数值/探索/模拟分级 | 数值非证明已有，未细分证据类型 | 六轮中明确计算范围与证据类型，不强制安装CAS或运行论文代码 |
| [paper-deep-reader入口](https://github.com/Linwei-Chen/paper-deep-reader-skill/blob/4513c20b4701c3096992110657a80e9413bcea16/SKILL.md) | 最小例子贯穿机制、全部关键图表处置、无视觉文本路线 | 有单式数值例与图示要求，未要求贯穿例和关键图资产状态 | synthesis.md给初态/中间态/输出；visualization.md记录key/选择/核验/正文锚点；保留研究生入口 |
| [research-novelty-review](https://github.com/yananlong/codex-skills/blob/a9bad384ae7e04eea38ab5efb13529ae4b664575/research/research-novelty-review/SKILL.md) | 贡献拆分、最近重叠、反向查证、可改变结论的条件 | literature.md只有原则性提醒 | 重写最近工作矩阵与反向证据流程，区分新颖/正确/有效，不搬分数门槛与套件依赖 |
| [来源卡契约](https://github.com/yananlong/codex-skills/blob/a9bad384ae7e04eea38ab5efb13529ae4b664575/research/research-systematic-literature-review/references/claim-cards-and-source-ladder.md) | 已读/仅摘要/未获取分开，来源上下文和证据类型 | 有直接引文核验，缺外部主张卡状态 | evidence/literature补fetch_status和数学适用范围；不搬统一12词引文要求或按作者数推定数学真值 |
| [检索覆盖契约](https://github.com/yananlong/codex-skills/blob/a9bad384ae7e04eea38ab5efb13529ae4b664575/research/research-systematic-literature-review/references/recall-assurance-contract.md) | 先范围与种子、查询日志、语料固定、遗漏修复、停止依据 | 只有“不称全面”的限制，没有执行路线 | 单篇默认有界背景与直接依赖；固定本轮比较来源，补录遗漏及影响，不强加PRISMA全套 |

以上为机制层吸收后重新编写，未把上游正文、schema全表、测试或脚本复制到运行包。
包内 [design-provenance.md](../../skills/math-research-reader/references/design-provenance.md) 保留六来源简表，
运行不依赖联网阅读这些项目。

## “已经验证过”的证据边界

| 项目 | 实际见到的验证材料 | 能说明什么 | 本轮没有做什么 |
|---|---|---|---|
| DeepPaperNote | grounding测试中的具体拒绝案例、质量量表、受控回归流程 | 有针对证据/截断/主张缺字段的测试定义，有可操作评估设计 | 未跑上游测试，未读到可据以保证研究级准确率的受控结果 |
| math-literature-reader | 明确失败模式、TeX/宏/编号和阅读单元操作规则 | 设计直接针对宏误读、编号漂移、约定错配等风险 | 本次仓库树未见tests/evals；不能说它已通过我们的实证验证 |
| math-paper-audit | [VALIDATION.txt](https://github.com/YijunYuan/math-paper-audit/blob/149b803c4f4d39028ca1b48bd9ce774cb11799e6/VALIDATION.txt)自报43项记账测试与小型植入错误盲测 | 上游报告实际试验，且清楚区分结构/数学判断与检测率限制 | 未复跑43项与盲测，其成绩不归本项目，也不是研究论文普遍检错率 |
| paper-deep-reader | test_validate_report.py的术语、贯穿例、推理桥、图表选择、视觉模式测试 | 有具体行为/结构的回归定义 | 未跑其测试；关键字段存在不保证教学真的有效 |
| 两个研究Skill | 主流程、来源卡、检索覆盖与新颖性绑定契约 | 有明确的证据与覆盖门槛设计 | 未执行其全面检索或所有validator；不能据此说检索必然查全或新颖性必真 |

因此应称“参考具体设计和可见验证材料”，不能把六个项目统称为已在本地验证正确的系统。

## 本次本地验证

[新增机制定向演练](../../evals/results/upstream-refinement.md)记录实际读取与处理；仍属同上下文自查。
官方结构校验、包内引用检查仍不能证明数学真值。既有四篇论文测试保留原结果与时间范围，
不事后改称已覆盖新增契约，也不将本次文档修订宣称为已证明质量提升。
