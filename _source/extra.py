"""Directory, regulation tracker, About / Editorial / Corrections pages."""
import json, glob, os, re, html
from i18n_extra import *

E = html.escape
HERE = os.path.dirname(os.path.abspath(__file__))

companies = []
for f in sorted(glob.glob(os.path.join(HERE, "directory", "*.json"))):
    d = json.load(open(f, encoding="utf-8")); d["slug"] = os.path.basename(f)[:-5]
    arf = os.path.join(HERE, "directory_ar", d["slug"] + ".json")
    if os.path.exists(arf):
        a = json.load(open(arf, encoding="utf-8"))
        d["ar"] = a["ar"]; d["status_note_ar"] = a.get("status_note_ar")
        for i, l in enumerate(d.get("licences") or []):
            if i < len(a.get("licences_ar") or []): l["label_ar"] = a["licences_ar"][i]
        for i, p in enumerate(d.get("people") or []):
            if i < len(a.get("people_roles_ar") or []): p["role_ar"] = a["people_roles_ar"][i]
        for i, fr in enumerate(d.get("funding") or []):
            if i < len(a.get("funding_round_ar") or []) and a["funding_round_ar"][i]: fr["round_ar"] = a["funding_round_ar"][i]
    companies.append(d)
_status_order = {"active": 0, "acquired": 1, "unclear": 2, "inactive": 3}
companies.sort(key=lambda c: (_status_order.get(c["status"], 9), c["name"].lower()))
COMPANY = {c["slug"]: c for c in companies}
TRACKER = json.load(open(os.path.join(HERE, "regulation", "tracker.json"), encoding="utf-8"))
REG = TRACKER["entries"]
_ar_path = os.path.join(HERE, "regulation", "tracker_ar.json")
if os.path.exists(_ar_path):
    _AR = json.load(open(_ar_path, encoding="utf-8"))
    for _e in REG:
        a = _AR.get(_e["id"])
        if a:
            _e["title_ar"] = a["title"]; _e["summary_ar"] = a["summary"]; _e["status_note_ar"] = a.get("status_note")
            _e["reference_ar"] = a.get("reference"); _e["in_force_ar"] = a.get("in_force")
REG_ID = {e["id"]: e for e in REG}

DIR_COLORS = {"payments": "#e31e24", "wallet": "#c2185b", "gateway": "#d84315", "infrastructure": "#24335c",
              "lending": "#1d5a3a", "insurtech": "#0f5268", "regtech": "#5d4037", "crowdfunding": "#6a2bb0",
              "b2b-finance": "#455a64", "remittance": "#b04a17", "banking-tech": "#2a2a2e", "crypto": "#8a6a10"}


def colon(L): return "\u00a0:" if L == "fr" else ":"


FR_REF = [(r"^Circular note No\.", "Note circulaire n°"), (r"^Circular No\.", "Circulaire n°"), (r"^Note No\.", "Note n°"),
          (r"^Decree-law No\.", "Décret-loi n°"), (r"^Government Decree No\.", "Décret gouvernemental n°"), (r"^Decree No\.", "Décret n°"),
          (r"^Organic Law No\.", "Loi organique n°"), (r"^Law No\.", "Loi n°"), (r"\bof (\d{1,2}) (January|February|March|April|May|June|July|August|September|October|November|December) (\d{4})", None)]
_MFR = dict(zip(["January","February","March","April","May","June","July","August","September","October","November","December"],
                ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]))


def ref(e, L):
    r = e["reference"]
    if L == "ar": return e.get("reference_ar") or r
    if L == "en": return r
    if e.get("reference_fr"): return e["reference_fr"]
    for pat, sub in FR_REF:
        if sub: r = re.sub(pat, sub, r)
        else: r = re.sub(pat, lambda m: f"du {m.group(1)} {_MFR[m.group(2)]} {m.group(3)}", r)
    return r


def companies_for_article(slug):
    return [c for c in companies if slug in (c.get("related_articles") or [])]


