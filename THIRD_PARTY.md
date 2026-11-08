# 第三方材料与许可范围

核对日期：2026-11-06。本项目MIT许可证仅适用于本项目有权授权的原创代码、说明和自编示例。
它不重新许可上游作品、字体程序、论文、原图、数据集或私人资料。公开可访问不等于允许任意再发布。

## 设计参考项目

以下固定快照用于机制研究，当前公开文件没有整包带入其Skill、脚本、模板、图片或数据。
本项目的机制选择和重新编写范围见[来源对照](docs/upstream-review/README.md)及
[随包来源说明](skills/math-research-reader/references/design-provenance.md)。

| 来源与固定版本 | 查到的许可 | 当前处理 |
|---|---|---|
| [DeepPaperNote / 4a7c066](https://github.com/917Dhj/DeepPaperNote/blob/4a7c066006cc4b6c75f21512128b8ec2891a8b53/LICENSE) | MIT | 保留来源，工作流重新编写；未纳入上游文件 |
| [math-literature-reader / 3d3a8c9](https://github.com/Ou-Liu-Red-Sugar/math-literature-reader/blob/3d3a8c9ce459f43ff9a60fe2ad43d85cc1a77caf/LICENSE) | MIT | 同上 |
| [math-paper-audit / 149b803](https://github.com/YijunYuan/math-paper-audit/blob/149b803c4f4d39028ca1b48bd9ce774cb11799e6/LICENSE) | Apache-2.0，并附[NOTICE](https://github.com/YijunYuan/math-paper-audit/blob/149b803c4f4d39028ca1b48bd9ce774cb11799e6/NOTICE) | 仅机制参考，未复制文件；后续若纳入其文件或改编作品，须另处理许可、修改标识和适用通知，不能只附本项目MIT |
| [paper-deep-reader / 4513c20](https://github.com/Linwei-Chen/paper-deep-reader-skill/blob/4513c20b4701c3096992110657a80e9413bcea16/LICENSE) | MIT | 保留来源，工作流重新编写；未纳入上游文件 |
| [codex-skills / a9bad38](https://github.com/yananlong/codex-skills/tree/a9bad384ae7e04eea38ab5efb13529ae4b664575) 中的两个research参考项目 | 所查根目录及两个项目目录未见明确许可证；授权状态未确认 | 仅保留链接和自行撰写的机制说明；不得将上游文件纳入分发，除非另行取得明确授权 |

上游声明和实际复用范围分别记录。本清单不声称已完成法律上的独创性鉴定，
也不将上游测试成绩或许可证归到本项目名下。未来复用文件时，须记录文件、版本、
许可、版权和通知，并重新检查分发清单。

## 图片、数学示例与PDF

`evals/fixtures/whitening.tex`是本项目自写的TikZ教学图源；
`evals/results/figures/whitening.pdf`及fixture中的同名图是它的派生物，内容相同。
`evals/results/applied-math.pdf`和`textbook-sample.pdf`是本地生成的限定范围教学样例，
不是原论文复印件。对应Markdown给出论文身份、来源和重建边界；不代表完整论文复现。

`evals/fixtures/first-year-depth/`中的代数教学单元及四份TikZ源为本项目自编，
同目录四份图形PDF由这些源生成，是保留的矢量测试资产，不是外部论文原图。
该单元只验证局部数学教学与构建，不认证任何加密方案；整篇测试PDF与编译中间文件留在忽略目录。

`skills/math-research-reader/assets/teaching/`中的四份TikZ源与同名矢量PDF也是本项目原创教学资产，
用于随包讲解示范的坐标对齐、复平面旋转、正交投影和误差方向；非论文原图。
它们适用下述字体嵌入范围，编译日志与测试整篇PDF不分发。

这些PDF含第三方字体子集。已核对本机TeX发行版中的字体许可：STIX Two Math和所用AMS/CM字体的
OFL许可、Fandol的GPL与字体嵌入例外、Latin Modern的GUST Font License。字体按其许可嵌入文档，
字体程序不因此改为MIT；本项目不分发原始字体文件。文档嵌入的规定另见
[OFL官方FAQ 1.10—1.14](https://openfontlicense.org/ofl-faq/)。提取字体后再次分发须遵守字体许可。

公开示例的数据是自编数学输入和本地复算结果，没有随包发布第三方训练集或原始实验数据集。
不得把原论文报告的数字标为本项目实际复现实验。

## 论文和私人资料的排除规则

- 外部论文、源TeX、原图截图、裁图和下载的参考文献不在当前公开清单中，仅存于忽略的本地缓存。
  公开文档保留论文链接、必要定位与自行撰写的分析。
- 完整精读测试所用[论文v2](https://arxiv.org/abs/2609.14379v2)标明
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。当前仍不分发其原件与裁图；
  未来单独发布带原图的教材时，须逐项署名、提供许可链接、标注裁剪或修改，不能仅标MIT。
  其他缓存论文未逐项确认再发布权，因此默认排除。
- 私人讲义、批注、逐字需求快照、原始文件名/哈希映射和未脱敏执行记录不公开。
  公开范例审阅只保留[匿名化设计摘要](docs/reference-report-review.md)。
- `.venv/`中的第三方库、可执行文件和附带数据不分发；它们各有独立许可。
  不可因项目根目录有MIT许可证就将整个虚拟环境重新许可。

本地忽略规则不是发布授权。打包时采用[发布检查清单](docs/release-readiness.md)，
不要直接压缩整个工作目录。新加入的第三方材料在确认授权前均须留在公开目录之外。
