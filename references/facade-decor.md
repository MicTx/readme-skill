# 门面装饰标准：badges / 视觉 / 社区文件 / 模板 / 发布 / 社区入口

> 来源：2026-10-04 第二轮蒸馏——四条车道实测 12 个 T0 范本（每维度 8–10 个），共 82 条规则。
> 完整原始观测表与逐条证据随开发记录归档（2026-10-04 任务包 notes/，四条车道各一份，不在发布件中）。
> 证据标注：[官方] GitHub 官方文档规则（附链接）/ [共识] ≥5 范本同做法 / [分布] 2–4 范本 / [个例] 单范本。

## 〇、总览：三层套餐与装饰顺序

| 层 | 内容 | 范本覆盖 | 说明 |
|---|---|---|---|
| 标配层 | README、LICENSE、CONTRIBUTING、SECURITY | 8/8 或 7/8 | 缺了就是硬伤 |
| 信任层 | CoC、私密漏洞报告开关、issue/PR 模板 | 4–6/8 | 拿满 Community Profile 分（如 react/transformers 的 100%）需要这层齐备 |
| 资助层 | FUNDING.yml（Sponsor 按钮） | 4/8 | 分水岭，按需 |

装饰优先级（时间有限先做上面的）：**issue 模板 > PR 模板 > 首屏 hero/badges > social preview > FUNDING**。[共识]

冷启动降级：新仓库 0 release / 无模板 / 无 CI 时，对应检查项记「首版发布前适用外」，不算问题；先做 标配层 + bug 模板，发布第一个 tag 后再补发布线装饰。

私有仓库注意：social preview 仅公开仓库可对外分享；og:image 外部验证法与部分 gh api 检查在私有仓库上不适用（无权限即跳过，别误报）。

---

## 一、badges

| # | 规则 | 证据 |
|---|---|---|
| 1 | 每个 badge 必须包链接 `[![alt](img)](target)`；41/41 范本 badge 无一裸图 | [共识 9/9] |
| 2 | shields 样式全 README 统一，首选默认 flat；要品牌感用 flat-square+logo；零混用、不用 social 样式 | [共识 9/9] |
| 3 | 单行 4–6 个；超过就拆两行：行1 项目健康度（CI/覆盖率/版本/下载量），行2 社区（twitter/license/help） | [共识+分布] |
| 4 | CI badge 第一公民（8/9 有，5 家放行首），链接指 workflow 文件本身；无 CI 不摆 CI badge | [共识] |
| 5 | 版本 badge 用包管理器官方源（npm/v、pypi/v、crates/v），紧跟 CI | [共识 7/9] |
| 6 | license badge 或正文文字声明二选一，至少其一（badge 4/9，正文文字 5/9） | [分布] |
| 7 | vanity badge（stars/contributors/sponsors/下载量）不进第一梯队：组织项目 ≤2 个放尾部；个人项目可整行 | [共识] |
| 8 | 不做「官网 badge」（0/10）——官网入口由 logo 链接或文字行承担 | [共识 0/10] |
| 9 | badge 非强制项：没有真实可链接的状态就不摆（ollama 零 badge 靠 logo+终端块撑首屏） | [个例] |

按仓库类型的推荐组合（顺序即排列顺序）：

- **库/框架**：CI → 版本(npm/pypi/crates) → license → （chat 可选）
- **CLI 工具**：CI → 版本 → license → 打包数（repology）
- **应用/自托管**：license → discord → （CI/版本可选）
- **AI 应用**：CI → 版本 → 模型生态 badge（可省）

badge lint 五连（audit.py 可机检）：裸 badge、死链 workflow badge、样式混用、单行 >6、vanity 排在 CI/版本之前。

---

## 二、首屏 hero 与视觉资产

hero 默认抄居中模板（7/10 范本形态）：

