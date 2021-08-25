---
layout: page
title: Podcast
excerpt: "The Last Week in AI Podcast - weekly coverage of AI news and interviews."
search_omit: true
permalink: /podcast.html
image:
   feature: assets/img/podcast_logo_wide.jpg
   small: true
display_title: false
---

<div class="row justify-content-center text-left ">

<div class="col-md-8">
<h1 class="mb-3 text-black font-weight-bold text-md-center">Last Week in AI Podcast</h1>

<p><font size="+1">Check out our podcast with weekly coverage of AI news and interviews!<br>
Subscribe: <a href="https://feed.podbean.com/aitalk/feed.xml">RSS</a> |
<a href="https://podcasts.apple.com/us/podcast/lets-talk-ai/id1502782720">iTunes</a> |
<a href="https://open.spotify.com/show/17HiNdxcoKJLLNibIAyUch">Spotify</a> |
<a href="https://pca.st/podcast/824c4060-472b-0138-9766-0acc26574db2">Pocket Casts</a> |
<a href="https://www.youtube.com/channel/UCKARTq-t5SPMzwtft8FWwnA">YouTube</a><br>
Listen to our latest episodes:<br></font></p>
<iframe title="Let's Talk AI" id="multi_iframe" class="podcast_embed"
 src="https://www.podbean.com/media/player/multi?playlist=http%3A%2F%2Fplaylist.podbean.com%2F7703921%2Fplaylist_multi.xml&vjs=1&kdsowie31j4k1jlf913=4975ccdd28d39e38bf5a1ccaf0c6ca4337fa996b&size=430&skin=9&episode_list_bg=%23ffffff&bg_left=%23000000&bg_mid=%230c5056&bg_right=%232a1844&podcast_title_color=%23c4c4c4&episode_title_color=%23ffffff&auto=0&share=1&fonts=Helvetica&download=0&rtl=0&show_playlist_recent_number=10&pbad=1"
 scrolling="yes" allowfullscreen="" width="100%" height="400px" frameborder="0"></iframe>
 
<p><font size="+1">Or check out some highlight episodes:</font></p> 
    <div class="row mt-3 cardrecent">
            {% for post in site.posts %}
            {% if post.categories contains "podcast" %}
            <div class="col-md-6 mb-30">                    
                {% include themecard.html %}                    
            </div>     
            {% endif %}       
        {% endfor %}            
    </div>
</div>

<p>Our podcast theme is Deliberate Thought by Kevin MacLeod (incompetech.com).</p>

</div>
