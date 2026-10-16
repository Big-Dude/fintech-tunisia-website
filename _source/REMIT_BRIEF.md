# Remittance comparator — data brief

We are building a comparator on fintechtunisia.com: "the cheapest way to send money to Tunisia" from
France, Italy and Germany. Each sending country is a "corridor". Today: 2026-10-15.
Accuracy is critical: real companies, real prices, read by people sending money to family.

## Primary source
World Bank **Remittance Prices Worldwide (RPW)** — https://remittanceprices.worldbank.org/
Corridor pages: /corridor/France/Tunisia, /corridor/Italy/Tunisia, /corridor/Germany/Tunisia
(the corridor may also be reachable via the "Countries" or data download pages). RPW surveys providers
quarterly for two amounts (the local equivalent of USD 200 and USD 500) and reports, per provider/product:
fee, exchange-rate margin (%), total cost (%), speed of transfer, how money is sent and how it is picked up.
Use the MOST RECENT quarter available and record which quarter.
If the corridor page doesn't load, try the RPW data download (Excel/CSV) or the corridor's "print" view.
If RPW for your corridor is truly unavailable, say so and fall back to providers' own published fee pages
(and mark each figure's source and date).

## Safety / regulation (second pass, per provider)
For each provider, find which entity serves customers in your sending country and its regulator, e.g.
"Western Union Payment Services Ireland Ltd, authorised by the Central Bank of Ireland" — check the
provider's legal/terms page or the regulator's register (ACPR REGAFI for France, Banca d'Italia, BaFin,
NBB, Central Bank of Ireland, Banco de España). Banks: their national banking licence. Record source URLs.
Also note how money is paid out in Tunisia (bank account, cash pickup at agent/bank/La Poste, wallet)
and any known Tunisian payout partners IF stated by the provider. Don't guess.

## Rules
- Never invent fees, margins, speeds or licences. Unknown → null.
- Use the provider's commercial name ("Western Union", "Ria", "MoneyGram", "Remitly", "WorldRemit",
  "Taptap Send", "Wise", "La Banque Postale", "Attijariwafa Bank"...). One offer per product/channel row in RPW.
- Wise: include only if it actually supports sending EUR to TND bank accounts in Tunisia (check its
  currency page). If not, list it under "not_available" with the source.
- Web search quota is limited and shared: be efficient (~15 searches/fetches total).

## Output: /home/claude/site-v2/remit/<CC>.json  (CC = FR, IT or DE)
```json
{
  "corridor": "FR",
  "country_en": "France", "country_fr": "France", "country_ar": "فرنسا",
  "currency": "EUR",
  "data_period": "Q2 2026",
  "data_collected": "2026-05 or null",
  "source_name": "World Bank, Remittance Prices Worldwide",
  "source_url": "https://remittanceprices.worldbank.org/corridor/France/Tunisia",
  "corridor_average_total_cost_pct": {"200": 5.50, "500": null},
  "offers": [
    {"provider_id": "western-union", "provider": "Western Union", "firm_type": "mto | bank | post | fintech",
     "product": "short description of the channel, e.g. 'Online to bank account'",
     "send_method": ["online", "app", "agent", "bank-branch"],
     "payout": ["bank-account", "cash-pickup", "mobile-wallet", "home-delivery", "post-office"],
     "speed": "minutes | same-day | next-day | 2-5-days | 6-plus-days",
     "basis_usd": 200, "send_amount": 175.0, "fee": 4.90, "fx_margin_pct": 1.95, "total_cost_pct": 4.75,
     "source_url": "https://..."}
  ],
  "providers": {
    "western-union": {
      "name": "Western Union", "website": "https://www.westernunion.com/fr/",
      "entity": "Western Union International Bank GmbH", "regulator": "Austrian Financial Market Authority (FMA)",
      "regulated_en": "short sentence", "regulated_fr": "phrase courte", "regulated_ar": "جملة قصيرة",
      "tunisia_payout_en": "how recipients in Tunisia receive money, or null", "tunisia_payout_fr": "...", "tunisia_payout_ar": "...",
      "source_urls": ["https://..."]
    }
  },
  "not_available": [{"provider": "Wise", "reason_en": "...", "reason_fr": "...", "reason_ar": "...", "source_url": "https://..."}],
  "notes": "anything the site owner should know"
}
```
Include BOTH the USD 200 and USD 500 basis rows when RPW publishes both (one offer object each, same
provider_id/product, different basis_usd). Validate the JSON. Write scripts in your own scratchpad folder.
Final report: data period found, number of offers, anything uncertain. Keep it short.