```html
<p align="center">
  <picture>                              <!-- 深浅色自适应，SVG 首选 [个例: vite] -->
    <source media="(prefers-color-scheme: dark)" srcset="docs/logo-dark.svg">
    <img src="docs/logo.svg" height="80" alt="ProjName">
  </picture>
</p>
<h3 align="center">一句话简介（与 About 一致，前 10 行内必现，10/10）</h3>
<p align="center">[badge 行]</p>
```

| # | 规则 | 证据 |
|---|---|---|
| 1 | 居中实现：`<p align="center">`（badge/单图）或 `<div align="center">`（多元素整包）；左对齐变体（标题行内嵌 badge）仅老牌项目在用 | [共识 7/10] |
| 2 | logo 尺寸显式带单位：横版 height 60–180，竖版 width ≤300（观测：60/138/180/200/300） | [分布 5 家] |
| 3 | logo 包官网链接（vite/fastapi/ollama/immich 都这么做）；无 logo 用全宽 banner 代替（pocketbase） | [分布] |
| 4 | 一句话简介必须在前 10 行——badge 行之外唯一不可省的首屏元素 | [共识 10/10] |
| 5 | 双语仓库的语言切换行放 badge 附近（右上角或快捷链接行） | [分布 2/10] |

截图策略按仓库类型分派（不要一刀切「都要截图」）：

| 仓库类型 | 首屏视觉 | 证据 |
|---|---|---|
| 纯库/框架 | **不硬凑截图**：logo + 首屏代码示例（react）/ emoji 特性列表（vite）/ 文档链接（fastapi） | [共识 3/3 零截图] |
| CLI 工具 | 终端运行 PNG 1 张放首屏（width=640 通用），风格截图组与视频 Demo 放后文小节 | [共识 2/2] |
| 应用/组件库 | 主截图或截图网格放首屏；GIF 演示放后文 | [分布 3/3] |
| AI/安装型 | 无图时用首屏终端示例块替代（安装命令 code fence） | [个例 ollama] |

截图统一包链接（指向 demo/官网/原图，4/5 范本如此）。图片托管求稳定即可；仓库内相对路径（`design/`）最抗外链失效。GIF 少用（仅 1/10 范本在后文放 GIF）。

---

## 三、social preview（分享卡）

[官方](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview)：

- 格式 PNG/JPG/GIF，**<1 MB**；至少 640×320，**最佳 1280×640（2:1）**；支持透明 PNG（注意深色模式平台）。
- 设置：仓库 **Settings → Social preview → Edit → Upload an image**（需仓库管理权限）。
- 仅公开仓库可上传并对外分享；不上传时默认展示仓库信息 + 所有者头像。
- og:image:alt 与 About 描述同源——About 写好，分享卡自动受益。

外部验证法（无需登录）：`curl -sL https://github.com/OWNER/REPO | grep -o 'property="og:image" content="[^"]*"'`——
域名是 `repository-images.githubusercontent.com` = 已设自定义图（范本 6/10 已设）；是 `opengraph.githubassets.com` = 未设（默认动态卡）。README hero 的 logo/截图资产可与 social preview 复用一套。

---

## 四、社区健康文件（内容级标准）

### CONTRIBUTING.md

| # | 规则 | 证据 |
|---|---|---|
| 1 | 放仓库 **root**（7/7 有文件的范本全在 root，0 个在 .github/ 或 docs/） | [共识] |
| 2 | 全量型骨架顺序：`# Contributing to X` 欢迎语 → 找任务/issue 筛选 → 本地 setup（环境+命令）→ 测试 → PR 规范；维护型内容（triage/release）放最后 | [共识 5/5 有 setup，4/5 有 issue 筛选] |
| 3 | 有文档站的大项目允许 <50 词短指针，但**必须含可点击链接**（react 28 词带链接 ✅；fastapi 9 词纯文字是反例） | [分布] |
| 4 | 「链接 CoC」不是必选项（6 个范本仅 1 个链了） | [共识反向] |
| 5 | 多仓库组织：CONTRIBUTING 放 `{org}/.github` 共享（或仓库内留 root 短指针），别每仓复制 | [分布 3/8] |

