# README / 仓库门面审查清单

用法：先跑 `scripts/audit.py`（门面模式加 `--repo user/repo`）拿硬指标，再按本清单逐条人工核对。报告格式：每条给
「✅ 通过 / ❌ 问题 + 证据（引用原文）+ 具体改法（写出改后文案）」。

## A. 仓库元信息层（有 GitHub API 时核对，无 API 时向用户要描述原文）

| # | 检查项 | 标准 | 范本依据 |
|---|---|---|---|
| A1 | About 描述存在且 ≤ 120 字符 | 含品类名词 + 差异化定语 | 全部 12 范本 |
| A2 | 三处一致：About = README 首段 = 包管理器 description | 逐字一致（语言可异） | standard-readme |
| A3 | topics 4–20 个，小写连字符 | 覆盖自身名/语言/品类/领域/生态五层中至少四层 | description-topics.md |
| A4 | homepage 已填且指向文档/官网 | 留空优于乱填 | 全部范本 |
| A5 | License 文件存在且 README 有 License 章节 | SPDX 名称 + 相对链接 | GitHub Community Profile |
| A6 | CONTRIBUTING / CODE_OF_CONDUCT / SECURITY 存在性（含 `{org}/.github` 回退） | 至少 CONTRIBUTING；缺失就在报告里提；内容级标准见 F 段 | Community Profile 检查项 |

## B. 首屏（第一屏决定去留）

| # | 检查项 | 标准 |
|---|---|---|
| B1 | 一句话说清「这是什么」 | 读者不需要点进文档就知道品类 |
| B2 | badges 真实且带链接 | 4–6 个：CI、版本、license、社区；无死链 badge；装饰层细标准见 E1 | 
| B3 | 有产品形态视觉物 | 截图/GIF/logo；CLI 至少给终端示例块；按类型分派细标准见 E3 |
| B4 | 首屏无长篇大论 | 前言 ≤ 3 段，深入内容路由出去 |

## C. 结构与内容

| # | 检查项 | 标准 |
|---|---|---|
| C1 | 核心章节齐全 | 安装/上手示例/文档链接/贡献/license 按仓库类型核对（见 templates.md） |
| C2 | 安装命令可复制执行 | 按平台分节；含包管理器 + 二进制 + 源码三种方式（CLI 类） |
| C3 | Usage 示例最小可跑 | < 20 行、有预期输出说明 |
| C4 | README 超 100 行有目录 | 至少覆盖二级标题 |
| C5 | 功能描述扫读友好 | 表格或 **加粗词**: 说明 的 bullet，不是散文段落 |
| C6 | 链接健康 | 相对路径在仓库内真实存在；外链 https；无「TODO」占位 |
| C7 | 性能/数字声明有出处 | 基准表注明环境，估算值有脚注 |
| C8 | 风险边界声明 | 数据安全/兼容性用 `> [!WARNING]`/`[!NOTE]`；未到 v1 明说 |

## D. 语气与措辞（T0 反例驱动的负面清单）

| # | 检查项 | 标准 |
|---|---|---|
| D1 | 无空洞形容词 | 禁「强大的/革命性的/best/revolutionary」——特性靠机制说明 |
| D2 | 无营销腔 | 「open source」不写在描述里（开源是默认假设）；团队自夸句删除 |
| D3 | 面向用户动线不面向模块 | Getting Started 按角色/场景分流（Pake 式），不按代码结构 |
| D4 | 中文项目的语言策略 | 英文为主：README.md 英文 + README.zh-CN.md 互链，About 英文；中文为主：README.md 中文 + README.en.md 互链，About「中文主句（English gloss）」 |

## E. 装饰层：badges 与首屏视觉（依据 facade-decor.md §一–三）

| # | 检查项 | 标准 | 范本依据 |
|---|---|---|---|
| E1 | badge 质量 | 全部包链接（41/41 无裸图）；样式全 README 统一；单行 ≤6，超出拆健康度/社区两行；vanity 不排在 CI/版本前 | 9 仓 41 badge 观测 |
| E2 | hero 结构 | 居中模板：logo（带尺寸、包官网链接）→ 标题 → 一句话（前 10 行内必现）→ badge 行 | 7/10 居中 hero |
| E3 | 视觉资产按类型分派 | 纯库不硬凑截图（logo+代码即视觉）；CLI 首屏终端 PNG；应用/组件库首屏主截图；安装型给终端块 | 3/3 库零截图 |
| E4 | social preview 已设 | 1280×640 PNG <1MB；Settings → Social preview；og:image 域名二分可外部验证 | 6/10 已设 + 官方规则 |

## F. 社区健康文件内容级（依据 facade-decor.md §四；存在性在 A6）

