# Security Policy

## Reporting a vulnerability

Please report vulnerabilities **privately** — do not open a public issue:

- Preferred: GitHub's private vulnerability reporting — the **Report a vulnerability** button on the [security advisories page](https://github.com/MicTx/readme-skill/security/advisories).
- Or email **dawudcn@qq.com** with `[security]` in the subject.

Response is best-effort, usually within a few weeks. This is a docs-and-scripts side project, not a service — no SLA.

## Scope

In scope:

- `scripts/audit.py` and `scripts/fetch_corpus.py` — they run on your machine and make read-only calls to `api.github.com`; anything that could exfiltrate data, execute unintended code, or hit the GitHub API with your credentials in unexpected ways matters.

Out of scope:

- The content of the 12 sample repositories (they are references, not dependencies).
- Rule/wording disagreements in `references/` — those are regular issues.
- Reports from automated scanners without a human-verified reproduction.

## Supported versions

The latest [release](https://github.com/MicTx/readme-skill/releases) only.
