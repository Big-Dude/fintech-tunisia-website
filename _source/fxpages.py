"""SEO exchange-rate pages: EUR/USD/GBP/CAD -> TND, in EN/FR/AR.
Indexed and listed in the sitemap, but deliberately NOT linked from the menu, home page or footer
(only from relevant articles, the comparator source line, and from each other)."""
import json, os, html, math

E = html.escape
HERE = os.path.dirname(os.path.abspath(__file__))
HIST = json.load(open(os.path.join(HERE, "remit", "fx_history.json"), encoding="utf-8"))
DATES = sorted(HIST)
CURS = ["eur", "usd", "gbp", "cad"]

SLUG = {
    "en": {"eur": "euro-to-tunisian-dinar.html", "usd": "us-dollar-to-tunisian-dinar.html", "gbp": "british-pound-to-tunisian-dinar.html", "cad": "canadian-dollar-to-tunisian-dinar.html"},
    "fr": {"eur": "taux-euro-dinar-tunisien.html", "usd": "taux-dollar-dinar-tunisien.html", "gbp": "taux-livre-sterling-dinar-tunisien.html", "cad": "taux-dollar-canadien-dinar-tunisien.html"},
    "ar": {"eur": "euro-to-tunisian-dinar.html", "usd": "us-dollar-to-tunisian-dinar.html", "gbp": "british-pound-to-tunisian-dinar.html", "cad": "canadian-dollar-to-tunisian-dinar.html"},
}
CODE = {"eur": "EUR", "usd": "USD", "gbp": "GBP", "cad": "CAD"}
NAME = {
    "en": {"eur": "euro", "usd": "US dollar", "gbp": "British pound", "cad": "Canadian dollar"},
    "fr": {"eur": "euro", "usd": "dollar américain", "gbp": "livre sterling", "cad": "dollar canadien"},
    "ar": {"eur": "اليورو", "usd": "الدولار الأمريكي", "gbp": "الجنيه الإسترليني", "cad": "الدولار الكندي"},
}
NAMEC = {  # capitalised / title forms
    "en": {"eur": "Euro", "usd": "US Dollar", "gbp": "British Pound", "cad": "Canadian Dollar"},
    "fr": {"eur": "euro", "usd": "dollar", "gbp": "livre sterling", "cad": "dollar canadien"},
    "ar": NAME["ar"],
}
AMOUNTS = {"eur": [1, 10, 50, 100, 200, 500, 1000, 5000], "usd": [1, 10, 50, 100, 200, 500, 1000, 5000],
           "gbp": [1, 10, 50, 100, 200, 500, 1000, 5000], "cad": [1, 10, 50, 100, 200, 500, 1000, 5000]}
TND_AMOUNTS = [1, 10, 50, 100, 500, 1000, 5000, 10000]

