#!/usr/bin/env python3
"""Static site generator for fintechtunisia.com (EN + FR).

usage: python3 build.py live|preview OUTDIR
  live    -> pretty URLs (/blog/), for GitHub Pages
  preview -> explicit index.html links, for file-based previews
"""
import json, glob, os, re, sys, shutil, html, math, datetime
from xml.sax.saxutils import escape as xesc
import markdown
from covers import cover_svg
from i18n import *
import i18n_ar  # noqa: F401  (patches Arabic copy into i18n dicts)
import extra as XP
from i18n_extra import NAV, GOATCOUNTER, X as XX, ABOUT, EDITORIAL, CORRECTIONS

MODE = sys.argv[1] if len(sys.argv) > 1 else "live"
OUT = sys.argv[2] if len(sys.argv) > 2 else "dist"
HERE = os.path.dirname(os.path.abspath(__file__))
BUILD_DATE = "2026-10-10"
LANGS = ["en", "fr", "ar"]
RTL = {"ar"}
LANG_SHORT = {"en": "EN", "fr": "FR", "ar": "ع"}
LANG_NAME = {"en": "English", "fr": "Français", "ar": "العربية"}
E = html.escape
AC = ' aria-current="page"'
GC = f'<script data-goatcounter="https://{GOATCOUNTER}.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'
NBSP = "\u00a0"


def iso(d):
    """Full ISO 8601 datetime with Tunis time zone, as Google expects."""
    d = str(d)
    return d if "T" in d else (d + "T08:00:00+01:00" if len(d) == 10 else d)

# ---------------------------------------------------------------- content
posts = []
for f in sorted(glob.glob(os.path.join(HERE, "content", "*.json"))):
    d = json.load(open(f, encoding="utf-8"))
    d["slug"] = os.path.basename(f)[:-5]
    d.setdefault("date", BUILD_DATE)
    d["modified"] = BUILD_DATE
    arf = os.path.join(HERE, "content_ar", d["slug"] + ".json")
    if os.path.exists(arf):
        a = json.load(open(arf, encoding="utf-8"))
        d["ar"] = a["ar"]
        for i, st in enumerate(d.get("stats") or []):
            if i < len(a.get("stats_ar") or []): st["label_ar"] = a["stats_ar"][i]
            if i < len(a.get("stats_value_ar") or []): st["value_ar"] = a["stats_value_ar"][i]
        if d.get("chart") and a.get("chart_ar"):
            d["chart"]["title_ar"] = a["chart_ar"]["title"]
            d["chart"]["source_name_ar"] = a["chart_ar"].get("source_name")
            for i, b in enumerate(d["chart"]["bars"]):
                b["label_ar"] = a["chart_ar"]["bars"][i]
    for L in LANGS:
        words = len(re.sub(r"[#*_`>\[\]()]", " ", d[L]["body"]).split())
        d[L]["words"] = words
        d[L]["minutes"] = max(3, round(words / 220))
    posts.append(d)

# Editorial order for same-date posts: interleave categories so lists look varied
_order = {c: i for i, c in enumerate(CATS)}
by_cat = {c: [p for p in posts if p["category"] == c] for c in CATS}
inter, i = [], 0
while any(by_cat.values()):
    for c in CATS:
        if by_cat[c]: inter.append(by_cat[c].pop(0))
rank = {p["slug"]: n for n, p in enumerate(inter)}
FEATURE_FIRST = ["tunisia-fintech-ecosystem-map", "tunisia-startup-funding-trends", "payment-institutions-tunisia", "mobile-payments-tunisia"]
for n, s in enumerate(FEATURE_FIRST): rank[s] = -100 + n
posts.sort(key=lambda p: (p["date"], -rank[p["slug"]]), reverse=True)
POST = {p["slug"]: p for p in posts}

# Vary covers that share a category + motif
seen = {}
for p in sorted(posts, key=lambda p: p["slug"]):
    k = (p["category"], p.get("cover_motif"))
    p["variant"] = seen.get(k, 0); seen[k] = p["variant"] + 1


# ---------------------------------------------------------------- urls
def path_of(lang, kind, key=None):
    pre = {"en": "", "fr": "fr/", "ar": "ar/"}[lang]
    return {
        "home": f"{pre}index.html", "blog": f"{pre}blog/index.html",
        "cat": f"{pre}blog/category/{key}.html", "post": f"{pre}blog/{key}.html",
        "programs": f"{pre}programs.html", "contact": f"{pre}contact.html", "feed": f"{pre}feed.xml",
        "about": f"{pre}about.html", "editorial": f"{pre}editorial-policy.html", "corrections": f"{pre}corrections.html",
        "directory": f"{pre}directory/index.html", "company": f"{pre}directory/{key}.html", "tracker": f"{pre}regulation-tracker.html",
    }[kind]


def pretty(p):
    if MODE == "live":
        if p == "index.html": return ""
        if p.endswith("/index.html"): return p[:-10]
    return p


def absu(p):
    if p == "index.html": p = ""
    elif p.endswith("/index.html"): p = p[:-10]
    return f"{SITE}/{p}"


class Page:
    def __init__(self, path): self.path = path; self.depth = path.count("/")
    def rel(self, target):
        r = "../" * self.depth + pretty(target)
        return r if r else "./"


def cover_rel(slug): return f"assets/covers/{slug}.svg"
def og_rel(slug, L="en"): return f"assets/og/{slug}{'' if L == 'en' else '-' + L}.jpg"


def statval(s, L):
    if L == "ar": return s.get("value_ar") or s["value"]
    return frnum(s["value"], L)


def frnum(v, L):
    """Localise a free-text figure like '37.8%' or '1,352' for French."""
    if L == "en": return v
    v = re.sub(r"(\d),(\d{3})", "\\1\u202f\\2", v)
    v = re.sub(r"(\d),(\d{3})", "\\1\u202f\\2", v)
    v = re.sub(r"(\d)\.(\d)", r"\1,\2", v)
    v = re.sub(r"(\d)%", "\\1\u00a0%", v)
    return v


