---
name: repo-readme-skill
description: >
  开源仓库门面全套规范：按 GitHub 官方规则 + T0 级仓库（React/Vite/FastAPI/Ollama/ripgrep/
  PocketBase/Immich 等 12 个范本）两轮蒸馏的写法标准，审查或撰写 README、仓库 About 描述、topics、
  badges 与首屏视觉、social preview 分享卡、社区健康文件（CONTRIBUTING/CoC/SECURITY/FUNDING）、
  issue/PR 模板、releases 与 CHANGELOG、社区入口与 Discussions。凡用户提到 README 写法/改写/审查、
  仓库描述、repo 简介、topics 标签、badges、门面装饰、开源规范、准备开源、上架 GitHub、
  issue 模板、release notes 怎么写 —— 即使用户没说"规范"二字，也用本 skill。
---

# 仓库门面全套规范

把仓库的对外门面（README + About/topics + 装饰层 + 社区文件 + 模板 + 发布线 + 社区入口）按 T0 开源仓库的标准整治。

## 核心原则（先读懂再动手）

1. **README 是路由器不是百科**。T0 仓库的共识：README 只回答三件事——这是什么、值不值得用、
   30 分钟内怎么跑起来。所有深入内容路由到文档站、GUIDE.md、docs/ 目录。篇幅与文档站成反比：
   有 docs 站的 Vite/React 只有 3–5KB，无 docs 站的 ripgrep/fzf 才把 README 写成 20–40KB 的文档本体。
2. **三处描述一致**：GitHub About 字段 = README 首段 = 包管理器 description（npm/PyPI/crates）。
   standard-readme 要求短简介 < 120 字符，T0 实际范围 35–120 字符。
3. **诚实高于营销**。性能声明给基准链接（ripgrep 的对比表注明机器和"单一基准不够"），估算值加脚注
   （FastAPI 的 200%–300% 标注"internal team 估算"），未到 v1 的承诺写 WARNING（PocketBase、Immich 的备份提醒）。
4. **用户视角分段**。Pake 的 Getting Started 按"新手→开发者→高级用户→故障排查"四类人各给一条路。
   面向人的动线，不是面向模块的目录。

## 工作流

### 第一步：判定场景

用户要的是哪种？不确定就问一句。

- **A 审查/体检**：已有 README/门面，按标准打分并给修改清单 → 先跑 `scripts/audit.py`（有 gh 时加
  `--repo user/repo` 门面模式）拿硬指标，再读 `references/checklist.md` 逐条核对，
  产出「通过/问题（证据+改法）」报告。
- **B 撰写/重写**：从零写或大改 → 识别仓库类型，读 `references/templates.md` 对应模板起稿，
  首屏装饰层按 `references/facade-decor.md` §一–三，再过一遍 checklist。
- **C 门面装饰全套**：About/topics 文案、badges/hero/social preview、社区文件内容、issue/PR 模板、
  releases、社区入口 → 读 `references/description-topics.md`（About/topics）与
  `references/facade-decor.md`（其余全部），直接给可粘贴文案/配置。

### 第二步：识别仓库类型（选错模板全盘皆错）

| 类型 | 判定特征 | 结构基调 |
|---|---|---|
| 应用/自托管服务 | 有 Docker/部署章节，用户是运维者 | 功能表 + 部署 + demo 门票 |
| CLI 工具 | 装完在终端敲命令 | 安装(分平台) + 大量可复制示例 |
| 库/框架 | 发 npm/PyPI/Maven，用户写代码 import | 特性列表 + 最小可运行示例 + 文档链接 |
| 模型/AI 应用 | 模型名、prompt、agent | 快速启动 + API 示例 + 生态集成 |
| UI 组件库 | 组件、设计语言 | 环境支持 + install + usage + 全套链接 |

详见 `references/templates.md`。

### 第三步：产出

- 审查报告：每条问题附「证据（原文引用）→ 为什么违反 → 具体改法（给出改后文案）」。
- 新文档：直接给出完整可粘贴的 Markdown/描述文案，不要只给"建议加上 XX"。
- 中文项目的 README：默认双语策略——`README.md` 英文（standard-readme 规定英文占主名）+
  `README.zh-CN.md`，顶部互链（参考 Pake/Immich 的语言切换行）。用户明确只要中文时可用
  `README.md` 单文件中文，但 About 描述仍建议英文。

