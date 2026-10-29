#!/usr/bin/env python3
"""Generate the fully pre-rendered ICS production website from the approved build pack."""
from __future__ import annotations

import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "public"
ASSET_SOURCE = ROOT / "assets" / "source"
REFERENCE_HOME = ROOT.parent / "design-reference" / "index.html"
REFERENCE_INSIGHTS = ROOT.parent / "design-reference" / "insights.html"
REFERENCE_EFFECTS_CSS = ROOT.parent / "design-reference" / "assets" / "css" / "effects.css"
REFERENCE_EFFECTS_JS = ROOT.parent / "design-reference" / "assets" / "js" / "effects.js"
BASE_URL = "https://icsol.co.za"

CONTACT = {
    "streetAddress": "18 Ebony Road",
    "addressLocality": "Tokai",
    "addressRegion": "Cape Town",
    "postalCode": "7945",
    "email": "admin@icsol.co.za",
    "capeTown": "082 921 9965",
    "johannesburg": "079 103 2490",
    "linkedin": "https://www.linkedin.com/company/intrinsic-consulting-sa",
}

SERVICES = [
    ("hr-strategy", "Strategy", "Human resource strategy", "We develop a human resource strategy that underpins your organisational strategic goals and objectives, so your people plan and your business plan pull in the same direction.", "Mark Meredith", None),
    ("contracts-and-policies", "Compliance", "Contracts and policies", "Employment contracts, a disciplinary code and the policies you're legally expected to have, written for how your business actually runs.", "Marianne Steyn", "/insights/year-end-closedown/"),
    ("discipline-and-ccma", "Employee relations", "Discipline and the CCMA", "Warnings, hearings and grievances handled by the book, so a dismissal stands up if it's challenged. Representation when it gets that far.", "Caron Webb", "/insights/first-disciplinary-hearing-ccma/"),
    ("structure-culture-od", "Structure", "Structure, culture and organisational development", "Org structures, job descriptions and development work that turn your strategy into clear roles and build the culture you want as you grow.", "Mark Meredith", None),
    ("performance-and-incentives", "Performance", "Reviews and incentives", "A performance review framework and incentives linked to outcomes, so pay rewards the results that matter to you.", "Mark Meredith", None),
    ("workforce-planning", "Planning", "Workforce planning", "Which roles you'll need, when, and whether to hire, develop or contract, decided before growth forces a rushed hire.", "Mark Meredith", None),
    ("training-and-facilitation", "Development", "Training and facilitation", "Customised training for supervisors and teams, and facilitated sessions to carry people through change: restructures, new managers, new systems.", "Marianne Steyn", None),
    ("recruitment", "Supporting service", "Recruitment", "Executive search, and permanent and contract placements, from the same team that wrote the job description.", "Barbara Henshilwood", None),
]

ARTICLE_ROUTES = {
    "year-end": "/insights/year-end-closedown/",
    "ai-popia": "/insights/ai-at-work-popia/",
    "ccma-hearing": "/insights/first-disciplinary-hearing-ccma/",
    "hr-manager": "/insights/do-you-need-an-hr-manager/",
}

ARTICLE_META = {
    "year-end": ("Year-end closedown: leave, public holidays and pay over December", "Compliance · 5 min read"),
    "ai-popia": ("AI at work: what POPIA means for your business", "AI & the workplace · 6 min read"),
    "ccma-hearing": ("Your first disciplinary hearing: what the CCMA will look for", "Employee relations · 6 min read"),
    "hr-manager": ("Do you need an HR manager yet? A guide by headcount", "Growing a team · 4 min read"),
}

ROUTES = [
    ("/", "Home"),
    ("/hr-health-check/", "HR Health Check"),
    ("/services/", "Services"),
    *[(f"/services/{slug}/", title) for slug, _, title, _, _, _ in SERVICES],
    ("/about/", "About and our people"),
    ("/insights/", "Insights"),
    ("/insights/year-end-closedown/", ARTICLE_META["year-end"][0]),
    ("/insights/ai-at-work-popia/", ARTICLE_META["ai-popia"][0]),
    ("/insights/first-disciplinary-hearing-ccma/", ARTICLE_META["ccma-hearing"][0]),
    ("/insights/do-you-need-an-hr-manager/", ARTICLE_META["hr-manager"][0]),
    ("/job-seekers/", "Job seekers"),
    ("/contact/", "Contact"),
    ("/privacy/", "Privacy"),
]


