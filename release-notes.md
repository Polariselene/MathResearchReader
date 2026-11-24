# MathResearchReader v0.3.1

这次预发布改进完整精读正文的写法，让读者从开头就知道这一章要回答什么，以及答案如何一步步得出。

## 本次改动

- 每章围绕一个读者问题。章和核心单元先给出带必要条件的答案，再按依赖顺序展开推导。初稿篇幅不足时，在原主线深化证明、算例和图解。
- 将补充的误解澄清、适用范围和反例收进单元末尾的「边界与反例」段。证明所需的前提及反例仍在用到的地方交代。
- 答疑优先写回原段落或边界段。属于另一问题的内容归入对应章节，或标明为章末补充。
- 在既有教学检查中分别验收可读性和论证逻辑，具体检查主线、开头结论及补充澄清的位置。

## 安装与使用

安装完整的 `skills/math-research-reader/` 目录后，用 `$math-research-reader` 发起精读、审查或恢复。[安装与使用](https://github.com/Polariselene/MathResearchReader/blob/v0.3.1/README.md)

## 验证与限制

- 55 项单测通过，1 项因 Windows 符号链接权限跳过。官方 Skill 校验通过。
- 本次验证覆盖规则和工具回归。整篇新教材的可读性待实际精读验证。
- 许可与材料来源详见 [THIRD_PARTY.md](https://github.com/Polariselene/MathResearchReader/blob/v0.3.1/THIRD_PARTY.md)。