## 硬性规则（GitHub 官方，违反会实际出问题）

- 文件名 `README`（建议 `README.md`），放根目录 / `docs/` / `.github/`；同存时优先级 `.github` > 根 > `docs`
- 渲染超过 500 KiB 截断；链接用相对路径（绝对链接 clone 后会死）
- topics：仅小写字母/数字/连字符，单个 ≤ 50 字符，每仓库 ≤ 20 个；**私有仓库的 topics 也是公开的**
- 短简介（About 与 README 首段）< 120 字符，独占一行，不以 `> ` 开头
- README 超过 100 行应有目录（standard-readme）；GitHub 会按标题自动生成大纲
- social preview：PNG/JPG/GIF < 1 MB，至少 640×320（最佳 1280×640），Settings → Social preview 上传，仅公开仓库可分享
- FUNDING.yml 只在 `.github/` 生效，key 限 12 个白名单；组织 profile README 只在 `{org}/.github` 仓库的 `profile/README.md` 生效（根 README 不生效）
- API 陷阱：community profile 的 `files.issue_template` 对目录式模板恒为 null（须列 `.github/ISSUE_TEMPLATE/` 目录）；`files` 键恒在、值为 null 才是缺失；GitHub 会把 `{org}/.github` 回退文件计入 profile（以 html_url 判实际位置）

## 脚本检查（audit.py）

```bash
python ~/.agents/skills/repo-readme-skill/scripts/audit.py <README路径> [--desc "About描述"] [--name 包名]
# 门面模式（gh 已登录时）：实测 About/topics/社区文件(含组织回退)/issue模板/发布线/social preview
python ~/.agents/skills/repo-readme-skill/scripts/audit.py <README路径> --repo user/repo
```

输出 JSON：字数、首段长度、绝对链接、死链风险、`> `开头、缺失关键章节、badge 装饰层统计；
`--repo` 时另有 `facade` 段（health%、社区文件位置、issue 模板清单、tag 风格、最新 release、
social preview 判定）。审查场景先跑脚本拿硬指标，再人工按 checklist 深审。

## 范本索引

12 个 T0 范本对照表如下。本仓库版不随附语料快照（范本版权归各自项目）；需要离线对照原文时，
在仓库根目录跑 `python3 scripts/fetch_corpus.py` 重建到 `corpus/`（已 gitignore，勿再分发；
新版本同时抓取门面维度数据：community profile、.github 清单、issue 模板、FUNDING、最新 release）。

两轮蒸馏：第一轮（README/About/topics 结构与文案，产出 templates/description-topics）；
第二轮（2026-10-04，四车道并行实测门面装饰 82 条规则，产出 facade-decor.md——badges/hero/
social preview/社区文件内容/issue-PR 模板/releases-changelog/社区入口；完整观测证据随
开发记录归档，不在发布件中）。

| 范本 | 学什么 |
|---|---|
| Vite / React | 有文档站时的极简门面结构 |
| FastAPI | 特性卖点写法（动词开头+量化+脚注诚实） |
| Ollama | 分平台安装 + 三行跑通 + 模型生态 |
| ripgrep / fzf | 无文档站时 README 即文档 + 基准对比表 |
| PocketBase | 一句话特性列表 + WARNING 边界声明 |
| Immich | 功能矩阵表（功能×平台）+ demo 凭据 |
| Pake | 按用户角色分流 + 热门成品包展示 |
| ant-design | 组件库四件套（环境/安装/使用/链接） |

## 边界

- 代码本身的文档注释、API reference 生成、Wiki/文档站搭建不在本 skill 范围；README 只负责链接到它们。
- 不修改用户代码；只动门面文件：README/描述/topics、社区健康文件（LICENSE、CONTRIBUTING、
  CODE_OF_CONDUCT、SECURITY、FUNDING.yml）、issue/PR 模板、`.github/release.yml`、
  CHANGELOG 与 release notes 文案、组织/个人 profile README。
- CI workflow 本身的编写不在范围（只管 workflow badge 的挂法与 release.yml 的分区映射）；
  自动化工具（release-please/changesets 等）只做选型建议不做配置实施。
