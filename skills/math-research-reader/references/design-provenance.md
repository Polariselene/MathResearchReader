# 工作流的设计来源

本Skill依据用户八阶段数学阅读习惯重新组织，以下项目是设计参考，非必须安装的依赖。
没有整包复制上游文件，没有将上游验证成绩作为本项目验证成绩。

| 上游快照 | 吸收的机制 | 本包落点与适配 |
|---|---|---|
| [DeepPaperNote，4a7c066](https://github.com/917Dhj/DeepPaperNote/blob/4a7c066006cc4b6c75f21512128b8ec2891a8b53/skills/deeppapernote/SKILL.md) | 写作前主张/证据计划，内容与可读性分轮检查，最终文件绑定检查版本 | synthesis.md、quality.md；中文研究生教学，Markdown/PDF双交付，不要求Obsidian |
| [math-literature-reader，3d3a8c9](https://github.com/Ou-Liu-Red-Sugar/math-literature-reader/blob/3d3a8c9ce459f43ff9a60fe2ad43d85cc1a77caf/references/reliability_principles.md) | 来源分流、宏/编号核对、完整阅读单元、约定转换、准确回答重载源 | source-reading.md；全文精读仍逐项登记，局部问题才按需索引 |
| [math-paper-audit，149b803](https://github.com/YijunYuan/math-paper-audit/blob/149b803c4f4d39028ca1b48bd9ce774cb11799e6/skills/math-paper-audit/references/audit-contract.md) | 分轮审查、范围与结论分账、引用逐次适用性、修补关闭与下游重查 | proof-audit.md、evidence.md；单入口、默认中文、专项可缩放，不安装七个Skill |
| [paper-deep-reader，4513c20](https://github.com/Linwei-Chen/paper-deep-reader-skill/blob/4513c20b4701c3096992110657a80e9413bcea16/SKILL.md) | 一个例子贯穿机制、关键图表全处置、图文论证相邻、无视觉诚实降级 | synthesis.md、visualization.md；研究生入口、数学八阶段，不强套实验章节 |
| [research-novelty-review，a9bad38](https://github.com/yananlong/codex-skills/blob/a9bad384ae7e04eea38ab5efb13529ae4b664575/research/research-novelty-review/SKILL.md) | 贡献拆分、最近重叠、优先反向证据、证据不足时收窄创新说法 | literature.md；不继承分数阈值或整套研究Skill依赖 |
| [research-systematic-literature-review，a9bad38](https://github.com/yananlong/codex-skills/blob/a9bad384ae7e04eea38ab5efb13529ae4b664575/research/research-systematic-literature-review/references/recall-assurance-contract.md) | 有界证据图、已读来源卡、查询/覆盖记录、固定语料与遗漏修复、停止依据 | literature.md；默认只核直接依赖与单篇背景，不冒称全面系统综述 |

这些机制是阅读具体规则后重新编写的实现约束，非上游正确性认证。上游中只有实际见到
测试/试验材料的机制才能称“有验证材料”；测试定义、项目自报通过和本地独立复验分别记录。
本次未运行上游完整测试套件，未取得所有项目的研究级效果证明。运行时无需读取本文件外部链接。

进一步筛选后，本包采用textbook.md、proof-obligations.md明确教科书级长篇和适用的专门证明检查。
补充来源包括D的deep-analysis/evidence-first/final-writing/figure-placement与glossary契约，
M的memory/convention/macro/diagram规则，A的proof/stress检查表，P的audience/reading/quality，
N的反向查询和S的数学adapter。固定快照仍为上表版本，具体文件在仓库审阅manifest中登记。

明确不采用：D的少量公式/数字配额和工程师默认入口；M将主动深读全部改成用户逐项点选；
P的零背景默认和固定六部分；N的研究项目去留评分；S的默认全面系统检索；以及
上游专用Vault、API/服务器、审批界面与多Skill安装链。它们有各自产品用途，超出或不适配本需求。
百页教学讲义不是任何单一上游已验证交付，长篇单元、接口、恢复和整书编译由本项目重组实现。

另参考用户提供的四份私人教材式精读范例，抽读目录、代表性推导与实际页面后，补强
来源/数学性质分轴、近似转换、算法不变量、可识别性/稳定性、贯穿例与失败例、反向索引、
早期还借鉴了带解答自检及阅读路线；首次整书用户反馈后，按textbook.md默认移出PDF，
不再把它们作为完整精读的必生成内容。仅吸收教学组织，不复制文本、图像、批注或私人PDF；
范例不是数学正确性基准，运行不需要取得这些文件。具体范围与取舍保存在仓库审阅记录。

## 许可与分发边界

2026-11-06核对上述固定快照：DeepPaperNote、math-literature-reader和paper-deep-reader的
LICENSE为MIT；math-paper-audit为Apache-2.0并有NOTICE；两个codex-skills参考项目在
所查根目录和项目目录未见明确许可证，其文件再发布授权尚未确认。

本包只保留来源链接和重新编写的工作流，不带入上游项目的源文件、图片、模板或数据。
授权不明文件一律不得纳入分发。后续若需复用，先记录具体文件/版本/许可和通知；
MIT不覆盖本项目无权授权的部分。私人原始材料和论文原图也不随包发布。