| # | 检查项 | 标准 | 范本依据 |
|---|---|---|---|
| F1 | CONTRIBUTING 内容 | root 位置；全量型骨架（找任务→setup→测试→PR 规范）；<50 词指针必须带可点击链接 | 7/7 在 root |
| F2 | CoC 内容 | Contributor Covenant ≥2.0 全文零自撰，落款保留版本行 | 4/4 全 Covenant |
| F3 | SECURITY 私密渠道 | `/security` 链接或专属安全邮箱 +「勿开公开 issue」；私密报告开关已开；外部白帽页/赏金平台也算合法渠道 | 7/8 开私密报告 |
| F4 | FUNDING 规范 | `.github/FUNDING.yml`；key ∈ 12 白名单；含 `:` 的 custom URL 加引号 | 官方 + 4/8 |
| F5 | org 回退已排除 | 判缺失前查 `{org}/.github`（root 与 .github/ 两处）；profile 值的 html_url 判实际位置 | 3/8 组织在用 |

## G. issue / PR 模板（依据 facade-decor.md §五）

| # | 检查项 | 标准 | 范本依据 |
|---|---|---|---|
| G1 | .github 门面最小集 | `ISSUE_TEMPLATE/`（含 config.yml）+ `workflows/`；PR 模板 `.github/PULL_REQUEST_TEMPLATE.md` | 8/8 / 6/8 生效 |
| G2 | bug 模板质量 | YAML issue forms（非 markdown）；必填四件套：描述/复现/版本/环境；环境给生成命令或 dropdown | 5/7 forms |
| G3 | config.yml 分流 | blank_issues_enabled 有人力分诊 false / 宽进 true；contact_links 至少分流问答（Discussions/Discord/论坛） | 8/8 有 config |
| G4 | PR 模板质量 | 四节：Summary(Fixes #)/验证方式/Related Issue/checklist 3–9 项；UI 项目留截图位；2025+ 加 AI 披露条款 | 3 家完全符合 |
| G5 | 无空壳模板 | frontmatter-only 零正文的模板 = 反模式（引流或删掉）；双语仓库给双语模板 | ollama 反例 |

## H. 发布与 CHANGELOG（依据 facade-decor.md §六）

| # | 检查项 | 标准 | 范本依据 |
|---|---|---|---|
| H1 | tag 规范 | 小写 `v`+semver 全仓库一致（含预发布渠道）；杂渠道用 `v0.0.0-` 前缀防污染 latest | 8/10 |
| H2 | release 标题与 notes | 标题默认 = tag；notes 手写 highlights：一句话主题→分节→逐条 issue/PR 链接+作者；自动路线配 `.github/release.yml` | 8/10 手写 |
| H3 | prerelease 渠道 | beta/rc/canary 全标 prerelease:true 保护 latest 指稳定版 | vite/immich/lobe-chat |
| H4 | CHANGELOG 同源 | 有文件（7/10）则与 notes 同源同文 + 逐版本 compare 链接；monorepo 放主包目录；**别默认 Keep a Changelog**（0/10） | 10 仓观测 |
| H5 | 资产策略 | 按「是否分发二进制」判定：终端产品附多平台资产+校验和（Rust target-triple+.sha256 / GOOS_GOARCH+checksums.txt / 桌面全家桶）；库 0 资产；部署型挂 compose/env | 6/10 vs 4/10 |

## I. 社区入口与仓库开关（依据 facade-decor.md §七）

| # | 检查项 | 标准 | 范本依据 |
|---|---|---|---|
| I1 | 社区入口档位 L0–L3 | L0 无链接不扣分 → L1 顶部 Discord badge → L2 专门章节 → L3 开 Discussions；加分项非必需 | 4/10 完全无链接 |
| I2 | has_discussions | 默认开（8/10）；开了就要配分类与问答分流链接；有外置社区载体可关 | 8/10 |
| I3 | 组织/个人 profile README | 组织生效位是 `{org}/.github` 的 **profile/README.md**（根 README 不生效）；个人用 `user/user` 仓库 | 3/7 组织 |

## 报告模板

```markdown
# 仓库文档体检报告：<repo>

## 总评
（一句话：当前处于什么水平，最要紧的 3 件事）

## 元信息（A）
- A1 ❌ 描述 158 字符超限。现文：「...」
  → 改为：「<120 字符新文案（含品类词+差异化）」

## 首屏（B） / 结构（C） / 措辞（D）
（同上格式：编号、判定、证据、改法）

## 装饰层（E） / 社区文件（F） / 模板（G） / 发布（H） / 社区入口（I）
（同上格式；audit.py --repo 的 facade 段输出可直接引用为 A/E/F/G/H 的机器证据）

## 修改优先级
P0 = 阻断读者上手；P1 = 明显减分；P2 = 锦上添花
```
