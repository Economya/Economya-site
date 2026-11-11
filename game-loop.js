/* Economya : cadence de jeu constante.
   Les jeux d'arcade avancent d'un pas par image affichée. Sans ce script, ils vont jusqu'à 2 fois plus vite
   sur un écran 90/120/144 Hz et au ralenti sur un appareil lent ou en mode économie d'énergie (30 images/s).
   Ici, la boucle du jeu est rappelée 60 fois par seconde en moyenne, quelle que soit la fréquence de l'écran.
   À charger AVANT le script du jeu. Aucun effet sur un écran 60 Hz classique. */
(function () {
  if (!window.requestAnimationFrame || window.__ecoGameLoop) return;
  window.__ecoGameLoop = true;
  var nativeRaf = window.requestAnimationFrame.bind(window);
  var STEP = 1000 / 60;      // durée d'un pas de jeu
  var MAX_STEPS = 3;         // rattrapage maximum par image (évite l'emballement au retour d'un onglet)
  var queue = [];            // rappels en attente du prochain pas
  var nextId = 1;
  var acc = 0, last = 0, vtime = 0, scheduled = false;

  function ensure() {
    if (!scheduled) { scheduled = true; nativeRaf(frame); }
  }

  function frame(now) {
    scheduled = false;
    if (!last) {
      // première image (ou reprise après une pause) : un pas tout de suite
      vtime = Math.max(vtime, now);
      acc = STEP;
    } else {
      var d = now - last;
      if (Math.abs(d - STEP) < 2.5) d = STEP;         // écran 60 Hz : exactement un pas par image
      acc = Math.min(acc + d, STEP * MAX_STEPS);
    }
    last = now;
    var steps = 0;
    while (acc >= STEP - 0.5 && steps < MAX_STEPS && queue.length) {
      acc -= STEP;
      steps++;
      vtime += STEP;
      var run = queue;
      queue = [];
      for (var i = 0; i < run.length; i++) {
        if (run[i].cancelled) continue;
        try { run[i].fn(vtime); }
        catch (e) { (function (err) { setTimeout(function () { throw err; }, 0); })(e); }
      }
    }
    if (queue.length) ensure();
    else { last = 0; acc = 0; }                        // plus rien à animer : on repart proprement plus tard
  }

  window.requestAnimationFrame = function (fn) {
    var id = nextId++;
    queue.push({ id: id, fn: fn, cancelled: false });
    ensure();
    return id;
  };
  window.cancelAnimationFrame = function (id) {
    for (var i = 0; i < queue.length; i++) {
      if (queue[i].id === id) { queue[i].cancelled = true; break; }
    }
  };
})();
