# ICS website: Manus build pack

Build pack for the new **Intrinsic Consulting Solutions (ICS)** website, icsol.co.za.
Prepared by 247 Digital, 29 October 2026.

The content and design were reviewed and agreed with Mark Meredith and Barbara Henshilwood
(feedback rounds 21 to 28 October 2026). This repo hands that approved demo to Manus for the
production build.

- Approved demo: https://claude.ai/artifact/3Dmxy9JnUJqZGCn77CBx57
- Client contacts: Mark Meredith (admin@icsol.co.za), Barbara Henshilwood (barbara@icsol.co.za)
- 247 owner: Andrew Friedmann. Developer: Oliver (devteam@247digital.co.za)

## What's in the repo

| Path | What it is |
|---|---|
| `MANUS-PROMPT.md` | The prompt to paste into Manus. Start here. |
| `BUILD-SPEC.md` | Full build specification: sitemap, page-by-page content map, design system, integrations, SEO, and what to strip from the demo. |
| `QA-CHECKLIST.md` | Sign-off checklist before go-live. |
| `design-reference/` | The approved demo, unchanged in content. Open `design-reference/index.html` in a browser. **This is the source of truth for copy and look.** |
| `assets/brand/` | ICS logo (PNG, transparent). |
| `assets/team/` | Team headshots, cropped 4:5 at 480 x 600. |
| `assets/photography/` | Hero banner (concept image, to be replaced before launch). |
| `site/` | Empty until Manus pushes the production build here. |

## How to build it in Manus

1. **Start a new Manus task** in the 247 Digital workspace. Name it `ICS website build`.
2. **Give Manus the source.** Connect this GitHub repo to the task (or upload the repo as a zip if the connector isn't available).
3. **Paste the prompt** from `MANUS-PROMPT.md` as the first message. Don't edit the copy rules in it: they keep the approved wording intact.
4. **Let it run, then review the preview** against `design-reference/` page by page, using `QA-CHECKLIST.md`.
5. **Give feedback in the same task**, one batch at a time, quoting the page and section.
6. **Push the build back to GitHub.** Ask Manus to commit the finished site to the `site/` folder on a branch called `manus-build` and open a pull request to `main`. Merge once QA passes.
7. **Back up the Manus task.** Export the task data once the build is approved, and again after every later change (lesson from Printafoil: a Manus restore only brings back what was in the last export).
8. **Go live** (see below).

## Go-live

- **Domain:** icsol.co.za is currently managed by Tanya at Spyderweb (info@spyderweb.co.za). Mark introduced Oliver on 27 October and asked Tanya to pass on logins. Get registrar and DNS access before launch day.
- **DNS:** point the domain at the Manus-hosted site (or wherever we host the `site/` build). Keep the existing MX records so ICS email keeps working.
- **Redirects:** map the old site's main URLs (job portal pages, contact, about) to their new equivalents with 301s. See `BUILD-SPEC.md` § Redirects.
- **After launch:** submit the sitemap in Google Search Console, confirm GA4 is receiving data, and send a test enquiry through every form.

## Open items before launch

These are placeholders in the approved content. None blocks the build; all must be resolved before go-live.

1. **Hero photo:** AI-generated concept image. Replace with licensed stock or a real shoot.
2. **Sizing guide:** the days per week for 51 to 100 and 101 to 250 people are 247 placeholders. ICS to confirm. The same figures appear in the Insights article "Do you need an HR manager yet?", so update both together.
3. **Testimonials:** three slots waiting on quotes Mark is collecting.
4. **Insights articles:** four drafts for ICS to fact-check and approve before publishing.
5. **Health check:** confirm whether it's free and whether to show a price.
6. **Hire comparison:** R25k to R45k+ is a market benchmark; confirm ICS is happy to show it.
7. **Andy Mackenzie:** add a team card if he's client-facing.
8. **Integrations:** CRM form endpoint, chatbot embed code, GA4/GTM IDs, vacancies feed URL (see `BUILD-SPEC.md` § Integrations).
