#!/usr/bin/env python3
"""重建 12 个 T0 范本语料：README 全文 + 仓库元数据，写入 corpus/（已 gitignore）。

用途：skill 写作/审查时离线对照范本。范本版权归各自项目，故不随仓库再分发。
用法:
    python3 fetch_corpus.py [--proxy http://127.0.0.1:18118]
需要 gh CLI 已登录（或带 token 的 curl）。
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPOS = [
    "facebook/react",
    "vitejs/vite",
    "fastapi/fastapi",
    "ollama/ollama",
    "BurntSushi/ripgrep",
    "junegunn/fzf",
    "pocketbase/pocketbase",
    "huggingface/transformers",
    "ant-design/ant-design",
    "immich-app/immich",
    "lobehub/lobe-chat",
    "tw93/Pake",
]


def gh(args: str) -> str:
    r = subprocess.run(["gh", "api", args], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or f"gh api {args} failed")
    return r.stdout


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--proxy", default="", help="如 http://127.0.0.1:18118（gh 走代理时用）")
    args = ap.parse_args()

    env_proxy = args.proxy
    out = Path(__file__).resolve().parent.parent / "corpus"
    out.mkdir(exist_ok=True)

    ok = 0
    for repo in REPOS:
        slug = repo.replace("/", "_")
        try:
            if env_proxy:
                subprocess.run(["git", "config", "--global", "http.https://api.github.com/.proxy", env_proxy],
                               capture_output=True)
            meta = json.loads(gh(f"repos/{repo}"))
            json.dump({k: meta.get(k) for k in
                       ("full_name", "description", "homepage", "topics", "stargazers_count", "language")},
                      open(out / f"{slug}.json", "w"), ensure_ascii=False, indent=2)
            readme = gh(f"repos/{repo}/readme")  # raw via Accept header default json; use media type
            r = subprocess.run(["gh", "api", f"repos/{repo}/readme",
                                "-H", "Accept: application/vnd.github.raw"],
                               capture_output=True, text=True)
            readme = r.stdout if r.returncode == 0 else ""
            if not readme.strip():
                raise RuntimeError("empty readme")
            (out / f"{slug}.md").write_text(readme, encoding="utf-8")
            print(f"OK  {repo}  ({len(readme)} bytes)")
            ok += 1
        except Exception as e:  # noqa: BLE001 - report per-repo and continue
            print(f"FAIL {repo}: {e}", file=sys.stderr)

    print(f"\n{ok}/{len(REPOS)} 个范本已写入 {out}")
    print("注意：corpus/ 已 gitignore，范本内容归各自项目所有，勿再分发。")
    return 0 if ok == len(REPOS) else 1


if __name__ == "__main__":
    sys.exit(main())