# ---------------------------------------------------------------- formatting
MONTHS_FR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
MONTHS_AR = ["جانفي", "فيفري", "مارس", "أفريل", "ماي", "جوان", "جويلية", "أوت", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def fdate(s, L):
    d = datetime.date.fromisoformat(s)
    if L == "ar": return f"{d.day} {MONTHS_AR[d.month-1]} {d.year}"
    return f"{MONTHS_EN[d.month-1]} {d.day}, {d.year}" if L == "en" else f"{d.day} {MONTHS_FR[d.month-1]} {d.year}"


def fnum(v, L):
    v = float(v)
    dec = 0 if v == int(v) else (2 if abs(v) < 10 and round(v, 2) != round(v, 1) else 1)
    s = f"{v:,.{dec}f}"
    if L == "fr": s = s.replace(",", " ").replace(".", ",")
    if L == "ar": s = s.replace(",", " ").replace(".", ",")
    return s


def fval(v, unit, L):
    n = fnum(v, L); u = unit.strip()
    sp = " "
    table = {
        "%": (f"{n}%", f"{n}{sp}%"),
        "$M": (f"${n}M", f"{n}{sp}M$"), "US$M": (f"${n}M", f"{n}{sp}M$"),
        "US$bn": (f"${n}bn", f"{n}{sp}Md$"), "€M": (f"€{n}M", f"{n}{sp}M€"),
        "bn TND": (f"TND{sp}{n}bn", f"{n}{sp}Md{sp}TND"), "M TND": (f"TND{sp}{n}M", f"{n}{sp}M{sp}TND"),
        "TND": (f"TND{sp}{n}", f"{n}{sp}TND"), "EGP m": (f"EGP{sp}{n}m", f"{n}{sp}M{sp}EGP"),
        "M": (f"{n}M", f"{n}{sp}M"),
    }
    ar = {"%": f"{n}%", "$M": f"{n} مليون دولار", "US$M": f"{n} مليون دولار", "US$bn": f"{n} مليار دولار",
          "€M": f"{n} مليون يورو", "bn TND": f"{n} مليار دينار", "M TND": f"{n} مليون دينار", "TND": f"{n} دينار",
          "EGP m": f"{n} مليون جنيه", "M": f"{n} مليون"}
    if L == "ar": return ar.get(u, n)
    if u in table: return table[u][0 if L == "en" else 1]
    return n


# ---------------------------------------------------------------- markdown
def slugify(value, sep="-"):
    import unicodedata
    v = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    out = re.sub(r"[^a-z0-9]+", "-", v.lower()).strip("-")[:60]
    if len(out) < 3:  # Arabic or other non-Latin heading
        out = re.sub(r"[^\w]+", "-", value, flags=re.U).strip("-")[:60]
    return out


def render_md(text, page, L):
    def repl(m):
        target = m.group(1)
        if target in POST: return "](" + page.rel(path_of(L, "post", target)) + ")"
        return "](" + page.rel(path_of(L, "blog")) + ")"
    text = re.sub(r"\]\(post:([a-z0-9\-]+)\)", repl, text)
    md = markdown.Markdown(extensions=["tables", "sane_lists", "toc"], extension_configs={"toc": {"slugify": slugify, "toc_depth": "2"}})
    out = md.convert(text)
    out = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', out)
    out = out.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    toc = [(t["id"], t["name"]) for t in md.toc_tokens]
    return out, toc


# ---------------------------------------------------------------- icons
ICON = {
    "linkedin": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.34V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.07 2.07 0 1 1 0-4.13 2.07 2.07 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45z"/></svg>',
    "facebook": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 12a10 10 0 1 0-11.56 9.88v-6.99H7.9V12h2.54V9.8c0-2.5 1.49-3.89 3.78-3.89 1.1 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56V12h2.78l-.44 2.89h-2.34v6.99A10 10 0 0 0 22 12z"/></svg>',
    "x": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18.24 2.25h3.31l-7.23 8.26 8.5 11.24h-6.66l-5.21-6.82-5.97 6.82H1.67l7.73-8.84L1.25 2.25h6.83l4.71 6.23 5.45-6.23zm-1.16 17.52h1.83L7.08 4.13H5.12l11.96 15.64z"/></svg>',
    "whatsapp": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.65.07-.3-.15-1.26-.46-2.4-1.48-.89-.79-1.49-1.77-1.66-2.07-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.08c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.69.63.71.23 1.36.2 1.87.12.57-.08 1.76-.72 2.01-1.42.25-.7.25-1.29.17-1.42-.07-.12-.27-.2-.57-.35zM12.05 21.8h-.01a9.8 9.8 0 0 1-5-1.37l-.36-.21-3.72.98 1-3.63-.24-.37a9.8 9.8 0 0 1-1.5-5.2C2.22 6.58 6.63 2.18 12.06 2.18c2.63 0 5.1 1.03 6.96 2.89a9.78 9.78 0 0 1 2.88 6.96c0 5.43-4.41 9.83-9.85 9.83z"/></svg>',
    "search": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10.5 3a7.5 7.5 0 0 1 5.96 12.06l4.24 4.24-1.42 1.42-4.24-4.24A7.5 7.5 0 1 1 10.5 3zm0 2a5.5 5.5 0 1 0 0 11 5.5 5.5 0 0 0 0-11z"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.17 5.3l6.7 6.7-6.7 6.7-1.41-1.41L16.05 13H4v-2h12.05l-4.29-4.29z"/></svg>',
    "globe": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 1 1 0 20 10 10 0 0 1 0-20zm6.93 9a8.03 8.03 0 0 0-3.03-5.6c.6 1.6.97 3.5 1.07 5.6h1.96zM12 4.06c-.74.9-1.67 3.17-1.94 6.94h3.88C13.67 7.23 12.74 4.96 12 4.06zM8.1 5.4A8.03 8.03 0 0 0 5.07 11h1.96c.1-2.1.47-4 1.07-5.6zM5.07 13a8.03 8.03 0 0 0 3.03 5.6c-.6-1.6-.97-3.5-1.07-5.6H5.07zm4.99 0c.27 3.77 1.2 6.04 1.94 6.94.74-.9 1.67-3.17 1.94-6.94h-3.88zm5.84 5.6A8.03 8.03 0 0 0 18.93 13h-1.96c-.1 2.1-.47 4-1.07 5.6z"/></svg>',
}


# ---------------------------------------------------------------- layout
def head(page, L, title, desc, canonical_path, alt_paths, og_image, og_type="website", extra_meta="", ld=None, noindex=False):
    t = T[L]
    alts = "".join(f'<link rel="alternate" hreflang="{l}" href="{absu(p)}">' for l, p in alt_paths.items())
    if "en" in alt_paths: alts += f'<link rel="alternate" hreflang="x-default" href="{absu(alt_paths["en"])}">'
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld or []))
    return f"""<!doctype html>
<html lang="{L}" dir="{'rtl' if L in RTL else 'ltr'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
{'<meta name="robots" content="noindex">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'}
<link rel="canonical" href="{absu(canonical_path)}">
{alts}
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{absu(canonical_path)}">
<meta property="og:image" content="{SITE}/{og_image}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:locale" content="{t['locale']}">{''.join(f'<meta property="og:locale:alternate" content="{T[o]["locale"]}">' for o in LANGS if o != L)}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(desc)}">
<meta name="twitter:image" content="{SITE}/{og_image}">
{extra_meta}
<link rel="icon" href="{page.rel('assets/favicon.svg')}" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="{SITE_NAME} ({L.upper()})" href="{page.rel(path_of(L,'feed'))}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{page.rel('assets/site.css')}">
{f'<link rel="preload" as="font" type="font/woff2" crossorigin href="{page.rel("assets/fonts/ibm-plex-sans-arabic-400.woff2")}"><link rel="stylesheet" href="{page.rel("assets/rtl.css")}">' if L in RTL else ''}
<meta name="theme-color" content="#e31e24">
{lds}
{GC if MODE == "live" else ""}
</head>
<body>
<a class="skip" href="#main">{ {'en': 'Skip to content', 'fr': 'Aller au contenu', 'ar': 'انتقل إلى المحتوى'}[L] }</a>"""


