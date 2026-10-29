# ICS website: QA checklist

Tick every item on the Manus preview before merging to `main`, and again on the live domain after launch.

## Content
- [ ] Every page's copy matches `design-reference/` word for word (spot-check five paragraphs per page).
- [ ] Every `[NEW COPY]` block has been reviewed by 247 and the marker removed.
- [ ] "Book an HR Health Check" is the only CTA wording. No "SMEs", no "10 to 50 employees".
- [ ] Questionnaire says 5 minutes; turnaround says about 2 days.
- [ ] Team: four cards, correct photos, Barbara's role reads "Recruitment and Labour Law".
- [ ] Contact details match `BUILD-SPEC.md` § 10 everywhere (header, footer, contact page, schema).
- [ ] Testimonials hidden until real quotes are approved.

## Design
- [ ] Colours, fonts and spacing match the reference on desktop (1440 px) and mobile (375 px).
- [ ] Hero photo fades in from indigo on the right; readable overlay on mobile.
- [ ] Dark mode looks right (logo sits on its white plate).
- [ ] Motion works, and turns off with "reduce motion" enabled.
- [ ] Sizing slider: 18 shows "One to two days a week"; 75 shows "Three days a week"; 250+ shows "Talk to us".

## Function
- [ ] Health check form: required fields enforced, consent required, submission reaches the CRM, success message shows.
- [ ] Checklist sign-up reaches the CRM.
- [ ] Chatbot loads (or the launcher is hidden if the embed isn't ready).
- [ ] Phone and email links work on mobile.
- [ ] All internal links resolve; no 404s. The 404 page works.
- [ ] Job seekers page links to live vacancies.

## Technical
- [ ] Lighthouse mobile 90+ (Performance, Accessibility, Best Practices, SEO) on Home, HR Health Check, one service page and one article.
- [ ] Unique title and meta description on every page.
- [ ] JSON-LD validates in Google's Rich Results Test (ProfessionalService, FAQPage, Article).
- [ ] `sitemap.xml`, `robots.txt`, `llms.txt` and canonical tags present.
- [ ] GTM fires; GA4 shows `form_submit` as a conversion; cookie banner blocks tags until consent.
- [ ] No console errors.

## Launch
- [ ] Registrar and DNS logins received from Spyderweb.
- [ ] MX records unchanged; send and receive a test email at admin@icsol.co.za after the DNS switch.
- [ ] 301 redirects from `site/redirects.csv` live and tested.
- [ ] HTTPS active on icsol.co.za and www.
- [ ] Sitemap submitted in Search Console.
- [ ] Manus task exported as a backup.
- [ ] Hero concept image replaced with licensed or real photography.