def monogram(c, size=64):
    words = re.sub(r"[^A-Za-z0-9 ]", " ", c["name"]).split()
    ini = (words[0][0] + (words[1][0] if len(words) > 1 else words[0][1] if len(words[0]) > 1 else "")).upper() if words else "?"
    col = DIR_COLORS.get(c["category"], "#24335c")
    return (f'<svg class="mono" viewBox="0 0 64 64" width="{size}" height="{size}" aria-hidden="true">'
            f'<rect width="64" height="64" rx="16" fill="{col}"/>'
            f'<text x="32" y="41" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-weight="800" font-size="24" fill="#fff">{E(ini)}</text></svg>')


def md_links(B, page, L, text):
    links = {"DIR": B.path_of(L, "directory"), "REG": B.path_of(L, "tracker"), "PROG": B.path_of(L, "programs"),
             "EDIT": B.path_of(L, "editorial"), "CORR": B.path_of(L, "corrections"), "CONTACT": B.path_of(L, "contact"), "REMIT": B.path_of(L, "remit")}
    for k, v in links.items(): text = text.replace(f"]({k})", f"]({page.rel(v)})")
    return text


# ------------------------------------------------------------ static info pages
def info_page(B, L, kind, data, og_slug, extra_html=""):
    t = B.T[L]; path = B.path_of(L, kind); page = B.Page(path)
    alt = {l: B.path_of(l, kind) for l in B.LANGS}
    crumbs = [(t["home"], B.path_of(L, "home")), (data["h1"], path)]
    typ = {"about": "AboutPage", "editorial": "WebPage", "corrections": "WebPage"}[kind]
    lds = [{"@context": "https://schema.org", "@type": typ, "name": data["h1"], "url": B.absu(path), "inLanguage": L,
            "about": {"@id": f"{B.SITE}/#org"}, "dateModified": B.iso(B.BUILD_DATE)}, B.crumbs_ld(crumbs)]
    if kind == "about": lds.append(dict(B.org_ld(), **{"@context": "https://schema.org"}))
    h = B.head(page, L, data["title"], data["desc"], path, alt, B.og_rel(og_slug, L), ld=lds)
    h += B.header(page, L, "about" if kind == "about" else "", alt)
    body = ""
    if data.get("md"):
        import markdown
        body = markdown.markdown(md_links(B, page, L, data["md"]), extensions=["sane_lists"])
    h += f"""
<section class="page-head"><div class="wrap narrow">
  {B.crumbs_html(page, crumbs)}
  <h1>{E(data['h1'])}</h1><p class="lead">{E(data['lead'])}</p>
  <p class="meta-line">{X[L]['updated']} <time datetime="{B.BUILD_DATE}">{B.fdate(B.BUILD_DATE, L)}</time></p>
</div></section>
<section class="sec-tight"><div class="wrap narrow"><div class="prose">{body}{extra_html}</div>
<nav class="info-nav">{''.join(f'<a href="{page.rel(B.path_of(L,k))}"{B.AC if k==kind else ""}>{lab}</a>' for k, lab in [("about", ABOUT[L]["h1"]), ("editorial", EDITORIAL[L]["h1"]), ("corrections", CORRECTIONS[L]["h1"])])}</nav>
</div></section>"""
    h += B.footer(page, L)
    B.write(path, h)


def build_corrections(B, L):
    import markdown
    c = CORRECTIONS[L]; page = B.Page(B.path_of(L, "corrections"))
    intro = markdown.markdown(md_links(B, page, L, c["intro"]))
    items = ""
    for date, slug, text in c["items"]:
        p = B.POST.get(slug)
        title = p[L]["title"] if p else slug
        items += f'<li><time datetime="{date}">{B.fdate(date, L)}</time><a href="{page.rel(B.path_of(L,"post",slug))}">{E(title)}</a><p>{E(text)}</p></li>'
    extra = f'{intro}<h2>{c["log"]}</h2><ol class="corr-log">{items}</ol>'
    info_page(B, L, "corrections", {**c, "md": ""}, "tunisia-fintech-ecosystem-map", extra)