def header(page, L, active, alts):
    t = T[L]
    links = [("articles", path_of(L, "blog")), ("directory", path_of(L, "directory")), ("tracker", path_of(L, "tracker")),
             ("programs", path_of(L, "programs")), ("about", path_of(L, "about")), ("contact", path_of(L, "contact"))]
    lab = lambda k: NAV[L].get(k) or t.get(k) or CAT[L][k]
    nav = "".join(f'<a href="{page.rel(p)}"{AC if k==active else ""}>{E(lab(k))}</a>' for k, p in links)
    langs = "".join(f'<a class="lang" href="{page.rel(alts[o])}" hreflang="{o}" lang="{o}" title="{LANG_NAME[o]}">{LANG_SHORT[o]}</a>' for o in LANGS if o != L and o in alts)
    return f"""
<header class="site-header">
  <div class="wrap nav">
    <a class="logo" href="{page.rel(path_of(L,'home'))}" aria-label="{SITE_NAME} — {t['home']}"><img src="{page.rel('assets/logo.png')}" alt="{SITE_NAME}" width="122" height="38"></a>
    <nav class="links" id="site-nav" aria-label="Main">{nav}</nav>
    <div class="nav-right">
      <div class="langs" role="group" aria-label="{t['language']}">{ICON['globe']}{langs}</div>
      <button class="menu-toggle" aria-label="Menu" aria-controls="site-nav" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<main id="main">"""


def newsletter(page, L):
    t = T[L]
    return f"""
<section class="newsletter">
  <div class="wrap nl-inner">
    <div><h2>{t['nl_title']}</h2><p>{t['nl_text']}</p></div>
    <form class="nl-form js-ajax-form" action="{FORMSPREE}" method="POST" data-err="{E(CONTACT[L]['err'])}">
      <input type="hidden" name="_subject" value="Newsletter signup ({L.upper()}) — Fintech Tunisia">
      <input type="hidden" name="language" value="{L}">
      <input type="text" name="_gotcha" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <label class="sr" for="nl-{page.depth}">{CONTACT[L]['email']}</label>
      <input id="nl-{page.depth}" type="email" name="email" placeholder="{t['nl_ph']}" required>
      <button class="btn btn-primary" type="submit">{t['nl_btn']}</button>
      <p class="form-ok" role="status">{t['nl_ok']}</p>
    </form>
  </div>
</section>"""


def footer(page, L):
    t = T[L]
    cats = "".join(f'<a href="{page.rel(path_of(L,"cat",c))}">{CAT[L][c]}</a>' for c in CATS)
    return f"""
</main>
{newsletter(page, L)}
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <div class="wordmark">Fin<span>Tech</span> Tunisia</div>
        <p>{t['tagline']}</p>
        <p class="foot-contact">{CONTACT[L]['address_v']}<br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        <p class="foot-langs">{' · '.join(f'<a href="{page.rel(path_of(o,"home"))}" hreflang="{o}" lang="{o}">{LANG_NAME[o]}</a>' for o in LANGS)}</p>
        <div class="social">
          <a href="{LINKEDIN}" target="_blank" rel="noopener" aria-label="LinkedIn">{ICON['linkedin']}</a>
          <a href="{FACEBOOK}" target="_blank" rel="noopener" aria-label="Facebook">{ICON['facebook']}</a>
        </div>
      </div>
      <div class="foot-col"><h3>{t['topics']}</h3>{cats}</div>
      <div class="foot-col"><h3>{t['explore']}</h3>
        <a href="{page.rel(path_of(L,'blog'))}">{t['all_articles']}</a>
        <a href="{page.rel(path_of(L,'directory'))}">{XX[L]['tool_dir']}</a>
        <a href="{page.rel(path_of(L,'tracker'))}">{XX[L]['tool_reg']}</a>
        <a href="{page.rel(path_of(L,'programs'))}">{t['programs']}</a>
        <a href="{page.rel(path_of(L,'feed'))}">RSS</a>
      </div>
      <div class="foot-col"><h3>{t['about']}</h3>
        <a href="{page.rel(path_of(L,'about'))}">{ABOUT[L]['h1']}</a>
        <a href="{page.rel(path_of(L,'editorial'))}">{EDITORIAL[L]['h1']}</a>
        <a href="{page.rel(path_of(L,'corrections'))}">{CORRECTIONS[L]['h1']}</a>
        <a href="{page.rel(path_of(L,'contact'))}">{t['contact']}</a>
      </div>

    </div>
    <div class="foot-bottom"><span>&copy; 2026 {SITE_NAME}. {t['rights']}</span><span>{t['footer_note']}</span></div>
  </div>
</footer>
<script src="{page.rel('assets/site.js')}" defer></script>
</body>
</html>"""


def card(page, L, p, size="", lazy=True):
    a = p[L]; url = page.rel(path_of(L, "post", p["slug"]))
    return f"""<article class="card {size}" data-search="{E((a['title']+' '+a['excerpt']+' '+' '.join(a.get('tags',[]))+' '+CAT[L][p['category']]).lower())}">
  <a class="card-media" href="{url}" tabindex="-1" aria-hidden="true"><img src="{page.rel(cover_rel(p['slug']))}" alt="" width="1200" height="630"{' loading="lazy"' if lazy else ''} decoding="async"></a>
  <div class="card-body">
    <a class="pill pill-{p['category']}" href="{page.rel(path_of(L,'cat',p['category']))}">{CAT[L][p['category']]}</a>
    <h3><a href="{url}">{E(a['title'])}</a></h3>
    <p>{E(a['excerpt'])}</p>
    <div class="meta"><time datetime="{p['date']}">{fdate(p['date'], L)}</time> · {a['minutes']} {T[L]['min_read']}</div>
  </div>
</article>"""


def org_ld():
    return {"@type": "Organization", "@id": f"{SITE}/#org", "name": SITE_NAME, "url": SITE + "/",
            "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/logo.png", "width": 600, "height": 189},
            "sameAs": [LINKEDIN, FACEBOOK], "email": EMAIL}


