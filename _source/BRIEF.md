# Fintech Tunisia — article writing brief (read fully before writing)

Site: https://fintechtunisia.com — an independent bilingual (English + French) publication covering
fintech in Tunisia, North Africa and Africa. Audience: founders, bankers, investors, regulators,
students, journalists. Today's date: 2026-10-09.

## Your job
For EACH topic assigned to you: research it on the web, then write ONE JSON file
`/home/claude/site-v2/content/<slug>.json` containing the article in BOTH English and French.

## Accuracy rules (most important)
- Research every topic with web searches and read real sources before writing. Prefer primary
  sources (BCT, CMF, laws in JORT, World Bank Findex, company sites, GSMA) and reputable press
  (Reuters, TechCabal, Launchbase Africa, Wamda, African Manager, La Presse, Webdo, Kapitalis,
  Ilboursa, Businessnews.com.tn, Partech Africa reports, Briter Bridges).
- NEVER invent numbers, dates, names, funding amounts, quotes or laws. Every figure must come from a
  source you actually read. If you can't verify something, write about it qualitatively or leave it out.
- No fabricated quotes. Do not put words in real people's mouths.
- Time-sensitive facts: anchor them ("as of 2025", "according to the 2025 Findex").
  If something may have changed, say so.
- If a topic turns out to rest on a false premise (e.g. a law doesn't exist), write the accurate
  version of the story instead and say so in your final report.
- List the sources you used (2–6) in `sources`, with real URLs you opened.

## Writing
- English: 750–1100 words of body. French: same substance, written natively (not a literal
  translation), proper French typography (espace avant : ; ? !, guillemets « »).
- Journalistic, clear, specific, useful. Explain why it matters for Tunisian founders/users.
  No hype, no filler ("in today's fast-paced world"), no marketing tone.
- Structure: short intro (2–3 sentences, no heading), then 4–7 sections with `##` headings,
  optional `###` subheadings, short paragraphs, some bullet lists where they help.
  Do NOT include an H1 (the title is rendered separately). Do NOT include a "Sources" or
  "FAQ" section in the body (rendered separately).
- Internal links: link to 2–4 other articles from the topic list when relevant, using the
  syntax `[anchor text](post:other-slug)` — exactly that `post:` prefix, same in EN and FR.
  Only use slugs from the master list below.
- External links in body are fine: `[text](https://...)` — only URLs you verified.
- SEO: put the main keyword naturally in the title, the first paragraph and one `##` heading.
  Titles ≤ 65 characters where possible. meta_description 140–158 characters, compelling, no quotes.

## JSON format (must be valid JSON; use \n for newlines inside strings)
```json
{
  "slug": "kebab-case-slug-from-your-assignment",
  "category": "ecosystem | regulation | payments | banking | inclusion | funding | africa | startups",
  "cover_motif": "one of: map-tunisia, map-africa, phone-wallet, bank-building, chart-up, chart-down, shield-lock, network-nodes, coins, globe-links, scales-law, rocket, people, document, chip-ai, handshake",
  "stats": [
    {"value": "37%", "label_en": "short label", "label_fr": "libellé court", "source": "Source name, year"}
  ],
  "chart": null,
  "en": {
    "title": "...",
    "meta_description": "...",
    "excerpt": "1–2 sentence teaser for cards",
    "keywords": ["5 to 8 search phrases"],
    "tags": ["3 to 5 short tags"],
    "key_takeaways": ["3 to 4 one-sentence takeaways"],
    "body": "Markdown body...",
    "faq": [{"q": "question people actually search", "a": "2–4 sentence answer"}]
  },
  "fr": { same keys, in French },
  "sources": [{"title": "...", "publisher": "...", "url": "https://..."}]
}
```
- `stats`: 0–3 headline numbers, ONLY if sourced. Rendered as big stat cards.
- `chart`: either `null` or a bar chart built ONLY from sourced numbers:
  `{"title_en": "...", "title_fr": "...", "unit": "%", "bars": [{"label_en": "...", "label_fr": "...", "value": 37.0}], "source_name": "...", "source_url": "https://..."}`
  3–8 bars. Include a chart when the topic has a natural, verified numeric comparison
  (aim for roughly half of your articles). Never estimate values.
- `faq`: 2–4 items each language.

## Master topic list (slug — working angle). Only link to these.
### Ecosystem
- tunisia-fintech-ecosystem-map — Who's who: banks, PSPs, wallets, startups, regulators, investors
- startup-act-tunisia-explained — The 2018 Startup Act & Startup Label: what fintech founders get
- tunisia-fintech-key-numbers — Key numbers: accounts, cards, mobile money, internet, e-commerce
- tunisia-tech-talent-brain-drain — Engineering talent, emigration and what it means for fintech
- tunisia-incubators-accelerators — Incubators/accelerators supporting fintech founders
- tunisia-morocco-egypt-fintech-comparison — North Africa compared
### Regulation
- bct-regulatory-sandbox — The Central Bank of Tunisia's fintech regulatory sandbox
- payment-institutions-tunisia — Payment institutions & e-money licensing in Tunisia
- tunisia-foreign-exchange-code-reform — FX code reform and why it matters for startups
- crypto-regulation-tunisia — The legal status of crypto assets in Tunisia
- crowdfunding-law-tunisia — Tunisia's crowdfunding law and the CMF framework
- data-protection-tunisia-fintech — Personal data protection (INPDP, 2004 law, reform) for fintechs
- ekyc-aml-tunisia — AML/CFT and remote onboarding (e-KYC) rules
- tunisia-labor-law-reform-startups — 2025 labour code reform (fixed-term contracts/subcontracting) and startups
### Payments
- mobile-payments-tunisia — The mobile wallet landscape in Tunisia
- flouci-profile — Flouci: company profile
- konnect-networks-profile — Konnect Networks: company profile
- paymee-profile — Paymee: company profile
- la-poste-tunisienne-e-dinar-d17 — La Poste Tunisienne's e-Dinar and D17
- instant-payments-tunisia — Instant payments, national switching (SMT/Monétique Tunisie) & interoperability
- ecommerce-payments-tunisia — Online payments, ClicToPay, cash on delivery
### Banking
- digital-banking-tunisia — Tunisian banks' digital transformation
- neobanks-tunisia — Can neobanks emerge in Tunisia?
- open-banking-tunisia — Open banking & APIs: where Tunisia stands
- islamic-fintech-tunisia — Islamic finance and fintech (Zitouna, Al Baraka, Wifak)
- ai-in-tunisian-banking — AI in Tunisian banking
- cybersecurity-financial-sector-tunisia — Cybersecurity in Tunisia's financial sector
- insurtech-tunisia — Insurtech in Tunisia
### Inclusion
- financial-inclusion-tunisia — Financial inclusion: what the data says (Findex etc.)
- microfinance-tunisia — Microfinance: Enda Tamweel, Taysir, the ACM regulator
- women-financial-inclusion-tunisia — Women and access to finance
- diaspora-remittances-tunisia — Diaspora remittances and digital transfer channels
- cash-economy-tunisia — Cash, informality and the cashless push
### Funding
- tunisia-startup-funding-trends — Startup funding trends 2024–2026
- anava-fund-of-funds — ANAVA fund of funds explained
- venture-capital-tunisia — VC firms investing in Tunisian startups
- expensya-medius-acquisition — Expensya's acquisition by Medius: an exit story
- instadeep-biontech-lessons — InstaDeep/BioNTech: lessons for Tunisian tech
- how-to-raise-funding-tunisian-fintech — Practical guide to raising money as a Tunisian fintech
### Africa
- african-fintech-funding — African fintech funding: the latest picture
- m-pesa-lessons — M-Pesa: lessons for North Africa
- flutterwave-paystack-payment-rails — Flutterwave, Paystack and Africa's payment rails
- papss-pan-african-payments — PAPSS: the Pan-African Payment and Settlement System
- afcfta-digital-trade-payments — AfCFTA, digital trade and cross-border payments
- african-fintech-unicorns — Africa's fintech unicorns (Moniepoint, OPay, Wave, etc.)
- wave-senegal-mobile-money — How Wave disrupted mobile money pricing
- egypt-fintech-instapay — Egypt's fintech boom: InstaPay, MNT-Halan, Fawry
- morocco-fintech — Morocco's fintech scene and regulation
- stablecoins-africa — Stablecoins and crypto adoption in Africa
- enaira-cbdc-lessons — The eNaira and lessons on CBDCs for North Africa
### Migrated news (agent "news" only)
- tunisia-zero-equity-deals-h1-2026, tunisia-startups-h1-2026-funding, bolt-withdraws-tunisia,
  easybank-funding, atb-temenos-core-banking

## When done
Validate each file with `python3 -c "import json;json.load(open('<file>'))"`.
Final report: list of files written, any topic whose premise you corrected, any facts you
were unsure of. Keep the report short.
