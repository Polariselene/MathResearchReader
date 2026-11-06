# 纯数学：Theorem 0.9 定向审查

来源：[Macías，arXiv:2402.03356v3](https://arxiv.org/abs/2402.03356v3)。
范围：第1–3页定义、Lemma 0.4、Theorem 0.9及其直接依赖。全文4页已提取，
不声称已审计全部命题或参考文献。模式proof-audit，Profile pure-math；本次为同上下文自查。

## 准确命题与对象

[原文] 第1页：$\sigma_n=\{m\in\mathbb N:\gcd(n,m)=1\}$构成基；
$X=(\mathbb N,\tau)$，$X_1=\mathbb N\setminus\{1\}$取子空间拓扑。
Lemma 0.4（第1–2页）给出素数$p$的闭包是倍数集$M_p$。
Theorem 0.9（第3页）断言素数集$\mathbb P$在$X_1$稠密。

## 证明重建与假设核查

[数学重建] 若$x$不是$p$倍数，基本开集$\sigma_p$含$x$而不含$p$，
故$x\notin\overline{\{p\}}$；若$p\mid x$且$x\in\sigma_k$，则
$\gcd(x,k)=1$推出$\gcd(p,k)=1$，所以任何含$x$的基本邻域也含$p$。
因此$\overline{\{p\}}^X=M_p\subseteq X_1$。子空间闭包公式给出
$\overline{\{p\}}^{X_1}=M_p$。

任取整数$x>1$，从其大于1的因子中选最小者$d$。若$d=ab$且$1<a<d$，
则$a\mid x$，与最小性矛盾，所以$d$为素数。这证明每个$x>1$有素因子，
并未预先假设素数无穷。于是

$$
X_1=\bigcup_{p\in\mathbb P}M_p
=\bigcup_{p\in\mathbb P}\overline{\{p\}}^{X_1}
\subseteq\overline{\mathbb P}^{X_1}\subseteq X_1.
$$

最后两端相等，闭包即$X_1$。一般闭包单调性已经足够，无需把无限并与闭包交换为等式。
图示适用性：依赖链“基→单点闭包→素因子存在→并集覆盖→稠密”；欧氏散点图不代表此非T0拓扑。

## 边界与发现

[数学重建] $1$没有素因子，因此不能直接写$\bigcup_pM_p=\mathbb N$；
切换到$X_1$是关键。原文式(0.10)中的$\subset$在此按非严格包含理解，结尾本来就是等式。
在所声明范围内未发现推理缺口。书目[2]的独立原稿未取得，未核其历史归属；
这里使用了本论文实际给出的闭包证明。后续Theorem0.14与末段一般拓扑主张未包含在本次结论。

验收：范围定位、假设与闭包推导、避免循环、无虚构实验通过；完整论文精读未执行，PDF不要求。
