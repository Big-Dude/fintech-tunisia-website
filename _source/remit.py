"""Remittance comparator: Europe -> Tunisia. Builds /send-money-to-tunisia (EN/FR/AR)."""
import json, os, re, html, glob

E = html.escape
HERE = os.path.dirname(os.path.abspath(__file__))
RD = os.path.join(HERE, "remit")
CORRIDORS = ["FR", "IT", "DE"]

# ------------------------------------------------------------------ data
_extra = json.load(open(os.path.join(RD, "providers_extra.json"), encoding="utf-8"))
_ref_path = os.path.join(RD, "referrals.json")
REFERRALS = json.load(open(_ref_path, encoding="utf-8")) if os.path.exists(_ref_path) else {}
FX = json.load(open(os.path.join(RD, "fx.json"), encoding="utf-8"))  # {"rate":..,"date":..}

DATA = {}
for cc in CORRIDORS:
    d = json.load(open(os.path.join(RD, cc + ".json"), encoding="utf-8"))
    DATA[cc] = d


def provider(cc, pid):
    p = dict(_extra.get(pid, {}))
    for k, v in (DATA[cc]["providers"].get(pid) or {}).items():
        if v not in (None, "", []): p[k] = v
    # fill regulator from another corridor if missing (same EU entity)
    if not p.get("regulator"):
        for oc in CORRIDORS:
            q = DATA[oc]["providers"].get(pid) or {}
            if q.get("regulator") and q.get("entity", "")[:20] == (p.get("entity") or "")[:20]:
                p["regulator"] = q["regulator"]; break
    return p


def channel(o):
    sm = o.get("send_method") or []
    for c in ("agent", "bank-branch", "post-office", "app", "online"):
        if c in sm: return c
    return sm[0] if sm else "online"


def link_for(cc, pid, p):
    r = REFERRALS.get(pid) or {}
    url = (r.get(cc) or r.get("default") or "").strip()
    if url: return url, True
    return p.get("website") or "", False


def offers(cc):
    """Merge credit/debit duplicates and pair the USD 200 / USD 500 survey rows of the same product."""
    rows = DATA[cc]["offers"]
    groups = {}
    for o in rows:
        key = (o["provider_id"], channel(o), tuple(sorted(o.get("payout") or [])), o.get("speed"))
        g = groups.setdefault(key, {"pid": o["provider_id"], "name": o["provider"], "ch": key[1], "payout": list(key[2]),
                                    "speed": o.get("speed"), "b": {}})
        basis = str(o.get("basis_usd") or "")
        cur = {"amt": o.get("send_amount"), "fee": o.get("fee"), "fx": o.get("fx_margin_pct"), "tot": o.get("total_cost_pct")}
        prev = g["b"].get(basis)
        if prev is None or (cur["tot"] is not None and (prev["tot"] is None or cur["tot"] < prev["tot"])):
            g["b"][basis] = cur
    out = []
    for g in groups.values():
        p = provider(cc, g["pid"])
        url, ref = link_for(cc, g["pid"], p)
        g.update({"url": url, "ref": ref, "reg": p.get("regulator"), "ent": p.get("entity")})
        out.append(g)
    return out


