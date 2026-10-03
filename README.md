# repo-readme-skill

**A distilled standard for repo description docs: README, About, topics — learned from 12 top-tier OSS repos.**

Ships as an agent skill: audit an existing README or write a new one that reads like it was written by the React / Vite / FastAPI / Ollama teams.

[简体中文](README.zh-CN.md) · License: MIT

## Why

Most README guidance is either a vague checklist ("add badges!") or a rigid spec nobody follows. This project did the opposite: we fetched the actual READMEs and repo metadata of 12 elite repositories — React, Vite, FastAPI, Ollama, ripgrep, fzf, PocketBase, Immich, transformers, ant-design, LobeHub, Pake — reverse-engineered the patterns they share, and turned them into a working standard with templates, a review checklist, and an audit script.

## What's inside

```
repo-readme-skill/
├── SKILL.md                          # the skill: workflow, hard rules, repo-type detection
├── references/
│   ├── description-topics.md         # 6 description formulas + 5-layer topics recipe
│   ├── templates.md                  # README templates for 5 repo types
│   └── checklist.md                  # 22-item review checklist (A/B/C/D) + report format
└── scripts/
    ├── audit.py                      # hard-metric audit: error (official rules) vs hint (T0 practice)
    └── fetch_corpus.py               # rebuild the 12-repo sample corpus locally (optional)
```

## Highlights from the distillation

- **Six description formulas** — every T0 `About` fits one: category-noun-first (ant-design), three-selling-points (FastAPI), verb + quantifier (Pake), benefit-first (Ollama), comparative positioning (Vite, React), adjective + noun (Immich). All ≤ 120 chars, all contain a category noun.
- **Five-layer topics recipe** — own name → language → category → domain → ecosystem ride-along words (Ollama tags 8 model names; Pake tags `chatgpt` `claude` `gemini`).
- **The README is a router** — its length is inversely proportional to the docs site: Vite/React keep it to 3–5 KB, while docs-site-less ripgrep/fzf go 20–40 KB with GUIDE.md/FAQ.md splits.
- **Honesty over marketing** — benchmark tables state the machine, estimates get footnotes (FastAPI's "200%–300%" says *internal team estimate*), pre-v1 gets a `> [!WARNING]`.

## Install (as an agent skill)

```bash
git clone https://github.com/MicTx/repo-readme-skill.git
mkdir -p ~/.agents/skills
cp -R repo-readme-skill ~/.agents/skills/
```

Then ask your agent things like "audit this repo's README" or "rewrite my About description" — or run the audit directly:

```bash
python3 scripts/audit.py README.md --desc "your About text" --name user/repo --root .
```

The script exits `0` clean, `1` on errors (official GitHub rules: size limit, broken links, placeholders), `2` on bad input. `hints` are T0-practice suggestions — judge by repo type.

Optional: rebuild the sample corpus (12 full READMEs + metadata, gitignored) for offline reference:

```bash
python3 scripts/fetch_corpus.py   # writes to corpus/
```

## The 12 samples

| Repo | Stars* | What it demonstrates |
|---|---|---|
| react/react | 250k | minimal facade when a docs site exists |
| ollama/ollama | 182k | per-platform install, model ecosystem ride-along topics |
| huggingface/transformers | 166k | "when *not* to use" trust-building section |
| immich-app/immich | 115k | feature matrix table, demo credentials |
| fastapi/fastapi | 102k | quantified selling points with honest footnotes |
| ant-design/ant-design | 99k | UI-library four-piece structure |
| junegunn/fzf | 83k | README-as-document, dense copyable examples |
| lobehub/lobehub | 82k | AI app: quick start + ecosystem links |
| BurntSushi/ripgrep | 68k | benchmark comparison table with caveats |
| tw93/Pake | 61k | persona-based getting-started routing |
| pocketbase/pocketbase | 61k | one-line feature list, WARNING boundary |
| vitejs/vite | 83k | 3 KB facade, monorepo package table |

\* at distillation time, 2026-10.

Full-text snapshots are not redistributed (copyright stays with each project); `fetch_corpus.py` pulls them fresh from the source repos.

## Contributing

Issues and PRs welcome — the checklist and templates are meant to evolve with real-world use. Run `python3 scripts/audit.py` against your own README before and after to show the delta.

## License

MIT — see [LICENSE](LICENSE). The 12 sample READMEs remain the property of their respective projects.
