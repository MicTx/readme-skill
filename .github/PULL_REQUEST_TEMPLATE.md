## Summary

<!-- One or two sentences. Link the issue this closes: Fixes #123 -->

## Evidence

<!-- Rule changes: which repository(ies) or official docs back this? Script changes: what output changes, on which repo did you run it? -->

## Verification

<!-- How you tested. For rules/docs: `python3 scripts/audit.py <README> --name owner/repo --root .` before/after delta. For scripts: the command and its exit code. -->

## Checklist

- [ ] Docs updated in both `README.md` and `README.zh-CN.md` (or N/A)
- [ ] New/changed rules carry an evidence tag（[官方]/[共识]/[分布]/[个例]）with a source link
- [ ] No sample README text copied verbatim into the repo (copyright stays with each project)
- [ ] `python3 scripts/audit.py README.md --name MicTx/readme-skill --root .` exits 0

## AI assistance

<!-- If an AI agent helped write this PR, one line on what it did and what you verified yourself. -->