T = {
    "en": {
        "title": "{C} to Tunisian Dinar ({X}/TND) Exchange Rate Today",
        "desc": "{C} to Tunisian dinar rate today: 1 {X} = {r} TND ({d}). Converter, 90-day chart, high/low and conversion tables, updated daily.",
        "h1": "{C} to Tunisian dinar ({X}/TND) today",
        "lead": "Today's mid-market {n} to Tunisian dinar rate, a converter, the last 90 days and ready-made conversion tables. Updated every day.",
        "rate_lbl": "Mid-market rate", "inv": "1 TND = {v} {X}", "d1": "vs previous day", "d30": "over 30 days",
        "conv": "Converter", "hist": "Last 90 days", "hi": "30-day high", "lo": "30-day low", "avg": "30-day average",
        "table1": "{X} to TND conversion table", "table2": "TND to {X} conversion table", "date": "Date", "rate": "Rate",
        "recent": "Daily rates, last 10 days", "about_h": "About this rate",
        "about": ["This is the mid-market reference rate (the midpoint between buy and sell prices on international markets), from an open dataset updated daily. It is a reference, not a quote: banks, exchange offices and transfer services in Tunisia and abroad apply their own rates and fees.",
                  "The Central Bank of Tunisia publishes its own figure, the average of the previous day's interbank trades, which can differ slightly. The Tunisian dinar is not freely convertible and can't be bought outside Tunisia; read our [guide to the euro–dinar rate](ART) for the rules."],
        "send": "Sending money to Tunisia? The rate you get depends on the provider. [Compare transfer costs](REMIT) to see how many dinars actually arrive.",
        "faq": "Frequently asked questions", "others": "Other rates to the Tunisian dinar", "src": "Source: mid-market rates from the open fawazahmed0/currency-api dataset. Last update",
        "q1": "How much is 1 {n} in Tunisian dinars today?", "a1": "On {d}, 1 {X} was worth {r} TND at the mid-market rate. Banks and exchange offices apply their own buy and sell rates, so the amount you get will be slightly lower.",
        "q2": "How much is 100 {X} in Tunisian dinars?", "a2": "At {d}'s mid-market rate, 100 {X} = {r100} TND. Check the conversion table above for other amounts.",
        "q3": "Has the {n} gone up or down against the dinar?", "a3": "Over the last 30 days the rate moved {chg} (from {r30} to {r} TND). The 30-day range was {lo} to {hi} TND.",
        "q4": "Why is my bank's rate different?", "a4": "This page shows the mid-market reference. Banks, exchange offices and transfer services add a margin and sometimes a fee. For transfers, compare the total amount received rather than the headline rate.",
        "up": "up {p}", "down": "down {p}", "flat": "almost unchanged",
    },
    "fr": {
        "title": "Taux {c} dinar tunisien aujourd'hui ({X}/TND)",
        "desc": "Taux {c} dinar tunisien aujourd'hui : 1 {X} = {r} TND ({d}). Convertisseur, courbe sur 90 jours, plus haut/plus bas et tableaux de conversion.",
        "h1": "Taux {c} / dinar tunisien ({X}/TND) aujourd'hui",
        "lead": "Le taux moyen du marché {n} – dinar tunisien du jour, un convertisseur, les 90 derniers jours et des tableaux de conversion. Mis à jour chaque jour.",
        "rate_lbl": "Taux moyen du marché", "inv": "1 TND = {v} {X}", "d1": "par rapport à la veille", "d30": "sur 30 jours",
        "conv": "Convertisseur", "hist": "90 derniers jours", "hi": "Plus haut 30 j", "lo": "Plus bas 30 j", "avg": "Moyenne 30 j",
        "table1": "Tableau de conversion {X} en dinars", "table2": "Tableau de conversion dinars en {X}", "date": "Date", "rate": "Taux",
        "recent": "Taux des 10 derniers jours", "about_h": "À propos de ce taux",
        "about": ["Il s'agit du taux moyen du marché (le point médian entre les prix d'achat et de vente sur les marchés internationaux), issu d'un jeu de données ouvert actualisé chaque jour. C'est une référence, pas une cotation : banques, bureaux de change et services de transfert appliquent leurs propres taux et frais.",
                  "La Banque centrale de Tunisie publie son propre chiffre, la moyenne des transactions interbancaires de la veille, qui peut légèrement différer. Le dinar n'est pas librement convertible et ne s'achète pas hors de Tunisie : consultez notre [guide du taux euro–dinar](ART) pour les règles."],
        "send": "Vous envoyez de l'argent en Tunisie ? Le taux obtenu dépend du prestataire. [Comparez le coût des transferts](REMIT) pour voir combien de dinars arrivent vraiment.",
        "faq": "Questions fréquentes", "others": "Autres taux face au dinar tunisien", "src": "Source : taux moyens du marché, jeu de données ouvert fawazahmed0/currency-api. Dernière mise à jour",
        "q1": "Combien vaut 1 {n} en dinars tunisiens aujourd'hui ?", "a1": "Le {d}, 1 {X} valait {r} TND au taux moyen du marché. Les banques et bureaux de change appliquent leurs propres cours d'achat et de vente : le montant obtenu sera légèrement inférieur.",
        "q2": "Combien font 100 {X} en dinars tunisiens ?", "a2": "Au taux moyen du {d}, 100 {X} = {r100} TND. Le tableau de conversion ci-dessus donne d'autres montants.",
        "q3": "Le {n} a-t-il monté ou baissé face au dinar ?", "a3": "Sur les 30 derniers jours, le taux est {chg} (de {r30} à {r} TND). La fourchette sur 30 jours va de {lo} à {hi} TND.",
        "q4": "Pourquoi le taux de ma banque est-il différent ?", "a4": "Cette page affiche le taux de référence du marché. Banques, bureaux de change et services de transfert ajoutent une marge et parfois des frais. Pour un transfert, comparez le montant total reçu plutôt que le taux affiché.",
        "up": "en hausse de {p}", "down": "en baisse de {p}", "flat": "quasi stable",
    },
    "ar": {
        "title": "سعر {n} مقابل الدينار التونسي اليوم ({X}/TND)",
        "desc": "سعر {n} مقابل الدينار التونسي اليوم: 1 {X} = {r} دينار ({d}). محوّل عملات، ومنحنى 90 يومًا، وأعلى وأدنى سعر، وجداول تحويل.",
        "h1": "سعر {n} مقابل الدينار التونسي اليوم ({X}/TND)",
        "lead": "السعر المتوسط في السوق لـ{n} مقابل الدينار التونسي اليوم، مع محوّل عملات، وآخر 90 يومًا، وجداول تحويل جاهزة. يُحدَّث يوميًا.",
        "rate_lbl": "السعر المتوسط في السوق", "inv": "1 TND = {v} {X}", "d1": "مقارنة بالأمس", "d30": "خلال 30 يومًا",
        "conv": "محوّل العملات", "hist": "آخر 90 يومًا", "hi": "أعلى سعر (30 يومًا)", "lo": "أدنى سعر (30 يومًا)", "avg": "المتوسط (30 يومًا)",
        "table1": "جدول تحويل {X} إلى الدينار", "table2": "جدول تحويل الدينار إلى {X}", "date": "التاريخ", "rate": "السعر",
        "recent": "الأسعار اليومية لآخر 10 أيام", "about_h": "حول هذا السعر",
        "about": ["هذا هو السعر المتوسط في السوق (النقطة الوسطى بين سعري الشراء والبيع في الأسواق الدولية)، من مجموعة بيانات مفتوحة تُحدَّث يوميًا. وهو سعر مرجعي لا عرض أسعار: تطبّق البنوك ومكاتب الصرف وخدمات التحويل أسعارها ورسومها الخاصة.",
               "ينشر البنك المركزي التونسي رقمه الخاص، أي متوسط المعاملات بين البنوك في اليوم السابق، وقد يختلف قليلًا. والدينار التونسي غير قابل للتحويل الحر ولا يمكن شراؤه خارج تونس؛ اطّلع على [دليلنا حول سعر اليورو مقابل الدينار](ART) لمعرفة القواعد."],
        "send": "هل ترسل أموالًا إلى تونس؟ السعر الذي تحصل عليه يتوقف على المزوّد. [قارن تكلفة التحويل](REMIT) لترى عدد الدنانير التي تصل فعلًا.",
        "faq": "أسئلة شائعة", "others": "أسعار عملات أخرى مقابل الدينار التونسي", "src": "المصدر: أسعار السوق المتوسطة من مجموعة البيانات المفتوحة fawazahmed0/currency-api. آخر تحديث",
        "q1": "كم يساوي 1 {X} بالدينار التونسي اليوم؟", "a1": "في {d}، كان 1 {X} يساوي {r} دينار بالسعر المتوسط في السوق. تطبّق البنوك ومكاتب الصرف أسعار شراء وبيع خاصة بها، لذلك سيكون المبلغ الذي تحصل عليه أقل بقليل.",
        "q2": "كم تساوي 100 {X} بالدينار التونسي؟", "a2": "بالسعر المتوسط ليوم {d}، تساوي 100 {X} نحو {r100} دينار. يتضمن جدول التحويل أعلاه مبالغ أخرى.",
        "q3": "هل ارتفع {n} أم انخفض مقابل الدينار؟", "a3": "خلال آخر 30 يومًا كان السعر {chg} (من {r30} إلى {r} دينار). وتراوح خلال 30 يومًا بين {lo} و{hi} دينار.",
        "q4": "لماذا يختلف سعر بنكي؟", "a4": "تعرض هذه الصفحة السعر المرجعي للسوق. تضيف البنوك ومكاتب الصرف وخدمات التحويل هامشًا وأحيانًا رسومًا. عند التحويل، قارن المبلغ الإجمالي الواصل لا السعر المعلن.",
        "up": "مرتفعًا بنسبة {p}", "down": "منخفضًا بنسبة {p}", "flat": "شبه مستقر",
    },
}


