#!/usr/bin/env python3
"""repo-readme-skill 审计脚本：对 README 做硬指标检查。

用法:
    python audit.py <README路径> [--desc "GitHub About 描述"] [--name user/repo] [--root 仓库根目录]

输出 JSON（stdout）。分两级：
  error = 违反 GitHub 官方硬规则或客观缺陷（体积超限、死链、占位符、无 License）
  hint  = T0 实践建议（standard-readme 风格项），是否采纳按仓库类型人工判断
退出码：0 无 error，1 有 error，2 文件不存在。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SHORT_DESC_MAX = 120   # standard-readme 短简介上限
TOC_THRESHOLD = 100    # 超过此行数建议有目录
RENDER_LIMIT = 500 * 1024  # GitHub 渲染截断线

# 绝对链接合法的 GitHub 页面（相对链接无法表达）
GH_PAGE_WHITELIST = (
    "/releases", "/issues", "/discussions", "/projects", "/actions",
    "/security", "/graphs", "/labels", "/wiki", "/compare", "/blob/main/LICENSE",
    "/blob/master/LICENSE",
)

SECTION_HINTS = {
    "install": ["install", "安装", "getting started", "快速开始", "快速上手", "download", "部署", "setup"],
    "usage": ["usage", "使用", "quick start", "快速开始", "example", "示例", "getting started"],
    "docs": ["documentation", "docs", "文档", "links", "链接"],
    "contributing": ["contributing", "贡献"],
    "license": ["license", "许可", "开源协议"],
}


def line_of_first_paragraph(text: str) -> str:
    """首个非空、非标题、非 badge、非 HTML 块的行（含 '> ' 标语行）= 短简介。"""
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("<"):
            continue
        if re.match(r"^\[!?[a-z_]+!\]", s, re.I) or s.startswith("[!"):
            continue
        if s in ("---", "***", "___"):
            continue
        return s
    return ""


def strip_md(s: str) -> str:
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)   # 链接取文本
    s = re.sub(r"[*_`>]", "", s)
    return s.lower()


def word_overlap(a: str, b: str) -> set[str]:
    stop = {"the", "a", "an", "for", "and", "with", "of", "to", "in", "is", "your", "it",
            "that", "this", "on", "by", "as", "or", "be", "can", "从", "的", "与", "和"}
    wa = {w for w in re.findall(r"[a-z0-9\u4e00-\u9fff]+", strip_md(a)) if w not in stop and len(w) > 1}
    wb = {w for w in re.findall(r"[a-z0-9\u4e00-\u9fff]+", strip_md(b)) if w not in stop and len(w) > 1}
    return wa & wb


def check(path: Path, desc: str, name: str, root: Path | None) -> dict:
    raw = path.read_text(encoding="utf-8", errors="replace")
    lines = raw.splitlines()
    report: dict = {"file": str(path), "errors": [], "hints": [], "info": {}}
    errs, hints = report["errors"], report["hints"]

    def error(code, msg, **kw):
        errs.append({"code": code, "message": msg, **kw})

    def hint(code, msg, **kw):
        hints.append({"code": code, "message": msg, **kw})

    # 体积（官方硬规则）
    size = len(raw.encode("utf-8"))
    report["info"]["bytes"] = size
    report["info"]["lines"] = len(lines)
    if size > RENDER_LIMIT:
        error("SIZE", f"README 源码 {size} 字节，渲染将被 GitHub 500 KiB 截断")

    # 短简介
    first = line_of_first_paragraph(raw)
    report["info"]["first_paragraph"] = first
    if not first:
        hint("DESC_MISSING", "未找到短简介行（首个非标题、非徽章的段落）")
    else:
        plain_len = len(re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", first))
        if plain_len > SHORT_DESC_MAX:
            hint("DESC_LONG", f"短简介纯文本 {plain_len} 字符 > {SHORT_DESC_MAX}（standard-readme 上限）",
                 current=first)

    # 三处一致（同义即可，按词重叠判断）
    if desc:
        report["info"]["about_desc"] = desc
        if len(desc) > SHORT_DESC_MAX:
            hint("ABOUT_LONG", f"About 描述 {len(desc)} 字符 > {SHORT_DESC_MAX}（网页端约 350 字符硬限）")
        if first:
            ov = word_overlap(desc, first)
            report["info"]["desc_overlap_words"] = sorted(ov)
            if not ov:
                hint("DESC_MISMATCH", "About 描述与 README 首段无任何实词重叠——应保证语义一致（T0 做法是同义改写或逐字复用）",
                     about=desc, readme_first=first)

    # 绝对链接指本仓库文件（releases/issues 等页面豁免）
    if name and "/" in name:
        repo = name.lower()
        bad_abs = []
        for link in re.findall(r"\]\((https?://[^)]*)\)", raw):
            low = link.lower()
            if f"github.com/{repo}/" not in low:
                continue
            tail = low.split(f"github.com/{repo}/", 1)[1]
            if tail.startswith(GH_PAGE_WHITELIST):
                continue
            if "/blob/" in tail or "/raw/" in tail or tail.startswith(("docs", "packages", "src", "examples")):
                bad_abs.append(link)
        if bad_abs:
            hint("ABS_LINK", f"{len(bad_abs)} 处用绝对 GitHub 链接指向仓库内文件，clone/换分支后会失真，应改相对路径",
                 examples=bad_abs[:3])

    # 占位符（客观缺陷）
    for i, line in enumerate(lines, 1):
        if re.search(r"\bTODO\b|待补充|【占位】|<your-", line):
            error("TODO", f"第 {i} 行有未完成占位: {line.strip()[:70]}")
            break

    # 目录建议
    h2 = [l for l in lines if re.match(r"^## (?!#)", l)]
    report["info"]["h2_sections"] = len(h2)
    anchor_links = len(re.findall(r"\]\(#[^)]+\)", raw))
    has_toc = "table of contents" in raw.lower() or "目录" in raw[:3000] or anchor_links >= len(h2)
    if len(lines) > TOC_THRESHOLD and not has_toc:
        hint("NO_TOC", f"README {len(lines)} 行，建议加目录（standard-readme：>100 行必须有；GitHub 大纲可部分替代）")

    # 章节覆盖提示
    low = raw.lower()
    missing = [k for k, kws in SECTION_HINTS.items() if not any(kw in low for kw in kws)]
    if missing:
        hint("SECTION_HINT", f"未检测到这些主题的章节（按仓库类型判断是否真的不需要）: {', '.join(missing)}")

    # 相对链接存在性（客观缺陷）
    if root and root.is_dir():
        broken = []
        for target in re.findall(r"\]\((?!https?:|mailto:|#)([^)#]+)(?:#[^)]*)?\)", raw):
            t = target.strip()
            if t and not (root / t).exists():
                broken.append(t)
        if broken:
            error("BROKEN_REL_LINK", f"{len(broken)} 个相对链接指向仓库内不存在的文件",
                  examples=broken[:5])

    # License（LICENSE 文件是硬要求、由 GitHub 侧栏判定；README 里提及是 T0 多数做法但不普遍——ollama/ant-design 就不写）
    if not re.search(r"(?i)licen|\b(MIT|Apache-?[0-9.]+|GPL-?[0-9.]*|BSD-[0-9]-Clause|UNLICENSE|MPL-[0-9.]+|AGPL[_-]?v?[0-9.]*)\b", raw):
        hint("NO_LICENSE", "README 未提及 License（T0 多数会写；若仓库根已有 LICENSE 文件可接受）")

    report["ok"] = len(errs) == 0
    return report


def main() -> int:
    ap = argparse.ArgumentParser(description="README 硬指标审计（error=官方硬规则, hint=T0 实践建议）")
    ap.add_argument("readme", type=Path)
    ap.add_argument("--desc", default="", help="GitHub About 描述原文")
    ap.add_argument("--name", default="", help='仓库全名，如 "user/repo"')
    ap.add_argument("--root", type=Path, default=None, help="仓库根目录（核对相对链接）")
    args = ap.parse_args()

    if not args.readme.exists():
        print(json.dumps({"error": f"{args.readme} 不存在"}), file=sys.stderr)
        return 2

    report = check(args.readme, args.desc, args.name, args.root)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
