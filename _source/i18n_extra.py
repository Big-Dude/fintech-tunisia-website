"""Copy for About / Editorial policy / Corrections, plus directory and tracker labels."""

GOATCOUNTER = "fintechtunisia"   # https://fintechtunisia.goatcounter.com

NAV = {
    "en": {"directory": "Directory", "tracker": "Regulation", "about": "About", "remit": "Send money"},
    "fr": {"directory": "Annuaire", "tracker": "Réglementation", "about": "À propos", "remit": "Transferts"},
}

DIR_CAT = {
    "en": {"payments": "Payments", "wallet": "Mobile wallet", "gateway": "Payment gateway", "infrastructure": "Payment infrastructure",
           "lending": "Lending & microfinance", "insurtech": "Insurtech", "regtech": "RegTech", "crowdfunding": "Crowdfunding",
           "b2b-finance": "B2B finance software", "remittance": "Remittances & FX", "banking-tech": "Banking software", "crypto": "Crypto"},
    "fr": {"payments": "Paiements", "wallet": "Portefeuille mobile", "gateway": "Passerelle de paiement", "infrastructure": "Infrastructure de paiement",
           "lending": "Crédit et microfinance", "insurtech": "Insurtech", "regtech": "RegTech", "crowdfunding": "Financement participatif",
           "b2b-finance": "Logiciels financiers B2B", "remittance": "Transferts et change", "banking-tech": "Logiciels bancaires", "crypto": "Crypto"},
}
DIR_STATUS = {
    "en": {"active": "Active", "acquired": "Acquired", "inactive": "Inactive", "unclear": "Status unclear"},
    "fr": {"active": "Active", "acquired": "Rachetée", "inactive": "Inactive", "unclear": "Statut incertain"},
}
REG_STATUS = {
    "en": {"in_force": "In force", "adopted_not_in_force": "Adopted, not yet in force", "in_parliament": "In parliament",
           "draft": "Draft", "announced": "Announced", "repealed": "Repealed", "replaced": "Replaced", "unclear": "Status unclear"},
    "fr": {"in_force": "En vigueur", "adopted_not_in_force": "Adopté, pas encore en vigueur", "in_parliament": "Au Parlement",
           "draft": "Projet", "announced": "Annoncé", "repealed": "Abrogé", "replaced": "Remplacé", "unclear": "Statut incertain"},
}
REG_GROUP = {  # filter groups
    "in_force": "force", "adopted_not_in_force": "pending", "in_parliament": "pending", "draft": "pending",
    "announced": "pending", "repealed": "past", "replaced": "past", "unclear": "unclear",
}
REG_TYPE = {
    "en": {"law": "Law", "decree": "Decree", "decree-law": "Decree-law", "bct-circular": "BCT circular", "cmf-regulation": "CMF regulation",
           "bill": "Bill", "strategy": "Strategy", "other": "Other"},
    "fr": {"law": "Loi", "decree": "Décret", "decree-law": "Décret-loi", "bct-circular": "Circulaire BCT", "cmf-regulation": "Règlement CMF",
           "bill": "Projet de loi", "strategy": "Stratégie", "other": "Autre"},
}
REG_TOPIC = {
    "en": {"payments": "Payments", "kyc": "KYC / AML", "fx": "Foreign exchange", "crypto": "Crypto", "crowdfunding": "Crowdfunding",
           "data": "Data protection", "startups": "Startups", "labour": "Labour", "cyber": "Cybersecurity", "cash": "Cash",
           "insurance": "Insurance", "banking": "Banking"},
    "fr": {"payments": "Paiements", "kyc": "KYC / LBC", "fx": "Change", "crypto": "Crypto", "crowdfunding": "Crowdfunding",
           "data": "Données personnelles", "startups": "Startups", "labour": "Travail", "cyber": "Cybersécurité", "cash": "Espèces",
           "insurance": "Assurance", "banking": "Banque"},
}

