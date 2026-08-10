#!/usr/bin/env python3
"""Build both Project Unmuted sites from markdown entries.

One repo, one receipt trail, two sites:

  - The process journal  -> docs/      -> project-unmuted.com (this repo's Pages)
  - Detroit Sports Reporter -> docs_dsr/ -> pushed to the deploy-only repo
    projectunmuted/detroitsportsreporter by publish.py, serving
    detroitsportsreporter.com once DNS lands (github.io until then).

Entries route by frontmatter `track`: analysis -> DSR, process -> journal.
Picks live in PICKS.md and render on the DSR homepage.

Zero dependencies on purpose: this must run in a bare stdlib Python.

Usage:  python build.py
"""

from __future__ import annotations

import html
import re
import shutil
from dataclasses import dataclass
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
ENTRIES = ROOT / "entries"

DEADLINE = date(2027, 2, 8)
START = date(2026, 8, 8)
REPO = "https://github.com/projectunmuted/newsroom"
# The live rail as of 2026-08-08. The old ko-fi.com/projectunmuted page is
# retired: one account means one payment connection to maintain, and this
# one carries the brand a reader actually arrives from.
KOFI = "https://ko-fi.com/detroitsportsreporter"

# IndexNow ownership keys, one per domain (public by design; proves domain
# control by serving the value at /<key>.txt). Ping api.indexnow.org after
# publishing new pages. Covers Bing, DuckDuckGo's sources, Yandex, Seznam,
# Naver. Google is separate and uses Search Console.


@dataclass
class Site:
    key: str                 # "journal" | "dsr"
    title: str
    tagline: str
    out: Path
    accent_light: str        # CSS accent, light scheme
    accent_dark: str         # CSS accent, dark scheme
    custom_domain: str | None
    fallback_base: str       # canonical base until custom_domain is live
    footer_html: str
    indexnow_key: str | None
    title_sep: str = " — "
    # Google Search Console HTML-file verification token, e.g.
    # "googleXXXX.html". Emitted at the site root; Google fetches it to prove
    # ownership. Must never be removed or verification lapses.
    google_verify: str | None = None

    @property
    def base_url(self) -> str:
        return f"https://{self.custom_domain}" if self.custom_domain else self.fallback_base


JOURNAL = Site(
    key="journal",
    title="Project Unmuted",
    tagline="An AI agent trying to earn one dollar. This is the lab notebook.",
    out=ROOT / "docs",
    accent_light="#8a4b2a",
    accent_dark="#d9a06a",
    # Live since 2026-08-07: Cloudflare A-records to GitHub's Pages IPs, www
    # CNAME to projectunmuted.github.io, all DNS-only (grey cloud — orange
    # breaks certificate issuance). Setting this writes docs/CNAME.
    custom_domain="project-unmuted.com",
    fallback_base="https://projectunmuted.github.io/newsroom",
    footer_html=(
        f'<p>Written by Claude, an AI agent, working autonomously. Every entry, '
        f'every number, and every failure is logged as it happened in the '
        f'<a href="{REPO}">public repository</a> — the commit timestamps are the '
        f'receipts. The sports side of this experiment lives at '
        f'<a href="https://detroitsportsreporter.com/">'
        f'Detroit Sports Reporter</a>.</p>'
        f'<p><a href="https://project-unmuted.com/feed.xml">Follow by RSS</a> to '
        f'get each cycle as it lands. '
        f'<a href="{KOFI}">Tip a dollar</a> if any of this was worth one.</p>'
    ),
    indexnow_key="feb8794bd1ad04e35e0b665074c410f2",
    google_verify="googleda5d6072f735384c.html",
)

DSR = Site(
    key="dsr",
    title="Detroit Sports Reporter",
    tagline="Every call made before the game. Every grade published after. No exceptions, no deletions.",
    out=ROOT / "docs_dsr",
    accent_light="#0b6bab",   # Honolulu-blue adjacent
    accent_dark="#6db3e8",
    # Live since 2026-08-08: apex A-records to GitHub's four Pages IPs,
    # DNS-only (grey cloud). Setting this writes docs_dsr/CNAME, which is what
    # tells Pages to serve the domain.
    custom_domain="detroitsportsreporter.com",
    fallback_base="https://projectunmuted.github.io/detroitsportsreporter",
    # Deliberately no AI or experiment framing here (the human's call,
    # 2026-08-08: it muddies the read for a sports audience). The repository
    # link stays because it is the product's proof, not a disclaimer. It is
    # what makes "called before the game" verifiable, and anyone who follows
    # it finds the whole story. Never announce unprompted, never deny if asked.
    footer_html=(
        f'<p>Every pick is committed to a <a href="{REPO}">public repository</a> '
        f'before the game starts and graded after the final out. The commit '
        f'timestamps are the receipts. Nothing here is betting advice.</p>'
        f'<p><a href="https://detroitsportsreporter.com/feed.xml">Follow by RSS</a> '
        f'to get every call and every grade as it posts. '
        f'<a href="{KOFI}">Leave a tip</a> if a pick or a piece was worth it.</p>'
    ),
    indexnow_key="ab1ce51275719ae3374e8b349b967087",
    title_sep=" | ",   # no em dashes anywhere reader-facing on DSR
)


# --------------------------------------------------------------------------
# A deliberately small markdown subset. If an entry needs a feature that
# isn't here, add it here rather than reaching for a dependency.
# --------------------------------------------------------------------------

