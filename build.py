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
import json
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
ENTRIES = ROOT / "entries"


def main_worktree_root() -> "Path | None":
    """Where the repo's *main* checkout lives, if this one is a linked worktree.

    A linked worktree's `.git` is a file reading `gitdir: <main>/.git/worktrees/<name>`,
    while the main checkout's `.git` is a directory. Returns None when this is
    already the main checkout.
    """
    g = ROOT / ".git"
    if not g.is_file():
        return None
    try:
        text = g.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    if not text.startswith("gitdir:"):
        return None
    gitdir = Path(text.split(":", 1)[1].strip())
    if gitdir.parent.name == "worktrees" and gitdir.parent.parent.name == ".git":
        return gitdir.parent.parent.parent
    return None


def local_config(name: str) -> "Path | None":
    """Find a gitignored config file, looking in the main checkout too.

    This exists because of a two-day silent failure. Background cycles build
    inside `.claude/worktrees/`, and a gitignored file by definition does not
    exist there: only the main checkout has it. So `ROOT / ".analytics.json"`
    came back missing, `analytics_tag` returned an empty string exactly as
    designed, and the built pages shipped with no beacon while three cycles of
    `MEASURE.md` reported it as live and collecting. Nothing errored. The same
    trap is waiting for `.reddit-credentials.json`, which is why this is a
    shared helper rather than a patch inside one function.
    """
    here = ROOT / name
    if here.exists():
        return here
    main = main_worktree_root()
    if main is not None and (main / name).exists():
        return main / name
    return None

DEADLINE = date(2027, 2, 8)
START = date(2026, 8, 8)
REPO = "https://github.com/projectunmuted/newsroom"
# The live rail as of 2026-08-08. The old ko-fi.com/projectunmuted page is
# retired: one account means one payment connection to maintain, and this
# one carries the brand a reader actually arrives from.
KOFI = "https://ko-fi.com/detroitsportsreporter"

# The address a reader can actually reach. Until 2026-08-15 neither site carried
# one: there was a button asking for a dollar and no way to ask for anything.
# MONEY.md ranks somebody paying for a specific breakdown as the likeliest first
# dollar, and its input is a person asking a question, so the question needed
# somewhere to arrive.
ASK_EMAIL = "projectunmuted@proton.me"

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
    tagline="Analysis and picks. Tigers, Lions, Pistons, Red Wings.",
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
    """The entry's primary team, or None.

    `team:` is normally one slug. The Monday column covers all 4 clubs, so it
    carries a comma separated list and the first one supplies the accent. See
    `Entry.teams` for the full set.
    """
    return TEAM_BY_SLUG.get(entry.teams[0]) if entry.teams else None


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
    # Optional tiebreak within a day: higher is later. Entries carry a date and
    # no clock, so a day with two entries used to order them by reverse
    # alphabetical filename, which put a freshly published grade below two
    # pieces written hours earlier. Absent means 0, which preserves the old
    # behaviour for every entry that does not set it.
    seq: int = 0

    @property
    def teams(self) -> list[str]:
        """Every team slug this entry belongs to, in frontmatter order.

        A single slug is the normal case. The Monday column writes
        `team: tigers, lions, pistons, redwings` because it genuinely is about
        all 4, and a piece that covers a club should appear on that club's
        page and count against its coverage floor.
        """
        return [t for t in (x.strip().lower() for x in self.team.split(","))
                if t in TEAM_BY_SLUG]

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
        seq=int(meta["seq"]) if meta.get("seq", "").strip().isdigit() else 0,
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
header{border-bottom:1px solid var(--rule);margin-bottom:1.5rem}
header.hero{position:relative;border-bottom:0;margin-bottom:0}
header.plain{margin-bottom:2.5rem}
header.plain h1{font-size:2.1rem;line-height:1.15;margin:0 0 .5rem;letter-spacing:-.02em}
header.plain h1 a{color:inherit;text-decoration:none}
header.plain .tagline{color:var(--muted);font-size:1.05rem;margin:0}
header.plain .hero-text{max-width:40rem;margin:0 auto;padding:2.25rem 1.25rem 1.25rem}
.band{position:relative;line-height:0;overflow:hidden;background:var(--wash)}
.band img{display:block;width:100%;height:230px;object-fit:cover;
  object-position:50% 56%;filter:saturate(.95) contrast(1.02)}
.band::after{content:"";position:absolute;inset:0;background:var(--wash);
  mix-blend-mode:multiply;opacity:.26}
.band::before{content:"";position:absolute;inset:0;z-index:1;background:
  linear-gradient(to top,rgba(0,0,0,.72) 0%,rgba(0,0,0,.28) 42%,rgba(0,0,0,0) 78%)}
.hero .hero-text{position:absolute;left:0;right:0;bottom:0;z-index:2;
  padding:0 1.5rem 1.1rem;line-height:1.2}
.hero h1{color:#fff;text-shadow:0 1px 14px rgba(0,0,0,.45);font-size:2.4rem;
  margin:0 0 .2rem}
.hero h1 a{color:inherit}
.hero .tagline{color:rgba(255,255,255,.92);text-shadow:0 1px 10px rgba(0,0,0,.5);
  font-size:1rem;margin:0;letter-spacing:.01em}
.navbar{border-bottom:1px solid var(--rule);margin-bottom:2.5rem;
  padding:0 1.5rem}
.navbar h1 a{color:inherit;text-decoration:none}
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
/* The standing, kept deliberately small. It is a reference a returning reader
   glances at, not the headline, and it sits above the board so the first thing
   on the page is the score rather than the newest call. His call 2026-08-14. */
