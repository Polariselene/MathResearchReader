# 连贯讲解局部改写样例

这是根据首次整书反馈新写的两个局部教学单元，用于检查写作规则是否能落到真实论述中。
第一个重写旧报告的线性系统机制，参照该用户论文第13—14页及已保存的第6—7章；
第二个采用此前白化定向测试的标准线性代数背景。均为自写教学重建，不是作者原文摘录，
不冒称完整执行了新的全文精读。此段评测说明不属于待导出的教学正文。

## 从遗漏坐标造成的困难理解伪逆与额外候选

假设我们已把同一局部区域内的$r$次查询整理成线性响应。每次查询产生一个实数，
因此观测组成列向量$t\in\mathbb R^r$；若当前需要解释的隐藏坐标有$c$个，就把它们的响应
按列放进$H\in\mathbb R^{r\times c}$。未知系数$v\in\mathbb R^c$与观测的关系是$Hv=t$。
这一步并没有说$v$可以被唯一确定：不同系数是否可能产生同一批观测，还取决于$H$的列是否独立。

未知架构时，我们未必找到了全部坐标。把其中$p$个已找到的坐标留在
$H_L\in\mathbb R^{r\times p}$，把其余$q=c-p$个放入
$H_R\in\mathbb R^{r\times q}$，对应的真实系数分别为$v_L\in\mathbb R^p$和$v_R\in\mathbb R^q$，
便有
$$
H=[H_L,H_R],\qquad
v=\begin{pmatrix}v_L\\v_R\end{pmatrix},\qquad
t=H_Lv_L+H_Rv_R.
$$
实际可计算的只有保留块，最直接的想法是把全部观测仍交给它解释，求
$H_L\widetilde v_L=t$。问题在于，$H_L\widetilde v_L$无论怎样调系数都只能落在
$H_L$的列空间中；遗漏贡献$H_Rv_R$却可能有落在这个空间外的部分。此时失败原因是方程
根本无解，不能归咎于求解器不够精确。例如保留响应$(1,0)^\top$，观测却是$(2,3)^\top$，
方程的第二行会要求$0=3$。

既然不能保证精确相等，就先问保留坐标究竟能解释多少观测。于是改为最小化
$\|H_Lz-t\|_2^2$，其中待选择的$z\in\mathbb R^p$仍是保留坐标上的系数。
若直接写$z=(H_L^\top H_L)^{-1}H_L^\top t$，又会遇到一个限制：列不独立时
$H_L^\top H_L$没有普通逆。伪逆的用途正是统一处理这些秩情形，而非凭空恢复已经丢失的信息。

可以从奇异值分解看清它做了什么。设$H_L$的秩为$s>0$，取紧奇异值分解
$$
H_L=U_s\Sigma_sW_s^\top,
$$
其中$U_s\in\mathbb R^{r\times s}$的列是观测空间中的正交单位方向，
$W_s\in\mathbb R^{p\times s}$的列是系数空间中可被观测的正交单位方向，
$\Sigma_s\in\mathbb R^{s\times s}$是正奇异值组成的对角矩阵。
把观测投影到这些可解释方向，写成
$t=U_sU_s^\top t+(I_r-U_sU_s^\top)t$。后一部分与$U_s$的列空间正交，
而$H_Lz$总在该空间内，因此勾股分解给出
$$
\begin{aligned}
\|H_Lz-t\|_2^2
&=\|U_s(\Sigma_sW_s^\top z-U_s^\top t)
       -(I_r-U_sU_s^\top)t\|_2^2\\
&=\|\Sigma_sW_s^\top z-U_s^\top t\|_2^2
  +\|(I_r-U_sU_s^\top)t\|_2^2.
\end{aligned}
$$
第二项不受$z$影响，第一项可以取零，只须
$W_s^\top z=\Sigma_s^{-1}U_s^\top t$。
这确定了$z$在$W_s$列空间中的分量，却没有限制与它正交的分量。所有最小二乘解因而可写成
$$
z=W_s\Sigma_s^{-1}U_s^\top t+z_0,
\qquad W_s^\top z_0=0.
$$
这两项正交，其范数平方之和在$z_0=0$时最小。于是最小范数的最小二乘解为
$\widetilde v_L=H_L^\dagger t$，其中
$H_L^\dagger=W_s\Sigma_s^{-1}U_s^\top\in\mathbb R^{p\times r}$。
若$s=0$，则$H_L=0$，所有系数的残差都等于$\|t\|_2$，最小范数选择仍是零向量；
此时将伪逆定义为零矩阵即可覆盖这一边界。

