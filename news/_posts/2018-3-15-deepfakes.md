---
layout: post
title: "Deepfakes"
excerpt: "Has widespread misuse of AI finally arrived?"
categories: news
author: joshua_morton
editor: 
tags: []
comments: true
share: true
published: false
---

# Deepfakes

The most creative and worrying application of AI thus far in 2018.

## What Happened

In late September 2017, a reddit user by the name of "deepfakes" appeared. By
February 2018, "deepfakes" had been covered by Forbes, the BBC and the NYT, in
addition to a multitude of tech news sources.

The cause of this coverage? Deepfakes, as the name implies, used deep neural
networks to generate fake, but convincing, images and videos of pornstars with
the faces of celebrities attached to them.

The images and videos look highly realistic. Other people, like one named
"derpfakes" used the same methods for more amusing results, things like pasting
Angela Merkel's face onto Donald Trump, or sticking Nicholas Cage into every
film role ever:

![Rehost this.](https://thumbor.forbes.com/thumbor/960x0/smart/https%3A%2F%2Fblogs-images.forbes.com%2Fianmorris%2Ffiles%2F2018%2F02%2FUntitled-5-1200x675.jpg%3Fwidth%3D960)

It's important to discuss the research vs. the application in this case. The
original deepfakes appears to be based on a simplified version of [this paper
from NVIDIA](https://arxiv.org/abs/1703.00848). It however doesn't use
Generative Aversarial Networks (GANs), instead just taking advantage of dual
autoencoder with a shared encoder and latent space idea. More recent versions of
the Deepfakes code do take advantage of GANs[1][2][3], but the original did not.

## The Reactions

Vice's motherboard broke the story of deepfakes with a headline reading "We're
All Fucked" [4], in December. It focused on a worrying video where the face of
Gal Gadot, star of DC's Wonder Woman, was pasted onto the body of a pornstar.

It took another month for the coverage to really explode though. Motherboard
again broke the story that deepfakes had been appified by a tool called
"FakeApp", this time the headline read "We are Truly Fucked, Everyone Is Making
AI-Generated Fake Porn Now" [5]. FakeApp heavily automates the deepfake creation
process, and allows laypeople to create the faceswapped videos with relative
ease.

In that second article, Vice says "It isn’t difficult to imagine an amateur
programmer running their own algorithm to create a sex tape of someone they want
to harass." And other media outlets, like Lawfare went, claiming that deepfakes
and similar generative technologies will be used for blackmail, or even become a
tool used to undermine "National Security and Democracy" [6].

Soon after that second Vice Article, a number of other news outlets, including
The Verge [7], Forbes [8], and the BBC [9] provided similar coverage, not adding
much to the discussion although rehashing the potentials for abuse like revenge
porn. Then, on February 7, Reddit updated its rules about involuntary
pornography [10], outlawing " any person in a state of nudity [...] posted without
their permission, including depictions that have been faked" [11]. This caused
discussion on both Reddit [12] and Hacker News [13], about questions of ethics,
speech, and intellectual property law.

## Our Perspective

So how bad is this, are we all fucked, really?

Its not good, and for the most part the media coverage is solid. But there are a
few places where they get carried away and overestimate what the tools are
capable of now. Its important to note though that for the most part, these are
quibbles, and in general, the coverage has been correct.

While the ability of generative tools to create realistic fakes has vastly
improved over the past 5 or so years [14], they aren't yet all the way there,
and a upon close investigation, these videos will appear clearly fake. What's
more, state of the art methods for generated video rely on a paired set of
models, one that generates fakes, and one that recognizes fakes (the "GAN"
mentioned in The Research). If this continues to be the favored method, it means
that it will at least be possible to determine which things are fake, although
there's no garauntee that any given fake-recognizer will be availible.

Many of the articles also suggest faked revenge porn or blackmail as possible
outcomes. While that shouldn't be wholly discounted, that specific application
is not as easy as claimed. Deepfakes, like most machine learning models,
requires a lot of data. Making a fake requires a significant number of good
quality images of a person. For celebrities and politicians, this is easy to
come by. But for an application like personal blackmail, its less likely that
there will be a lot of good images or video availible. 

It took thousands of professional-quality headshots for a NYT reporter to get
decent results with FaceApp [15], and nearly one thousand for Sven Charlier, an
HCI researcher, to get reasonable results at a relatively low resolution. That
implies that at least for forseeable future, most deepfaked blackmail will be
low resolution and grainy.

## TLDR

Deepfaked pornography is certainly an ethical concern and bringing it to light
is important. However, media outlets probably overreach somewhat when they
suggest that you might be next.

Keep on the lookout for a longer form discussion of broader ethics in AI,
deepfakes will be central to, but only a facet of, that post.

*Josh is currently employed by Google, but these opinions are his own.*



### Citations
1. https://github.com/junyanz/CycleGAN
2. https://github.com/phillipi/pix2pix
3. https://github.com/shaoanlu/faceswap-GAN
4. https://motherboard.vice.com/en_us/article/gydydm/gal-gadot-fake-ai-porn
5. https://motherboard.vice.com/en_us/article/bjye8a/reddit-fake-porn-app-daisy-ridley
6. https://lawfareblog.com/deep-fakes-looming-crisis-national-security-democracy-and-privacy
7. https://www.theverge.com/2018/1/24/16929148/fake-celebrity-porn-ai-deepfake-face-swapping-artificial-intelligence-reddit
8. https://www.forbes.com/sites/ianmorris/2018/02/05/fakeapp-allows-anyone-to-make-deepfake-porn-of-anyone/#1cbb82b7391c
9. http://www.bbc.com/news/technology-42912529
10. https://www.reddit.com/r/announcements/comments/7vxzrb/update_on_sitewide_rules_regarding_involuntary/
11. https://www.reddithelp.com/en/categories/rules-reporting/account-and-community-restrictions/do-not-post-involuntary-pornography
12. https://www.reddit.com/r/SubredditDrama/comments/7vy9cw/rdeepfakes_the_aigenerated_fake_celebrity_porn/
13. https://news.ycombinator.com/item?id=16327489
14. https://twitter.com/goodfellow_ian/status/969776035649675265
15. https://www.nytimes.com/2018/03/04/technology/fake-videos-deepfakes.html
16. http://svencharleer.com/blog/2018/02/02/family-fun-with-deepfakes-or-how-i-got-my-wife-onto-the-tonight-show/
17. https://www.wired.com/story/gfycat-artificial-intelligence-deepfakes/

