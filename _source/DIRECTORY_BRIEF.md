# Fintech Tunisia — company directory brief

Site: https://fintechtunisia.com (bilingual EN/FR). Today: 2026-10-10.
We are building a directory of fintech companies operating in Tunisia. Each company = one JSON file in
`/home/claude/site-v2/directory/<slug>.json`. Each gets its own public page, so accuracy matters:
companies will read their own listing.

## Accuracy rules
- Research every company on the web (company site, LinkedIn page, BCT lists, startup.gov.tn, CMF,
  press: Launch Base Africa, Wamda, TechCabal, African Manager, La Presse, Webdo, Managers, Kapitalis,
  Ilboursa, Business News, Tuniscope, webmanagercenter). Never invent facts.
- Unknown = `null`. Don't guess founding years, funding, licences or founders.
- Licence status must be backed by a source (BCT announcement/list, press report, company statement).
  If a company says it works "with a partner bank", say that; don't upgrade it to a licence.
- Funding: only disclosed rounds with a source. Undisclosed amount → `"amount": null`.
- Status: "active", "acquired", "inactive", or "unclear" (e.g. site down, no news in 2+ years,
  conflicting reports). Explain unclear cases in `status_note`.
- No founder names unless widely reported in reputable press (then OK to include in `people`).
- Descriptions: neutral, factual, not promotional. Company claims → attribute them ("the company says").
- Existing site articles have relevant research: read /home/claude/site-v2/content/flouci-profile.json,
  konnect-networks-profile.json, paymee-profile.json, mobile-payments-tunisia.json,
  payment-institutions-tunisia.json, tunisia-fintech-ecosystem-map.json, insurtech-tunisia.json,
  crowdfunding-law-tunisia.json, easybank-funding.json, expensya-medius-acquisition.json before searching.
- Web search quota is limited and shared: ~2–3 searches per company. Prioritise companies with
  enough public information; skip ones you can't verify (mention them in your report).

## JSON format
```json
{
  "slug": "kebab-case-name",
  "name": "Official name",
  "also_known_as": ["brand or legal names"],
  "category": "payments | wallet | gateway | infrastructure | lending | insurtech | regtech | crowdfunding | b2b-finance | remittance | banking-tech | crypto",
  "website": "https://... or null",
  "founded": 2018,
  "hq": "Tunis",
  "status": "active | acquired | inactive | unclear",
  "status_note": "short explanation or null",
  "licences": [
    {"type": "bct-payment-institution | bct-sandbox | startup-label | cmf | acm | cga | bank | partner-bank | other",
     "label_en": "Licensed payment institution (BCT)", "label_fr": "Établissement de paiement agréé (BCT)",
     "date": "2021-05 or null", "source_url": "https://..."}
  ],
  "funding": [{"date": "2024-12", "round": "Seed", "amount": "$1.5M", "investors": ["..."], "source_url": "https://..."}],
  "people": [{"name": "...", "role": "Co-founder & CEO", "source_url": "https://..."}],
  "en": {"tagline": "≤ 90 chars, what it does", "description": "120–220 words, neutral", "products": ["2–5 short items"]},
  "fr": {"tagline": "...", "description": "120–220 mots, français natif", "products": ["..."]},
  "related_articles": ["slugs from /home/claude/site-v2/content/ that mention it"],
  "sources": [{"title": "...", "publisher": "...", "url": "https://..."}],
  "last_verified": "2026-10-10"
}
```
Validate each file with `python3 -c "import json;json.load(open('<file>'))"`. Write each file as soon as
it's done. Helper scripts go in your own scratchpad subfolder, not in /home/claude/site-v2.

Final report: files written, companies skipped and why, anything uncertain. Keep it short.
