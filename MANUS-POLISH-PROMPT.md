# Manus prompt: demo polish

Paste everything below the line into the existing Manus task (icsolsite-h9bvevuq.manus.space).

---

Pull the latest from the GitHub repo 247digitalZAR/Icsol_website (main branch). This site is a client preview: ICS will use it to decide whether to go into production, so it must look finished. CRM, Google Tag Manager, the chatbot embed and the vacancy feed are NOT needed for this version; leave those config values empty.

Make these changes:

1. **Fill all the placeholder copy.** Every `[NEW COPY: for 247 review]` marker must be gone from every page. The approved text for each one is in `COPY-DEMO-POLISH.md` in the repo: the 8 service pages ("What's included" and "Who it's for"), About, Job seekers, Privacy and the 404 page. Use it word for word. Don't show "(ICS to confirm)" on the site; that note is for us.

2. **Make the forms work by emailing admin@icsol.co.za.** Both the HR Health Check form and the checklist sign-up must send every submission to admin@icsol.co.za, with all fields, the page it came from and the consent wording in the email. Use a server-side function if this project supports one. If not, use FormSubmit's AJAX endpoint (`https://formsubmit.co/ajax/admin@icsol.co.za`) with `_subject` set to "New HR Health Check request" or "New checklist request", `_template` set to "table" and `_captcha` set to false. Keep the honeypot. Show "Thanks, request received. We'll call you back within one business day." on success, and a clear error with the phone number (082 921 9965) if sending fails. Tell me which method you used.

3. **Job seekers links.** "Search current vacancies" goes to https://www.icsol.co.za/job-search/ and add a second button, "Submit your CV", to https://www.icsol.co.za/submit-your-cv/. Both open in a new tab.

4. **Chat assistant.** With no chatbot embed set, the launcher must still work: restore the scripted demo answers from `design-reference/assets/js/chat.js`, with the changes listed in `COPY-DEMO-POLISH.md`.

5. **Stop old cached styles showing.** Add a version string to every CSS and JS link (for example `styles.css?v=20261030`) and change it whenever those files change, so visitors who saw the earlier unstyled build get the new styles.

6. **Proper 404.** Unknown URLs must return the 404 page with a 404 status, not the home page.

7. **Final check, then show me the preview.** On every page at 1440 px and 375 px: no placeholder markers, no unstyled elements, no broken links or images, no console errors. Submit one test enquiry with the name "247 TEST, please ignore" and confirm it arrived. If you used FormSubmit, the first submission sends an activation email to admin@icsol.co.za; tell me so I can ask ICS to click it.

Don't change any other copy, page structure or design. Commit to the `manus-build` branch and update the pull request to main.
