// Economya.fr — indicateur de compte partagé pour les pages hors-forum
// (index.html, community.html, astuce.html…). Lit la session déjà posée
// en localStorage par forum-astuces.html (clés eco_user / eco_session) :
// pas de nouvelle logique d'authentification, juste un reflet de l'état,
// avec un mini menu (profil + déconnexion directe) façon compte utilisateur.
(function () {
  var scriptEl = document.currentScript;
  var hideId = scriptEl && scriptEl.getAttribute('data-hide-when-logged-in');

  var PALETTE = [
    ['#F59E0B', '#1A0A00'], ['#22C55E', '#fff'], ['#3B82F6', '#fff'],
    ['#8B5CF6', '#fff'], ['#EC4899', '#fff'], ['#F97316', '#fff'],
    ['#14B8A6', '#fff'], ['#6366F1', '#fff']
  ];
  function pc(name) { return PALETTE[(name || '?').charCodeAt(0) % PALETTE.length]; }
  function ini(name) {
    return (name || '?').split(' ').map(function (w) { return w[0]; }).join('').toUpperCase().slice(0, 2);
  }

  function getUser() {
    try {
      var u = localStorage.getItem('eco_user');
      var s = JSON.parse(localStorage.getItem('eco_session') || 'null');
      if (u && s && s.access_token) return u;
    } catch (e) {}
    return null;
  }

  function logout() {
    try {
      localStorage.removeItem('eco_session');
      localStorage.removeItem('eco_user');
    } catch (e) {}
    window.location.href = '/index.html';
  }

  function injectStyleOnce() {
    if (document.getElementById('ecoNavAvStyle')) return;
    var st = document.createElement('style');
    st.id = 'ecoNavAvStyle';
    st.textContent =
      '.eco-navav-trigger{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;' +
      'font-weight:800;font-size:12px;cursor:pointer;box-shadow:0 2px 6px rgba(0,0,0,.15);transition:transform .15s ease,box-shadow .15s ease;border:none;font-family:inherit}' +
      '.eco-navav-trigger:hover{transform:translateY(-1px);box-shadow:0 4px 10px rgba(0,0,0,.2)}' +
      '.eco-navav-login{display:inline-flex;align-items:center;gap:6px;background:#1A0A00;color:#fff;border-radius:99px;' +
      'padding:7px 14px;font-size:13px;font-weight:700;text-decoration:none;white-space:nowrap;transition:transform .15s ease,background .15s ease}' +
      '.eco-navav-login:hover{transform:translateY(-1px);background:#000}' +
      '.eco-navav-menu{position:absolute;right:0;top:calc(100% + 10px);background:#fff;border:1px solid rgba(0,0,0,.08);' +
      'border-radius:14px;box-shadow:0 12px 28px rgba(0,0,0,.14);min-width:190px;overflow:hidden;z-index:500;' +
      'opacity:0;transform:translateY(-6px) scale(.98);pointer-events:none;transition:opacity .15s ease,transform .15s ease}' +
      '.eco-navav-menu.open{opacity:1;transform:translateY(0) scale(1);pointer-events:auto}' +
      '.eco-navav-menu .hd{padding:12px 14px;font-weight:700;font-size:13px;color:#2C2C2A;border-bottom:1px solid rgba(0,0,0,.06);' +
      'display:flex;align-items:center;gap:8px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}' +
      '.eco-navav-menu a, .eco-navav-menu button{display:flex;align-items:center;gap:8px;width:100%;padding:10px 14px;' +
      'font-size:13px;font-weight:600;color:#2C2C2A;text-decoration:none;background:none;border:none;cursor:pointer;' +
      'text-align:left;font-family:inherit;transition:background .12s ease}' +
      '.eco-navav-menu a:hover, .eco-navav-menu button:hover{background:#F7F7F5}' +
      '.eco-navav-menu button.danger{color:#DC2626}';
    document.head.appendChild(st);
  }

  function closeAllMenus() {
    var open = document.querySelectorAll('.eco-navav-menu.open');
    for (var i = 0; i < open.length; i++) open[i].classList.remove('open');
  }

  function renderDesktop(el, user) {
    if (user) {
      var c = pc(user);
      el.style.position = 'relative';
      el.innerHTML =
        '<button type="button" class="eco-navav-trigger" style="background:' + c[0] + ';color:' + c[1] + '">' + ini(user) + '</button>' +
        '<div class="eco-navav-menu">' +
        '  <div class="hd">👋 ' + user + '</div>' +
        '  <a href="/profil/' + encodeURIComponent(user) + '">👤 Mon profil</a>' +
        '  <button type="button" class="danger">🚪 Déconnexion</button>' +
        '</div>';
      var trigger = el.querySelector('.eco-navav-trigger');
      var menu = el.querySelector('.eco-navav-menu');
      trigger.addEventListener('click', function (e) {
        e.stopPropagation();
        var wasOpen = menu.classList.contains('open');
        closeAllMenus();
        if (!wasOpen) menu.classList.add('open');
      });
      el.querySelector('.danger').addEventListener('click', function (e) {
        e.preventDefault();
        logout();
      });
    } else {
      el.style.position = '';
      el.innerHTML = '<a href="/forum-astuces.html" class="eco-navav-login">👤 Mon compte</a>';
    }
  }

  function renderMobile(el, user) {
    if (user) {
      el.textContent = '👤 Mon profil';
      el.setAttribute('href', '/profil/' + encodeURIComponent(user));
    } else {
      el.textContent = '👤 Mon compte';
      el.setAttribute('href', '/forum-astuces.html');
    }
    var lo = document.getElementById('navAvMobileLogout');
    if (lo) {
      lo.style.display = user ? '' : 'none';
      if (!lo._bound) {
        lo._bound = true;
        lo.addEventListener('click', function (e) { e.preventDefault(); logout(); });
      }
    }
  }

  function render() {
    injectStyleOnce();
    var user = getUser();
    var d = document.getElementById('navAv');
    if (d) renderDesktop(d, user);
    var m = document.getElementById('navAvMobile');
    if (m) renderMobile(m, user);
    if (hideId) {
      var h = document.getElementById(hideId);
      if (h) h.style.display = user ? 'none' : '';
    }
  }

  document.addEventListener('click', closeAllMenus);

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', render);
  } else {
    render();
  }
})();