.recnote{font-size:.8rem;color:var(--muted);margin:0 0 1.6rem}
.teamnav{display:flex;flex-wrap:wrap;gap:.5rem;margin:0 0 .5rem;padding:0;list-style:none}
.teamnav a{display:inline-flex;align-items:center;gap:.45rem;text-decoration:none;
  color:var(--fg);font-size:.88rem;border:1px solid var(--rule);border-radius:999px;
  padding:.3rem .8rem;font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.teamnav a:hover{border-color:var(--tc,var(--accent))}
.teamnav a[aria-current="page"]{border-color:var(--tc,var(--accent));
  box-shadow:inset 0 -2px 0 var(--tc,var(--accent))}
/* With records in it the nav stops being a wrapping row of labels and becomes a
   scoreboard, so it gets fixed columns: 4 across, 2x2 under 40rem, never the
   3-then-1 that flex-wrap chose on its own. His call 2026-08-14. */
.teamnav.withrec{display:grid;grid-template-columns:repeat(4,1fr);gap:.4rem}
@media(max-width:40rem){.teamnav.withrec{grid-template-columns:repeat(2,1fr)}}
.teamnav.withrec a{justify-content:center;white-space:nowrap;padding:.28rem .55rem}
.teamnav .rec{margin-left:.45rem;color:var(--fg);font-weight:600;font-size:.95em}
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
.sitenav{margin:0}
.navbar .sitenav ul{padding:.7rem 0}
@media(max-width:44rem){.band img{height:168px}
  .hero h1{font-size:1.7rem}
  .hero .tagline{font-size:.92rem}
  .hero .hero-text{padding:0 1.1rem .9rem}
  .navbar{padding:0 1.1rem}}
@media(prefers-color-scheme:dark){.band img{filter:saturate(.85) brightness(.8)}
  .band::after{opacity:.3}}
.sitenav{margin-top:1rem}
.sitenav ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;
  gap:0 1.4rem;font-size:.9rem}
.sitenav a{color:var(--muted);text-decoration:none;padding:.2rem 0;
  border-bottom:2px solid transparent}
.sitenav a:hover{color:var(--fg);border-bottom-color:var(--accent)}
.scroll{width:min(58rem,100vw - 2rem);margin-left:50%;transform:translateX(-50%)}
@media(max-width:44rem){.scroll{width:auto;margin-left:0;transform:none}}
/* The board breaks the reading measure the way the ledger table used to: the
   column is 600px, so a card grid inside it can only ever be one-up, which is
   the tall layout this was meant to replace. Same widening as .scroll. */
.pickcards{list-style:none;padding:0;margin:1.2rem 0;display:grid;gap:.6rem;
  grid-template-columns:repeat(auto-fill,minmax(20rem,1fr));
  width:min(58rem,100vw - 2rem);margin-left:50%;transform:translateX(-50%)}
@media(max-width:44rem){.pickcards{grid-template-columns:1fr;width:auto;
  margin-left:0;transform:none}}
.pickcards li{border:1px solid var(--rule);border-radius:10px;padding:.7rem .9rem;
  background:var(--card)}
.pickcards .g{font-size:.8rem;color:var(--muted)}
.pickcards .c{font-size:1rem;margin:.15rem 0}
.pickcards .o{font-size:.85rem;color:var(--muted)}
.pickcards .why{font-size:.85rem;margin-top:.35rem;display:flex;gap:.9rem;
  flex-wrap:wrap}
.chip{display:inline-block;font-size:.72rem;text-transform:uppercase;
  letter-spacing:.06em;padding:.15rem .5rem;border-radius:999px;
  border:1px solid var(--rule);color:var(--muted);margin-right:.4rem}
.related{margin:3rem 0 0;padding-top:1.4rem;border-top:1px solid var(--rule)}
.related h3{font-size:.75rem;text-transform:uppercase;letter-spacing:.08em;
  color:var(--muted);margin:0 0 .6rem}
.prevnext{display:flex;justify-content:space-between;gap:1rem;margin-top:2rem;
  font-size:.92rem}
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
/* The ask, at the end of a piece rather than only on its own page. Same box as
   .note, spaced away from the last paragraph so it reads as an invitation and
   not as a footnote to the argument above it. */
.note.ask{margin:2.75rem 0 0}
.note.ask strong{color:var(--fg)}
/* Reader requests. The question is the heading, because on this page the
   question is the thing a visitor scans for, not the answer. */
.reqs{list-style:none;margin:1.25rem 0 0;padding:0}
.req{border-top:1px solid var(--rule);padding:1.1rem 0}
.req .q{margin:0 0 .5rem;font-weight:600;color:var(--fg)}
.req .a{margin:0 0 .45rem;font-size:.95rem}
.req .meta{margin:0;font-size:.85rem;color:var(--muted)}
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




def skyline_band(color: str = "", up: str = "") -> str:
    """The Detroit riverfront at sunset, washed in the page's colour.

    One CC0 photograph from Wikimedia Commons, cropped to a band. Team pages
    wash it in that team's colour with a multiply blend, so the same image reads
    as Tigers navy or Lions blue without shipping four files. A drawn skyline
    came first and looked like any city; this one is Detroit.
    """
    tint = color or "var(--accent)"
    return (
        f'<div class="band" style="--wash:{tint}">'
        f'<picture>'
        f'<source media="(max-width:44rem)" srcset="{up}assets/skyline-narrow.jpg">'
        f'<img src="{up}assets/skyline.jpg" alt="The Detroit skyline across the '
        f'river at sunset" width="1920" height="456" loading="eager" '
        f'decoding="async">'
        f"</picture></div>"
    )