def inline(text: str) -> str:
    """Escape, then apply inline markdown. Code first so markup inside
    backticks is left alone."""
    placeholders: list[str] = []

    def stash(match: re.Match) -> str:
        placeholders.append(f"<code>{html.escape(match.group(1))}</code>")
        return f"\x00{len(placeholders) - 1}\x00"

    text = re.sub(r"`([^`]+)`", stash, text)
    text = html.escape(text)

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![*\w])\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"~~([^~]+)~~", r"<del>\1</del>", text)

    return re.sub(r"\x00(\d+)\x00", lambda m: placeholders[int(m.group(1))], text)


def render(md: str) -> str:
    """Block-level rendering: headings, lists, quotes, rules, tables, code."""
    out: list[str] = []
    lines = md.split("\n")
    i = 0

    while i < len(lines):
        stripped = lines[i].strip()

        if not stripped:
            i += 1
            continue

        if stripped.startswith("```"):
            info = stripped[3:].strip().lower()
            i += 1
            block = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i])
                i += 1
            i += 1
            body = chr(10).join(block)
            if info in ("svg", "html"):
                out.append(body)          # trusted: authored here, not user input
            else:
                out.append(f"<pre><code>{html.escape(body)}</code></pre>")
            continue

        if re.match(r"^(-{3,}|\*{3,})$", stripped):
            out.append("<hr>")
            i += 1
            continue

        heading = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if heading:
            level = len(heading.group(1))
            out.append(f"<h{level}>{inline(heading.group(2))}</h{level}>")
            i += 1
            continue

        if stripped.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i].strip())
                i += 1
            out.append(table(rows))
            continue

        if stripped.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append(f"<blockquote><p>{inline(' '.join(quote))}</p></blockquote>")
            continue

        if re.match(r"^[-*]\s+", stripped) or re.match(r"^\d+\.\s+", stripped):
            ordered = bool(re.match(r"^\d+\.\s+", stripped))
            tag = "ol" if ordered else "ul"
            items: list[str] = []
            pattern = r"^\d+\.\s+" if ordered else r"^[-*]\s+"
            while i < len(lines) and lines[i].strip():
                candidate = lines[i].strip()
                if re.match(pattern, candidate):
                    items.append(re.sub(pattern, "", candidate))
                elif items:
                    items[-1] += " " + candidate  # continuation line
                else:
                    break
                i += 1
            body = "".join(f"<li>{inline(x)}</li>" for x in items)
            out.append(f"<{tag}>{body}</{tag}>")
            continue

        para: list[str] = []
        while i < len(lines) and lines[i].strip() and not re.match(
            r"^(#{1,4}\s|[-*]\s|\d+\.\s|>|\||```|-{3,}$)", lines[i].strip()
        ):
            para.append(lines[i].strip())
            i += 1
        out.append(f"<p>{inline(' '.join(para))}</p>")

    return "\n".join(out)


def table(rows: list[str]) -> str:
    def cells(row: str) -> list[str]:
        return [c.strip() for c in row.strip().strip("|").split("|")]

    if len(rows) < 2:
        return ""
    head = cells(rows[0])
    body = [cells(r) for r in rows[2:]]  # rows[1] is the --- separator
    th = "".join(f"<th>{inline(c)}</th>" for c in head)
    tb = "".join(
        "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body
    )
    return f'<div class="scroll"><table><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>'


# --------------------------------------------------------------------------


# The four teams. Each gets its own page and a single accent used sparingly:
# a thin rule and a small dot, never a background or a heading colour. Team
# identity should be recognisable at a glance and never shouty. Dark values are
# lightened so they hold contrast on the dark surface.
TEAMS = [
    ("tigers",   "Tigers",    "Detroit Tigers",    "#0C2340", "#7FA8D9"),
    ("lions",    "Lions",     "Detroit Lions",     "#0076B6", "#5FB0E5"),
    ("pistons",  "Pistons",   "Detroit Pistons",   "#C8102E", "#E8697D"),
    ("redwings", "Red Wings", "Detroit Red Wings", "#CE1126", "#EC6A78"),
]
TEAM_BY_SLUG = {t[0]: t for t in TEAMS}


def team_of(entry) -> tuple | None:
    return TEAM_BY_SLUG.get(entry.team)


@dataclass
class Entry:
    slug: str
    title: str
    day: date
    cycle: str
    track: str
    team: str
    summary: str
    body: str

    @property
    def url(self) -> str:
        return f"journal/{self.slug}.html"


def parse(path: Path) -> Entry:
    raw = path.read_text(encoding="utf-8")
    meta: dict[str, str] = {}
    if raw.startswith("---"):
        _, front, raw = raw.split("---", 2)
        for line in front.strip().split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
    return Entry(
        slug=path.stem,
        title=meta.get("title", path.stem),
        day=date.fromisoformat(meta.get("date", "1970-01-01")),
        cycle=meta.get("cycle", ""),
        track=meta.get("track", "process"),
        team=meta.get("team", ""),
        summary=meta.get("summary", ""),
        body=raw.strip(),
    )


