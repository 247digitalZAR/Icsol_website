# ICS website — client-preview handover

This is the ICS client-review website, not a production launch. The 2 November 2026 handover contains the source and static output corresponding to published Manus checkpoint `d6d2c7d570e8be8643f5858139f0622749c93b7d`.

Preview: https://testsite247digital.online/

The existing `www.icsol.co.za` website and DNS have not been changed. Do not launch on the production domain, alter shared Placement Partner settings, or submit test applications without ICS approval.

## Build and run

Use Python 3.10+ (the container uses Python 3.12). No third-party Python dependency is needed for the static build or server.

Run from this `site/` directory, keeping the sibling `design-reference/` directory in place:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 build.py
PYTHONDONTWRITEBYTECODE=1 python3 serve.py --port 3000 --directory public
```

`build.py` recreates `public/`, importing approved reference HTML, styles and effects from `../design-reference/`. Edit source and rebuild; do not edit generated HTML directly. `serve.py` binds to `0.0.0.0`; use a trusted development environment. Port is selectable via `--port`.

The committed `public/` directory is self-contained. The supplied Dockerfile runs `serve.py` with that output. The unauthenticated health endpoint is `/_app/health`. Use this server, or equivalent hosting rules, to retain branded HTTP 404 responses and staging indexing controls.

## Key files

- `build.py`: content, service catalogue, templates, shared CSS additions, routes and metadata.
- `src/app.js`: navigation, sizing guide, enquiry forms, consent preferences, flags and demo-chat loading.
- `src/chat-demo.js`: scripted assistant; no lead delivery or monitored inbox.
- `site.config.js`: optional integration placeholders, approved testimonial flag and sizing tiers.
- `assets/source/`, `assets/fonts/`: supplied imagery and self-hosted Young Serif, Figtree and IBM Plex Mono.
- `public/`: 23 generated page routes plus 404, styles/scripts, assets, sitemap and route manifest.
- `serve.py`, `Dockerfile`: serving, 404s and staging indexing.
- `HANDOVER.md`, `LAUNCH-INPUTS.md`: delivered scope, checks and deferred production work.
- `../BUILD-SPEC.md`, `../COPY-DEMO-POLISH.md`, `../design-reference/`: original build pack. Later client amendments appear in `build.py` and this handover.

## Current integrations

Enquiry/checklist forms post to `https://formsubmit.co/ajax/admin@icsol.co.za`. Delivery/activation is not confirmed; leave this unchanged for the current test phase. Checklist requests notify ICS; they do not automatically deliver a checklist file.

`CRM_FORM_ENDPOINT`, `CRM_CHECKLIST_ENDPOINT`, `CHATBOT_EMBED`, `GTM_ID` and `VACANCIES_URL` remain empty. The current form handler does not consume the CRM endpoint placeholders, so adding values alone does not complete a CRM integration. GTM and a configured live chatbot are consent-gated; the scripted assistant is a demo. `SHOW_TESTIMONIALS` is true for the three supplied references.

Recruitment embeds are explicit in the generator, independent of `VACANCIES_URL`:

- `/job-seekers/`: `https://webapp.placementpartner.com/wi/weblinks.php?id=intrinsic&logo=0`
- `/job-seekers/submit-cv/`: `https://webapp.placementpartner.com/wi/application_form.php?id=intrinsic`

These are LIVE-account embeds even on the test domain. Submissions go to ICS's Placement Partner Post Box. Do not submit tests without ICS agreement. The Hotlist is absent. Provider CSS/settings are unchanged; parent-page CSS cannot restyle cross-origin iframe content.

## Serving and indexing

Unknown routes return the branded page with HTTP 404. HTML on non-`icsol.co.za` hostnames gets `noindex, nofollow`; canonical hosts are indexable. `/robots.txt` disallows staging crawling. Canonical metadata and the sitemap use `https://icsol.co.za`; these values are not authorisation for DNS cutover or launch.

CSS/JS links are versioned. Main stylesheet version: `20261102.3`. Shared app/config/chat version: `20261102.2`. Increment the relevant version whenever those assets change.