def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": absu(u)} for i, (n, u) in enumerate(items)]}


def crumbs_html(page, items):
    out = []
    for i, (n, u) in enumerate(items):
        if i < len(items) - 1: out.append(f'<a href="{page.rel(u)}">{E(n)}</a>')
        else: out.append(f'<span aria-current="page">{E(n)}</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span class="sep">/</span>'.join(out) + "</nav>"


_PROTECT = re.compile(r"(<svg.*?</svg>|<script.*?</script>|<style.*?</style>)", re.S)
_GROUP = re.compile(r"(\d)[ \u00a0](\d{3})(?!\d)")


def bidi_numbers(html_text):
    """In RTL pages, join digit groups ("512 000") with a narrow no-break space so the
    bidi algorithm keeps the number in one piece instead of reversing the groups."""
    parts = _PROTECT.split(html_text)
    for i in range(0, len(parts), 2):
        for _ in range(3): parts[i] = _GROUP.sub("\\1\u202f\\2", parts[i])
    return "".join(parts)


def write(path, content):
    if path.startswith("ar/"): content = bidi_numbers(content)
    full = os.path.join(OUT, path); os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    with open(full, "w", encoding="utf-8") as f: f.write(content)


# ---------------------------------------------------------------- article page
def stat_cards(p, L):
    st = p.get("stats") or []
    if not st: return ""
    items = "".join(f'<div class="stat"><div class="stat-v">{E(statval(s, L))}</div><div class="stat-l">{E(s["label_"+L])}</div><div class="stat-s">{E(s.get("source",""))}</div></div>' for s in st)
    return f'<section class="stats" aria-label="{T[L]["in_numbers"]}">{items}</section>'


def chart_html(p, L):
    c = p.get("chart")
    if not c: return ""
    bars = c["bars"]; mx = max(abs(float(b["value"])) for b in bars) or 1
    tunisia = re.compile(r"tunisi", re.I)
    has_tn = any(tunisia.search(b["label_en"]) for b in bars)
    rows = ""
    for b in bars:
        lab = b["label_" + L]; v = float(b["value"])
        hl = " hl" if (has_tn and tunisia.search(b["label_en"])) else ""
        rows += f'<div class="bar-row{hl}"><span class="bar-label">{E(lab)}</span><span class="bar-track"><span class="bar-fill" style="width:{max(1.5, v/mx*100):.1f}%"></span></span><span class="bar-val">{fval(v, c.get("unit",""), L)}</span></div>'
    trs = "".join(f'<tr><td>{E(b["label_"+L])}</td><td>{fval(b["value"], c.get("unit",""), L)}</td></tr>' for b in bars)
    src = c.get("source_name_" + L) or c.get("source_name", ""); su = c.get("source_url", "")
    srch = f'<a href="{E(su)}" target="_blank" rel="noopener">{E(src)}</a>' if su else E(src)
    return f"""<figure class="chart">
  <figcaption>{E(c['title_'+L])}</figcaption>
  <div class="bars{'' if has_tn else ' allred'}" role="img" aria-label="{E(c['title_'+L])}">{rows}</div>
  <p class="chart-src">{T[L]['source']}{NBSP + ':' if L == 'fr' else ':'} {srch}</p>
  <details class="chart-data"><summary>{T[L]['view_data']}</summary><table><thead><tr><th>{T[L]['label']}</th><th>{T[L]['value']}</th></tr></thead><tbody>{trs}</tbody></table></details>
</figure>"""


def related_for(p, n=3):
    same = [q for q in posts if q["category"] == p["category"] and q["slug"] != p["slug"]]
    linked = set(re.findall(r"post:([a-z0-9\-]+)", p["en"]["body"]))
    pool = [POST[s] for s in linked if s in POST and s != p["slug"]] + same
    out, seen_ = [], set()
    for q in pool:
        if q["slug"] not in seen_: out.append(q); seen_.add(q["slug"])
    for q in posts:
        if len(out) >= n: break
        if q["slug"] not in seen_ and q["slug"] != p["slug"]: out.append(q); seen_.add(q["slug"])
    return out[:n]


def build_post(p, L):
    a = p[L]; t = T[L]; slug = p["slug"]
    path = path_of(L, "post", slug); page = Page(path)
    alt = {l: path_of(l, "post", slug) for l in LANGS}
    body, toc = render_md(a["body"], page, L)
    # insert chart before the 3rd h2 (or at end)
    ch = chart_html(p, L)
    if ch:
        parts = body.split("<h2")
        if len(parts) > 3: body = "<h2".join(parts[:3]) + ch + "<h2" + "<h2".join(parts[3:])
        else: body += ch
    title = a["title"]; desc = a["meta_description"]
    url_abs = absu(path)
    faq = a.get("faq") or []
    lds = [
        {"@context": "https://schema.org", "@type": "BlogPosting", "@id": url_abs + "#article", "mainEntityOfPage": url_abs,
         "headline": title[:110], "description": desc, "image": [f"{SITE}/{og_rel(slug, L)}"],
         "datePublished": iso(p["date"]), "dateModified": iso(p["modified"]), "inLanguage": L,
         "articleSection": CAT[L][p["category"]], "keywords": ", ".join(a.get("keywords", [])), "wordCount": a["words"],
         "author": {"@type": "Organization", "name": t["byline"], "url": SITE + "/"},
         "publisher": org_ld(), "isAccessibleForFree": True,
         "citation": [{"@type": "CreativeWork", "name": s.get("title", ""), "url": s.get("url", "")} for s in p.get("sources", [])]},
        crumbs_ld([(t["home"], path_of(L, "home")), (t["breadcrumb_blog"], path_of(L, "blog")), (CAT[L][p["category"]], path_of(L, "cat", p["category"])), (title, path)]),
    ]
    if faq:
        lds.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faq]})
    extra = (f'<meta property="article:published_time" content="{p["date"]}T08:00:00+01:00">'
             f'<meta property="article:modified_time" content="{p["modified"]}T08:00:00+01:00">'
             f'<meta property="article:section" content="{E(CAT[L][p["category"]])}">' +
             "".join(f'<meta property="article:tag" content="{E(x)}">' for x in a.get("tags", [])) +
             f'<link rel="preload" as="image" href="{page.rel(cover_rel(slug))}">')
    h = head(page, L, f"{title} | {SITE_NAME}", desc, path, alt, og_rel(slug, L), "article", extra, lds)
    h += header(page, L, "articles", alt)
    take = "".join(f"<li>{E(x)}</li>" for x in a.get("key_takeaways", []))
    tocs = "".join(f'<li><a href="#{i}">{E(n)}</a></li>' for i, n in toc)
    faqs = "".join(f'<details class="faq-item"><summary>{E(f["q"])}</summary><p>{E(f["a"])}</p></details>' for f in faq)
    srcs = "".join(f'<li><a href="{E(s["url"])}" target="_blank" rel="noopener nofollow">{E(s.get("title") or s["url"])}</a>{" — " + E(s["publisher"]) if s.get("publisher") else ""}</li>' for s in p.get("sources", []))
    share_u = url_abs.replace(":", "%3A").replace("/", "%2F")
    share_t = E(title).replace(" ", "%20")
    share = (f'<div class="share"><span>{t["share"]}</span>'
             f'<a href="https://www.linkedin.com/sharing/share-offsite/?url={share_u}" target="_blank" rel="noopener" aria-label="LinkedIn">{ICON["linkedin"]}</a>'
             f'<a href="https://x.com/intent/post?url={share_u}&amp;text={share_t}" target="_blank" rel="noopener" aria-label="X">{ICON["x"]}</a>'
             f'<a href="https://www.facebook.com/sharer/sharer.php?u={share_u}" target="_blank" rel="noopener" aria-label="Facebook">{ICON["facebook"]}</a>'
             f'<a href="https://wa.me/?text={share_t}%20{share_u}" target="_blank" rel="noopener" aria-label="WhatsApp">{ICON["whatsapp"]}</a></div>')
    rel = "".join(card(page, L, q) for q in related_for(p))
    h += f"""
<article class="post">
  <header class="post-head">
    <div class="wrap narrow">
      {crumbs_html(page, [(t['home'], path_of(L,'home')), (t['breadcrumb_blog'], path_of(L,'blog')), (CAT[L][p['category']], path_of(L,'cat',p['category']))])}
      <a class="pill pill-{p['category']}" href="{page.rel(path_of(L,'cat',p['category']))}">{CAT[L][p['category']]}</a>
      <h1>{E(title)}</h1>
      <p class="dek">{E(a['excerpt'])}</p>
      <div class="post-meta">
        <span class="by">{t['byline']}</span>
        <span><time datetime="{p['date']}">{fdate(p['date'], L)}</time></span>
        <span>{a['minutes']} {t['min_read']}</span>
        <span class="other-lang">{ICON['globe']}{''.join(f'<a href="{page.rel(alt[o])}" hreflang="{o}" lang="{o}">{LANG_NAME[o]}</a>' for o in LANGS if o != L)}</span>
      </div>
    </div>
    <div class="wrap hero-wrap"><img class="post-hero" src="{page.rel(cover_rel(slug))}" alt="{E(title)}" width="1200" height="630" fetchpriority="high"></div>
  </header>
  <div class="wrap post-grid">
    <aside class="toc" aria-label="{t['on_this_page']}">
      <div class="toc-inner"><h2>{t['on_this_page']}</h2><ol>{tocs}</ol>{share}</div>
    </aside>
    <div class="post-body">
      {f'<section class="takeaways"><h2>{t["key_takeaways"]}</h2><ul>{take}</ul></section>' if take else ''}
      {stat_cards(p, L)}
      <div class="prose">{body}</div>
      {XP.mentioned_box(sys.modules[__name__], page, L, slug)}
      {f'<section class="faq" id="faq"><h2>{t["faq"]}</h2>{faqs}</section>' if faqs else ''}
      <section class="sources" id="sources"><h2>{t['sources']}</h2><ol>{srcs}</ol></section>
      <p class="disclaimer">{t['disclaimer']}</p>
      <div class="share-bottom">{share}</div>
    </div>
  </div>
</article>
<section class="related"><div class="wrap"><h2>{t['related']}</h2><div class="grid grid-3">{rel}</div></div></section>"""
    h += footer(page, L)
    write(path, h)