现在才把真实观测的分块表达式代入，得到
$$
\begin{aligned}
\widetilde v_L
&=H_L^\dagger(H_Lv_L+H_Rv_R)\\
&=(H_L^\dagger H_L)v_L+H_L^\dagger H_Rv_R\\
&=W_sW_s^\top v_L+H_L^\dagger H_Rv_R.
\end{aligned}
$$
这不仅给出了一个答案，还指出答案为什么可能偏离真实系数：第一项只能保留$v_L$在可观测
系数方向上的投影，第二项则把遗漏贡献中可解释的部分吸收到已保留系数中。
只有$H_L$满列秩，或已知$v_L$就在其行空间内，才可把第一项直接写成$v_L$。
这个条件解决的是投影损失，不保证遗漏贡献已经消失。

未被解释的部分可继续直接算出。令$P_L=H_LH_L^\dagger=U_sU_s^\top$，
这是观测空间$\mathbb R^r$中投到$H_L$列空间的正交投影，那么残差为
$$
\begin{aligned}
e&=t-H_L\widetilde v_L=(I_r-P_L)t\\
 &=(I_r-P_L)H_Lv_L+(I_r-P_L)H_Rv_R\\
 &=(I_r-P_L)H_Rv_R.
\end{aligned}
$$
最后一行用到$P_LH_L=H_L$。至此可解释部分与不可解释部分各有去处，
不能把“遗漏了一些坐标”简化成“保留系数必错”或“残差必非零”。

取一个可以逐项核对的情况：在二维观测空间中，令
$H_L=(1,2)^\top$、$H_R=(2,-1)^\top$，真实系数分别是实数$v_L=3$、$v_R=4$。
观测为$t=3(1,2)^\top+4(2,-1)^\top=(11,2)^\top$。
保留块的伪逆是$(1,2)/5$，所以$\widetilde v_L=(11+4)/5=3$；
残差却是$(11,2)^\top-3(1,2)^\top=(8,-4)^\top$，范数为$\sqrt{80}$。
保留系数没有被污染，因为$(1,2)\cdot(2,-1)=0$；遗漏贡献全部进入残差。
反过来，只把遗漏响应改成$H_R=H_L$，其他系数不变，则$t=7H_L$，
拟合系数变成7而残差为零。这个变化故意让两个响应列相关，用来隔离可补偿误差，
不能把它当作满足联合满列秩条件的例子。

这就引出相反方向的问题：如果保留的不是太少，而是多加了假候选，真实信号会不会被
分配给它们？“它们不是真的”只是语义标签，不是方程会自动识别的数学条件。
回到完整的$H\in\mathbb R^{r\times c}$和$t=Hv$，再加入$f$列响应
$H_F\in\mathbb R^{r\times f}$，拟合时允许额外系数$w\in\mathbb R^f$，便要求
$H\widetilde v+H_Fw=t$。如果假列能被真实列线性表示，它们便可能分担真实信号。
因此真正有用的条件是联合矩阵$Q=[H,H_F]$满列秩；这也要求$r\ge c+f$。

在这个条件下，假系数确实只能为零，这对应原论文引理1的条件性结论。
证明先检查答案是否存在：将$\widetilde v=v$与$w=0_f$代入，左侧成为$Hv=t$。
再考虑任意一个解$\widetilde v\in\mathbb R^c,w\in\mathbb R^f$，将它的方程减去$Hv=t$，得
$$
\begin{aligned}
0_r
&=H\widetilde v+H_Fw-Hv\\
&=H(\widetilde v-v)+H_Fw\\
&=[H,H_F]\begin{pmatrix}\widetilde v-v\\w\end{pmatrix}
=Q\begin{pmatrix}\widetilde v-v\\w\end{pmatrix}.
\end{aligned}
$$
括号内向量属于$\mathbb R^{c+f}$。由于$Q$的$c+f$列线性无关，
它们的线性组合为零只能使用全部为零的系数，故$\widetilde v-v=0_c$且$w=0_f$。
我们同时证明了原系数的唯一性和假系数为零，没有预先排除$w=0$但$\widetilde v\ne v$的可能。
若仅取一条真实响应和一条完全相同的假响应，方程就只约束两个系数之和；
这说明条件失效时证明恰好断在线性无关这一步。

线性代数由此解释了为什么额外独立候选可呈现零系数，但还没有证明实际采样必然给出联合
满秩矩阵，也没有证明找到的真实坐标已全部覆盖。要把它变成架构恢复判据，
下一步必须检查响应怎样生成、不同局部模式怎样合并，以及坐标如何对齐；
这些是应用引理所需的额外接口，不能由引理的结论倒推。

