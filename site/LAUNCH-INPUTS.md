# ICS test-site status and launch dependencies

Updated 2 November 2026. This is a client preview, not a production launch. Keep the enquiry/checklist implementation unchanged for this phase, as instructed by Andrew.

## Implemented

Approved About, service-detail, Privacy and 404 copy is present, with later client service amendments in `build.py`. There are ten services and 23 declared page routes. Three supplied client-reference cards are enabled. Fonts are self-hosted and assets cache-versioned.

Job seekers and Submit your CV embed Placement Partner directly. `VACANCIES_URL` stays blank because iframe URLs are explicit in the generator. No Hotlist is exposed.

## Enquiry/checklist delivery — deferred

The browser handler posts Health Check/Contact enquiries and checklist requests to FormSubmit's AJAX endpoint for `admin@icsol.co.za`, including submitted fields, page URL, timestamp and consent wording. Honeypot and validation remain in place.

Inbox delivery and activation are not confirmed. Previous test attempts did not establish receipt. Before production, verify activation and complete an agreed end-to-end submission/inbox check. Do not treat a displayed success state alone as proof of delivery. Checklist requests notify ICS; automatic checklist delivery is not implemented.

CRM endpoint placeholders remain empty and are not consumed by the current handler. A future CRM integration requires an intentional code change and delivery tests, not just configuration values.

## Chat and measurement — deferred

`CHATBOT_EMBED` and `GTM_ID` are empty. The assistant uses scripted answers and does not forward conversations to ICS. Some replies imply personal follow-up; review that wording before production. Demo Health Check links currently use `#contact`, while the booking form uses `#booking-form`; resolve that mismatch during production preparation.

Future live chatbot/GTM integrations must preserve consent behaviour and be tested separately. Platform analytics is distinct from the blank GTM setting.

## Recruitment boundaries

Placement Partner URLs use the live `intrinsic` account. Applications/CVs enter ICS's real Post Box. No submissions were made during integration QA. Obtain ICS agreement before test applications/uploads, or request a sandbox account for isolated testing.

Provider-hosted styling/settings remain unchanged. CSS requests could affect other sites using the same account; confirm scope with Placement Partner first. Do not expose Hotlist list 33 without ICS approval that the candidate content is intended for public display.

## Production approvals and checks

- Full client sign-off on the preview, quotations, photography and final content.
- End-to-end enquiry/checklist delivery verification and any chosen production integrations.
- Confirmation of Privacy notice officer details, retention periods and provider disclosures.
- Final licensed/approved hero/share imagery if the current concept image is not accepted.
- Production domain/DNS/TLS cutover plan that preserves email DNS.
- Mobile, accessibility and performance revalidation on the intended production host.
- Legacy redirect-map review and deployment. The CSV is not applied by `serve.py`; CV redirects should reach the dedicated CV route, and same-path redirect loops must be avoided.

Preserve `serve.py`'s hostname-aware staging `noindex, nofollow` and branded HTTP 404 behaviour if changing the deployment stack.
