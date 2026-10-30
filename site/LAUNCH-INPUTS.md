# ICS launch inputs and approval list

The static build is complete and the unresolved items below are intentionally visible/configured rather than invented.

## `[NEW COPY: for 247 review]`

The About page carries a short history marker: `ICS has supported businesses since 2017.` It needs approved narrative copy.

Each of the eight service pages has two marked content blocks, **What’s included** and **Who it’s for**, because the approved demo contains the service-card introductions only. These sixteen blocks need content approval before their markers are removed.

The Job seekers page marks the Placement Partners vacancy feed connection. It will become live when `VACANCIES_URL` is supplied.

The Privacy page is intentionally marked because the current legacy POPI policy focuses on recruitment applicants rather than the new HR Health Check enquiry use case. ICS or 247 needs to approve the new notice.

The 404 page has the required one-line marker awaiting 247 approval.

## Integration and launch dependencies

`CRM_FORM_ENDPOINT` and `CRM_CHECKLIST_ENDPOINT` are blank, so the Health Check and checklist forms show a clear fallback rather than claiming a submission. Supply the endpoints and test the payloads end to end before launch.

`CHATBOT_EMBED` and `GTM_ID` are blank. The site correctly keeps chat and analytics blocked until the visitor accepts cookie consent, but neither integration can activate until its value is supplied.

`VACANCIES_URL` is blank. The recruitment button remains pointed at Contact until the approved live feed/page is supplied.

`SHOW_TESTIMONIALS` is `false`, so the three unapproved testimonial placeholders are not published. Switch it only after quotes are approved.

The 51–100 and 101–249 headcount tiers remain the agreed 247 placeholders and must be confirmed by ICS; update `site.config.js` and the “Do you need an HR manager yet?” article together.

The supplied hero is still the approved concept image. Replace it with licensed stock or real photography before launch. The present Open Graph image uses that temporary hero; a final 1200 × 630 logo-on-indigo share asset still needs approval.

## Redirect audit

`redirects.csv` covers the 24 legacy HTML/archive routes found in the live robots-declared sitemap feed on 29 October 2026. The sitemap also lists ten `/wp-content/uploads/` image assets; these are retained as legacy media rather than routed as pages. The underlying sitemap downloads and full URL inventory are recorded under `../../.work/research/icsol-legacy-urls/`.