def compact(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def extract_section(document: str, section_id: str) -> str:
    match = re.search(rf'<section\b[^>]*\bid="{re.escape(section_id)}"[^>]*>.*?</section>', document, re.S)
    if not match:
        raise RuntimeError(f"Could not find section #{section_id} in approved reference")
    return match.group(0)


def extract_article(document: str, article_id: str) -> str:
    match = re.search(rf'<article\b[^>]*\bid="{re.escape(article_id)}"[^>]*>.*?</article>', document, re.S)
    if not match:
        raise RuntimeError(f"Could not find article #{article_id} in approved reference")
    article = match.group(0)
    article = re.sub(r'\s+hidden(?=[\s>])', "", article, count=1)
    article = article.replace('href="./#contact"', 'href="/hr-health-check/"')
    article = article.replace('href="#all"', 'href="/insights/"')
    return article


def picture(name: str, alt: str, width: int, height: int, loading: str = "lazy") -> str:
    stem = Path(name).stem
    suffix = Path(name).suffix
    webp = ASSET_SOURCE / f"{stem}.webp"
    source = f'<source srcset="/assets/img/{stem}.webp" type="image/webp">' if webp.exists() else ""
    return f'<picture>{source}<img src="/assets/img/{name}" alt="{alt}" width="{width}" height="{height}" loading="{loading}" decoding="async"></picture>'


def professional_schema() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "Intrinsic Consulting Solutions",
        "alternateName": "ICS",
        "url": BASE_URL,
        "image": f"{BASE_URL}/assets/img/hero-concept.jpg",
        "description": "Outsourced and fractional HR for South African small to medium-sized businesses.",
        "email": CONTACT["email"],
        "telephone": CONTACT["capeTown"],
        "sameAs": [CONTACT["linkedin"]],
        "foundingDate": "2017",
        "areaServed": ["Cape Town", "Johannesburg", "South Africa"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": CONTACT["streetAddress"],
            "addressLocality": CONTACT["addressLocality"],
            "addressRegion": CONTACT["addressRegion"],
            "postalCode": CONTACT["postalCode"],
            "addressCountry": "ZA",
        },
    }


def breadcrumb(path: str, name: str) -> dict:
    segments = [segment for segment in path.split("/") if segment]
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL + "/"}]
    running = ""
    for position, segment in enumerate(segments, start=2):
        running += f"/{segment}"
        items.append({"@type": "ListItem", "position": position, "name": name if position == len(segments) + 1 else segment.replace("-", " ").title(), "item": BASE_URL + running + "/"})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def shared_header(active: str = "") -> str:
    navigation = [
        ("How it works", "/hr-health-check/", "health"),
        ("Services", "/services/", "services"),
        ("Our people", "/about/", "about"),
        ("Insights", "/insights/", "insights"),
        ("Job seekers", "/job-seekers/", "jobs"),
    ]
    link_items = []
    for label, href, key in navigation:
        current = ' aria-current="page"' if key == active else ""
        link_items.append(f'<li><a href="{href}"{current}>{label}</a></li>')
    links = "".join(link_items)
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site"><div class="wrap">
  <a class="brand" href="/">{picture("ics-logo.png", "ICS logo", 360, 127, "eager")}<span><b>Intrinsic Consulting Solutions</b><small>Outsourced HR · Est. 2017</small></span></a>
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
  <nav class="main" id="nav" aria-label="Main"><ul>{links}<li><a class="btn btn-primary" href="/hr-health-check/">Book an HR Health Check</a></li></ul></nav>
</div></header>'''


def shared_footer() -> str:
    return f'''<footer class="site"><div class="wrap footer-grid">
  <div><strong>Intrinsic Consulting Solutions</strong><span>18 Ebony Road, Tokai, Cape Town, 7945</span><a href="mailto:{CONTACT['email']}">{CONTACT['email']}</a></div>
  <div><strong>Speak to us</strong><a href="tel:+27829219965">Cape Town: {CONTACT['capeTown']}</a><a href="tel:+27791032490">Johannesburg: {CONTACT['johannesburg']}</a></div>
  <div><strong>Explore</strong><a href="/services/">Services</a><a href="/insights/">Insights</a><a href="/privacy/">Privacy</a><a href="{CONTACT['linkedin']}" target="_blank" rel="noopener">LinkedIn</a></div>
  <div class="copyright">© 2026 Intrinsic Consulting Solutions. Outsourced HR, IR and recruitment.</div>
</div></footer>'''


def document(title: str, description: str, path: str, content: str, active: str = "", schemas: list[dict] | None = None) -> str:
    canonical = BASE_URL + path
    title_html = html.escape(title, quote=True)
    description_html = html.escape(description, quote=True)
    schema_list = [professional_schema()]
    if path != "/":
        schema_list.append(breadcrumb(path, title.split(" | ")[0]))
    if schemas:
        schema_list.extend(schemas)
    schema = json.dumps({"@context": "https://schema.org", "@graph": schema_list}, ensure_ascii=False)
    return f'''<!doctype html>
<html lang="en-ZA">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title_html}</title>
  <meta name="description" content="{description_html}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website"><meta property="og:site_name" content="Intrinsic Consulting Solutions">
  <meta property="og:title" content="{title_html}"><meta property="og:description" content="{description_html}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{BASE_URL}/assets/img/hero-concept.jpg">
  <meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title_html}"><meta name="twitter:description" content="{description_html}">
  <link rel="icon" href="/assets/img/ics-logo.png" type="image/png">
  <link rel="stylesheet" href="/assets/fonts/fonts.css"><link rel="stylesheet" href="/css/styles.css"><link rel="stylesheet" href="/css/effects.css">
  <script type="application/ld+json">{schema}</script>
