# 五类仓库 README 模板（T0 蒸馏）

先判类型再用模板。每个模板后的「范本」标注该结构的出处，写作时回忆其做法。

---

## 通用骨架（所有类型共享）

```markdown
[logo 或居中标题]
[一行短简介，<120 字符，与 About 一致]
[badges：CI / 版本 / license / 社区，4–6 个，每个必须带链接]
[截图或 demo GIF —— 能一眼看懂产品形态的]

## ✨ Features / 特性          ← 3–6 条，每条 **加粗词**: 一句解释
## 📦 Installation            ← 按平台/按包管理器
## 🔨 Usage / Quick Start     ← 最小可运行示例，可复制、有预期输出
## 🔗 Links / Documentation   ← 文档、demo、社区、roadmap
## 🤝 Contributing            ← 链到 CONTRIBUTING.md，附行为准则
## License                    ← SPDX 名称 + 相对链接
```

顺序不变，段落按需删减；README 超 100 行就在 Usage 前加目录。

---

## 1. 应用 / 自托管服务（Immich、PocketBase、LobeChat）

用户是部署者，最关心「长什么样→怎么部署→有没有坑」。

- 功能用**矩阵表**：功能 × 平台（Mobile/Web）或功能 × 说明，一行一项可扫读（Immich 30 行功能表）
- **Demo 必备**：给地址 + 测试凭据表（Immich 给了 demo@immich.app / demo）
- 部署章节给 docker-compose 最小配置，其余链到 docs
- 边界声明用 GitHub alert 语法：
  `> [!WARNING]` 数据安全/兼容性警告（PocketBase v1 前不保证兼容；Immich 的 3-2-1 备份提醒）
- 生态位声明：「Google Photos 的自托管替代」这类比较定位放首段

## 2. CLI 工具（ripgrep、fzf、Ollama）

用户在终端，README 就是 man page 的门面。

- 安装**按平台分小节**（macOS/Windows/Linux/Docker），每平台一条可复制命令（Ollama 三平台各一行 curl/irm）
- **示例密度是生命线**：fzf README 42KB 里大半是可复制命令块，每块带注释说明效果
- 有性能主张就上**对比基准表**：工具 × 命令 × 耗时（倍数），注明测试机器 + 「单一基准不代表全部」（ripgrep）
- 无文档站时拆文件：`GUIDE.md`（用户指南）、`FAQ.md`、`CHANGELOG.md`，README 只放 quick links
- 安装方式全列：包管理器（brew/cargo/apt）+ 预编译二进制 + 从源码构建

## 3. 库 / 框架（React、Vite、FastAPI、transformers）

用户是写代码的开发者，README 是转化漏斗。

- 首段一句话定位 + **特性 bullet 列表**（每条 **加粗关键词** 开头：Declarative: / Fast: / Intuitive:）
- 量化卖点可写但必须诚实：FastAPI 的「200%–300% 开发提速」带 small 脚注「internal team 估算」
- **最小示例必须能跑**：短（< 20 行）、可复制、说明预期输出（React 的 HelloMessage 渲染说明）
- 「何时不用」章节是高级技巧（transformers 的 "When shouldn't I use Transformers?"）——建立信任
- monorepo 用包表：包名 × 版本 badge × changelog 链接（Vite 的 Packages 表）
- 有文档站时全部深入内容路由出去，README 保持 < 200 行

## 4. 模型 / AI 应用（Ollama、lobe-chat、transformers）

用户想「30 秒看到模型回答」。

- 开头即**最快路径**：`ollama run gemma4` 这种一行命令放最前
- REST/SDK 示例三连：curl + python + js，各 < 10 行（Ollama）
- 模型/集成列表用链接矩阵，把生态伙伴名字写全（蹭搜索 + 展示生态）
- 社区入口集中一个章节：Discord/X/Reddit 各一行

## 5. UI 组件库（ant-design）

- 固定四件套顺序：**环境支持**（浏览器/框架版本表）→ **Install** → **Usage**（import 示例）→ **Links**
- 使用 emoji 章节前缀是该类型惯例（✨🖥📦🔨🔗⌨️🤝❤️）
- 赞助/Backers 区固定文末（OpenCollective badge）

---

## 双语 README 策略（Pake、Immich 实证）

- **英文为主**（默认，国际受众）：主 `README.md` 用英文；中文版 `README.zh-CN.md`，其他语言 `README.<BCP47>.md` 放 `readme_i18n/`（Immich）或根目录（Pake 的 README_CN.md）
- **中文为主**（中文社区受众优先）：主 `README.md` 用中文；英文版 `README.en.md`。standard-readme 要求英文占主名，此式是自觉取舍——写给谁就把主名给谁
- 顶部互链行：`English | 简体中文`（Pake 把当前语言加粗，其余为链接）
- 两版本结构一致，中文版可省略赞助区

## 各类型的「不要做」

- 应用类：不要把功能写成散文段落，一律表格或 bullet
- CLI 类：不要只给 `--help` 截图不给可复制命令
- 库类：不要在 README 里堆 API reference（链到 docs.rs / api 文档）
- 所有类：不要用「一个强大的、革命性的」这类空形容词——T0 描述里没有一个 such 词；特性靠**具体机制**支撑
