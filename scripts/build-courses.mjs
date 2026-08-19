// Regenerates courses.html from the app's courses.json so the public
// directory never drifts from what the app actually covers.
//
//   node scripts/build-courses.mjs ../tee-times/scraper/config/courses.json
//
// Reads: id, name, city, state, holes, system, pccTier, disabled.
// Writes: courses.html (full page, client-side filter, no framework).
import { readFileSync, writeFileSync } from 'node:fs';

const src = process.argv[2] ?? '../tee-times/scraper/config/courses.json';
const { courses } = JSON.parse(readFileSync(src, 'utf8'));
const active = courses.filter(c => !c.disabled);

const live = active.filter(c => c.system !== 'phone').length;
const pcc = active.filter(c => c.pccTier != null).length;
const states = [...new Set(active.map(c => c.state))].sort().join(' & ');

const esc = s => String(s).replace(/[&<>"]/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[ch]));

const rows = active
  .sort((a, b) => a.name.localeCompare(b.name))
  .map(c => {
    const booking = c.system === 'phone' ? '<span class="muted">Call to book</span>' : 'Live online times';
    const badge = c.pccTier != null ? ' <span class="pcc" title="Public Country Club participating course">PCC</span>' : '';
    // data-* carries a lowercase search key; tier is deliberately NOT emitted.
    return `      <tr data-q="${esc((c.name + ' ' + c.city + ' ' + c.state).toLowerCase())}" data-pcc="${c.pccTier != null ? 1 : 0}">
        <td>${esc(c.name)}${badge}</td>
        <td>${esc(c.city)}, ${esc(c.state)}</td>
        <td class="hide-sm">${c.holes}</td>
        <td class="hide-sm">${booking}</td>
      </tr>`;
  })
  .join('\n');

const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Courses — TeeSheet TC</title>
  <meta name="description" content="All ${active.length} public golf courses covered by TeeSheet TC across ${states}, including ${pcc} Public Country Club participating courses.">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">TeeSheet TC</a>
    <nav class="nav">
      <a href="index.html#how">How it works</a>
      <a href="courses.html">Courses</a>
      <a href="index.html#pro">Pro</a>
      <a href="support.html">Support</a>
      <a class="cta" href="index.html#get">Get the app</a>
    </nav>
  </div>
</header>

<section class="block">
  <div class="wrap">
    <h2>Courses in the app</h2>
    <p class="sub">${active.length} public courses across ${states}. ${live} show live online tee times in the app; the rest are listed with a phone number because they don't offer online booking. ${pcc} are Public Country Club participating courses, marked <span class="pcc">PCC</span>.</p>
    <div class="toolbar">
      <input id="q" type="search" placeholder="Search by course or city…" aria-label="Search courses">
      <label><input id="pccOnly" type="checkbox"> PCC courses only</label>
      <span id="count" class="muted" style="align-self:center"></span>
    </div>
    <div style="overflow-x:auto">
    <table class="courses">
      <thead><tr><th>Course</th><th>Location</th><th class="hide-sm">Holes</th><th class="hide-sm">Booking</th></tr></thead>
      <tbody id="rows">
${rows}
      </tbody>
    </table>
    </div>
    <p class="muted" style="margin-top:1.5em; font-size:0.85rem">Missing a course? <a href="support.html">Tell us</a>. Generated from the app's course list${new Date().toISOString().slice(0,10) ? ' on ' + new Date().toISOString().slice(0,10) : ''}.</p>
  </div>
</section>

<footer class="site-footer">
  <div class="wrap">
    <span>© 2026 TeeSheet TC</span>
    <span><a href="index.html">Home</a> · <a href="support.html">Support</a> · <a href="privacy.html">Privacy</a> · <a href="terms.html">Terms</a> · <a href="delete-account.html">Data deletion</a></span>
  </div>
</footer>

<script>
(function () {
  var q = document.getElementById('q'), pcc = document.getElementById('pccOnly'),
      rows = Array.prototype.slice.call(document.querySelectorAll('#rows tr')), count = document.getElementById('count');
  function apply() {
    var term = q.value.trim().toLowerCase(), only = pcc.checked, n = 0;
    rows.forEach(function (r) {
      var show = (!term || r.getAttribute('data-q').indexOf(term) !== -1) && (!only || r.getAttribute('data-pcc') === '1');
      r.style.display = show ? '' : 'none'; if (show) n++;
    });
    count.textContent = n + ' course' + (n === 1 ? '' : 's');
  }
  q.addEventListener('input', apply); pcc.addEventListener('change', apply); apply();
})();
</script>
</body>
</html>
`;
writeFileSync('courses.html', html);
console.log(`courses.html: ${active.length} courses (${live} live, ${pcc} PCC)`);
