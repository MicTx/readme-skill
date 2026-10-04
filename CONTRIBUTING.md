# Contributing to repo-readme-skill

Thanks for helping the standard get sharper. This repo is distilled evidence about how top-tier repositories present themselves — the best contributions keep it that way.

## Finding work

Browse [open issues](https://github.com/MicTx/repo-readme-skill/issues). Bug reports land with the `pending triage` label first; rule-change proposals are `enhancement`.

## Ground rule: evidence or it didn't happen

Every rule in `references/` carries an evidence tag — [官方] (official GitHub docs), [共识] (≥5 of the 12 samples agree), [分布] (2–4 samples), [个例] (one sample, marked as such). A contribution that adds or changes a rule must say **which repository or official document demonstrates it**, with a link. Unverifiable taste ("I think badges look better centered") is the kind of guidance this project exists to replace.

## Local setup

Python 3 only, no dependencies:

```bash
git clone https://github.com/MicTx/repo-readme-skill.git
cd repo-readme-skill
python3 scripts/audit.py README.md --name MicTx/repo-readme-skill --root .   # should exit 0
```

Optional offline corpus (12 full sample READMEs + facade metadata; gitignored, never redistribute):

```bash
python3 scripts/fetch_corpus.py   # requires gh CLI authenticated
```

## Pull requests

- Fill in the PR template — the verification section wants an `audit.py` before/after delta for rule or script changes.
- Keep the bilingual pair in sync: `README.md` and `README.zh-CN.md` change together (same for the checklist if both halves of a section are affected).
- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/) (`docs(rules): ...`, `fix(audit): ...`).
- Never paste sample README text verbatim into this repo — paraphrase the pattern, link the source.

## Code of conduct

By participating you agree to uphold the [Contributor Covenant](CODE_OF_CONDUCT.md).
