---
layout: post
title: "Are AI systems racist? Or is it a problem of diversity?"
excerpt: "Flashy headlines often hijack meaningful and important conversations, even when the articles are solid. Who reads the fine print anyway?"
author: viraat_aryabumi
editor: [andrey_kurenkov, limor_gultchin]
tags: [facial recognition,bias,ethics,fairness]
---

A great example of how misleading and click-baity article titles can cause hype and often diminish well-researched articles. 


## What Happened

Joy Buolamwi, a Rhodes scholar at MIT Media labs found that facial recognition systems [^frexplainer] did not work as well for her as it did for others. The models just did not seem to recognize her compared to her fairer skinned friends. This led her to investigate facial recognition systems in the context of people of color. In her recently published [paper](http://proceedings.mlr.press/v81/buolamwini18a/buolamwini18a.pdf) and project - [“Gender shades”](http://gendershades.org), she evaluated commercially available gender identification systems from Microsoft, IBM, and the chinese company Mobvii. 

The results showed that all three systems performed poorly for people of color compared to fairer skinned subjects. To make things worse, the systems performed abysmally for darker-skinned women failing to correctly identify them up to 34% of the time. Looking for what might be causing such disparity in performance led Joy to examining two commonly used datasets [^datasetexplainer] of faces. She found both datasets to be composed of a higher number of lighter skinned subjects leading to an imbalance [^imbalance] in the datasets. To help correct the lack of balanced datasets she has contributed a new dataset consisting of face images which is relatively more balanced on the basis of skin color. 

This work was covered by the NYT, WIRED, The Verge and other media outlets. 


## The Reactions

The media reacted to the results of the paper with headlines like "Photo algorithms ID white men fine—black women, not so much” [(WIRED)](https://www.wired.com/story/photo-algorithms-id-white-men-fineblack-women-not-so-much) and “Facial Recognition Is Accurate, if You’re a White Guy” [(NYT)](https://www.nytimes.com/2018/02/09/technology/facial-recognition-race-artificial-intelligence.html). 

* Contrary to the headlines which seem to blame the algorithms, the wired article says, 
> The skewed accuracy appears to be due to underrepresentation of darker skin tones in the training data used to create the face-analysis algorithms.

* [The Verge](https://www.theverge.com/2018/2/11/17001218/facial-recognition-software-accuracy-technology-mit-white-men-black-women-error) put it succinctly, saying 
> The algorithms aren’t intentionally biased, but more research supports the notion that a lot more work needs to be done to limit these biases.

* As the Atlantic [points out](https://www.theatlantic.com/technology/archive/2016/04/the-underlying-bias-of-facial-recognition-systems/476991/), 
>An algorithm trained exclusively on either African American or Caucasian faces recognized members of the race in its training set more readily than members of any other race.

Microsoft and IBM were both given access to Joy Buolamwi’s research and the newly created dataset. Microsoft’s response was that it had already taken steps to improve the accuracy of the facial recognition technology. IBM went a step further and published a [white paper](https://www.ibm.com/blogs/research/2018/02/mitigating-bias-ai-models/
) replicating the results from the paper and showing the improvements in the systems after re-training on a balanced dataset. 

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">.<a href="https://twitter.com/jovialjoy?ref_src=twsrc%5Etfw">@jovialjoy</a> sent a pre-print of their paper to the companies after <a href="https://twitter.com/hashtag/FAT2018?src=hash&amp;ref_src=twsrc%5Etfw">#FAT2018</a> acceptance. Face++ didn&#39;t respond. MS sent a response. IBM had the best response -- replicated the paper internally and released a new API yesterday. Wow. New API classified darker females at 96.5%</p>&mdash; Alex Hanna, Data Witch (@alexhanna) <a href="https://twitter.com/alexhanna/status/967434590494355456?ref_src=twsrc%5Etfw">February 24, 2018</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 

While most of the NYT article focused on the research itself, it closed with this great line 
> “Technology", Ms. Buolamwini said, "should be more attuned to the people who use it and the people it’s used on.
You can’t have ethical A.I. that’s not inclusive,” she said. “And whoever is creating the technology is setting the standards.”

The reports rightly point out the underlying problems of diversity and inclusivity that the tech industry faces. 

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Here is how a diversity issue in tech companies leads to a bias in tech usability. &quot;Facial Recognition Is Accurate, if You’re a White Guy&quot; <a href="https://t.co/n2hz3DrwUH">https://t.co/n2hz3DrwUH</a></p>&mdash; Fiede Schillmoeller (@fiede) <a href="https://twitter.com/fiede/status/962835998999658496?ref_src=twsrc%5Etfw">February 11, 2018</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 

## Our Perspective

How bad is this really? Are the systems racist? Or are the people designing these systems wantonly discriminating against people of color?

Not really. As most of the media coverage correctly points out, this is a problem caused by lack of balanced data. As IBM’s white paper shows, when these systems are trained with datasets that are well balanced they are very accurate. The important question to ask is why these systems were not trained with balanced datasets from the beginning. The answer might be, as most of the articles say, due to a lack of diversity in AI. 

On a broader note, face recognition might actually be the least of our worries with bias and fairness of AI systems. There are worrying examples of bias and discrimination in [criminal sentencing](https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing), [hiring](https://work.qz.com/1098954/ai-is-the-future-of-hiring-but-it-could-introduce-bias-if-were-not-careful/), and mortgage grants. Worse, recent [research](http://arxiv.org/abs/1707.00391) has shown that when multiple AI systems are used together, where each of them is bias-free, can still amplify bias. 

Although challenges exist, it is not all bad news - a fast growing community of researchers are now hard at work on problems in the fields of Fairness, Accountability and Transparency. Some of the best minds in the field have set their sights on these problems. The community has responded strongly to these issues and have 

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Be woke. <a href="https://twitter.com/mrtz?ref_src=twsrc%5Etfw">@mrtz</a>&#39;s epic class on fairness in <a href="https://twitter.com/hashtag/MachineLearning?src=hash&amp;ref_src=twsrc%5Etfw">#MachineLearning</a> is a must read for everyone using ML. <a href="https://t.co/nfoiJtoDZE">https://t.co/nfoiJtoDZE</a> <a href="https://t.co/AvSrL9HduF">pic.twitter.com/AvSrL9HduF</a></p>&mdash; Delip Rao (@deliprao) <a href="https://twitter.com/deliprao/status/904892267869093888?ref_src=twsrc%5Etfw">September 5, 2017</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 


<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Excited to see 54 submissions to FATML 2018, up 12.5% from last year even though <a href="https://twitter.com/fatconference?ref_src=twsrc%5Etfw">@fatconference</a> just happened.</p>&mdash; Moritz Hardt (@mrtz) <a href="https://twitter.com/mrtz/status/991699500593922048?ref_src=twsrc%5Etfw">May 2, 2018</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 

However, most of the research attacks these problems from a technical perspective. As Kate Crawford points out in her [excellent keynote]( https://www.youtube.com/watch?v=fMym_BKWQzk
) at the NIPS 2017 conference, bias cannot be considered a purely technical problem.

> “Bias is a highly complex issue that permeates every aspect of machine learning. We have to ask: who is going to benefit from our work, and who might be harmed? To put fairness first, we must ask this question.”

As [Moustapha Cissé](https://twimlai.com/twiml-talk-108-security-safety-ai-adversarial-examples-bias-trust-moustapha-cisse/) of Facebook AI Research says,
> the datasets are a result of the problems being considered by the designers. If we focus on problems that are important to only a specific population of the world, the end result is these unbalanced datasets. These datasets then, are used for training the models that make biased and unfair decisions.

To ensure that a wide variety of problems are considered, there is a need for a more diverse community of researchers and engineers in AI.

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Looking forward to seeing <a href="https://twitter.com/jovialjoy?ref_src=twsrc%5Etfw">@jovialjoy</a> and <a href="https://twitter.com/timnitGebru?ref_src=twsrc%5Etfw">@timnitgebru</a> present their paper on bias in facial recognition systems at <a href="https://twitter.com/hashtag/FAT2018?src=hash&amp;ref_src=twsrc%5Etfw">#FAT2018</a> this weekend—so much research needed to ensure AI is inclusive <a href="https://t.co/KeL0Aq6stx">https://t.co/KeL0Aq6stx</a></p>&mdash; Mustafa Suleyman (@mustafasuleymn) <a href="https://twitter.com/mustafasuleymn/status/967235628776742913?ref_src=twsrc%5Etfw">February 24, 2018</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 


While the content of the news articles is well articulated and on point, hyperboles such as the ones in the headlines are harmful and misleading. In the short-term, as pointed out in this [great blog post](https://developers.googleblog.com/2018/04/text-embedding-models-contain-bias.html) by researchers at Google, researchers and engineers need to be aware of undesirable biases that might exist in the systems they are designing and look to mitigate them. Further, system designers should be mindful of *all* possible users of their system. The onus is on the Machine Learning and AI community to be more inclusive and work towards greater diversity in datasets and in the community itself.


## TLDR

Contrary to what some headlines said, the systems in question are not racist technology.  Non inclusive datasets produced skewed results, but the same models showed remarkable accuracy when trained on a more racially diverse set. However, this is still a warning sign pointing at an underlying problem - lack of diversity in the AI community. In the short-term, researchers and engineers need to be aware of all their users and the fact that the systems they build may contain possible biases. While increasing research in the fields of fairness, accountability and transparency provides hope for a technical solution, the AI community needs to step up and make efforts to be more inclusive and increase diversity. 

[^frexplainer]: A facial recognition system is a technology capable of identifying or verifying a person from a digital image or a video frame from a video source.
[^datasetexplainer]: A dataset is a collection of data. All Machine Learning systems are “trained” on a dataset. If you’re confused or intimidated by the term machine learning - watch [this video](https://www.youtube.com/watch?v=f_uwKZIAeM0)
[^imbalance]: When the dataset consists of more examples belonging to one group than the others it leads to an imbalance. For example, if the datasets consisted of more males than females it would be considered an imbalanced dataset.