### CODE_OF_CONDUCT.md

- 直接用 **Contributor Covenant 全文，零自撰**（4/4）[共识]；版本选 ≥2.0（现行 2.1）[分布]。
- 保留完整文本不删节（v2.x ≈ 710–720 词），落款保留 "adapted from the Contributor Covenant, version X" 便于机器识别 [共识]。
- 位置：单仓库 root；组织共享放 `{org}/.github` root [分布]。

### SECURITY.md

| # | 规则 | 证据 |
|---|---|---|
| 1 | 必备「上报漏洞」章节并指明**私密渠道**：开 GitHub 私密报告（7/8 开启，`repos/{o}/{r}/private-vulnerability-reporting` 可查）并写 `/security` 链接，或专属安全邮箱；写明「不要开公开 issue」 | [共识] |
| 2 | 版本支持**不用** markdown 表（0/8！GitHub 官方模板有但范本无人用）：一句话「只支持最新版」或指向 Releases 页 | [共识反向] |
| 3 | 响应时效只做软承诺（"within a few weeks"），不写硬 SLA | [分布 2/8] |
| 4 | 写 out-of-scope 范围界定能显著降低无效报告（vite 威胁模型 / immich 8 条 Scope） | [分布 4/8] |
| 5 | 2025+ 新趋势：AI 报告政策（要求人工验证复现、拒绝批量提交） | [分布 3/8] |
| 6 | 有独立域名可加 `.well-known/security.txt` | [分布 2/8] |
| 7 | 位置 root 或 .github/ 均可；SECURITY.md **不计入** community profile 分数 | [官方+共识] |

注意：合法的私密渠道还包括外部白帽页（react 的 facebook.com/whitehat）与赏金平台（transformers 用 Huntr）——审查时别把「不在信号集里」直接判为缺失。

### FUNDING.yml

[官方](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/displaying-a-sponsor-button-in-your-repository)：

- 位置 `.github/FUNDING.yml`；key 白名单 12 个：`github / patreon / open_collective / ko_fi / tidelift / community_bridge / polar / issuehunt / liberapay / buy_me_a_coffee / thanks_dev / custom`（范本实际只用 github、open_collective、custom）。
- 多平台各写一行；多人用 YAML 列表 `github: [a, b]`；`custom` 最多 4 条、含 `:` 的 URL 必须加引号。
- 组织回退：放 `{org}/.github` 仓库 root 或其 `.github/` 子目录，对全组织仓库生效（vite/immich/fastapi 实测）。

### org 回退链与 API 陷阱（审查必读）

1. 判「缺社区文件」前先查 `{org}/.github` 回退（root 与 `.github/` 子目录两处都生效）——否则对 fastapi/immich/vite 误报。
2. `community/profile` 的 `files.issue_template` 对目录式模板**恒为 null**（8/8 如此）——判 issue 模板必须列 `.github/ISSUE_TEMPLATE/` 目录。
3. `files` 对象的 key 恒在，值 null 才是缺失——判存在看值不看键。
4. `health_percentage` 权重不可反推（文件更多的 ollama 62 反而低于 pocketbase 75），且 SECURITY/FUNDING 不计分——只记录展示，不当门槛。

---

## 五、issue / PR 模板

### .github/ 门面最小集

`ISSUE_TEMPLATE/`（含 `config.yml`）+ `workflows/` 是 8/8 标配；PR 模板实际 6/8 生效（5/8 自备 + fastapi 经 `{org}/.github` 回退生效——**GitHub 的 Community Profile 会把组织回退文件计入**，审查时以 profile 值的 html_url 判实际位置）；FUNDING.yml、DISCUSSION_TEMPLATE/、dependabot.yml 是可选项（2–4/8）。

### bug 模板：用 YAML issue forms，别用 markdown

[官方语法](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)。5/7 范本 bug 模板用 forms（markdown 无法设 `required: true`，只能注释恳求）。默认骨架：