# ------------------------------------------------------------ directory
def lic_html(c, L):
    if not c.get("licences"): return f'<p class="muted">{X[L]["no_licence"]}</p>'
    out = ""
    for l in c["licences"]:
        date = f' <span class="muted">· {E(l["date"])}</span>' if l.get("date") else ""
        src = f' <a class="src" href="{E(l["source_url"])}" target="_blank" rel="noopener nofollow">{X[L]["source"]}</a>' if l.get("source_url") else ""
        out += f'<li><span class="lic lic-{E(l["type"])}">{E(l.get("label_"+L) or l["type"])}</span>{date}{src}</li>'
    return f'<ul class="lic-list">{out}</ul>'


def fund_html(c, L):
    if not c.get("funding"): return f'<p class="muted">{X[L]["no_funding"]}</p>'
    rows = ""
    for f in c["funding"]:
        amt = E(f["amount"]) if f.get("amount") else f'<span class="muted">{X[L]["undisclosed"]}</span>'
        inv = E(", ".join(f.get("investors") or [])) or "—"
        src = f' <a class="src" href="{E(f["source_url"])}" target="_blank" rel="noopener nofollow">↗</a>' if f.get("source_url") else ""
        rows += f'<tr><td>{E(f.get("date") or "—")}</td><td>{E(f.get("round_" + L) or f.get("round") or "—")}</td><td>{amt}</td><td>{inv}{src}</td></tr>'
    return f'<div class="table-wrap"><table><thead><tr><th>{X[L]["date"]}</th><th>{X[L]["round"]}</th><th>{X[L]["amount"]}</th><th>{X[L]["investors"]}</th></tr></thead><tbody>{rows}</tbody></table></div>'


def company_card(B, page, L, c):
    a = c[L]; url = page.rel(B.path_of(L, "company", c["slug"]))
    lic = "".join(f'<span class="lic lic-{E(l["type"])}">{E(l.get("label_"+L) or l["type"])}</span>' for l in (c.get("licences") or [])[:2])
    search = " ".join([c["name"], " ".join(c.get("also_known_as") or []), a["tagline"], DIR_CAT[L].get(c["category"], ""), " ".join(a.get("products") or [])]).lower()
    return f"""<article class="co-card" data-cat="{E(c['category'])}" data-status="{E(c['status'])}" data-search="{E(search)}">
  <div class="co-top">{monogram(c, 48)}<div><h3><a href="{url}">{E(c['name'])}</a></h3><span class="co-cat">{E(DIR_CAT[L].get(c['category'], c['category']))}</span></div></div>
  <p>{E(a['tagline'])}</p>
  <div class="co-meta"><span class="st st-{E(c['status'])}">{DIR_STATUS[L][c['status']]}</span>{f'<span>{X[L]["founded"]} {c["founded"]}</span>' if c.get('founded') else ''}</div>
  {f'<div class="co-lic">{lic}</div>' if lic else ''}
</article>"""


