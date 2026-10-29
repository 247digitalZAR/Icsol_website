# Manus prompt

Paste everything below the line into a new Manus task, with this repo attached.

---

You are building the production website for **Intrinsic Consulting Solutions (ICS)**, a Cape Town HR consultancy (icsol.co.za). ICS provides outsourced and fractional HR to South African small to medium-sized businesses, with recruitment as a supporting service.

The content and design are already approved by the client. Your job is to turn the approved single-page demo into a fast, multi-page, SEO-ready website. **Do not redesign it and do not rewrite the copy.**

## Source files (in the attached repo)

- `design-reference/index.html` and `design-reference/insights.html`: the approved demo. This is the source of truth for every word, colour, font, layout and interaction.
- `design-reference/assets/css/site.css`: **the complete stylesheet** (tokens, layout and every component). `insights.css` adds the article layout; `effects.css` is the motion layer.
- `design-reference/assets/`: the JS and images used by the demo.
- `assets/`: the production images (logo, team photos, hero).
- `BUILD-SPEC.md`: the full specification. Read it completely before you start, and follow it where it adds detail to this prompt.

## Rules

1. **Copy is locked.** Use the text from the design reference word for word. Don't shorten, rephrase, add marketing copy or change spelling (South African English). Where a new page needs a heading or intro that doesn't exist in the reference, mark it `[NEW COPY: for 247 review]` so we can approve it.
2. **Design is locked.** Port `site.css`, `insights.css` and `effects.css` in full as your base stylesheets, then add only what new pages need. Every class used in your HTML must be styled; check this before showing me a preview. Match the reference: colour tokens, fonts (Young Serif, Figtree, IBM Plex Mono), spacing, the indigo and lime brand, light and dark mode, and the motion layer (with `prefers-reduced-motion` respected).
3. **Split into pages** exactly as in `BUILD-SPEC.md` § Sitemap. The home page stays short and points to the HR Health Check.
4. **Every page must be pre-rendered HTML.** No content that only appears after JavaScript runs. A static build is ideal; if you use a framework, use static generation.
5. **Strip all demo-only elements** listed in `BUILD-SPEC.md` § Remove from the demo (the green "concept draft" ribbon, the "What's placeholder?" notes panel, the scripted demo chat answers, the demo form messages).
6. **Integrations go behind a single config file** (`site.config.js` or `.env`) with clearly named placeholders. Don't invent endpoints or IDs.
7. **Images:** use the files in `assets/`, served as optimised WebP with JPEG fallback, with explicit width and height, and lazy loading below the fold.
8. **Accessibility:** WCAG 2.2 AA. Keep the reference's labels, focus styles, skip link and ARIA attributes.
9. **Performance:** Lighthouse 90+ on mobile for Performance, Accessibility, Best Practices and SEO, on every page.

## Deliverables

1. A working preview I can click through.
2. The full source, committed to the attached GitHub repo in a `site/` folder, on a branch called `manus-build`, with a pull request to `main`.
3. A short `site/README.md` explaining how to build, where the config lives and how to add an Insights article.
4. A list of everything you marked `[NEW COPY]` or couldn't complete, with the reason.

Work in this order: read the spec, then build the shared layout (header, footer, design tokens, chat button), then the home page, then the remaining pages, then SEO and integrations, then the Lighthouse pass. Show me the preview after the home page, before building the rest.
