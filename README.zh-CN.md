# readme-skill

**从 12 个 T0 级开源仓库蒸馏出的 GitHub 门面全套规范——从 README 到 releases。**

以 agent skill 形式交付：既能体检现有仓库门面，也能写出「像 React / Vite / FastAPI / Ollama 团队亲手写的」新门面。

[![License: AGPL v3](https://img.shields.io/badge/license-AGPL%20v3-blue)](LICENSE) [![Release](https://img.shields.io/badge/release-v0.2.0-blue)](https://github.com/MicTx/readme-skill/releases) · [English](README.md)

## 为什么做这个

市面上的 README 指南要么是空泛清单（「加徽章！」），要么是没人遵守的死板规格。本项目反过来做：抓取 12 个顶级仓库（React、Vite、FastAPI、Ollama、ripgrep、fzf、PocketBase、Immich、transformers、ant-design、LobeHub、Pake）的 README 全文和仓库元数据，反向工程出它们共同遵守的写法模式，再落成可执行的标准——模板、审查清单、审计脚本。

第二轮蒸馏（2026-10）把覆盖面从 README/About/topics 扩展到**全套门面**：badges 与首屏 hero、social preview 分享卡、社区健康文件（CONTRIBUTING/CoC/SECURITY/FUNDING）的内容级标准、issue/PR 模板、releases 与 CHANGELOG、社区入口——新增 82 条规则，每条标注证据强度。

## 目录结构

```
readme-skill/
├── SKILL.md                          # skill 主体：工作流、硬规则、仓库类型判定
├── references/
│   ├── description-topics.md         # 描述六句式 + topics 五层配方
│   ├── templates.md                  # 五类仓库的 README 模板
│   ├── facade-decor.md               # 门面装饰标准：badges/首屏/social preview/
│   │                                 #   社区文件内容级标准/issue-PR 模板/releases/社区入口
│   └── checklist.md                  # 审查清单 A–I 段 + 报告格式
├── scripts/
│   ├── audit.py                      # 硬指标审计 + --repo 门面模式（gh api 实测）
│   └── fetch_corpus.py               # 本地重建 12 仓库范本语料 + 门面数据（可选）
├── .github/                          # issue 表单（bug/feature）+ PR 模板
└── CONTRIBUTING.md · CODE_OF_CONDUCT.md · SECURITY.md
```

## 蒸馏出的核心规律

- **描述六句式**——所有 T0 的 About 都命中其一：品类词开头（ant-design）、三卖点连排（FastAPI）、动词+量化（Pake）、收益开头（Ollama）、比较级定位（Vite/React）、形容词+名词（Immich）。全部 ≤ 120 字符、必含品类名词。
- **topics 五层配方**——自身名 → 语言 → 品类 → 领域 → 生态搭车词（Ollama 挂了 8 个模型名；Pake 挂 `chatgpt` `claude` `gemini`）。
- **README 是路由器**——篇幅与文档站成反比：有 docs 站的 Vite/React 只写 3–5 KB；没有 docs 站的 ripgrep/fzf 才写到 20–40 KB 并拆出 GUIDE.md/FAQ.md。
- **诚实高于营销**——性能表注明测试机器、估算值带脚注（FastAPI 的「200%–300%」标注*内部团队估算*）、未到 v1 用 `> [!WARNING]` 声明边界。
- **badges：41/41 全包链接、零样式混用**——CI badge 排第一（8/9）、单行 ≤ 6 个、vanity badge 不排在 CI/版本前、没有任何一家用 badge 指官网（0/10）。
- **组织回退链**——`{org}/.github` 可为全组织仓库提供 CONTRIBUTING/CoC/SECURITY/FUNDING（3/8 组织在用）；GitHub 的 community profile 会计入回退文件，判「缺失」前必须先排除回退。
- **release notes 以手写 highlights 为主流**（8/10）——一句话主题 → 分节 → 逐条 issue/PR 链接带作者；prerelease 标记保护 latest；Keep a Changelog 无人用（0/10）——选与 notes 同构的格式即可。

## 安装（作为 agent skill）

```bash
git clone https://github.com/MicTx/readme-skill.git
mkdir -p ~/.agents/skills
cp -R readme-skill ~/.agents/skills/
```

然后对 agent 说「按规范体检这个 README」「帮我重写仓库描述」即可；也可直接跑审计脚本：

```bash
python3 scripts/audit.py README.md --desc "About 描述原文" --name user/repo --root .
# 门面模式（gh 已登录）：实测 About/topics/社区文件(含组织回退)/issue 模板/发布线/social preview
python3 scripts/audit.py README.md --repo user/repo
```

退出码：`0` 干净，`1` 有 error（GitHub 官方硬规则：体积超限、死链、占位符、topics 非法格式），`2` 输入错误。`hints` 是 T0 实践建议，按仓库类型自行判断。

可选：重建范本语料（12 篇 README 全文 + 元数据 + 门面数据，已 gitignore），供离线对照：

```bash
python3 scripts/fetch_corpus.py   # 输出到 corpus/
```

## 12 个范本

| 仓库 | Stars* | 学什么 |
|---|---|---|
| react/react | 250k | 有文档站时的极简门面 |
| ollama/ollama | 182k | 分平台安装、模型生态搭车 topics |
| huggingface/transformers | 166k | 「何时不用」信任章节 |
| immich-app/immich | 115k | 功能矩阵表、demo 凭据 |
| fastapi/fastapi | 102k | 量化卖点 + 诚实脚注 |
| ant-design/ant-design | 99k | 组件库四件套结构 |
| junegunn/fzf | 83k | README 即文档、高密度可复制示例 |
| lobehub/lobehub | 82k | AI 应用：快速启动 + 生态链接 |
| BurntSushi/ripgrep | 68k | 带环境注明的基准对比表 |
| tw93/Pake | 61k | 按用户角色分流的 Getting Started |
| pocketbase/pocketbase | 61k | 一句话特性列表、WARNING 边界 |
| vitejs/vite | 83k | 3 KB 门面、monorepo 包表 |

\* 蒸馏时点（2026-10）数据。

范本全文不随本仓库再分发（版权归各自项目所有）；用 `fetch_corpus.py` 从源仓库现拉。

## 贡献

欢迎 issue 与 PR——清单和模板就该随真实使用进化。见 [CONTRIBUTING.md](CONTRIBUTING.md)；唯一铁律：改规则必须给证据（哪个仓库或官方文档示范了这个模式）。改动前后各跑一次 `python3 scripts/audit.py`，把差值贴进 PR。

## 安全

审计脚本在本地运行、只读调用 GitHub API——若发现可利用问题请私密上报：[SECURITY.md](SECURITY.md)。

## 许可证

[AGPL-3.0](LICENSE)——可自由使用与修改（含商用），衍生品与网络服务必须开源。12 篇范本 README 版权归各自项目。
