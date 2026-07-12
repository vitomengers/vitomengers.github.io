// Sort the publications list either by year (default) or by paper type.
// - "By year" view: years descending; within each year sorted by type
//   (journal, conference, preprint, workshop papers / extended abstracts).
// - "By type" view: types in the same order; within each type sorted by year.
document.addEventListener("DOMContentLoaded", function () {
  const container = document.querySelector(".publications");
  const toggle = document.getElementById("pub-sort-toggle");
  if (!container || !toggle) return;

  const TYPE_ORDER = ["journal", "conference", "preprint", "workshop_or_abstract"];
  const TYPE_LABELS = {
    journal: "Journal papers",
    conference: "Conference papers",
    preprint: "Preprints",
    workshop_or_abstract: "Workshop papers and extended abstracts",
    other: "Other",
  };

  const typeRank = (t) => {
    const i = TYPE_ORDER.indexOf(t);
    return i === -1 ? TYPE_ORDER.length : i;
  };

  // Capture every entry once, keeping a reference to its <li> node so we can
  // move (not clone) it between layouts and preserve its event handlers.
  const entries = [];
  container.querySelectorAll("ol.bibliography > li").forEach(function (li) {
    const row = li.querySelector(".row");
    const year = parseInt((row && row.dataset.year) || "0", 10);
    let type = (row && row.dataset.papertype) || "";
    if (!TYPE_ORDER.includes(type)) type = "other";
    entries.push({ li, year, type });
  });

  const clear = () =>
    container.querySelectorAll("h2.bibliography, ol.bibliography").forEach((el) => el.remove());

  function appendGroup(title, items) {
    const h2 = document.createElement("h2");
    h2.className = "bibliography";
    h2.setAttribute("data-toc-skip", "");
    h2.textContent = title;
    const ol = document.createElement("ol");
    ol.className = "bibliography";
    items.forEach((e) => ol.appendChild(e.li));
    container.appendChild(h2);
    container.appendChild(ol);
  }

  function renderByYear() {
    clear();
    const years = [...new Set(entries.map((e) => e.year))].sort((a, b) => b - a);
    years.forEach((yr) => {
      const items = entries
        .filter((e) => e.year === yr)
        .sort((a, b) => typeRank(a.type) - typeRank(b.type));
      appendGroup(String(yr), items);
    });
  }

  function renderByType() {
    clear();
    const types = [...new Set(entries.map((e) => e.type))].sort((a, b) => typeRank(a) - typeRank(b));
    types.forEach((t) => {
      const items = entries.filter((e) => e.type === t).sort((a, b) => b.year - a.year);
      appendGroup(TYPE_LABELS[t] || "Other", items);
    });
  }

  // Re-apply any active bibsearch filter after we rebuild the DOM.
  function refreshSearch() {
    const box = document.getElementById("bibsearch");
    if (box) setTimeout(() => box.dispatchEvent(new Event("input")), 0);
  }

  let byType = false;
  function render() {
    if (byType) {
      renderByType();
      toggle.textContent = "Sort by year";
    } else {
      renderByYear();
      toggle.textContent = "Sort by type";
    }
    refreshSearch();
  }

  toggle.addEventListener("click", function () {
    byType = !byType;
    render();
  });

  render();
});