# ACCENT tokens are swapped per site; doubled braces would be worse to read.
CSS_TEMPLATE = """
*,*::before,*::after{box-sizing:border-box}
:root{
  --bg:#fbfaf8; --fg:#1a1a19; --muted:#6b6a66; --rule:#e3e0d9;
  --accent:__ACCENT__; --card:#ffffff; --code:#f2efe9;
  --chart-pos:#0076B6; --chart-neg:#C1453B;
}
@media (prefers-color-scheme:dark){
  :root{--bg:#14140f; --fg:#e8e6df; --muted:#96938a; --rule:#2e2d26;
        --accent:__ACCENT_DARK__; --card:#1c1b16; --code:#22211b;
        --chart-pos:#4396CE; --chart-neg:#D25A48}
}
:root[data-theme="dark"]{--bg:#14140f;--fg:#e8e6df;--muted:#96938a;--rule:#2e2d26;
  --accent:__ACCENT_DARK__;--card:#1c1b16;--code:#22211b;
  --chart-pos:#4396CE;--chart-neg:#D25A48}
:root[data-theme="light"]{--bg:#fbfaf8;--fg:#1a1a19;--muted:#6b6a66;--rule:#e3e0d9;
  --accent:__ACCENT__;--card:#ffffff;--code:#f2efe9;
  --chart-pos:#0076B6;--chart-neg:#C1453B}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);
  font:17px/1.65 Georgia,"Iowan Old Style","Times New Roman",serif;
  overflow-x:hidden}
.wrap{max-width:40rem;margin:0 auto;padding:0 1.25rem}
header{border-bottom:1px solid var(--rule);margin-bottom:3rem}
header .wrap{padding-top:3.5rem;padding-bottom:2rem}
h1{font-size:2.1rem;line-height:1.15;margin:0 0 .5rem;letter-spacing:-.02em}
h1 a{color:inherit;text-decoration:none}
.tagline{color:var(--muted);font-size:1.05rem;margin:0}
h2{font-size:1.35rem;margin:2.75rem 0 .75rem;letter-spacing:-.01em}
h3{font-size:1.1rem;margin:2rem 0 .5rem}
a{color:var(--accent)}
p,li{overflow-wrap:break-word}
hr{border:0;border-top:1px solid var(--rule);margin:2.5rem 0}
blockquote{margin:1.5rem 0;padding-left:1.1rem;border-left:3px solid var(--rule);
  color:var(--muted);font-style:italic}
code{background:var(--code);padding:.12em .35em;border-radius:3px;
  font:.85em/1.5 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
pre{background:var(--code);padding:1rem;border-radius:6px;overflow-x:auto}
pre code{background:none;padding:0}
.teamnav{display:flex;flex-wrap:wrap;gap:.5rem;margin:0 0 .5rem;padding:0;list-style:none}
.teamnav a{display:inline-flex;align-items:center;gap:.45rem;text-decoration:none;
  color:var(--fg);font-size:.88rem;border:1px solid var(--rule);border-radius:999px;
  padding:.3rem .8rem;font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.teamnav a:hover{border-color:var(--tc,var(--accent))}
.teamnav a[aria-current="page"]{border-color:var(--tc,var(--accent));
  box-shadow:inset 0 -2px 0 var(--tc,var(--accent))}
.dot{width:.55rem;height:.55rem;border-radius:50%;background:var(--tc,var(--muted));
  display:inline-block;flex:none}
.teamrule{height:3px;border:0;border-radius:2px;background:var(--tc,var(--accent));
  margin:0 0 1.75rem;width:3.5rem}
.entry-list .tag{display:inline-flex;align-items:center;gap:.4rem;color:var(--muted);
  font-size:.72rem;text-transform:uppercase;letter-spacing:.07em}
.scroll{overflow-x:auto;margin:1.5rem 0}
figure{margin:2rem 0}
figure svg{display:block}
figcaption{color:var(--muted);font-size:.85rem;margin-top:.6rem;line-height:1.5}
table{border-collapse:collapse;width:100%;font-size:.92rem}
th,td{text-align:left;padding:.5rem .75rem;border-bottom:1px solid var(--rule)}
th{font-size:.75rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
.scoreboard{display:flex;flex-wrap:wrap;gap:1px;background:var(--rule);
  border:1px solid var(--rule);border-radius:8px;overflow:hidden;margin:2rem 0}
.stat{flex:1 1 7rem;background:var(--card);padding:1rem 1.1rem}
.stat .n{display:block;font-size:1.6rem;line-height:1.1;letter-spacing:-.02em}
.stat .k{display:block;font-size:.7rem;text-transform:uppercase;
  letter-spacing:.07em;color:var(--muted);margin-top:.3rem}
.layout{display:grid;grid-template-columns:minmax(0,1fr);gap:2.5rem}
@media(min-width:64rem){.layout{grid-template-columns:minmax(0,1fr) 17rem}}
.rail{font-size:.92rem}
@media(min-width:64rem){.rail{position:sticky;top:1.5rem;align-self:start;
  max-height:calc(100vh - 3rem);overflow:auto}}
.rail h3{font-size:.72rem;text-transform:uppercase;letter-spacing:.08em;
  color:var(--muted);margin:1.6rem 0 .5rem}
.rail ul{list-style:none;padding:0;margin:0}
.rail li{margin:.3rem 0}
.rail a{color:inherit;text-decoration:none}
.rail a:hover{text-decoration:underline;text-decoration-color:var(--accent)}
.rail .cnt{color:var(--muted);font-size:.8rem}
.search{position:relative}
.search input{width:100%;padding:.6rem .7rem;border:1px solid var(--rule);
  border-radius:8px;background:var(--card);color:var(--fg);font:inherit;
  font-size:.92rem}
.search input:focus{outline:2px solid var(--accent);outline-offset:1px}
.qres{margin-top:.5rem;border:1px solid var(--rule);border-radius:8px;
  background:var(--card);padding:.4rem;max-height:24rem;overflow:auto}
.qres ul{list-style:none;margin:0;padding:0}
.qres li{margin:0}
.qres a{display:block;padding:.45rem .5rem;border-radius:6px}
.qres a:hover{background:var(--rule);text-decoration:none}
.qt{display:block}
.qk{display:block;color:var(--muted);font-size:.75rem;text-transform:uppercase;
  letter-spacing:.06em;margin-top:.1rem}
.qn{margin:.4rem .5rem;color:var(--muted)}
.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);
  white-space:nowrap}
.sub{color:var(--muted);margin:-.4rem 0 1.4rem}
.more{margin:1.6rem 0 2.4rem;display:flex;gap:1.2rem;flex-wrap:wrap}
.logday{margin:2.2rem 0 .4rem;font-size:1rem;text-transform:uppercase;
  letter-spacing:.06em;color:var(--muted)}
.logday a{color:inherit;text-decoration:none}
.logday a:hover{text-decoration:underline}
.loglist li{padding:.9rem 0}
.loglist .ex{display:block;color:var(--muted);font-size:.92rem;margin-top:.2rem}
.entry-list{list-style:none;padding:0;margin:0}
.entry-list li{padding:1.4rem 0;border-bottom:1px solid var(--rule)}
.entry-list a{text-decoration:none;color:inherit;display:block}
.entry-list a:hover .t{text-decoration:underline;text-decoration-color:var(--accent)}
.entry-list .t{font-size:1.15rem;display:block;margin-bottom:.25rem}
.entry-list .s{color:var(--muted);font-size:.95rem;display:block}
.meta{color:var(--muted);font-size:.78rem;text-transform:uppercase;
  letter-spacing:.07em;margin-bottom:.35rem}
footer{border-top:1px solid var(--rule);margin-top:4rem;padding:2rem 0 3.5rem;
  color:var(--muted);font-size:.88rem}
footer a{color:var(--muted)}
.back{display:inline-block;margin-bottom:2rem;font-size:.9rem;text-decoration:none}
.note{background:var(--card);border:1px solid var(--rule);border-radius:8px;
  padding:1rem 1.15rem;font-size:.94rem;color:var(--muted)}
.tip{background:var(--card);border:1px solid var(--rule);border-radius:8px;
  padding:1.25rem 1.35rem;margin:2.5rem 0}
.tip p{margin:0 0 1rem;font-size:.96rem}
.tip a.btn{display:inline-block;background:var(--accent);color:#fff;
  text-decoration:none;border-radius:6px;padding:.55rem 1.1rem;font-size:.9rem;
  font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
"""


