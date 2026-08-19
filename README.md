# teesheettc-site

Marketing / informational site for **TeeSheet TC** (Twin Cities tee-time app).
Static HTML + one stylesheet, no build step. Hosted on GitHub Pages.

| File | Purpose |
|---|---|
| `index.html` | Landing page (what it is, store badges, features, Free vs Pro) |
| `courses.html` | Public course directory — **generated**, don't hand-edit (see below) |
| `support.html` | Support / FAQ page (store listings require a support URL) |
| `privacy.html` | Privacy policy — copied verbatim from the previous site |
| `terms.html` | Terms of service — copied verbatim from the previous site |
| `delete-account.html` | Account/data deletion page — **Google Play requires this URL** |
| `app-ads.txt` | AdMob authorized sellers — **must stay at the domain root** |
| `styles.css` | Shared styles (brand green `#2E7D32` matches the app) |

## Regenerating the course list

```
node scripts/build-courses.mjs ../tee-times/scraper/config/courses.json
```

Reads the app's course config and rewrites `courses.html`. Run it whenever
courses are added/removed in the app repo. PCC tier numbers are intentionally
never emitted — only the boolean badge (partner condition).

## URLs the app and store listings depend on

These paths must keep resolving (same filenames as the old
`ribby21.github.io/teesheet-site/` so the app can be repointed with a URL change only):

- `/privacy.html`, `/terms.html`, `/delete-account.html`, `/app-ads.txt`

## TODO before switching the app over

- Decide on a custom domain; if used, set `CNAME` here and keep the old
  GitHub Pages URLs redirecting until the app + store listings are updated.