def home_title(site: Site) -> str:
    """The DSR homepage title was the bare brand name, which can only match a
    brand query, and nobody searches a brand they have never heard of."""
    if site.key == "dsr":
        return ("Detroit Tigers, Lions, Pistons and Red Wings analysis and "
                "predictions | Detroit Sports Reporter")
    return "Project Unmuted — an AI agent trying to earn one dollar in public"


def redirect_page(site: Site, frm: str, to: str, label: str) -> str:
    """A URL that has moved, kept alive rather than deleted.

    Static hosting has no 301, so this is the honest substitute: a canonical
    pointing at the destination so search engines consolidate rather than treat
    the two as duplicates, a meta refresh for readers, and a real link for
    anyone the refresh fails. `noindex` keeps it out of results while the
    canonical does the consolidating.
    """
    dest = f"{site.base_url}/{to}"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(label)}{site.title_sep}{html.escape(site.title)}</title>
<link rel="canonical" href="{dest}">
<meta name="robots" content="noindex,follow">
<meta http-equiv="refresh" content="0; url={dest}">
<style>{css_for(site)}</style>
</head>
<body>
<main class="wrap"><p>{html.escape(label)} moved to
<a href="{dest}">{dest}</a>.</p></main>
</body>
</html>
"""


def site_nav(site: Site, up: str) -> str:
    """The thing both sites were missing. Before this, `<header>` held exactly
    one link, the logo, and a sidebar was standing in for navigation on the
    handful of pages that had one. A nav that is present on some pages is worse
    than none, because a reader learns it exists and then loses it."""
    if site.key == "dsr":
        items = [
            ("Picks", f"{up}index.html#picks"),
            ("Analysis", f"{up}analysis.html"),
            ("Teams", f"{up}index.html#teams"),
            ("Requests", f"{up}requests.html"),
            ("About", f"{up}about.html"),
        ]
    else:
        items = [
            ("Essays", f"{up}index.html"),
            ("Working log", f"{up}log/index.html"),
            ("About", f"{up}about.html"),
            ("Detroit Sports Reporter", f"{DSR.base_url}/"),
        ]
    links = "".join(f'<li><a href="{href}">{label}</a></li>' for label, href in items)
    return f'<nav class="sitenav"><ul>{links}</ul></nav>'


# Every reason a beacon was not emitted this build, reported loudly at the end.
# Silence is what let the sites run for two days collecting nothing.
BEACON_MISSES: list[str] = []


def analytics_tag(site: Site) -> str:
    """Cloudflare Web Analytics beacon, emitted only when a token exists.

    GitHub Pages produces no server logs, so without this there is no such thing
    as a page view for either site: the number is not small, it does not exist.
    Free, cookieless, no consent banner. Tokens live in `.analytics.json` at the
    repo root, gitignored, so the build works fine without the file and nothing
    lands in git.
    """
    f = local_config(".analytics.json")
    if f is None:
        BEACON_MISSES.append(f"{site.key}: no .analytics.json found from {ROOT}")
        return ""
    try:
        token = json.loads(f.read_text(encoding="utf-8")).get(site.key, "")
    except json.JSONDecodeError:
        BEACON_MISSES.append(f"{site.key}: {f} is not valid JSON")
        return ""
    if not token:
        BEACON_MISSES.append(f"{site.key}: no token for '{site.key}' in {f}")
        return ""
    beacon = json.dumps({"token": token})
    return ('<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
            f"data-cf-beacon='{beacon}'></script>")


def clip(text: str, limit: int = 155) -> str:
    """Meta descriptions are cut around 155 characters, so cut them here on a
    word boundary rather than letting Google truncate mid-thought. Article
    descriptions were running 490 characters."""
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(",.;:") + "..."


def page(site: Site, title: str, body: str, depth: int = 0, path: str = "",
         description: str = "", kind: str = "page",
         day: "date | None" = None, accent: str = "") -> str:
    up = "../" * depth
    layout_open, layout_close = "", ""
    main_open, main_close = '<main class="wrap">', "</main>"
    desc = clip(description or site.tagline)
    # The skyline belongs to the sports site. The journal is about an
    # experiment, not about Detroit, and borrowing the imagery would blur two
    # things that are deliberately separate.
    banner = skyline_band(accent, up) if site.key == "dsr" else ""
    canonical = f"{site.base_url}/{path}"
    # Every share of this site to Reddit, Discord or iMessage used to render as
    # a bare grey link: there was no og:image anywhere. Sharing is the only
    # distribution this site has for months, so the card matters more than any
    # schema. One image per site, generated by scripts/make_og_image.py.
    og_image = f"{site.base_url}/og.png"
    og_type = "article" if kind == "article" else "website"
    published = (
        f'<meta property="article:published_time" content="{day.isoformat()}">'
        if kind == "article" and day
        else ""
    )
    ld = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "Article" if kind == "article" else "WebSite",
            "headline": title,
            "description": desc,
            "url": canonical,
            "image": og_image,
            **({"datePublished": day.isoformat()} if day else {}),
            "publisher": {"@type": "Organization", "name": site.title},
        },
        separators=(",", ":"),
    )
    og = f"""<link rel="canonical" href="{canonical}">
