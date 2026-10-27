/* CLBI v1.1 site script: search, tables and charts. No build step. */
(function () {
  "use strict";
  var CLBI = (window.CLBI = {});
  var root = (document.body && document.body.getAttribute("data-root")) || "";

  CLBI.ready = function (fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  };
  function data() {
    var el = document.getElementById("page-data");
    return el ? JSON.parse(el.textContent) : {};
  }
  function css(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }
  function alpha(hex, a) {
    hex = hex.replace("#", "");
    if (hex.length === 3) hex = hex.split("").map(function (c) { return c + c; }).join("");
    var n = parseInt(hex, 16);
    return "rgba(" + ((n >> 16) & 255) + "," + ((n >> 8) & 255) + "," + (n & 255) + "," + a + ")";
  }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  var nfIN = {};
  function fmt(x, dp) {
    if (x == null || !isFinite(x)) return "–";
    dp = dp == null ? 1 : dp;
    var k = dp;
    if (!nfIN[k]) nfIN[k] = new Intl.NumberFormat("en-IN", { minimumFractionDigits: dp, maximumFractionDigits: dp });
    return nfIN[k].format(x);
  }
  function sig(x, s) {
    if (x == null || !isFinite(x)) return "–";
    if (x === 0) return "0";
    s = s || 3;
    var mag = Math.floor(Math.log10(Math.abs(x)));
    if (mag >= s - 1) return fmt(Math.round(x), 0);
    var dp = Math.min(8, s - 1 - mag);
    return new Intl.NumberFormat("en-IN", { maximumFractionDigits: dp, minimumFractionDigits: 0 }).format(Number(x.toPrecision(s)));
  }
  CLBI.fmt = fmt; CLBI.sig = sig;

  /* ------------------------------------------------------------------ search */
  var COMPANIES = (window.CLBI_COMPANIES || []).map(function (c) {
    return { sym: c[0], name: c[1], slug: c[2], group: c[3], key: (c[1] + " " + c[0]).toLowerCase() };
  });
  var ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>';
  var searchCount = 0;
  function hl(text, q) {
    var i = text.toLowerCase().indexOf(q);
    if (!q || i < 0) return esc(text);
    return esc(text.slice(0, i)) + "<mark>" + esc(text.slice(i, i + q.length)) + "</mark>" + esc(text.slice(i + q.length));
  }
  function match(q) {
    q = q.trim().toLowerCase();
    if (!q) return [];
    var out = [];
    COMPANIES.forEach(function (c, idx) {
      var s = c.sym.toLowerCase(), n = c.name.toLowerCase(), score = -1;
      if (s === q) score = 0;
      else if (s.indexOf(q) === 0) score = 1;
      else if (n.indexOf(q) === 0) score = 2;
      else if (new RegExp("\\b" + q.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).test(n)) score = 3;
      else if (c.key.indexOf(q) >= 0) score = 4;
      if (score >= 0) out.push({ c: c, s: score, i: idx });
    });
    out.sort(function (a, b) { return a.s - b.s || a.i - b.i; });
    return out.slice(0, 8).map(function (o) { return o.c; });
  }
  function initSearch(host) {
    var id = "s" + (++searchCount);
    var lg = host.getAttribute("data-size") === "lg";
    host.classList.add("search");
    if (lg) host.classList.add("lg");
    host.innerHTML =
      '<div class="search-box" role="combobox" aria-haspopup="listbox" aria-owns="' + id + '-list" aria-expanded="false">' + ICON +
      '<label class="sr" for="' + id + '-in">Find a company</label>' +
      '<input id="' + id + '-in" type="search" autocomplete="off" spellcheck="false" aria-autocomplete="list" aria-controls="' + id + '-list" placeholder="' +
      (lg ? (window.innerWidth < 520 ? "Company name or NSE symbol" : "Search " + COMPANIES.length + " companies by name or NSE symbol") : "Find a company") + '">' +
      (lg ? "<kbd>/</kbd>" : "") + "</div>" +
      '<ul class="results" id="' + id + '-list" role="listbox" hidden></ul>';
    var input = host.querySelector("input"), list = host.querySelector(".results"), box = host.querySelector(".search-box");
    var items = [], sel = -1;
    function render() {
      var q = input.value;
      items = match(q);
      sel = items.length ? 0 : -1;
      if (!q.trim()) { list.hidden = true; box.setAttribute("aria-expanded", "false"); return; }
      if (!items.length) {
        list.innerHTML = '<li class="empty">No company matches “' + esc(q) + '”. Try a shorter name or the NSE symbol.</li>';
      } else {
        var ql = q.trim().toLowerCase();
        list.innerHTML = items.map(function (c, i) {
          return '<li role="option" id="' + id + "-o" + i + '" aria-selected="' + (i === sel) + '"><a href="' + root + "company/" + c.slug + '.html"><span class="rn">' +
            hl(c.name, ql) + '</span><span class="rs">' + hl(c.sym, ql) + '</span><span class="rg">' + esc(c.group) + "</span></a></li>";
        }).join("");
      }
      list.hidden = false;
      box.setAttribute("aria-expanded", "true");
    }
    function move(d) {
      if (!items.length) return;
      sel = (sel + d + items.length) % items.length;
      Array.prototype.forEach.call(list.children, function (li, i) { li.setAttribute("aria-selected", i === sel); });
      var cur = list.children[sel];
      if (cur && cur.scrollIntoView) cur.scrollIntoView({ block: "nearest" });
      input.setAttribute("aria-activedescendant", id + "-o" + sel);
    }
    input.addEventListener("input", render);
    input.addEventListener("focus", function () { if (input.value) render(); });
    input.addEventListener("keydown", function (ev) {
      if (ev.key === "ArrowDown") { ev.preventDefault(); move(1); }
      else if (ev.key === "ArrowUp") { ev.preventDefault(); move(-1); }
      else if (ev.key === "Enter") {
        if (sel >= 0 && items[sel]) { ev.preventDefault(); window.location.href = root + "company/" + items[sel].slug + ".html"; }
      } else if (ev.key === "Escape") { list.hidden = true; input.blur(); }
    });
    document.addEventListener("click", function (ev) { if (!host.contains(ev.target)) list.hidden = true; });
    return input;
  }
  CLBI.ready(function () {
    var inputs = [];
    document.querySelectorAll("[data-search]").forEach(function (h) { inputs.push(initSearch(h)); });
    document.addEventListener("keydown", function (ev) {
      if (ev.key === "/" && !/input|textarea|select/i.test(document.activeElement.tagName)) {
        ev.preventDefault();
        var hero = document.querySelector(".hero-search input") || inputs[0];
        if (hero) hero.focus();
      }
    });
    initSortable();
  });

  /* ------------------------------------------------------------------ tooltip for HTML elements */
  var tipEl;
  function tip(container) {
    if (!tipEl) { tipEl = document.createElement("div"); tipEl.className = "tip"; tipEl.hidden = true; document.body.appendChild(tipEl); }
    container.addEventListener("mouseover", function (ev) {
      var t = ev.target.closest("[data-tip]");
      if (!t) return;
      tipEl.textContent = t.getAttribute("data-tip"); tipEl.hidden = false;
    });
    container.addEventListener("mousemove", function (ev) {
      if (tipEl.hidden) return;
      var x = ev.clientX + 14, y = ev.clientY + 16, w = tipEl.offsetWidth;
      if (x + w > window.innerWidth - 8) x = ev.clientX - w - 14;
      tipEl.style.left = x + "px"; tipEl.style.top = y + "px";
    });
    container.addEventListener("mouseout", function (ev) { if (ev.target.closest("[data-tip]")) tipEl.hidden = true; });
  }
  CLBI.universe = function () { var u = document.getElementById("universe"); if (u) tip(u); };

  /* ------------------------------------------------------------------ sortable tables */
  function cellVal(td) {
    if (!td) return "";
    var v = td.getAttribute("data-v");
    if (v != null && v !== "") return parseFloat(v);
    var t = td.textContent.trim();
    var n = parseFloat(t.replace(/[₹,%+×\s]|cr/g, ""));
    return isNaN(n) || /[a-z]{3,}/i.test(t.replace(/cr\b/, "")) && !/^[−\-\d.,\s₹]+/.test(t) ? t.toLowerCase() : n;
  }
  function initSortable() {
    document.querySelectorAll("table.sortable").forEach(function (table) {
      var ths = table.querySelectorAll("thead th");
      ths.forEach(function (th, idx) {
        if (!th.hasAttribute("data-sort")) return;
        th.setAttribute("tabindex", "0");
        function go() {
          var asc = th.getAttribute("aria-sort") !== "ascending";
          ths.forEach(function (t) { t.removeAttribute("aria-sort"); });
          th.setAttribute("aria-sort", asc ? "ascending" : "descending");
          var tb = table.tBodies[0];
          var rows = Array.prototype.slice.call(tb.rows);
          rows.sort(function (a, b) {
            var x = cellVal(a.cells[idx]), y = cellVal(b.cells[idx]);
            if (typeof x === "number" && typeof y === "number") return asc ? x - y : y - x;
            return asc ? String(x).localeCompare(String(y)) : String(y).localeCompare(String(x));
          });
          rows.forEach(function (r) { tb.appendChild(r); });
        }
        th.addEventListener("click", go);
        th.addEventListener("keydown", function (ev) { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); go(); } });
      });
    });
  }

  /* ------------------------------------------------------------------ chart defaults */
  var EL = {
    climate: { label: "Climate", unit: "tCO₂e per ₹ crore", v: "--climate" },
    water: { label: "Water", unit: "m³ per ₹ crore", v: "--water" },
    waste: { label: "Waste", unit: "tonnes per ₹ crore", v: "--waste" },
    air: { label: "Air", unit: "tonnes per ₹ crore", v: "--air" }
  };
  function setupCharts() {
    if (!window.Chart) return false;
    var C = window.Chart;
    C.defaults.font.family = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif";
    C.defaults.font.size = 12;
    C.defaults.color = css("--muted");
    C.defaults.borderColor = css("--rule");
    C.defaults.animation = window.matchMedia("(prefers-reduced-motion: reduce)").matches ? false : { duration: 500 };
    C.defaults.maintainAspectRatio = false;
    C.defaults.plugins.legend.display = false;
    var tt = C.defaults.plugins.tooltip;
    tt.backgroundColor = css("--ink");
    tt.titleColor = css("--paper");
    tt.bodyColor = css("--paper");
    tt.titleFont = { weight: "600", size: 13 };
    tt.bodyFont = { size: 12.5 };
    tt.padding = 10;
    tt.cornerRadius = 6;
    tt.displayColors = false;
    tt.caretSize = 5;
    return true;
  }
  function logTicks(scale) {
    return {
      callback: function (v) {
        var l = Math.log10(v);
        if (Math.abs(l - Math.round(l)) > 1e-9) return "";
        return v >= 1 ? fmt(v, 0) : String(Number(v.toPrecision(1)));
      },
      autoSkip: false, maxRotation: 0
    };
  }
  function isPow10(v) { var l = Math.log10(v); return Math.abs(l - Math.round(l)) < 1e-9; }
  function logGrid() { var rule = css("--rule"); return { drawTicks: false, color: function (c) { return c.tick && isPow10(c.tick.value) ? rule : "transparent"; } }; }
  function spread(vals) {
    var p = vals.filter(function (v) { return v > 0; });
    if (!p.length) return 1;
    return Math.max.apply(null, p) / Math.min.apply(null, p);
  }
  function goTo(slug) { window.location.href = root + "company/" + slug + ".html"; }
  function hoverCursor(ev, els) { ev.native.target.style.cursor = els.length ? "pointer" : "default"; }

  var valueLabels = {
    id: "valueLabels",
    afterDatasetsDraw: function (chart, args, opts) {
      if (!opts || !opts.fmt) return;
      var ctx = chart.ctx;
      ctx.save();
      ctx.font = "600 12.5px Inter, sans-serif";
      ctx.fillStyle = css("--ink");
      ctx.textAlign = "center";
      chart.data.datasets.forEach(function (ds, di) {
        var meta = chart.getDatasetMeta(di);
        meta.data.forEach(function (bar, i) {
          var txt = opts.fmt(ds.data[i], i);
          if (!txt) return;
          if (chart.options.indexAxis === "y") {
            ctx.textAlign = "left"; ctx.textBaseline = "middle";
            ctx.fillText(txt, Math.max(bar.x, bar.base) + 6, bar.y);
          } else {
            ctx.fillText(txt, bar.x, Math.min(bar.y, bar.base) - 7);
          }
        });
      });
      ctx.restore();
    }
  };

  /* ------------------------------------------------------------------ rankings */
  CLBI.rankings = function () {
    var D = data(), rows = D.rows || [], nair = D.nair || {};
    var tb = document.querySelector("#rank-table tbody");
    var q = document.getElementById("f-q"), g = document.getElementById("f-g"), s = document.getElementById("f-s");
    var cnt = document.getElementById("f-count");
    var sortK = "g", asc = true, PAGE = 75, shown = PAGE;
    var more = document.getElementById("f-more");
    var TN = ["Scope 1", "Scope 2", "Water withdrawal", "Waste generated"];
    function tiers(t) {
      return '<span class="tiers">' + t.map(function (x, i) {
        return '<i class="tq t' + (x || 0) + '" title="' + TN[i] + ": " + (x ? "tier " + x : "not reported") + '"></i>';
      }).join("") + "</span>";
    }
    function maxTier(t) { var m = 0, miss = 0; t.forEach(function (x) { if (x) m = Math.max(m, x); else miss++; }); return miss * 10 + m; }
    function key(r) {
      switch (sortK) {
        case "c": return r.c.toLowerCase();
        case "g": return r.g.toLowerCase() + "|" + (r.r == null ? 9999 : r.r).toString().padStart(5, "0") + "|" + r.c.toLowerCase();
        case "t": return maxTier(r.t);
        case "k": return r.kl;
        default: return r[sortK];
      }
    }
    function render() {
      var qq = q.value.trim().toLowerCase(), gg = g.value, ss = s.value;
      var list = rows.filter(function (r) {
        if (gg && r.g !== gg) return false;
        if (ss === "unranked") { if (r.k === "ranked") return false; }
        else if (ss && r.k !== ss) return false;
        if (qq && (r.c + " " + r.s).toLowerCase().indexOf(qq) < 0) return false;
        return true;
      });
      list.sort(function (a, b) {
        var x = key(a), y = key(b);
        var nx = x == null, ny = y == null;
        if (nx && ny) return 0; if (nx) return 1; if (ny) return -1;
        var c = typeof x === "number" ? x - y : String(x).localeCompare(String(y));
        return asc ? c : -c;
      });
      var total = list.length;
      list = list.slice(0, shown);
      tb.innerHTML = list.map(function (r) {
        var rank = r.r != null ? fmt(r.r, 0) + "<small>/" + fmt(r.n, 0) + "</small>" : '<span class="missing">–</span>';
        var air = r.a != null ? fmt(r.a, 0) + "<small>/" + (nair[r.g] || "") + "</small>" : '<span class="missing">–</span>';
        var status = '<span class="pill pill-' + r.k + '">' + esc(r.kl) + "</span>" +
          (r.k !== "ranked" && r.why ? '<span class="why">' + esc(r.why.charAt(0).toUpperCase() + r.why.slice(1)) + "</span>" : "");
        return '<tr class="' + (r.k === "ranked" ? "" : "unranked") + '"><td class="l"><a href="company/' + r.u + '.html">' + esc(r.c) + '</a>' + (r.nc ? '<span class="dagger" title="Check before naming: ' + esc(r.nc) + '" aria-label="Check before naming: ' + esc(r.nc) + '">†</span>' : "") + '<span class="sym">' + esc(r.s) + "</span></td>" +
          '<td class="l"><a class="grp" href="sector/' + r.gu + '.html">' + esc(r.g) + "</a></td>" +
          '<td class="r num">' + rank + '</td><td class="r num strong">' + (r.f != null ? fmt(r.f, 1) : "–") + "</td>" +
          '<td class="r num">' + (r.p != null ? fmt(r.p, 1) : "–") + '</td><td class="r num">' + (r.cr != null ? "+" + fmt(r.cr, 1) : "–") + "</td>" +
          '<td class="r num">' + air + '</td><td class="c">' + tiers(r.t) + '</td><td class="l">' + status + "</td></tr>";
      }).join("") || '<tr><td colspan="9" class="l muted">No company matches these filters. Clear the search or choose another peer group.</td></tr>';
      cnt.textContent = (total > list.length ? "Showing " + list.length + " of " + total : total) + (total === rows.length ? " companies" : " matching, of " + rows.length);
      if (more) { more.hidden = total <= list.length; more.textContent = "Show all " + total; }
    }
    document.querySelectorAll("#rank-table th[data-k]").forEach(function (th) {
      th.setAttribute("tabindex", "0");
      function go() {
        var k = th.getAttribute("data-k");
        if (sortK === k) asc = !asc; else { sortK = k; asc = !(k === "f" || k === "p" || k === "cr"); }
        document.querySelectorAll("#rank-table th").forEach(function (t) { t.removeAttribute("aria-sort"); });
        th.setAttribute("aria-sort", asc ? "ascending" : "descending");
        render();
      }
      th.addEventListener("click", go);
      th.addEventListener("keydown", function (ev) { if (ev.key === "Enter") go(); });
    });
    var params = new URLSearchParams(window.location.search);
    if (params.get("group")) g.value = params.get("group");
    function reset() { shown = PAGE; render(); }
    [q, g, s].forEach(function (el) { el.addEventListener("input", reset); el.addEventListener("change", reset); });
    if (more) more.addEventListener("click", function () { shown = 1e6; render(); });
    render();
  };

  /* ------------------------------------------------------------------ sector page */
  CLBI.sector = function () {
    var D = data(), comps = D.comps || [];
    if (!setupCharts()) return;
    var C = window.Chart;
    var peer = css("--peer"), ink = css("--ink"), muted = css("--muted"), rule = css("--rule");

    // stacked composition
    var st = document.getElementById("stack");
    if (st) {
      var sc = comps.filter(function (c) { return c.p != null; }).sort(function (a, b) {
        return (b.f || 0) - (a.f || 0);
      });
      new C(st, {
        type: "bar",
        data: {
          labels: sc.map(function (c) { return c.s; }),
          datasets: [
            { label: "Pressure score", data: sc.map(function (c) { return c.p; }), backgroundColor: sc.map(function (c) { return c.rk != null ? css("--pressure") : alpha(css("--pressure"), 0.35); }) },
            { label: "Restoration credit", data: sc.map(function (c) { return c.rp || 0; }), backgroundColor: css("--c-rest") },
            { label: "Recycling credit", data: sc.map(function (c) { return c.yp || 0; }), backgroundColor: css("--c-recy") },
            { label: "Renewable electricity credit", data: sc.map(function (c) { return c.ep || 0; }), backgroundColor: css("--c-re") }
          ]
        },
        options: {
          indexAxis: "y", responsive: true,
          datasets: { bar: { barPercentage: 0.78, categoryPercentage: 0.9 } },
          scales: {
            x: { stacked: true, min: 0, suggestedMax: 100, grid: { color: rule, drawTicks: false }, border: { display: false }, ticks: { stepSize: 25, padding: 6 } },
            y: { stacked: true, grid: { display: false }, border: { display: false }, ticks: { color: ink, font: { size: 11.5 }, autoSkip: false } }
          },
          plugins: {
            tooltip: {
              callbacks: {
                title: function (it) { var c = sc[it[0].dataIndex]; return c.c + (c.rk != null ? "  ·  rank " + c.rk : "  ·  not ranked"); },
                label: function (it) { return it.dataset.label + ": " + fmt(it.raw, it.datasetIndex ? 2 : 1); },
                footer: function (it) { var c = sc[it[0].dataIndex]; return c.f != null ? "Final score " + fmt(c.f, 1) : ""; }
              }
            }
          },
          onClick: function (ev, els) { if (els.length) goTo(sc[els[0].index].u); },
          onHover: hoverCursor
        }
      });
    }

    // intensity bars
    document.querySelectorAll("canvas[data-intensity]").forEach(function (cv) {
      var el = cv.getAttribute("data-intensity");
      var col = css(EL[el].v);
      var rows = comps.filter(function (c) { return c[el] != null && c[el] > 0; }).sort(function (a, b) { return a[el] - b[el]; });
      var vals = rows.map(function (c) { return c[el]; });
      var useLog = spread(vals) > 100;
      var colors = rows.map(function (c) {
        var scored = c[el + "_s"] != null;
        if (!scored) return peer;
        return c.rk != null ? col : alpha(col, 0.38);
      });
      new C(cv, {
        type: "bar",
        data: { labels: rows.map(function (c) { return c.s; }), datasets: [{ data: vals, backgroundColor: colors, borderRadius: 2, barPercentage: 0.82, categoryPercentage: 0.92 }] },
        options: {
          indexAxis: "y", responsive: true,
          scales: {
            x: useLog ? { type: "logarithmic", grid: logGrid(), border: { display: false }, ticks: logTicks() }
              : { beginAtZero: true, grid: { color: rule, drawTicks: false }, border: { display: false }, ticks: { maxTicksLimit: 6, callback: function (v) { return sig(v, 3); } } },
            y: { grid: { display: false }, border: { display: false }, ticks: { color: ink, font: { size: 11.5 }, autoSkip: false } }
          },
          plugins: {
            tooltip: {
              callbacks: {
                title: function (it) { return rows[it[0].dataIndex].c; },
                label: function (it) {
                  var c = rows[it.dataIndex];
                  return [sig(it.raw, 4) + " " + EL[el].unit,
                    c[el + "_s"] != null ? "Element score " + fmt(c[el + "_s"], 1) + (c.rk != null ? ", ranked " + c.rk : ", not ranked") : "Not scored"];
                }
              }
            }
          },
          onClick: function (ev, els) { if (els.length) goTo(rows[els[0].index].u); },
          onHover: hoverCursor
        }
      });
      var note = document.querySelector('[data-note="' + el + '"]');
      if (note) {
        var zero = comps.filter(function (c) { return c[el] === 0; }).length;
        note.textContent = (useLog ? "Logarithmic axis. " : "") + (zero ? zero + " reported zero value" + (zero > 1 ? "s are" : " is") + " not plotted." : "");
      }
    });

    // slope chart for comparator
    var sl = document.getElementById("slope");
    if (sl) {
      var cs = comps.filter(function (c) { return c.rk != null && c.rc != null; });
      var maxR = Math.max.apply(null, cs.map(function (c) { return Math.max(c.rk, c.rc); }).concat([2]));
      var accent = css("--forest"), warm = css("--climate");
      var endLabels = {
        id: "endLabels",
        afterDatasetsDraw: function (chart) {
          var ctx = chart.ctx; ctx.save(); ctx.font = "500 11.5px Inter, sans-serif"; ctx.textBaseline = "middle";
          chart.data.datasets.forEach(function (ds, i) {
            var m = chart.getDatasetMeta(i), a = m.data[0], b = m.data[1];
            ctx.fillStyle = ds.borderColor;
            ctx.textAlign = "right"; ctx.fillText(ds.label, a.x - 10, a.y);
            ctx.textAlign = "left"; ctx.fillText(ds.label, b.x + 10, b.y);
          });
          ctx.restore();
        }
      };
      new C(sl, {
        type: "line",
        data: {
          labels: ["Per ₹ crore revenue", "Per unit of output"],
          datasets: cs.map(function (c) {
            var moved = Math.abs(c.rk - c.rc) >= 3;
            var color = moved ? warm : accent;
            return { label: c.s, data: [c.rk, c.rc], borderColor: color, backgroundColor: color, borderWidth: moved ? 2 : 1.5, pointRadius: 4, pointHoverRadius: 6, tension: 0 };
          })
        },
        options: {
          responsive: true, layout: { padding: { left: 96, right: 96, top: 8, bottom: 4 } },
          scales: {
            x: { grid: { display: false }, border: { display: false }, ticks: { color: ink, font: { weight: "600" } }, offset: false },
            y: { reverse: true, min: 0.5, max: maxR + 0.5, display: false }
          },
          plugins: { tooltip: { callbacks: { title: function (it) { return cs[it[0].datasetIndex].c; }, label: function (it) { return it.label + ": rank " + it.raw; } } } },
          onClick: function (ev, els) { if (els.length) goTo(cs[els[0].datasetIndex].u); },
          onHover: hoverCursor
        },
        plugins: [endLabels]
      });
    }

    // nature cost strip
    var sp = document.getElementById("strip");
    if (sp) {
      var rowsR = comps.filter(function (c) { return c.nr != null && c.nr > 0; });
      var rowsE = comps.filter(function (c) { return c.ne != null && c.ne > 0; });
      function jit(i) { var x = Math.sin((i + 1) * 12.9898) * 43758.5453; return ((x - Math.floor(x)) - 0.5) * 0.5; }
      function median(a) { a = a.slice().sort(function (x, y) { return x - y; }); var m = a.length >> 1; return a.length % 2 ? a[m] : (a[m - 1] + a[m]) / 2; }
      var forest = css("--forest");
      var ds = [
        { label: "% of revenue", data: rowsR.map(function (c, i) { return { x: c.nr, y: 1 + jit(i), c: c }; }), backgroundColor: alpha(forest, 0.55), borderColor: forest, borderWidth: 0.5, pointRadius: 4.5, pointHoverRadius: 7 },
        { label: "% of EBITDA", data: rowsE.map(function (c, i) { return { x: c.ne, y: 0 + jit(i + 7), c: c }; }), backgroundColor: alpha(css("--waste"), 0.6), borderColor: css("--waste"), borderWidth: 0.5, pointRadius: 4.5, pointHoverRadius: 7 }
      ];
      var notes = [];
      [[rowsR, "nr", 1, "revenue"], [rowsE, "ne", 0, "EBITDA"]].forEach(function (t) {
        if (t[0].length >= 5) {
          var m = median(t[0].map(function (c) { return c[t[1]]; }));
          ds.push({ type: "line", label: "Median", data: [{ x: m, y: t[2] - 0.38 }, { x: m, y: t[2] + 0.38 }], borderColor: ink, borderWidth: 2, pointRadius: 0, showLine: true, _median: m });
          notes.push("Median " + sig(m, 3) + "% of " + t[3] + " (" + t[0].length + " companies)");
        } else if (t[0].length) notes.push("Median not shown for " + t[3] + ": fewer than 5 companies");
      });
      if (!rowsE.length) { sp.parentNode.style.height = "160px"; notes.push("No EBITDA basis for this group (financial companies, or EBITDA not available)"); }
      var allv = rowsR.map(function (c) { return c.nr; }).concat(rowsE.map(function (c) { return c.ne; }));
      new C(sp, {
        type: "scatter",
        data: { datasets: ds },
        options: {
          responsive: true,
          scales: {
            x: spread(allv) > 50 ? { type: "logarithmic", grid: logGrid(), border: { display: false }, ticks: { maxRotation: 0, callback: function (v) { return isPow10(v) ? sig(v, 2) + "%" : ""; }, autoSkip: false } }
              : { grid: { color: rule, drawTicks: false }, border: { display: false }, ticks: { maxRotation: 0, callback: function (v) { return sig(v, 3) + "%"; } } },
            y: { min: rowsE.length ? -0.6 : 0.4, max: 1.6, grid: { display: false }, border: { display: false }, afterBuildTicks: function (ax) { ax.ticks = rowsE.length ? [{ value: 0 }, { value: 1 }] : [{ value: 1 }]; }, ticks: { color: ink, font: { size: 12.5, weight: "600" }, callback: function (v) { return v === 1 ? "% of revenue" : v === 0 ? "% of EBITDA" : ""; } } }
          },
          plugins: {
            tooltip: {
              filter: function (it) { return !it.dataset._median; },
              callbacks: {
                title: function (it) { return it[0].raw.c ? it[0].raw.c.c : ""; },
                label: function (it) { return sig(it.raw.x, 3) + "% " + it.dataset.label.replace("% ", ""); }
              }
            }
          },
          onClick: function (ev, els) { if (els.length && els[0].element.$context.raw.c) goTo(els[0].element.$context.raw.c.u); },
          onHover: hoverCursor
        }
      });
      var nt = document.getElementById("strip-note"); if (nt) nt.textContent = notes.join(". ") + ".";
    }
  };

  /* ------------------------------------------------------------------ company page */
  CLBI.company = function () {
    var D = data();
    if (!setupCharts()) return;
    var C = window.Chart;
    var ink = css("--ink"), rule = css("--rule"), forest = css("--forest"), peer = css("--peer"), paper = css("--surface");

    // waterfall
    var wfc = document.getElementById("waterfall");
    if (wfc) {
      var w = D.wf, p = w.pressure;
      var labels = ["Climate", "Water", "Waste", "Pressure score", "Restoration", "Recycling", "Renewables", "Final score"];
      var vals = [], colors = [];
      function el(v, c) { vals.push(v == null ? null : [0, v]); colors.push(c); }
      el(w.climate, css("--climate")); el(w.water, css("--water")); el(w.waste, css("--waste"));
      el(p, css("--pressure"));
      var base = p == null ? 0 : p;
      [["rest", "--c-rest"], ["recy", "--c-recy"], ["re", "--c-re"]].forEach(function (k) {
        var v = w[k[0]] || 0;
        vals.push([base, base + v]); colors.push(css(k[1])); base += v;
      });
      el(w.final, forest);
      var lab = vals.map(function (v, i) {
        if (v == null) return "n/a";
        var d = v[1] - v[0];
        return (i >= 4 && i <= 6 ? "+" + fmt(d, 2) : fmt(d, 1));
      });
      var naLabels = {
        id: "naLabels",
        afterDatasetsDraw: function (chart) {
          var ctx = chart.ctx, h = chart.options.indexAxis === "y";
          ctx.save(); ctx.font = "italic 12px Inter, sans-serif"; ctx.fillStyle = css("--faint"); ctx.textAlign = h ? "left" : "center"; ctx.textBaseline = "middle";
          vals.forEach(function (v, i) {
            if (v != null) return;
            if (h) ctx.fillText("not scored", chart.scales.x.getPixelForValue(0) + 6, chart.scales.y.getPixelForValue(i));
            else ctx.fillText("not scored", chart.scales.x.getPixelForValue(i), chart.scales.y.getPixelForValue(0) - 10);
          });
          ctx.restore();
        }
      };
      var horiz = wfc.parentNode.clientWidth < 600;
      if (horiz) wfc.parentNode.style.height = "340px";
      var valAxis = { min: 0, max: 100, grid: { color: rule, drawTicks: false }, border: { display: false }, ticks: { stepSize: 25, padding: 8 } };
      var catAxis = { grid: { display: false }, border: { color: css("--rule-2") }, ticks: { color: ink, font: { size: 12, weight: "500" }, maxRotation: 0, autoSkip: false } };
      new C(wfc, {
        type: "bar",
        data: { labels: labels, datasets: [{ data: vals, backgroundColor: colors, borderRadius: 3, barPercentage: horiz ? 0.75 : 0.66, categoryPercentage: 0.9 }] },
        options: {
          responsive: true, indexAxis: horiz ? "y" : "x", layout: { padding: horiz ? { right: 44 } : { top: 22 } },
          scales: horiz ? { x: valAxis, y: catAxis } : { y: valAxis, x: catAxis },
          plugins: {
            valueLabels: { fmt: function (v, i) { return v == null ? "" : lab[i]; } },
            tooltip: { callbacks: { label: function (it) { var v = it.raw; return v ? (it.dataIndex >= 4 && it.dataIndex <= 6 ? "Adds " + fmt(v[1] - v[0], 2) + " points" : "Score " + fmt(v[1] - v[0], 1)) : "Not scored"; } } }
          }
        },
        plugins: [valueLabels, naLabels]
      });
    }

    // peer dots
    document.querySelectorAll("canvas[data-peer]").forEach(function (cv) {
      var el = cv.getAttribute("data-peer");
      var arr = D.peers[el] || [];
      var me = D.me[el];
      var vals = arr.map(function (a) { return a[1]; });
      var useLog = spread(vals) > 100;
      function jit(i) { var x = Math.sin((i + 3) * 78.233) * 12345.678; return ((x - Math.floor(x)) - 0.5) * 1.3; }
      var others = arr.filter(function (a) { return a[0] !== D.sym; });
      var col = css(EL[el].v);
      var ds = [
        { data: others.map(function (a, i) { return { x: a[1], y: jit(i), a: a }; }),
          backgroundColor: others.map(function (a) { return a[2] ? alpha(peer.indexOf("#") === 0 ? peer : "#C9C3B5", 0.9) : "transparent"; }),
          borderColor: others.map(function (a) { return a[2] ? "transparent" : css("--faint"); }), borderWidth: 1.2, pointRadius: 4, pointHoverRadius: 6 }
      ];
      if (me != null && me > 0) ds.push({ data: [{ x: me, y: 0, a: [D.sym, me, true, D.name] }], backgroundColor: forest, borderColor: paper, borderWidth: 2, pointRadius: 8.5, pointHoverRadius: 10 });
      new C(cv, {
        type: "scatter",
        data: { datasets: ds },
        options: {
          responsive: true, layout: { padding: { top: 6, right: 8 } },
          scales: {
            x: useLog ? { type: "logarithmic", grid: logGrid(), border: { display: false }, ticks: logTicks() }
              : { grid: { color: rule, drawTicks: false }, border: { display: false }, ticks: { maxTicksLimit: 6, callback: function (v) { return sig(v, 3); } } },
            y: { display: false, min: -1.1, max: 1.1 }
          },
          plugins: { tooltip: { callbacks: { title: function (it) { return it[0].raw.a[3]; }, label: function (it) { return sig(it.raw.x, 4) + " " + EL[el].unit + (it.raw.a[2] ? "" : " (not scored)"); } } } },
          onHover: hoverCursor,
          onClick: function (ev, els) {
            if (!els.length) return;
            var a = els[0].element.$context.raw.a, c = (window.CLBI_COMPANIES || []).filter(function (x) { return x[0] === a[0]; })[0];
            if (c && a[0] !== D.sym) goTo(c[2]);
          }
        }
      });
    });
  };
})();