X = {
    "en": {
        "dir_title": "Tunisian Fintech Directory: 2026 Company List",
        "dir_h1": "Tunisian fintech directory",
        "dir_desc": "Who's who in Tunisian fintech: wallets, payment institutions, gateways, lenders, insurtechs and banking software, with licences, funding and sources.",
        "dir_lead": "The companies behind fintech in Tunisia, with what each one does, its licences, disclosed funding and the sources we used. Listings are free and independent.",
        "dir_search": "Search companies…", "all": "All", "companies": "companies", "founded": "Founded", "hq": "Headquarters",
        "website": "Website", "category": "Category", "status": "Status", "licences": "Licences and registrations",
        "funding": "Disclosed funding", "people": "People", "products": "Products and services", "about_co": "About",
        "date": "Date", "round": "Round", "amount": "Amount", "investors": "Investors", "undisclosed": "Undisclosed",
        "no_licence": "No licence or registration found in public sources.", "no_funding": "No disclosed funding rounds.",
        "in_articles": "Covered in", "last_verified": "Last verified", "fix": "Spotted an error or outdated information?",
        "fix_link": "Send a correction", "dir_crumb": "Directory", "view": "View profile",
        "dir_note": "Listings are compiled from public sources. Inclusion is free and never paid. Companies can ask for corrections.",
        "mentioned": "Companies in this article",
        "reg_title": "Tunisia Fintech Regulation Tracker (2026)",
        "reg_h1": "Fintech regulation tracker",
        "reg_desc": "Every law, BCT circular, decree and bill that shapes fintech in Tunisia, with its status: in force, pending or in parliament. Updated regularly.",
        "reg_lead": "Laws, Central Bank circulars, decrees and bills that shape fintech in Tunisia, with their current status and links to the source text or report.",
        "reg_crumb": "Regulation tracker", "updated": "Updated", "pending": "Pending", "past": "Replaced or repealed",
        "in_force_from": "In force from", "replaces": "Replaces", "source": "Source", "read": "Read our analysis", "topics": "Topic",
        "texts": "texts", "reg_note": "This tracker is for information only and is not legal advice. Check the Official Journal (JORT) and the issuing authority for authoritative texts.",
        "tools": "Reference tools", "tools_sub": "Two resources we keep up to date.",
        "tool_dir": "Fintech directory", "tool_dir_t": "Wallets, payment institutions, lenders, insurtechs and banking software, with licences and funding.",
        "tool_reg": "Regulation tracker", "tool_reg_t": "Laws, BCT circulars and bills that affect fintech, and where each one stands.",
        "open": "Open", "all_topics": "All topics", "last_update": "Last update",
    },
    "fr": {
        "dir_title": "Annuaire des fintechs tunisiennes : la liste 2026",
        "dir_h1": "Annuaire des fintechs tunisiennes",
        "dir_desc": "Qui fait quoi dans la fintech tunisienne : wallets, établissements de paiement, passerelles, crédit, insurtech et logiciels bancaires, avec agréments et sources.",
        "dir_lead": "Les entreprises derrière la fintech en Tunisie : leur activité, leurs agréments, leurs levées de fonds publiques et les sources utilisées. Les fiches sont gratuites et indépendantes.",
        "dir_search": "Rechercher une entreprise…", "all": "Toutes", "companies": "entreprises", "founded": "Création", "hq": "Siège",
        "website": "Site web", "category": "Catégorie", "status": "Statut", "licences": "Agréments et enregistrements",
        "funding": "Levées de fonds publiques", "people": "Équipe", "products": "Produits et services", "about_co": "Présentation",
        "date": "Date", "round": "Tour", "amount": "Montant", "investors": "Investisseurs", "undisclosed": "Non communiqué",
        "no_licence": "Aucun agrément ni enregistrement trouvé dans les sources publiques.", "no_funding": "Aucune levée de fonds rendue publique.",
        "in_articles": "Dans nos articles", "last_verified": "Dernière vérification", "fix": "Une erreur ou une information dépassée ?",
        "fix_link": "Signaler une correction", "dir_crumb": "Annuaire", "view": "Voir la fiche",
        "dir_note": "Les fiches sont établies à partir de sources publiques. L'inscription est gratuite et jamais payante. Les entreprises peuvent demander des corrections.",
        "mentioned": "Entreprises citées",
        "reg_title": "Suivi de la réglementation fintech en Tunisie (2026)",
        "reg_h1": "Suivi de la réglementation fintech",
        "reg_desc": "Toutes les lois, circulaires BCT, décrets et projets de loi qui encadrent la fintech en Tunisie, avec leur statut : en vigueur, en attente ou au Parlement.",
        "reg_lead": "Lois, circulaires de la Banque centrale, décrets et projets de loi qui encadrent la fintech en Tunisie, avec leur statut actuel et un lien vers le texte ou sa couverture.",
        "reg_crumb": "Suivi réglementaire", "updated": "Mis à jour le", "pending": "En attente", "past": "Remplacés ou abrogés",
        "in_force_from": "En vigueur à partir de", "replaces": "Remplace", "source": "Source", "read": "Lire notre analyse", "topics": "Thème",
        "texts": "textes", "reg_note": "Ce suivi est fourni à titre d'information et ne constitue pas un conseil juridique. Seuls le JORT et l'autorité émettrice font foi.",
        "tools": "Outils de référence", "tools_sub": "Deux ressources que nous tenons à jour.",
        "tool_dir": "Annuaire fintech", "tool_dir_t": "Wallets, établissements de paiement, crédit, insurtech et logiciels bancaires, avec agréments et levées de fonds.",
        "tool_reg": "Suivi réglementaire", "tool_reg_t": "Lois, circulaires BCT et projets de loi qui touchent la fintech, et où en est chacun.",
        "open": "Ouvrir", "all_topics": "Tous les thèmes", "last_update": "Dernière mise à jour",
    },
}