</head>
<body>
{shared_header(active)}
<main id="main">{content}</main>
{shared_footer()}
<button class="chat-launcher" type="button" hidden aria-label="Open chat">Chat</button>
<div class="cookie-banner" role="dialog" aria-label="Privacy choices" aria-live="polite"><p>We use cookies for analytics and chat only if you accept. Read our <a href="/privacy/">POPIA privacy notice</a>.</p><div><button class="btn btn-ghost" type="button" data-consent="declined">Decline</button><button class="btn btn-primary" type="button" data-consent="accepted">Accept</button></div></div>
<script src="/site.config.js"></script><script src="/js/effects.js" defer></script><script src="/js/app.js" defer></script>
</body></html>'''


def services_grid() -> str:
    cards = []
    for slug, category, title, intro, _, _ in SERVICES:
        cards.append(f'''<article><a class="service-card-link" href="/services/{slug}/" aria-label="{title}"><span class="k">{category}</span><h3>{title}</h3><p>{intro}</p></a></article>''')
    return '<div class="svc">' + "".join(cards) + "</div>"


def rewrite_reference_assets(content: str) -> str:
    content = content.replace('src="assets/img/', 'src="/assets/img/').replace('url("assets/img/', 'url("/assets/img/')
    return content.replace('src="/assets/img/team/', 'src="/assets/img/')


def lead_form_markup(content: str, form_name: str = "hr_health_check") -> str:
    content = content.replace('<form class="check" id="check-form" novalidate>', f'<form class="check lead-form" id="check-form" data-lead-form data-form-name="{form_name}" novalidate>')
    content = content.replace('<form id="magnet-form" novalidate>', '<form id="magnet-form" data-lead-form data-form-name="checklist" data-endpoint="checklist" novalidate>')
    for field_id, name in [("f-name", "name"), ("f-company", "business_name"), ("f-email", "email"), ("f-phone", "phone"), ("f-size", "number_of_employees"), ("f-need", "main_reason"), ("f-msg", "message"), ("f-consent", "consent"), ("mag-email", "email")]:
        content = content.replace(f'id="{field_id}"', f'id="{field_id}" name="{name}"')
    content = content.replace('ICS POPIA privacy notice', '<a href="/privacy/">ICS POPIA privacy notice</a>')
    content = re.sub(r'<p id="form-err"[^>]*></p>', '<p data-form-message role="status" hidden></p>', content)
    content = re.sub(r'<div class="form-ok" id="form-ok" hidden>.*?</div>', '', content, flags=re.S)
    content = content.replace('<p id="mag-msg" hidden', '<p data-form-message role="status" hidden')
    content = content.replace('<button class="btn btn-primary" type="submit">Book an HR Health Check</button>', '<input class="honeypot" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true"><button class="btn btn-primary" type="submit">Book an HR Health Check</button>')
    content = content.replace('<button class="btn btn-primary" type="submit">Send me the checklist</button>', '<input class="honeypot" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true"><button class="btn btn-primary" type="submit">Send me the checklist</button>')
    return content


def home_page(reference: str) -> str:
    main_match = re.search(r'<main id="top">(.*?)</main>', reference, re.S)
    if not main_match:
        raise RuntimeError("Could not read approved homepage main content")
    content = main_match.group(1)
    content = re.sub(r'<section\b[^>]*\bid="clients"[^>]*>.*?</section>', '', content, flags=re.S)
    content = re.sub(r'<section\b[^>]*\bid="services"[^>]*>.*?</section>', f'''<section class="band" id="services"><div class="wrap"><div class="svc-head"><div><p class="eyebrow">What your HR person handles</p><h2 style="margin-top:12px">One person on your team. A full HR function behind them.</h2></div><p class="lede">Outsourced or fractional, you deal with one HR executive who knows your business. When something needs a specialist, they bring in a colleague from the ICS team.</p></div>{services_grid()}</div></section>''', content, flags=re.S)
    closing = '''<section class="band steps-band closing-cta"><div class="wrap"><p class="eyebrow">Book an HR Health Check</p><h2 style="margin-top:12px">Find out where your business stands.</h2><p class="lede">Tell us a little about your business. We'll call you back within one business day to set up your health check.</p><p class="steps-cta"><a class="btn btn-primary" href="/hr-health-check/">Book an HR Health Check</a><span>The questionnaire takes about 5 minutes. Results in about 2 days.</span></p></div></section>'''
    content = re.sub(r'<section\b[^>]*\bid="contact"[^>]*>.*?</section>', closing, content, flags=re.S)
    replacements = {
        'href="#contact"': 'href="/hr-health-check/"',
        'href="#careers"': 'href="/job-seekers/"',
        'href="insights.html#year-end"': 'href="/insights/year-end-closedown/"',
        'href="insights.html#ai-popia"': 'href="/insights/ai-at-work-popia/"',
        'href="insights.html#ccma-hearing"': 'href="/insights/first-disciplinary-hearing-ccma/"',
        'href="insights.html"': 'href="/insights/"',
    }
    for original, replacement in replacements.items():
        content = content.replace(original, replacement)
    content = rewrite_reference_assets(content)
    content = lead_form_markup(content)
    return content


