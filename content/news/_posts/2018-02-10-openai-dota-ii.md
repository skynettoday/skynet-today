---
title: "OpenAI's Not So Open DotA AI"
excerpt: "An impressive demo by OpenAI leaves many questions unanswered."
categories: news
author: joshua_morton
editor: andrey_kurenkov
tags: [OpenAI,game,hype]
---

Among the biggest AI stories of 2017, and one of the most opaque in terms of
actual significance. 

## What Happened
Just months after [AlphaGo's historic
triumph](https://en.wikipedia.org/wiki/Future_of_Go_Summit) against the world's
best human Go player, OpenAI released an [incredible
video](https://openai.com/the-international/) and [associated press
release](https://blog.openai.com/dota-2/) showing that for the first time ever,
a team was able to develop a self-learning bot capable of beating professionals
at [DotA II](https://en.wikipedia.org/wiki/Dota_2) (an online multiplayer game).

Unfortunately, OpenAI didn't accompany their press with an academic paper. At
first, they only released a video that purported to show some of the mechanics
the bot was able to learn, a short blog post summary, and an offer to apply to
work at OpenAI. Highly unusual.

<blockquote class="twitter-tweet" data-lang="en" align="center" data-conversation="none"><p lang="en" dir="ltr">AI
research community spent many hours investigating the extent of the achievement.
OpenAI could have been, well, open about what they did.</p>&mdash; Mark O. Riedl
(@mark_riedl) <a
href="https://twitter.com/mark_riedl/status/897190855735480323?ref_src=twsrc%5Etfw">August
14, 2017</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js"
charset="utf-8"></script>

The most the broader AI community ever got was [a longer blog
post](https://blog.openai.com/more-on-dota-2/). This blog post did contain some
important information: a clarification that the bot was primarily trained via [competetive self-play](https://blog.openai.com/competitive-self-play/),
a timeline of the model's skill, and some discussion of the limitations of the agent 
(that the bot had to be explicitly taught certain necessary strategies, and that it was 
weak against certain uncommon tactics).

However, even this post fell short of the discussion of methodology one would
normally expect from a paper. It instead focused mostly on perceived shortcomings
and the (still quite interesting!) infrastructural challenges of getting DotA to
run in an environment suitable for repeated self-play.

A paper with significant results in the area of real-time strategy or popular online
multiplayer games would be groundbreaking. Thus far, successful self-learning
agents in such games have proven elusive. The freedom that players
have in games like Starcraft and DotA compared to ones like Chess and Go makes
the former much more difficult to "solve" with conventional machine learning and
game AI. So it is a significant letdown that OpenAI did not choose to publish
their approach with the justification that "We’re not ready to talk about agent
internals — the team is focused on solving 5v5 first."

## The Reactions
OpenAI themselves claim that the bot

> has learned — entirely via self-play — to predict where other players will
> move, to improvise in response to unfamiliar situations, and how to influence
> the other player’s allied units to help it succeed.

OpenAI co-founder Elon Musk was quick to chime in

<blockquote class="twitter-tweet" data-lang="en" align="center"><p lang="en" dir="ltr">If
you&#39;re not concerned about AI safety, you should be. Vastly more risk than
North Korea. <a
href="https://t.co/2z0tiid0lc">pic.twitter.com/2z0tiid0lc</a></p>&mdash; Elon
Musk (@elonmusk) <a
href="https://twitter.com/elonmusk/status/896166762361704450?ref_src=twsrc%5Etfw">August
12, 2017</a></blockquote>
<blockquote class="twitter-tweet" data-lang="en" align="center"><p lang="en" dir="ltr">Nobody
likes being regulated, but everything (cars, planes, food, drugs, etc)
that&#39;s a danger to the public is regulated. AI should be too.</p>&mdash;
Elon Musk (@elonmusk) <a
href="https://twitter.com/elonmusk/status/896169801277517824?ref_src=twsrc%5Etfw">August
12, 2017</a></blockquote>

And his alarming statements were soon picked up by tech media, exemplified by
this frightening headline from The Verge:

> [The world’s best Dota 2 players just got destroyed by a killer AI from Elon
> Musk’s
> startup](https://www.theverge.com/2017/8/11/16137388/dota-2-dendi-open-ai-elon-musk)

Yikes!

Other descriptions were more varied, with The Register calling the results
[humiliating and
scary](https://www.theregister.co.uk/2017/08/12/openai_bot_beats_top_dota_2_players_in_surprise_match/),
and TechCrunch giving a much more reserved description, simply calling the bot
[undefeated](https://techcrunch.com/2017/08/12/openai-bot-remains-undefeated-against-worlds-greatest-dota-2-players/).
Almost every article though, cited Musk's tweets.

Luckily, more level-headed coverage quickly followed:

> [Did Elon Musk’s AI champ destroy humans at video games? It’s complicated
](https://www.theverge.com/2017/8/14/16143392/dota-ai-openai-bot-win-elon-musk)

> [Hype or Not? Some Perspective on OpenAI’s DotA 2
> Bot](http://www.wildml.com/2017/08/hype-or-not-some-perspective-on-openais-dota-2-bot/)

These articles are able to bring a level of expertise and analysis that some of
the earlier publications lacked, but unfortunately come somewhat delayed when
compared to the more exciting headlines.

## Our Perspective

To begin, it's difficult to understate how unusual it is that there is no
paper here. The only information that has released is a press release and a
follow up blog post.

Further, some of the claims made in the first press release do not appear to
hold up to scrutiny. For example, one of most impressive parts of the demo,
creep blocking, [was not learned through self
play](https://news.ycombinator.com/item?id=15001521), but was taught via some
other method. The longer blog post by OpenAI also brings up another issue: 5v5
and 1v1 DotA are very different games. The OpenAI bot has trouble handling
unusual situations, but as [OpenAI says](https://blog.openai.com/more-on-dota-2/):

>for 5v5, [unusual situations] aren’t exploits at all, and we’ll need a system
>which can handle totally weird and wacky situations it’s never seen.

In fact, OpenAI was not the first to encounter this same issue when dealing with
1v1 games. Earlier in 2017 some MIT researchers were able to [use similar
self-play methods to play Super Smash Bros Melee at a near-professional
level](https://arxiv.org/pdf/1702.06230.pdf). They too encountered similar
issues with "degenerate" strategies. 

This is not to say that *nothing* novel was accomplished. The bot did appear to
learn at least one unique skill: the ability to deny information by casting a
spell from just outside the enemy's vision range.

<blockquote class="twitter-tweet" data-conversation="none" data-lang="en" align="center"><p
lang="en" dir="ltr">Most impressive was re: partial observability. Much of 1v1
is observable/predictable but avoiding enemy&#39;s vision due to game mechanic
is ++. <a
href="https://t.co/8lqmhKSEyP">pic.twitter.com/8lqmhKSEyP</a></p>&mdash; Smerity
(@Smerity) <a
href="https://twitter.com/Smerity/status/897959521661759488?ref_src=twsrc%5Etfw">August
16, 2017</a></blockquote>

Unfortunately, without a full paper it is difficult to fairly judge how
impressive that is. The questionable novelty of their achievement, lack of
transparency, and exaggerated PR all tarnished what was otherwise a new
impressive milestone for AI.

<blockquote class="twitter-tweet" data-lang="en" align="center"><p lang="en" dir="ltr">To
clarify: what OpenAI did was cool. Then Musk stepped in and made unjustified
hyperbolic claims, spoiling the achievement &amp; casting doubt.</p>&mdash; Mark
O. Riedl (@mark_riedl) <a
href="https://twitter.com/mark_riedl/status/897190444957913088?ref_src=twsrc%5Etfw">August
14, 2017</a></blockquote>

## TLDR

While OpenAI undoubtedly created an impressive demo, it seems unlikely that
their research, if it is ever published, will have been much more than an
application of existing methods to a new game under a very specifically
controlled set of circumstances. In no way does it represent a "Killer AI" or
some sort of existential threat.


*Josh is currently employed by Google, but these opinions are his own.*