ABOUT = {
    "en": {
        "title": "About Fintech Tunisia | Independent Fintech Publication",
        "desc": "Fintech Tunisia is an independent, bilingual publication based in Tunis covering fintech in Tunisia and Africa, with sourced reporting, a directory and programs.",
        "h1": "About Fintech Tunisia",
        "lead": "An independent publication based in Tunis that explains fintech in Tunisia and across Africa, in English and French.",
        "md": """## Who we are

Fintech Tunisia is an independent publication and community based in Tunis. We report on the companies, regulators, money flows and ideas shaping financial technology in Tunisia, and we follow what is happening across Africa because it often shows where Tunisia could go next.

We publish in **English and French** so that founders, bankers, investors, regulators, students, journalists and the Tunisian diaspora can all use the same reference.

## What we publish

- **Articles** on the ecosystem, regulation, payments, banking, financial inclusion, funding, startups and African fintech. Every article lists its sources.
- **[The fintech directory](DIR)**: profiles of the companies active in Tunisian fintech, with their licences and disclosed funding.
- **[The regulation tracker](REG)**: the laws, Central Bank circulars and bills that affect fintech, with their current status.

## Our programs

Beyond publishing, we run cohort-based **education programs** and an **incubation track** for early-stage fintech ideas. [Learn more about our programs](PROG).

When an article covers an organisation we work with through these programs, we say so in the article.

## How we work

Our standards for sourcing, fact-checking, independence and the use of AI tools are set out in our **[editorial policy](EDIT)**. When we get something wrong, we fix it and log the change on our **[corrections page](CORR)**.

## Contact

Write to us at **hello@fintechtunisia.com** or through the [contact form](CONTACT). We welcome story tips, corrections and partnership enquiries.""",
    },
    "fr": {
        "title": "À propos de Fintech Tunisia | Média fintech indépendant",
        "desc": "Fintech Tunisia est un média indépendant et bilingue basé à Tunis qui couvre la fintech en Tunisie et en Afrique : articles sourcés, annuaire et programmes.",
        "h1": "À propos de Fintech Tunisia",
        "lead": "Un média indépendant basé à Tunis qui décrypte la fintech en Tunisie et en Afrique, en français et en anglais.",
        "md": """## Qui sommes-nous

Fintech Tunisia est un média et une communauté indépendants basés à Tunis. Nous couvrons les entreprises, les régulateurs, les flux financiers et les idées qui façonnent la technologie financière en Tunisie, et nous suivons ce qui se passe en Afrique, car le continent montre souvent la voie que la Tunisie pourrait prendre.

Nous publions en **français et en anglais** pour que fondateurs, banquiers, investisseurs, régulateurs, étudiants, journalistes et diaspora tunisienne disposent de la même référence.

## Ce que nous publions

- **Des articles** sur l'écosystème, la réglementation, les paiements, la banque, l'inclusion financière, le financement, les startups et la fintech africaine. Chaque article indique ses sources.
- **[L'annuaire fintech](DIR)** : les fiches des entreprises actives dans la fintech tunisienne, avec leurs agréments et leurs levées de fonds publiques.
- **[Le suivi réglementaire](REG)** : les lois, circulaires de la Banque centrale et projets de loi qui touchent la fintech, avec leur statut actuel.

## Nos programmes

Au-delà de l'information, nous proposons des **formations en cohorte** et un **parcours d'incubation** pour les projets fintech en amorçage. [Découvrir nos programmes](PROG).

Lorsqu'un article traite d'une organisation avec laquelle nous travaillons dans le cadre de ces programmes, nous le précisons dans l'article.

## Notre méthode

Nos règles en matière de sources, de vérification, d'indépendance et d'usage des outils d'IA sont décrites dans notre **[charte éditoriale](EDIT)**. Quand nous nous trompons, nous corrigeons et nous consignons la modification sur notre **[page des corrections](CORR)**.

## Contact

Écrivez-nous à **hello@fintechtunisia.com** ou via le [formulaire de contact](CONTACT). Informations, corrections et propositions de partenariat sont les bienvenues.""",
    },
}

