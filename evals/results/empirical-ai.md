# 实证 AI：attention 与证据一致性

来源：[Vaswani等，arXiv:1706.03762v7](https://arxiv.org/abs/1706.03762v7)。
范围：第4页§3.2.1式(1)/脚注4，第8页Table2/§6.1，第9页Table3；
15页全文已提取，但仅选定内容进入本次定向检查。Profile empirical-cs-ai；同上下文自查。

## 机制与例子

[原文] attention为$\operatorname{softmax}(QK^\top/\sqrt{d_k})V$。
[数学重建] 对$Q\in\mathbb R^{n_q\times d_k}$、$K\in\mathbb R^{n_k\times d_k}$、
$V\in\mathbb R^{n_k\times d_v}$，分数矩阵为$n_q\times n_k$，softmax逐行归一，
输出$n_q\times d_v$。取$d_k=1$、$Q=[1]$、$K=[0,\log3]^\top$、
$V=[2,6]^\top$，权重为$(1/4,3/4)$，输出$5$。

[原文] 脚注4以独立、零均值、单位方差分量说明点积方差为$d_k$。
[数学重建] 在这些假设下，$\mathbb E[q_ik_i]=0$、$\operatorname{Var}(q_ik_i)=1$，
交叉协方差为0，故求和方差$d_k$，缩放后为1。这是动机中的模型计算，
不是对所有训练得到Q/K的无条件定理。

## 实验读取与发现

[原文] 第8页Table2中Transformer big的EN-DE为28.4，EN-FR为41.8；
同页§6.1正文对EN-FR写41.0。已视觉核对确有不一致。
发现AI-01：presentation/data-consistency，最终数值应向版本记录/作者补核；
报告保留两数，不能静默替作者选一数或写为本次复现结果。

[原文] 第9页Table3用newstest2013开发集，Table2比较newstest2014测试集；
不能直接用两表BLEU差异当同一协议的增益。Table3的PPL按wordpiece，不是每词PPL。

## 范围与限制

有实验与架构分析，无需捏造主定理。本次未训练、未重新算BLEU、未核其他baseline原文，
不声称复现、当前SOTA或整篇审计通过。公式/表格解释完成，数值冲突保持unverified。
