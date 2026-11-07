"""Soft, clearly labelled ad slots. Used only on article pages and exchange-rate pages."""
import json, os, html, zlib
E = html.escape
CFG = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ads.json"), encoding="utf-8"))
REF = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "remit", "referrals.json"), encoding="utf-8"))

LBL = {"en": "Advertisement", "fr": "Publicité", "ar": "إعلان"}
REFL = {"en": "Referral link: we may earn a commission, at no cost to you.", "fr": "Lien de parrainage : nous pouvons percevoir une commission, sans frais pour vous.", "ar": "رابط إحالة: قد نحصل على عمولة دون أي تكلفة عليك."}
C = {
    "remit": {"en": ("Sending money to Tunisia?", "Compare fees, exchange rates and speed across banks and transfer apps, updated daily.", "Compare transfers"),
              "fr": ("Vous envoyez de l'argent en Tunisie ?", "Comparez frais, taux de change et délais des banques et applis de transfert, mis à jour chaque jour.", "Comparer les transferts"),
              "ar": ("هل ترسل أموالًا إلى تونس؟", "قارن الرسوم وأسعار الصرف والسرعة لدى البنوك وتطبيقات التحويل، مع تحديث يومي.", "قارن خدمات التحويل")},
    "sendwave": {"en": ("Sendwave: €10 off your first transfer to Tunisia", "Use code IS11I on your first transfer. Sendwave's terms apply.", "Try Sendwave"),
                 "fr": ("Sendwave : 10 € offerts sur votre premier transfert vers la Tunisie", "Code IS11I sur votre premier transfert. Conditions Sendwave.", "Essayer Sendwave"),
                 "ar": ("Sendwave: خصم 10 يورو على أول تحويل إلى تونس", "استعمل الرمز IS11I في أول تحويل. وفق شروط Sendwave.", "جرّب Sendwave")},
    "wu": {"fr": ("Western Union : envoyez de l'argent depuis la France", "Retrait en espèces ou versement sur compte en Tunisie. Comparez le montant reçu avant d'envoyer.", "Voir Western Union")},
}


def _pool(L, kind):
    pool = []
    if REF.get("sendwave", {}).get("default"): pool.append(("sendwave", REF["sendwave"]["default"]))
    if L == "fr" and REF.get("western-union", {}).get("FR"): pool.append(("wu", REF["western-union"]["FR"]))
    if kind == "article": pool.append(("remit", None))
    return pool or [("remit", None)]


def slot(B, page, L, key, kind):
    if not CFG.get("enabled"): return ""
    lbl = f'<span class="ad-lbl">{LBL[L]}</span>'
    client, sid = CFG.get("adsense_client"), CFG.get(f"adsense_slot_{kind}")
    if client and sid:
        return (f'<aside class="ad ad-g" aria-label="{LBL[L]}">{lbl}<ins class="adsbygoogle" style="display:block" data-ad-client="{E(client)}" data-ad-slot="{E(sid)}" data-ad-format="auto" data-full-width-responsive="true"></ins>'
                f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={E(client)}" crossorigin="anonymous"></script><script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script></aside>')
    pool = _pool(L, kind)
    cid, url = pool[zlib.crc32(key.encode()) % len(pool)]
    h, p, cta = C[cid][L]
    if url:
        href, rel, fine = url, "sponsored noopener", f'<span class="ad-fine">{REFL[L]}</span>'
    else:
        href, rel, fine = page.rel(B.path_of(L, "remit")), "", ""
    ra = f' target="_blank" rel="{rel}"' if rel else ""
    return (f'<aside class="ad ad-house ad-{cid}" aria-label="{LBL[L]}">{lbl}<div class="ad-body"><div><strong>{E(h)}</strong><p>{E(p)}</p>{fine}</div>'
            f'<a class="btn btn-ghost ad-cta" href="{E(href)}"{ra} data-goatcounter-click="ad-{cid}">{E(cta)}</a></div></aside>')
