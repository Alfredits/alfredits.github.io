// Bóveda de la comunidad: botones de copiar, selector Mac/Windows, progreso de la guía y checklists.
(function () {
  function store(key, val) {
    try {
      if (val === undefined) return localStorage.getItem(key);
      localStorage.setItem(key, val);
    } catch (e) { return null; }
  }

  // Copiar
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var src = document.getElementById(btn.getAttribute('data-copy'));
      if (!src) return;
      var text = src.innerText;
      var done = function () {
        var old = btn.textContent;
        btn.textContent = 'Copiado';
        btn.classList.add('is-done');
        setTimeout(function () { btn.textContent = old; btn.classList.remove('is-done'); }, 1800);
      };
      var fallback = function () {
        var r = document.createRange(); r.selectNodeContents(src);
        var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
        try { document.execCommand('copy'); done(); } catch (e) {}
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, fallback);
      } else { fallback(); }
    });
  });

  // Mac / Windows
  var osBtns = document.querySelectorAll('[data-os]');
  if (osBtns.length) {
    var guess = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent) ? 'mac' : 'win';
    var setOs = function (os) {
      document.documentElement.setAttribute('data-os', os);
      osBtns.forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-os') === os ? 'true' : 'false'); });
      store('boveda-os', os);
    };
    setOs(store('boveda-os') || guess);
    osBtns.forEach(function (b) { b.addEventListener('click', function () { setOs(b.getAttribute('data-os')); }); });
  }

  // Progreso de la guía
  var steps = document.querySelectorAll('.step[data-step]');
  if (steps.length) {
    var key = 'boveda-guia-' + (document.body.getAttribute('data-guide') || 'x');
    var saved = {};
    try { saved = JSON.parse(store(key) || '{}') || {}; } catch (e) { saved = {}; }
    var bar = document.querySelector('.progress__bar i');
    var txt = document.querySelector('.progress__txt b');
    var paint = function () {
      var n = 0;
      steps.forEach(function (s) {
        var on = !!saved[s.getAttribute('data-step')];
        s.classList.toggle('is-done', on);
        var b = s.querySelector('.done-btn');
        if (b) b.textContent = on ? 'Hecho ✓' : 'Listo, siguiente paso';
        if (on) n++;
      });
      if (bar) bar.style.width = (n / steps.length * 100) + '%';
      if (txt) txt.textContent = n;
    };
    steps.forEach(function (s, i) {
      var b = s.querySelector('.done-btn');
      if (!b) return;
      b.addEventListener('click', function () {
        var id = s.getAttribute('data-step');
        saved[id] = !saved[id];
        store(key, JSON.stringify(saved));
        paint();
        if (saved[id] && steps[i + 1]) steps[i + 1].scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });
    paint();
  }

  // Checklists que se recuerdan
  document.querySelectorAll('.check[data-key]').forEach(function (list) {
    var k = 'boveda-check-' + list.getAttribute('data-key');
    var st = {};
    try { st = JSON.parse(store(k) || '{}') || {}; } catch (e) { st = {}; }
    list.querySelectorAll('input[type=checkbox]').forEach(function (cb) {
      cb.checked = !!st[cb.id];
      cb.addEventListener('change', function () { st[cb.id] = cb.checked; store(k, JSON.stringify(st)); });
    });
  });
})();