def health_check_page(reference: str) -> str:
    steps = extract_section(reference, "how")
    size = extract_section(reference, "size")
    contact = extract_section(reference, "contact")
    faq = extract_section(reference, "faq")
    steps = steps.replace('href="#contact"', 'href="#booking-form"')
    size = rewrite_reference_assets(size)
    contact = lead_form_markup(rewrite_reference_assets(contact))
    contact = contact.replace('id="contact"', 'id="booking-form"')
    return f'''<section class="page-hero"><div class="wrap"><p class="eyebrow">Book an HR Health Check</p><h1>Start with a health check. Decide from there.</h1><p class="lede">No long contract up front. We look at where your business stands first, then agree what level of support makes sense.</p></div></section>{steps}{size}{contact}{faq}'''


def services_page() -> str:
    corporate = '''<section class="band corp"><div class="wrap corp-grid"><div><p class="eyebrow">Already have an HR team?</p><h2 style="margin-top:12px">We take the project work off your desk.</h2><p class="lede">Corporate HR managers bring us in for the work that never gets done between day-to-day queries. Fixed scope, fixed fee, delivered to your standards.</p></div><div class="chips" aria-label="Typical corporate projects"><span>HR strategy</span><span>Workforce planning</span><span>Job description libraries</span><span>Organisational design</span><span>Performance frameworks</span><span>Competency frameworks</span><span>Policy reviews</span><span>Change management</span><span>Incentive design</span><span>Recruitment and executive search</span></div></div></section>'''
    return f'''<section class="page-hero"><div class="wrap"><p class="eyebrow">What your HR person handles</p><h1>One person on your team. A full HR function behind them.</h1><p class="lede">Outsourced or fractional, you deal with one HR executive who knows your business. When something needs a specialist, they bring in a colleague from the ICS team.</p></div></section><section class="band"><div class="wrap">{services_grid()}</div></section>{corporate}<section class="band closing-cta"><div class="wrap"><a class="btn btn-primary" href="/hr-health-check/">Book an HR Health Check</a></div></section>'''


def service_page(service: tuple[str, str, str, str, str, str | None]) -> str:
    slug, category, title, intro, lead, related = service
    related_markup = f'<p><a class="btn btn-ghost" href="{related}">Read the related Insight</a></p>' if related else ""
    return f'''<section class="page-hero"><div class="wrap"><p class="eyebrow">{category}</p><h1>{title}</h1><p class="lede">{intro}</p></div></section>
<section class="band"><div class="wrap service-detail"><div><p class="eyebrow">What's included</p><div class="review-note">[NEW COPY: for 247 review]</div></div><div><p class="eyebrow">Who it's for</p><div class="review-note">[NEW COPY: for 247 review]</div></div><aside class="service-team"><p class="eyebrow">Your ICS lead</p><h2>{lead}</h2><p><a href="/about/">Meet our people</a></p>{related_markup}</aside></div></section>
<section class="band steps-band closing-cta"><div class="wrap"><h2>Start with a health check. Decide from there.</h2><p class="steps-cta"><a class="btn btn-primary" href="/hr-health-check/">Book an HR Health Check</a><span>The questionnaire takes about 5 minutes. Results in about 2 days.</span></p></div></section>'''


def about_page(reference: str) -> str:
    team = rewrite_reference_assets(extract_section(reference, "team"))
    person_schema = [{"@context": "https://schema.org", "@type": "Person", "name": name, "worksFor": {"@type": "Organization", "name": "Intrinsic Consulting Solutions"}} for name in ["Barbara Henshilwood", "Mark Meredith", "Marianne Steyn", "Caron Webb"]]
    content = f'''<section class="page-hero"><div class="wrap"><p class="eyebrow">About ICS</p><h1>Outsourced and fractional HR for South African small to medium-sized businesses.</h1><p class="lede">[NEW COPY: for 247 review] ICS has supported businesses since 2017.</p></div></section>
<div class="proof"><div class="wrap"><div><strong>Since 2017</strong><span>Cape Town head office, Johannesburg presence</span></div><div><strong>4 HR executives</strong><span>Each with 20+ years in HR, IR or labour law</span></div><div><strong>CCMA-tested</strong><span>Disciplinaries, grievances and representation</span></div><div><strong>Global depth</strong><span>Experience with brands like Coca-Cola, DHL and Toyota</span></div></div></div>{team}<section class="band steps-band closing-cta"><div class="wrap"><a class="btn btn-primary" href="/hr-health-check/">Book an HR Health Check</a></div></section>'''
    return content, person_schema