def fmt(v, L, dec=4):
    s = f"{v:,.{dec}f}"
    if L == "en": return s
    return s.replace(",", " ").replace(".", ",")


def pct(v, L):
    s = f"{abs(v):.2f}".replace(".", "," if L != "en" else ".")
    return s + (" %" if L == "fr" else "%")


def series(cur, n=None):
    ds = DATES[-n:] if n else DATES
    return [(d, HIST[d][cur]) for d in ds]


def chart_svg(cur, L):
    pts = series(cur, 90)
    W, H, P = 720, 220, 34
    vals = [v for _, v in pts]; lo, hi = min(vals), max(vals)
    pad = (hi - lo) * 0.15 or 0.01; lo -= pad; hi += pad
    x = lambda i: P + i * (W - 2 * P) / (len(pts) - 1)
    y = lambda v: H - P - (v - lo) / (hi - lo) * (H - 2 * P)
    line = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, (_, v) in enumerate(pts))
    area = f"M{x(0):.1f},{H-P} L" + line.replace(" ", " L") + f" L{x(len(pts)-1):.1f},{H-P} Z"
    grid = ""
    for k in range(4):
        gv = lo + (hi - lo) * k / 3
        grid += f'<line x1="{P}" x2="{W-P}" y1="{y(gv):.1f}" y2="{y(gv):.1f}" class="fx-grid"/><text x="{W-P+4}" y="{y(gv)+4:.1f}" class="fx-ax">{fmt(gv, L, 3)}</text>'
    ticks = ""
    for i in (0, len(pts) // 2, len(pts) - 1):
        d = pts[i][0]
        ticks += f'<text x="{x(i):.1f}" y="{H-10}" class="fx-ax" text-anchor="{"start" if i == 0 else "end" if i == len(pts)-1 else "middle"}">{d[8:]}/{d[5:7]}</text>'
    lx, ly = x(len(pts) - 1), y(pts[-1][1])
    return (f'<svg viewBox="0 0 {W+20} {H}" class="fx-svg" role="img" aria-label="{CODE[cur]}/TND 90 days" direction="ltr">'
            f'<defs><linearGradient id="fxg-{cur}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e31e24" stop-opacity=".18"/><stop offset="1" stop-color="#e31e24" stop-opacity="0"/></linearGradient></defs>'
            f'{grid}<path d="{area}" fill="url(#fxg-{cur})"/><polyline points="{line}" fill="none" stroke="#e31e24" stroke-width="2.5" stroke-linejoin="round"/>'
            f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="4.5" fill="#e31e24" stroke="#fff" stroke-width="2"/>{ticks}</svg>')


def md_inline(B, page, L, text):
    import markdown, re
    text = text.replace("](ART)", "](" + page.rel(B.path_of(L, "post", "euro-tunisian-dinar-exchange-rate-explained")) + ")")
    text = text.replace("](REMIT)", "](" + page.rel(B.path_of(L, "remit")) + ")")
    return re.sub(r"^<p>|</p>$", "", markdown.markdown(text))


def build(B):
    for L in B.LANGS:
        for cur in CURS:
            _page(B, L, cur)


def _page(B, L, cur):
    t = T[L]; X = CODE[cur]; n = NAME[L][cur]; C = NAMEC[L][cur]
    path = B.path_of(L, "fx", cur); page = B.Page(path)
    alt = {l: B.path_of(l, "fx", cur) for l in B.LANGS}
    s30 = series(cur, 31); last_d, r = s30[-1]; prev = s30[-2][1]; r30 = s30[0][1]
    v30 = [v for _, v in s30[1:]]; hi30, lo30, avg30 = max(v30), min(v30), sum(v30) / len(v30)
    d_txt = B.fdate(last_d, L)
    ch1 = (r / prev - 1) * 100; ch30 = (r / r30 - 1) * 100
    chg = t["flat"] if abs(ch30) < 0.1 else (t["up"] if ch30 > 0 else t["down"]).format(p=pct(ch30, L))
    fill = dict(C=C, c=C, n=n, X=X, r=fmt(r, L), d=d_txt, r100=fmt(r * 100, L, 2), chg=chg, r30=fmt(r30, L), lo=fmt(lo30, L), hi=fmt(hi30, L))
    title = t["title"].format(**fill); desc = t["desc"].format(**fill)
    faq = [(t[f"q{i}"].format(**fill), t[f"a{i}"].format(**fill)) for i in (1, 2, 3, 4)]
    crumbs = [(B.T[L]["home"], B.path_of(L, "home")), (f"{X}/TND", path)]
    lds = [{"@context": "https://schema.org", "@type": "WebPage", "name": title, "description": desc, "url": B.absu(path), "inLanguage": L,
            "dateModified": B.iso(last_d), "publisher": {"@id": f"{B.SITE}/#org"}},
           B.crumbs_ld(crumbs),
           {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]
    h = B.head(page, L, f"{title} | {B.SITE_NAME}", desc, path, alt, B.og_rel("fx-" + cur, L), ld=lds)
    h += B.header(page, L, "", alt)
    arrow = lambda v: ("▲" if v > 0 else "▼" if v < 0 else "•")
    cls = lambda v: "up" if v > 0.005 else "down" if v < -0.005 else "flat"
    t1 = "".join(f"<tr><td>{fmt(a, L, 0)} {X}</td><td>{fmt(a * r, L, 2)} TND</td></tr>" for a in AMOUNTS[cur])
    t2 = "".join(f"<tr><td>{fmt(a, L, 0)} TND</td><td>{fmt(a / r, L, 2)} {X}</td></tr>" for a in TND_AMOUNTS)
    recent = "".join(f"<tr><td>{B.fdate(d, L)}</td><td>{fmt(v, L)}</td></tr>" for d, v in reversed(series(cur, 10)))
    others = "".join(f'<a class="chip" href="{page.rel(B.path_of(L, "fx", o))}">{CODE[o]} → TND</a>' for o in CURS if o != cur)
    faqs = "".join(f'<details class="faq-item"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faq)
    about = "".join(f"<p>{md_inline(B, page, L, p)}</p>" for p in t["about"])
    data = json.dumps({"cur": cur, "rate": r, "date": last_d, "L": L}).replace("</", "<\\/")
    h += f"""
<section class="page-head fx-head"><div class="wrap">
  {B.crumbs_html(page, crumbs)}
  <h1>{E(t['h1'].format(**fill))}</h1>
  <p class="lead">{E(t['lead'].format(**fill))}</p>
  <div class="fx-top">
    <div class="fx-rate">
      <span class="fx-lbl">{t['rate_lbl']}</span>
      <div class="fx-big"><bdi dir="ltr">1 {X} = <b id="fx-r">{fmt(r, L)}</b> TND</bdi></div>
      <div class="fx-sub"><span id="fx-inv"><bdi dir="ltr">{t['inv'].format(v=fmt(1 / r, L), X=X)}</bdi></span> · <time id="fx-d" datetime="{last_d}">{d_txt}</time></div>
      <div class="fx-chg"><span class="{cls(ch1)}">{arrow(ch1)} <bdi dir="ltr">{pct(ch1, L)}</bdi> {t['d1']}</span><span class="{cls(ch30)}">{arrow(ch30)} <bdi dir="ltr">{pct(ch30, L)}</bdi> {t['d30']}</span></div>
    </div>
    <form class="fx-conv" onsubmit="return false" aria-label="{t['conv']}">
      <span class="fx-lbl">{t['conv']}</span>
      <label class="fx-in"><input id="fx-a" type="number" inputmode="decimal" value="100" min="0" step="any"><span>{X}</span></label>
      <div class="fx-eq" aria-hidden="true">⇅</div>
      <label class="fx-in"><input id="fx-b" type="number" inputmode="decimal" value="{r*100:.2f}" min="0" step="any"><span>TND</span></label>
    </form>
  </div>
</div></section>
<section class="sec-tight"><div class="wrap">
  <div class="fx-grid2">
    <div class="fx-card"><h2>{t['hist']}</h2>{chart_svg(cur, L)}
      <div class="fx-stats"><div><span>{t['hi']}</span><b><bdi dir="ltr">{fmt(hi30, L)}</bdi></b></div><div><span>{t['lo']}</span><b><bdi dir="ltr">{fmt(lo30, L)}</bdi></b></div><div><span>{t['avg']}</span><b><bdi dir="ltr">{fmt(avg30, L)}</bdi></b></div></div>
    </div>
    <div class="fx-card"><h2>{t['recent']}</h2><div class="table-wrap"><table class="fx-t"><thead><tr><th>{t['date']}</th><th>{t['rate']}</th></tr></thead><tbody>{recent}</tbody></table></div></div>
  </div>
  {B.ad_slot(page, L, "fx-" + cur, "fx")}
  <div class="fx-grid2">
    <div class="fx-card"><h2>{E(t['table1'].format(X=X))}</h2><div class="table-wrap"><table class="fx-t"><tbody>{t1}</tbody></table></div></div>
    <div class="fx-card"><h2>{E(t['table2'].format(X=X))}</h2><div class="table-wrap"><table class="fx-t"><tbody>{t2}</tbody></table></div></div>
  </div>
  <div class="fx-about"><h2>{t['about_h']}</h2>{about}<p class="fx-send">{md_inline(B, page, L, t['send'])}</p></div>
  <section class="faq"><h2>{t['faq']}</h2>{faqs}</section>
  <div class="fx-others"><h2>{t['others']}</h2><div class="chips">{others}</div></div>
  <p class="remit-fine">{t['src']}: {d_txt}.</p>
</div></section>
<script type="application/json" id="fx-data">{data}</script>
<script src="{page.rel('assets/fx.js')}" defer></script>"""
    h += B.footer(page, L)
    B.write(path, h)