```yaml
name: 🐛 Bug report
description: Something is broken
labels: [pending triage]        # 模板即分诊：预设 labels + title 前缀（6 家在用）
body:
  - type: checkboxes
    attributes:
      label: 查重声明
      options: [label: I have searched the existing issues, both open and closed, required: true]  # immich 放第一字段
  - type: textarea
    id: description
    attributes: {label: 描述, placeholder: 明确描述异常行为}
    validations: {required: true}
  - type: input
    id: repro
    attributes: {label: 复现, description: 无复现可能被标记 needs-reproduction 并自动关闭}
    validations: {required: true}
  - type: input
    id: version
    attributes: {label: 版本, placeholder: "运行 `proj --version`"}   # 别让用户手打：给生成命令
    validations: {required: true}
  - type: dropdown
    id: os
    attributes: {label: OS, multiple: true, options: [Linux, macOS, Windows, Docker]}  # 封闭枚举用 dropdown
  - type: textarea
    id: logs
    attributes: {label: 日志, render: shell}   # render 选填
```

要点：必填四件套 = **描述、复现、版本、环境**（4 家 forms 全把描述设必填）；环境信息给生成命令（vite 的 `npx envinfo …` `render: shell`）或 dropdown `multiple: true`；尾部放必填 Validations checkbox 组（vite 7 项是标杆：查重/CoC/贡献指南/最小复现/问对仓库）。

### config.yml（8/8 都有）

```yaml
blank_issues_enabled: false   # 有人力分诊选 false（react/vite/fastapi/immich）；没人力宽进选 true
contact_links:
  - name: 💬 Questions & Answers
    url: https://github.com/OWNER/REPO/discussions/categories/q-a  # 问答分流：Discussions 分类页(4)/Discord(3)/论坛 三选一
    about: 问使用问题请到 Discussions，issue 只收 bug 与功能请求
```

feature request 可不设模板：immich 由 contact_links 引流到 Discussions 的 feature-request 分类；react 干脆 bug-only。**反模式：空壳模板**（只有 frontmatter 正文 0 字节，ollama 的 20_feature_request.md 是反面教材）。多模板排序用数字前缀（`10_bug.yml` / `20_feature.yml`）。

### PR 模板：`.github/PULL_REQUEST_TEMPLATE.md`（6/6 放这里）

正文四节骨架：**Summary（含 `Fixes #` 占位）→ 验证方式（How did you test）→ Related Issue → checklist（3–9 项，每项一个可验证动作）**；UI 项目加截图节（lobehub 的 Before/After 双列表格）。ant-design 的 18 项是「PR 类型选择器」不是 checklist。

2025+ 新标配——AI 披露条款，三档强度：lobehub 结构化（`Contribution source:` 必填标签 + Harness/Model/Division of work/Verification 六字段）/ transformers 严厉（首次贡献者禁 AI 代写，违规拉黑）/ immich 自由文本一段。

双语仓库提供双语模板（ant-design `PULL_REQUEST_TEMPLATE_CN.md` 互链、config.yml 双语）。`PULL_REQUEST_TEMPLATE/config.yml` 的 `blank_pull_request_template_enabled` 不是 GitHub 可移植功能（全球仅 immich 用），照抄前确认平台支持。

---

## 六、releases 与 CHANGELOG

