# 私人教材范例：匿名化设计借鉴记录

2026-11-06。此前在用户授权的本地阅读任务中参考了四份私人讲义，抽读目录、代表性推导
和渲染页面。不是逐页或逐式数学认证。原件、文件名、文件哈希、页码对应、批注和提取结果
只保留在本地私密归档；公开项目不需要取得这些讲义才能运行。

这里只记录重新编写后的教学设计取舍，不复制讲义的表述、公式展开、图像或批注。
早期练习集和阅读路线建议现由[最新用户反馈](design/05-teaching-feedback.md)覆盖。

## 吸收的组织方法

| 设计观察 | 重新编写后的要求 | 规则位置 |
|---|---|---|
| 精确推导与近似转换应有明显依据 | 每次替换解释条件、误差与结论强度；来源标签和数学性质分别记录 | [数学教学](../skills/math-research-reader/references/mathematics.md)、[证据规则](../skills/math-research-reader/references/evidence.md) |
| 数学可识别与数值稳定是不同问题 | 将存在、唯一、扰动、谱隙和实际阈值分开解释，补可复算失败例 | mathematics、[长篇教学](../skills/math-research-reader/references/textbook.md) |
| 依赖顺序比原文顺序更适合学习 | 工具在需要时引入，正文和附录按依赖重组，保留反向索引 | textbook、[成稿流程](../skills/math-research-reader/references/synthesis.md) |
| 算法变量应沿状态转换讲解 | 连接输入、状态、不变量、分支、返回值和实际目标，不能只翻译伪代码 | mathematics |
| 同一贯穿例应能接起中间结果 | 保持参数和约定连续，必要时只改变一个条件定位失败步骤 | textbook |
| 简短解释应能追溯到完整依据 | 稳定锚点链接唯一数学正文，符号与原文对象可反查 | [知识库](../skills/math-research-reader/references/knowledge-base.md) |
| 实验表头和代价口径决定结论范围 | 区分状态、表示、单阶段与整流程成本，不把不同指标混为一谈 | [应用数学与安全](../skills/math-research-reader/references/profiles/applied-security.md) |

## 不继承的部分与验证边界

不复制私人讲义的内容、版式、批注、截图、研究结论或文件指纹；不将特定论文的维数、
网络或硬件设置变成所有论文的模板。不默认输出演讲包或练习库，不以页数配额凑教材。

本次公开记录是设计方法摘要。原始读取范围及未脱敏证据保存在本地；
[历史迭代验证](../evals/results/reference-report-validation.md)与
[自编教学案例](../evals/results/reference-report-teaching-cases.md)保留各自真实范围，
不是私人讲义的再发布、全部正确性证明或读者学习效果测试。

发布时仅纳入匿名化说明与自编案例。私人材料的公开授权未确认，因此一律不纳入分发，
不能用本项目MIT许可证替代其权利人的许可。材料范围见[第三方说明](../THIRD_PARTY.md)。

## 2026-11-07再次对照：从设计标签回到实际讲法

用户再次反馈短稿仍听不懂。本次重新读取四份讲义的目录与代表性完整段落，
包括局部映射递推、几何观测转方程、算法状态与两分支、商环消元与表示转换；
实际查看每份的代表页面。没有逐页审查全部讲义或认证其全部数学内容。

重新识别的重点是解释的停留尺度：一次操作的输入和输出先讲透，
逐项说明坐标/系数怎样移动，再将这个过程一般化；例子会承担推导任务，而不只是证明后的装饰。
讲义还会主动回答当前最容易误解的问题，再回到论文目标。
吸收这种解释方法，不复制其句子、公式案例、版式和附属问答章节。

此前抽象的“背景—推导—算例”检查没有阻止专家式压缩。本次将
[讲解尺度](../skills/math-research-reader/references/teaching-style.md)及
[自编完整单元](../skills/math-research-reader/references/examples/adjoint-walkthrough.md)
纳入Skill，并要求在实际论文的难单元先校准，具体见
[本轮反馈](design/07-readable-teaching-feedback.md)及[验证](../evals/results/readability-validation.md)。
