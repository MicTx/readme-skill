# readme-skill

**开源仓库门面全套规范——README 到 releases，12 个顶级开源范本蒸馏，附审计脚本。**

以 agent skill 形式交付：既能体检现有仓库门面，也能写出「像 React / Vite / FastAPI / Ollama 团队亲手写的」新门面——每条判断都出自 12 个范本的实际做法，不是某人的口味。

[![License: AGPL v3](https://img.shields.io/badge/license-AGPL%20v3-blue)](LICENSE) [![Release](https://img.shields.io/github/v/release/MicTx/readme-skill?style=flat&color=blue)](https://github.com/MicTx/readme-skill/releases) · [English](README.en.md)

## 目录

- [为什么做这个](#为什么做这个)
- [安装（作为 agent skill）](#安装作为-agent-skill)
- [30 秒尝鲜](#30-秒尝鲜)
- [蒸馏出的核心规律](#蒸馏出的核心规律)
- [12 个范本](#12-个范本)
- [深入阅读](#深入阅读)
- [贡献](#贡献) · [安全](#安全) · [许可证](#许可证)

## 为什么做这个

你大概读过那种清单式指南——「加个徽章」「放张截图」，照着做完，README 还是差口气。这类指南答不好「头部团队实际怎么做」：它们出自个人经验，缺少对真实仓库的系统观察。本项目补的就是这块。语料是 12 个顶级仓库的 README 全文加仓库元数据：React、Vite、FastAPI、Ollama、ripgrep、fzf、PocketBase、Immich、transformers、ant-design、LobeChat、Pake。反向工程出它们共同遵守的模式，落成可执行的标准——模板、审查清单、审计脚本。

第二轮蒸馏（2026-10）把覆盖面从 README/About/topics 扩展到**全套门面**：badges 与首屏 hero、social preview 分享卡、社区健康文件（CONTRIBUTING/CoC/SECURITY/FUNDING）的内容级标准、issue/PR 模板、releases 与 CHANGELOG、社区入口——新增 82 条规则，每条标注证据强度。

## 安装（作为 agent skill）

```bash
git clone https://github.com/MicTx/readme-skill.git
mkdir -p ~/.agents/skills
cp -R readme-skill ~/.agents/skills/
```

然后对 agent 说「按规范体检这个 README」「帮我重写仓库描述」即可。

## 30 秒尝鲜

最短的验证方式是让它审自己：本仓库的 README 就是按这套标准写的。

```bash
python3 scripts/audit.py README.md
```

真实输出如下，装好后复跑，数字应一致：

```json
{
  "file": "README.md",
  "errors": [],
  "hints": [],
  "info": {
    "bytes": 8098,
    "lines": 130,
    "first_paragraph": "**开源仓库门面全套规范——README 到 releases，12 个顶级开源范本蒸馏，附审计脚本。**",
    "h2_sections": 10,
    "badges": {
      "linked": 2,
      "bare": 0,
      "styles": [
        "flat"
      ]
    }
  },
  "ok": true
}
```

`errors` 只收 GitHub 官方硬规则：体积超限、死链、占位符、topics 非法格式，命中退出码 `1`，输入错误退出 `2`。`hints` 是头部仓库的实践建议，退出码 `0` 也可能带着，按仓库类型取舍。审自己的仓库时把 About 原文一并传入，首段与 About 的一致性也会查：

```bash
python3 scripts/audit.py README.md --desc "About 描述原文" --name user/repo --root .
# 门面模式（gh 已登录）：实测 About/topics/社区文件(含组织回退)/issue 模板/发布线/social preview
python3 scripts/audit.py README.md --repo user/repo
```

可选：`python3 scripts/fetch_corpus.py` 重建范本语料（12 篇 README 全文 + 元数据 + 门面数据，已 gitignore），供离线对照。

## 蒸馏出的核心规律

以下规律全部实测自 12 个顶级（T0）开源仓库的语料；分数与计数的口径、逐条证据见 [references/facade-decor.md](references/facade-decor.md)。

- **描述六句式**——所有 T0 的 About 都命中其一：品类词开头（ant-design）、三卖点连排（FastAPI）、动词+量化（Pake）、收益开头（Ollama）、比较级定位（Vite/React）、形容词+名词（Immich）。全部 ≤ 120 字符、必含品类名词。
- **topics 五层配方**——自身名 → 语言 → 品类 → 领域 → 生态搭车词（Ollama 挂了 8 个模型名；Pake 挂 `chatgpt` `claude` `gemini`）。
- **README 是路由器**——篇幅与文档站成反比：有 docs 站的 Vite/React 只写 3–5 KB；没有 docs 站的 ripgrep/fzf 才写到 20–40 KB 并拆出 GUIDE.md/FAQ.md。
- **诚实高于营销**——性能表注明测试机器、估算值带脚注（FastAPI 的「200%–300%」标注*内部团队估算*）、未到 v1 用 `> [!WARNING]` 声明边界。
- **badges：41/41 全包链接、零样式混用**——8/9 摆 CI badge（5 家放行首）、单行 ≤ 6 个、vanity badge 不排在 CI/版本前、没有一家用 badge 指官网（0/10）。
- **组织回退链**——`{org}/.github` 可为全组织仓库提供 CONTRIBUTING/CoC/SECURITY/FUNDING（3/8 组织在用）；GitHub 的 community profile 会计入回退文件，判「缺失」前必须先排除回退。
- **release notes 以手写 highlights 为主流**（8/10）——一句话主题 → 分节 → 逐条 issue/PR 链接带作者；prerelease 标记保护 latest；Keep a Changelog 无人用（0/10）——选与 notes 同构的格式即可。

## 12 个范本

| 仓库 | Stars* | 学什么 |
|---|---|---|
| [facebook/react](https://github.com/facebook/react) | 250.9k | 有文档站时的极简门面 |
| [ollama/ollama](https://github.com/ollama/ollama) | 182.2k | 分平台安装、模型生态搭车 topics |
| [huggingface/transformers](https://github.com/huggingface/transformers) | 166.9k | 「何时不用」信任章节 |
| [immich-app/immich](https://github.com/immich-app/immich) | 115.6k | 功能矩阵表、demo 凭据 |
| [fastapi/fastapi](https://github.com/fastapi/fastapi) | 102.8k | 量化卖点 + 诚实脚注 |
| [ant-design/ant-design](https://github.com/ant-design/ant-design) | 99.7k | 组件库四件套结构 |
| [junegunn/fzf](https://github.com/junegunn/fzf) | 83.4k | README 即文档、高密度可复制示例 |
| [vitejs/vite](https://github.com/vitejs/vite) | 83.1k | 3 KB 门面、monorepo 包表 |
| [lobehub/lobe-chat](https://github.com/lobehub/lobe-chat) | 83.0k | AI 应用：快速启动 + 生态链接 |
| [BurntSushi/ripgrep](https://github.com/BurntSushi/ripgrep) | 68.8k | 带环境注明的基准对比表 |
| [tw93/Pake](https://github.com/tw93/Pake) | 61.9k | 按用户角色分流的 Getting Started |
| [pocketbase/pocketbase](https://github.com/pocketbase/pocketbase) | 61.3k | 一句话特性列表、WARNING 边界 |

\* 2026-10-04 经 GitHub API 实测。范本全文不随本仓库再分发（版权归各自项目所有）；需要离线对照时，用 `fetch_corpus.py` 从源仓库现拉。

## 深入阅读

| 想做什么 | 去哪里 |
|---|---|
| 让 agent 接活：判定场景（审查 / 撰写 / 装饰）、走工作流 | [SKILL.md](SKILL.md) |
| 写 About 描述、配 topics | [references/description-topics.md](references/description-topics.md) |
| 从零起一份 README（五类仓库模板） | [references/templates.md](references/templates.md) |
| 弄 badges、首屏 hero、社区文件、issue/PR 模板、releases | [references/facade-decor.md](references/facade-decor.md) |
| 逐项审一个仓库门面（A–I 清单 + 报告格式） | [references/checklist.md](references/checklist.md) |

`.github/` 里的 issue 表单与 PR 模板、根目录的社区文件，本身都按这套标准写成，可直接当样例参考。

## 贡献

欢迎 issue 与 PR——清单和模板就该随真实使用进化。见 [CONTRIBUTING.md](CONTRIBUTING.md)；唯一铁律：改规则必须给证据（哪个仓库或官方文档示范了这个模式）。改动前后各跑一次 `python3 scripts/audit.py`，把差值贴进 PR。

## 安全

审计脚本在本地运行、只读调用 GitHub API——若发现可利用问题请私密上报：[SECURITY.md](SECURITY.md)。

## 许可证

[AGPL-3.0](LICENSE)——可自由使用与修改（含商用），衍生品与网络服务必须开源。12 篇范本 README 版权归各自项目。
