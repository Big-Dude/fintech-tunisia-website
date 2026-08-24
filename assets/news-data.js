// Fintech Tunisia — news articles data
// This is the fallback list used if JSONBin.io isn't set up yet or is unreachable.
// To add a new article: copy an object below, edit the fields, and add it to the TOP of the array
// (newest first). Save the file and re-upload/redeploy the site.
//
// Fields:
//   id        - unique short slug, matches the article's own page filename when it has one
//   date      - "YYYY-MM-DD"
//   tag       - one of: "Funding", "Regulation", "Banking", "Startups", "Policy" (or add your own)
//   title     - headline
//   summary   - 2-3 sentence summary shown on the card
//   url       - link to the article's own page on this site, e.g. "news/my-article.html".
//               Leave "" if this article doesn't have its own page yet (falls back to a
//               same-page anchor on news.html instead).
//   source    - name of the original outlet cited within the article (leave "" if none)
//   sourceUrl - link to that outlet (leave "" if none) — shown inside the article, not on the card

const NEWS_ARTICLES = [
  {
    id: "tunisia-zero-equity-deals-h1-2026",
    date: "2026-07-29",
    tag: "Startups",
    title: "Zero Disclosed Equity Deals: What Happened to Tunisia's Startup Ecosystem in H1 2026",
    summary: "Tunisia recorded no disclosed equity deals in the first half of 2026, down from six deals worth roughly $5.4 million a year earlier. A restrictive labor law and unfinished FX reform pushed investor activity to a standstill.",
    url: "news/tunisia-zero-equity-deals-h1-2026.html",
    source: "Launchbase Africa",
    sourceUrl: "https://launchbaseafrica.com/2026/07/29/near-zero-equity-deals-in-h1-what-happened-to-tunisias-startup-ecosystem/"
  },
  {
    id: "tunisia-startups-h1-2026-funding",
    date: "2026-07-17",
    tag: "Funding",
    title: "Tunisian Startups Raised Just $300,000 in H1 2026 — Here's What That Signals",
    summary: "Local ventures secured three deals worth $300,000 combined in H1 2026 — a fraction of what neighboring Morocco raised alone, and a warning sign for Tunisia's place in the regional funding map.",
    url: "news/tunisia-startups-h1-2026-funding.html",
    source: "African Manager",
    sourceUrl: "https://en.africanmanager.com/tunisian-startups-raise-just-300000-in-h1-2026/"
  },
  {
    id: "bolt-withdraws-tunisia",
    date: "2025-05-09",
    tag: "Regulation",
    title: "Bolt Officially Withdraws From Tunisia After Money-Laundering Probe",
    summary: "Nearly two months after Tunisian authorities suspended its operations over tax and licensing allegations, Bolt quietly shut down in Tunisia — with no public explanation and millions in seized assets left behind.",
    url: "news/bolt-withdraws-tunisia.html",
    source: "Launchbase Africa",
    sourceUrl: "https://launchbaseafrica.com/2025/03/24/tunisian-authorities-suspend-bolt-operations-and-seize-millions-in-money-laundering-probe/"
  },
  {
    id: "easybank-funding",
    date: "2025-02-04",
    tag: "Funding",
    title: "EasyBank Raises $370K to Bring AI-Powered Banking to Underserved Tunisians",
    summary: "The Tunis-based fintech will use its 1.2 million dinar raise to expand AI-driven banking and lending tools across the Middle East, North Africa and France.",
    url: "news/easybank-funding.html",
    source: "Techpression",
    sourceUrl: "https://techpression.com/tunisian-startup-easybank-secures-370000/"
  },
  {
    id: "atb-temenos-core-banking",
    date: "2022-06-22",
    tag: "Banking",
    title: "Arab Tunisian Bank Goes Live on Temenos in Two-Phase Modernization",
    summary: "The 134-branch bank has migrated its retail and corporate operations onto Temenos' composable banking platform, with digital banking and payments modernization planned as phase two.",
    url: "news/atb-temenos-core-banking.html",
    source: "Temenos",
    sourceUrl: "https://www.temenos.com/press_release/arab-tunisian-bank-goes-live-on-temenos-to-power-sustainable-growth/"
  }
];
