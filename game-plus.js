/* Economya : enrichissement commun des jeux.
   - sons et vibrations (bouton 🔊 pour couper, choix mémorisé) ;
   - médailles bronze / argent / or selon le score, conservées d'une visite à l'autre ;
   - en fin de partie : objectif suivant et trois autres jeux à essayer ;
   - sur la page /jeux : médailles gagnées affichées sur chaque carte.
   Chargé automatiquement par cookie-manage.js sur les pages de jeu. Aucun jeu n'est modifié : le script observe
   le score, les vies et l'écran de fin déjà présents dans la page (table CFG ci-dessous). */
(function () {
  "use strict";
  if (window.__ecoPlus) return;
  window.__ecoPlus = true;

  var slug = location.pathname.replace(/\.html$/, "").replace(/\/+$/, "").split("/").pop() || "";

  // [adresse, titre, famille]  familles : a = arcade, g = gestion, q = quiz, p = profil
  var GAMES = [["inflation-run", "Inflation Run", "a"], ["ou-vivre-mieux", "Où vivre mieux ?", "q"], ["calendrier-bons-plans", "Calendrier des Bons Plans", "q"], ["le-bon-deal", "Le Bon Deal", "q"], ["le-negociateur", "Le Négociateur", "g"], ["roue-economies", "La Roue des Économies", "q"], ["jackpot-finance", "Jackpot Finance", "q"], ["vrai-ou-faux", "Vrai ou Faux Finance", "q"], ["finance-wrapped", "Finance Wrapped 2026", "p"], ["aura-financiere", "Ton Aura Financière", "p"], ["investisseur-virtuel", "L'Investisseur Virtuel", "g"], ["primo-accedant", "Parcours Primo-Accédant", "g"], ["budget-tower", "Budget Tower", "a"], ["radar-arnaques", "Le Radar à Arnaques", "q"], ["tas-combien-dans-les-mains", "T'as combien dans les mains ?", "q"], ["attrape-economies", "Attrape tes Économies", "a"], ["boule-de-patrimoine", "Boule de Patrimoine", "a"], ["sprint-epargne", "Sprint de l'Épargne", "a"], ["tri-de-budget", "Tri de Budget", "a"], ["grand-prix-epargne", "Grand Prix de l'Épargne", "a"], ["eclateur-de-dettes", "Éclateur de Dettes", "a"], ["casse-tes-dettes", "Casse tes Dettes", "a"], ["le-gestionnaire-de-crise", "Le Gestionnaire de Crise", "a"], ["le-marche-vivant", "Le Marché Vivant", "g"], ["la-roue-des-scenarios", "La Roue des Scénarios", "g"], ["le-grand-cycle-economique", "Le Grand Cycle Économique", "g"], ["la-machine-a-reves", "La Machine à Rêves", "p"], ["ton-annee-bons-plans", "Ton Année Bons Plans", "p"], ["ton-totem-financier", "Ton Totem Financier", "p"], ["le-trophee-du-jour", "Le Trophée du Jour", "p"], ["le-sosie-celebre-de-ton-epargne", "Le Sosie Célèbre de ton Épargne", "p"], ["le-mur-des-bravos", "Le Mur des Bravos", "p"], ["chef-econome", "Chef Économe", "a"], ["coach-econome", "Coach Économe", "g"], ["chef-resto-v2", "Chef Resto", "g"], ["marathon-budgetaire-v2", "Marathon Budgétaire", "g"], ["finance-runner-3d-v2", "Finance Runner 3D", "a"], ["bar-de-plage", "Bar de Plage", "g"], ["domaine-viticole", "Domaine Viticole", "g"], ["hotel-manager", "Hôtel Manager", "g"], ["memory-finance", "Memory Finance", "a"], ["budget-run", "Budget Run", "a"], ["happy-budget", "Happy Budget", "a"], ["prix-party", "Prix Party", "q"], ["ile-aux-oeufs", "L'Île aux Œufs", "g"], ["pile-ou-face-financier", "Pile ou Face Financier", "q"]];

  // end : écran de fin · score : score final · live : score en cours · lives : vies
  // m : seuils [bronze, argent, or] · low : plus petit = meilleur · u : unité affichée · at : où insérer le panneau
  var CFG = {
    "attrape-economies": {"end": "#screen-over", "score": "#goScore", "live": "#hudScore", "lives": "#hudLives", "u": "pts", "m": [150, 350, 700]},
    "boule-de-patrimoine": {"end": "#screen-over", "score": "#goScore", "live": "#hudSize", "u": "€", "m": [500, 2500, 10000]},
    "budget-run": {"end": "#ovOver", "score": "#ovScore", "u": "pièces", "m": [150, 350, 700]},
    "budget-tower": {"end": "#screen-over", "score": "#goScore", "live": "#hudScore", "u": "mois", "m": [5, 10, 18]},
    "casse-tes-dettes": {"end": "#screen-over", "score": "#goScore", "live": "#hudScore", "lives": "#hudLives", "u": "pts", "m": [150, 350, 800]},
    "eclateur-de-dettes": {"end": "#screen-over", "score": "#goScore", "live": "#hudScore", "lives": "#hudLives", "u": "pts", "m": [150, 400, 900]},
    "finance-runner-3d-v2": {"end": "#screen-over", "score": "#goScore", "live": "#hudScore", "lives": "#hudLives", "u": "pièces", "m": [15, 35, 70]},
    "grand-prix-epargne": {"end": "#screen-over", "score": "#goScore", "live": "#hudScore", "lives": "#hudLives", "u": "pts", "m": [640, 950, 1300]},
    "happy-budget": {"end": "#oOver", "score": "#sScore", "u": "€", "m": [2000, 6000, 15000]},
    "sprint-epargne": {"end": "#screen-over", "score": "#goScore", "live": "#hudCoins", "lives": "#hudLives", "u": "pièces", "m": [15, 40, 80]},
    "tri-de-budget": {"end": "#screen-over", "score": "#goScore", "live": "#hudScore", "lives": "#hudLives", "u": "pts", "m": [10, 20, 35]},
    "le-gestionnaire-de-crise": {"end": "#screen-over", "score": "#goScore", "live": "#hudScore", "u": "pts", "m": [500, 1000, 1800]},
    "chef-econome": {"end": "#screen-result", "score": "#resultScore", "live": "#scoreDisplay", "u": "pts", "m": [90, 140, 190]},
    "inflation-run": {"end": "#btn-restart", "score": "#hud-score", "live": "#hud-savings", "lives": "#hud-lives", "at": ".controls", "u": "pts", "m": [800, 1800, 3600]},
    "memory-finance": {"end": "#screen-end", "score": "#endTime", "low": true, "m": [60, 40, 25], "u": "s"},
    "ile-aux-oeufs": {"end": "#screen-over", "score": "#goScore", "m": [3, 5, 7], "u": "œufs"},
    "la-roue-des-scenarios": {"end": "#screen-over", "score": "#goScore", "m": [430, 600, 920], "u": "pts"},
    "le-grand-cycle-economique": {"end": "#screen-over", "score": "#goScore", "m": [95, 135, 210], "u": "pts"},
    "le-marche-vivant": {"end": "#screen-over", "score": "#goScore", "u": "pts", "m": [1030, 1070, 1120]},
    "bar-de-plage": {"end": "#screen-end", "score": "#endCA", "u": "€", "m": [6000, 10000, 15000]},
    "chef-resto-v2": {"end": "#screen-end", "score": "#endCA", "live": "#hudCA", "u": "€", "m": [800, 1200, 1700]},
    "coach-econome": {"end": "#screen-end", "score": "#endPerf", "u": "%", "m": [35, 50, 70]},
    "domaine-viticole": {"end": "#screen-end", "score": "#endScore", "m": [50000, 80000, 150000], "u": "€"},
    "hotel-manager": {"end": "#screen-end", "score": "#endScore", "m": [10, 30, 60], "u": "% de CA"},
    "marathon-budgetaire-v2": {"end": "#screen-end", "score": "#endPerf", "m": [50, 70, 85], "u": "%"},
    "le-negociateur": {"end": "#screen-final"},
    "investisseur-virtuel": {"end": "#screen-final"},
    "radar-arnaques": {"end": "#screen-result", "score": "#resultScore", "m": [6, 8, 10], "u": "bonnes réponses"},
    "le-bon-deal": {"end": "#results-screen", "score": "#resScore", "m": [2000, 3500, 5000], "u": "€"},
    "vrai-ou-faux": {"end": "#screen-results", "score": "#r-score", "u": "pts", "m": [600, 1000, 1400]},
    "prix-party": {"end": "#screen-final", "score": "#totalScore", "u": "pts", "m": [250, 350, 430]},
    "tas-combien-dans-les-mains": {"end": "#screen-result", "score": "#finalPct", "m": [50, 70, 85], "u": "%"},
    "pile-ou-face-financier": {"end": "#screen-result"},
    "aura-financiere": {"end": "#result"},
    "le-sosie-celebre-de-ton-epargne": {"end": "#screen-result"},
    "ton-totem-financier": {"end": "#screen-result"},
    "ton-annee-bons-plans": {"end": "#card-final"}
  };

  var KEY_MED = "economya_medailles", KEY_SND = "economya_son";
  function load(k, d) { try { var v = JSON.parse(localStorage.getItem(k)); return v == null ? d : v; } catch (e) { return d; } }
  function save(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function q(sel) { try { return sel ? document.querySelector(sel) : null; } catch (e) { return null; } }
  function visible(el) {
    if (!el || !el.getClientRects().length) return false;
    var cs = getComputedStyle(el);
    return cs.visibility !== "hidden" && cs.display !== "none";
  }
  function num(el) {
    if (!el) return null;
    var t = (el.textContent || "").replace(/[\s  ]/g, "");
    var m = t.match(/-?\d+(?:[.,]\d+)?/);
    return m ? parseFloat(m[0].replace(",", ".")) : null;
  }
  function maxMedals(c) { return c && c.m ? 3 : 1; }
  function levelFor(c, score) {
    if (!c || !c.m) return 1;
    if (score == null || isNaN(score)) return 0;
    var n = 0;
    for (var i = 0; i < 3; i++) { if (c.low ? score <= c.m[i] : score >= c.m[i]) n = i + 1; }
    return n;
  }
  function fmt(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, " "); }

  /* ---------- Page /jeux : médailles sur les cartes ---------- */
  if (slug === "jeux") {
    var store = load(KEY_MED, {}), total = 0, got = 0;
    var cards = document.querySelectorAll("a.game-card[href]");
    for (var i = 0; i < cards.length; i++) {
      var s = (cards[i].getAttribute("href") || "").replace(/^\//, "");
      var c = CFG[s]; if (!c) continue;
      var mx = maxMedals(c), lv = Math.min(mx, store[s] || 0);
      total += mx; got += lv;
      var thumb = cards[i].querySelector(".game-thumb"); if (!thumb) continue;
      var b = document.createElement("div");
      b.setAttribute("aria-label", lv + " médaille" + (lv > 1 ? "s" : "") + " sur " + mx);
      b.style.cssText = "position:absolute;right:10px;bottom:10px;z-index:4;background:rgba(0,0,0,.55);border-radius:999px;padding:3px 8px;font-size:13px;line-height:1.2;letter-spacing:1px";
      var icons = mx === 3 ? ["🥉", "🥈", "🥇"] : ["🎖️"], h = "";
      for (var k = 0; k < icons.length; k++) h += '<span style="' + (k < lv ? "" : "opacity:.28;filter:grayscale(1)") + '">' + icons[k] + "</span>";
      b.innerHTML = h;
      if (getComputedStyle(thumb).position === "static") thumb.style.position = "relative";
      thumb.appendChild(b);
    }
    var title = document.querySelector(".section-title");
    if (title && total) {
      var line = document.createElement("div");
      line.style.cssText = "margin:-.4rem 0 1rem;font:600 .9rem 'DM Sans',system-ui,sans-serif;opacity:.85";
      line.textContent = "🏅 Mes médailles : " + got + " / " + total + (got ? "" : " — jouez pour gagner les premières !");
      title.parentNode.insertBefore(line, title.nextSibling);
    }
    return;
  }

  var cfg = CFG[slug];
  if (!cfg) return;

  /* ---------- Sons et vibrations ---------- */
  var soundOn = load(KEY_SND, true) !== false, actx = null;
  function audio() {
    if (!soundOn) return null;
    if (!actx) { var A = window.AudioContext || window.webkitAudioContext; if (!A) return null; try { actx = new A(); } catch (e) { return null; } }
    if (actx.state === "suspended") { try { actx.resume(); } catch (e) {} }
    return actx;
  }
  function tone(freq, dur, type, vol, delay, slideTo) {
    var a = audio(); if (!a) return;
    try {
      var o = a.createOscillator(), g = a.createGain(), t = a.currentTime + (delay || 0);
      o.type = type || "sine";
      o.frequency.setValueAtTime(freq, t);
      if (slideTo) o.frequency.exponentialRampToValueAtTime(slideTo, t + dur);
      g.gain.setValueAtTime(0.0001, t);
      g.gain.exponentialRampToValueAtTime(vol || 0.07, t + 0.012);
      g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
      o.connect(g); g.connect(a.destination);
      o.start(t); o.stop(t + dur + 0.03);
    } catch (e) {}
  }
  function buzz(p) { if (soundOn && navigator.vibrate) { try { navigator.vibrate(p); } catch (e) {} } }
  var lastGood = 0;
  var fx = {
    good: function () { var n = Date.now(); if (n - lastGood < 70) return; lastGood = n; tone(880, 0.09, "triangle", 0.06); tone(1320, 0.11, "triangle", 0.05, 0.06); },
    bad: function () { tone(190, 0.22, "sawtooth", 0.07, 0, 90); buzz(70); },
    win: function () { [523, 659, 784, 1047].forEach(function (f, i) { tone(f, 0.16, "triangle", 0.07, i * 0.11); }); },
    medal: function () { [523, 659, 784, 1047, 1319].forEach(function (f, i) { tone(f, 0.2, "triangle", 0.08, i * 0.1); }); tone(1568, 0.5, "sine", 0.06, 0.55); buzz([40, 60, 40]); },
    lose: function () { tone(392, 0.2, "triangle", 0.06); tone(294, 0.3, "triangle", 0.06, 0.18); },
    tap: function () { tone(660, 0.04, "square", 0.025); }
  };
  window.EcoFx = fx; // utilisable par un jeu qui veut déclencher lui-même un son

  // Le navigateur n'autorise le son qu'après un geste du joueur
  function unlock() { audio(); }
  document.addEventListener("pointerdown", unlock, true);
  document.addEventListener("keydown", unlock, true);
  // petit clic sur les boutons
  document.addEventListener("click", function (e) {
    var t = e.target && e.target.closest ? e.target.closest("button,.btn") : null;
    if (t && !t.closest("#economya-cookie-banner") && t.id !== "eco-son") fx.tap();
  }, true);

  function addSoundButton() {
    var b = document.createElement("button");
    b.id = "eco-son"; b.type = "button";
    var hasBack = !!document.querySelector('a[aria-label="Retour aux jeux Economya"]');
    b.style.cssText = "position:fixed;z-index:999998;width:34px;height:34px;border-radius:50%;border:1px solid rgba(255,255,255,.25);background:rgba(0,0,0,.6);color:#fff;font-size:15px;line-height:1;cursor:pointer;padding:0;opacity:.78;" + (hasBack ? "top:8px;right:48px;display:none" : "bottom:16px;left:12px");
    // Sur les jeux plein écran, le bouton apparaît à côté de la flèche retour dès que la partie commence.
    if (hasBack) { var iv = setInterval(function () { if (document.documentElement.classList.contains("economya-play-mode")) { b.style.display = ""; clearInterval(iv); } }, 250); }
    function paint() { b.textContent = soundOn ? "🔊" : "🔇"; b.setAttribute("aria-label", soundOn ? "Couper le son" : "Activer le son"); b.title = b.getAttribute("aria-label"); }
    b.addEventListener("click", function (e) { e.stopPropagation(); soundOn = !soundOn; save(KEY_SND, soundOn); paint(); if (soundOn) fx.good(); });
    paint();
    document.body.appendChild(b);
  }

  /* ---------- Panneau de fin : médailles + autres jeux ---------- */
  function suggestions() {
    var me = null, same = [], others = [];
    GAMES.forEach(function (g) { if (g[0] === slug) me = g; });
    GAMES.forEach(function (g) { if (g[0] === slug) return; (me && g[2] === me[2] ? same : others).push(g); });
    var seed = new Date().getDate() + slug.length, pick = [];
    function take(list, n) { for (var i = 0; i < n && list.length; i++) { pick.push(list.splice((seed + i * 7) % list.length, 1)[0]); } }
    take(same, 2); take(others, 1);
    return pick;
  }
  // Couleur du texte du panneau : claire sur fond sombre, sombre sur fond clair (on lit le fond réel de l'écran de fin).
  function isDarkBehind(el) {
    for (var n = el; n && n.nodeType === 1; n = n.parentNode) {
      var cs = getComputedStyle(n), src = cs.backgroundColor, m = src && src.match(/rgba?\(([^)]+)\)/);
      var parts = m ? m[1].split(",").map(parseFloat) : null;
      if (!parts || (parts.length > 3 && parts[3] < 0.5)) {
        var g = cs.backgroundImage && cs.backgroundImage.indexOf("gradient") >= 0 ? cs.backgroundImage.match(/rgba?\(([^)]+)\)/) : null;
        parts = g ? g[1].split(",").map(parseFloat) : null;
        if (parts && parts.length > 3 && parts[3] < 0.5) parts = null;
      }
      if (parts) return (0.299 * parts[0] + 0.587 * parts[1] + 0.114 * parts[2]) < 140;
    }
    return true;
  }
  var ICON = { a: "🕹️", g: "📈", q: "❓", p: "✨" };
  function renderPanel(score) {
    var old = document.getElementById("eco-plus"); if (old) old.parentNode.removeChild(old);
    var store = load(KEY_MED, {}), prev = store[slug] || 0, lv = levelFor(cfg, score), isNew = lv > prev;
    if (isNew) { store[slug] = lv; save(KEY_MED, store); }
    var best = Math.max(prev, lv), box = document.createElement("div");
    box.id = "eco-plus";
    box.style.cssText = "margin:16px auto 6px;max-width:360px;width:100%;text-align:center;font-family:inherit;color:inherit";
    var h = "";
    if (cfg.m) {
      var names = ["bronze", "argent", "or"], icons = ["🥉", "🥈", "🥇"], u = cfg.u ? " " + cfg.u : "";
      h += '<div style="font-size:30px;letter-spacing:6px;line-height:1.1">';
      for (var i = 0; i < 3; i++) h += '<span style="' + (i < best ? "" : "opacity:.25;filter:grayscale(1)") + (isNew && i === lv - 1 ? ";display:inline-block;animation:ecoPop .6s ease" : "") + '">' + icons[i] + "</span>";
      h += "</div>";
      var msg;
      if (isNew) msg = "Nouvelle médaille : " + names[lv - 1] + " !";
      else if (lv > 0) msg = "Médaille " + (lv === 3 ? "d'or" : lv === 2 ? "d'argent" : "de bronze") + " sur cette partie.";
      else msg = "Pas de médaille cette fois.";
      if (best < 3) msg += " Objectif " + names[best] + " : " + (cfg.low ? "moins de " : "") + fmt(cfg.m[best]) + u + ".";
      else msg += " Toutes les médailles sont à vous 🎉";
      h += '<div style="font-size:13px;font-weight:600;margin-top:6px;opacity:.9">' + msg + "</div>";
    } else if (isNew) {
      h += '<div style="font-size:13px;font-weight:600;opacity:.9">🎖️ Jeu terminé : médaille ajoutée à votre collection.</div>';
    }
    var sug = suggestions();
    h += '<div style="margin-top:14px;font-size:11px;letter-spacing:.08em;text-transform:uppercase;opacity:.65;font-weight:700">Encore un jeu ?</div><div style="display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin-top:8px">';
    sug.forEach(function (g) {
      h += '<a href="/' + g[0] + '" style="background:rgba(127,127,127,.16);border:1px solid rgba(127,127,127,.38);color:inherit;border-radius:999px;padding:7px 12px;font-size:12.5px;font-weight:600;text-decoration:none;line-height:1.2">' + ICON[g[2]] + " " + g[1] + "</a>";
    });
    h += "</div>";
    box.innerHTML = h;
    var end = q(cfg.end), at = q(cfg.at);
    if (at && at.parentNode) at.parentNode.insertBefore(box, at.nextSibling);
    else if (end) {
      var foot = end.querySelector(".brand-footer");
      if (foot && foot.parentNode) foot.parentNode.insertBefore(box, foot); else end.appendChild(box);
    }
    if (box.parentNode) box.style.color = isDarkBehind(box.parentNode) ? "#f3f3f3" : "#1d1d1d";
    if (isNew && cfg.m) fx.medal(); else if (lv > 0) fx.win(); else fx.lose();
    (window.__ecoEnds = window.__ecoEnds || []).push(score);
  }

  /* ---------- Observation de la partie ---------- */
  function start() {
    var st = document.createElement("style");
    st.textContent = "@keyframes ecoPop{0%{transform:scale(.3) rotate(-20deg)}60%{transform:scale(1.35) rotate(8deg)}100%{transform:scale(1) rotate(0)}}";
    document.head.appendChild(st);
    addSoundButton();
    var wasEnd = false, lastScore = null, lastLives = null;
    function hearts(el) { if (!el) return null; var t = el.textContent || "", n = (t.match(/❤/g) || []).length; return n || (t.indexOf("🖤") >= 0 ? 0 : num(el)); }
    setInterval(function () {
      var endEl = q(cfg.end), isEnd = visible(endEl);
      if (isEnd && !wasEnd) renderPanel(num(q(cfg.score)));
      if (!isEnd && wasEnd) { var op = document.getElementById("eco-plus"); if (op && op.parentNode) op.parentNode.removeChild(op); }
      wasEnd = isEnd;
      if (isEnd) { lastScore = null; lastLives = null; return; }
      if (cfg.live) { var s = num(q(cfg.live)); if (s != null && lastScore != null && s > lastScore) fx.good(); lastScore = s; }
      if (cfg.lives) { var l = hearts(q(cfg.lives)); if (l != null && lastLives != null && l < lastLives) fx.bad(); lastLives = l; }
    }, 200);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();