# ------------------------------------------------------------------ labels
LBL = {
    "en": {
        "ch": {"online": "Online", "app": "App", "agent": "Cash at an agent", "bank-branch": "At a bank branch", "post-office": "At a post office"},
        "po": {"bank-account": "Bank account", "cash-pickup": "Cash pickup", "mobile-wallet": "Mobile wallet", "home-delivery": "Home delivery", "post-office": "Post office", "unknown": "payout method not stated"},
        "sp": {"minutes": "Within minutes", "same-day": "Same day", "next-day": "Next day", "2-5-days": "2–5 days", "6-plus-days": "6+ days", "": "Speed not stated"},
        "country": {"FR": "France", "IT": "Italy", "DE": "Germany"},
    },
    "fr": {
        "ch": {"online": "En ligne", "app": "Application", "agent": "Espèces en agence", "bank-branch": "En agence bancaire", "post-office": "Au bureau de poste"},
        "po": {"bank-account": "Compte bancaire", "cash-pickup": "Retrait en espèces", "mobile-wallet": "Portefeuille mobile", "home-delivery": "Livraison à domicile", "post-office": "Bureau de poste", "unknown": "mode de versement non précisé"},
        "sp": {"minutes": "En quelques minutes", "same-day": "Le jour même", "next-day": "Le lendemain", "2-5-days": "2 à 5 jours", "6-plus-days": "6 jours et plus", "": "Délai non précisé"},
        "country": {"FR": "France", "IT": "Italie", "DE": "Allemagne"},
    },
    "ar": {
        "ch": {"online": "عبر الإنترنت", "app": "عبر التطبيق", "agent": "نقدًا لدى وكيل", "bank-branch": "في فرع بنكي", "post-office": "في مكتب بريد"},
        "po": {"bank-account": "حساب بنكي", "cash-pickup": "سحب نقدي", "mobile-wallet": "محفظة إلكترونية", "home-delivery": "توصيل إلى المنزل", "post-office": "مكتب بريد", "unknown": "طريقة الصرف غير مذكورة"},
        "sp": {"minutes": "خلال دقائق", "same-day": "في اليوم نفسه", "next-day": "في اليوم الموالي", "2-5-days": "من 2 إلى 5 أيام", "6-plus-days": "6 أيام فأكثر", "": "المدة غير مذكورة"},
        "country": {"FR": "فرنسا", "IT": "إيطاليا", "DE": "ألمانيا"},
    },
}

