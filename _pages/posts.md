---
layout: page
title: Posts
excerpt: "An archive of articles sorted by date."
search_omit: true
permalink: /posts
---
{% include mailchimp-sign-up.html %}
<ul class="post-list"> 
  {% for post in site.posts %} 
    {% if post.published %} 
      {% include entry.html %}
    {% endif %} 
  {% endfor %}
</ul>