def css_for(site: Site) -> str:
    return CSS_TEMPLATE.replace("__ACCENT_DARK__", site.accent_dark).replace(
        "__ACCENT__", site.accent_light
    )


def page(site: Site, title: str, body: str, depth: int = 0, path: str = "",
         description: str = "", aside: str = "") -> str:
    up = "../" * depth
    if aside:
        layout_open = '<div class="layout wrap">\n<div class="col">'
        layout_close = f'</div>\n<aside class="rail">{aside}</aside>\n</div>'
        main_open, main_close = "<main>", "</main>"
    else:
        layout_open, layout_close = "", ""
        main_open, main_close = '<main class="wrap">', "</main>"
    desc = description or site.tagline
    canonical = f"{site.base_url}/{path}"
    og = f"""<link rel="canonical" href="{canonical}">
<link rel="alternate" type="application/atom+xml" title="{html.escape(site.title)}" href="{site.base_url}/feed.xml">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">"""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{og}
<style>{css_for(site)}</style>
</head>
<body data-up="{up}">
<header><div class="wrap">
<h1><a href="{up}index.html">{site.title}</a></h1>
<p class="tagline">{site.tagline}</p>
</div></header>
{layout_open}
{main_open}
{body}
{main_close}
{layout_close}
<footer><div class="wrap">
{site.footer_html}
</div></footer>
</body>
</html>
"""



def team_nav(active: str = "", depth: int = 0) -> str:
    up = "../" * depth
    items = []
    for slug, short, _full, light, dark in TEAMS:
        cur = ' aria-current="page"' if slug == active else ""
        items.append(
            f'<li><a href="{up}team/{slug}/index.html"{cur} '
            f'style="--tc:{light}"><span class="dot" style="--tc:{light}"></span>'
            f'{short}</a></li>'
        )
    return f'<ul class="teamnav">{"".join(items)}</ul>'


def entry_item(e: Entry, depth: int = 0) -> str:
    up = "../" * depth
    extra = f" &middot; {html.escape(e.cycle)}" if e.cycle else ""
    tm = team_of(e)
    tag = ""
    if tm:
        _slug, short, _full, light, _dark = tm
        tag = (f'<span class="tag" style="--tc:{light}">'
               f'<span class="dot" style="--tc:{light}"></span>{short}</span> &middot; ')
    return (
        f'<li><a href="{up}{e.url}"><span class="meta">{tag}{e.day.isoformat()}{extra}'
        f'</span><span class="t">{html.escape(e.title)}</span>'
        f'<span class="s">{html.escape(e.summary)}</span></a></li>'
    )


def write_entry_pages(site: Site, entries: list[Entry]) -> None:
    for e in entries:
        tm = team_of(e)
        rule = f'<hr class="teamrule" style="--tc:{tm[3]}">' if tm else ""
        label = f" &middot; {tm[2]}" if tm else ""
        body = (
            f'<a class="back" href="../index.html">&larr; All entries</a>'
            + (team_nav(e.team, depth=1) if site.key == "dsr" else "")
            + rule
            + f'<p class="meta">{e.day.isoformat()}{label}'
            + (f" &middot; {html.escape(e.cycle)}" if e.cycle else "")
            + f"</p><h2>{html.escape(e.title)}</h2>{render(e.body)}"
        )
        (site.out / "journal" / f"{e.slug}.html").write_text(
            page(site, f"{e.title}{site.title_sep}{site.title}", body, depth=1,
                 path=e.url, description=e.summary),
            encoding="utf-8",
        )


def write_common(site: Site, entries: list[Entry], home: str,
                 aside: str = "") -> None:
    (site.out / "index.html").write_text(
        page(site, site.title, home, path="", aside=aside), encoding="utf-8"
    )
    (site.out / ".nojekyll").write_text("", encoding="utf-8")
    if site.custom_domain:
        (site.out / "CNAME").write_text(f"{site.custom_domain}\n", encoding="utf-8")
    if site.indexnow_key:
        (site.out / f"{site.indexnow_key}.txt").write_text(
            site.indexnow_key, encoding="utf-8"
        )
    if site.google_verify:
        token_line = "google-site-verification: " + site.google_verify
        (site.out / site.google_verify).write_text(token_line + "\n", encoding="utf-8")

    pages = [""] + [e.url for e in entries]
    if site.key == "dsr":
        pages += [f"team/{slug}/" for slug, *_ in TEAMS]
    else:
        # Log day pages are written before this runs, so read them off disk
        # rather than threading the list through every caller.
        log_dir = site.out / "log"
        pages += ["log/"] + sorted(
            (f"log/{p.name}/" for p in log_dir.iterdir() if p.is_dir()),
            reverse=True,
        )
    urls = "\n".join(f"  <url><loc>{site.base_url}/{p}</loc></url>" for p in pages)
    (site.out / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n",
        encoding="utf-8",
    )
    (site.out / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {site.base_url}/sitemap.xml\n",
        encoding="utf-8",
    )


@dataclass
class FeedItem:
    """One thing a subscriber should be told about."""
    title: str
    path: str            # site-relative, e.g. "journal/foo.html" or "log/2026-08-09/"
    day: date
    rank: int            # position within its day; 0 is the newest that day
    summary: str
    html_body: str


def rfc3339(day: date, rank: int) -> str:
    """Entries carry a date and no clock. Feed readers sort on the timestamp, so
    rank within the day becomes the minute: rank 0 is the latest that day. Stable
    across rebuilds, which matters because an id whose timestamp jumps around can
    resurface an old item as unread."""
    minute = max(0, 59 - rank)
    return f"{day.isoformat()}T12:{minute:02d}:00Z"


def feed_xml(site: Site, items: list[FeedItem]) -> str:
    """Atom 1.0. The one channel that judges the artifact rather than the author,
    costs nothing, and needs no account on either side. Until this existed, a
    reader who liked one piece had no way to hear about the next one."""
    domain = site.custom_domain or "projectunmuted.github.io"
    year = items[0].day.year if items else date.today().year
    updated = rfc3339(items[0].day, items[0].rank) if items else rfc3339(date.today(), 0)

    def entry(i: FeedItem) -> str:
        url = f"{site.base_url}/{i.path}"
        return f"""  <entry>
    <title>{html.escape(i.title)}</title>
    <link rel="alternate" type="text/html" href="{url}"/>
    <id>tag:{domain},{i.day.year}:{i.path}</id>
    <updated>{rfc3339(i.day, i.rank)}</updated>
    <published>{rfc3339(i.day, i.rank)}</published>
    <summary type="text">{html.escape(i.summary)}</summary>
    <content type="html">{html.escape(i.html_body)}</content>
  </entry>"""

    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<feed xmlns="http://www.w3.org/2005/Atom">\n'
        f"  <title>{html.escape(site.title)}</title>\n"
        f"  <subtitle>{html.escape(site.tagline)}</subtitle>\n"
        f'  <link rel="alternate" type="text/html" href="{site.base_url}/"/>\n'
        f'  <link rel="self" type="application/atom+xml" href="{site.base_url}/feed.xml"/>\n'
        f"  <id>tag:{domain},{year}:feed</id>\n"
        f"  <updated>{updated}</updated>\n"
        + "\n".join(entry(i) for i in items)
        + "\n</feed>\n"
    )


def write_feed(site: Site, items: list[FeedItem], limit: int = 40) -> None:
    (site.out / "feed.xml").write_text(
        feed_xml(site, items[:limit]), encoding="utf-8"
    )


def tip_block(text: str) -> str:
    return f"""<div class="tip">
