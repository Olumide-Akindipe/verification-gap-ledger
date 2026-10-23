// Search, filter and sort for the program list. Works on the rows already in the page.
(function () {
  var $ = function (id) { return document.getElementById(id); };
  var tbody = document.querySelector("#programs tbody");
  if (!tbody) return;
  var rows = Array.prototype.slice.call(tbody.rows);
  var total = rows.length;
  var q = $("q"), level = $("f-level"), agency = $("f-agency"), status = $("f-status"), gap = $("f-gap");

  function apply() {
    var term = q.value.trim().toLowerCase(), shown = 0;
    rows.forEach(function (r) {
      var ok = (!term || r.dataset.search.indexOf(term) !== -1) &&
        (!level.value || r.dataset.level === level.value) &&
        (!agency.value || r.dataset.agency === agency.value) &&
        (!status.value || r.dataset.status === status.value) &&
        (!gap.checked || r.dataset.gap === "1");
      r.hidden = !ok; if (ok) shown++;
    });
    $("count").textContent = "Showing " + shown + " of " + total + " programs";
    $("empty").hidden = shown !== 0;
  }
  [q, level, agency, status, gap].forEach(function (el) { el.addEventListener("input", apply); el.addEventListener("change", apply); });

  var keyOf = {
    name: function (r) { return r.cells[0].textContent.trim().toLowerCase(); },
    level: function (r) { return r.dataset.level; },
    r: function (r) { return +r.dataset.r; }, c: function (r) { return +r.dataset.c; }, a: function (r) { return +r.dataset.a; }
  };
  document.querySelectorAll("#programs th button").forEach(function (b) {
    b.addEventListener("click", function () {
      var th = b.parentElement, k = b.dataset.sort;
      var dir = th.getAttribute("aria-sort") === "ascending" ? "descending" : "ascending";
      document.querySelectorAll("#programs th").forEach(function (h) { h.removeAttribute("aria-sort"); });
      th.setAttribute("aria-sort", dir);
      var f = keyOf[k], s = dir === "ascending" ? 1 : -1;
      rows.sort(function (x, y) { var a = f(x), b2 = f(y); return a < b2 ? -s : a > b2 ? s : 0; });
      rows.forEach(function (r) { tbody.appendChild(r); });
    });
  });
})();
