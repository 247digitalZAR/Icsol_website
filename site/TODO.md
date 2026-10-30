# ICS website build TODO

The approved implementation plan is `../BUILD-SPEC.md`; the approved demo in `../design-reference/` is the copy and visual source of truth.

- [ ] **Shared static website system** — Generate fully pre-rendered HTML for the complete sitemap, with one reusable header, footer, responsive navigation, the approved Young Serif/Figtree/IBM Plex Mono design system, light/dark themes, reduced-motion support, visible focus states and a skip link. All demo ribbon, notes drawer, forced-scroll logic and scripted demo chat must be absent.

- [ ] **Home and HR Health Check conversion path** — Deliver the short home page with the approved hero, proof, marquee, why, example week, sizing slider, services overview, three-step health check, team preview, insights, FAQ and a closing route to `/hr-health-check/`. The questionnaire must say 5 minutes, the turnaround about 2 days, and the only primary CTA wording must be “Book an HR Health Check”. The non-linear slider must map track positions 0, 400, 600, 800 and 1000 to 5, 25, 50, 100 and 250 people respectively.

- [ ] **Services and people pages** — Deliver the Services overview, all eight service pages, and the About/people page. Each service page must retain the approved card intro, show relevant team and article links where specified, end with the health-check CTA, and mark every required new section `[NEW COPY: for 247 review]` until approved. The four team cards must use supplied 4:5 portraits and Barbara’s role must read “Recruitment and Labour Law”.

- [ ] **Insights and secondary pages** — Deliver Insights index, all four approved article pages, Job seekers, Contact, Privacy and 404. Approved article copy must remain verbatim. Job seeker feed, privacy notice and any unapproved copy must remain clearly marked/configured rather than invented.

- [ ] **Forms, privacy and integrations** — Keep `CRM_FORM_ENDPOINT`, `CRM_CHECKLIST_ENDPOINT`, `CHATBOT_EMBED`, `GTM_ID`, `VACANCIES_URL` and `SHOW_TESTIMONIALS` in one `site.config.js`. Implement required fields, honeypot spam protection, POPIA consent linking to `/privacy/`, UTM/page/timestamp payloads and the specified success message. Do not load chat or analytics before Accept/Decline cookie consent. Keep testimonials hidden until `SHOW_TESTIMONIALS` is true.

- [ ] **SEO, performance and launch files** — Deliver unique metadata, canonical URLs, Open Graph/Twitter metadata, JSON-LD for ProfessionalService, Person, Service, Article, FAQPage and BreadcrumbList where applicable; plus `sitemap.xml`, `robots.txt`, `llms.txt`, `manus-routes.json` and `redirects.csv`. Use supplied imagery with explicit dimensions, lazy loading below the fold, WebP where tooling permits and JPEG/PNG fallback.

- [ ] **Verification and handoff** — Validate generated HTML, internal links, static routes, forms in configured/unconfigured modes and the local preview on port 3000. Record unresolved launch inputs: CRM/checklist endpoints, chatbot embed, GTM ID, vacancies URL, testimonials, privacy notice, approved new service-page copy, final sizing tiers and licensed hero/share imagery.
