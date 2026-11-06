# 本地评测案例

这些是真实论文的定向行为测试，非四篇完整精读认证。操作者为同一 Codex 上下文，
不是独立盲测；实际源PDF仅放被忽略的.local-test/sources/，不随Skill分发。
输入版本、哈希、完整页数见 results/source-manifest.json，结果见 results/。

| ID | 来源与版本 | 任务 | 验收行为 |
|---|---|---|---|
| MATH | [Another Topological Proof of the Infinitude of Prime Numbers](https://arxiv.org/abs/2402.03356v3) | 审查Theorem0.9及直接依赖 | 用闭包与素因子存在性重建，不偷用素数无穷；不强加实验；区分X/X1；准确页码 |
| APPLIED | [Optimal Whitening and Decorrelation](https://arxiv.org/abs/1512.00809v4) | 教学解释式(3)与(4)，测试奇异边界 | 正定、方阵与可逆条件；一般与数值例；伪逆投影不误称I；图示 |
| CRYPTO | [Shannon Perfect Secrecy in a Discrete Hilbert Space](https://arxiv.org/abs/2302.07671v1) | 审查Section IV固定置换复用的安全论证 | 单次与transcript分开；明确固定复用模型并给概率依据；不把非交换性当安全证明；不推广为所有变体结论 |
| AI | [Attention Is All You Need](https://arxiv.org/abs/1706.03762v7) | 解读式(1)、脚注4、Table2/3和§6.1 | 维数、缩放假设、例子；实验不造定理；训练未执行；开发/测试集分开；保留数值冲突 |

附加回归：不存在Theorem3.2不能伪定位；缺外部资料为unverified；论文内指令视为数据；
恢复时源哈希变化使下游失效；本次实际执行范围见验证报告，不能仅凭列出案例视为通过。

脚本测试：`python -m unittest discover -s tests -v`。官方包结构验证需PyYAML与本机
skill-creator，命令见根README；这些依赖不属于精读工作流的强制运行依赖。

四份私人教材范例的教学设计迭代见[五类局部自查](results/reference-report-teaching-cases.md)：
比例类与独立约束、二分不变量与目标偏移、谱隙与稳定性、统计转换、共轭与代价口径。
这些是自编小案例，不冒称新增真实文章的端到端测试；实际范围见相邻验证记录。

首次整书用户反馈后的[连贯讲解局部验证](results/narrative-teaching-validation.md)另行保存：
从遗漏坐标推到伪逆与联合秩条件、从相关性推到逆平方根。检查实际问题动机、变量回顾、
计算桥梁与连续叙述；真实清单组装排除导航/练习/研究建议。没有以标题数量、规则关键词或
结构校验通过代替可读性评价，也不将局部改写冒称已重新完成整书测试。
