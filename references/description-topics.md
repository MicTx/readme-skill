# 仓库描述（About）与 Topics 蒸馏规则

来源：12 个 T0 仓库实测元数据（2026-10 抓取）+ GitHub 官方 topics 规则。

## 一、About 描述：六种句式

T0 描述全部在 35–120 字符内，且必含**类别词**（library / framework / tool / solution / backend / UI design language）。
按仓库类型选句式：

| # | 句式 | 范本 |
|---|---|---|
| 1 | **类别词开头**：「An enterprise-class UI design language and React UI library」 | ant-design |
| 2 | **类别 + 三个卖点逗号连排**：「FastAPI framework, high performance, easy to learn, fast to code, ready for production」 | fastapi |
| 3 | **一句话动词句 + 量化**：「Turn any webpage into a desktop app with one command.」 | Pake |
| 4 | **收益动词开头**：「Get up and running with Kimi, GLM, DeepSeek, Qwen...」 | ollama |
| 5 | **比较级定位**：「Next generation frontend tooling. It's fast!」「The library for web and native user interfaces.」 | vite / react |
| 6 | **两个形容词 + 名词**：「High performance self-hosted photo and video management solution.」 | immich |

写法要点：

- **核心名词必须出现**（photo management / fuzzy finder / backend / search tool），读者扫一眼就知道品类。
- 差异化定语放最前：「realtime backend **in 1 file**」「**recursively** searches ... **while respecting your gitignore**」。
- 卖点最多三项连排，超过就砍（FastAPI 的三项是性能/易学/生产可用）。
- emoji 可选（fzf `:cherry_blossom:`、Pake 🤱🏻、transformers 🤗），锦上添花不是必须。
- 团队名/公司名不进描述；「open source」二字 T0 很少写（开源是默认假设）。

## 二、Topics 五层配方（从具体到生态）

12 个范本的 topics 全部命中以下分层，按顺序挑选，总量 4–20 个：

1. **自身名**：`react` `vite` `fastapi` `ripgrep`（品牌词占位，防抢）
2. **语言/运行时**：`rust` `go` `python` `typescript` `golang`
3. **品类词**：`cli` `framework` `library` `backend` `build-tool` `ui-library` `self-hosted`
4. **领域/能力词**：`regex` `search` `llm` `realtime` `hmr` `machine-learning` `photo-gallery` `design-systems`
5. **生态搭车词**：ollama 列了 8 个模型名（`deepseek` `qwen` `gemma3` `glm`...）；Pake 搭 `chatgpt` `claude` `gemini` `tauri`；transformers 搭 `deepseek` `qwen` `gemma`。**目的是出现在这些热词的 topic 搜索结果里。**

规则提醒（官方硬性）：小写字母/数字/连字符；单个 ≤ 50 字符；每仓库 ≤ 20 个；私有仓库 topics 公开可见；
仅仓库管理员可改。单复数选高频那个（`llm` 和 `llms` ollama 都占了——热度词可双占，普通词选一个）。

## 三、Homepage 与 About 的配合

- 有文档站必填 homepage（T0 全部填了）：`https://vite.dev`、`https://immich.app`。
- homepage 填**文档/官网**，不是 GitHub Pages 之外的随机链接；没有官网就留空，别塞 issue 链接。

## 四、自检清单

- [ ] 描述 ≤ 120 字符，含品类名词，含至少一个差异化定语
- [ ] 描述与 README 首段、包管理器 description 三处一致
- [ ] topics 4–20 个，覆盖五层中至少四层，全小写连字符
- [ ] 热度搭车词只搭真实相关的（挂羊头卖狗肉会被社区反感）
- [ ] homepage 已填且指向文档站