def insight_cards() -> str:
    return '''<section class="band ins-index"><div class="wrap"><div class="filters" role="group" aria-label="Filter by topic"><button type="button" class="chip on" data-filter="all">All topics</button><button type="button" class="chip" data-filter="compliance">Compliance</button><button type="button" class="chip" data-filter="er">Employee relations</button><button type="button" class="chip" data-filter="growing">Growing a team</button><button type="button" class="chip" data-filter="ai">AI &amp; the workplace</button></div><a class="feature" href="/insights/year-end-closedown/" data-category="compliance"><div class="feature-art" aria-hidden="true"><span>DEC</span><b>16 · 25 · 26</b><span>JAN 1</span></div><div class="feature-body"><span class="meta">Compliance · 5 min read · Featured</span><h2>Year-end closedown: leave, public holidays and pay over December</h2><p>Shutdown leave, the Day of Goodwill falling on a Saturday, and who gets paid what if they work on the 16th. A practical checklist for the next six weeks.</p><span class="more">Read the article</span></div></a><div class="cards"><a class="card" href="/insights/ai-at-work-popia/" data-category="ai"><span class="meta">AI &amp; the workplace · 6 min</span><h3>AI at work: what POPIA means for your business</h3><p>Staff pasting client details into chatbots, smart glasses in meetings, AI screening CVs. The law hasn't changed. The risks have.</p><span class="more">Read the article</span></a><a class="card" href="/insights/first-disciplinary-hearing-ccma/" data-category="er"><span class="meta">Employee relations · 6 min</span><h3>Your first disciplinary hearing: what the CCMA will look for</h3><p>A fair reason and a fair process. The steps owners skip most often, and why skipping them costs more than the hearing.</p><span class="more">Read the article</span></a><a class="card" href="/insights/do-you-need-an-hr-manager/" data-category="growing"><span class="meta">Growing a team · 4 min</span><h3>Do you need an HR manager yet? A guide by headcount</h3><p>What changes at 10, 25 and 50 employees, and the point at which DIY HR starts costing more than it saves.</p><span class="more">Read the article</span></a><div class="card soon" data-category="compliance"><span class="meta">Compliance · Coming soon</span><h3>Employment contracts: the clauses most small business contracts are missing</h3><p>Probation, restraint of trade, remote work and POPIA consent. What to check in the contracts you already have.</p></div><div class="card soon" data-category="compliance"><span class="meta">Compliance · Coming soon</span><h3>What's changing in South African labour law</h3><p>A plain-English round-up of recent and upcoming changes, and what each one means for a business with 5 to 50 people.</p></div></div><p class="empty" data-filter-empty hidden>No articles in this topic yet.</p></div></section>'''


def magnet() -> str:
    return '''<section class="band magnet-band"><div class="wrap"><div class="magnet"><div><h2>The small business HR compliance checklist</h2><p>Twenty questions to check your contracts, policies and records against the BCEA, LRA, EEA and POPIA. Free download.</p></div><form data-lead-form data-form-name="checklist" data-endpoint="checklist" novalidate><label for="checklist-email" class="sr-only">Work email</label><input id="checklist-email" name="email" type="email" placeholder="Your work email" required autocomplete="email"><input class="honeypot" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true"><button class="btn btn-primary" type="submit">Send me the checklist</button><p data-form-message role="status" hidden></p></form></div></div></section>'''


def insights_page() -> str:
    return f'''<section class="ins-hero"><div class="wrap"><p class="eyebrow">Insights</p><h1>Plain-English HR for South African business owners.</h1><p class="lede">Practical guidance on the people side of running a small or medium business: what the law expects, what goes wrong, and what to do about it.</p></div></section>{insight_cards()}{magnet()}'''


def article_page(reference: str, article_id: str) -> tuple[str, dict]:
    title, meta = ARTICLE_META[article_id]
    article = extract_article(reference, article_id)
    article = article.replace('class="band post-view"', 'class="band post-view article-page"')
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "author": {"@type": "Organization", "name": "Intrinsic Consulting Solutions"},
        "publisher": {"@type": "Organization", "name": "Intrinsic Consulting Solutions"},
        "mainEntityOfPage": BASE_URL + ARTICLE_ROUTES[article_id],
    }
    return f'''<section class="ins-hero compact-hero"><div class="wrap"><p class="eyebrow">Insights</p><p class="lede">{meta}</p></div></section>{article}{magnet()}''', schema


def job_seekers_page() -> str:
    return '''<section class="page-hero"><div class="wrap"><p class="eyebrow">Job seekers</p><h1>Looking for your next role?</h1><p class="lede">We still recruit for skilled and professional positions across South Africa.</p></div></section><section class="careers"><div class="wrap"><p><b>Looking for your next role?</b> We still recruit for skilled and professional positions across South Africa.</p><a class="btn btn-ghost" data-vacancies-link href="/contact/">Search current vacancies</a></div></section><section class="band"><div class="wrap vacancies"><p class="review-note">[NEW COPY: for 247 review] The Placement Partners vacancies feed is being connected.</p></div></section><section class="band steps-band closing-cta"><div class="wrap"><a class="btn btn-primary" href="/hr-health-check/">Book an HR Health Check</a></div></section>'''


def contact_page(reference: str) -> str:
    contact = extract_section(reference, "contact")
    contact = lead_form_markup(rewrite_reference_assets(contact))
    contact = contact.replace('id="contact"', 'id="contact-details"')
    map_url = "https://www.google.com/maps?q=18+Ebony+Road,+Tokai,+Cape+Town,+7945&output=embed"
    return f'''<section class="page-hero"><div class="wrap"><p class="eyebrow">Contact</p><h1>Find out where your business stands.</h1><p class="lede">Tell us a little about your business. We'll call you back within one business day to set up your health check.</p></div></section>{contact}<section class="band map-band"><div class="wrap"><iframe title="ICS head office at 18 Ebony Road, Tokai" loading="lazy" src="{map_url}"></iframe></div></section>'''


