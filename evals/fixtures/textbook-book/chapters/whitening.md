# 阅读范围与导航

来源：[Optimal Whitening and Decorrelation，arXiv:1512.00809v4](https://arxiv.org/abs/1512.00809v4)。
本报告仅解释第3–4页式(1)、(3)、(4)与相应条件，不是14页全文精读。
Profile为applied-security中的应用数学部分，不要求威胁模型；本次为同上下文自查。

# 一句话与符号 {#definition}

白化通过缩放协方差的主轴，将不同方向的方差归一，同时允许额外正交变换。

| 符号 | 类型与作用 |
|---|---|
| $x$ | $\mathbb R^d$随机向量，有有限二阶矩 |
| $\mu$ | $\mathbb E[x]$，不必为零 |
| $\Sigma$ | $d\times d$实对称正定协方差 |
| $W$ | $d\times d$白化矩阵 |
| $z$ | $Wx$，目标为$\operatorname{Cov}(z)=I_d$ |

[原文] 第3页§1显式假设协方差正定；式(1)定义$z=Wx$，式(3)为
$W^\top W=\Sigma^{-1}$。原文说明中心化并非单位协方差的必要条件。

# 逐步推导 {#derivation}

[数学重建] 首先按协方差定义展开：

$$
\begin{aligned}
\operatorname{Cov}(Wx)
&=\mathbb E[(Wx-W\mu)(Wx-W\mu)^\top]\\
&=W\,\mathbb E[(x-\mu)(x-\mu)^\top]W^\top\\
&=W\Sigma W^\top.
\end{aligned}
$$

令此矩阵等于$I_d$。因为$W$是方阵且乘积满秩，$W$可逆。
左乘$W^{-1}$并右乘$W^{-\top}$，得到
$\Sigma=W^{-1}W^{-\top}$，取逆便是$\Sigma^{-1}=W^\top W$。
反过来，正定性使$W^\top W=\Sigma^{-1}$满秩，故$W$可逆，逆推得到目标恒等式。

[原文] 第4页§3式(4)：$W=Q_1\Sigma^{-1/2}$，$Q_1^\top Q_1=I_d$。
[数学重建] 写$\Sigma=U\Lambda U^\top$，其中$\lambda_i>0$，则

$$
\begin{aligned}
W\Sigma W^\top
&=Q_1U\Lambda^{-1/2}U^\top U\Lambda U^\top
 U\Lambda^{-1/2}U^\top Q_1^\top\\
&=Q_1UU^\top Q_1^\top=I_d.
\end{aligned}
$$

因此缩放完成白化后，旋转或反射仍保持协方差为$I_d$。正交自由度不等于只有旋转。

# 最小例与一般形式

[数学重建] 对任意$a,b>0$，取$\Sigma=\operatorname{diag}(a^2,b^2)$，
$W=\operatorname{diag}(a^{-1},b^{-1})$，可直接算出$W\Sigma W^\top=I_2$。
数值例$a=2,b=3$：$W=\operatorname{diag}(1/2,1/3)$，
输入$(2,3)^\top$变为$(1,1)^\top$。单个向量的变换只示范机制，
不能从一个样本证明其总体协方差。

看图时比较两条主轴；这是一条等协方差轮廓，并非所有分布的等概率密度线。

![教学示意图：正定对角协方差的主轴缩放；左为半轴2和3的椭圆，右为单位圆。示意轮廓不假设总体一定服从高斯分布。](../figures/whitening.pdf){width=90%}

# 退化边界 {#boundary}

[数学重建] 若$\Sigma=\operatorname{diag}(4,0)$，普通逆平方根不存在。
伪逆平方根$H=\operatorname{diag}(1/2,0)$满足

$$
H\Sigma H^\top=
\begin{pmatrix}1&0\\0&0\end{pmatrix}\ne I_2.
$$

一般秩$r<d$时结果是协方差值域上的投影；任意$d\times d$线性变换的协方差秩最多$r$，
所以不能在全空间得到满秩$I_d$。可在非零特征值子空间得到$r$维白化。
正则化$\Sigma+\varepsilon I$改变目标；与原$\Sigma$相乘后的特征值为
$\lambda_i/(\lambda_i+\varepsilon)$，不能继续声称原等式精确成立。

# 审查结论与未验证

所选正定方阵范围的代数推导闭合；奇异例说明扩展的边界，不能用来推翻原文明确正定的结论。
没有假设零均值，也未把不相关声称为独立。后续最优性命题、外部文献、数值实验未在本次审查范围。
参见[推导](#derivation)与[边界](#boundary)。PDF构建和视觉QA另行记录，不能由正文自称通过。
