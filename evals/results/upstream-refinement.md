# 上游机制吸收后的定向演练

日期2026-11-06。输入为[自编案例](../fixtures/upstream-mechanisms.md)与
[实际TeX](../fixtures/upstream-mechanisms.tex)。按修订后的Skill在当前上下文执行，
不属于新agent盲测；不据此宣称优于上一版。

| 案例 | 实际处理结果 | 可检查依据/范围 |
|---|---|---|
| U1 | \R按\mathcal R解释为$M_2(\mathbb R)$，不作实数域；读取全局对称条件和依赖引理；label可定位，渲染编号unverified | 实际读取TeX第3–5、9–10、19行；存在共享计数器，不能数theorem环境冒充编号；本次未编译 |
| U2 | 两个citation-use分别处理：C1适用，C2不适用 | $[0,1]$紧且非空，最大值1；$\mathbb R$虽闭但不紧，对任意$x$有$f(x+1)>f(x)$，所以无最大值。B已提供陈述不等于两次都满足条件 |
| U3 | C保持unsupported/unverified；图登记key=true、asset=null、visual_verification=not-performed；不称完整精读完成 | 标题/图注未提供曲线或数据，不能推出稳定下降，缺口传递到主张C |
| U4 | 发现仍open，建议修补另记；T依赖未消除 | 增加正定改变假设，未被采用并复查；伪逆也不等于普通逆。不能把建议视为已修复 |
| U5 | 删除“首次证明”的报告判断，保留[原文]作者自称；可称相同结论的更短证明候选贡献 | 本地B已经覆盖同一A/P；未核更短证明正确性及其他文献，创新只限已提供语料，不宣称查全 |
| U6 | h1教学/数学检查失效，保留用户修改，重查假设及依赖后再以当前哈希出具检查 | 内容变化不是纯样式变动；旧报告不能继续假装覆盖h2 |
| U7 | 同时报告“C1有已证实问题”和“覆盖未完成：C2/C3” | 范围分母为3；C2=blocked、C3=pending，不能以只检查1项的结论取代全部；来源缺失不归not-applicable |

以上为规则实际应用的可读结果，未编写只匹配关键词的“能力测试”。U1没有PDF，因此没有把
预期计数结果登记为已核验原编号。没有新增运行脚本。旧四类论文报告保留原样，
本次没有重跑四篇全文精读、上游测试套件或PDF排版（PDF代码/模板均未修改）。

机器结构/链接检查与官方quick_validate见upstream-refinement-checks.json及upstream-quick-validate.txt。
