---
layout: page
permalink: /publications/
title: Publications
nav: true
nav_order: 3
---

<div class="pub-intro">
  <div class="pub-intro-text">
    <span class="pub-type-badge journal">Journal papers</span>,
    <span class="pub-type-badge conference">conference papers</span>,
    and <span class="pub-type-badge other">others</span>
    (e.g., workshop papers or extended abstracts).
    For citations and other metrics see
    <a href="https://scholar.google.com/citations?user=4Yp4lRwAAAAJ&hl=en">my Google Scholar page</a>.
  </div>
  <div class="pub-intro-controls">
    <button id="pub-sort-toggle" type="button" class="btn btn-sm z-depth-0">Sort by type</button>
    {% include bib_search.liquid %}
  </div>
</div>

<div class="publications">

{% bibliography %}

</div>

<script src="{{ '/assets/js/publications_sort.js' | relative_url | bust_file_cache }}"></script>
