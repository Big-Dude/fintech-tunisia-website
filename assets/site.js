(function () {
  "use strict";
  var body = document.body;

  // Mobile menu
  var toggle = document.querySelector(".menu-toggle");
  if (toggle) toggle.addEventListener("click", function () {
    var open = body.classList.toggle("nav-open");
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  });

  // Article search on the index page
  var search = document.getElementById("post-search");
  if (search) {
    var cards = Array.prototype.slice.call(document.querySelectorAll("#post-grid .card, .featured .card"));
    var empty = document.querySelector(".no-results");
    var norm = function (s) { return s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); };
    search.addEventListener("input", function () {
      var terms = norm(search.value).split(/\s+/).filter(Boolean), shown = 0;
      cards.forEach(function (c) {
        var hay = norm(c.getAttribute("data-search") || "");
        var ok = terms.every(function (t) { return hay.indexOf(t) !== -1; });
        c.style.display = ok ? "" : "none"; if (ok) shown++;
      });
      if (empty) empty.hidden = shown !== 0;
    });
  }

  // Directory: search + category filter
  function setupFilter(gridSel, itemSel, searchId, chipsId, attr, extraSel) {
    var grid = document.querySelector(gridSel); if (!grid) return;
    var items = Array.prototype.slice.call(grid.querySelectorAll(itemSel));
    var input = searchId && document.getElementById(searchId);
    var chips = chipsId ? Array.prototype.slice.call(document.querySelectorAll("#" + chipsId + " .chip")) : [];
    var extra = extraSel && document.querySelector(extraSel);
    var empty = grid.parentNode.querySelector(".no-results");
    var cur = "all";
    var norm = function (s) { return (s || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, ""); };
    function apply() {
      var terms = input ? norm(input.value).split(/\s+/).filter(Boolean) : [], shown = 0, topic = extra ? extra.value : "";
      items.forEach(function (it) {
        var ok = (cur === "all" || it.getAttribute(attr) === cur);
        if (ok && terms.length) { var hay = norm(it.getAttribute("data-search")); ok = terms.every(function (t) { return hay.indexOf(t) !== -1; }); }
        if (ok && topic) ok = (" " + it.getAttribute("data-topics") + " ").indexOf(" " + topic + " ") !== -1;
        it.hidden = !ok; if (ok) shown++;
      });
      grid.querySelectorAll(".yr").forEach(function (y) {
        var n = y.nextElementSibling, any = false;
        while (n && !n.classList.contains("yr")) { if (!n.hidden) any = true; n = n.nextElementSibling; }
        y.hidden = !any;
      });
      if (empty) empty.hidden = shown !== 0;
    }
    chips.forEach(function (c) { c.addEventListener("click", function () {
      chips.forEach(function (o) { o.classList.remove("active"); o.setAttribute("aria-pressed", "false"); });
      c.classList.add("active"); c.setAttribute("aria-pressed", "true"); cur = c.getAttribute("data-filter"); apply();
    }); });
    if (input) input.addEventListener("input", apply);
    if (extra) extra.addEventListener("change", apply);
  }
  setupFilter("#co-grid", ".co-card", "co-search", "co-filters", "data-cat");
  setupFilter("#reg-list", ".reg", null, "reg-filters", "data-group", "#reg-topic");

  // Table of contents: highlight the current section
  var tocLinks = document.querySelectorAll(".toc a[href^='#']");
  if (tocLinks.length && "IntersectionObserver" in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          tocLinks.forEach(function (a) { a.classList.remove("on"); });
          var a = map[e.target.id]; if (a) a.classList.add("on");
        }
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    Object.keys(map).forEach(function (id) { var el = document.getElementById(id); if (el) io.observe(el); });
  }

  function send(form) {
    return fetch(form.action, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } })
      .then(function (r) { if (r.ok) form.classList.add("submitted"); else throw new Error(); })
      .catch(function () { alert(form.getAttribute("data-err") || "Something went wrong — please try again."); });
  }

  // Newsletter forms
  document.querySelectorAll(".js-ajax-form").forEach(function (f) {
    f.addEventListener("submit", function (e) { e.preventDefault(); send(f); });
  });

  // Contact form with a simple human check (plus Formspree honeypot)
  var cf = document.getElementById("contact-form");
  if (cf) {
    var a, b, q = document.getElementById("captcha-q"), cap = document.getElementById("cf-captcha"), err = document.getElementById("captcha-error");
    var fresh = function () { a = 1 + Math.floor(Math.random() * 8); b = 1 + Math.floor(Math.random() * 8); if (q) q.textContent = a + " + " + b; };
    fresh();
    cf.addEventListener("submit", function (e) {
      e.preventDefault();
      if (parseInt(cap.value, 10) !== a + b) { err.hidden = false; cap.value = ""; cap.focus(); fresh(); return; }
      err.hidden = true; send(cf);
    });
  }
})();