def build_directory(B, L):
    t = B.T[L]; x = X[L]; path = B.path_of(L, "directory"); page = B.Page(path)
    alt = {l: B.path_of(l, "directory") for l in B.LANGS}
    crumbs = [(t["home"], B.path_of(L, "home")), (x["dir_crumb"], path)]
    lds = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": x["dir_h1"], "description": x["dir_desc"], "url": B.absu(path), "inLanguage": L,
            "mainEntity": {"@type": "ItemList", "numberOfItems": len(companies), "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "url": B.absu(B.path_of(L, "company", c["slug"])), "name": c["name"]} for i, c in enumerate(companies)]}},
           B.crumbs_ld(crumbs)]
    h = B.head(page, L, f"{x['dir_title']} | {B.SITE_NAME}", x["dir_desc"], path, alt, B.og_rel("directory", L), ld=lds)
    h += B.header(page, L, "directory", alt)
    cats = [k for k in DIR_CAT[L] if any(c["category"] == k for c in companies)]
    chips = f'<button class="chip active" data-filter="all">{x["all"]} <b>{len(companies)}</b></button>' + "".join(
        f'<button class="chip" data-filter="{k}">{DIR_CAT[L][k]} <b>{sum(1 for c in companies if c["category"]==k)}</b></button>' for k in cats)
    grid = "".join(company_card(B, page, L, c) for c in companies)
    h += f"""
<section class="page-head"><div class="wrap">
  {B.crumbs_html(page, crumbs)}
  <h1>{E(x['dir_h1'])}</h1><p class="lead">{E(x['dir_lead'])}</p>
  <div class="tools"><label class="search">{B.ICON['search']}<span class="sr">{x['dir_search']}</span><input type="search" id="co-search" placeholder="{x['dir_search']}" autocomplete="off"></label></div>
  <div class="chips" id="co-filters" role="group" aria-label="{x['category']}">{chips}</div>
</div></section>
<section class="listing"><div class="wrap">
  <div class="co-grid" id="co-grid">{grid}</div>
  <p class="no-results" hidden>{t['no_results']}</p>
  <p class="dir-note">{x['dir_note']} <a href="{page.rel(B.path_of(L,'editorial'))}">{EDITORIAL[L]['h1']}</a> · <a href="{page.rel(B.path_of(L,'contact'))}">{x['fix_link']}</a></p>
</div></section>"""
    h += B.footer(page, L)
    B.write(path, h)