# ---------------------------------------------------------------- listing pages
def build_blog(L):
    t = T[L]; path = path_of(L, "blog"); page = Page(path)
    alt = {l: path_of(l, "blog") for l in LANGS}
    title = {"en": "Fintech in Tunisia & Africa: All Articles", "fr": "Fintech en Tunisie et en Afrique : tous les articles",
             "ar": "التكنولوجيا المالية في تونس وإفريقيا: كل المقالات"}[L]
    desc = {"en": f"{len(posts)} sourced articles on Tunisian fintech: BCT regulation, mobile payments, startups, funding, financial inclusion and African fintech.",
            "fr": f"{len(posts)} articles sourcés sur la fintech tunisienne : réglementation BCT, paiement mobile, startups, financement, inclusion et fintech africaine.",
            "ar": f"{len(posts)} مقالًا موثّقًا حول التكنولوجيا المالية في تونس: تشريعات البنك المركزي، والدفع عبر الجوال، والشركات الناشئة، والتمويل، والشمول المالي، والفنتك في إفريقيا."}[L]
    lds = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "description": desc, "url": absu(path), "inLanguage": L,
            "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": absu(path_of(L, "post", p["slug"]))} for i, p in enumerate(posts)]}},
           crumbs_ld([(t["home"], path_of(L, "home")), (t["breadcrumb_blog"], path)])]
    h = head(page, L, f"{title} | {SITE_NAME}", desc, path, alt, og_rel(posts[0]["slug"], L), ld=lds)
    h += header(page, L, "articles", alt)
    chips = f'<a class="chip active" href="{page.rel(path)}">{t["all_articles"]} <b>{len(posts)}</b></a>' + "".join(
        f'<a class="chip" href="{page.rel(path_of(L,"cat",c))}">{CAT[L][c]} <b>{sum(1 for p in posts if p["category"]==c)}</b></a>' for c in CATS)
    feat = posts[0]
    rest = "".join(card(page, L, p) for p in posts[1:])
    h += f"""
<section class="page-head"><div class="wrap">
  {crumbs_html(page, [(t['home'], path_of(L,'home')), (t['breadcrumb_blog'], path)])}
  <h1>{E(title)}</h1>
  <p class="lead">{E(desc)}</p>
  <div class="tools"><label class="search">{ICON['search']}<span class="sr">{t['search_ph']}</span><input type="search" id="post-search" placeholder="{t['search_ph']}" autocomplete="off"></label></div>
  <nav class="chips" aria-label="{t['topics']}">{chips}</nav>
</div></section>
<section class="listing"><div class="wrap">
  <div class="featured">{card(page, L, feat, 'card-feature', lazy=False)}</div>
  <div class="grid grid-3" id="post-grid">{rest}</div>
  <p class="no-results" hidden>{t['no_results']}</p>
</div></section>"""
    h += footer(page, L)
    write(path, h)


