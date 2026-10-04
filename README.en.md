# readme-skill

**A distilled standard for the full GitHub repo facade — README to releases — learned from 12 top-tier OSS repos.**

Ships as an agent skill: audit an existing repo facade or write a new one that reads like it was written by the React / Vite / FastAPI / Ollama teams — grounded in what those 12 repos actually do, not in one author's taste.

[![License: AGPL v3](https://img.shields.io/badge/license-AGPL%20v3-blue)](LICENSE) [![Release](https://img.shields.io/github/v/release/MicTx/readme-skill?style=flat&color=blue)](https://github.com/MicTx/readme-skill/releases) · [简体中文](README.md)

## Table of Contents

- [Why](#why)
- [Install (as an agent skill)](#install-as-an-agent-skill)
- [A 30-second taste](#a-30-second-taste)
- [Highlights from the distillation](#highlights-from-the-distillation)
- [The 12 samples](#the-12-samples)
- [Read deeper](#read-deeper)
- [Contributing](#contributing) · [Security](#security) · [License](#license)

## Why

You've probably read those checklist guides — "add a badge", "include a screenshot" — and finished with a README that still feels off. They can't answer *how top teams actually do it*: they come from personal experience, not from systematic observation. This project supplies the observation. The corpus is the full READMEs plus repo metadata of 12 elite repositories: React, Vite, FastAPI, Ollama, ripgrep, fzf, PocketBase, Immich, transformers, ant-design, LobeChat, Pake. The patterns they share were reverse-engineered into a working standard: templates, a review checklist, and an audit script.

A second distillation round (2026-10) extended coverage from README/About/topics to the **full facade**: badges and the hero first screen, social preview cards, community health files (CONTRIBUTING / CoC / SECURITY / FUNDING) down to content level, issue/PR templates, releases and CHANGELOGs, and community entry points — 82 more rules, each tagged with evidence strength.

## Install (as an agent skill)

```bash
git clone https://github.com/MicTx/readme-skill.git
mkdir -p ~/.agents/skills
cp -R readme-skill ~/.agents/skills/
```

Then ask your agent things like "audit this repo's README" or "rewrite my About description".

## A 30-second taste

The shortest way to see it work is to aim it at itself: this README is written to the standard it ships.

```bash
python3 scripts/audit.py README.en.md
```

Actual output — after installing, run it again and the numbers should match:

```json
{
  "file": "README.en.md",
  "errors": [],
  "hints": [],
  "info": {
    "bytes": 8574,
    "lines": 131,
    "first_paragraph": "**A distilled standard for the full GitHub repo facade — README to releases — learned from 12 top-tier OSS repos.**",
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

`errors` collects only official GitHub hard rules: size limits, broken links, placeholders, illegal topics — exit code `1` when any hit, `2` on bad input. `hints` are top-team practices; exit code `0` can still carry them, so judge them by repo type. Pass your About text along and first-paragraph/About consistency gets checked too:

```bash
python3 scripts/audit.py README.en.md --desc "your About text" --name user/repo --root .
# facade mode (gh CLI logged in): About/topics/community files with org fallback/
# issue templates/release line/social preview, via live GitHub API
python3 scripts/audit.py README.en.md --repo user/repo
```

Optional: `python3 scripts/fetch_corpus.py` rebuilds the sample corpus (12 full READMEs + metadata + facade data, gitignored) for offline reference.

## Highlights from the distillation

Every rule below was measured against the corpus of 12 top-tier (T0) OSS repos; denominators, counts, and per-rule evidence live in [references/facade-decor.md](references/facade-decor.md).

- **Six description formulas** — every T0 `About` fits one: category-noun-first (ant-design), three-selling-points (FastAPI), verb + quantifier (Pake), benefit-first (Ollama), comparative positioning (Vite, React), adjective + noun (Immich). All ≤ 120 chars, all contain a category noun.
- **Five-layer topics recipe** — own name → language → category → domain → ecosystem ride-along words (Ollama tags 8 model names; Pake tags `chatgpt` `claude` `gemini`).
- **The README is a router** — its length is inversely proportional to the docs site: Vite/React keep it to 3–5 KB, while docs-site-less ripgrep/fzf go 20–40 KB with GUIDE.md/FAQ.md splits.
- **Honesty over marketing** — benchmark tables state the machine, estimates get footnotes (FastAPI's "200%–300%" says *internal team estimate*), pre-v1 gets a `> [!WARNING]`.
- **Badges: 41/41 wrapped in links, zero style mixing** — 8/9 carry a CI badge (5 place it first), single row ≤ 6, vanity badges never before CI/version, and nobody points a badge at their own website (0/10).
- **Org fallback chain** — `{org}/.github` can provide CONTRIBUTING/CoC/SECURITY/FUNDING for every repo (3/8 orgs do); GitHub's community profile counts them, so "missing" verdicts must check the fallback first.
- **Release notes are hand-written highlights** (8/10) — one-line theme → sections → per-change issue/PR links with authors; prerelease flags protect `latest`; nobody uses Keep a Changelog (0/10) — pick the format that mirrors your notes.

## The 12 samples

| Repo | Stars* | What it demonstrates |
|---|---|---|
| [facebook/react](https://github.com/facebook/react) | 250.9k | minimal facade when a docs site exists |
| [ollama/ollama](https://github.com/ollama/ollama) | 182.2k | per-platform install, model ecosystem ride-along topics |
| [huggingface/transformers](https://github.com/huggingface/transformers) | 166.9k | "when *not* to use" trust-building section |
| [immich-app/immich](https://github.com/immich-app/immich) | 115.6k | feature matrix table, demo credentials |
| [fastapi/fastapi](https://github.com/fastapi/fastapi) | 102.8k | quantified selling points with honest footnotes |
| [ant-design/ant-design](https://github.com/ant-design/ant-design) | 99.7k | UI-library four-piece structure |
| [junegunn/fzf](https://github.com/junegunn/fzf) | 83.4k | README-as-document, dense copyable examples |
| [vitejs/vite](https://github.com/vitejs/vite) | 83.1k | 3 KB facade, monorepo package table |
| [lobehub/lobe-chat](https://github.com/lobehub/lobe-chat) | 83.0k | AI app: quick start + ecosystem links |
| [BurntSushi/ripgrep](https://github.com/BurntSushi/ripgrep) | 68.8k | benchmark comparison table with caveats |
| [tw93/Pake](https://github.com/tw93/Pake) | 61.9k | persona-based getting-started routing |
| [pocketbase/pocketbase](https://github.com/pocketbase/pocketbase) | 61.3k | one-line feature list, WARNING boundary |

\* measured via the GitHub API on 2026-10-04. Full-text snapshots are not redistributed (copyright stays with each project); `fetch_corpus.py` pulls them fresh from the source repos.

## Read deeper

| Want to | Go to |
|---|---|
| Have the agent take a job: pick a scenario (audit / write / decorate), run the workflow | [SKILL.md](SKILL.md) |
| Write an About description, pick topics | [references/description-topics.md](references/description-topics.md) |
| Start a README from scratch (templates for 5 repo types) | [references/templates.md](references/templates.md) |
| Badges, hero, community files, issue/PR templates, releases | [references/facade-decor.md](references/facade-decor.md) |
| Audit a repo facade item by item (A–I checklist + report format) | [references/checklist.md](references/checklist.md) |

The issue forms and PR template in `.github/` and the root community files are themselves written to this standard — free to copy as living examples.

## Contributing

Issues and PRs welcome — the checklist and templates are meant to evolve with real-world use. See [CONTRIBUTING.md](CONTRIBUTING.md); the one ground rule is that rule changes need evidence (a repo or official doc that demonstrates the pattern). Run `python3 scripts/audit.py` against your own README before and after to show the delta.

## Security

The audit scripts run locally and call the GitHub API read-only — if you spot something exploitable in them, please report privately: [SECURITY.md](SECURITY.md).

## License

[AGPL-3.0](LICENSE) — free to use and modify, including commercially; derivatives and network deployments must share their source. The 12 sample READMEs remain the property of their respective projects.
