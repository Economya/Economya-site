/* Lien « Gérer mes cookies » : permet de modifier ou retirer son consentement à tout moment. */
(function () {
  var K = "economya_cookie_consent_v2";
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
      link.style.cssText = "position:fixed;left:12px;bottom:12px;z-index:9000;background:#085041;color:#fff;padding:6px 12px;border-radius:999px;font-size:12px;text-decoration:none;opacity:.85";
      document.body.appendChild(link);
    }
  });
})();
