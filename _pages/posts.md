---
layout: page
title: Posts
excerpt: "Sane, informed criticism of the latest AI hype and doomsaying"
search_omit: true
permalink: /posts
---

<ul class="post-list"> 
  {% for post in site.posts %} 
    {% if post.published %} 
      {% include entry.html %}
    {% endif %} 
  {% endfor %}
</ul>
