(function () {
  "use strict";
  var el = document.getElementById("fx-data");
  if (!el) return;
  var D = JSON.parse(el.textContent), rate = D.rate, last = "a";
  var loc = D.L === "en" ? "en-US" : "fr-FR";
  var f4 = new Intl.NumberFormat(loc, { minimumFractionDigits: 4, maximumFractionDigits: 4 });
  var $ = function (id) { return document.getElementById(id); };
  var a = $("fx-a"), b = $("fx-b");
  function sync() {
    if (last === "a") { var v = parseFloat(a.value); b.value = v >= 0 ? (v * rate).toFixed(2) : ""; }
    else { var w = parseFloat(b.value); a.value = w >= 0 ? (w / rate).toFixed(2) : ""; }
  }
  a.addEventListener("input", function () { last = "a"; sync(); });
  b.addEventListener("input", function () { last = "b"; sync(); });
  function setRate(v, date) {
    rate = v; $("fx-r").textContent = f4.format(v);
    var inv = $("fx-inv").querySelector("bdi"); if (inv) inv.textContent = "1 TND = " + f4.format(1 / v) + " " + D.cur.toUpperCase();
    try {
      var t = $("fx-d"); t.setAttribute("datetime", date);
      t.textContent = new Date(date + "T12:00:00").toLocaleDateString(D.L === "ar" ? "ar-TN-u-nu-latn" : loc, { day: "numeric", month: "long", year: "numeric" });
    } catch (e) {}
    sync();
  }
  // Newer daily release if one exists (dated releases first, then "latest" aliases).
  var base = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@", file = "/v1/currencies/" + D.cur + ".min.json", urls = [];
  for (var k = 0; k < 3; k++) { var d = new Date(Date.now() - k * 864e5); urls.push(base + d.getUTCFullYear() + "." + (d.getUTCMonth() + 1) + "." + d.getUTCDate() + file); }
  urls.push("https://latest.currency-api.pages.dev" + file, base + "latest" + file);
  (function tryNext(i) {
    if (i >= urls.length || !window.fetch) return;
    fetch(urls[i]).then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (j) {
      var v = j && j[D.cur] && j[D.cur].tnd;
      if (!(v > 0.5 && v < 20)) throw 0;
      if (j.date > D.date) setRate(v, j.date); else if (j.date < D.date) tryNext(i + 1);
    }).catch(function () { tryNext(i + 1); });
  })(0);
})();
