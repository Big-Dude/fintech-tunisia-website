# Fintech Tunisia — regulation tracker brief

Build a tracker of laws, decrees, BCT circulars, CMF regulations, bills and official strategies that
affect fintech in Tunisia. Output ONE file: `/home/claude/site-v2/regulation/tracker.json`.
Today: 2026-10-10.

## Method
1. FIRST read the existing researched articles in /home/claude/site-v2/content/*.json (especially
   bct-regulatory-sandbox, payment-institutions-tunisia, tunisia-foreign-exchange-code-reform,
   crypto-regulation-tunisia, crowdfunding-law-tunisia, data-protection-tunisia-fintech, ekyc-aml-tunisia,
   tunisia-labor-law-reform-startups, startup-act-tunisia-explained, cash-economy-tunisia,
   cybersecurity-financial-sector-tunisia, open-banking-tunisia, neobanks-tunisia, instant-payments-tunisia,
   insurtech-tunisia, la-poste-tunisienne-e-dinar-d17). They contain sourced facts and source URLs.
2. Extract every regulatory instrument they mention. Then use a few web searches (quota is limited:
   ~10–15 total) to fill clear gaps and check the latest status of pending items (bills).
3. Never invent numbers, dates or statuses. If a date is only known to the month or year, use that.
   If status is unclear, use "unclear" and explain.

## Entry format
```json
{
  "updated": "2026-10-10",
  "entries": [
    {
      "id": "bct-circular-2026-10",
      "type": "law | decree | decree-law | bct-circular | cmf-regulation | bill | strategy | other",
      "reference": "Circular No. 2026-10",
      "issuer": "BCT | Parliament | Government | CMF | ACM | CGA | Presidency",
      "title_en": "Payment institutions: licensing, KYC tiers and account caps",
      "title_fr": "Établissements de paiement : agrément, niveaux KYC et plafonds",
      "date": "2026-09-25",
      "in_force": "2026-12 (approx.) or null",
      "status": "in_force | adopted_not_in_force | in_parliament | draft | announced | repealed | replaced | unclear",
      "status_note_en": "short", "status_note_fr": "court",
      "summary_en": "40–90 words: what it does and who it affects",
      "summary_fr": "40–90 mots",
      "topics": ["payments", "kyc", "fx", "crypto", "crowdfunding", "data", "startups", "labour", "cyber", "cash", "insurance", "banking"],
      "related_articles": ["slugs of articles in content/"],
      "replaces": "id of the entry it replaces, or null",
      "source_url": "https://...",
      "source_name": "..."
    }
  ]
}
```
Aim for 20–35 entries, including older foundational texts still in force (e.g. Startup Act 2018-20,
data protection law 2004-63, the 1976 FX code, banking law 2016-48, crowdfunding law 2020-37,
BCT circular 2018-16, cheque law 2024-41, labour law 2025-9) and pending items (FX code bill,
data protection bill, Startup Act 2.0 if officially announced). Sort entries newest first.

Validate the JSON. Final report: count, any items whose status you couldn't confirm. Keep it short.