<link rel="alternate" type="application/atom+xml" title="{html.escape(site.title)}" href="{site.base_url}/feed.xml">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{html.escape(site.title)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
{published}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{og_image}">
<script type="application/ld+json">{ld}</script>"""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{og}
<style>{css_for(site)}</style>
{analytics_tag(site)}
</head>
<body>
<header class="{'hero' if site.key == 'dsr' else 'plain'}">
{banner}
<div class="hero-text"><h1><a href="{up}index.html">{site.title}</a></h1>
<p class="tagline">{site.tagline}</p></div>
</header>
<div class="navbar">{site_nav(site, up)}</div>
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



def team_nav(active: str = "", depth: int = 0,
             records: "dict[str, tuple[int, int, int]] | None" = None) -> str:
    """The team switcher, carrying each team's record when one is passed.

    These were 2 separate rows for a day: the switcher, then a scoreboard strip
    directly under it with the same 4 names and the same 4 dots. His call
    2026-08-14 was to merge them, and he is right that a reader does not need
    the word "Tigers" twice 3 lines apart. The record rides in the pill.

    A team with no graded calls says so rather than showing 0-0, which would
    read as 0 wins rather than as nothing having happened yet.
    """
    up = "../" * depth
    items = []
    for slug, short, _full, light, dark in TEAMS:
        cur = ' aria-current="page"' if slug == active else ""
        rec = ""
        if records is not None:
            w, l, _pending = records.get(slug, (0, 0, 0))
            val = f"{w}-{l}" if (w or l) else "none yet"
            rec = f'<span class="rec">{val}</span>'
        items.append(
            f'<li><a href="{up}team/{slug}/index.html"{cur} '
            f'style="--tc:{light}"><span class="dot" style="--tc:{light}"></span>'
            f'{short}{rec}</a></li>'
        )
    cls = "teamnav withrec" if records is not None else "teamnav"
    return f'<ul class="{cls}">{"".join(items)}</ul>'


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


def write_entry_pages(site: Site, entries: list[Entry],
                      records: "dict[str, tuple[int, int, int]] | None" = None) -> None:
    """Entries were leaves: one internal link each, no date on the page, no way
    to reach the next piece, and "All entries" pointed at a homepage whose lead
    section was something else. Every article now carries a date, its
    neighbours, and three related pieces."""
    index_href = "../analysis.html" if site.key == "dsr" else "../index.html"
    index_label = "All analysis" if site.key == "dsr" else "All essays"

    for i, e in enumerate(entries):
        tm = team_of(e)
        rule = f'<hr class="teamrule" style="--tc:{tm[3]}">' if tm else ""
        label = f" &middot; {tm[2]}" if tm else ""

        newer = entries[i - 1] if i > 0 else None
        older = entries[i + 1] if i + 1 < len(entries) else None
        nav_bits = []
        if older:
            nav_bits.append(
                f'<a href="{older.slug}.html">&larr; {html.escape(older.title)}</a>'
            )
        if newer:
            nav_bits.append(
                f'<a href="{newer.slug}.html">{html.escape(newer.title)} &rarr;</a>'
            )
        prevnext = (
            f'<nav class="prevnext">{"".join(nav_bits)}</nav>' if nav_bits else ""
        )

        # Same team first, then anything else, newest first. Cheap, and it turns
        # a set of orphans into a graph a crawler and a reader can both walk.
        pool = [x for x in entries if x.slug != e.slug]
        same = [x for x in pool if set(x.teams) & set(e.teams)]
        rest = [x for x in pool if x not in same]
        related = (same + rest)[:3]
        related_html = (
            '<section class="related"><h3>More like this</h3>'
            + '<ul class="entry-list">'
            + "".join(entry_item(x) for x in related)
            + "</ul></section>"
            if related
            else ""
        )

        body = (
            f'<a class="back" href="{index_href}">&larr; {index_label}</a>'
            + (team_nav(e.team, depth=1, records=records)
               if site.key == "dsr" else "")
            + rule
            + f'<p class="meta"><time datetime="{e.day.isoformat()}">'
            + f"{e.day.strftime('%B')} {e.day.day}, {e.day.year}</time>{label}"
            + (f" &middot; {html.escape(e.cycle)}" if e.cycle else "")
            + f"</p><h2>{html.escape(e.title)}</h2>{render(e.body)}"
            + (ask_block(depth=1) if site.key == "dsr" else "")
            + prevnext
            + related_html
        )
        (site.out / "journal" / f"{e.slug}.html").write_text(
            page(site, f"{e.title}{site.title_sep}{site.title}", body, depth=1,
                 path=e.url, description=e.summary, kind="article", day=e.day),
            encoding="utf-8",
        )


def copy_assets(site: Site) -> None:
    """Static files that are not generated. `build.py` wipes the output
    directory every run, so anything hand-made has to be copied back in."""
    src = ROOT / "assets"
    if not src.exists():
        return
    dest = site.out / "assets"
    dest.mkdir(parents=True, exist_ok=True)
    for f in src.iterdir():
        if f.is_file():
            shutil.copy2(f, dest / f.name)


def write_common(site: Site, entries: list[Entry], home: str) -> None:
    copy_assets(site)
    (site.out / "index.html").write_text(
        page(site, home_title(site), home, path="",
             description=site.tagline), encoding="utf-8"
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
        pages += ["picks.html", "analysis.html", "requests.html", "about.html"]
        pages += [f"team/{slug}/" for slug, *_ in TEAMS]
    else:
        # essays.html is a redirect to "/" now and is deliberately absent: a
        # sitemap should not advertise a noindex page.
        pages += ["about.html"]
        log_dir = site.out / "log"
        pages += ["log/"] + sorted(
            (f"log/{p.name}/" for p in log_dir.iterdir() if p.is_dir()),
            reverse=True,
        )
    pages += ["feed.xml"]

    # lastmod is the main recrawl signal and it is free. Omitting it on a site
    # built entirely around timestamps was an odd thing to have done.
    newest = max((e.day for e in entries), default=date.today()).isoformat()
    urls = "\n".join(
        f"  <url><loc>{site.base_url}/{p}</loc>"
        f"<lastmod>{newest}</lastmod></url>"
        for p in pages
    )
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


def load_requests() -> list[dict]:
    """Reader requests, as data, from requests.json.

    Validated rather than trusted. A row marked answered must name an entry
    slug that exists in entries/, and the build stops if it does not. The page
    this feeds exists because "delivered" once meant a chart on a disk nobody
    could reach; a published page pointing at a 404 would be that same failure
    with better production values.
    """
    path = ROOT / "requests.json"
    if not path.exists():
        return []
    rows = json.loads(path.read_text(encoding="utf-8")).get("requests", [])
    for r in rows:
        if r.get("status") != "answered":
            continue
        slug = r.get("entry", "")
        if not (ROOT / "entries" / f"{slug}.md").exists():
            raise SystemExit(
                f"requests.json: answered request names entry '{slug}', "
                f"which has no file in entries/. Fix the slug or mark it open."
            )
    return rows


def requests_page_body(rows: list[dict]) -> str:
    """The ask, and the evidence that asking works.

    The order matters. The invitation comes first, because that is the point of
    the page, and the answered questions come second as proof rather than as an
    archive: a reader deciding whether it is worth typing an email wants to see
    that the last 4 people who asked got a real answer with numbers in it.
    """
    answered = [r for r in rows if r.get("status") == "answered"]
    still_open = [r for r in rows if r.get("status") != "answered"]

    def card(r: dict) -> str:
        link = (
            f' <a href="/journal/{r["entry"]}.html">Read the answer</a>'
            if r.get("status") == "answered" else ""
        )
        meta = f'Asked {r["asked"]} in {r["asked_where"]}'
        return (
            '<li class="req"><p class="q">'
            f'{html.escape(r["question"])}</p>'
            f'<p class="a">{html.escape(r.get("answer", ""))}{link}</p>'
            f'<p class="meta">{html.escape(meta)}</p></li>'
        )

    out = [
        "<h2>Ask for a breakdown</h2>",
        '<p class="sub">If there is a Detroit number you want looked at '
        "properly, ask and it gets looked at.</p>",
        render(
            "Something you argued about in a game thread and nobody could "
            "settle. A stat somebody quoted that smells wrong. A thing you have "
            "always assumed about one of these 4 teams and have never seen "
            "checked. Those are the best questions and they make better pieces "
            f"than anything picked unprompted.\n\n"
            f"**[{ASK_EMAIL}](mailto:{ASK_EMAIL})**\n\n"
            "Every question that arrives gets listed on this page, with the "
            "answer when there is one, including the ones where the answer is "
            "no or the data doesn't exist. Nothing gets quietly dropped. If a "
            "question needs a lot of work, that will be said too."
        ),
    ]
    if answered:
        out += [
            "<h2>Answered</h2>",
            '<p class="sub">Questions readers have already asked, and where '
            "the answer went.</p>",
            f'<ul class="reqs">{"".join(card(r) for r in answered)}</ul>',
        ]
    if still_open:
        out += [
            "<h2>Open</h2>",
            '<p class="sub">Asked, not answered yet. Listed so it is visible '
            "that they have not been.</p>",
            f'<ul class="reqs">{"".join(card(r) for r in still_open)}</ul>',
        ]
    return "".join(out)


def ask_block(depth: int = 0) -> str:
    """The request ask, rendered at the end of an entry.

    Added 2026-08-26 after counting where the two money routes were actually
    asked for. `MONEY.md` ranks "somebody pays for a specific breakdown" above
    tips, because it needs 1 reader rather than several hundred. The Ko-fi
    button was on all 52 pages of this site. The invitation to ask a question
    was on the homepage and on /requests.html, and /requests.html has been
    loaded zero times since it was published on 08-15. So the favourite route
    was asked for on the one page nobody visits and the coin-flip route was
    asked for everywhere.

    This puts it at the bottom of the piece, which is where a reader who just
    got something out of it is sitting. The address is inline rather than
    behind a link because a route that needs 1 person cannot afford a click.
    """
    up = "../" * depth
    return (
        '<div class="note ask">'
        "<p><strong>Got a Detroit number you want looked at?</strong> "
        f'Email <a href="mailto:{ASK_EMAIL}">{ASK_EMAIL}</a> and it gets '
        "looked at properly. A stat somebody quoted that smells wrong, a thing "
        "you have always assumed about one of these 4 teams and have never seen "
        "checked. Every question that arrives is "
        f'<a href="{up}requests.html">listed with its answer</a>, including the '
        "ones where the answer is no.</p></div>"
    )


def tip_block(text: str) -> str:
    return f"""<div class="tip">
<p>{text}</p>
<p><a class="btn" href="{KOFI}">Tip $1 on Ko-fi</a></p>
</div>"""


def picks_cards(md: str, writeups: dict[str, dict[str, str]] | None = None,
                limit: int | None = None) -> str:
    """The picks ledger as cards, at every width.

    Built from the same markdown rows the ledger is stored in, so the page and
    PICKS.md cannot drift apart. Each card carries its own reasoning and grade
    links: the write-ups used to be a separate list of full-size entries below
    the board, which pushed the analysis — the part readers actually come for —
    another screen down. His call 2026-08-12.
    """
    rows = [ln.strip() for ln in md.split("\n") if ln.strip().startswith("|")]
    if len(rows) < 3:
        return ""
    writeups = writeups or {}
    header = [c.strip() for c in rows[0].strip("|").split("|")]
    out = []
    for line in rows[2:]:
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != len(header):
            continue
        row = dict(zip(header, cells))
        game = re.sub(r"\s*\(`[^`]*`\)", "", row.get("Game (MLB gamePk)", ""))
        result = row.get("Result", "")
        grade = row.get("Grade", "")
        outcome = (
            f"{inline(result)} &middot; {inline(grade)}"
            if result and result not in ("pending", "—", "-")
            else "Not played yet"
        )
        links = writeups.get(row.get("#", ""), {})
        why = "".join(
            f'<a href="{href}">{label}</a>'
            for label, href in (
                ("Why I called it", links.get("pick")),
                ("How it graded", links.get("grade")),
            )
            if href
        )
        out.append(
            "<li>"
            f'<div class="g">{inline(row.get("First pitch", ""))}</div>'
            f'<div class="c">{inline(game)}</div>'
            f'<div class="c"><strong>{inline(row.get("Call", ""))}</strong>'
            f'<span class="chip" style="margin-left:.5rem">'
            f'{inline(row.get("Confidence", ""))}</span></div>'
            f'<div class="o">{outcome}</div>'
            + (f'<div class="why">{why}</div>' if why else "")
            + "</li>"
        )
        if limit and len(out) >= limit:
            break
    return f'<ul class="pickcards">{"".join(out)}</ul>'


def team_records(md: str, entries: list[Entry]) -> dict[str, tuple[int, int, int]]:
    """Slug -> (wins, losses, pending), from the ledger joined to the entries.

    The ledger has no team column, and adding one would mean maintaining the
    same fact in 2 places. The pick's own write-up already carries `team:`, so
    the pick number is the join and the ledger stays as it is.
    """
    by_no = {}
    for e in entries:
        m = PICK_NO.search(e.slug)
        if m and not e.cycle.lower().startswith("grade") and e.teams:
            by_no[str(int(m.group(1)))] = e.teams[0]

    out: dict[str, list[int]] = {slug: [0, 0, 0] for slug, *_ in TEAMS}
    rows = [ln.strip() for ln in md.split("\n") if ln.strip().startswith("|")]
    if len(rows) < 3:
        return {k: tuple(v) for k, v in out.items()}
    header = [c.strip() for c in rows[0].strip("|").split("|")]
    for line in rows[2:]:
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != len(header):
            continue
        row = dict(zip(header, cells))
        slug = by_no.get(row.get("#", ""))
        if slug not in out:
            continue
        grade = row.get("Grade", "").lower()
        if "correct" in grade:
            out[slug][0] += 1
        elif "wrong" in grade or "❌" in grade:
            out[slug][1] += 1
        else:
            out[slug][2] += 1
    return {k: tuple(v) for k, v in out.items()}


def record_note(records: dict[str, tuple[int, int, int]], depth: int = 0) -> str:
    """The one line under the team nav: overall record, and where to audit it.

    The per-team numbers ride in the nav pills now, so this carries only the
    total and the provenance. It used to be a second row of team pills sitting
    directly under the first; his call 2026-08-14 was to merge them.

    Ungraded calls are deliberately not in the total. "4-1 +1" reads as a third
    number in a win-loss line, and the pending game is on the board below with
    its own "Not played yet".
    """
    up = "../" * depth
    total_w = sum(r[0] for r in records.values())
    total_l = sum(r[1] for r in records.values())
    return (f'<p class="recnote">Overall <strong>{total_w}-{total_l}</strong>. '
            "Every call posted before first pitch and graded after the last "
            f'out. <a href="{up}picks.html">The full record</a>.</p>')


# Matches a pick number in a slug: "...pick-03-..." and "...grade-pick-03".
# Used by both team_records() above and pick_writeups() below, which is why it
# sits between them.
PICK_NO = re.compile(r"pick[-\s]*(?:no\.?\s*)?0*(\d+)", re.I)


def pick_writeups(entries: list[Entry]) -> dict[str, dict[str, str]]:
    """Pick number -> {"pick": url, "grade": url}.

    The number comes from the slug (`...pick-03-...`, `...grade-pick-03`), which
    is the only field both the ledger row and the entry reliably share.
    """
    out: dict[str, dict[str, str]] = {}
    for e in entries:
        m = PICK_NO.search(e.slug)
        if not m:
            continue
        kind = "grade" if e.cycle.lower().startswith("grade") else "pick"
        out.setdefault(str(int(m.group(1))), {})[kind] = e.url
    return out


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
                 depth=2, path=f"log/{day}/"),
            encoding="utf-8",
        )

    def day_row(day: str, cycles: list[dict], prefix: str) -> str:
        """A day, its count and the titles in it. No excerpts: the excerpt
        version made /, /log/ and /log/<date>/ three views of the same text."""
        titles = "; ".join(html.escape(c["title"]) for c in cycles[:3])
        more = f" and {len(cycles) - 3} more" if len(cycles) > 3 else ""
        return (
            f'<li><a href="{prefix}{day}/"><span class="meta">{len(cycles)} '
            + ("cycle" if len(cycles) == 1 else "cycles")
            + f'</span><span class="t">{pretty_day(day)}</span>'
            + f'<span class="s">{titles}{more}</span></a></li>'
        )

    index_body = (
        "<h2>Working log</h2>"
        + '<p class="sub">What each cycle did, what failed and what it decided. '
        "One page per day, newest first. This is the raw tape; the essays are the "
        "considered version.</p>"
        + '<ul class="entry-list">'
        + "".join(day_row(day, cycles, "") for day, cycles in days)
        + "</ul>"
    )
    (site.out / "log" / "index.html").write_text(
        page(site, f"Working log{site.title_sep}{site.title}", index_body,
             depth=1, path="log/",
             description="What each cycle of this experiment did, failed at, and decided."),
        encoding="utf-8",
    )

    intro_md = (ROOT / "intro.md").read_text(encoding="utf-8")

    # The essays ARE the landing page; /essays.html was a second copy of the
    # same list at a second URL, which splits inbound links and makes the nav
    # point away from the page a reader is already on. His call 2026-08-12. It
    # still serves, because it has been in the sitemap and submitted to IndexNow
    # and a URL that has been advertised should not start 404ing.
    (site.out / "essays.html").write_text(
        redirect_page(site, "essays.html", "", "Essays"),
        encoding="utf-8",
    )
    (site.out / "about.html").write_text(
        page(site, f"About{site.title_sep}{site.title}", render(intro_md),
             path="about.html",
             description="What this experiment is, how it works, and what it is trying to prove."),
        encoding="utf-8",
    )

    recent, rest = days[:3], days[3:]
    log_teaser = (
        "<h2>Working log</h2>"
        + '<p class="sub">Every cycle writes down what it did, what failed and '
        "what it decided. The last three days:</p>"
        + '<ul class="entry-list">'
        + "".join(day_row(day, cycles, "log/") for day, cycles in recent)
        + "</ul>"
        + '<p class="more"><a href="log/">Every day since the start'
        + (f", {len(rest)} more" if rest else "")
        + "</a></p>"
    )
    tip = tip_block(
        "<strong>The whole goal is one dollar.</strong> Not a subscription, not "
        "a business — one dollar, from one stranger, because something here was "
        "worth it. If this experiment is worth following, that's the entire ask."
    )
    # Order matters and this is the order: the good writing, the raw log, then
    # housekeeping. The full explainer used to sit on top of it, which meant
    # every return visitor scrolled past the same unchanging block of text to
    # reach the one part of the page that had changed. It lives on /about.html
    # now, with a single line here for anyone arriving cold. His call 2026-08-12.
    home = (
        "<h2>Essays</h2>"
        + '<p class="sub">An AI agent has six months to earn one dollar. These '
        "are the considered pieces on where that stands: what is working, what "
        'is not, and what the plan is. <a href="about.html">What this is</a>.</p>'
        + f'<ul class="entry-list">{"".join(entry_item(e) for e in process)}</ul>'
        + log_teaser
        + scoreboard
        + tip
    )
    write_common(site, process, home)

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

    picks_md_raw = (ROOT / "PICKS.md").read_text(encoding="utf-8")
    # Records first: the team nav carries them on every page of this site, so
    # they have to exist before anything is rendered.
    recs = team_records(picks_md_raw, analysis)

    write_entry_pages(site, analysis, recs)

    picks_md = picks_md_raw
    # Drop the H1; the homepage supplies its own heading.
    picks_md = re.sub(r"^# .*\n", "", picks_md, count=1)
    # Cycles append new picks to the bottom of the file, which is right for an
    # append-only ledger and wrong for a reader: by October the newest call
    # would be a long scroll down. Reverse the rows at render time so the file
    # stays append-only and the page shows newest first. His call 2026-08-09.
    ordered = newest_first(picks_md)
    writeups = pick_writeups(analysis)

    # The board leads. It is the product, and a reader should hit it before any
    # explanation of it. His call 2026-08-09 was that the self-congratulation
    # about the record reads badly and the board should simply be there. His
    # call 2026-08-12 was that it should also be short: the homepage shows the
    # four most recent calls, the full ledger has its own page, and the analysis
    # starts within a screen of the top.
    HOME_PICKS = 4
    picks_html = picks_cards(ordered, writeups, limit=HOME_PICKS)

    # The record line lived inside the ledger prose the homepage used to render
    # whole. Pull just that one number forward; the rest of the explanation is
    # on /about.html where a reader who wants it will look.
    # The record itself moved up into the strip above the board, so this line
    # is only the provenance now. Repeating "Record 4-1" here would put the same
    # number twice on one screen.
    about = (
        '<div class="note">Every prediction is a public commit, timestamped '
        f'before the game. <a href="{REPO}">Receipts</a>.</div>'
    )
    tip = tip_block(
        "<strong>Free, and staying that way.</strong> No subscriptions, no "
        "paywall, nothing for sale. If a call or a piece was worth something to "
        "you, the tip jar is open."
    )
    # The ask sits above the tip jar rather than inside it, because they are
    # different requests and pairing them makes the question look like a price
    # list. Asking is free and always will be.
    ask = (
        '<div class="note">Got a Detroit number you want looked at? '
        '<a href="requests.html">Ask for a breakdown</a>. '
        "Every question that arrives gets listed, answered or not.</div>"
    )
    by_team = {}
    for e in analysis:
        by_team.setdefault(e.teams[0] if e.teams else "", []).append(e)

    # Grades are a different product from writing: they report a result the
    # board already shows. They reach the reader through their own pick's card
    # now, so the homepage list is analysis and nothing else. Every grade is
    # still on /analysis.html, in the feed and on its team page.
    grades = [e for e in analysis if e.cycle.lower().startswith("grade")]
    essays = [e for e in analysis if e not in grades]

    teams_block = (
        '<h2 id="teams">By team</h2>'
        + '<ul class="entry-list">'
        + "".join(
            f'<li><a href="team/{slug}/"><span class="t">{full}</span>'
            f'<span class="meta">'
            + (
                f"{len(by_team.get(slug, []))} piece"
                + ("" if len(by_team.get(slug, [])) == 1 else "s")
                if by_team.get(slug)
                else "nothing yet; the page is waiting"
            )
            + "</span></a></li>"
            for slug, short, full, *_ in TEAMS
        )
        + "</ul>"
    )

    home = (
        team_nav(records=recs)
        + record_note(recs)
        + '<h2 id="picks">Every call, before the game</h2>'
        + picks_html
        + about
        + (
            "<h2>Analysis</h2>"
            + f'<ul class="entry-list">{"".join(entry_item(e) for e in essays)}</ul>'
            if essays
            else ""
        )
        + teams_block
        + ask
        + tip
    )
    write_common(site, analysis, home)

    # The complete ledger, table and all, so trimming the homepage to four cards
    # hides nothing. This is where a reader goes to audit the record.
    (site.out / "picks.html").write_text(
        page(site, f"Every call{site.title_sep}{site.title}",
             "<h2>Every call, before the game</h2>"
             + '<p class="sub">Committed to a public repository before first '
             'pitch, graded after the last out. Newest first.</p>'
             + picks_cards(ordered, writeups)
             + "<h2>The raw ledger</h2>"
             + '<p class="sub">The same calls as they are stored in the '
             "repository, carrying the league's own game id so a grade can only "
             "be matched to the exact game that was called.</p>"
             + f'<div class="scroll">{render(ordered)}</div>',
             path="picks.html",
             description="Every Detroit prediction, its confidence, its result and its grade."),
        encoding="utf-8",
    )

    # A full analysis index, so the nav's "Analysis" goes somewhere real rather
    # than to an anchor halfway down the homepage.
    (site.out / "analysis.html").write_text(
        page(site, f"All analysis{site.title_sep}{site.title}",
             "<h2>Every piece</h2>"
             + '<p class="sub">Calls, grades and analysis, newest first.</p>'
             + f'<ul class="entry-list">{"".join(entry_item(e) for e in analysis)}</ul>',
             path="analysis.html",
             description="Every Detroit Tigers, Lions, Pistons and Red Wings piece, newest first."),
        encoding="utf-8",
    )
    (site.out / "requests.html").write_text(
        page(site, f"Requests{site.title_sep}{site.title}",
             requests_page_body(load_requests()),
             path="requests.html",
             description="Ask for a Detroit breakdown, and see the questions "
                         "readers have already asked and where the answers went."),
        encoding="utf-8",
    )
    (site.out / "about.html").write_text(
        page(site, f"About{site.title_sep}{site.title}",
             "<h2>How this works</h2>"
             + render(
                 "Every prediction on this site is committed to a public "
                 f"repository **before** the game starts, at [{REPO}]({REPO}). "
                 "The commit timestamp is the proof, and git history makes any "
                 "later edit visible.\n\n"
                 "Every prediction is then graded after the final out, win or "
                 "lose. Nothing is deleted and no call is quietly revised.\n\n"
                 "Confidence has two settings. **High** means I like it and I "
                 "will look stupid if it misses. **Low** means picking a side is "
                 "the job, and I will tell you what worries me.\n\n"
                 "The analysis is built from primary sources: the MLB Stats API "
                 "for baseball and ESPN's public data for the other three "
                 "sports. Scripts that produce the numbers live in the same "
                 "repository, so any figure here can be re-derived.\n\n"
                 "Nothing here is betting advice.\n\n"
                 "The skyline photograph is released under CC0 and comes from "
                 "[Wikimedia Commons]"
                 "(https://commons.wikimedia.org/wiki/File:Detroit_Skyline_(123143197).jpeg). "
                 "No team logos or marks appear anywhere on this site; the "
                 "colours are just colours."
             ),
             path="about.html",
             description="How the predictions work: committed before the game, graded after, nothing deleted."),
        encoding="utf-8",
    )

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
        mine = [e for e in analysis if slug in e.teams]
        (site.out / "team" / slug).mkdir(parents=True, exist_ok=True)
        if mine:
            listing = f'<ul class="entry-list">{"".join(entry_item(e, depth=2) for e in mine)}</ul>'
        else:
            listing = ('<div class="note">Nothing here yet. Calls go up before the '
                       'game and grades go up after, so this page fills in as the '
                       'season does.</div>')
        body = (
            team_nav(slug, depth=2, records=recs)
            + f'<hr class="teamrule" style="--tc:{light}">'
            + f"<h2>{full}</h2>"
            + f'<p>Every {short} call and every grade, in one place.</p>'
            + listing
        )
        (site.out / "team" / slug / "index.html").write_text(
            page(site, f"{full}{site.title_sep}{site.title}", body, depth=2,
                 path=f"team/{slug}/",
                 description=f"Detroit {short} analysis: calls made before the game, graded after.",
                 accent=light),
            encoding="utf-8",
        )

    # An entry takes its team's colour too, so a Tigers piece and a Lions piece
    # are not the same page with different words. A post-pass, because
    # write_entry_pages is shared with the journal, which has no teams.
    for e in analysis:
        tm = team_of(e)
        if not tm:
            continue
        fp = site.out / "journal" / f"{e.slug}.html"
        doc = fp.read_text(encoding="utf-8")
        fp.write_text(
            doc.replace('<div class="band">',
                        f'<div class="band" style="color:{tm[3]}">', 1),
            encoding="utf-8",
        )


def build() -> None:
    # Validated before anything is written, because build_dsr() wipes the output
    # directory first. Discovered by testing the failure path: a bad slug in
    # requests.json used to exit 1 having already deleted the built site.
    load_requests()
    entries = sorted(
        (parse(p) for p in ENTRIES.glob("*.md")),
        key=lambda e: (e.day, e.seq, e.slug),
        reverse=True,
    )
    analysis = [e for e in entries if e.track == "analysis"]
    process = [e for e in entries if e.track != "analysis"]

    build_journal(process)
    build_dsr(analysis)
    print(f"journal: {len(process)} entries -> {JOURNAL.out}")
    print(f"dsr:     {len(analysis)} entries -> {DSR.out}")
    if BEACON_MISSES:
        print("", file=sys.stderr)
        print("!! NO ANALYTICS BEACON IN THIS BUILD. The pages will collect "
              "nothing and page views will not exist.", file=sys.stderr)
        for why in dict.fromkeys(BEACON_MISSES):
            print(f"   - {why}", file=sys.stderr)
        print("   Do not record page views as 'live' in MEASURE.md after a "
              "build that printed this.", file=sys.stderr)


if __name__ == "__main__":
    build()
