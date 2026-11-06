# README 功能与命令验证

日期：2026-11-06。范围为项目根README的功能描述、安装方法、对话示例与PDF命令。
没有更改Skill规则或构建器，没有安装系统依赖、写入真实用户技能目录、初始化Git或上传。

## 功能描述核对

逐项对照SKILL.md、agents/openai.yaml以及数学教学、成稿、知识库、PDF、文献关联和Lean规则，
并核对build_pdf.py实际参数和行为。README明确区分由Codex执行的阅读工作流与仅接受Markdown的构建脚本。
保留最新PDF收录边界、完整精读与专项审查的不同默认交付、依赖宿主的全文获取/OCR/视觉能力，
没有把可选Lean规则写成内置形式化工具，没有将局部测试写成独立数学认证或最新整书验收。

安装路径、技能发现与显式调用已搜索并实际打开[OpenAI官方技能文档](https://learn.chatgpt.com/docs/build-skills)核对。
README给出本地完整目录复制方法，没有构造未发布的包名、GitHub克隆地址或市场安装命令。

## 实际执行

从最终README提取PowerShell代码块以及Markdown/JSON样例，在被忽略的
`.local-test/readme-verification-7153c4e2/`内建立隔离项目，执行原代码块。
测试没有改写示例命令的参数；为满足README声明的PATH前提，将已有Pandoc所在目录临时加入测试进程PATH。
系统Python和TeX已经可用，未下载安装。具体命令、工具位置与manifest定位见
[原始检查记录](readme-command-checks.json)。

| 检查 | 实际结果 |
|---|---|
| 项目级目录安装 | 执行复制代码块，返回True；目标文件逐个与源文件核对SHA-256一致 |
| 重复安装 | 再执行同一代码块，命中目标已存在保护，未覆盖 |
| `--help` | 与README使用的参数一致 |
| `--check` | 返回tools-available和font_check=requires-build |
| `--input report.md` | 构建成功，生成1页中文数学测试PDF |
| `--book book.json` | 构建成功，生成1页带书名的中文数学测试PDF |
| 已存在PDF保护 | 重复输出被拒绝，退出码1，旧PDF哈希未改变 |
| 构建状态 | 两份manifest均为built，visual_qa仍为unverified；不把构建器当视觉验收器 |
| 页面检查 | 两份PDF均渲染并实际查看全部页面；中文、矩阵、上下标和目录无可见缺陷；独立检查记录绑定文件和渲染图哈希 |
| 官方quick_validate | 对隔离安装后的Skill运行，返回Skill is valid! |
| README单元测试命令 | 本轮已在真实项目根执行：22项中21项通过，1项因OS符号链接权限跳过；没有重复运行 |
| 本地链接 | 用Pandoc解析最终README，检查实际本地链接目标存在；外部技能文档另由网页实际核对 |

## 验证边界

安装验证证明复制命令和目录结构有效，没有在新Codex会话中测试界面发现，也没有实际写入用户级目录；
用户级路径依据官方文档。只提供已在Windows/PowerShell环境执行的安装代码，未给未经测试的其他平台命令。

PDF仅为README最小导出例，不能证明数学阅读、证明审计或长篇教学效果。没有重新执行一篇论文的完整精读，
没有更新旧83页教材，也没有验证修订版百页成稿。既有研究与教学验证仍保持其原有范围。
两份测试PDF和渲染图属于本地中间测试材料，不作为项目对外示例教材分发。