R = {
    "en": {
        "title": "Send Money to Tunisia: Compare Fees & Exchange Rates (2026)",
        "desc": "Compare money transfer providers from France, Italy and Germany to Tunisia: fees, exchange-rate margins, speed, regulation and how much your family receives.",
        "eyebrow": "Money transfer comparator", "h1": "Send money to Tunisia: compare the real cost",
        "lead": "See how much your family receives in dinars with each provider, once fees and exchange-rate margins are counted. Independent and sorted by what arrives, never by commission.",
        "from": "Sending from", "amount": "Amount you send", "via": "Received as", "all": "All", "sort": "Sort by",
        "s_best": "Most received", "s_fee": "Lowest fee", "s_speed": "Fastest",
        "gets": "Recipient gets", "pays": "You pay", "incl": "fee included", "fee": "Transfer fee", "fx": "Exchange-rate margin", "tot": "Total cost",
        "speed": "Speed", "safety": "Regulated by", "notconf": "Regulator not confirmed", "go": "Go to", "best": "Most received",
        "fastest": "Fastest", "noprice": "Price not independently surveyed — check the provider's calculator", "seeprov": "See price",
        "rate": "Exchange rate used", "rate_live": "mid-market rate, updated daily", "rate_of": "rate of",
        "est": "Estimates. The final amount depends on the provider's rate on the day you send. Always check the quote before paying.",
        "src_rpw": "Fees and exchange-rate margins: World Bank, Remittance Prices Worldwide, {period} (collected {collected}), for transfers of about €140 and €345. We use the closest of the two to your amount.",
        "src_de": "The World Bank does not survey Germany→Tunisia. Below are providers that serve this route, with what their own websites showed in October 2026. Independent prices are not available, so the list is not ranked.",
        "neg": "A negative margin means the provider's rate was better than the mid-market reference on the survey day.",
        "ref": "Some “Go to” buttons are referral links: we may earn a commission if you sign up, at no extra cost to you. It never changes the order.",
        "noresults": "No provider in our data offers this option for this country.",
        "details": "Regulation and payout", "paidout": "Paid out in Tunisia", "entity": "Legal entity",
        "method_h": "How we compare", "method": [
            "We start from the World Bank's Remittance Prices Worldwide survey, the reference used by the G20 and the UN to track transfer costs. It records each provider's fee and exchange-rate margin for two amounts.",
            "We apply those to your amount and to today's mid-market euro–dinar rate, so you see an estimate of what arrives in Tunisia. The mid-market rate is refreshed every day.",
            "Results are sorted by the amount received. Providers cannot pay to appear or to rank higher."],
        "safety_h": "How to check a provider is safe", "safety_items": [
            "Use a provider authorised in the EU. Its legal name and licence are in its terms; you can check them in the regulator's register (ACPR's REGAFI in France, Banca d'Italia in Italy, BaFin in Germany, or the regulator of the country where it is licensed).",
            "Avoid informal channels: there is no protection if money is lost, and they fall outside Tunisian exchange rules.",
            "Never share a transfer reference or code with anyone other than the recipient, and be wary of anyone asking you to send money to a stranger."],
        "tips_h": "Ways to pay less", "tips": [
            "Compare the amount received, not just the fee: a “zero fee” offer can hide a wide exchange-rate margin.",
            "Fees are partly fixed, so one larger transfer usually costs less in percentage terms than several small ones.",
            "Online transfers are usually cheaper than paying cash at an agent or a bank branch.",
            "First-transfer promotions can be generous but are one-offs; compare the regular price too."],
        "related": "Guides", "faq": "Frequently asked questions", "updated": "Data checked",
    },
    "fr": {
        "title": "Envoyer de l'argent en Tunisie : comparateur de frais 2026",
        "desc": "Comparez les services de transfert d'argent de la France, l'Italie et l'Allemagne vers la Tunisie : frais, marge de change, délai, régulation et montant reçu.",
        "eyebrow": "Comparateur de transferts d'argent", "h1": "Envoyer de l'argent en Tunisie : comparez le vrai coût",
        "lead": "Voyez combien vos proches reçoivent en dinars avec chaque service, frais et marge de change compris. Indépendant, et trié selon le montant reçu, jamais selon une commission.",
        "from": "Envoi depuis", "amount": "Montant envoyé", "via": "Réception", "all": "Tous", "sort": "Trier par",
        "s_best": "Montant reçu", "s_fee": "Frais les plus bas", "s_speed": "Plus rapide",
        "gets": "Le bénéficiaire reçoit", "pays": "Vous payez", "incl": "frais inclus", "fee": "Frais d'envoi", "fx": "Marge de change", "tot": "Coût total",
        "speed": "Délai", "safety": "Régulé par", "notconf": "Régulateur non confirmé", "go": "Aller sur", "best": "Le plus reçu",
        "fastest": "Le plus rapide", "noprice": "Prix non relevé de façon indépendante — vérifiez le simulateur du prestataire", "seeprov": "Voir le prix",
        "rate": "Taux de change utilisé", "rate_live": "taux moyen du marché, mis à jour chaque jour", "rate_of": "taux du",
        "est": "Estimations. Le montant final dépend du taux du prestataire le jour de l'envoi. Vérifiez toujours le devis avant de payer.",
        "src_rpw": "Frais et marges de change : Banque mondiale, Remittance Prices Worldwide, {period} (relevés {collected}), pour des envois d'environ 140 € et 345 €. Nous utilisons le plus proche de votre montant.",
        "src_de": "La Banque mondiale ne suit pas le corridor Allemagne→Tunisie. Voici les prestataires qui le desservent, avec ce qu'affichaient leurs sites en octobre 2026. Faute de prix indépendants, la liste n'est pas classée.",
        "neg": "Une marge négative signifie que le taux du prestataire était meilleur que le taux de référence le jour du relevé.",
        "ref": "Certains boutons « Aller sur » sont des liens de parrainage : nous pouvons toucher une commission si vous vous inscrivez, sans surcoût pour vous. Cela ne change jamais le classement.",
        "noresults": "Aucun prestataire de nos données ne propose cette option pour ce pays.",
        "details": "Régulation et versement", "paidout": "Versement en Tunisie", "entity": "Entité légale",
        "method_h": "Notre méthode", "method": [
            "Nous partons de l'enquête Remittance Prices Worldwide de la Banque mondiale, la référence utilisée par le G20 et l'ONU pour suivre le coût des transferts. Elle relève les frais et la marge de change de chaque prestataire pour deux montants.",
            "Nous les appliquons à votre montant et au taux moyen euro–dinar du jour, pour estimer ce qui arrive en Tunisie. Ce taux est actualisé chaque jour.",
            "Les résultats sont triés selon le montant reçu. Aucun prestataire ne peut payer pour apparaître ou être mieux classé."],
        "safety_h": "Comment vérifier qu'un service est sûr", "safety_items": [
            "Utilisez un prestataire agréé dans l'UE. Sa raison sociale et son agrément figurent dans ses conditions ; vérifiez-les dans le registre du régulateur (REGAFI de l'ACPR en France, Banca d'Italia en Italie, BaFin en Allemagne, ou le régulateur du pays où il est agréé).",
            "Évitez les circuits informels : aucune protection en cas de perte, et ils échappent à la réglementation des changes tunisienne.",
            "Ne communiquez jamais le code ou la référence d'un transfert à quelqu'un d'autre que le bénéficiaire, et méfiez-vous de toute demande d'envoi à un inconnu."],
        "tips_h": "Pour payer moins", "tips": [
            "Comparez le montant reçu, pas seulement les frais : une offre « sans frais » peut cacher une large marge de change.",
            "Les frais sont en partie fixes : un envoi plus important coûte généralement moins, en pourcentage, que plusieurs petits.",
            "Les envois en ligne sont généralement moins chers que le paiement en espèces en agence ou au guichet d'une banque.",
            "Les offres de premier transfert peuvent être intéressantes mais ponctuelles : comparez aussi le prix habituel."],
        "related": "Guides", "faq": "Questions fréquentes", "updated": "Données vérifiées",
    },
    "ar": {
        "title": "تحويل الأموال إلى تونس: مقارنة الرسوم وأسعار الصرف 2026",
        "desc": "قارن خدمات تحويل الأموال من فرنسا وإيطاليا وألمانيا إلى تونس: الرسوم، وهامش الصرف، والمدة، والجهة الرقابية، والمبلغ الذي يصل فعلًا إلى عائلتك.",
        "eyebrow": "أداة مقارنة تحويل الأموال", "h1": "تحويل الأموال إلى تونس: قارن التكلفة الحقيقية",
        "lead": "اعرف كم يصل إلى عائلتك بالدينار مع كل مزوّد بعد احتساب الرسوم وهامش الصرف. مقارنة مستقلة مرتبة حسب المبلغ الواصل، لا حسب أي عمولة.",
        "from": "الإرسال من", "amount": "المبلغ المرسَل", "via": "طريقة الاستلام", "all": "الكل", "sort": "الترتيب حسب",
        "s_best": "المبلغ الواصل", "s_fee": "أقل رسوم", "s_speed": "الأسرع",
        "gets": "يستلم المستفيد", "pays": "تدفع", "incl": "شاملة الرسوم", "fee": "رسوم التحويل", "fx": "هامش الصرف", "tot": "التكلفة الإجمالية",
        "speed": "المدة", "safety": "الجهة الرقابية", "notconf": "الجهة الرقابية غير مؤكدة", "go": "انتقل إلى", "best": "أعلى مبلغ واصل",
        "fastest": "الأسرع", "noprice": "لا يوجد سعر مستقل — راجع حاسبة المزوّد", "seeprov": "اطّلع على السعر",
        "rate": "سعر الصرف المعتمد", "rate_live": "السعر المتوسط في السوق، يُحدَّث يوميًا", "rate_of": "سعر يوم",
        "est": "أرقام تقديرية. يتوقف المبلغ النهائي على سعر المزوّد يوم الإرسال. تحقّق دائمًا من العرض قبل الدفع.",
        "src_rpw": "الرسوم وهوامش الصرف: البنك الدولي، قاعدة Remittance Prices Worldwide، {period} (جُمعت البيانات في {collected})، لتحويلات بقيمة 140 و345 يورو تقريبًا. نعتمد الأقرب إلى مبلغك.",
        "src_de": "لا يرصد البنك الدولي ممر ألمانيا←تونس. فيما يلي المزوّدون الذين يخدمونه، مع ما عرضته مواقعهم في أكتوبر 2026. ولعدم توفر أسعار مستقلة، لم يتم ترتيب القائمة.",
        "neg": "الهامش السالب يعني أن سعر المزوّد كان أفضل من السعر المرجعي يوم جمع البيانات.",
        "ref": "بعض أزرار «انتقل إلى» روابط إحالة: قد نحصل على عمولة إذا سجّلت، دون أي تكلفة إضافية عليك. ولا يغيّر ذلك الترتيب أبدًا.",
        "noresults": "لا يوفّر أي مزوّد في بياناتنا هذا الخيار لهذا البلد.",
        "details": "الرقابة وطريقة الصرف", "paidout": "الصرف في تونس", "entity": "الكيان القانوني",
        "method_h": "كيف نقارن", "method": [
            "ننطلق من مسح Remittance Prices Worldwide للبنك الدولي، المرجع الذي تعتمده مجموعة العشرين والأمم المتحدة لمتابعة تكلفة التحويلات. ويرصد رسوم كل مزوّد وهامش الصرف لديه لمبلغين.",
            "نطبّق هذه الأرقام على مبلغك وعلى السعر المتوسط لليورو مقابل الدينار لهذا اليوم، لتقدير ما يصل إلى تونس. ويُحدَّث هذا السعر يوميًا.",
            "تُرتَّب النتائج حسب المبلغ الواصل. ولا يمكن لأي مزوّد أن يدفع مقابل الظهور أو التقدّم في الترتيب."],
        "safety_h": "كيف تتأكد من أمان المزوّد", "safety_items": [
            "استعمل مزوّدًا مرخّصًا في الاتحاد الأوروبي. يرد اسمه القانوني وترخيصه في شروط الاستخدام، ويمكنك التحقق منهما في سجل الجهة الرقابية (سجل REGAFI لدى ACPR في فرنسا، أو بنك إيطاليا، أو BaFin في ألمانيا، أو الجهة الرقابية في البلد الذي رُخّص فيه).",
            "تجنّب القنوات غير الرسمية: لا حماية فيها إذا ضاعت الأموال، وهي خارج تراتيب الصرف التونسية.",
            "لا تشارك رمز التحويل أو مرجعه إلا مع المستفيد، واحذر كل من يطلب منك إرسال المال إلى شخص لا تعرفه."],
        "tips_h": "كيف تدفع أقل", "tips": [
            "قارن المبلغ الواصل لا الرسوم فقط: عرض «بدون رسوم» قد يخفي هامش صرف مرتفعًا.",
            "الرسوم ثابتة جزئيًا، لذلك يكلّف تحويل واحد أكبر عادةً أقل، كنسبة مئوية، من عدة تحويلات صغيرة.",
            "التحويل عبر الإنترنت أرخص عادةً من الدفع نقدًا لدى وكيل أو في فرع بنكي.",
            "عروض التحويل الأول قد تكون مغرية لكنها لمرة واحدة؛ قارن السعر المعتاد أيضًا."],
        "related": "أدلة", "faq": "أسئلة شائعة", "updated": "تاريخ التحقق",
    },
}

