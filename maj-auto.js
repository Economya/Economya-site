/* Affiche l'ancienneté de la dernière révision d'un comparateur et prévient automatiquement après 90 jours. */
(function () {
  try {
    var M = { janvier: 0, "février": 1, fevrier: 1, mars: 2, avril: 3, mai: 4, juin: 5, juillet: 6, "août": 7, aout: 7, septembre: 8, octobre: 9, novembre: 10, "décembre": 11, decembre: 11 };
    var notes = document.querySelectorAll(".maj-note");
    for (var i = 0; i < notes.length; i++) {
      var strong = notes[i].querySelector("strong");
      if (!strong) continue;
      var m = strong.textContent.match(/(\d{1,2})(?:er)?\s+([a-zéûè]+)\s+(\d{4})/i);
      if (!m || M[m[2].toLowerCase()] === undefined) continue;
      var d = new Date(+m[3], M[m[2].toLowerCase()], +m[1]);
      var jours = Math.floor((Date.now() - d.getTime()) / 86400000);
      if (isNaN(jours) || jours < 0) continue;
      var span = document.createElement("span");
      if (jours > 90) {
        span.style.cssText = "display:block;margin-top:.4rem;color:#92400e;font-weight:600";
        span.textContent = "⚠️ Cette page n'a pas été revérifiée depuis plus de 90 jours : contrôlez les chiffres sur le site de l'établissement avant de vous décider.";
      } else {
        span.style.cssText = "margin-left:.35rem;font-weight:400";
        span.textContent = jours <= 1 ? "(mise à jour récente)" : "(il y a " + jours + " jours)";
      }
      strong.parentNode.insertBefore(span, strong.nextSibling);
    }
  } catch (e) {}
})();
