# readme-skill

**A distilled standard for the full GitHub repo facade — README to releases — learned from 12 top-tier OSS repos.**

Ships as an agent skill: audit an existing repo facade or write a new one that reads like it was written by the React / Vite / FastAPI / Ollama teams.

[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-blue)](LICENSE) [![Release](https://img.shields.io/badge/release-v0.2.0-blue)](https://github.com/MicTx/readme-skill/releases) · [简体中文](README.zh-CN.md)

## Why

Most README guidance is either a vague checklist ("add badges!") or a rigid spec nobody follows. This project did the opposite: we fetched the actual READMEs and repo metadata of 12 elite repositories — React, Vite, FastAPI, Ollama, ripgrep, fzf, PocketBase, Immich, transformers, ant-design, LobeHub, Pake — reverse-engineered the patterns they share, and turned them into a working standard with templates, a review checklist, and an audit script.

A second distillation round (2026-10) extended coverage from README/About/topics to the **full facade**: badges and the hero first screen, social preview cards, community health files (CONTRIBUTING / CoC / SECURITY / FUNDING) down to content level, issue/PR templates, releases and CHANGELOGs, and community entry points — 82 more rules, each tagged with evidence strength.

## What's inside

```
readme-skill/
├── SKILL.md                          # the skill: workflow, hard rules, repo-type detection
├── references/
│   ├── description-topics.md         # 6 description formulas + 5-layer topics recipe
│   ├── templates.md                  # README templates for 5 repo types
│   ├── facade-decor.md               # full-facade standard: badges/hero/social preview/
│   │                                 #   community files content/issue-PR templates/releases/community
│   └── checklist.md                  # review checklist A–I + report format
├── scripts/
│   ├── audit.py                      # hard-metric audit + --repo facade mode (gh api)
│   └── fetch_corpus.py               # rebuild the 12-repo corpus + facade data locally (optional)
├── .github/                          # issue forms (bug/feature) + PR template
└── CONTRIBUTING.md · CODE_OF_CONDUCT.md · SECURITY.md
```

## Highlights from the distillation

- **Six description formulas** — every T0 `About` fits one: category-noun-first (ant-design), three-selling-points (FastAPI), verb + quantifier (Pake), benefit-first (Ollama), comparative positioning (Vite, React), adjective + noun (Immich). All ≤ 120 chars, all contain a category noun.
- **Five-layer topics recipe** — own name → language → category → domain → ecosystem ride-along words (Ollama tags 8 model names; Pake tags `chatgpt` `claude` `gemini`).
- **The README is a router** — its length is inversely proportional to the docs site: Vite/React keep it to 3–5 KB, while docs-site-less ripgrep/fzf go 20–40 KB with GUIDE.md/FAQ.md splits.
- **Honesty over marketing** — benchmark tables state the machine, estimates get footnotes (FastAPI's "200%–300%" says *internal team estimate*), pre-v1 gets a `> [!WARNING]`.
- **Badges: 41/41 wrapped in links, zero style mixing** — CI badge first (8/9), single row ≤ 6, vanity badges never before CI/version, and nobody points a badge at their own website (0/10).
- **Org fallback chain** — `{org}/.github` can provide CONTRIBUTING/CoC/SECURITY/FUNDING for every repo (3/8 orgs do); GitHub's community profile counts them, so "missing" verdicts must check the fallback first.
- **Release notes are hand-written highlights** (8/10) — one-line theme → sections → per-change issue/PR links with authors; prerelease flags protect `latest`; nobody uses Keep a Changelog (0/10) — pick the format that mirrors your notes.

## Install (as an agent skill)

```bash
git clone https://github.com/MicTx/readme-skill.git
mkdir -p ~/.agents/skills
cp -R readme-skill ~/.agents/skills/
```

Then ask your agent things like "audit this repo's README" or "rewrite my About description" — or run the audit directly:

```bash
python3 scripts/audit.py README.md --desc "your About text" --name user/repo --root .
# facade mode (gh CLI logged in): About/topics/community files with org fallback/
# issue templates/release line/social preview, via live GitHub API
python3 scripts/audit.py README.md --repo user/repo
```

The script exits `0` clean, `1` on errors (official GitHub rules: size limit, broken links, placeholders, illegal topics), `2` on bad input. `hints` are T0-practice suggestions — judge by repo type.

Optional: rebuild the sample corpus (12 full READMEs + metadata + facade data, gitignored) for offline reference:

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

Issues and PRs welcome — the checklist and templates are meant to evolve with real-world use. See [CONTRIBUTING.md](CONTRIBUTING.md); the one ground rule is that rule changes need evidence (a repo or official doc that demonstrates the pattern). Run `python3 scripts/audit.py` against your own README before and after to show the delta.

## Security

The audit scripts run locally and call the GitHub API read-only — if you spot something exploitable in them, please report privately: [SECURITY.md](SECURITY.md).

## License

[CC BY-NC 4.0](LICENSE) — free for personal and non-commercial use, attribution required. The 12 sample READMEs remain the property of their respective projects.