EDITORIAL = {
    "en": {
        "title": "Editorial Policy | Fintech Tunisia",
        "desc": "How Fintech Tunisia sources, fact-checks, corrects and updates its reporting, how we use AI tools, and how we keep coverage independent from sponsors.",
        "h1": "Editorial policy",
        "lead": "How we research, check, correct and update what we publish.",
        "md": """## Sourcing

- We rely first on **primary sources**: laws published in the Official Journal (JORT), Central Bank of Tunisia (BCT) circulars and statistics, the Financial Market Council (CMF), World Bank data and company statements.
- We complement them with **reputable press**, local and international.
- **Every article lists its sources** at the end, with links.
- **Every figure is dated**, because numbers change. When sources disagree, we show both figures and say who published each one.
- **Company claims are attributed** to the company ("the company says") unless we could confirm them independently.

## Fact-checking

Before publication, each factual claim is checked against the source it cites. We do not publish invented numbers, unverifiable rumours or fabricated quotes. We only quote people when we can point to where they said it.

If something cannot be verified, we either say so plainly or leave it out.

## Use of AI tools

We use AI tools to help with research, drafting and translation between English and French. They do not replace verification: every article is checked against its cited sources before publication, and Fintech Tunisia is responsible for everything it publishes.

## Independence

- Companies **cannot pay** to be covered, to change an article or to appear in the directory.
- If we ever publish sponsored content, it will be clearly labelled as sponsored.
- Our [money transfer comparator](REMIT) may include referral links. If you sign up through one, we may earn a commission at no extra cost to you. Results are always ordered by the amount your recipient receives; a referral link never changes the order.
- When an article covers an organisation we work with through our programs, we disclose it in the article.

## Updates and corrections

Articles show their publication date. When we update an article with new information, we change the update date. When we correct an error, we fix the article and record the correction on our [corrections page](CORR).

To report an error, use the [contact form](CONTACT) and choose "Story tip / correction", or write to hello@fintechtunisia.com.

## Directory and regulation tracker

- **Directory listings** are compiled from public sources and are free. We include companies active in fintech in Tunisia that we can verify, and we mark a company's status as "unclear" when the public record is thin or contradictory. Companies can ask us to correct their listing; we change it when the correction is supported by evidence.
- **The regulation tracker** records texts and their status as reported by official or reputable sources. It is not legal advice.

## Not advice

Our content is for information only. It is not legal, financial or investment advice.""",
    },
    "fr": {
        "title": "Charte éditoriale | Fintech Tunisia",
        "desc": "Comment Fintech Tunisia choisit ses sources, vérifie, corrige et met à jour ses contenus, comment nous utilisons l'IA et comment nous restons indépendants.",
        "h1": "Charte éditoriale",
        "lead": "Comment nous recherchons, vérifions, corrigeons et mettons à jour ce que nous publions.",
        "md": """## Sources

- Nous nous appuyons d'abord sur les **sources primaires** : textes publiés au Journal officiel (JORT), circulaires et statistiques de la Banque centrale de Tunisie (BCT), Conseil du marché financier (CMF), données de la Banque mondiale et communiqués des entreprises.
- Nous les complétons par une **presse reconnue**, tunisienne et internationale.
- **Chaque article indique ses sources** en fin de page, avec des liens.
- **Chaque chiffre est daté**, car les chiffres évoluent. Lorsque les sources divergent, nous donnons les deux chiffres et précisons qui publie chacun.
- **Les affirmations d'une entreprise lui sont attribuées** (« selon l'entreprise ») lorsque nous n'avons pas pu les vérifier nous-mêmes.

## Vérification

Avant publication, chaque information factuelle est vérifiée au regard de la source citée. Nous ne publions ni chiffres inventés, ni rumeurs invérifiables, ni citations fabriquées. Nous ne citons une personne que si nous pouvons indiquer où elle l'a dit.

Lorsqu'une information ne peut pas être vérifiée, nous le disons clairement ou nous la retirons.

## Usage des outils d'IA

Nous utilisons des outils d'IA pour nous aider dans la recherche, la rédaction et la traduction entre le français et l'anglais. Ils ne remplacent pas la vérification : chaque article est contrôlé au regard de ses sources avant publication, et Fintech Tunisia est responsable de tout ce qu'il publie.

## Indépendance

- Une entreprise **ne peut pas payer** pour être couverte, pour faire modifier un article ou pour figurer dans l'annuaire.
- Si nous publions un jour un contenu sponsorisé, il sera clairement signalé comme tel.
- Notre [comparateur de transferts d'argent](REMIT) peut contenir des liens de parrainage. Si vous vous inscrivez par l'un d'eux, nous pouvons toucher une commission, sans surcoût pour vous. Les résultats sont toujours classés selon le montant reçu par votre bénéficiaire ; un lien de parrainage ne change jamais le classement.
- Lorsqu'un article traite d'une organisation avec laquelle nous travaillons dans le cadre de nos programmes, nous le mentionnons dans l'article.

## Mises à jour et corrections

Les articles affichent leur date de publication. Lorsque nous mettons à jour un article avec de nouvelles informations, nous modifions la date de mise à jour. Lorsque nous corrigeons une erreur, nous corrigeons l'article et consignons la correction sur notre [page des corrections](CORR).

Pour signaler une erreur, utilisez le [formulaire de contact](CONTACT) en choisissant « Information / correction », ou écrivez à hello@fintechtunisia.com.

## Annuaire et suivi réglementaire

- **Les fiches de l'annuaire** sont établies à partir de sources publiques et sont gratuites. Nous incluons les entreprises actives dans la fintech en Tunisie que nous pouvons vérifier, et nous indiquons un statut « incertain » lorsque les informations publiques sont minces ou contradictoires. Les entreprises peuvent demander une correction ; nous la faisons lorsqu'elle est étayée.
- **Le suivi réglementaire** recense les textes et leur statut tels que rapportés par des sources officielles ou fiables. Il ne constitue pas un conseil juridique.

## Pas de conseil

Nos contenus sont fournis à titre d'information. Ils ne constituent pas un conseil juridique, financier ou en investissement.""",
    },
}

