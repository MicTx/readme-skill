#!/usr/bin/env python3
"""readme-skill 审计脚本：对 README 做硬指标检查，可选门面模式。

用法:
    python audit.py <README路径> [--desc "GitHub About 描述"] [--name user/repo] [--root 仓库根目录]
    python audit.py <README路径> --repo user/repo        # 门面模式：gh api 实测 About/topics/社区文件/模板/发布/分享卡

输出 JSON（stdout）。分两级：
  error = 违反 GitHub 官方硬规则或客观缺陷（体积超限、死链、占位符、topics 非法格式）
  hint  = T0 实践建议（standard-readme 风格项 / 门面装饰标准），是否采纳按仓库类型人工判断
门面模式额外输出 report["facade"]（原始观测）并把检查结果并入 errors/hints；gh 不可用或私有仓库时
记 FACADE_SKIP 跳过，不影响退出码。证据依据 references/facade-decor.md（2026-10 T0 蒸馏）。
退出码：0 无 error，1 有 error，2 文件不存在。
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

SHORT_DESC_MAX = 120   # standard-readme 短简介上限
BILINGUAL_DESC_MAX = 200  # 中文为主双语（中文主句+English gloss）上限；纯英文仍 120
TOC_THRESHOLD = 100    # 超过此行数建议有目录
RENDER_LIMIT = 500 * 1024  # GitHub 渲染截断线


def desc_limit(s: str) -> int:
    """含 CJK 时按中文为主双语口径放宽到 200；纯 ASCII 维持 standard-readme 的 120。"""
    return BILINGUAL_DESC_MAX if re.search(r"[\u4e00-\u9fff]", s) else SHORT_DESC_MAX

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
        limit = desc_limit(first)
        if plain_len > limit:
            hint("DESC_LONG", f"短简介纯文本 {plain_len} 字符 > {limit}"
                 f"（纯英文 {SHORT_DESC_MAX}；中文为主双语 {BILINGUAL_DESC_MAX}）",
                 current=first)

    # 三处一致（同义即可，按词重叠判断）
    if desc:
        report["info"]["about_desc"] = desc
        dlimit = desc_limit(desc)
        if len(desc) > dlimit:
            hint("ABOUT_LONG", f"About 描述 {len(desc)} 字符 > {dlimit}（网页端约 350 字符硬限）")
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

    # badge 装饰层（T0 标准：全包链接、样式统一、单行 4–6 个；见 references/facade-decor.md）
    md_linked = re.findall(r"\[!\[[^\]]*\]\([^)]+\)\]\([^)]+\)", raw)
    html_linked = [s for s in re.findall(r'<a\s[^>]*href="[^"]+"[^>]*>\s*<img\s+(?:[^>]*\s)?src="([^"]+)"', raw)
                   if "shields.io" in s or "badge" in s.lower() or "status.svg" in s]
    linked = len(md_linked) + len(html_linked)
    bare = re.findall(r"(?<!\[)!\[[^\]]*\]\((https?://img\.shields\.io[^)]+)\)", raw)
    shield_urls = re.findall(r'\((https?://img\.shields\.io[^)\s"]+)', raw) + \
                  re.findall(r'src="(https?://img\.shields\.io[^"\s]+)', raw)
    styles = set()
    for u in shield_urls:
        m = re.search(r"style=([a-z-]+)", u)
        styles.add(m.group(1) if m else "flat")
    report["info"]["badges"] = {"linked": linked, "bare": len(bare), "styles": sorted(styles)}
    if bare:
        hint("BADGE_BARE", f"{len(bare)} 个裸 badge 未包链接（T0 范本 41/41 全部包裹）", examples=bare[:3])
    if len(styles) > 1:
        hint("BADGE_STYLE_MIX", f"badge 样式混用 {sorted(styles)}（T0 零混用，全 README 统一一种）")
    if linked > 6:
        hint("BADGE_MANY", f"badge 共 {linked} 个 > 6，建议拆两行：项目健康度 / 社区（ant-design 式）")

    report["ok"] = len(errs) == 0
    return report


# ---------------- 门面模式（--repo：gh api 实测仓库门面） ----------------

# 含 react 白帽页 / Huntr 赏金平台等合法外部渠道；邮箱信号含混淆写法（"support at pocketbase.io"、"AT gmail DOT com"）
SECURITY_CHANNEL_PATTERNS = (
    r"/security", r"advisories/new", r"security@", r"security\.txt", r"whitehat", r"huntr",
    r"[\w.+-]+@[\w-]+\.\w+",                              # 任一明文邮箱（SECURITY.md 里的邮箱即联系渠道）
    r"[\w.+-]+\s+(?:at|AT)\s+[\w-]+\.(?:com|io|dev|net|org|me|app|co|ai)\b",   # "support at pocketbase.io"
    r"\b(?:AT|at)\s+[\w.-]+\s+(?:DOT|dot)\s+\w+",         # "AT gmail DOT com"
)

FUNDING_KEYS = {"github", "patreon", "open_collective", "ko_fi", "tidelift", "community_bridge",
                "polar", "issuehunt", "liberapay", "buy_me_a_coffee", "thanks_dev", "custom"}


def gh_api(path: str):
    """gh api 取 JSON；404/不存在返回 None；其他失败抛 RuntimeError。"""
    try:
        r = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    except FileNotFoundError as e:
        raise RuntimeError(f"gh CLI 不可用: {e}") from e
    if r.returncode != 0:
        err = (r.stderr or "") + (r.stdout or "")
        if "404" in err or "Not Found" in err:
            return None
        raise RuntimeError(f"gh api {path}: {err.strip()[:160]}")
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return None


def gh_raw(path: str) -> str | None:
    """gh api 取文件原文（Accept raw）；不存在返回 None，其他失败抛 RuntimeError。"""
    try:
        r = subprocess.run(["gh", "api", path, "-H", "Accept: application/vnd.github.raw"],
                           capture_output=True, text=True)
    except FileNotFoundError as e:
        raise RuntimeError(f"gh CLI 不可用: {e}") from e
    body = r.stdout or ""
    # 404 时 gh 可能以退出码 0 返回错误 JSON 体（蒸馏实测），双重判定
    if r.returncode != 0 or '"status": "404"' in body or '"message": "Not Found"' in body:
        return None
    return body


def social_preview_kind(name: str) -> str:
    """og:image 域名二分：custom=已设自定义分享卡 / default=默认动态卡 / ''=无法判定（网络失败或私有）。"""
    try:
        req = urllib.request.Request(f"https://github.com/{name}", headers={"User-Agent": "readme-skill-audit"})
        html = urllib.request.urlopen(req, timeout=10).read(400_000).decode("utf-8", "replace")
    except Exception:
        return ""
    m = re.search(r'property="og:image"\s+content="(https://[^"]+)"', html)
    if not m:
        return ""
    url = m.group(1)
    if "repository-images.githubusercontent.com" in url:
        return "custom"
    if "opengraph.githubassets.com" in url:
        return "default"
    return ""


def facade_check(repo: str, meta: dict) -> tuple[list, list, dict]:
    """门面检查（About/topics/社区文件/模板/发布/分享卡）。返回 (errors, hints, info)。

    依据 references/facade-decor.md。原则：官方硬规则（topics 格式/数量）进 error；
    T0 实践进 hint；org 回退链先排除再判缺失；health_percentage 只记录不当门槛。
    """
    errs: list = []
    hints: list = []
    info: dict = {"repo": repo}

    def error(code, msg, **kw):
        errs.append({"code": code, "message": msg, **kw})

    def hint(code, msg, **kw):
        hints.append({"code": code, "message": msg, **kw})

    owner = repo.split("/")[0]

    # About / topics / homepage / 开关（仓库元数据）
    desc = meta.get("description") or ""
    info["about_desc"] = desc
    if not desc:
        hint("ABOUT_MISSING", "About 描述为空——T0 全部有 35–120 字符描述（含品类词+差异化定语）")
    elif len(desc) > desc_limit(desc):
        hint("ABOUT_LONG", f"About 描述 {len(desc)} 字符超限（纯英文 {SHORT_DESC_MAX} / 中文为主双语 {BILINGUAL_DESC_MAX}）")
    info["homepage"] = meta.get("homepage")
    info["has_discussions"] = meta.get("has_discussions")
    info["has_wiki"] = meta.get("has_wiki")
    if not meta.get("has_discussions"):
        hint("DISCUSSIONS_OFF", "Discussions 未开启（T0 8/10 默认开；有外置社区载体可忽略）")

    topics = meta.get("topics") or []
    info["topics"] = topics
    bad_fmt = [t for t in topics if not re.fullmatch(r"[a-z0-9-]+", t) or len(t) > 50]
    if bad_fmt:
        error("TOPIC_FORMAT", f"topics 非法格式（仅小写字母/数字/连字符，单个 ≤50 字符）: {bad_fmt}")
    if len(topics) > 20:
        error("TOPIC_COUNT", f"topics {len(topics)} 个 > 20（GitHub 官方上限）")
    if len(topics) < 4:
        hint("TOPICS_FEW", f"topics 仅 {len(topics)} 个——T0 配方 4–20 个覆盖五层（自身名/语言/品类/领域/生态）")

    # 社区健康文件（先 repo，后 {owner}/.github 组织回退；profile 值优先）
    profile = gh_api(f"repos/{repo}/community/profile") or {}
    pfiles = profile.get("files") or {}
    info["health_percentage"] = profile.get("health_percentage")

    def resolve(fname: str, profile_key: str, paths: tuple) -> str:
        """返回 repo / org / ''（先 profile 值——注意 GitHub 会把 {org}/.github 回退计入
        profile（如 fastapi 的 PR 模板），从 html_url 判实际位置；再本仓库两位置、组织仓库两位置）。"""
        pv = pfiles.get(profile_key) if profile_key else None
        if pv:
            url = pv.get("html_url", "") if isinstance(pv, dict) else str(pv)
            return "org" if f"/{owner}/.github/" in url else "repo"
        for p in paths:
            if gh_api(f"repos/{repo}/contents/{p}") is not None:
                return "repo"
        for p in paths:
            if gh_api(f"repos/{owner}/.github/contents/{p}") is not None:
                return "org"
        return ""

    where = {
        "contributing": resolve("CONTRIBUTING", "contributing", ("CONTRIBUTING.md", ".github/CONTRIBUTING.md", "docs/CONTRIBUTING.md")),
        "code_of_conduct": resolve("CoC", "code_of_conduct", ("CODE_OF_CONDUCT.md", ".github/CODE_OF_CONDUCT.md", "docs/CODE_OF_CONDUCT.md")),
        "security": resolve("SECURITY", "", ("SECURITY.md", ".github/SECURITY.md", "docs/SECURITY.md", ".github/SECURITY/SECURITY.md")),
        "pull_request_template": resolve("PR 模板", "pull_request_template",
                                         (".github/PULL_REQUEST_TEMPLATE.md", "PULL_REQUEST_TEMPLATE.md", "docs/PULL_REQUEST_TEMPLATE.md")),
        "funding": resolve("FUNDING", "", (".github/FUNDING.yml",)),
    }
    info["community_files"] = where

    if not where["contributing"]:
        hint("CONTRIB_MISSING", "无 CONTRIBUTING.md（标配层 8/8；多仓库组织可放 {org}/.github 共享）")
    if not where["code_of_conduct"]:
        hint("COC_MISSING", "无 CODE_OF_CONDUCT.md（信任层；直接用 Contributor Covenant ≥2.0 全文，零自撰）")
    if not where["security"]:
        hint("SECURITY_MISSING", "无 SECURITY.md（标配层 8/8 都有；需私密上报渠道）")
    if not where["pull_request_template"]:
        hint("PR_TPL_MISSING", "无 PR 模板（6/8 范本放 .github/PULL_REQUEST_TEMPLATE.md）")

    # SECURITY 内容信号：私密渠道
    if where["security"] == "repo":
        body = gh_raw(f"repos/{repo}/contents/SECURITY.md") or gh_raw(f"repos/{repo}/contents/.github/SECURITY.md") or ""
    elif where["security"] == "org":
        body = gh_raw(f"repos/{owner}/.github/contents/SECURITY.md") or ""
    else:
        body = ""
    pvr = gh_api(f"repos/{repo}/private-vulnerability-reporting") or {}
    info["private_vuln_reporting"] = pvr.get("enabled")
    if body and not any(re.search(p, body, re.I) for p in SECURITY_CHANNEL_PATTERNS):
        if not pvr.get("enabled"):
            hint("SECURITY_CHANNEL", "SECURITY.md 未检出私密上报渠道（/security 链接、明文或混淆安全邮箱、security.txt、白帽页/赏金平台均无）且私密报告开关未开")

    # issue 模板：profile 恒为 null（目录式），必须列目录
    itpl = gh_api(f"repos/{repo}/contents/.github/ISSUE_TEMPLATE")
    itpl_names = [f.get("name") for f in itpl] if isinstance(itpl, list) else []
    info["issue_templates"] = itpl_names
    if not itpl_names:
        hint("ISSUE_TPL_MISSING", "无 .github/ISSUE_TEMPLATE/（门面最小集 8/8；bug 模板用 YAML issue forms）")
    elif "config.yml" not in itpl_names and "config.yaml" not in itpl_names:
        hint("ISSUE_TPL_NO_CONFIG", "ISSUE_TEMPLATE/ 缺 config.yml（8/8 都有；负责 blank_issues_enabled 与 contact_links 问答分流）")

    # FUNDING key 白名单（仅本仓库文件校验内容）
    if where["funding"] == "repo":
        fbody = gh_raw(f"repos/{repo}/contents/.github/FUNDING.yml") or ""
        bad_keys = [k for k in re.findall(r"^([a-z_]+)\s*:", fbody, re.M) if k and k not in FUNDING_KEYS]
        if bad_keys:
            hint("FUNDING_KEY", f"FUNDING.yml 含非白名单 key {bad_keys}（官方仅 12 个 key 生效）")

    # 发布线：tag 前缀一致性、release 标题、冷启动降级
    rel = gh_api(f"repos/{repo}/releases?per_page=5")
    tags = gh_api(f"repos/{repo}/tags?per_page=8")
    info["releases_checked"] = isinstance(rel, list) and len(rel) or 0
    if isinstance(rel, list) and not rel:
        hint("RELEASE_NONE", "尚无 release（冷启动适用外：发第一个 v+semver tag 时记得建 release）")
    if isinstance(tags, list) and tags:
        prefixes = set()
        for t in tags:
            name = t.get("name") or ""
            m = re.match(r"^(v)(\d)", name)
            prefixes.add("v" if m else ("bare" if re.match(r"^\d", name) else "other"))
        info["tag_style"] = sorted(prefixes)
        versionish = {p for p in prefixes if p in ("v", "bare")}
        if len(versionish) > 1:
            hint("TAG_INCONSISTENT", "tag 前缀混用（v 前缀与裸版本并存）——T0 全仓库一致（8/10 用小写 v）")
    if isinstance(rel, list) and rel:
        latest = rel[0]
        info["latest_release"] = {"tag": latest.get("tag_name"), "name": latest.get("name"),
                                  "prerelease": latest.get("prerelease"),
                                  "assets": len(latest.get("assets") or [])}

    # social preview（仅公开仓库；网络失败静默跳过）
    if meta.get("private") is False:
        kind = social_preview_kind(repo)
        info["social_preview"] = kind
        if kind == "default":
            hint("SOCIAL_PREVIEW_DEFAULT", "未设自定义 social preview（可选装饰非强制，T0 6/10 已设；要设：1280×640 PNG <1MB，Settings → Social preview 上传）")

    return errs, hints, info



def main() -> int:
    ap = argparse.ArgumentParser(description="README 硬指标审计（error=官方硬规则, hint=T0 实践建议）")
    ap.add_argument("readme", type=Path)
    ap.add_argument("--desc", default="", help="GitHub About 描述原文")
    ap.add_argument("--name", default="", help='仓库全名，如 "user/repo"')
    ap.add_argument("--root", type=Path, default=None, help="仓库根目录（核对相对链接）")
    ap.add_argument("--repo", default="", help="门面模式：gh api 实测 user/repo 的 About/topics/社区文件/模板/发布/分享卡")
    args = ap.parse_args()

    if not args.readme.exists():
        print(json.dumps({"error": f"{args.readme} 不存在"}), file=sys.stderr)
        return 2

    desc = args.desc
    meta: dict = {}
    if args.repo:
        try:
            meta = gh_api(f"repos/{args.repo}") or {}
        except RuntimeError as e:
            print(f"门面模式初始化失败：{e}", file=sys.stderr)
            meta = {}
        if not desc:
            desc = meta.get("description") or ""

    report = check(args.readme, desc, args.name or args.repo, args.root)

    if args.repo:
        if meta:
            f_errs, f_hints, f_info = facade_check(args.repo, meta)
            report["errors"].extend(f_errs)
            report["hints"].extend(f_hints)
            report["facade"] = f_info
        else:
            report["facade"] = {"repo": args.repo, "skipped": "仓库不可访问（私有/不存在）或 gh 不可用"}
        report["ok"] = len(report["errors"]) == 0

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
