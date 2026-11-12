/* Lien « Gérer mes cookies » : permet de modifier ou retirer son consentement à tout moment. */
/* Copie dans le presse-papiers : ne plante plus quand le navigateur la refuse (navigation privée, appli intégrée,
   ancien navigateur). On retombe sur l'ancienne méthode, et en dernier recours on affiche le texte à copier.
   Les confirmations « copié » s'affichent dans une petite bulle au lieu d'une fenêtre bloquante. */
(function () {
  function toast(msg) {
    try {
      var t = document.getElementById("economya-toast");
      if (!t) {
        t = document.createElement("div");
        t.id = "economya-toast";
        t.setAttribute("role", "status");
        t.style.cssText = "position:fixed;left:50%;bottom:28px;transform:translateX(-50%);z-index:100000;background:#085041;color:#fff;padding:10px 18px;border-radius:999px;font:600 14px system-ui,-apple-system,sans-serif;box-shadow:0 6px 20px rgba(0,0,0,.3);max-width:86vw;text-align:center;transition:opacity .3s;opacity:0;pointer-events:none";
        document.body.appendChild(t);
      }
      t.textContent = msg;
      t.style.opacity = "1";
      clearTimeout(t._h);
      t._h = setTimeout(function () { t.style.opacity = "0"; }, 2200);
    } catch (e) {}
  }
  function legacyCopy(text) {
    return new Promise(function (resolve, reject) {
      try {
        var ta = document.createElement("textarea");
        ta.value = text;
        ta.setAttribute("readonly", "");
        ta.style.cssText = "position:fixed;top:0;left:0;opacity:0";
        document.body.appendChild(ta);
        ta.select();
        ta.setSelectionRange(0, text.length);
        var ok = document.execCommand("copy");
        document.body.removeChild(ta);
        if (ok) resolve(); else reject(new Error("copy"));
      } catch (e) { reject(e); }
    });
  }
  function lastResort(text) {
    try { window.prompt("Copiez ce texte :", text); } catch (e) {}
    return new Promise(function () {}); // on ne confirme pas une copie qui n'a pas eu lieu
  }
  try {
    var c = navigator.clipboard;
    if (c && c.writeText) {
      var orig = c.writeText.bind(c);
      c.writeText = function (text) {
        text = String(text);
        return orig(text).catch(function () { return legacyCopy(text); }).catch(function () { return lastResort(text); });
      };
    } else {
      Object.defineProperty(navigator, "clipboard", {
        configurable: true,
        value: { writeText: function (text) { text = String(text); return legacyCopy(text).catch(function () { return lastResort(text); }); } }
      });
    }
  } catch (e) {}
  try {
    var nativeAlert = window.alert;
    window.alert = function (msg) {
      if (/copi[ée]/i.test(String(msg))) toast(String(msg));
      else nativeAlert.call(window, msg);
    };
  } catch (e) {}
})();

