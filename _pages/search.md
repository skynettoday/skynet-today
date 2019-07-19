---
layout: page-narrow
title: Search
excerpt: "Discover all AI news and trends. Enter a topic you're interested in!"
permalink: /search.html
sitemap: false
footer_minimal: true
center: true
---


<form onsubmit="return false;" class="mt-5">
<div class="input-group">
    <input type="input" id="search" class="search-input form-control" style="padding: .875rem .75rem;"  placeholder="{{ site.data.text[site.locale].search_placeholder_text | default: 'Search Skynet Today...' }}" autofocus>
    <div class="input-group-append">
      <button class="btn btn-warning" type="button">
        <img width="20" src="{{site.baseurl}}/assets/img/icons/search.svg">
      </button>
    </div>
  </div>
</form>

<div id="results"></div>