LOCALE = {"en": "en-GB", "fr": "fr-FR", "ar": "ar-TN-u-nu-latn"}


def best_lines(L):
    """Facts for the FAQ, computed from the data so they can't drift from the table."""
    out = {}
    for cc in ("FR", "IT"):
        rows = [o for o in DATA[cc]["offers"] if o.get("basis_usd") == 200 and o.get("total_cost_pct") is not None]
        rows.sort(key=lambda o: o["total_cost_pct"])
        seen, top = set(), []
        for o in rows:
            if o["provider_id"] in seen: continue
            seen.add(o["provider_id"]); top.append(o)
            if len(top) == 3: break
        out[cc] = top
    return out


def faq(L):
    b = best_lines(L)
    lab = LBL[L]
    def fmt(o):
        pct = f"{o['total_cost_pct']:.2f}".replace(".", "," if L != "en" else ".")
        return f"{o['provider']} ({lab['ch'][channel(o)].lower() if L != 'ar' else lab['ch'][channel(o)]} → {lab['po'].get((o.get('payout') or ['bank-account'])[0], '')}{', ' if L != 'ar' else '، '}{pct}%)"
    fr_, it_ = "; ".join(fmt(o) for o in b["FR"]), "; ".join(fmt(o) for o in b["IT"])
    period = DATA["FR"].get("data_period") or ""
    if L == "en":
        return [
            ("What is the cheapest way to send money to Tunisia?", f"In the latest World Bank survey ({period}, transfers of about €140), the cheapest options from France were {fr_}. From Italy they were {it_}. Prices change, so use the comparator above with your amount."),
            ("How is the cost of a transfer to Tunisia calculated?", "It has two parts: the transfer fee, and the exchange-rate margin, which is the difference between the rate the provider gives you and the mid-market rate. The comparator adds both and shows how many dinars your recipient gets."),
            ("Is the exchange rate in this comparator up to date?", "Yes. The euro–dinar mid-market rate is refreshed every day. Providers' fees and margins come from the latest World Bank survey, so always confirm the final quote on the provider's website before paying."),
            ("How do I know a money transfer service is safe?", "Use a provider authorised in the European Union. Its legal entity and licence appear in its terms and in the regulator's public register. We show the regulator for each provider in the comparator."),
            ("Why are there no prices for Germany?", "The World Bank does not survey the Germany to Tunisia route, and most providers only show prices in their own calculators. We list who serves the route and how, without ranking them."),
        ]
    if L == "fr":
        return [
            ("Quel est le moyen le moins cher d'envoyer de l'argent en Tunisie ?", f"Dans la dernière enquête de la Banque mondiale ({period}, envois d'environ 140 €), les options les moins chères depuis la France étaient : {fr_}. Depuis l'Italie : {it_}. Les prix évoluent : utilisez le comparateur ci-dessus avec votre montant."),
            ("Comment est calculé le coût d'un transfert vers la Tunisie ?", "Il comprend deux éléments : les frais d'envoi, et la marge de change, c'est-à-dire l'écart entre le taux appliqué par le prestataire et le taux moyen du marché. Le comparateur additionne les deux et indique combien de dinars reçoit votre bénéficiaire."),
            ("Le taux de change du comparateur est-il à jour ?", "Oui. Le taux moyen euro–dinar est actualisé chaque jour. Les frais et marges des prestataires proviennent de la dernière enquête de la Banque mondiale : vérifiez toujours le devis final sur le site du prestataire avant de payer."),
            ("Comment savoir si un service de transfert est sûr ?", "Choisissez un prestataire agréé dans l'Union européenne. Son entité légale et son agrément figurent dans ses conditions et dans le registre public du régulateur. Le comparateur indique le régulateur de chaque prestataire."),
            ("Pourquoi n'y a-t-il pas de prix pour l'Allemagne ?", "La Banque mondiale ne suit pas le corridor Allemagne–Tunisie, et la plupart des prestataires n'affichent leurs prix que dans leur simulateur. Nous indiquons qui dessert ce corridor et comment, sans classement."),
        ]
    return [
        ("ما أرخص طريقة لتحويل المال إلى تونس؟", f"في آخر مسح للبنك الدولي ({period}، تحويلات بقيمة 140 يورو تقريبًا)، كانت أرخص الخيارات من فرنسا: {fr_}. ومن إيطاليا: {it_}. الأسعار تتغير، لذا استعمل أداة المقارنة أعلاه مع مبلغك."),
        ("كيف تُحتسب تكلفة التحويل إلى تونس؟", "تتكون من عنصرين: رسوم التحويل، وهامش الصرف أي الفرق بين السعر الذي يطبّقه المزوّد والسعر المتوسط في السوق. تجمع أداة المقارنة العنصرين وتبيّن عدد الدنانير التي يستلمها المستفيد."),
        ("هل سعر الصرف في أداة المقارنة محدَّث؟", "نعم. يُحدَّث السعر المتوسط لليورو مقابل الدينار يوميًا. أما رسوم المزوّدين وهوامشهم فمصدرها آخر مسح للبنك الدولي، لذا تحقّق دائمًا من العرض النهائي على موقع المزوّد قبل الدفع."),
        ("كيف أعرف أن خدمة التحويل آمنة؟", "اختر مزوّدًا مرخّصًا في الاتحاد الأوروبي. يرد كيانه القانوني وترخيصه في شروط الاستخدام وفي السجل العمومي للجهة الرقابية. وتعرض أداة المقارنة الجهة الرقابية لكل مزوّد."),
        ("لماذا لا توجد أسعار لألمانيا؟", "لا يرصد البنك الدولي ممر ألمانيا–تونس، ومعظم المزوّدين لا يعرضون أسعارهم إلا في حاسباتهم الخاصة. لذلك نذكر من يخدم هذا الممر وكيف، دون ترتيب."),
    ]


