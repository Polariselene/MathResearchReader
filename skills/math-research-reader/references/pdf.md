# 中文 PDF 发布

Markdown 是唯一数学内容源；PDF 从声明顺序的 Markdown 自动生成，不能另外撰写一份。
脚本只构建，不替代数学核验或视觉QA。完整精读需PDF；专项审查仅明确要求时导出。
完整精读按[交付契约](delivery-contract.md)至少90页有效教学正文。
命令传`--full-read`，book.json写`task_mode=deep-read`；任一方式都会启用至少90个物理页的发布门槛。
构建器也读取`.mrr/state.json`与`.mrr/reading-plan.json`；其中`mode/task_mode=deep-read`或
`minimum_teaching_pages>=90`（可在delivery_contract内）会继承相同门槛；旧70/71页契约也继承当前90页要求。
state中`first_manuscript_status=planned/composing`会在整书编译前被阻止，正文及必要图示完成内容审阅后才设`content-reviewed`。
此状态不是质量认证，90页计数、至多10章及完整内容/版面验收仍需通过。
内部小型样张只在隔离目录验证字体、长公式和图形风格，不包含一份缩略整书，不作为估算还缺多少页的循环。
完整任务不能通过省略标志、换输出文件名或改用`--input`绕过；状态损坏须先修复，构建期间状态改变也停止发布。
独立专项/短导出使用独立任务工作区，不抹去全文任务契约。
另需Poppler `pdfinfo`，不在PATH时传`--pdfinfo <实际可执行文件>`；无法计数或不足时不替换最终文件。
门槛只核物理页数，有效正文和排版仍单独检查；普通export和专项不受此门槛影响。

## 环境与构建

需要 Python 3.10+（标准库）、Pandoc、XeLaTeX、ctex、中文与数学字体。
默认中文fontset=fandol、数学STIX Two Math；可用Noto Serif CJK SC或已确认的系统字体替换。
字体须实际编译验证。原论文解析另需宿主PDF工具，未捆绑解析器。

从 Skill 安装目录调用；root 指向单篇工作区，输入/输出使用其下相对路径：

```text
python scripts/build_pdf.py --root <论文工作区> --input report.md --input audit.md --output exports/report.zh-CN.pdf
```

多输入顺序即报告顺序。不需要audit时省略。已存在PDF需明确 --replace；输入Markdown和source目录
永不被此脚本改写。可用 --pandoc 与 --xelatex 指定可执行文件，--cjk-font 指定字体；
不自动下载安装。--check只诊断工具/ctex，不写文件；字体和排版以构建和视觉核查为准。

脚本在build中保留命令、退出码、日志、输入/模板哈希、工具版本、构建状态。
缺工具、缺输入、越界路径、编译失败、缺字会非零退出，不替换已有PDF。
新PDF构建后状态为built，visual_qa=unverified；核查记录另存.mrr/quality.json。

脚本采用Pandoc默认LaTeX模板+ctexart+随包header；中文A4、正文11pt、一级标题19pt，
有目录、页码、页眉、自动图表编号。Markdown图片caption加图号；
公式/定理保留原编号，显式锚点供交叉跳转，不让新编号冒充原文。

## 图与链接

原图标来源，自绘标教学示意。PDF嵌入PNG/JPEG/PDF等已确认格式；SVG/Mermaid先转换。
自绘数学教学图按[可视化规则](visualization.md)保留矢量，原文截图可用高分辨率栅格。
SVG/TikZ转换为PDF后检查仍为矢量；不以流程图或PNG包装替代数学拆解。
跨Markdown的链接如 audit.md#finding-1，在合并前的build派生副本
改为本PDF锚点，不能修改唯一正文源；脚本不会猜测跨文件链接目标。
跨库文件链接需明确本机可访问性，离开本机不能保证。

## 分章整书

长篇使用--book，不与--input混用。book.json只含元数据和实际收录的有序正文，不复制正文。
默认排除阅读说明/整书导航、独立练习/解答及研究启发；知识库文件不等于PDF收录清单。
短篇report.md若就是数学正文可收入；长篇report.md若只是导航则不收入，不按文件名盲删内容。
保留正常目录、正文教学算例以及与结论相连的假设/证据局限。示例：

```json
{
  "schema_version": 1,
  "task_mode": "deep-read",
  "title": "论文教科书级精读",
  "author": "读者笔记",
  "lang": "zh-CN",
  "chapters": [
    {"id": "background", "file": "chapters/background.md"},
    {"id": "proofs", "file": "chapters/proofs.md"},
    {"id": "audit", "file": "audit.md"}
  ]
}
```

```text
python scripts/build_pdf.py --root <论文工作区> --book book.json --full-read --output exports/book.zh-CN.pdf
```

chapter id必须唯一且为小写字母开头的字母/数字/连字符；章节文件存在且不重复。
用Pandoc实际解析每章Markdown，再在build派生AST里给锚点加章节前缀，改写章间
`background.md#definition`及章内`#definition`链接，按章节目录解析图片路径。
不同章可有同名标题；同章重复显式锚点、未知目标、遗漏链接章、越界资源会阻止导出。
图片先在知识库落地，不在编译时自动下载。源Markdown及作者定理/公式编号保持不变。
精确对象建议显式锚点；原始LaTeX中的手工label/ref不经过Markdown AST命名空间，需另核唯一性。

PDF正文不链接仅存于Markdown的导航/额外练习等文件来完成必要论证：
必要说明改写在正文正确位置，来源反查链接到实际收录的对象；外部知识库入口留给交付消息。
构建器不会按标题自动筛掉内容，先由写作者审查清单和正文边界；漏收数学依赖或误收附属材料
都须修正后再构建，不靠静默忽略缺失链接通过验收。--input也先审查实际收录范围。

完整精读至多10个可见主章，无页数上限，有90页有效正文下限。长篇先逐单元充分写作并验收，再合并做整书检查；构建成功和百页输出都不证明
教学深度或数学正确。--input保持原有轻量路线；需要自动章间链接时选--book。
复杂长篇可用--timeout调整单次编译时限（默认600秒，范围1–3600），超时保留失败记录，
不将其转化为削减数学正文的理由。
长时间构建结束再次核对Markdown、book.json和模板哈希；源或既有输出期间变化则停止发布，
保留用户/其他写入者的版本，防止把旧检查绑定到新内容。

## 每次导出检查

默认先完成正文，只做一次小型版式样张和最终整书构建；不为每个章节编译阶段稿。
最终仍逐页查看，可批量渲染接触表后放大密集/可疑页；所有页均要实际看，不能只看抽样。
修复后比较实际渲染与内容变化，只复查改变的页面及相关链接/页码，不因一个局部修改无故重复整书视觉输入。

先核实际PDF不存在被移出的阅读说明、练习解答或研究启发（也不能改名藏入附录），
必要教学内容未丢、正文章号连续。再检查日志及所有渲染页：中文乱码/缺字；公式完整；上下标/分数/矩阵；图片；表格溢出；
目录页码；书目与内部链接；意外空页/截断。含链接需实际核目标，不能只看蓝色文字。
用pdftoppm或可用渲染器逐页出图，实际检查；提取文本不能证明版式正确。
发现问题修复Markdown/模板后重建；无法修复标PDF交付未完成。
缺依赖时可交付Markdown，但不能宣布完整精读交付成功。
一致再生成指内容与引用一致，非含时间戳PDF的字节完全相等。
