# ICS developer handover — 2 November 2026

Status: client-review/test website. Production launch is not authorised by this handover.

Live preview: https://testsite247digital.online/

Repository: https://github.com/247digitalZAR/Icsol_website

Review branch: `manus-build`

Pull request: https://github.com/247digitalZAR/Icsol_website/pull/1

## Source snapshot

The website source and committed `public/` output are exported from the saved and published Manus checkpoint `d6d2c7d570e8be8643f5858139f0622749c93b7d`. This SHA belongs to the separate managed website history, not the GitHub handover history. GitHub receives a normal commit on the existing review branch; the project remains managed by Manus. Private `.manus-webdev/`, credentials, local QA scripts and device-specific managed declarations are not exported.

The original repository build pack, approved copy files and design references are retained. The handover docs are updated without modifying runtime form integrations or the existing production website.

## Today's delivered updates

1. Homepage client-reference cards for Nexia, Berlin Packaging and Discover Africa Group, using the exact supplied quotations and attribution. The existing testimonials flag is enabled.
2. Ten-service catalogue on the homepage and Services index. New HR technology and AI and People analytics and workforce insights pages cover all requested systems/AI and reporting/analysis/survey services.
3. Workforce Planning's visible service copy replaced with Organisational design, covering operating models, role architecture, job evaluation, performance-management systems and workforce restructuring. The existing `/services/workforce-planning/` URL is retained to avoid breaking links; its visible title is Organisational design.
4. Team effectiveness workshops added to Training and facilitation. Employer value proposition development and employer recruitment branding added to Recruitment.
5. Contextual balance between people, employees, workforce and staff. Direct client quotes and appropriate legal/operational language remain intact.
6. Job seekers now embeds the direct Placement Partner vacancies feed, not the entire old ICS web page. A linked `/job-seekers/submit-cv/` page embeds the direct application form. Both have new-tab fallback links. The CV page discloses that submissions enter ICS's live recruitment system.
7. Updated route manifest, sitemap and asset cache versions. The duplicated Organisational design item in the homepage's mirrored list was removed.

## Checks completed

- Generator syntax/build and 23 generated page routes verified, with one H1 per page.
- Generated local links and the integration-page anchors verified; missing routes return branded HTTP 404.
- Recruitment pages checked at 1440px and 375px: Figtree body font, fitting buttons/iframe containers, no outer horizontal overflow, no broken page images or placeholder markers.
- Provider content inside both mobile iframes measured without horizontal overflow.
- Real vacancy listing, vacancy-detail navigation, application destination and blank CV form rendering verified.
- Browser console checks on the updated pages showed no errors.
- Live test-domain deployment verified at checkpoint `d6d2c7d`.
- No applications or CVs filled, uploaded or submitted. No Placement Partner account/shared styling changes made. No Hotlist exposure.

## Operational boundaries

Read `LAUNCH-INPUTS.md` before moving toward production. The enquiry/checklist handlers remain as-is, with email delivery unverified. No CRM, GTM ID or live chatbot is configured. The demo chat does not forward messages to ICS. Placement Partner embeds are live-account forms, not sandbox forms. Domain cutover, shared provider CSS changes and any submission test need separate approval.

The redirect CSV is a handover/audit map, not an installed redirect engine. Review it against the final production routes and implement redirects at the deployment layer; in particular, the legacy CV page should resolve to the new CV page rather than only the vacancies index.
