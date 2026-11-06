# 知识库与恢复

默认当前工作区 MathResearchReader-Library/，用户路径优先。不静默写个人Vault，不覆盖原稿或用户修改。
稳定paper-id绑定明确版本；按实际任务创建所需文件，不创建空壳目录。

```text
MathResearchReader-Library/
  index.md
  concepts/                         # 实际复用才创建
  comparisons/                      # 实际比较才创建
  papers/<paper-id>/
    paper.json                      # 身份、来源、版本、哈希
    source/                         # 原始受保护副本
    report.md                       # 精读唯一数学正文
    chapters/                       # 长篇时唯一分章正文，report改为导读
    book.json                       # 实际进入PDF的有序正文清单与元数据；不含导航/额外练习
    audit.md                        # 审计发现唯一正文
    figures/                        # 原图/教学图及来源
    .mrr/
      objects.json
      reading-plan.json             # 写作前主线、主张证据与章节计划
      audit.json                    # 需要审计时的范围、六轮与发现状态
      dependencies.json
      state.json
      quality.json
      checkpoints/<id>.md
    build/                          # 派生物、日志
    exports/report.zh-CN.pdf
```

专项可只有audit.md，局部追问不强制全库。大论文可拆Markdown章节按顺序传构建器，
对象索引链接唯一正文锚点，不在卡片/报告/JSON维护多份独立证明。
使用标准相对链接、稳定显式锚点、LaTeX数学。

JSON为UTF-8，顶层schema_version=1；字段允许扩展，未知用null/unverified：

| 文件 | 最小字段 |
|---|---|
| paper.json | paper_id,title,authors,version,identifiers,sources[{file,url,sha256}] |
| objects.json | objects[{id,type,original_label,locator,core,core_reason,read,explained,audited,note_anchor,omission_reason}] |
| dependencies.json | edges[{from,to,used_result,hypothesis_mapping,evidence,status}]；依赖项→使用者 |
| state.json | mode,scope,profiles,stage,completed_objects,next_action,open_issues,checkpoint,source_hashes,note_hashes,status |
| quality.json | checks[{id,scope,applicable,status,evidence,reason}] |

reading-plan.json按 [成稿规则](synthesis.md)；audit.json按 [审计规则](proof-audit.md)。
dependencies边额外记录origin=explicit/reconstructed及原文证据，不把模型推断伪装成作者引用。
state记录当前reading_unit、已加载宏索引/约定表、visual_mode、output_language和实际未决项。
按需在对象中增claim_kind，并索引近似转换、算法状态/不变量与误差依赖到唯一正文；
源附录重排映射、符号/等价类约定保存为导航，不为它们另存完整正文副本。
用户另行要求的练习/研究建议可单独保存，默认不加入book.json；教学算例仍留在唯一正文中。
quality中的文件检查保存reviewed_hashes，交付前比对真实文件，不能只写一个脱离版本的pass。

定位按 [证据规则](evidence.md)，提取不等于理解。每阶段与中断前保存已读范围、约定、
完成对象、未闭合证明、不可访问依赖、发现、产物、下一具体行动。临时文件原子替换状态，
保留上一checkpoint。

恢复读paper/state/checkpoint及相关源，比对源与笔记哈希。源/定义/假设/引理改变让下游失效；
只改样式通常只重做PDF与QA。保留用户修改并重新核对，不为恢复而覆盖。
状态损坏从源和checkpoint重建并披露不确定性，不直接继承旧通过状态。
状态值in-progress/blocked/reviewed-with-open-issues/complete-for-declared-scope。
审计报告完成不代表定理通过；完整精读需全范围覆盖和所需交付。

长篇state另存chapter_id、unit_id、chapter_statuses、接口依赖、尚未完成对象、下次具体目标，
和被逐出上下文但可以重新打开的源片段位置。切换主题、完成单元、上下文紧张时保存checkpoint；
始终保存非平凡约定转换、未决条件、活动依赖及用户符号选择。顶层index只放导航，
不把全部论文内容塞入自动加载记忆。精确主张恢复后重载源。

知识概念复用分create/enrich/reuse：不存在才新建，已有定义只补缺失内容和本篇使用记录；
同名异义、别名冲突或前提不同则建区分/转换记录，不自动覆盖旧定义。
后文引用记录其所属定义/版本、原位置与当前用途，不因概念库条目存在就当本论文假设已满足。
