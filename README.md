# teesheettc-site

Marketing / informational site for **TeeSheet TC** (Twin Cities tee-time app),
live at **https://teesheettc.com**. Static HTML + one stylesheet, no build step.
Hosted on GitHub Pages: **pushing `master` publishes the live site** within a
couple of minutes.

| File | Purpose |
|---|---|
| `index.html` | Landing page (what it is, store badges, features, Free vs Pro) |
| `support.html` | Support / FAQ page (store listings require a support URL) |
| `privacy.html` | Privacy policy |
| `terms.html` | Terms of service (see the Lightspeed note below) |
| `delete-account.html` | Account/data deletion page — **Google Play requires this URL** |
| `get.html` | QR-code landing: detects iOS/Android and redirects to the right store; `?src=<tag>` is passed to Play's install referrer for attribution |
| `print/` | Printable 4x6 counter card (single + letter-size 2-up); its QR points to `/get?src=card` |
| `app-ads.txt` | AdMob authorized sellers — **must stay at the domain root** |
| `styles.css` | Shared styles (brand green `#2E7D32` matches the app) |
| `assets/`, `favicon.ico`, `site.webmanifest` | Icons and OG images, generated from the app icon by `scripts/seo.py` |
| `robots.txt`, `sitemap.xml` | SEO; update `lastmod` in the sitemap when a page changes |
| `CNAME` | Custom domain `teesheettc.com` |

## URLs the app and store listings depend on

The app (1.2.2+) and both store listings link to these paths. They must keep
resolving:

- `/privacy.html`, `/terms.html`, `/delete-account.html`, `/app-ads.txt`
- `/get` (QR codes on printed counter cards)

## Lightspeed terms section (hidden until go-live)

`terms.html` contains a "Third-Party Booking Systems" section inside an HTML
comment. The Lightspeed API License Agreement requires it once the Partner API
integration is live in production. The comment explains how to turn it on:
uncomment, renumber the later sections, and bump "Last updated". Details are in
the `tee-times` repo (CLAUDE.md, "Lightspeed Partner API").