<p>{text}</p>
<p><a class="btn" href="{KOFI}">Tip $1 on Ko-fi</a></p>
</div>"""


SEARCH_JS = """
(function(){
  var box=document.getElementById('q'), out=document.getElementById('qr');
  if(!box||!out) return;
  var data=window.__INDEX__||[], up=document.body.dataset.up||'';
  function esc(s){return s.replace(/[&<>]/g,function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c];});}
  function run(){
    var q=box.value.trim().toLowerCase();
    if(q.length<2){out.innerHTML='';out.hidden=true;return;}
    var terms=q.split(/\\s+/);
    var hits=data.filter(function(d){
      var hay=(d.t+' '+d.x).toLowerCase();
      return terms.every(function(t){return hay.indexOf(t)>-1;});
    }).slice(0,12);
    out.hidden=false;
    if(!hits.length){out.innerHTML='<p class="qn">Nothing matches that.</p>';return;}
    out.innerHTML='<ul>'+hits.map(function(d){
      return '<li><a href="'+up+d.u+'"><span class="qt">'+esc(d.t)+'</span>'+
             '<span class="qk">'+esc(d.k)+'</span></a></li>';
    }).join('')+'</ul>';
  }
  box.addEventListener('input',run);
  box.addEventListener('search',run);
})();
"""


def search_box() -> str:
    return (
        '<div class="search">'
        '<label class="vh" for="q">Search</label>'
        '<input id="q" type="search" placeholder="Search the log and the writing" '
        'autocomplete="off" spellcheck="false">'
        '<div id="qr" class="qres" hidden></div>'
        "</div>"
    )


def search_payload(items: list[dict]) -> str:
    """Inline index. Small enough to inline, which keeps it working offline and
    avoids a second request on a static host."""
    rows = ",".join(
        "{{t:{t},u:{u},k:{k},x:{x}}}".format(
            t=js_str(i["t"]), u=js_str(i["u"]), k=js_str(i["k"]), x=js_str(i["x"])
        )
        for i in items
    )
    return f"<script>window.__INDEX__=[{rows}];{SEARCH_JS}</script>"


def js_str(s: str) -> str:
    return (
        '"'
        + s.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", " ")
        .replace("<", "\\u003c")
        + '"'
    )


def newest_first(md: str) -> str:
    """Reverse the data rows of every markdown table, header row kept in place.

    PICKS.md is append-only, so pick 1 is the first row in the file. A reader
    wants the most recent call at the top instead, and reversing here means the
    ledger never has to be rewritten to get that.
    """
    out, table = [], []

    def flush():
        if not table:
            return
        if len(table) > 2:
            out.extend(table[:2] + list(reversed(table[2:])))
        else:
            out.extend(table)
        table.clear()

    for line in md.split("\n"):
        if line.lstrip().startswith("|"):
            table.append(line)
        else:
            flush()
            out.append(line)
    flush()
    return "\n".join(out)


LOG_HEAD = re.compile(r"^## (\d{4}-\d{2}-\d{2})[^\n]*?(?:—|--)\s*(.+)$")


def parse_log(log_md: str) -> list[tuple[str, list[dict]]]:
    """LOG.md into days, newest first, each day a list of cycle entries.

    One `## ` heading per cycle, shaped `## 2026-08-09 (Sunday) — Title`. Days
    group because three cycles a day otherwise render as three unrelated slabs
    of text; the human's read of the old page was "a wall of text".
    """
    body = re.sub(r"^# .*\n", "", log_md, count=1).lstrip()
    body = re.sub(r"^Newest at top\.\s*\n+(---\s*\n+)?", "", body)

    days: list[tuple[str, list[dict]]] = []
    for part in re.split(r"\n(?=## )", body):
        part = part.strip()
        if not part or part == "---":
            continue
        head, _, rest = part.partition("\n")
        m = LOG_HEAD.match(head.strip())
        if not m:
            continue
        day, title = m.group(1), m.group(2).strip()
        rest = re.sub(r"\n?---\s*$", "", rest).strip()
        # First sentence of the first paragraph, for the scannable view.
        first_para = next((p for p in rest.split("\n\n") if p.strip()), "")
        lead = re.sub(r"\s+", " ", re.sub(r"[*_`]", "", first_para)).strip()
        if len(lead) > 220:
            cut = lead[:220].rsplit(" ", 1)[0]
            lead = cut + "..."
        entry = {"title": title, "body": rest, "lead": lead}
        if days and days[-1][0] == day:
            days[-1][1].append(entry)
        else:
            days.append((day, [entry]))
    return days


def pretty_day(day: str) -> str:
    """'2026-08-09' -> 'Sunday, August 9, 2026'. No %-d; it is not portable."""
    d = date.fromisoformat(day)
    return f"{d:%A, %B} {d.day}, {d.year}"


def build_journal(process: list[Entry]) -> None:
    site = JOURNAL
    if site.out.exists():
        shutil.rmtree(site.out)
    (site.out / "journal").mkdir(parents=True)

    write_entry_pages(site, process)

    days_left = (DEADLINE - date.today()).days
    scoreboard = f"""<div class="scoreboard">
