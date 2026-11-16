# MathResearchReader v0.3.0

问题链教学、正文回写与重复开销约束更新，作为早期Pre-release发布。

## 本次改动

- 主章及核心单元由driving_question驱动，明确自然尝试、失败点、论文方法、效果和剩余缺口；新增八项必写动作、讲解降级及问题链自检。
- 有效正文优先承重推导，弱相关先修证明不计页；保留至少90页、至多10章、首次完整教材成稿的要求。
- 交付前先核债务登记完整性，再按问答锚点取片段、原位回写正文；未清零不得标记内容已审阅或完整交付。
- 统一context_ledger及14项开销约束，合并重复检查与记账；保留必要证据取回、全部页实际目视及必要修复复检。
- 排除本地reading-work目录并更新使用说明；既有PDF缓存、构建脚本和调用方式不变。

## 安装与使用

按[README](https://github.com/Polariselene/MathResearchReader/blob/v0.3.0/README.md)安装完整的skills/math-research-reader目录，使用`$math-research-reader`发起精读、审查或恢复。
原有Python/Pandoc/XeLaTeX/Poppler依赖不变，不自动安装工具。

## 验证与限制

- 56项单测：55通过，1项因Windows符号链接权限跳过；官方Skill校验通过。
- 本次主要是执行规则更新，没有新增自动台账、债务判定或用量监控程序；没有新教材对照实验或账户token测量，不承诺固定省额比例或教学效果。
- 跨平台与复杂OCR/TeX兼容性尚未全面验证，不认证数学正确性。MIT及第三方边界见[THIRD_PARTY.md](https://github.com/Polariselene/MathResearchReader/blob/v0.3.0/THIRD_PARTY.md)。

保留v0.1.0和v0.2.0，不覆盖旧标签；不附私人论文、阅读产物、依赖环境或额外附件。