| # | 规则 | 证据 |
|---|---|---|
| 1 | tag 用小写 `v` + semver，**全仓库一致**（8/10；别学 Pake 大写 V、fastapi 孤立 v0.1.16） | [共识] |
| 2 | release 标题默认 = tag；日期/代号/emoji 是可选点缀；别风格漂移（transformers 反例） | [分布] |
| 3 | 每个 release 锚定一个 tag，但不是每个 tag 都要 release（差额来自 beta/rc/canary、monorepo 子包 tag） | [官方+共识] |
| 4 | prerelease 标记 = 预发布渠道开关，保护 `latest` 指稳定版（vite-beta / immich-rc / lobe-chat canary 全标 true）；杂渠道版本号用 `v0.0.0-` 前缀确保永远小于正式版 | [官方+分布] |
| 5 | notes 以**手写 highlights 为主流**（8/10）：一句话主题 → 升级提示（可选）→ 分节（Features/Bug fixes/…）→ 每条带 issue/PR 链接与作者（`PR #16418 by @tiangolo`） | [共识] |
| 6 | 自动生成路线必须配 `.github/release.yml` 做 label→分区映射（[官方](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes)；immich 7 分区：🚨Breaking/Deprecated/🔒Security/🚀Features/🌟Enhancements/🐛Bug fixes/📚Docs），正文自带 What's Changed + 贡献者 + Full Changelog 链接 | [官方+个例] |
| 7 | Full Changelog compare 链接：release 正文里 2/10 才有（非必需）；**文件式 changelog 里逐版本 compare 链接是标配** | [官方+分布] |
| 8 | changelog 文件多数派 7/10（根目录 5、monorepo 放主包目录如 `packages/vite/`、fastapi 放 docs）；与 release notes **同源同文**避免两套口径（pocketbase 逐字一致） | [共识] |
| 9 | **不要默认 Keep a Changelog**（0/10 用）；选与 release notes 同构的格式即可；顶部 Unreleased/TBD 段是加分实践（ripgrep/fzf） | [共识反向] |
| 10 | 双语项目可发双语 notes（Pake `### Changelog` + `### 更新日志`）；README 可直链 `releases/latest/download/<asset>` 免翻页 | [个例] |

资产策略按「**是否分发二进制**」判定（库+CLI 混合形态也按此判定，不按仓库类型）：

- 走包管理器的库：0 资产（npm/PyPI 即渠道）。
- 终端用户产品附多平台资产 + 校验和：Rust `{name}-{ver}-{target-triple}.tar.gz` + 逐文件 `.sha256`；Go `{name}_{ver}_{GOOS}_{GOARCH}.zip` + `checksums.txt`；桌面 electron-builder 全家桶（dmg/exe + `.blockmap` + `latest.yml`）。
- 部署型项目：配置即资产（immich 把 docker-compose.yml/example.env/APK 挂进 release，让部署者锁定配套配置）。

自动化工具速查（用户必问「每版手写太累」）：GitHub 原生 `.github/release.yml` 自动笔记（零依赖）；conventional-changelog/release-please（commit 规范驱动，vite 路线）；changesets（monorepo 版本管理，lobe-chat 路线）。选一种，别叠加。

---

## 七、社区入口与仓库开关

社区入口是加分项不是必需项（4/10 范本完全无社区链接），按档位递进：

| 档位 | 形态 | 做法 |
|---|---|---|
| L0 | 无链接 | 不扣分（fastapi/ripgrep/fzf/pocketbase 均如此） |
| L1 | 顶部 badge | Discord 为主（3/4），`img.shields.io/discord/<服务器ID>`，放 README 前 30 行 |
| L2 | 专门章节 | Community 章节卡片矩阵（lobe-chat）或生态清单（transformers awesome 列表） |
| L3 | Discussions 开关 | `has_discussions` 默认开（8/10；两个超大库关闭是因为有外置社区载体） |

L3 配套（打开 Discussions 就要做）：设计分类（Q&A / Ideas / Show and tell / Announcements）；问答分流链接指到具体分类页（`discussions/categories/q-a`）；可选 `DISCUSSION_TEMPLATE/`（2/8 在用）。

组织与个人 profile README：

- 组织门面生效位是 `{org}/.github` 仓库的 **`profile/README.md`**（根 README 只是 `# .github` 占位，不生效）。[官方](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/customizing-your-organizations-profile) 内容一句话介绍 + logo + Discord 入口即可（immich/vitejs/lobehub 3/7 组织在用）。
- 个人维护者：`用户名/用户名` 仓库（作品集式 tw93 / 赞助导向 junegunn）。

仓库开关基线：discussions 开、wiki 关（6/8 关，仅两个老仓库开着）。[分布]