CORRECTIONS = {
    "en": {
        "title": "Corrections | Fintech Tunisia",
        "desc": "Corrections and clarifications to Fintech Tunisia articles: what we got wrong, what we changed and when. Report an error through our contact form.",
        "h1": "Corrections",
        "lead": "When we get something wrong, we fix it and record it here.",
        "intro": "To report an error, use the [contact form](CONTACT) and choose \"Story tip / correction\", or write to hello@fintechtunisia.com. We review every request against the evidence. Minor fixes (typos, broken links) are not listed.",
        "log": "Corrections log",
        "items": [
            ("2026-10-10", "bolt-withdraws-tunisia", "An earlier version said TND 12 million had been seized from Bolt. The funds were seized from the accounts of several ride-hailing apps. We also removed a statement that Bolt intended to appeal, as we found no record of a formal appeal, and corrected the dollar conversion to about $3.8 million."),
            ("2026-10-10", "tunisia-startups-h1-2026-funding", "An earlier version presented the UAE ($591M) and Saudi ($102M) figures as first-half totals. They were second-quarter figures. The first-half totals are $1.2 billion and $259 million."),
            ("2026-10-10", "easybank-funding", "An earlier version described EasyBank as offering AI-based underwriting. EasyBank is a platform that helps people access loans and banking services; it is not a bank or a lender. We also replaced an unsourced account-ownership estimate with the World Bank Findex figure (37.8% in 2024) and removed unsourced card and mobile-money figures."),
            ("2026-10-10", "tunisia-zero-equity-deals-h1-2026", "An earlier version said Tunisia recorded zero equity deals in H1 2026. The source reported near-zero activity and cited one undisclosed investment, in RoboCare. We also removed two claims the source did not support."),
        ],
    },
    "fr": {
        "title": "Corrections et précisions | Fintech Tunisia",
        "desc": "Corrections et précisions apportées aux articles de Fintech Tunisia : ce qui était faux, ce que nous avons changé et quand. Signalez une erreur via le formulaire.",
        "h1": "Corrections",
        "lead": "Quand nous nous trompons, nous corrigeons et nous le consignons ici.",
        "intro": "Pour signaler une erreur, utilisez le [formulaire de contact](CONTACT) en choisissant « Information / correction », ou écrivez à hello@fintechtunisia.com. Chaque demande est examinée au regard des éléments fournis. Les corrections mineures (coquilles, liens cassés) ne sont pas listées.",
        "log": "Journal des corrections",
        "items": [
            ("2026-10-10", "bolt-withdraws-tunisia", "Une version précédente indiquait que 12 millions de dinars avaient été saisis chez Bolt. Les fonds ont été saisis sur les comptes de plusieurs applications de VTC. Nous avons aussi retiré l'affirmation selon laquelle Bolt comptait faire appel, faute de trace d'un recours formel, et corrigé la conversion en dollars (environ 3,8 millions)."),
            ("2026-10-10", "tunisia-startups-h1-2026-funding", "Une version précédente présentait les chiffres des Émirats (591 M$) et de l'Arabie saoudite (102 M$) comme des totaux semestriels. Il s'agissait des chiffres du deuxième trimestre. Les totaux du premier semestre sont de 1,2 milliard et 259 millions de dollars."),
            ("2026-10-10", "easybank-funding", "Une version précédente décrivait EasyBank comme proposant une évaluation du crédit par IA. EasyBank est une plateforme qui aide à accéder au crédit et aux services bancaires ; ce n'est ni une banque ni un prêteur. Nous avons aussi remplacé une estimation non sourcée du taux de bancarisation par le chiffre Findex de la Banque mondiale (37,8 % en 2024) et retiré des chiffres non sourcés sur les cartes et le mobile money."),
            ("2026-10-10", "tunisia-zero-equity-deals-h1-2026", "Une version précédente affirmait que la Tunisie n'avait enregistré aucune levée en fonds propres au premier semestre 2026. La source évoquait une activité quasi nulle et citait un investissement non communiqué, dans RoboCare. Nous avons aussi retiré deux affirmations non étayées par la source."),
        ],
    },
}