## 从消除相关性的目标推到逆平方根

设$x\in\mathbb R^d$具有有限二阶矩，均值为$\mu=\mathbb E[x]$。
我们希望把中心化向量$x-\mu$线性变换为$y=H(x-\mu)$，
使$y$的各坐标方差为1、两两协方差为0。
把原协方差记为$C=\mathbb E[(x-\mu)(x-\mu)^\top]\in\mathbb R^{d\times d}$，
这里先假设$C$正定。所求的$H\in\mathbb R^{d\times d}$应满足
$$
\operatorname{Cov}(y)
=\mathbb E[H(x-\mu)(x-\mu)^\top H^\top]
=HCH^\top=I_d.
$$
均值为零来自中心化，不是单靠协方差归一化就能得到的。

最自然的尝试是让每个坐标除以自己的标准差，这能修正方差，却未必消除相关性。
例如二维协方差$C=\begin{pmatrix}2&1\\1&2\end{pmatrix}$的两个标准差都是$\sqrt2$，
这种做法使用$H=I_2/\sqrt2$，于是$HCH^\top=C/2$的非对角元仍为$1/2$。
问题在于相关方向没有与当前坐标轴对齐：沿原坐标轴缩放，处理不了混在一起的方向。

因此改为先找协方差的正交特征方向。由实对称矩阵的谱分解，可写
$C=Q\Lambda Q^\top$，其中$Q\in\mathbb R^{d\times d}$正交，
$\Lambda=\operatorname{diag}(\lambda_1,\ldots,\lambda_d)$且每个$\lambda_i>0$。
将$x-\mu$转到$Q$的坐标系后，协方差成为
$Q^\top CQ=\Lambda$，各方向已不相关，只剩方差$\lambda_i$。
现在在第$i$个方向除以$\sqrt{\lambda_i}$，再转回原坐标系，就得到
$H=Q\Lambda^{-1/2}Q^\top$。逆平方根由逐方向的方差归一化推来，
不是单凭记号$C^{-1/2}$猜出的操作。

把这个选择代回目标，计算过程为
$$
\begin{aligned}
HCH^\top
&=(Q\Lambda^{-1/2}Q^\top)(Q\Lambda Q^\top)
  (Q\Lambda^{-1/2}Q^\top)\\
&=Q\Lambda^{-1/2}(Q^\top Q)\Lambda
      (Q^\top Q)\Lambda^{-1/2}Q^\top\\
&=Q(\Lambda^{-1/2}\Lambda\Lambda^{-1/2})Q^\top\\
&=QI_dQ^\top=I_d.
\end{aligned}
$$
倒数第二步在第$i$个对角元上正是
$\lambda_i^{-1/2}\lambda_i\lambda_i^{-1/2}=1$，这里用到了正定性。

对刚才的二维矩阵，两个单位特征向量是
$q_1=(1,1)^\top/\sqrt2$、$q_2=(1,-1)^\top/\sqrt2$，
直接相乘可得$Cq_1=3q_1$、$Cq_2=q_2$。
取$Q=[q_1,q_2]$并记实数$a=1/\sqrt3$，则
$$
\begin{aligned}
H&=\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}
      \begin{pmatrix}a&0\\0&1\end{pmatrix}
      \frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}\\
 &=\frac12\begin{pmatrix}a&1\\a&-1\end{pmatrix}
                \begin{pmatrix}1&1\\1&-1\end{pmatrix}
 =\frac12\begin{pmatrix}a+1&a-1\\a-1&a+1\end{pmatrix}.
\end{aligned}
$$
它在对角方向$q_1$上缩小$\sqrt3$倍，在反对角方向$q_2$上不缩放，
于是原本的相关性与不同方向的方差都被处理。这个对称白化矩阵是一种选择，
并不是所有白化变换都必须对称；再左乘任意正交矩阵$O$仍有
$(OH)C(OH)^\top=OI_dO^\top=I_d$。

若把正定性弱化成半正定，例如$C=\operatorname{diag}(4,0)$，问题就不再只是选哪种白化。
对任何二维线性变换，$\operatorname{rank}(HCH^\top)\le\operatorname{rank}(C)=1$，
不可能等于秩为2的$I_2$。使用伪逆平方根$\operatorname{diag}(1/2,0)$只能得到
$\operatorname{diag}(1,0)$：非零方差方向被归一化，缺失方向没有凭空长出方差。
这样既解释了正定条件在证明中用在哪里，也说明奇异情形需要改成子空间目标，
不能沿用原来的全维结论。
