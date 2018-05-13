---
layout: page
title: Coverage
display_title: true
search_omit: true
excerpt: "Skynet Today Coverage"
extra_css: ["assets/css/toggle.css","assets/css/toggle_coverage.css" ]
extra_js: ["assets/js/toggle.js"]
permalink: /coverage
---
<form class="form" id="writingToggleForm">
  <div class="switch-field">
    <input type="radio" id="switch_news" name="switch" value="yes" checked data-st-contentid="#news"/>
    <label for="switch_news">Coverage</label>
    <input type="radio" id="switch_editorials" name="switch" value="no" data-st-contentid="#editorials"/>
    <label for="switch_editorials">Editorial</label>
  </div>
</form>
<div id='news'>
  <ul class="post-list"> 
    {% for post in site.categories.news %} 
        {% include entry.html %}
    {% endfor %}
  </ul>
</div>
<div id='editorials' style="display:none">
  <ul class="post-list"> 
    {% for post in site.categories.editorials %} 
        {% include entry.html %}
    {% endfor %}
  </ul>
</div>
