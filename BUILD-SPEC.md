# ICS website: build specification

Version 1.0, 29 October 2026. Source of truth for copy and design: `design-reference/`.
Section references like `#why` are element IDs in `design-reference/index.html`.

## 1. Goal

One job: turn visitors into **HR Health Check bookings**. Every page ends with a route to the health check. Recruitment and job seekers stay available but secondary.

Audience: owners and MDs of South African small to medium-sized businesses (5 to 250+ staff), mainly Cape Town and Johannesburg. Second audience: corporate HR managers who need project support.

## 2. Sitemap

| URL | Page | Built from (reference) |
|---|---|---|
| `/` | Home | `.hero`, `.proof` + marquee, `#why`, `#week`, `#size` (slider only), `#services` (overview cards linking to service pages), `#how`, `#clients`, `#team` (preview: photo, name, role, link to About), `#insights` (latest 3 articles), `#faq`, closing CTA band linking to `/hr-health-check` |
| `/hr-health-check` | HR Health Check | `#how` (3 steps), `#size` (comparison table **and** slider), `#contact` (form and contact details), the checklist sign-up (`#magnet-form`), FAQ items relevant to cost and contracts |
| `/services` | Services overview | `#services` (all 8 cards), `#corporate` ("Already have an HR team?") |
| `/services/hr-strategy` | Human resource strategy | Card copy from `#services`, plus `[NEW COPY]` body |
| `/services/contracts-and-policies` | Contracts and policies | as above |
| `/services/discipline-and-ccma` | Discipline and the CCMA | as above |
| `/services/structure-culture-od` | Structure, culture and organisational development | as above |
| `/services/performance-and-incentives` | Reviews and incentives | as above |
| `/services/workforce-planning` | Workforce planning | as above |
| `/services/training-and-facilitation` | Training and facilitation | as above |
| `/services/recruitment` | Recruitment (executive search, permanent and contract placements) | as above |
| `/about` | About and our people | `.proof` stats, `#team` (full bios), `[NEW COPY]` short story since 2017 |
| `/insights` | Insights index | `design-reference/insights.html` hero and article list, checklist sign-up |
| `/insights/year-end-closedown` | Article | `#year-end` in insights.html |
| `/insights/ai-at-work-popia` | Article | `#ai-popia` |
| `/insights/first-disciplinary-hearing-ccma` | Article | `#ccma-hearing` |
| `/insights/do-you-need-an-hr-manager` | Article | `#hr-manager` |
| `/job-seekers` | Job seekers | `#careers`, plus the vacancies feed (see § 6) |
| `/contact` | Contact | `#contact` details and form, Google Map of 18 Ebony Road, Tokai |
| `/privacy` | POPIA privacy notice | `[NEW COPY]`: ICS to supply, or 247 drafts for ICS approval. The form consent text links here. |
| `/404` | Not found | `[NEW COPY]` one line plus links to Home and HR Health Check |

