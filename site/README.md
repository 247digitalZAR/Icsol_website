# ICS production website

This directory contains the static production build for Intrinsic Consulting Solutions (ICS).

## Run locally

```bash
PYTHONDONTWRITEBYTECODE=1 python3 build.py
PYTHONDONTWRITEBYTECODE=1 python3 serve.py --port 3000 --directory public
```

The generated static site is in `public/`. The build uses no Node or framework dependencies and produces pre-rendered HTML for every route.

## Source of truth

- Approved content and visual reference: `../design-reference/`
- Build requirements: `../BUILD-SPEC.md`
- Integration configuration: `site.config.js`
- Static site generator: `build.py`
- Shared production JavaScript: `src/app.js`
- Supplied production imagery: `assets/source/`

## Configure before go-live

Populate the following fields in `site.config.js`: `CRM_FORM_ENDPOINT`, `CRM_CHECKLIST_ENDPOINT`, `CHATBOT_EMBED`, `GTM_ID` and `VACANCIES_URL`. Keep `SHOW_TESTIMONIALS` set to `false` until testimonials are approved.

The HTML intentionally displays the form fallback rather than pretending to submit while the CRM endpoint is blank. Analytics and chat do not load until the visitor accepts the cookie banner.

## Add an Insights article

Add its approved title, meta data, URL slug and body to the `ARTICLES` dictionary in `build.py`; add the path to `routes`; then rebuild. Articles must retain approved South African English and use `[NEW COPY: for 247 review]` for any copy that does not yet appear in the approved reference.

## Known launch inputs

The repository build pack identifies unresolved inputs that remain outside this source tree: CRM endpoints, chatbot embed, GTM ID, vacancy feed URL, POPIA privacy notice, approved testimonials, confirmed sizing-guide figures, approved new service-page copy and licensed/replacement hero/share artwork.
