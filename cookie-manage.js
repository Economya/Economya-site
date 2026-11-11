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
        // Si un élément du bandeau de score se trouve sous la flèche, on le décale d'un cran vers la gauche.
        var tries = 0;
        var clearCorner = function () {
          var list = document.querySelectorAll("#hud,.hud,.hud-row,.hud-top,.game-meta,#boardTrack");
          for (var j = 0; j < list.length; j++) {
            var el = list[j];
            if (el.getAttribute("data-eco-pad")) continue;
            var r = el.getBoundingClientRect();
            if (r.width < 2 || r.height < 2 || r.top > 44 || r.bottom < 8 || r.right < window.innerWidth - 50) continue;
            if (el.querySelector(".hud-row,.hud-top")) continue; // on décale la ligne intérieure, pas le conteneur
            el.setAttribute("data-eco-pad", "1");
            el.style.boxSizing = "border-box";
            el.style.paddingRight = "50px";
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