def payload(L):
    lab = LBL[L]
    cors = {}
    for cc in CORRIDORS:
        d = DATA[cc]
        cors[cc] = {
            "rpw": cc != "DE",
            "period": d.get("data_period"), "collected": d.get("data_collected"),
            "avg": (d.get("corridor_average_total_cost_pct") or {}).get("200"),
            "offers": offers(cc),
        }
        for g in cors[cc]["offers"]:
            p = provider(cc, g["pid"])
            g["note"] = p.get("regulated_" + L) or ""
            g["paid"] = p.get("tunisia_payout_" + L) or ""
    return {"rate": FX["rate"], "date": FX["date"], "corridors": cors, "L": L, "locale": LOCALE[L],
            "lbl": {"ch": lab["ch"], "po": lab["po"], "sp": lab["sp"]},
            "t": {k: R[L][k] for k in ("gets", "pays", "incl", "fee", "fx", "tot", "speed", "safety", "notconf", "go", "best", "fastest",
                                       "noprice", "seeprov", "noresults", "details", "paidout", "entity", "rate_of")}}


def build(B):
    for L in B.LANGS:
        _build(B, L)


def _build(B, L):
    t = B.T[L]; r = R[L]; lab = LBL[L]
    path = B.path_of(L, "remit"); page = B.Page(path)
    alt = {l: B.path_of(l, "remit") for l in B.LANGS}
    crumbs = [(t["home"], B.path_of(L, "home")), (r["eyebrow"], path)]
    fq = faq(L)
    lds = [{"@context": "https://schema.org", "@type": "WebPage", "name": r["h1"], "description": r["desc"], "url": B.absu(path),
            "inLanguage": L, "dateModified": B.iso(B.BUILD_DATE), "publisher": {"@id": f"{B.SITE}/#org"}},
           B.crumbs_ld(crumbs),
           {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in fq]}]
    h = B.head(page, L, f"{r['title']} | {B.SITE_NAME}", r["desc"], path, alt, B.og_rel("send-money-to-tunisia", L), ld=lds)
    h += B.header(page, L, "remit", alt)
    data = json.dumps(payload(L), ensure_ascii=False).replace("</", "<\\/")
    countries = "".join(f'<button type="button" class="seg{" on" if cc == "FR" else ""}" data-cc="{cc}" aria-pressed="{"true" if cc == "FR" else "false"}">{lab["country"][cc]}</button>' for cc in CORRIDORS)
    pos = ["bank-account", "cash-pickup", "mobile-wallet"]
    via = f'<button type="button" class="chip active" data-po="">{r["all"]}</button>' + "".join(f'<button type="button" class="chip" data-po="{p}">{lab["po"][p]}</button>' for p in pos)
    any_ref = any(g["ref"] for cc in CORRIDORS for g in offers(cc))
    period = DATA["FR"].get("data_period") or ""
    collected = "août 2025" if L == "fr" else ("أوت 2025" if L == "ar" else "August 2025")
    rate_txt = f"{FX['rate']:.4f}" if L == "en" else f"{FX['rate']:.4f}".replace(".", ",")
    rel_posts = [B.POST[s] for s in ("cheapest-way-send-money-to-tunisia", "receive-money-in-tunisia", "diaspora-remittances-tunisia") if s in B.POST]
    rel = "".join(B.card(page, L, p) for p in rel_posts)
    faqs = "".join(f'<details class="faq-item"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in fq)
    h += f"""
<section class="page-head remit-head"><div class="wrap">
  {B.crumbs_html(page, crumbs)}
  <span class="eyebrow">{r['eyebrow']}</span>
  <h1>{E(r['h1'])}</h1>
  <p class="lead">{E(r['lead'])}</p>
  <form class="calc" id="remit-calc" onsubmit="return false">
    <div class="calc-row">
      <div class="calc-f"><span class="calc-l" id="lbl-from">{r['from']}</span><div class="segs" role="group" aria-labelledby="lbl-from">{countries}</div></div>
      <div class="calc-f"><label class="calc-l" for="remit-amt">{r['amount']}</label><div class="amt"><input id="remit-amt" type="number" inputmode="decimal" min="10" max="10000" step="10" value="200"><span>EUR</span></div></div>
    </div>
    <div class="calc-row">
      <div class="calc-f"><span class="calc-l" id="lbl-via">{r['via']}</span><div class="chips" id="remit-po" role="group" aria-labelledby="lbl-via">{via}</div></div>
      <div class="calc-f calc-sort"><label class="calc-l" for="remit-sort">{r['sort']}</label><select id="remit-sort"><option value="best">{r['s_best']}</option><option value="fee">{r['s_fee']}</option><option value="speed">{r['s_speed']}</option></select></div>
    </div>
  </form>
  <p class="rate-line" id="remit-rate">{r['rate']}: <b>1 EUR = <span id="rate-v">{rate_txt}</span> TND</b> · {r['rate_live']} (<span id="rate-d">{B.fdate(FX['date'], L)}</span>)</p>
</div></section>
<section class="listing remit-list"><div class="wrap">
  <p class="remit-src" id="remit-src" data-rpw="{E(r['src_rpw'].format(period=period, collected=collected))}" data-de="{E(r['src_de'])}">{E(r['src_rpw'].format(period=period, collected=collected))}</p>
  <div id="remit-results" class="remit-results" aria-live="polite"></div>
  <p class="no-results" id="remit-empty" hidden>{r['noresults']}</p>
  <p class="remit-fine">{E(r['est'])} {E(r['neg'])}{(' ' + E(r['ref'])) if any_ref else ''}</p>
</div></section>
<section class="sec sec-alt"><div class="wrap remit-info">
  <div><h2>{r['method_h']}</h2>{''.join(f'<p>{E(x)}</p>' for x in r['method'])}</div>
  <div><h2>{r['safety_h']}</h2><ul>{''.join(f'<li>{E(x)}</li>' for x in r['safety_items'])}</ul></div>
  <div><h2>{r['tips_h']}</h2><ul>{''.join(f'<li>{E(x)}</li>' for x in r['tips'])}</ul></div>
</div></section>
{f'<section class="related"><div class="wrap"><h2>{r["related"]}</h2><div class="grid grid-3">{rel}</div></div></section>' if rel else ''}
<section class="sec"><div class="wrap narrow"><section class="faq"><h2>{r['faq']}</h2>{faqs}</section>
<p class="disclaimer">{E(t['disclaimer'])}</p></div></section>
<script type="application/json" id="remit-data">{data}</script>
<script src="{page.rel('assets/remit.js')}" defer></script>"""
    h += B.footer(page, L)
    B.write(path, h)
