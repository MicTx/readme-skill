#!/usr/bin/env python3
"""重建 12 个 T0 范本语料：README 全文 + 仓库元数据 + 门面维度数据，写入 corpus/（已 gitignore）。

用途：skill 写作/审查时离线对照范本。范本版权归各自项目，故不随仓库再分发。
抓取维度：
  - {slug}.md   README 全文
  - {slug}.json 元数据（description/homepage/topics/stars/language）
                + facade 门面维度（2026-10 蒸馏口径）：community profile、.github 顶层清单、
                  ISSUE_TEMPLATE 清单、FUNDING.yml 原文（如有）、最新 release 概要、discussions 开关
用法:
    python3 fetch_corpus.py [--proxy http://127.0.0.1:18118] [--repos owner/name[,owner/name]]
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


def gh_maybe(path: str) -> str | None:
    """gh api；404/不存在返回 None；其他失败也返回 None（语料抓取尽力而为，不中断）。"""
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    body = r.stdout or ""
    if r.returncode != 0 or '"message": "Not Found"' in body or '"status": "404"' in body:
        return None
    return body or None


def facade_data(repo: str) -> dict:
    """门面维度数据（对齐 references/facade-decor.md 的审查口径）。"""
    out: dict = {}
    try:
        profile = json.loads(gh(f"repos/{repo}/community/profile"))
        files = profile.get("files") or {}
        out["health_percentage"] = profile.get("health_percentage")
        # 值为 null 表示缺失；dict 时取 html_url 便于判 org 回退实际位置
        out["community_files"] = {
            k: (v.get("html_url") if isinstance(v, dict) else v) for k, v in files.items()
            if k in ("readme", "license", "contributing", "code_of_conduct",
                     "issue_template", "pull_request_template")
        }
    except Exception:  # noqa: BLE001
        out["health_percentage"] = None
    dot = gh_maybe(f"repos/{repo}/contents/.github")
    out["dotgithub"] = sorted(f.get("name") for f in json.loads(dot)) if dot else []
    itpl = gh_maybe(f"repos/{repo}/contents/.github/ISSUE_TEMPLATE")
    out["issue_templates"] = sorted(f.get("name") for f in json.loads(itpl)) if itpl else []
    funding = gh_maybe('repos/{r}/contents/.github/FUNDING.yml -H "Accept: application/vnd.github.raw"'.replace("{r}", repo))
    out["funding_yml"] = funding
    rel = gh_maybe(f"repos/{repo}/releases/latest")
    if rel:
        rj = json.loads(rel)
        out["latest_release"] = {
            "tag": rj.get("tag_name"), "name": rj.get("name"),
            "prerelease": rj.get("prerelease"),
            "assets": [a.get("name") for a in (rj.get("assets") or [])][:30],
            "body_head": (rj.get("body") or "")[:800],
        }
    else:
        out["latest_release"] = None
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--proxy", default="", help="如 http://127.0.0.1:18118（gh 走代理时用）")
    ap.add_argument("--repos", default="", help="只抓指定范本，逗号分隔 owner/name（调试用）")
    args = ap.parse_args()

    env_proxy = args.proxy
    repos = [r.strip() for r in args.repos.split(",") if r.strip()] or REPOS
    out = Path(__file__).resolve().parent.parent / "corpus"
    out.mkdir(exist_ok=True)

    ok = 0
    for repo in repos:
        slug = repo.replace("/", "_")
        try:
            if env_proxy:
                subprocess.run(["git", "config", "--global", "http.https://api.github.com/.proxy", env_proxy],
                               capture_output=True)
            meta = json.loads(gh(f"repos/{repo}"))
            record = {k: meta.get(k) for k in
                      ("full_name", "description", "homepage", "topics", "stargazers_count", "language",
                       "has_discussions", "has_wiki")}
            r = subprocess.run(["gh", "api", f"repos/{repo}/readme",
                                "-H", "Accept: application/vnd.github.raw"],
                               capture_output=True, text=True)
            readme = r.stdout if r.returncode == 0 else ""
            if not readme.strip():
                raise RuntimeError("empty readme")
            record["facade"] = facade_data(repo)
            json.dump(record, open(out / f"{slug}.json", "w"), ensure_ascii=False, indent=2)
            (out / f"{slug}.md").write_text(readme, encoding="utf-8")
            print(f"OK  {repo}  ({len(readme)} bytes, facade: "
                  f"health={record['facade'].get('health_percentage')}, "
                  f"itpl={len(record['facade'].get('issue_templates') or [])})")
            ok += 1
        except Exception as e:  # noqa: BLE001 - report per-repo and continue
            print(f"FAIL {repo}: {e}", file=sys.stderr)

    print(f"\n{ok}/{len(repos)} 个范本已写入 {out}")
    print("注意：corpus/ 已 gitignore，范本内容归各自项目所有，勿再分发。")
    return 0 if ok == len(repos) else 1


if __name__ == "__main__":
    sys.exit(main())
