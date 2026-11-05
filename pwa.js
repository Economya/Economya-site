/* Economya : installation sur l'écran d'accueil (PWA).
   - enregistre le service worker ;
   - propose, de façon discrète, « Installer Economya » quand le navigateur le permet (Chrome / Android).
   Le bouton n'apparaît que : hors application installée, après réponse au bandeau cookies,
   8 secondes après l'arrivée, et plus du tout pendant 30 jours si la personne le ferme. */
(function () {
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
      navigator.serviceWorker.register('/sw.js').catch(function () {});
    });
  }

  var standalone = (window.matchMedia && window.matchMedia('(display-mode: standalone)').matches) || window.navigator.standalone;
  if (standalone) return;

  var DISMISS_KEY = 'eco_install_dismissed';
  var CONSENT_KEY = 'economya_cookie_consent_v2';
  try {
    var t = parseInt(localStorage.getItem(DISMISS_KEY) || '0', 10);
    if (t && Date.now() - t < 30 * 24 * 3600 * 1000) return;
  } catch (e) {}

  var deferred = null;
  var timer = null;

  function consentAnswered() {
    try { return !!localStorage.getItem(CONSENT_KEY); } catch (e) { return true; }
  }
  function dismiss() {
    try { localStorage.setItem(DISMISS_KEY, String(Date.now())); } catch (e) {}
    remove();
  }
  function remove() {
    var el = document.getElementById('eco-install');
    if (el && el.parentNode) el.parentNode.removeChild(el);
  }
  function track(name) {
    if (typeof gtag === 'function') { try { gtag('event', name); } catch (e) {} }
  }

  function build() {
    if (document.getElementById('eco-install') || !deferred) return;
    var st = document.createElement('style');
    st.textContent =
      '#eco-install{position:fixed;left:14px;bottom:14px;z-index:90;display:flex;align-items:center;gap:2px;background:#085041;color:#fff;border-radius:99px;padding:3px 3px 3px 4px;font:600 12.5px system-ui,-apple-system,sans-serif;box-shadow:0 6px 18px -6px rgba(0,0,0,.4);opacity:0;transform:translateY(8px);animation:ecoInstallIn .35s .05s forwards}' +
      '#eco-install button{font:inherit;color:inherit;background:none;border:0;cursor:pointer}' +
      '#eco-install .go{padding:8px 8px 8px 12px}' +
      '#eco-install .x{padding:8px 10px;opacity:.7;font-size:13px}' +
      '#eco-install .x:hover,#eco-install .go:hover{opacity:1}' +
      '@keyframes ecoInstallIn{to{opacity:1;transform:none}}' +
      'body:has(.modal-bg.open) #eco-install{display:none}' +
      '@media (prefers-reduced-motion:reduce){#eco-install{animation:none;opacity:1;transform:none}}';
    document.head.appendChild(st);
    var box = document.createElement('div');
    box.id = 'eco-install';
    box.setAttribute('role', 'region');
    box.setAttribute('aria-label', 'Installer Economya');
    var go = document.createElement('button');
    go.type = 'button'; go.className = 'go'; go.textContent = '📲 Installer Economya';
    var x = document.createElement('button');
    x.type = 'button'; x.className = 'x'; x.setAttribute('aria-label', 'Fermer'); x.textContent = '✕';
    go.addEventListener('click', function () {
      var ev = deferred; deferred = null;
      track('pwa_install_click');
      if (!ev || !ev.prompt) { remove(); return; }
      ev.prompt();
      if (ev.userChoice && ev.userChoice.then) {
        ev.userChoice.then(function (c) {
          track(c && c.outcome === 'accepted' ? 'pwa_install_accepted' : 'pwa_install_dismissed');
          if (!c || c.outcome !== 'accepted') dismiss(); else remove();
        });
      } else { remove(); }
    });
    x.addEventListener('click', dismiss);
    box.appendChild(go); box.appendChild(x);
    document.body.appendChild(box);
  }

  function schedule() {
    var tries = 0;
    timer = setInterval(function () {
      tries++;
      if (consentAnswered()) { clearInterval(timer); build(); }
      else if (tries > 40) { clearInterval(timer); }
    }, 2000);
  }

  window.addEventListener('beforeinstallprompt', function (e) {
    e.preventDefault();
    deferred = e;
    setTimeout(schedule, 8000);
  });
  window.addEventListener('appinstalled', function () {
    try { localStorage.setItem(DISMISS_KEY, String(Date.now())); } catch (e) {}
    remove();
    track('pwa_installed');
  });
})();
