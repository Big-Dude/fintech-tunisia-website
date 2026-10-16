(function () {
  "use strict";
  var el = document.getElementById("remit-data");
  if (!el) return;
  var D = JSON.parse(el.textContent);
  var T = D.t, LB = D.lbl, AR = D.L === "ar";
  var nf = new Intl.NumberFormat(AR ? "fr-FR" : D.locale, { maximumFractionDigits: 2, minimumFractionDigits: 2 });
  var nf0 = new Intl.NumberFormat(AR ? "fr-FR" : D.locale, { maximumFractionDigits: 0 });
  var state = { cc: "FR", amt: 200, po: "", sort: "best", rate: D.rate };
  var SPEED = { "minutes": 0, "same-day": 1, "next-day": 2, "2-5-days": 3, "6-plus-days": 4 };
  var $ = function (id) { return document.getElementById(id); };
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  // In Arabic, keep each figure in left-to-right order so signs and % stay attached.
  var ltr = function (s) { return AR ? '<bdi dir="ltr">' + s + "</bdi>" : s; };
  var eur = function (v) { return ltr(D.L === "en" ? "€" + nf.format(v) : nf.format(v) + " €"); };
  var tnd = function (v) { return ltr(nf.format(v)) + (AR ? " د.ت" : " TND"); };
  var pct = function (v) { return ltr(D.L === "fr" ? nf.format(v) + " %" : nf.format(v) + "%"); };

  function quote(g, amt, rate) {
    var key = amt < 242.5 ? "200" : "500", alt = key === "200" ? "500" : "200";
    var b = g.b[key] && g.b[key].fee != null && g.b[key].fx != null ? g.b[key] : g.b[alt];
    if (!b || b.fee == null || b.fx == null) return { priced: false, fee: b ? b.fee : null };
    // You spend `amt` in total; the fee comes out of it and the rest is converted at the provider's rate.
    var recv = Math.max(0, (amt - b.fee) * rate * (1 - b.fx / 100));
    return { priced: true, fee: b.fee, fx: b.fx, recv: recv, pay: amt, cost: (1 - recv / (amt * rate)) * 100 };
  }

  function render() {
    var C = D.corridors[state.cc], amt = state.amt;
    var src = $("remit-src"); src.textContent = C.rpw ? src.getAttribute("data-rpw") : src.getAttribute("data-de");
    var rows = C.offers.filter(function (g) { return !state.po || g.payout.indexOf(state.po) !== -1; })
      .map(function (g) { return { g: g, q: quote(g, amt, state.rate) }; });
    rows.sort(function (a, b) {
      if (a.q.priced !== b.q.priced) return a.q.priced ? -1 : 1;
      if (!a.q.priced) return a.g.name.localeCompare(b.g.name);
      if (state.sort === "fee") return a.q.fee - b.q.fee || b.q.recv - a.q.recv;
      if (state.sort === "speed") return ((SPEED[a.g.speed] ?? 9) - (SPEED[b.g.speed] ?? 9)) || b.q.recv - a.q.recv;
      return b.q.recv - a.q.recv;
    });
    var priced = rows.filter(function (r) { return r.q.priced; });
    var best = priced.slice().sort(function (a, b) { return b.q.recv - a.q.recv; })[0];
    var fast = priced.filter(function (r) { return r.g.speed === "minutes"; }).sort(function (a, b) { return b.q.recv - a.q.recv; })[0];
    var html = rows.map(function (r) {
      var g = r.g, q = r.q, badges = "";
      if (best && r === best) badges += '<span class="rbadge rb-best">' + esc(T.best) + "</span>";
      if (fast && r === fast && r !== best) badges += '<span class="rbadge rb-fast">' + esc(T.fastest) + "</span>";
      var how = esc(LB.ch[g.ch] || g.ch) + ' <span aria-hidden="true">' + (AR ? "←" : "→") + "</span> " + (g.payout.length ? g.payout.map(function (p) { return esc(LB.po[p] || p); }).join(" / ") : esc(LB.po.unknown));
      var gets = q.priced ? '<b>' + tnd(q.recv) + '</b><span class="ro-pay">' + esc(T.pays) + " " + eur(q.pay) + " · " + esc(T.incl) + "</span>"
                          : '<b class="ro-np">—</b><span class="ro-pay">' + esc(T.noprice) + "</span>";
      var meta = '<div><dt>' + esc(T.fee) + '</dt><dd>' + (q.fee != null ? eur(q.fee) : "—") + "</dd></div>" +
        '<div><dt>' + esc(T.fx) + '</dt><dd>' + (q.priced ? pct(q.fx) : "—") + "</dd></div>" +
        '<div><dt>' + esc(T.tot) + '</dt><dd>' + (q.priced ? pct(q.cost) : "—") + "</dd></div>" +
        '<div><dt>' + esc(T.speed) + '</dt><dd>' + esc(LB.sp[g.speed || ""]) + "</dd></div>";
      var btn = g.url ? '<a class="btn btn-primary ro-go" href="' + esc(g.url) + '" target="_blank" rel="' + (g.ref ? "sponsored noopener" : "nofollow noopener") + '">' + esc(T.go) + " " + esc(g.name) + "</a>" : "";
      var reg = g.reg ? esc(T.safety) + ": " + esc(g.reg) : esc(T.notconf);
      var det = (g.ent ? "<p><b>" + esc(T.entity) + ":</b> " + esc(g.ent) + "</p>" : "") + (g.note ? "<p>" + esc(g.note) + "</p>" : "") +
        (g.paid ? "<p><b>" + esc(T.paidout) + ":</b> " + esc(g.paid) + "</p>" : "");
      return '<article class="ro' + (r === best ? " ro-top" : "") + '">' + (badges ? '<div class="ro-badges">' + badges + "</div>" : "") +
        '<div class="ro-main"><div class="ro-name"><strong>' + esc(g.name) + "</strong><span>" + how + "</span></div>" +
        '<div class="ro-gets"><span class="k">' + esc(T.gets) + "</span>" + gets + "</div>" +
        '<dl class="ro-meta">' + meta + "</dl>" + btn + "</div>" +
        '<details class="ro-det"><summary><span class="shield' + (g.reg ? "" : " shield-no") + '" aria-hidden="true"></span>' + reg + "</summary>" + det + "</details></article>";
    }).join("");
    $("remit-results").innerHTML = html;
    $("remit-empty").hidden = rows.length !== 0;
  }

  function setRate(rate, date) {
    state.rate = rate;
    $("rate-v").textContent = new Intl.NumberFormat(AR ? "fr-FR" : D.locale, { maximumFractionDigits: 4, minimumFractionDigits: 4 }).format(rate);
    if (date) {
      try { $("rate-d").textContent = new Date(date + "T12:00:00").toLocaleDateString(AR ? "ar-TN-u-nu-latn" : D.locale, { day: "numeric", month: "long", year: "numeric" }); } catch (e) {}
    }
    render();
  }

  document.querySelectorAll(".segs .seg").forEach(function (b) {
    b.addEventListener("click", function () {
      document.querySelectorAll(".segs .seg").forEach(function (o) { o.classList.remove("on"); o.setAttribute("aria-pressed", "false"); });
      b.classList.add("on"); b.setAttribute("aria-pressed", "true"); state.cc = b.getAttribute("data-cc"); render();
    });
  });
  document.querySelectorAll("#remit-po .chip").forEach(function (b) {
    b.addEventListener("click", function () {
      document.querySelectorAll("#remit-po .chip").forEach(function (o) { o.classList.remove("active"); o.setAttribute("aria-pressed", "false"); });
      b.classList.add("active"); b.setAttribute("aria-pressed", "true"); state.po = b.getAttribute("data-po"); render();
    });
  });
  $("remit-amt").addEventListener("input", function () {
    var v = parseFloat(this.value); if (v >= 10 && v <= 10000) { state.amt = v; render(); }
  });
  $("remit-sort").addEventListener("change", function () { state.sort = this.value; render(); });
  render();

  // Daily mid-market EUR→TND rate (open data, refreshed every day); keeps the built-in rate if unavailable.
  var urls = ["https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/eur.min.json",
              "https://latest.currency-api.pages.dev/v1/currencies/eur.min.json"];
  (function tryNext(i) {
    if (i >= urls.length || !window.fetch) return;
    fetch(urls[i]).then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (j) {
      var v = j && j.eur && j.eur.tnd;
      if (v > 1 && v < 10 && (!D.date || j.date >= D.date)) setRate(v, j.date);
    }).catch(function () { tryNext(i + 1); });
  })(0);
})();