(function () {
  var K = "economya_cookie_consent_v2";
  // PWA : service worker et bouton « Installer Economya » (voir pwa.js)
  try { var pw = document.createElement("script"); pw.src = "/pwa.js"; pw.defer = true; document.head.appendChild(pw); } catch (e) {}
  // Jeux : sons, médailles et suggestions (voir game-plus.js). Chargé seulement sur les pages de jeu et sur /jeux.
  try {
    var ecoPath = location.pathname.replace(/\.html$/, "").replace(/\/+$/, "");
    var ecoIsGame = ecoPath === "/jeux" || document.querySelector('a[aria-label="Retour aux jeux Economya"], a.nav-back[href="/jeux"], a.nav-back[href="/"]');
    if (ecoIsGame) { var gp = document.createElement("script"); gp.src = "/game-plus.js"; gp.defer = true; document.head.appendChild(gp); }
  } catch (e) {}
  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }
  ready(function () {
    var banner = document.getElementById("economya-cookie-banner");
    if (!banner) return;

    function openBanner(e) {
      if (e) e.preventDefault();
      var simple = document.getElementById("economya-cmp-simple");
      var cats = document.getElementById("economya-cmp-categories");
      var a = document.getElementById("economya-cat-analytics");
      var p = document.getElementById("economya-cat-publicite");
      try {
        var d = JSON.parse(localStorage.getItem(K) || "null");
        if (a) a.checked = !!(d && d.analytics);
        if (p) p.checked = !!(d && d.publicite);
      } catch (err) {}
      if (simple) simple.style.display = "none";
      if (cats) cats.style.display = "block";
      banner.style.display = "block";
    }

    var link = document.createElement("a");
    link.href = "#";
    link.id = "economya-cookie-manage";
    link.textContent = "Gérer mes cookies";
    link.addEventListener("click", openBanner);

    var footer = document.querySelector("footer");
    if (footer) {
      var holder = footer.querySelector("span") || footer;
      holder.appendChild(document.createTextNode(" · "));
      link.style.cssText = "color:rgba(255,255,255,.75);text-decoration:none";
      holder.appendChild(link);
    } else {
      // Pas de <footer> : on range le lien dans le bloc légal « © Economya » s'il existe (pages de jeu),
      // sinon on affiche une pastille flottante.
      var legalBlock = null;
      var ml = document.querySelectorAll('a[href="/mentions-legales"]');
      for (var i = 0; i < ml.length; i++) {
        var pr = ml[i].parentElement;
        if (pr && pr.tagName === "DIV" && /©/.test(pr.textContent) && !ml[i].getAttribute("aria-label")) { legalBlock = pr; break; }
      }
      if (legalBlock) {
        legalBlock.appendChild(document.createTextNode(" · "));
        link.style.cssText = "color:inherit;text-decoration:underline";
        legalBlock.appendChild(link);
      } else {
        link.style.cssText = "position:fixed;left:12px;bottom:12px;z-index:9000;background:#085041;color:#fff;padding:6px 12px;border-radius:999px;font-size:12px;text-decoration:none;opacity:.85;transition:opacity .3s";
        link.setAttribute("data-eco-float", "1");
        document.body.appendChild(link);
      }
    }

    // Jeux plein écran : dès la première action du joueur, on allège les boutons flottants
    // (retour, mentions, cookies) pour qu'ils ne masquent plus le score ni les commandes.
    // Ils sont tous visibles à l'arrivée sur la page ; le bouton retour reste cliquable (flèche compacte).
    var back = document.querySelector('a[aria-label="Retour aux jeux Economya"]');
    var info = document.querySelector('a[aria-label="Informations légales"]');
    var floating = link.getAttribute("data-eco-float") ? link : null;
    if (back || info || floating) {
      // Jeux plein écran : pas de zoom par double appui quand on tape vite (le pincement pour zoomer reste possible).
      if (back) { try { document.documentElement.style.touchAction = "manipulation"; } catch (e) {} }
      var played = false;
      var enterPlay = function (ev) {
        if (played) return;
        var t = ev && ev.target;
        if (t && t.closest && (t.closest("#economya-cookie-banner") || t === link || t === back || t === info)) return;
        played = true;
        document.documentElement.classList.add("economya-play-mode");
        if (back) {
          back.textContent = "←";
          back.title = "Retour aux jeux";
          back.style.padding = "0";
          back.style.width = "34px";
          back.style.height = "34px";
          back.style.justifyContent = "center";
          back.style.fontSize = "16px";
          back.style.top = "8px";
          back.style.right = "8px";
          back.style.opacity = ".72";
        }
        if (info) info.style.display = "none";
        // Si un élément du bandeau de score se trouve sous la flèche ou le bouton son, on le décale vers la gauche.
        var tries = 0;
        var clearCorner = function () {
          var list = document.querySelectorAll("#hud,.hud,.hud-row,.hud-top,.game-meta,#boardTrack");
          for (var j = 0; j < list.length; j++) {
            var el = list[j];
            if (el.getAttribute("data-eco-pad")) continue;
            var r = el.getBoundingClientRect();
            if (r.width < 2 || r.height < 2 || r.top > 44 || r.bottom < 8 || r.right < window.innerWidth - 92) continue;
            if (el.querySelector(".hud-row,.hud-top")) continue; // on décale la ligne intérieure, pas le conteneur
            el.setAttribute("data-eco-pad", "1");
            el.style.boxSizing = "border-box";
            el.style.paddingRight = "92px"; // place pour la flèche retour et le bouton son
          }
          if (++tries < 40) setTimeout(clearCorner, 750);
        };
        clearCorner();
        if (floating && banner.style.display === "none") floating.style.display = "none";
        document.removeEventListener("pointerdown", enterPlay, true);
        document.removeEventListener("keydown", enterPlay, true);
      };
      document.addEventListener("pointerdown", enterPlay, true);
      document.addEventListener("keydown", enterPlay, true);
    }
  });
})();

