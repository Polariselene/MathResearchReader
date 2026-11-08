# 知识库与恢复

默认当前工作区 MathResearchReader-Library/，用户路径优先。不静默写个人Vault，不覆盖原稿或用户修改。
稳定paper-id绑定明确版本；按实际任务创建所需文件，不创建空壳目录。

## 首次创建与保存

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
| state.json | mode,scope,profiles,stage,completed_objects,next_action,open_issues,checkpoint,source_hashes,note_hashes,status；状态为in-progress/blocked/reviewed-with-open-issues/complete-for-declared-scope |
| quality.json | checks[{id,scope,applicable,status,evidence,reason}] |

reading-plan按[成稿规则](synthesis.md)，audit按[审计规则](proof-audit.md)。以下记录各有唯一归属，
其他文件引用ID/锚点，不复制证明、算例、提取文本或同义章节总结：

| 归属 | 保留内容 |
|---|---|
| reading-plan | 全文对象到至多10主章的课程蓝图、教学/图解义务、各章工作量；分批文件不等于新章 |
| state | reading_unit、chapter_id/unit_id、chapter_statuses、活动队列/已完成锚点、teaching_debt及补写位置、next_action、真实blocked_reason和open_issues |
| state的上下文 | 读者reader_profile、宏/符号/等价类约定索引、接口依赖、已加载规则/逐出源位置、visual_mode、output_language、source_cache配置/索引/哈希；skill_snapshot用实际版本或文件哈希，未知不编造 |
| objects | 每个核心对象的teaching或等价证据：prerequisite_bridge、worked_example、proof_steps、boundary、visual_explanation各有正文锚点、pass/fail/unverified及不适用理由；按需增claim_kind、近似/算法不变量/误差到正文的索引 |
| dependencies | origin=explicit/reconstructed、原文证据及逐项假设映射；不把推断伪装成作者引用 |
| quality | coverage与depth分别给证据，物理/有效正文页范围和计数、reviewed_hashes；旧explained布尔值不推出深度通过 |

完整精读首次建state/plan即标`mode=deep-read`及90页契约、maximum_reader_chapters=10，
从当前原论文重建，不依赖旧产物；按百页级课程展开，不以90页计数驱动写作。
`first_manuscript_status=planned/composing/content-reviewed`只在state维护，全部正文/必要图示内容审阅后才进入末态。
任一页数或其他交付门槛未过不能记完整交付；普通导出继承全文模式。独立专项片段另用明确范围工作区，保留全文状态。

按完整单元批量更新索引和checkpoint，用户笔记修改或强制中断前及时保存；checkpoint后继续队列。
难章校准保留具体理解问题、正文依据和修订位置。实质用户反馈记reader_feedback并打开相关teaching_debt，
使相应教学检查失效；缺口修回正文，不能只留qa/聊天。条件改变仅重开受影响单元。

内部unit/文件不成为读者标题；可用`[已有正文]{#unit-id}`定位补写。源附录重排与约定转换只建导航索引。
[来源缓存](source-reading.md#pdf本地缓存与定量取页)不复制到state；已逐出材料需重新加载真实片段，曾经loaded不等于现在已掌握。
默认只加载活动恢复包，历史checkpoint留供追溯；用户另要的练习/研究建议单存且默认不进book，教学算例仍留正文。

定位按[证据规则](evidence.md)，提取不等于理解。阶段/中断前记录已读范围、约定、完成对象、
未闭合证明、不可访问依赖、发现、产物和下一行动；状态原子替换，保留上一checkpoint。

切换主题、完成单元或上下文紧张时保存checkpoint，含非平凡约定转换、未决条件、活动依赖和用户符号选择。
顶层index只导航，不把全文塞入自动记忆；恢复精确主张须重载源，并核交付文件与已查哈希一致。

## 恢复既有阅读

定位用户指定的单篇工作区；本节配合paper.json、state.json和活动checkpoint即可开始，不先重读建库规范。
核版本、源/笔记/相关规则哈希与用户修改，再加载活动单元、所用定义/约定、未决条件和完整必要源片段。
索引/摘要只导航，不用过去loaded/read/pass代替当前证据；不全量回读对象JSON、旧checkpoint或整书。
规则变化只复核受影响义务；结构/字段缺失或任务转为新建才查前节及相关规范。
源/定义/假设/引理改变让下游失效；
只改样式通常只重做PDF与QA。保留用户修改并重新核对，不为恢复而覆盖。
状态损坏从源和checkpoint重建并披露不确定性，不直接继承旧通过状态。
审计报告完成不代表定理通过；完整精读需全范围覆盖和所需交付。

恢复后直接继续next_action或当前追问，保存实质更新；不重建未变计划，也不把恢复成功当整书完成。

## 复用概念

知识概念复用分create/enrich/reuse：不存在才新建，已有定义只补缺失内容和本篇使用记录；
同名异义、别名冲突或前提不同则建区分/转换记录，不自动覆盖旧定义。
后文引用记录其所属定义/版本、原位置与当前用途，不因概念库条目存在就当本论文假设已满足。