**Navigation (header):** How it works (`/hr-health-check`), Services, Our people (`/about`), Insights, Job seekers, and the primary button **Book an HR Health Check**.
**Footer:** address, both phone numbers, email, LinkedIn (https://www.linkedin.com/company/intrinsic-consulting-sa), page links, Privacy, © Intrinsic Consulting Solutions.

Each service page: H1 = service name, the card text as the intro, a `[NEW COPY]` section ("What's included", "Who it's for"), a link to the related Insights article where one exists (CCMA page → the hearing article, Contracts page → the year-end article), the relevant team member, and the health check CTA.

## 3. Copy rules

- All approved copy comes verbatim from `design-reference/`. South African English (organisation, labour, programme).
- The button label is always **Book an HR Health Check**.
- The questionnaire is **5 minutes**; the turnaround is **about 2 days**.
- Positioning line: "Outsourced and fractional HR for South African small to medium-sized businesses." Never "SMEs", never "10 to 50 employees".
- Anything you write that isn't in the reference: wrap it in `[NEW COPY: for 247 review]`.

## 4. Design system

All styles are in `design-reference/assets/css/site.css` (load first on every page), `insights.css` (Insights pages) and `effects.css` (motion). Port all three in full; don't rebuild them from screenshots. The tokens are the `:root` block at the top of `site.css`, including both dark-mode blocks.

| Token | Light | Use |
|---|---|---|
| `--ink` | `#1d174d` | Text |
| `--band` | `#2b2667` | Dark bands, logo indigo |
| `--ochre` | `#8bc53f` | Lime fills and buttons only, never text on white |
| `--ochre-ink` | `#46732b` | Green text on light backgrounds |
| `--paper` / `--surface` | `#f6f6fa` / `#ffffff` | Page / cards |

- **Fonts:** Young Serif (display), Figtree (body), IBM Plex Mono (labels). Self-host them (woff2, `font-display: swap`).
- **Components to reuse across pages:** header with reading-progress bar, buttons, eyebrow labels, cards with lime top rule on hover, team card (4:5 portrait), FAQ accordion (`<details>`), sizing slider, comparison table, testimonial card, article layout, form.
- **Motion:** port `effects.css` and `effects.js` as they are. Respect `prefers-reduced-motion`.
- **Hero:** photo on the right, fading in from indigo (mask gradient in the reference). On mobile the photo sits behind an indigo overlay.

### Sizing slider (keep the logic exactly)

The slider is non-linear: track positions 0 to 1000 map to 5, 25, 50, 100 and 250+ people at 0, 40%, 60%, 80% and 100%. Tiers:

| People | Title |
|---|---|
| 5 to 9 | A few hours a week |
| 10 to 30 | One to two days a week |
| 31 to 50 | Two days a week |
| 51 to 100 | Three days a week *(placeholder, ICS to confirm)* |
| 101 to 249 | A full outsourced HR function *(placeholder, ICS to confirm)* |
| 250+ | Talk to us |

The tier copy is in the `tiers` array in the reference's inline script. Put it in a data file so ICS can change it without code.

## 5. Remove from the demo

- The green ribbon "Concept draft v4 by 247 Digital…" and its "What's placeholder?" button.
- The notes drawer (`<aside class="notes">`).
- The inline script that forces the page to the top and the `ics-jump` sessionStorage logic (not needed once pages are separate).
- Demo messages: "In the live site this lands in the CRM…" and "Demo only: in the live site the checklist is emailed…".
- The scripted answers in `chat.js`. Keep the launcher button styling, and load the real chatbot embed instead (§ 6).
- Testimonial placeholders: hide the `#clients` section until real quotes arrive, behind a config flag.

## 6. Integrations

Put every value in one config file. Use these exact placeholder names:

| Config key | What it is | Status |
|---|---|---|
| `CRM_FORM_ENDPOINT` | 247 CRM webhook for the HR Health Check and contact forms | 247 to supply |
| `CRM_CHECKLIST_ENDPOINT` | Webhook for the checklist sign-up | 247 to supply |
| `CHATBOT_EMBED` | 247 AI chatbot script tag | 247 to supply |
| `GTM_ID` | Google Tag Manager container (GA4 runs through it) | 247 to supply |
| `VACANCIES_URL` | Placement Partners vacancy feed or page | ICS / 247 to supply |
| `SHOW_TESTIMONIALS` | `false` until quotes are approved | |

**Forms.** Health check / contact form fields: name, business name, email, phone, number of employees (Under 10, 10 to 25, 26 to 50, 51 to 100, 101 to 250, More than 250), main reason (Ongoing HR support, A disciplinary or CCMA matter, Contracts and policies, Structure or performance project, Recruitment), message (optional), POPIA consent checkbox (required, unticked by default). Post JSON to the endpoint with the page URL, UTM parameters, timestamp and the exact consent wording. Client-side validation, a honeypot field for spam, and a success state: "Thanks, request received. We'll call you back within one business day."

**Analytics events** (dataLayer): `cta_click` (label, page), `form_start`, `form_submit` (form name), `slider_change` (tier), `chat_open`, `phone_click`, `email_click`, `article_read` (75% scroll). Mark `form_submit` as the GA4 conversion.

**POPIA.** Consent text links to `/privacy`. No analytics or chat cookies before consent: add a simple cookie banner with Accept / Decline, wired to GTM consent mode.

## 7. SEO and AI search

- Unique `<title>` (under 60 characters) and meta description (under 155) per page. Pattern: `{Page} | Outsourced HR | ICS`. Home: `Outsourced & Fractional HR for SA Businesses | ICS`.
- One H1 per page. Clean heading order.
- Canonical URLs, `sitemap.xml`, `robots.txt`, Open Graph and Twitter tags with a 1200 x 630 share image (logo on indigo).
- Structured data (JSON-LD): `ProfessionalService` with both locations (Tokai head office, Johannesburg), phones and areas served; `Person` for each team member; `Service` on each service page; `Article` with author on each Insights article; `FAQPage` on Home and HR Health Check; `BreadcrumbList` on inner pages.
- Write the answer first on service pages and in articles (answer engines quote the opening lines).
- Add `/llms.txt` listing the main pages and a one-line description of each.

## 8. Redirects

Crawl the current icsol.co.za and add a 301 for every indexed URL: job and vacancy pages → `/job-seekers`, about/team → `/about`, services → the closest service page, contact → `/contact`, anything else → `/`. Deliver the map as `site/redirects.csv`.

## 9. Quality bar

- Lighthouse mobile 90+ on all four scores, every page.
- WCAG 2.2 AA; full keyboard use; visible focus.
- Works from 320 px wide; no horizontal scroll.
- Images WebP with fallback, sized, lazy-loaded below the fold. Hero under 200 KB.
- No console errors. All links resolve. Forms tested end to end.

## 10. Contact details (use exactly)

- Head office: 18 Ebony Road, Tokai, Cape Town, 7945
- Email: admin@icsol.co.za
- Cape Town: 082 921 9965
- Johannesburg: 079 103 2490
- LinkedIn: https://www.linkedin.com/company/intrinsic-consulting-sa
- Founded 2017
