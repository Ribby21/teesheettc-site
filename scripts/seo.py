"""One-shot: inject SEO/OG/icon meta into the pages and write manifest, robots, sitemap.
Safe to re-run (it rewrites the <head> blocks it owns; policy-page BODIES are never touched)."""
import re, datetime

BASE = 'https://teesheettc.com'
OG_IMG = f'{BASE}/assets/og-image.png'


def head_block(title, desc, path, extra_ld=''):
    url = f'{BASE}/{path}' if path else f'{BASE}/'
    return f'''  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#2E7D32">

  <!-- Icons (generated from the app icon) -->
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/assets/favicon-16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">

  <!-- Open Graph / Twitter -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="TeeSheet TC">
  <meta property="og:locale" content="en_US">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{OG_IMG}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="TeeSheet TC: every tee time in the Twin Cities, one search">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{OG_IMG}">

  <link rel="stylesheet" href="/styles.css">
{extra_ld}'''


pages = {
    'index.html': (
        'TeeSheet TC: Every Twin Cities Tee Time, One App',
        'Live tee times from 140+ public golf courses across the Twin Cities metro and western Wisconsin, in one search. Pick a date, time, and distance; book directly with the course. Free on iOS and Android.',
        ''),
    'support.html': (
        'Support: TeeSheet TC',
        'Help, FAQ, and contact for the TeeSheet TC golf tee-time app: missing courses, subscriptions, restoring Pro, and data deletion.',
        'support.html'),
}

home_ld = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "MobileApplication",
        "name": "TeeSheet TC",
        "operatingSystem": "iOS, Android",
        "applicationCategory": "SportsApplication",
        "description": "Live tee times from 140+ public golf courses across the Twin Cities metro and western Wisconsin, in one search. Book directly with the course.",
        "url": "https://teesheettc.com/",
        "image": "https://teesheettc.com/assets/icon-512.png",
        "offers": [
          {"@type": "Offer", "price": "0", "priceCurrency": "USD", "description": "Free"},
          {"@type": "Offer", "price": "4.99", "priceCurrency": "USD", "description": "TeeSheet TC Pro, monthly"},
          {"@type": "Offer", "price": "39.99", "priceCurrency": "USD", "description": "TeeSheet TC Pro, yearly"}
        ],
        "installUrl": [
          "https://apps.apple.com/us/app/teesheet-tc/id6762153205",
          "https://play.google.com/store/apps/details?id=com.teesheetc.tee_times_app"
        ],
        "areaServed": {"@type": "Place", "name": "Minneapolis-Saint Paul, Minnesota and western Wisconsin"},
        "publisher": {"@id": "https://teesheettc.com/#org"}
      },
      {
        "@type": "Organization",
        "@id": "https://teesheettc.com/#org",
        "name": "TeeSheet TC",
        "url": "https://teesheettc.com/",
        "logo": "https://teesheettc.com/assets/icon-512.png",
        "email": "teesheet@ribby.dev",
        "contactPoint": {"@type": "ContactPoint", "contactType": "customer support", "email": "teesheet@ribby.dev"}
      },
      {
        "@type": "WebSite",
        "name": "TeeSheet TC",
        "url": "https://teesheettc.com/",
        "publisher": {"@id": "https://teesheettc.com/#org"}
      }
    ]
  }
  </script>
'''

support_ld = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {"@type": "Question", "name": "A tee time in the app was not available when I tapped through.", "acceptedAnswer": {"@type": "Answer", "text": "Tee times refresh roughly every 30 minutes and popular times go fast; the course's booking page is always the source of truth. If a course is consistently wrong, contact support."}},
      {"@type": "Question", "name": "Why is my course not in the app?", "acceptedAnswer": {"@type": "Answer", "text": "TeeSheet TC covers every public course it can reach across the Twin Cities metro and western Wisconsin. Courses without online booking are listed with a phone number. Email teesheet@ribby.dev to request a missing course."}},
      {"@type": "Question", "name": "How do I cancel or manage Pro?", "acceptedAnswer": {"@type": "Answer", "text": "Subscriptions are managed by your app store. Android: Google Play > profile > Payments & subscriptions > Subscriptions. iOS: Settings > your name > Subscriptions."}},
      {"@type": "Question", "name": "Do I need an account?", "acceptedAnswer": {"@type": "Answer", "text": "No. TeeSheet TC has no accounts; favorites and preferences are stored on your device."}},
      {"@type": "Question", "name": "Are you affiliated with the courses or GolfNow?", "acceptedAnswer": {"@type": "Answer", "text": "No. TeeSheet TC is not affiliated with any course or booking provider. It reads publicly available tee-time listings and sends you to the course's own booking page, never taking a booking fee."}}
    ]
  }
  </script>
'''

for fn, (title, desc, path) in pages.items():
    s = open(fn, encoding='utf-8').read()
    m = re.search(r'(<meta name="viewport"[^>]*>\n)(.*?)(</head>)', s, re.S)
    assert m, fn
    ld = home_ld if fn == 'index.html' else support_ld
    s = s[:m.end(1)] + head_block(title, desc, path, ld) + s[m.start(3):]
    open(fn, 'w', encoding='utf-8', newline='\n').write(s)
    print('head rewritten:', fn)

# Policy pages: body text stays verbatim; only add icon/canonical/og to <head>.
for fn, title in [('privacy.html', 'Privacy Policy: TeeSheet TC'),
                  ('terms.html', 'Terms of Service: TeeSheet TC'),
                  ('delete-account.html', 'Delete Your Data: TeeSheet TC')]:
    s = open(fn, encoding='utf-8').read()
    if '<link rel="canonical"' in s:
        print('already injected:', fn); continue
    inject = f'''  <link rel="canonical" href="{BASE}/{fn}">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png">
  <meta name="theme-color" content="#2E7D32">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="TeeSheet TC">
  <meta property="og:title" content="{title}">
  <meta property="og:url" content="{BASE}/{fn}">
  <meta property="og:image" content="{OG_IMG}">
  <meta name="twitter:card" content="summary_large_image">
'''
    s = s.replace('</title>\n', '</title>\n' + inject, 1)
    open(fn, 'w', encoding='utf-8', newline='\n').write(s)
    print('meta injected (body untouched):', fn)

s = open('404.html', encoding='utf-8').read()
if 'favicon.ico' not in s:
    s = s.replace('<link rel="stylesheet" href="/styles.css">',
                  '<link rel="icon" href="/favicon.ico"><meta name="robots" content="noindex"><link rel="stylesheet" href="/styles.css">')
    open('404.html', 'w', encoding='utf-8', newline='\n').write(s)

open('site.webmanifest', 'w', encoding='utf-8', newline='\n').write('''{
  "name": "TeeSheet TC",
  "short_name": "TeeSheet TC",
  "description": "Every tee time in the Twin Cities. One search.",
  "start_url": "/",
  "display": "browser",
  "background_color": "#2E7D32",
  "theme_color": "#2E7D32",
  "icons": [
    {"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png"}
  ]
}
''')
open('robots.txt', 'w', encoding='utf-8', newline='\n').write('User-agent: *\nAllow: /\n\nSitemap: https://teesheettc.com/sitemap.xml\n')

today = datetime.date.today().isoformat()
urls = [('', '1.0'), ('support.html', '0.7'), ('privacy.html', '0.3'), ('terms.html', '0.3'), ('delete-account.html', '0.3')]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for p, pr in urls:
    sm += f'  <url><loc>{BASE}/{p}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>\n'
sm += '</urlset>\n'
open('sitemap.xml', 'w', encoding='utf-8', newline='\n').write(sm)
print('manifest, robots, sitemap written')
