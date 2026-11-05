/* Economya - petites briques communes aux outils et comparateurs (sans dependance externe).
   1) EcoViz : barres, jauges et courbes en SVG/CSS  2) accessibilite, saisies et confort mobile. */
(function () {
  "use strict";
  var PAL = ["#F4B550", "#5EE0B5", "#9DB7FF", "#FF9AA2", "#D6C1FF", "#FFD98A"];
  function fmtN(n) { return Math.round(n).toLocaleString("fr-FR"); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  var E = (window.EcoViz = {});

  E.mount = function (id, afterSel) {
    var el = document.getElementById(id);
    if (el) return el;
    var ref = document.querySelector(afterSel || ".res-grid");
    if (!ref) return null;
    el = document.createElement("div");
    el.id = id; el.className = "eco-viz";
    ref.parentNode.insertBefore(el, ref.nextSibling);
    return el;
  };

  /* Barre segmentee + legende. parts = [{label, value, color?}] */
  E.stack = function (id, parts, o) {
    o = o || {};
    var h = E.mount(id, o.after); if (!h) return;
    parts = (parts || []).filter(function (p) { return p.value > 0 && isFinite(p.value); });
    var tot = 0; parts.forEach(function (p) { tot += p.value; });
    if (tot <= 0) { h.style.display = "none"; return; }
    h.style.display = "";
    var key = parts.map(function (p) { return p.label; }).join("|");
    var unit = o.unit === undefined ? " €" : o.unit;
    if (h._key !== key) {
      h._key = key;
      var bar = "", leg = "";
      parts.forEach(function (p, i) {
        var c = p.color || PAL[i % PAL.length];
        bar += '<span class="eco-seg" style="background:' + c + '"></span>';
        leg += '<li><i style="background:' + c + '"></i><span>' + esc(p.label) + "</span><b></b><em></em></li>";
      });
      h.innerHTML = (o.title ? '<div class="eco-viz-t">' + esc(o.title) + "</div>" : "") +
        '<div class="eco-stack" role="img"></div><ul class="eco-leg">' + leg + "</ul>";
      h.querySelector(".eco-stack").innerHTML = bar;
    }
    var segs = h.querySelectorAll(".eco-seg"), lis = h.querySelectorAll(".eco-leg li"), txt = [];
    parts.forEach(function (p, i) {
      var pc = p.value / tot * 100;
      segs[i].style.width = pc.toFixed(2) + "%";
      segs[i].title = p.label + " : " + fmtN(p.value) + unit;
      lis[i].querySelector("b").textContent = fmtN(p.value) + unit;
      lis[i].querySelector("em").textContent = Math.round(pc) + " %";
      txt.push(p.label + " " + Math.round(pc) + " %");
    });
    h.querySelector(".eco-stack").setAttribute("aria-label", (o.title ? o.title + " : " : "") + txt.join(", "));
  };

  /* Jauge avec repere. o = {title, value, max, limit, limitLabel, left, right, color} */
  E.gauge = function (id, o) {
    var h = E.mount(id, o.after); if (!h) return;
    var pc = Math.max(0, Math.min(100, o.value / o.max * 100));
    var lim = o.limit != null ? Math.max(0, Math.min(100, o.limit / o.max * 100)) : null;
    var col = o.color || (lim != null && o.value > o.limit ? "#FF9AA2" : "#5EE0B5");
    if (!h._g) {
      h._g = 1;
      h.innerHTML = '<div class="eco-viz-t"></div><div class="eco-gauge"><i></i><u></u></div><div class="eco-gauge-v"><span></span><span></span></div>';
    }
    h.querySelector(".eco-viz-t").textContent = o.title || "";
    var i = h.querySelector(".eco-gauge i"), u = h.querySelector(".eco-gauge u");
    i.style.width = pc + "%"; i.style.background = col;
    if (lim == null) u.style.display = "none"; else { u.style.display = ""; u.style.left = lim + "%"; u.setAttribute("data-l", o.limitLabel || ""); }
    var sp = h.querySelectorAll(".eco-gauge-v span");
    sp[0].textContent = o.left || ""; sp[1].textContent = o.right || "";
    h.setAttribute("role", "img");
    h.setAttribute("aria-label", (o.title || "") + " : " + (o.left || "") + " " + (o.right || ""));
  };


  /* Comparaison de barres horizontales. items = [{label, value, color?}] ; o.unit (par defaut " €"), o.dec (decimales) */
  E.compare = function (id, items, o) {
    o = o || {};
    var h = E.mount(id, o.after); if (!h) return;
    items = (items || []).filter(function (p) { return isFinite(p.value); });
    var max = 0; items.forEach(function (p) { max = Math.max(max, Math.abs(p.value)); });
    if (!items.length || max <= 0) { h.style.display = "none"; return; }
    h.style.display = "";
    var unit = o.unit === undefined ? " €" : o.unit, dec = o.dec || 0;
    var key = items.map(function (p) { return p.label; }).join("|");
    if (h._key !== key) {
      h._key = key;
      var rows = "";
      items.forEach(function (p, i) {
        rows += '<div class="eco-cmp-r"><span>' + esc(p.label) + '</span><div class="eco-cmp-b"><i style="background:' + (p.color || PAL[i % PAL.length]) + '"></i></div><b></b></div>';
      });
      h.innerHTML = (o.title ? '<div class="eco-viz-t">' + esc(o.title) + "</div>" : "") + '<div class="eco-cmp">' + rows + "</div>";
    }
    var rs = h.querySelectorAll(".eco-cmp-r"), txt = [];
    items.forEach(function (p, i) {
      var val = dec ? p.value.toFixed(dec).replace(".", ",") : fmtN(p.value);
      rs[i].querySelector("i").style.width = Math.max(2, Math.abs(p.value) / max * 100) + "%";
      rs[i].querySelector("b").textContent = val + unit;
      txt.push(p.label + " " + val + unit);
    });
    h.setAttribute("role", "img"); h.setAttribute("aria-label", (o.title ? o.title + " : " : "") + txt.join(", "));
  };

  /* Petite jauge a inserer dans une carte : renvoie du HTML */
  E.meter = function (pct) { return '<div class="eco-meter" aria-hidden="true"><i style="width:' + Math.max(0, Math.min(100, pct)).toFixed(1) + '%"></i></div>'; };

  /* Courbes. host = id d'un <canvas>/<div> (remplace par un SVG). series = [{name, color, data, dash, fill}] */
  function niceStep(raw) {
    var p = Math.pow(10, Math.floor(Math.log10(raw))), f = raw / p;
    return (f <= 1 ? 1 : f <= 2 ? 2 : f <= 2.5 ? 2.5 : f <= 5 ? 5 : 10) * p;
  }
  function kfmt(v) { return v >= 1000000 ? (v / 1000000).toFixed(v % 1000000 ? 1 : 0).replace(".", ",") + " M€" : v >= 1000 ? (v / 1000).toFixed(0) + " k€" : Math.round(v) + " €"; }

  E.line = function (id, labels, series, o) {
    o = o || {};
    var host = document.getElementById(id); if (!host) return;
    var box = host._eco;
    if (!box) {
      box = document.createElement("div"); box.className = "eco-line";
      host.style.display = "none"; host.parentNode.insertBefore(box, host.nextSibling); host._eco = box;
      window.addEventListener("resize", function () {
        clearTimeout(box._rz); box._rz = setTimeout(function () { if (box._last) E.line(id, box._last[0], box._last[1], box._last[2]); }, 150);
      });
    }
    box._last = [labels, series, o];
    var W = Math.max(260, box.clientWidth || host.parentNode.clientWidth || 320);
    var H = Math.round(Math.min(340, Math.max(210, W * 0.52)));
    var pl = W < 420 ? 44 : 54, pr = 12, pt = 12, pb = 30, n = labels.length, all = [];
    series.forEach(function (s) { s.data.forEach(function (v) { if (isFinite(v)) all.push(v); }); });
    var max = Math.max.apply(null, all.concat([1])), mn0 = Math.min.apply(null, all.concat([0])), step = niceStep((max - mn0) / 4), ymax = Math.ceil(max / step) * step, ymin = mn0 < 0 ? Math.floor(mn0 / step) * step : 0;
    function X(i) { return pl + (W - pl - pr) * (n > 1 ? i / (n - 1) : 0.5); }
    function Y(v) { return pt + (H - pt - pb) * (1 - (v - ymin) / (ymax - ymin)); }
    var svg = '<svg viewBox="0 0 ' + W + " " + H + '" width="' + W + '" height="' + H + '" role="img" aria-label="' + esc(o.label || "Graphique d'évolution") + '">';
    for (var v = ymin; v <= ymax + 1e-9; v += step) svg += '<line class="g" x1="' + pl + '" x2="' + (W - pr) + '" y1="' + Y(v) + '" y2="' + Y(v) + '"/><text x="' + (pl - 8) + '" y="' + (Y(v) + 4) + '" text-anchor="end">' + kfmt(v) + "</text>";
    var every = Math.max(1, Math.ceil(n / (W < 420 ? 5 : 8)));
    for (var i = 0; i < n; i += every) svg += '<text x="' + X(i) + '" y="' + (H - 8) + '" text-anchor="middle">' + esc(labels[i]) + "</text>";
    if (o.mark != null && o.mark >= 0 && o.mark < n) svg += '<line x1="' + X(o.mark) + '" x2="' + X(o.mark) + '" y1="' + pt + '" y2="' + (H - pb) + '" stroke="#EF9F27" stroke-width="1.5" stroke-dasharray="4 3"/><text x="' + X(o.mark) + '" y="' + (pt + 10) + '" text-anchor="middle" style="fill:#B8730A;font-weight:700">' + esc(o.markLabel || "") + "</text>";
    svg += '<g class="plot">';
    series.forEach(function (s) {
      var d = "";
      s.data.forEach(function (val, i) { d += (i ? "L" : "M") + X(i).toFixed(1) + " " + Y(val).toFixed(1); });
      if (s.fill) svg += '<path d="' + d + "L" + X(n - 1).toFixed(1) + " " + Y(Math.max(0, ymin)) + "L" + X(0).toFixed(1) + " " + Y(Math.max(0, ymin)) + 'Z" fill="' + s.color + '" fill-opacity=".13"/>';
      svg += '<path class="path" d="' + d + '" stroke="' + s.color + '" stroke-width="' + (s.width || 2.5) + '"' + (s.dash ? ' stroke-dasharray="' + s.dash + '"' : "") + "/>";
    });
    svg += "</g>";
    svg += '<line class="cur" y1="' + pt + '" y2="' + (H - pb) + '" x1="0" x2="0" style="display:none"/>';
    series.forEach(function (s, k) { svg += '<circle class="dot" r="4.5" fill="#fff" stroke="' + s.color + '" stroke-width="2.5" style="display:none" data-k="' + k + '"/>'; });
    svg += "</svg>";
    var leg = '<div class="eco-lline">' + series.map(function (s) { return '<span><i style="background:' + s.color + '"></i>' + esc(s.name) + "</span>"; }).join("") + "</div>";
    var first = !box._drawn;
    box.innerHTML = svg + '<div class="eco-tip" role="presentation"></div>' + leg;
    if (first) { box._drawn = 1; box.classList.add("draw"); } else box.classList.remove("draw");
    var sv = box.querySelector("svg"), tip = box.querySelector(".eco-tip"), cur = sv.querySelector(".cur"), dots = sv.querySelectorAll(".dot");
    function show(ev) {
      var r = sv.getBoundingClientRect(), x = (ev.clientX - r.left) * (W / r.width);
      var idx = Math.max(0, Math.min(n - 1, Math.round((x - pl) / ((W - pl - pr) / Math.max(1, n - 1)))));
      cur.setAttribute("x1", X(idx)); cur.setAttribute("x2", X(idx)); cur.style.display = "";
      var html = "<b>" + esc(labels[idx]) + "</b>";
      series.forEach(function (s, k) {
        dots[k].setAttribute("cx", X(idx)); dots[k].setAttribute("cy", Y(s.data[idx])); dots[k].style.display = "";
        html += '<div><i style="background:' + s.color + '"></i>' + esc(s.name) + " : " + fmtN(s.data[idx]) + " €</div>";
      });
      tip.innerHTML = html; tip.style.opacity = 1;
      var tw = tip.offsetWidth, left = X(idx) * (r.width / W) + 12;
      if (left + tw > r.width) left = X(idx) * (r.width / W) - tw - 12;
      tip.style.left = Math.max(0, left) + "px";
    }
    function hide() { cur.style.display = "none"; tip.style.opacity = 0; for (var k = 0; k < dots.length; k++) dots[k].style.display = "none"; }
    sv.addEventListener("pointermove", show); sv.addEventListener("pointerdown", show);
    sv.addEventListener("pointerleave", hide);
  };

  /* ---------- Accessibilite, saisies, confort ---------- */
  var uid = 0;
  function ensureId(el, p) { if (!el.id) el.id = p + (++uid); return el.id; }

  function labelise(el) {
    if (el.type === "hidden" || el.getAttribute("aria-label") || el.getAttribute("aria-labelledby")) return;
    if (el.id && document.querySelector('label[for="' + el.id.replace(/"/g, '\\"') + '"]')) return;
    if (el.closest("label")) return;
    var n = el;
    for (var d = 0; d < 4 && n; d++) {
      var p = n.previousElementSibling;
      while (p) {
        if (p.tagName === "LABEL") { el.setAttribute("aria-labelledby", ensureId(p, "eco-l")); return; }
        var inner = p.querySelector && p.querySelector("label");
        if (inner && !inner.querySelector("input,select")) { el.setAttribute("aria-labelledby", ensureId(inner, "eco-l")); return; }
        p = p.previousElementSibling;
      }
      n = n.parentElement;
    }
    var t = el.getAttribute("placeholder") || el.getAttribute("title") || el.getAttribute("name");
    if (t) el.setAttribute("aria-label", t);
  }

  function fillRange(r) {
    var mn = +r.min || 0, mx = r.max !== "" ? +r.max : 100, v = +r.value;
    r.style.setProperty("--p", (mx > mn ? (v - mn) / (mx - mn) * 100 : 0) + "%");
    var f = r.closest(".field, .slider-wrap, .opt-field"), val = f && f.querySelector(".val, .slider-val");
    if (val) r.setAttribute("aria-valuetext", val.textContent.replace(/\s+/g, " ").trim());
  }

  function enhance() {
    var main = document.querySelector("main");
    if (main && !document.querySelector(".eco-skip")) {
      main.id = main.id || "contenu";
      var a = document.createElement("a"); a.className = "eco-skip"; a.href = "#" + main.id; a.textContent = "Aller au contenu";
      document.body.insertBefore(a, document.body.firstChild);
      a.addEventListener("click", function () { main.setAttribute("tabindex", "-1"); main.focus({ preventScroll: false }); });
    }
    [].forEach.call(document.querySelectorAll("main input, main select, main textarea"), labelise);
    [].forEach.call(document.querySelectorAll('input[type="range"]'), function (r) {
      fillRange(r); r.addEventListener("input", function () { fillRange(r); }); r.addEventListener("change", function () { fillRange(r); });
    });
    [].forEach.call(document.querySelectorAll('input[type="number"]'), function (i) {
      if (!i.getAttribute("inputmode")) i.setAttribute("inputmode", /\./.test(i.getAttribute("step") || "") ? "decimal" : "numeric");
    });
    [].forEach.call(document.querySelectorAll("main table"), function (t) {
      if (t.parentNode.classList && t.parentNode.classList.contains("eco-scroll")) return;
      var w = document.createElement("div"); w.className = "eco-scroll"; w.tabIndex = 0; w.setAttribute("role", "region"); w.setAttribute("aria-label", "Tableau de données, défilable");
      t.parentNode.insertBefore(w, t); w.appendChild(t);
    });
    var res = document.querySelector(".results");
    if (res) {
      var hl = res.querySelector(".res-item.highlight") || res.querySelector(".res-item");
      if (hl) { hl.setAttribute("aria-live", "polite"); hl.setAttribute("aria-atomic", "true"); }
      if (window.MutationObserver) {
        new MutationObserver(function (ms) {
          ms.forEach(function (m) {
            var t = m.target.nodeType === 3 ? m.target.parentElement : m.target;
            if (!t || !t.closest || t.closest(".eco-viz")) return;
            var num = t.closest(".num");
            if (num && !num.classList.contains("eco-pop")) {
              num.classList.add("eco-pop");
              num.addEventListener("animationend", function f() { num.classList.remove("eco-pop"); num.removeEventListener("animationend", f); });
            }
          });
        }).observe(res, { subtree: true, childList: true, characterData: true });
      }
    }
  }

  /* Saisie : on borne les nombres aux min/max declares et on relance le calcul */
  document.addEventListener("change", function (e) {
    var t = e.target;
    if (!t || t.type !== "number") return;
    var mn = t.min !== "" ? +t.min : null, mx = t.max !== "" ? +t.max : null, v = +t.value;
    if (t.value === "" || isNaN(v)) { if (mn === null) return; t.value = mn; }
    else if (mn !== null && v < mn) t.value = mn;
    else if (mx !== null && v > mx) t.value = mx;
    else return;
    t.dispatchEvent(new Event("input", { bubbles: true }));
  }, true);

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", enhance); else enhance();
})();
