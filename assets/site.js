(function () {
  var root = document.body.getAttribute('data-root') || '';
  // mobile navigation
  var t = document.querySelector('.nav-toggle'), nav = document.getElementById('main-nav');
  if (t && nav) t.addEventListener('click', function () { var o = nav.classList.toggle('open'); t.setAttribute('aria-expanded', o); });

  // copy buttons
  function copyText(text, btn) {
    var done = function () { var o = btn.textContent; btn.textContent = 'Copied'; setTimeout(function () { btn.textContent = o; }, 1500); };
    if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, function () {});
  }
  document.querySelectorAll('[data-copy]').forEach(function (b) { b.addEventListener('click', function () { copyText(b.getAttribute('data-copy'), b); }); });
  document.querySelectorAll('[data-copy-target]').forEach(function (b) { b.addEventListener('click', function () { var el = document.getElementById(b.getAttribute('data-copy-target')); if (el) copyText(el.textContent, b); }); });

  // search
  var input = document.getElementById('search'), out = document.getElementById('search-results'), clear = document.getElementById('clear-search'), data = null;
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function load(cb) {
    if (data) return cb();
    fetch(root + 'assets/search.json').then(function (r) { return r.json(); }).then(function (d) { data = d; cb(); }).catch(function () { data = []; cb(); });
  }
  var weight = { 'Strategy': 3, 'Pupil need': 2.5, 'BSCS agreed practice': 2, 'Individual Development': 2, 'Evidence summary': 1.5 };
  function run() {
    var q = input.value.trim().toLowerCase();
    if (q.length < 2) { out.innerHTML = ''; return; }
    var terms = q.split(/\s+/);
    load(function () {
      var res = data.map(function (p) {
        var title = p.title.toLowerCase(), hay = (p.title + ' ' + p.desc + ' ' + p.text).toLowerCase(), s = 0;
        for (var i = 0; i < terms.length; i++) { var w = terms[i]; if (hay.indexOf(w) < 0) return null; if (title.indexOf(w) >= 0) s += 5; s += 1; }
        if (title.indexOf(q) >= 0) s += 8;
        return { p: p, s: s * (weight[p.kind] || 1) };
      }).filter(Boolean).sort(function (a, b) { return b.s - a.s; }).slice(0, 8);
      out.innerHTML = res.length ? res.map(function (r) {
        return '<a class="result" href="' + root + r.p.url + '"><strong>' + esc(r.p.title) + '</strong><span class="kind">' + esc(r.p.kind) + '</span><p>' + esc(r.p.desc) + '</p></a>';
      }).join('') : '<p class="muted">No pages match. Try a different word.</p>';
    });
  }
  if (input) { var timer; input.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(run, 150); }); }
  if (clear) clear.addEventListener('click', function () { input.value = ''; out.innerHTML = ''; input.focus(); });

  // strategy filters
  var grid = document.getElementById('strategy-grid');
  if (grid) {
    var st = 'all', tier = 'all', coreEl = document.getElementById('core-only'), count = document.getElementById('result-count');
    function apply() {
      var n = 0;
      grid.querySelectorAll('.s-card').forEach(function (c) {
        var show = (st === 'all' || c.dataset.stage === st) && (tier === 'all' || c.dataset.tier === tier) && (!coreEl.checked || c.dataset.core === '1');
        c.hidden = !show; if (show) n++;
      });
      count.textContent = 'Showing ' + n + ' strateg' + (n === 1 ? 'y' : 'ies');
    }
    function group(attr, set) {
      document.querySelectorAll('[' + attr + ']').forEach(function (b) {
        b.addEventListener('click', function () {
          document.querySelectorAll('[' + attr + ']').forEach(function (x) { x.classList.remove('active'); x.setAttribute('aria-pressed', 'false'); });
          b.classList.add('active'); b.setAttribute('aria-pressed', 'true'); set(b.getAttribute(attr)); apply();
        });
      });
    }
    group('data-f-stage', function (v) { st = v; }); group('data-f-tier', function (v) { tier = v; });
    coreEl.addEventListener('change', apply);
    var h = new URLSearchParams(location.search);
    if (h.get('core') === '1') { coreEl.checked = true; apply(); }
  }
})();
