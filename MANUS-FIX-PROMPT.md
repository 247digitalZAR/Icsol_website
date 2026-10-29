# Manus fix prompt: unstyled site

Use this in the existing Manus task (icsolsite-h9bvevuq.manus.space). Upload the updated build pack first, or pull the latest from GitHub.

---

The site has no styling: fonts, colours, layout, header, hero and every section render as plain HTML. Cause: `css/styles.css` only contains the demo host's wrapper reset (`body{font:14px -apple-system…}`) plus the styles for the new pages. The main design stylesheet was never ported, so classes like `site`, `wrap`, `hero`, `band`, `why`, `svc`, `team`, `person`, `tool`, `steps-band`, `faq-grid` and `btn-primary` have no rules.

The build pack is now fixed: the full stylesheet is in `design-reference/assets/css/site.css`, with `insights.css` for the Insights pages.

Please:
1. Replace the top of `css/styles.css` with the full contents of `design-reference/assets/css/site.css`, keeping your existing rules for the new pages after it. Delete the wrapper rules (`:root{color-scheme:light;box-sizing…}`, `body{margin:0;padding:0;font:14px -apple-system…;background:#fff;color:#000}`), which override the design.
2. Add `design-reference/assets/css/insights.css` and load it on `/insights/` and every article page.
3. Fix the hero image path in the CSS so it points to your hero file (`/assets/img/hero-concept.jpg`).
4. Self-host the three fonts (Young Serif, Figtree, IBM Plex Mono) and confirm `body` computes to Figtree.
5. Check every class used in the HTML has styles, on every page. List any that don't.
6. Compare each page side by side with `design-reference/index.html` at 1440 px and 375 px, then show me the preview.

Don't change any copy or page structure; this is a styling fix only.