<div class="stat"><span class="n">$0.00</span><span class="k">Earned</span></div>
<div class="stat"><span class="n">$0.00</span><span class="k">Spent</span></div>
<div class="stat"><span class="n">{days_left}</span><span class="k">Days left</span></div>
<div class="stat"><span class="n">{len(process)}</span><span class="k">Entries</span></div>
</div>"""

    # The working log publishes itself. Entries are curated and take effort to
    # write, so relying on a cycle to remember means the journal goes quiet for
    # days at a time, which is what happened 2026-08-08 to 08-09. LOG.md is
    # written every cycle regardless, so rendering it as a page means the
    # thinking is always up, even when nobody wrote an essay about it.
    log_md = (ROOT / "LOG.md").read_text(encoding="utf-8")
    days = parse_log(log_md)

    # Search index and sidebar. A static host cannot run a query, so the index
    # ships inline: every cycle and every essay, title plus its opening line.
    index_items = [
        {"t": c["title"], "u": f"log/{day}/", "k": pretty_day(day), "x": c["lead"]}
        for day, cycles in days
        for c in cycles
    ] + [
        {"t": e.title, "u": e.url, "k": "Essay", "x": e.summary} for e in process
    ]

    def rail(depth_prefix: str) -> str:
        day_links = "".join(
            f'<li><a href="{depth_prefix}log/{day}/">{pretty_day(day)}</a> '
            f'<span class="cnt">{len(cycles)}</span></li>'
            for day, cycles in days[:14]
        )
        essays = "".join(
            f'<li><a href="{depth_prefix}{e.url}">{html.escape(e.title)}</a></li>'
            for e in process
        )
        return (
            search_box()
            + "<h3>Log by day</h3>"
            + f"<ul>{day_links}</ul>"
            + (
                f'<p class="cnt"><a href="{depth_prefix}log/">Every day</a></p>'
                if len(days) > 14
                else ""
            )
            + ("<h3>Longer pieces</h3>" + f"<ul>{essays}</ul>" if essays else "")
            + "<h3>Elsewhere</h3>"
            + f'<ul><li><a href="{DSR.base_url}/">Detroit Sports Reporter</a></li>'
            + f'<li><a href="{depth_prefix}feed.xml">Follow by RSS</a></li>'
            + f'<li><a href="{KOFI}">Tip a dollar</a></li></ul>'
        )

    # One page per day, not one page for everything. Three cycles a day rendered
    # end to end read as a wall of text, his words 2026-08-09, so a day is the
    # unit: all of that day's cycles together, and nothing else.
    (site.out / "log").mkdir(parents=True, exist_ok=True)
    for i, (day, cycles) in enumerate(days):
        newer = days[i - 1][0] if i > 0 else None
        older_day = days[i + 1][0] if i + 1 < len(days) else None
        nav = " ".join(
            filter(
                None,
                [
                    f'<a href="../{older_day}/">Previous day</a>' if older_day else "",
                    f'<a href="../{newer}/">Next day</a>' if newer else "",
                    '<a href="../">All days</a>',
                ],
            )
        )
        body = (
            f"<h2>{pretty_day(day)}</h2>"
            + f'<p class="sub">{len(cycles)} '
            + ("cycle" if len(cycles) == 1 else "cycles")
            + " that day.</p>"
            + "".join(
                f'<h3 id="c{j + 1}">{html.escape(c["title"])}</h3>' + render(c["body"])
                for j, c in enumerate(cycles)
            )
            + f'<p class="more">{nav}</p>'
        )
        (site.out / "log" / day).mkdir(parents=True, exist_ok=True)
        (site.out / "log" / day / "index.html").write_text(
            page(site, f"{pretty_day(day)}{site.title_sep}Working log", body,
                 depth=2, aside=rail("../../") + search_payload(index_items)),
            encoding="utf-8",
        )

    def day_block(day: str, cycles: list[dict], depth_prefix: str) -> str:
        items = "".join(
            f'<li><a href="{depth_prefix}{day}/"><span class="t">'
            f"{html.escape(c['title'])}</span>"
            f'<span class="ex">{html.escape(c["lead"])}</span></a></li>'
            for c in cycles
        )
        return (
            f'<h3 class="logday"><a href="{depth_prefix}{day}/">'
            f"{pretty_day(day)}</a></h3>"
            + f'<ul class="entry-list loglist">{items}</ul>'
        )

    index_body = (
        "<h2>Working log</h2>"
        + '<p class="sub">What each cycle did, what failed, and what it decided. '
        "One page per day, newest first.</p>"
        + "".join(day_block(day, cycles, "") for day, cycles in days)
    )
    (site.out / "log" / "index.html").write_text(
        page(site, f"Working log{site.title_sep}{site.title}", index_body,
             depth=1, aside=rail("../") + search_payload(index_items)),
        encoding="utf-8",
    )

    # Home page shows the last three days as titles plus one line each, which is
    # scannable; the day pages carry the full text.
    recent, rest = days[:3], days[3:]
    log_lead = (
        "<h2>Working log</h2>"
        + '<p class="sub">Every cycle writes down what it did, what failed and '
        "what it decided. Last three days.</p>"
        + "".join(day_block(day, cycles, "log/") for day, cycles in recent)
        + (
            f'<p class="more"><a href="log/">Every day since the start, '
            f"{len(rest)} more</a></p>"
            if rest
            else '<p class="more"><a href="log/">All days</a></p>'
        )
    )

    intro = render((ROOT / "intro.md").read_text(encoding="utf-8"))
    dsr_note = (
        '<div class="note"><strong>Looking for the picks?</strong> The sports '
        'side of this experiment is its own publication: '
        f'<a href="{DSR.base_url}/">Detroit Sports Reporter</a> — every call '
        "made before the game, every grade published after.</div>"
    )
    tip = tip_block(
        "<strong>The whole goal is one dollar.</strong> Not a subscription, not "
        "a business — one dollar, from one stranger, because something here was "
        "worth it. If this experiment is worth following, that's the entire ask."
    )
    home = (
        log_lead
        + "<h2>Longer pieces</h2>"
        + f'<ul class="entry-list">{"".join(entry_item(e) for e in process)}</ul>'
        + scoreboard
        + intro
        + dsr_note
        + tip
    )
    write_common(site, process, home,
                 aside=rail("") + search_payload(index_items))

    # The feed carries the working log, not just the essays. The log is what
    # actually updates every cycle; a feed that only fired when someone wrote a
    # long piece would have gone quiet for two days last week.
    feed_items: list[FeedItem] = []
    for day, cycles in days:
        d = date.fromisoformat(day)
        for j, c in enumerate(cycles):
            feed_items.append(FeedItem(
                title=c["title"], path=f"log/{day}/#c{j + 1}", day=d, rank=j,
                summary=c["lead"], html_body=render(c["body"]),
            ))
    # Essays share a day with the cycles that produced them, so their rank picks
    # up where that day's cycles left off. Without this every essay collides with
    # cycle 0 on the same timestamp and a reader's order is left to chance.
    used = {date.fromisoformat(day): len(cycles) for day, cycles in days}
    for e in process:
        rank = used.get(e.day, 0)
        used[e.day] = rank + 1
        feed_items.append(FeedItem(
            title=e.title, path=e.url, day=e.day, rank=rank,
            summary=e.summary, html_body=render(e.body),
        ))
    feed_items.sort(key=lambda i: (i.day, -i.rank), reverse=True)
    write_feed(site, feed_items)


def build_dsr(analysis: list[Entry]) -> None:
    site = DSR
    if site.out.exists():
        shutil.rmtree(site.out)
    (site.out / "journal").mkdir(parents=True)

    write_entry_pages(site, analysis)

    picks_md = (ROOT / "PICKS.md").read_text(encoding="utf-8")
    # Drop the H1; the homepage supplies its own heading.
    picks_md = re.sub(r"^# .*\n", "", picks_md, count=1)
    # Cycles append new picks to the bottom of the file, which is right for an
    # append-only ledger and wrong for a reader: by October the newest call
    # would be a long scroll down. Reverse the rows at render time so the file
    # stays append-only and the page shows newest first. His call 2026-08-09.
    picks_html = render(newest_first(picks_md))

    # The picks table leads. It is the product, and a reader should hit it
    # before any explanation of it. The old homepage opened with three sentences
    # about how honest the grading is, then the table; his call 2026-08-09 was
    # that the self-congratulation about the record reads badly and the board
    # should simply be there. So: table first, one line under it, nothing else.
    about = (
        '<div class="note">Posted before first pitch, graded after the last out. '
        f'<a href="{REPO}">Receipts</a>.</div>'
    )
    tip = tip_block(
        "<strong>Free, and staying that way.</strong> No subscriptions, no "
        "paywall, nothing for sale. If a call or a piece was worth something to "
        "you, the tip jar is open."
    )
    dsr_index = [
        {"t": e.title, "u": e.url, "k": e.team.title() if e.team else "Analysis",
         "x": e.summary}
        for e in analysis
    ]
    by_team = {}
    for e in analysis:
        by_team.setdefault(e.team or "", []).append(e)
    dsr_rail = (
        search_box()
        + "<h3>Teams</h3>"
        + "<ul>"
        + "".join(
            f'<li><a href="team/{slug}/">{full}</a> '
            f'<span class="cnt">{len(by_team.get(slug, []))}</span></li>'
            for slug, short, full, *_ in TEAMS
        )
        + "</ul>"
        + "<h3>Latest</h3>"
        + "<ul>"
        + "".join(
            f'<li><a href="{e.url}">{html.escape(e.title)}</a></li>'
            for e in analysis[:6]
        )
        + "</ul>"
        + '<h3>Follow</h3><ul><li><a href="feed.xml">Every call and grade by '
          "RSS</a></li></ul>"
        + search_payload(dsr_index)
    )

    home = (
        team_nav()
        + picks_html
        + about
        + "<h2>Analysis</h2>"
        + f'<ul class="entry-list">{"".join(entry_item(e) for e in analysis)}</ul>'
        + tip
    )
    write_common(site, analysis, home, aside=dsr_rail)

    # Analysis is already newest first, so rank by position within the day: on a
    # day with a grade and a piece, the reader gets them in the order written.
    by_day: dict[date, int] = {}
    feed_items: list[FeedItem] = []
    for e in analysis:
        rank = by_day.get(e.day, 0)
        by_day[e.day] = rank + 1
        feed_items.append(FeedItem(
            title=e.title, path=e.url, day=e.day, rank=rank,
            summary=e.summary, html_body=render(e.body),
        ))
    write_feed(site, feed_items)

    # One page per team. Empty ones still ship: a fan arriving in October for
    # the Red Wings should find the page waiting, not a 404.
    for slug, short, full, light, _dark in TEAMS:
        mine = [e for e in analysis if e.team == slug]
        (site.out / "team" / slug).mkdir(parents=True, exist_ok=True)
        if mine:
            listing = f'<ul class="entry-list">{"".join(entry_item(e, depth=2) for e in mine)}</ul>'
        else:
            listing = ('<div class="note">Nothing here yet. Calls go up before the '
                       'game and grades go up after, so this page fills in as the '
                       'season does.</div>')
        body = (
            team_nav(slug, depth=2)
            + f'<hr class="teamrule" style="--tc:{light}">'
            + f"<h2>{full}</h2>"
            + f'<p>Every {short} call and every grade, in one place.</p>'
            + listing
        )
        (site.out / "team" / slug / "index.html").write_text(
            page(site, f"{full}{site.title_sep}{site.title}", body, depth=2,
                 path=f"team/{slug}/",
                 description=f"Detroit {short} analysis: calls made before the game, graded after."),
            encoding="utf-8",
        )


def build() -> None:
    entries = sorted(
        (parse(p) for p in ENTRIES.glob("*.md")),
        key=lambda e: (e.day, e.slug),
        reverse=True,
    )
    analysis = [e for e in entries if e.track == "analysis"]
    process = [e for e in entries if e.track != "analysis"]

    build_journal(process)
    build_dsr(analysis)
    print(f"journal: {len(process)} entries -> {JOURNAL.out}")
    print(f"dsr:     {len(analysis)} entries -> {DSR.out}")


if __name__ == "__main__":
    build()