def build_cat(L, c):
    t = T[L]; path = path_of(L, "cat", c); page = Page(path)
    alt = {l: path_of(l, "cat", c) for l in LANGS}
    items = [p for p in posts if p["category"] == c]
    name = CAT[L][c]
    title = ({"en": f"{name}: Fintech in Tunisia & Africa", "fr": f"{name} : la fintech en Tunisie et en Afrique",
              "ar": f"{name}: التكنولوجيا المالية في تونس وإفريقيا"}[L] if c != "africa" else
             {"en": "African Fintech: Lessons for Tunisia", "fr": "Fintech africaine : leçons pour la Tunisie",
              "ar": "التكنولوجيا المالية في إفريقيا: دروس لتونس"}[L])
    desc = CAT_DESC[L][c]
    lds = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "description": desc, "url": absu(path), "inLanguage": L,
            "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": absu(path_of(L, "post", p["slug"]))} for i, p in enumerate(items)]}},
           crumbs_ld([(t["home"], path_of(L, "home")), (t["breadcrumb_blog"], path_of(L, "blog")), (name, path)])]
    h = head(page, L, f"{title} | {SITE_NAME}", desc, path, alt, og_rel(items[0]["slug"], L), ld=lds)
    h += header(page, L, "articles", alt)
    chips = f'<a class="chip" href="{page.rel(path_of(L,"blog"))}">{t["all_articles"]} <b>{len(posts)}</b></a>' + "".join(
        f'<a class="chip{" active" if k==c else ""}" href="{page.rel(path_of(L,"cat",k))}"{AC if k==c else ""}>{CAT[L][k]} <b>{sum(1 for p in posts if p["category"]==k)}</b></a>' for k in CATS)
    grid = "".join(card(page, L, p) for p in items)
    h += f"""
<section class="page-head cat-{c}"><div class="wrap">
  {crumbs_html(page, [(t['home'], path_of(L,'home')), (t['breadcrumb_blog'], path_of(L,'blog')), (name, path)])}
  <h1>{E(title)}</h1>
  <p class="lead">{E(desc)}</p>
  <nav class="chips" aria-label="{t['topics']}">{chips}</nav>
</div></section>
<section class="listing"><div class="wrap"><div class="grid grid-3">{grid}</div></div></section>"""
    h += footer(page, L)
    write(path, h)


# ---------------------------------------------------------------- home
def build_home(L):
    t = T[L]; c = HOME[L]; path = path_of(L, "home"); page = Page(path)
    alt = {l: path_of(l, "home") for l in LANGS}
    lds = [dict(org_ld(), **{"@context": "https://schema.org"}),
           {"@context": "https://schema.org", "@type": "WebSite", "@id": f"{SITE}/#website", "url": absu(path), "name": SITE_NAME, "inLanguage": L, "publisher": {"@id": f"{SITE}/#org"}}]
    h = head(page, L, c["title"], c["desc"], path, alt, og_rel("tunisia-fintech-ecosystem-map", L), ld=lds)
    h += header(page, L, "home", alt)
    feat = posts[0]
    side = posts[1:4]
    side_html = "".join(f"""<a class="mini" href="{page.rel(path_of(L,'post',p['slug']))}"><img src="{page.rel(cover_rel(p['slug']))}" alt="" width="1200" height="630" loading="lazy"><span><em class="pill pill-{p['category']}">{CAT[L][p['category']]}</em><strong>{E(p[L]['title'])}</strong></span></a>""" for p in side)
    stats = ""
    for slug, idx in HOME_STATS:
        p = POST.get(slug)
        if not p or not p.get("stats"): continue
        s = p["stats"][idx]; v = statval(s, L)
        stats += f'<a class="hstat" href="{page.rel(path_of(L,"post",slug))}"><span class="hstat-v">{E(v)}</span><span class="hstat-l">{E(s["label_"+L])}</span><span class="hstat-s">{E(s["source"])}</span></a>'
    latest = "".join(card(page, L, p) for p in posts[4:10])
    tiles = ""
    for k in CATS:
        items = [p for p in posts if p["category"] == k]
        tiles += f'<a class="tile tile-{k}" href="{page.rel(path_of(L,"cat",k))}"><img src="{page.rel(cover_rel(items[0]["slug"]))}" alt="" width="1200" height="630" loading="lazy"><span class="tile-t">{CAT[L][k]}</span><span class="tile-n">{len(items)} {t["articles_count"]}</span></a>'
    start = "".join(f'<li><a href="{page.rel(path_of(L,"post",s))}"><span class="num">{i+1:02d}</span><span><strong>{E(POST[s][L]["title"])}</strong><em>{E(POST[s][L]["excerpt"])}</em></span></a></li>' for i, s in enumerate(START_HERE) if s in POST)
    afr = "".join(card(page, L, p) for p in [p for p in posts if p["category"] == "africa"][:3])
    h += f"""
<section class="home-hero"><div class="wrap hero-grid">
  <div class="hero-copy">
    <span class="eyebrow">{c['eyebrow']}</span>
    <h1>{c['h1a']} <span>{c['h1b']}</span></h1>
    <p class="lead">{c['lead']}</p>
    <div class="cta-row"><a class="btn btn-primary" href="{page.rel(path_of(L,'blog'))}">{c['cta1']} {ICON['arrow']}</a><a class="btn btn-ghost" href="{page.rel(path_of(L,'programs'))}">{c['cta2']}</a></div>
  </div>
  <div class="hero-feature">
    <a class="feature-main" href="{page.rel(path_of(L,'post',feat['slug']))}"><img src="{page.rel(cover_rel(feat['slug']))}" alt="" width="1200" height="630" fetchpriority="high"><span class="fm-body"><em class="pill pill-{feat['category']}">{t['featured']}</em><strong>{E(feat[L]['title'])}</strong></span></a>
    <div class="minis">{side_html}</div>
  </div>
</div></section>
<section class="home-stats"><div class="wrap"><h2 class="sec-label">{c['numbers_title']}</h2><div class="hstats">{stats}</div></div></section>
{XP.tools_section(sys.modules[__name__], page, L)}
<section class="sec sec-alt"><div class="wrap"><div class="sec-head"><h2>{t['latest']}</h2><a class="more" href="{page.rel(path_of(L,'blog'))}">{t['see_all']} {ICON['arrow']}</a></div><div class="grid grid-3">{latest}</div></div></section>
<section class="sec"><div class="wrap"><div class="sec-head"><h2>{t['browse_topics']}</h2></div><div class="tiles">{tiles}</div></div></section>
<section class="sec"><div class="wrap start-grid"><div><h2>{t['start_here']}</h2><p class="lead">{t['start_here_sub']}</p></div><ol class="start-list">{start}</ol></div></section>
<section class="sec sec-dark"><div class="wrap"><div class="sec-head"><div><h2>{t['africa_title']}</h2><p>{t['africa_sub']}</p></div><a class="more" href="{page.rel(path_of(L,'cat','africa'))}">{CAT[L]['africa']} {ICON['arrow']}</a></div><div class="grid grid-3">{afr}</div></div></section>
<section class="sec"><div class="wrap prog-teaser">
  <div><span class="eyebrow">{t['programs']}</span><h2>{c['prog_title']}</h2><p class="lead">{c['prog_text']}</p><a class="btn btn-primary" href="{page.rel(path_of(L,'programs'))}">{c['prog_cta']} {ICON['arrow']}</a></div>
  <div class="prog-cards"><div class="pc"><span class="pc-ic">01</span><h3>{c['prog_edu']}</h3><p>{c['prog_edu_t']}</p></div><div class="pc"><span class="pc-ic">02</span><h3>{c['prog_inc']}</h3><p>{c['prog_inc_t']}</p></div></div>
</div></section>"""
    h += footer(page, L)
    write(path, h)