def privacy_page() -> str:
    return '''<section class="page-hero"><div class="wrap"><p class="eyebrow">Privacy</p><h1>POPIA privacy notice</h1><p class="lede">[NEW COPY: for 247 review] ICS to supply, or 247 to draft for ICS approval.</p></div></section><section class="band"><div class="wrap read"><div class="review-note">[NEW COPY: for 247 review]</div><p>This page must be completed and approved before the website collects personal information through any live form.</p></div></section>'''


def faq_schema() -> dict:
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": "How is this different from an HR software subscription?", "acceptedAnswer": {"@type": "Answer", "text": "Software stores records and generates templates. It can't run a disciplinary hearing, coach a new manager or tell you whether a dismissal will hold."}},
        {"@type": "Question", "name": "Are we locked into a long contract?", "acceptedAnswer": {"@type": "Answer", "text": "No. Retainers run month to month. Start with the health check, and continue only if the support is earning its keep."}},
    ]}


def write_route(path: str, data: str) -> None:
    if path == "/":
        target = OUT / "index.html"
    else:
        target = OUT / path.strip("/") / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(re.sub(r"[ \t]+(?=\n)", "", data), encoding="utf-8")


def write_support_files() -> None:
    (OUT / "css").mkdir(parents=True, exist_ok=True)
    (OUT / "js").mkdir(parents=True, exist_ok=True)
    styles = re.search(r'<style>(.*?)</style>', REFERENCE_HOME.read_text(encoding="utf-8"), re.S).group(1)
    styles = styles.replace('url("assets/img/hero-concept.jpg")', 'image-set(url("/assets/img/hero-concept.webp") type("image/webp"), url("/assets/img/hero-concept.jpg") type("image/jpeg"))')
    additions = '''
/* Production additions: route layouts, consent UI and accessibility. */
.skip-link{position:absolute;left:16px;top:-80px;z-index:200;background:var(--ochre);color:var(--on-accent);padding:10px 14px;border-radius:var(--r);font-weight:700}.skip-link:focus{top:12px}
.sr-only{position:absolute!important;width:1px!important;height:1px!important;padding:0!important;margin:-1px!important;overflow:hidden!important;clip:rect(0,0,0,0)!important;white-space:nowrap!important;border:0!important}
.page-hero{background:var(--band);color:var(--band-fg);padding-block:clamp(56px,9vw,110px)}.page-hero .eyebrow{color:var(--ochre)}.page-hero h1{margin-top:12px;max-width:25ch}.page-hero .lede{color:var(--band-soft);margin-top:18px}
.footer-grid{display:grid!important;grid-template-columns:repeat(3,1fr) 1.2fr;align-items:start}.footer-grid>div{display:grid;gap:4px}.footer-grid strong{color:var(--band-fg)}.footer-grid .copyright{align-self:end}@media(max-width:760px){.footer-grid{grid-template-columns:1fr 1fr!important}.footer-grid .copyright{grid-column:1/-1}}
.service-card-link{display:grid;gap:10px;align-content:start;color:inherit;text-decoration:none;min-height:100%}.service-card-link .more{font-weight:600;text-decoration:underline;text-decoration-color:var(--ochre);text-underline-offset:4px}.service-detail{display:grid;grid-template-columns:1fr 1fr;gap:40px}.service-team{grid-column:1/-1;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:26px}.service-team h2{margin-top:8px}.review-note{display:inline-block;background:var(--ochre-wash);color:var(--ochre-ink);padding:8px 10px;border-radius:var(--r);font-family:var(--f-mono);font-size:.82rem;line-height:1.4}.closing-cta{text-align:center}.closing-cta .steps-cta{justify-content:center}.honeypot{position:absolute!important;left:-10000px!important;width:1px!important;height:1px!important;opacity:0!important}.lead-form [data-form-message][data-state="error"]{color:#b3261e}.lead-form [data-form-message][data-state="success"]{background:var(--ochre-wash);padding:12px;border-radius:var(--r);color:var(--ok)}
.ins-hero{background:var(--band);color:var(--band-fg);padding-block:clamp(48px,7vw,88px)}.ins-hero .eyebrow{color:var(--ochre)}.ins-hero h1{margin-top:12px;max-width:20ch}.ins-hero .lede{color:var(--band-soft);margin-top:16px}.compact-hero{padding-block:32px}.filters{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:32px}.chip{font:inherit;font-size:.92rem;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;padding:8px 16px;cursor:pointer}.chip.on{background:var(--band);border-color:var(--band);color:var(--band-fg)}.feature{display:grid;grid-template-columns:.8fr 1.2fr;border:1px solid var(--line);border-radius:10px;overflow:hidden;text-decoration:none;color:inherit;background:var(--surface);margin-bottom:28px}.feature-art{background:var(--band);color:var(--band-fg);display:grid;place-content:center;gap:6px;text-align:center;padding:40px 20px;font-family:var(--f-mono);letter-spacing:.14em;font-size:.8rem}.feature-art b{font-family:var(--f-display);font-weight:400;font-size:clamp(2rem,4vw,3rem);letter-spacing:0;color:var(--ochre)}.feature-body{padding:clamp(22px,3vw,36px);display:grid;gap:12px;align-content:center}.feature-body h2{font-size:clamp(1.5rem,2.6vw,2rem)}.feature-body p,.card p{color:var(--ink-soft)}.meta{font-family:var(--f-mono);font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;color:var(--ochre-ink)}.more{font-weight:600;text-decoration:underline;text-decoration-color:var(--ochre);text-underline-offset:4px}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}.card{display:grid;gap:10px;align-content:start;padding:22px;border:1px solid var(--line);border-radius:10px;background:var(--surface);text-decoration:none;color:inherit}.card.soon{background:transparent;border-style:dashed}.card.soon .meta{color:var(--ink-soft)}.read{max-width:760px}.back{display:inline-block;margin-bottom:24px;font-weight:600;text-decoration:none;color:var(--ochre-ink)}.read h1{font-size:clamp(2rem,4vw,2.9rem);margin-top:10px}.standfirst{font-size:1.2rem;color:var(--ink-soft);margin-top:18px;padding-bottom:24px;border-bottom:1px solid var(--line)}.read h2{font-size:1.45rem;margin-top:36px;margin-bottom:10px}.read p+p{margin-top:14px}.read ul,.read ol{padding-left:1.2em;display:grid;gap:8px;margin:12px 0}.dates{width:100%;border-collapse:collapse;margin:12px 0 16px;font-variant-numeric:tabular-nums}.dates th,.dates td{text-align:left;padding:10px;border-bottom:1px solid var(--line)}.dates th{font-family:var(--f-mono);font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-soft);font-weight:500}.checklist{margin-top:36px;background:var(--ochre-wash);border-radius:10px;padding:24px}.checklist h3{font-size:1.25rem}.checklist ul{list-style:none;padding:0}.checklist li{padding-left:28px;position:relative}.checklist li::before{content:"";position:absolute;left:0;top:.35em;width:16px;height:16px;border:2px solid var(--ochre-ink);border-radius:3px}.post-cta{margin-top:36px;background:var(--band);color:var(--band-fg);border-radius:10px;padding:24px;display:flex;gap:20px;align-items:center;justify-content:space-between;flex-wrap:wrap}.post-cta>div{flex:1 1 300px;min-width:0}.post-cta p{color:var(--band-soft);margin-top:6px}.disclaimer{margin-top:24px;font-size:.85rem;color:var(--ink-soft)}.magnet-band{background:var(--surface);border-top:1px solid var(--line)}.magnet-band .magnet{margin-top:0}.map-band iframe{width:100%;min-height:420px;border:1px solid var(--line);border-radius:10px}.vacancies{max-width:760px}.cookie-banner{position:fixed;z-index:100;right:16px;bottom:16px;width:min(520px,calc(100% - 32px));display:flex;gap:16px;align-items:center;justify-content:space-between;flex-wrap:wrap;background:var(--surface);color:var(--ink);box-shadow:0 14px 40px rgba(29,23,77,.25);border:1px solid var(--line);border-radius:10px;padding:16px}.cookie-banner p{font-size:.9rem;max-width:36ch}.cookie-banner div{display:flex;gap:8px}.chat-launcher{position:fixed;right:20px;bottom:20px;z-index:80;border:0;border-radius:999px;background:var(--ochre);color:var(--on-accent);padding:12px 18px;font:600 1rem var(--f-body);box-shadow:0 8px 24px rgba(29,23,77,.25);cursor:pointer}.cookie-banner[hidden]~.chat-launcher{bottom:20px}@media(max-width:900px){.feature{grid-template-columns:1fr}.cards{grid-template-columns:1fr 1fr}.service-detail{grid-template-columns:1fr}.service-team{grid-column:auto}}@media(max-width:560px){.cards{grid-template-columns:1fr}.cookie-banner{left:16px;right:16px;width:auto}.cookie-banner .btn{padding:.7em 1em}}
'''
    (OUT / "css" / "styles.css").write_text(styles + additions, encoding="utf-8")
    shutil.copy2(REFERENCE_EFFECTS_CSS, OUT / "css" / "effects.css")
    shutil.copy2(REFERENCE_EFFECTS_JS, OUT / "js" / "effects.js")
    shutil.copy2(ROOT / "src" / "app.js", OUT / "js" / "app.js")
    shutil.copy2(ROOT / "site.config.js", OUT / "site.config.js")
    shutil.copytree(ASSET_SOURCE, OUT / "assets" / "img", dirs_exist_ok=True)
    shutil.copytree(ROOT / "assets" / "fonts", OUT / "assets" / "fonts", dirs_exist_ok=True)
    (OUT / "manus-routes.json").write_text(json.dumps({"routes": [{"path": path, "title": title} for path, title in ROUTES]}, indent=2), encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n", encoding="utf-8")
    sitemap_entries = "\n".join(f"  <url><loc>{BASE_URL}{path}</loc></url>" for path, _ in ROUTES)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap_entries}\n</urlset>\n', encoding="utf-8")
    llms = "# Intrinsic Consulting Solutions\n\nOutsourced and fractional HR for South African small to medium-sized businesses.\n\n" + "\n".join(f"- {BASE_URL}{path}: {title}" for path, title in ROUTES) + "\n"
    (OUT / "llms.txt").write_text(llms, encoding="utf-8")
    redirects = """old_path,new_path,status,note
/about-us/,/about/,301,Legacy company page
/our-people/,/about/,301,Legacy team page
/contact/,/contact/,301,Legacy contact page
/popi/,/privacy/,301,Legacy POPI policy
/email-terms-and-conditions/,/privacy/,301,Legacy privacy and terms page
/submit-your-cv/,/job-seekers/,301,Legacy candidate submission page
/job-search/,/job-seekers/,301,Legacy job search page
/news/,/insights/,301,Legacy news index
/demystifying-the-recruitment-process/,/insights/,301,Legacy recruitment article
/whats-available-out-there/,/insights/,301,Legacy recruitment article
/understanding-an-advert/,/insights/,301,Legacy recruitment article
/do-i-do-this-myself-or-should-i-get-help/,/insights/,301,Legacy recruitment article
/competency-based-hr-decision-making/,/insights/,301,Legacy recruitment article
/category/uncategorised/,/insights/,301,Legacy article archive
/category/news/,/insights/,301,Legacy article archive
/category/interviews/,/insights/,301,Legacy article archive
/category/other/,/insights/,301,Legacy article archive
/category/the-recruitment-process/,/insights/,301,Legacy article archive
/tag/hiring/,/insights/,301,Legacy article tag
/tag/selection/,/insights/,301,Legacy article tag
/tag/recruitment/,/insights/,301,Legacy article tag
/tag/competency/,/insights/,301,Legacy article tag
/tag/employment/,/insights/,301,Legacy article tag
/thanks/,/,301,Legacy form confirmation
/test/,/,301,Legacy test page
/services,/services/,301,Legacy service alias
/jobs,/job-seekers/,301,Legacy jobs alias
/vacancies,/job-seekers/,301,Legacy vacancies alias
"""
    (ROOT / "redirects.csv").write_text(redirects, encoding="utf-8")