/* Confort sur téléphone (écrans tactiles uniquement) :
   - champs de saisie en 16 px minimum : sinon Safari iOS zoome automatiquement au toucher ;
   - zones à toucher agrandies (fil d'Ariane, boutons de partage, puces) ;
   - curseurs plus faciles à attraper (zone tactile de 32 px, piste visuelle inchangée). */
(function () {
  try {
    var css = "@media (hover:none) and (pointer:coarse){" +
      "input:not([type=range]):not([type=checkbox]):not([type=radio]):not([type=button]):not([type=submit]),select,textarea{font-size:16px!important}" +
      "[aria-label=\"Fil d'Ariane\"] a{display:inline-block;padding:.45rem .1rem}" +
      "a[href*=\"facebook.com/sharer\"],a[href*=\"twitter.com/intent\"],a[href*=\"linkedin.com/sharing\"],a[href^=\"whatsapp:\"],a[href*=\"pinterest.com/pin\"]{padding-top:.7rem!important;padding-bottom:.7rem!important}" +
      "html input[type=range][min]{box-sizing:content-box!important;padding:12px 0!important;margin-top:.2rem!important;margin-bottom:.2rem!important;background-clip:content-box!important}" +
      "#ecoCtaJoinBtn,#ecoNlJoinBtn{min-height:44px;display:inline-flex!important;align-items:center;justify-content:center}" +
      ".eco-cmp-chk{min-height:40px;display:inline-flex;align-items:center;gap:.4rem;padding:.2rem .5rem .2rem 0}" +
      "input[type=checkbox],input[type=radio]{min-width:22px;min-height:22px}" +
      "}";
    var st = document.createElement("style");
    st.id = "economya-touch";
    st.textContent = css;
    (document.head || document.documentElement).appendChild(st);
  } catch (e) {}
})();

/* Lisibilité (audit d'accessibilité) :
   - bouton « Voir les astuces » : texte foncé sur fond orange (contraste suffisant) ;
   - bandeau des liens légaux en bas de page : couleur adaptée au fond, clair ou sombre. */
(function () {
  try {
    var st = document.createElement("style");
    st.id = "economya-contraste";
    st.textContent = "#ecoCtaJoinBtn,#ecoNlJoinBtn{color:#2C2C2A!important}#economya-cookie-banner p,#economya-cookie-banner label{color:#fff!important}";
    (document.head || document.documentElement).appendChild(st);
  } catch (e) {}
  function fondSombre(el) {
    while (el && el.nodeType === 1) {
      var bg = getComputedStyle(el).backgroundColor, m = bg && bg.match(/rgba?\(([^)]+)\)/);
      if (m) { var p = m[1].split(",").map(parseFloat); if (p.length < 4 || p[3] > 0.5) return (0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) < 128; }
      el = el.parentElement;
    }
    return false;
  }
  function ajuster() {
    [].forEach.call(document.querySelectorAll('div[style*="color:#8a8a8a"]'), function (d) {
      if (!d.querySelector('a[href="/mentions-legales"]')) return;
      var c = fondSombre(d.parentElement) ? "#B4B4B4" : "#5F5E5A";
      d.style.color = c;
      [].forEach.call(d.querySelectorAll("a"), function (a) { a.style.color = c; });
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", ajuster); else ajuster();
})();