def build_company(B, L, c):
    t = B.T[L]; x = X[L]; a = c[L]; slug = c["slug"]
    path = B.path_of(L, "company", slug); page = B.Page(path)
    alt = {l: B.path_of(l, "company", slug) for l in B.LANGS}
    crumbs = [(t["home"], B.path_of(L, "home")), (x["dir_crumb"], B.path_of(L, "directory")), (c["name"], path)]
    org = {"@context": "https://schema.org", "@type": "Organization", "name": c["name"], "description": a["tagline"],
           "url": c.get("website") or B.absu(path)}
    if c.get("also_known_as"): org["alternateName"] = c["also_known_as"]
    if c.get("founded"): org["foundingDate"] = str(c["founded"])
    if c.get("hq"): org["address"] = {"@type": "PostalAddress", "addressLocality": c["hq"], "addressCountry": "TN"}
    if c.get("website"): org["sameAs"] = [c["website"]]
    if c.get("people"): org["founder"] = [{"@type": "Person", "name": p["name"]} for p in c["people"] if "found" in p["role"].lower()] or None
    org = {k: v for k, v in org.items() if v}
    lds = [{"@context": "https://schema.org", "@type": "ProfilePage", "url": B.absu(path), "inLanguage": L, "dateModified": B.iso(c.get("last_verified", B.BUILD_DATE)), "mainEntity": org},
           B.crumbs_ld(crumbs)]
    title = f"{c['name']}: {a['tagline']}"
    if len(title) > 70: title = f"{c['name']} — " + {"en": "Tunisian fintech profile", "fr": "fiche fintech tunisienne", "ar": "بطاقة شركة فنتك تونسية"}[L]
    desc = a["description"].split(". ")[0][:150].rstrip(".") + "."
    if len(desc) < 90: desc = (a["tagline"] + ". " + desc)[:158]
    h = B.head(page, L, f"{title} | {B.SITE_NAME}", desc, path, alt, B.og_rel("directory", L), ld=lds)
    h += B.header(page, L, "directory", alt)
    facts = [(x["category"], E(DIR_CAT[L].get(c["category"], c["category"]))),
             (x["status"], f'<span class="st st-{E(c["status"])}">{DIR_STATUS[L][c["status"]]}</span>')]
    if c.get("founded"): facts.append((x["founded"], str(c["founded"])))
    HQ_AR = {"Tunis": "تونس العاصمة", "Sfax": "صفاقس", "Sousse": "سوسة", "Ariana": "أريانة", "Lac 2, Tunis": "البحيرة 2، تونس", "Paris (engineering in Tunis)": "باريس (فريق الهندسة في تونس)"}
    if c.get("hq"): facts.append((x["hq"], E(HQ_AR.get(c["hq"], c["hq"]) if L == "ar" else c["hq"])))
    if c.get("website"): facts.append((x["website"], f'<a href="{E(c["website"])}" target="_blank" rel="noopener nofollow">{E(re.sub(r"^https?://(www\.)?", "", c["website"]).rstrip("/"))}</a>'))
    facts_html = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in facts)
    sn = c.get("status_note_" + L) or c.get("status_note")
    status_note = f'<p class="status-note">{E(sn)}</p>' if sn and c["status"] != "active" else ""
    desc_html = "".join(f"<p>{E(p)}</p>" for p in a["description"].split("\n") if p.strip())
    prods = "".join(f"<li>{E(p)}</li>" for p in a.get("products") or [])
    people = "".join(f'<li><strong>{E(p["name"])}</strong> — {E(p.get("role_" + L) or p["role"])}</li>' for p in c.get("people") or [])
    rel = [B.POST[s] for s in (c.get("related_articles") or []) if s in B.POST][:3]
    rel_html = "".join(B.card(page, L, p) for p in rel)
    srcs = "".join(f'<li><a href="{E(s["url"])}" target="_blank" rel="noopener nofollow">{E(s.get("title") or s["url"])}</a>{" — " + E(s["publisher"]) if s.get("publisher") else ""}</li>' for s in c.get("sources") or [])
    others = [o for o in companies if o["category"] == c["category"] and o["slug"] != slug][:3]
    others_html = "".join(company_card(B, page, L, o) for o in others)
    h += f"""
<section class="page-head co-head"><div class="wrap narrow">
  {B.crumbs_html(page, crumbs)}
  <div class="co-title">{monogram(c, 72)}<div><h1>{E(c['name'])}</h1><p class="lead">{E(a['tagline'])}</p></div></div>
  <dl class="co-facts">{facts_html}</dl>
  {status_note}
</div></section>
<section class="sec-tight"><div class="wrap narrow co-body">
  <h2>{x['about_co']}</h2><div class="prose">{desc_html}</div>
  {f'<h2>{x["products"]}</h2><ul class="prod-list">{prods}</ul>' if prods else ''}
  <h2>{x['licences']}</h2>{lic_html(c, L)}
  <h2>{x['funding']}</h2>{fund_html(c, L)}
  {f'<h2>{x["people"]}</h2><ul class="people">{people}</ul>' if people else ''}
  <section class="sources"><h2>{t['sources']}</h2><ol>{srcs}</ol></section>
  <p class="verify-line">{x['last_verified']}{colon(L)} <time datetime="{c.get('last_verified', B.BUILD_DATE)}">{B.fdate(c.get('last_verified', B.BUILD_DATE), L)}</time> · {x['fix']} <a href="{page.rel(B.path_of(L,'contact'))}">{x['fix_link']}</a></p>
</div></section>
{f'<section class="related"><div class="wrap"><h2>{x["in_articles"]}</h2><div class="grid grid-3">{rel_html}</div></div></section>' if rel_html else ''}
{f'<section class="sec"><div class="wrap"><h2>{DIR_CAT[L].get(c["category"], "")}</h2><div class="co-grid">{others_html}</div></div></section>' if others_html else ''}"""
    h += B.footer(page, L)
    B.write(path, h)