def main() -> None:
    reference_home = REFERENCE_HOME.read_text(encoding="utf-8")
    reference_insights = REFERENCE_INSIGHTS.read_text(encoding="utf-8")
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    write_support_files()

    home = home_page(reference_home)
    write_route("/", document("Outsourced & Fractional HR for SA Businesses | ICS", "Outsourced and fractional HR for South African small to medium-sized businesses.", "/", home, "", [faq_schema()]))
    write_route("/hr-health-check/", document("HR Health Check | Outsourced HR | ICS", "Start with a five-minute HR Health Check and receive a written report in about two days.", "/hr-health-check/", health_check_page(reference_home), "health", [faq_schema()]))
    write_route("/services/", document("HR Services | Outsourced HR | ICS", "HR strategy, compliance, employee relations, recruitment and more from ICS.", "/services/", services_page(), "services"))
    for service in SERVICES:
        slug, _, title, intro, _, _ = service
        service_schema = {"@context": "https://schema.org", "@type": "Service", "name": title, "description": intro, "provider": {"@type": "Organization", "name": "Intrinsic Consulting Solutions"}}
        write_route(f"/services/{slug}/", document(f"{title} | Outsourced HR | ICS", intro, f"/services/{slug}/", service_page(service), "services", [service_schema]))
    about_content, person_schemas = about_page(reference_home)
    write_route("/about/", document("Our people | Outsourced HR | ICS", "Meet the experienced HR executives behind Intrinsic Consulting Solutions.", "/about/", about_content, "about", person_schemas))
    write_route("/insights/", document("Insights | Outsourced HR | ICS", "Plain-English HR guidance for South African business owners.", "/insights/", insights_page(), "insights"))
    for article_id, route in ARTICLE_ROUTES.items():
        article_content, article_schema = article_page(reference_insights, article_id)
        title, meta = ARTICLE_META[article_id]
        write_route(route, document(f"{title} | ICS", meta, route, article_content, "insights", [article_schema]))
    write_route("/job-seekers/", document("Job seekers | Outsourced HR | ICS", "Recruitment opportunities for skilled and professional positions across South Africa.", "/job-seekers/", job_seekers_page(), "jobs"))
    write_route("/contact/", document("Contact | Outsourced HR | ICS", "Contact ICS in Cape Town or Johannesburg to book an HR Health Check.", "/contact/", contact_page(reference_home), ""))
    write_route("/privacy/", document("Privacy | Outsourced HR | ICS", "ICS POPIA privacy notice.", "/privacy/", privacy_page(), ""))
    not_found = document("Page not found | ICS", "The page you requested could not be found.", "/404", '<section class="page-hero"><div class="wrap"><h1>Page not found.</h1><p class="lede">[NEW COPY: for 247 review] The page you requested could not be found.</p><p class="steps-cta"><a class="btn btn-primary" href="/">Home</a><a class="btn btn-ghost" href="/hr-health-check/">Book an HR Health Check</a></p></div></section>')
    (OUT / "404.html").write_text(not_found, encoding="utf-8")
    print(f"Built {len(ROUTES)} routes in {OUT}")


if __name__ == "__main__":
    main()