# ---------------------------------------------------------------- programs / contact
def build_programs(L):
    t = T[L]; c = PROGRAMS[L]; path = path_of(L, "programs"); page = Page(path)
    alt = {l: path_of(l, "programs") for l in LANGS}
    lds = [crumbs_ld([(t["home"], path_of(L, "home")), (t["programs"], path)])]
    h = head(page, L, c["title"], c["desc"], path, alt, og_rel("tunisia-incubators-accelerators", L), ld=lds)
    h += header(page, L, "programs", alt)
    courses = "".join(f'<div class="pc"><span class="pc-ic">{i+1:02d}</span><h3>{E(a)}</h3><p>{E(b)}</p></div>' for i, (a, b) in enumerate(c["courses"]))
    facts = "".join(f'<div class="fact"><strong>{E(a)}</strong><span>{E(b)}</span></div>' for a, b in c["facts"])
    inits = "".join(f'<div class="pc"><h3>{E(a)}</h3><p>{E(b)}</p></div>' for a, b in c["inits"])
    steps = "".join(f'<li><span class="num">{i+1}</span><strong>{E(a)}</strong><p>{E(b)}</p></li>' for i, (a, b) in enumerate(c["steps"]))
    reads = "".join(card(page, L, POST[s]) for s in ["bct-regulatory-sandbox", "how-to-raise-funding-tunisian-fintech", "tunisia-incubators-accelerators"] if s in POST)
    h += f"""
<section class="page-head"><div class="wrap">
  {crumbs_html(page, [(t['home'], path_of(L,'home')), (t['programs'], path)])}
  <span class="eyebrow">{c['eyebrow']}</span><h1>{E(c['h1'])}</h1><p class="lead">{E(c['lead'])}</p>
  <div class="cta-row"><a class="btn btn-ghost" href="#education">{E(c['edu_h'])}</a><a class="btn btn-ghost" href="#incubation">{E(c['inc_h'])}</a></div>
</div></section>
<section class="sec" id="education"><div class="wrap"><h2>{E(c['edu_h'])}</h2><p class="lead">{E(c['edu_p'])}</p><div class="grid grid-4">{courses}</div>
  <div class="split"><div><h3>{E(c['how_h'])}</h3><p>{E(c['how_p'])}</p></div><div class="facts">{facts}</div></div></div></section>
<section class="sec sec-alt" id="incubation"><div class="wrap"><h2>{E(c['inc_h'])}</h2><p class="lead">{E(c['inc_p'])}</p><div class="grid grid-3">{inits}</div>
  <h3 class="mt">{E(c['steps_h'])}</h3><ol class="steps">{steps}</ol><p class="focus">{E(c['focus'])}</p></div></section>
<section class="sec"><div class="wrap cta-box"><div><h2>{E(c['cta_h'])}</h2><p>{E(c['cta_p'])}</p></div><a class="btn btn-primary" href="{page.rel(path_of(L,'contact'))}">{E(c['cta'])} {ICON['arrow']}</a></div></section>
<section class="related"><div class="wrap"><h2>{E(c['read_h'])}</h2><div class="grid grid-3">{reads}</div></div></section>"""
    h += footer(page, L)
    write(path, h)


def build_contact(L):
    t = T[L]; c = CONTACT[L]; path = path_of(L, "contact"); page = Page(path)
    alt = {l: path_of(l, "contact") for l in LANGS}
    lds = [{"@context": "https://schema.org", "@type": "ContactPage", "name": c["h1"], "url": absu(path), "inLanguage": L, "about": {"@id": f"{SITE}/#org"}},
           crumbs_ld([(t["home"], path_of(L, "home")), (t["contact"], path)])]
    h = head(page, L, c["title"], c["desc"], path, alt, og_rel("tunisia-fintech-ecosystem-map", L), ld=lds)
    h += header(page, L, "contact", alt)
    opts = "".join(f'<option value="{E(v)}">{E(lbl)}</option>' for v, lbl in c["subjects"])
    h += f"""
<section class="page-head"><div class="wrap">
  {crumbs_html(page, [(t['home'], path_of(L,'home')), (t['contact'], path)])}
  <span class="eyebrow">{c['eyebrow']}</span><h1>{E(c['h1'])}</h1><p class="lead">{E(c['lead'])}</p>
</div></section>
<section class="sec"><div class="wrap contact-grid">
  <div class="contact-card">
    <h2>{c['details']}</h2>
    <dl><dt>{c['address']}</dt><dd>{c['address_v']}</dd><dt>{c['email']}</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd><dt>{c['hours']}</dt><dd>{c['hours_v']}</dd></dl>
    <div class="social"><a href="{LINKEDIN}" target="_blank" rel="noopener" aria-label="LinkedIn">{ICON['linkedin']}</a><a href="{FACEBOOK}" target="_blank" rel="noopener" aria-label="Facebook">{ICON['facebook']}</a></div>
  </div>
  <form class="contact-form" id="contact-form" action="{FORMSPREE}" method="POST" data-err="{E(c['err'])}">
    <input type="hidden" name="_subject" value="New contact form message ({L.upper()}) — Fintech Tunisia">
    <input type="text" name="_gotcha" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
    <div class="row2">
      <div class="field"><label for="cf-name">{c['name']}</label><input id="cf-name" type="text" name="name" placeholder="{c['name_ph']}" required autocomplete="name"></div>
      <div class="field"><label for="cf-email">{c['email']}</label><input id="cf-email" type="email" name="email" placeholder="{c['mail_ph']}" required autocomplete="email"></div>
    </div>
    <div class="field"><label for="cf-subject">{c['subject']}</label><select id="cf-subject" name="subject" required><option value="" disabled selected>{c['choose']}</option>{opts}</select></div>
    <div class="field"><label for="cf-message">{c['message']}</label><textarea id="cf-message" name="message" rows="6" placeholder="{c['msg_ph']}" required></textarea></div>
    <div class="field"><label for="cf-captcha">{c['verify']} <span id="captcha-q">3 + 4</span> ?</label><input id="cf-captcha" type="text" inputmode="numeric" autocomplete="off" placeholder="{c['verify_ph']}" required></div>
    <p class="form-err" id="captcha-error" hidden>{c['verify_err']}</p>
    <button type="submit" class="btn btn-primary btn-block">{c['send']}</button>
    <p class="form-ok" role="status">{c['ok']}</p>
  </form>
</div></section>"""
    h += footer(page, L)
    write(path, h)