# ------------------------------------------------------------ tracker
def build_tracker(B, L):
    t = B.T[L]; x = X[L]; path = B.path_of(L, "tracker"); page = B.Page(path)
    alt = {l: B.path_of(l, "tracker") for l in B.LANGS}
    crumbs = [(t["home"], B.path_of(L, "home")), (x["reg_crumb"], path)]
    force_map = {"in_force": "https://schema.org/InForce", "repealed": "https://schema.org/NotInForce", "replaced": "https://schema.org/NotInForce"}
    items = []
    for i, e in enumerate(REG):
        if e["type"] in ("strategy", "other"): continue
        it = {"@type": "Legislation", "name": e["title_" + L], "legislationIdentifier": ref(e, L), "url": B.absu(path) + "#" + e["id"],
              "legislationJurisdiction": "TN"}
        if re.match(r"^\d{4}-\d{2}-\d{2}$", e.get("date") or ""): it["legislationDate"] = e["date"]
        if e["status"] in force_map: it["legislationLegalForce"] = force_map[e["status"]]
        items.append({"@type": "ListItem", "position": len(items) + 1, "item": it})
    lds = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": x["reg_h1"], "description": x["reg_desc"], "url": B.absu(path),
            "inLanguage": L, "dateModified": B.iso(TRACKER["updated"]), "mainEntity": {"@type": "ItemList", "itemListElement": items}},
           B.crumbs_ld(crumbs)]
    h = B.head(page, L, f"{x['reg_title']} | {B.SITE_NAME}", x["reg_desc"], path, alt, B.og_rel("regulation-tracker", L), ld=lds)
    h += B.header(page, L, "tracker", alt)
    groups = [("all", x["all"], len(REG)), ("force", REG_STATUS[L]["in_force"], sum(1 for e in REG if REG_GROUP[e["status"]] == "force")),
              ("pending", x["pending"], sum(1 for e in REG if REG_GROUP[e["status"]] == "pending")),
              ("unclear", REG_STATUS[L]["unclear"], sum(1 for e in REG if REG_GROUP[e["status"]] == "unclear")),
              ("past", x["past"], sum(1 for e in REG if REG_GROUP[e["status"]] == "past"))]
    chips = "".join(f'<button class="chip{" active" if k=="all" else ""}" data-filter="{k}">{lab} <b>{n}</b></button>' for k, lab, n in groups if n)
    topics = sorted({tp for e in REG for tp in e.get("topics", [])}, key=lambda k: REG_TOPIC[L].get(k, k))
    topic_opts = f'<option value="">{x["all_topics"]}</option>' + "".join(f'<option value="{tp}">{REG_TOPIC[L].get(tp, tp)}</option>' for tp in topics)
    rows = ""; year = None
    for e in REG:
        y = (e.get("date") or "")[:4]
        if y != year:
            rows += f'<li class="yr" data-year="{y}"><span>{y}</span></li>'; year = y
        d = e.get("date") or ""
        dshow = B.fdate(d, L) if re.match(r"^\d{4}-\d{2}-\d{2}$", d) else d
        rel = "".join(f'<a href="{page.rel(B.path_of(L,"post",s))}">{E(B.POST[s][L]["title"])}</a>' for s in (e.get("related_articles") or [])[:3] if s in B.POST)
        rep = REG_ID.get(e.get("replaces") or "")
        rep_html = f'<span>{x["replaces"]}{colon(L)} <a href="#{rep["id"]}">{E(ref(rep, L))}</a></span>' if rep else ""
        inforce = f'<span>{x["in_force_from"]}{colon(L)} {E(e.get("in_force_ar") or e["in_force"]) if L == "ar" else E(e["in_force"].replace("(approx.)", "(approx.)" if L == "en" else "(environ)"))}</span>' if e.get("in_force") and e["status"] != "in_force" else ""
        src = f'<a class="src" href="{E(e["source_url"])}" target="_blank" rel="noopener nofollow">{x["source"]}{colon(L)} {E(e.get("source_name") or "")}</a>' if e.get("source_url") else ""
        tps = "".join(f'<span class="tp">{REG_TOPIC[L].get(tp, tp)}</span>' for tp in e.get("topics", []))
        note = e.get("status_note_" + L)
        rows += f"""<li class="reg" id="{E(e['id'])}" data-group="{REG_GROUP[e['status']]}" data-topics="{' '.join(e.get('topics', []))}">
  <div class="reg-date"><time datetime="{E(d)}">{E(dshow)}</time></div>
  <div class="reg-card">
    <div class="reg-top"><span class="rs rs-{e['status']}">{REG_STATUS[L][e['status']]}</span><span class="reg-type">{REG_TYPE[L].get(e['type'], e['type'])} · {E(e['issuer'])}</span></div>
    <h3>{E(e['title_'+L])}</h3>
    <p class="reg-ref">{E(ref(e, L))}</p>
    <p>{E(e['summary_'+L])}</p>
    {f'<p class="reg-note">{E(note)}</p>' if note else ''}
    <div class="reg-meta">{inforce}{rep_html}</div>
    <div class="reg-tags">{tps}</div>
    {f'<div class="reg-rel"><span>{x["read"]}{colon(L)}</span>{rel}</div>' if rel else ''}
    {src}
  </div>
</li>"""
    pending_n = sum(1 for e in REG if REG_GROUP[e["status"]] == "pending")
    h += f"""
<section class="page-head"><div class="wrap">
  {B.crumbs_html(page, crumbs)}
  <h1>{E(x['reg_h1'])}</h1><p class="lead">{E(x['reg_lead'])}</p>
  <div class="reg-summary"><div><b>{len(REG)}</b><span>{x['texts']}</span></div><div><b>{groups[1][2]}</b><span>{REG_STATUS[L]['in_force']}</span></div><div><b>{pending_n}</b><span>{x['pending']}</span></div><div class="upd"><b>{B.fdate(TRACKER['updated'], L)}</b><span>{x['last_update']}</span></div></div>
  <div class="reg-tools"><div class="chips" id="reg-filters" role="group">{chips}</div><label class="sel"><span class="sr">{x['topics']}</span><select id="reg-topic">{topic_opts}</select></label></div>
</div></section>
<section class="listing"><div class="wrap narrow">
  <ol class="timeline" id="reg-list">{rows}</ol>
  <p class="no-results" hidden>{t['no_results']}</p>
  <p class="dir-note">{x['reg_note']}</p>
</div></section>"""
    h += B.footer(page, L)
    B.write(path, h)