# ---------------------------------------------------------------- misc
def build_404():
    page = Page("404.html"); L = "en"; t = T[L]
    h = head(page, L, f"{t['not_found']} | {SITE_NAME}", t["not_found_text"], "404.html", {}, og_rel("tunisia-fintech-ecosystem-map"), noindex=True)
    if MODE == "live":  # 404 is served at any depth on GitHub Pages: use absolute paths
        h = h.replace('href="assets/', 'href="/assets/').replace('src="assets/', 'src="/assets/')
    h += header(page, L, "", {l: path_of(l, "home") for l in LANGS})
    h += f"""<section class="page-head"><div class="wrap"><h1>{t['not_found']}</h1><p class="lead">{t['not_found_text']}</p>
<div class="cta-row"><a class="btn btn-primary" href="{page.rel(path_of('en','blog'))}">{t['all_articles']}</a><a class="btn btn-ghost" href="{page.rel(path_of('fr','blog'))}">{T['fr']['all_articles']}</a></div></div></section>"""
    h += footer(page, L)
    if MODE == "live":
        h = re.sub(r'(href|src)="(?!https?:|/|#|mailto:)([^"]*)"', lambda m: f'{m.group(1)}="/{m.group(2)}"', h)
    write("404.html", h)


def redirect(old, new):
    page = Page(old); target = page.rel(new)
    write(old, f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Moved</title><link rel="canonical" href="{absu(new)}"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={target}"><script>location.replace("{target}"+location.hash)</script></head><body><p>This page has moved: <a href="{target}">{absu(new)}</a></p></body></html>')


def build_sitemap():
    urls = []
    def add(kind, key=None, lastmod=BUILD_DATE, prio="0.6", img=None):
        alts = {l: path_of(l, kind, key) for l in LANGS}
        for l in LANGS:
            x = f"<url><loc>{absu(alts[l])}</loc><lastmod>{lastmod}</lastmod><priority>{prio}</priority>"
            x += "".join(f'<xhtml:link rel="alternate" hreflang="{k}" href="{absu(v)}"/>' for k, v in alts.items())
            x += f'<xhtml:link rel="alternate" hreflang="x-default" href="{absu(alts["en"])}"/>'
            if img: x += f"<image:image><image:loc>{SITE}/{og_rel(img, l)}</image:loc></image:image>"
            urls.append(x + "</url>")
    add("home", prio="1.0"); add("blog", prio="0.9")
    for c in CATS: add("cat", c, prio="0.7")
    add("programs", prio="0.6"); add("contact", prio="0.4")
    add("about", prio="0.5"); add("editorial", prio="0.4"); add("corrections", prio="0.3")
    add("directory", prio="0.9"); add("tracker", lastmod=XP.TRACKER["updated"], prio="0.9")
    for c in XP.companies: add("company", c["slug"], c.get("last_verified", BUILD_DATE), "0.7")
    for p in posts: add("post", p["slug"], p["modified"], "0.8", p["slug"])
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + "\n".join(urls) + "\n</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")


def build_feed(L):
    items = ""
    for p in posts[:30]:
        a = p[L]; u = absu(path_of(L, "post", p["slug"]))
        d = datetime.datetime.fromisoformat(p["date"] + "T08:00:00").strftime("%a, %d %b %Y %H:%M:%S +0100")
        items += f"<item><title>{xesc(a['title'])}</title><link>{u}</link><guid isPermaLink=\"true\">{u}</guid><pubDate>{d}</pubDate><category>{xesc(CAT[L][p['category']])}</category><description>{xesc(a['excerpt'])}</description></item>"
    home = absu(path_of(L, "home"))
    write(path_of(L, "feed"), f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>{SITE_NAME} ({L.upper()})</title><link>{home}</link><description>{xesc(T[L]["tagline"])}</description><language>{L}</language><atom:link href="{SITE}/{path_of(L,"feed")}" rel="self" type="application/rss+xml"/>{items}</channel></rss>\n')


def build_assets():
    os.makedirs(os.path.join(OUT, "assets", "covers"), exist_ok=True)
    for name in ("site.css", "site.js", "favicon.svg", "logo.png", "rtl.css"):
        shutil.copy(os.path.join(HERE, "static", name), os.path.join(OUT, "assets", name))
    shutil.copytree(os.path.join(HERE, "static", "fonts"), os.path.join(OUT, "assets", "fonts"), dirs_exist_ok=True)
    for p in posts:
        svg = cover_svg(p["slug"], p["category"], p.get("cover_motif"), variant=p["variant"])
        open(os.path.join(OUT, "assets", "covers", p["slug"] + ".svg"), "w").write(svg)
    og_dir = os.path.join(HERE, "og")
    if os.path.isdir(og_dir):
        shutil.copytree(og_dir, os.path.join(OUT, "assets", "og"), dirs_exist_ok=True)


def main():
    if os.path.isdir(OUT):
        for n in os.listdir(OUT):
            if n in (".git",): continue
            fp = os.path.join(OUT, n)
            shutil.rmtree(fp) if os.path.isdir(fp) else os.remove(fp)
    os.makedirs(OUT, exist_ok=True)
    build_assets()
    for L in LANGS:
        build_home(L); build_blog(L); build_programs(L); build_contact(L); build_feed(L)
        for c in CATS: build_cat(L, c)
        for p in posts: build_post(p, L)
    XP.build_all(sys.modules[__name__])
    build_404(); build_sitemap()
    # old URLs -> new
    redirect("news.html", path_of("en", "blog"))
    for s in ["tunisia-zero-equity-deals-h1-2026", "tunisia-startups-h1-2026-funding", "bolt-withdraws-tunisia", "easybank-funding", "atb-temenos-core-banking"]:
        redirect(f"news/{s}.html", path_of("en", "post", s))
    if MODE == "live":
        write("CNAME", "fintechtunisia.com\n"); write(".nojekyll", "")
    print(f"built {len(posts)} posts x {len(LANGS)} langs -> {OUT} ({MODE})")


if __name__ == "__main__":
    main()