# ------------------------------------------------------------ hooks used by build.py
def mentioned_box(B, page, L, slug):
    cs = companies_for_article(slug)
    if not cs: return ""
    items = "".join(f'<a class="co-chip" href="{page.rel(B.path_of(L,"company",c["slug"]))}">{monogram(c, 28)}<span>{E(c["name"])}</span></a>' for c in cs[:8])
    return f'<section class="mentioned"><h2>{X[L]["mentioned"]}</h2><div class="co-chips">{items}</div></section>'


def tools_section(B, page, L):
    x = X[L]
    n_pending = sum(1 for e in REG if REG_GROUP[e["status"]] == "pending")
    return f"""<section class="sec"><div class="wrap"><div class="sec-head"><div><h2>{x['tools']}</h2><p>{x['tools_sub']}</p></div></div>
<div class="tools-grid">
  <a class="tool" href="{page.rel(B.path_of(L,'directory'))}"><span class="tool-n">{len(companies)}</span><span class="tool-u">{x['companies']}</span><strong>{x['tool_dir']}</strong><p>{x['tool_dir_t']}</p><span class="more">{x['open']} {B.ICON['arrow']}</span></a>
  <a class="tool tool-red" href="{page.rel(B.path_of(L,'remit'))}"><span class="tool-n">{B.RM.FX['rate']:.2f}</span><span class="tool-u">EUR → TND · {B.RM.R[L]['rate_live']}</span><strong>{B.RM.R[L]['eyebrow']}</strong><p>{B.RM.R[L]['lead']}</p><span class="more">{x['open']} {B.ICON['arrow']}</span></a>
  <a class="tool tool-dark" href="{page.rel(B.path_of(L,'tracker'))}"><span class="tool-n">{len(REG)}</span><span class="tool-u">{x['texts']} · {n_pending} {x['pending'].lower()}</span><strong>{x['tool_reg']}</strong><p>{x['tool_reg_t']}</p><span class="more">{x['open']} {B.ICON['arrow']}</span></a>
</div></div></section>"""


def build_all(B):
    for L in B.LANGS:
        info_page(B, L, "about", ABOUT[L], "tunisia-fintech-ecosystem-map")
        info_page(B, L, "editorial", EDITORIAL[L], "tunisia-fintech-ecosystem-map")
        build_corrections(B, L)
        build_directory(B, L)
        for c in companies: build_company(B, L, c)
        build_tracker(B, L)
