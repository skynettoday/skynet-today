---
title: AlphaGo Zero Is Not A Sign of Imminent Human-Level AI
image:
  feature: content/editorials/images/is-alphago-zero-overrated/history.png
author: andrey_kurenkov
editor: joshua_morton
tags: [hype,BigBiz,game,Google]
excerpt: "Why DeepMind's Go playing program is not about to solve all of AI"
---

## Why AlphaGo Zero Is Great
Let's start with the coverage about DeepMind's recent successor to AlphaGo[^AlphaGo], AlphaGo Zero:

* ["Google's New AlphaGo Breakthrough Could Take Algorithms Where No Humans Have Gone"](http://fortune.com/2017/10/19/google-alphago-zero-deepmind-artificial-intelligence/): 
> "While it sounds like some sort of soda, AlphaGo Zero may represent as much of a breakthrough as its predecessor, since it could presage the development of algorithms with skills that humans do not have. ... AlphaGo achieved its dominance in the game of Go by studying the moves of human experts and by playing against itself—a technique known as reinforcement learning. AlphaGo Zero, meanwhile, trained itself entirely through reinforcement learning. And, despite starting with no tactical guidance or information beyond the rules of the game, the newer algorithm managed to beat the older AlphaGo by 100 games to zero."
* ["DeepMind’s Go-playing AI doesn’t need human help to beat us anymore"](https://www.theverge.com/2017/10/18/16495548/deepmind-ai-go-alphago-zero-self-taught): 
> "The company’s latest AlphaGo AI learned superhuman skills by playing itself over and over"
* ["'It's able to create knowledge itself': Google unveils AI that learns on its own"](https://www.theguardian.com/science/2017/oct/18/its-able-to-create-knowledge-itself-google-unveils-ai-learns-all-on-its-own): 
> "In a major breakthrough for artificial intelligence, AlphaGo Zero took just three days to master the ancient Chinese board game of Go ... with no human help"
* [" Google Artificial Intelligence 'Alpha Go Zero' Just Pressed Reset On How To Learn"](https://www.inc.com/lisa-calhoun/google-artificial-intelligence-alpha-go-zero-just-pressed-reset-on-how-we-learn.html): 
> "Alpha Go Zero is changing the game for how we solve big problems."

Point being: AlphaGo Zero (which we'll go ahead and shorten to AG0) is arguably the most impressive and definitely the most praised[^praised] recent AI accomplishment[^unaware]. Roughly speaking, AG0 is just a [Deep](http://theai.wiki/Deep%20Learning) [Neural Network](http://theai.wiki/Neural%20Network) that takes the current state of a Go board as input, and outputs a Go move. Not only is this much simpler than the original AlphaGo[^simpler], but it is also trained purely through self-play (pitting different AlphaGo Zero neural nets against each other; the original AlphaGo was 'warmed up' by training to mimic human expert Go players). It's not exactly right that it learns 'with no human help', since the very rules of Go are hand-coded by humans rather than learned by AlphaGo, but the basic idea that it learns through self-play rather without any mimicry of human Go players is correct. I'll let the key researcher behind it expand on that:

<figure>
     <iframe width="560" height="315" src="https://www.youtube.com/embed/tXlM99xPQC8" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
     <figcaption>DeepMind's own explanation of why AG0 is so exciting. 
</figcaption>
</figure>

So, surely DeepMind's demonstration that an AI algorithm can achieve superhuman Go and Chess play purely through self-play is a testament to the usefulness of such techniques for solving the hard problems of AI? Well, to some extent yes — it has taken the field decades to get here, since the [branching factor](http://theai.wiki/Branching%20Factor) of Go does indeed make it a challenging board game. This is also the first a time the same Deep Learning algorithm was used to crack both Chess and Go[^general], and was not specifically tailored for it such as was the case with [Deep Blue](https://en.wikipedia.org/wiki/Deep_Blue_(chess_computer)) (the much heralded machine of IBM that was the first to beat humanity's best at Chess) and the original AlphaGo. Therefore, AG0 is certainly monumental and exciting work (and great PR). 

<figure>
      <img src="/content/editorials/images/is-alphago-zero-overrated/history.png" alt="Game History"/>
     <figcaption>AlphaGo is the culmination of research into Game AI that stretches all the way back to the birth of AI as a research field. So, it is an inarguably great and historic achievement.<b><a href="http://www.andreykurenkov.com/writing/ai/a-brief-history-of-game-ai/">(source)</a></b></figcaption>
</figure>

## Why AlphaGo Zero Is Not That Great
With those positive things having been said, some perspective: AG0 is not really a testament to the usefulness of such techniques for solving the hard problems of AI. You see, Go is only hard within the context of the simplest category of AI problems. That is, it is in the category of problems with every property that makes a learning task easy: it is [deterministic, discrete, static, fully observable, fully-known, single-agent, episodic](https://en.wikibooks.org/wiki/Artificial_Intelligence/AI_Agents_and_their_Environments), cheap and easy to simulate, easy to score... Literally the only challenging aspect of Go is its huge branching factor. Predictions that [AGI (Artificial General Intelligence)](http://theai.wiki/AGI) is imminent based only on AlphaGo's success can be safely dismissed — [the real world is vastly more complex than a simple game like Go](https://medium.com/@karpathy/alphago-in-context-c47718cb95a5). Even fairly similar problems that have most but not all of the properties that make a learning task easy, [such as the strategic video game DotA II](/content/news/openai-dota-ii/), are far beyond our grasp right now. 

<figure>
     <img src="/content/editorials/images/is-alphago-zero-overrated/venn.svg" alt="Venn"/>
     <figcaption>A (rough) diagram of AI problem complexity. Note that Go and (most) Atari games are in the same league as chess; just about the only distinction is branching factor. The techniques that power AG0 may solve games like Go, but as <a href="http://www.skynettoday.com/news/alphago/">I've written elsewhere in more detail</a> most AI problems are vastly more difficult — categorically different.
    </figcaption>
</figure>

Another important thing to understand beyond the categorical simplicity of Go is its narrowness. AG0 is a definite example of [Weak AI](http://theai.wiki/Weak%20AI), also known as narrow AI. Weak AI agents are characterized by only being able to perform one 'narrow' task, such as playing a 19 by 19 game of Go. Though AG0 has the impressive ability to learn to play 3 different board games, it does so separately per game [^separately]. And, it can only learn a vary narrow range of games: basically just 2-player grid based board games without any necessary memorization of prior positions or moves[^memorization].
<figure>
<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">&quot;Generalized AI is worth thinking about because it stretches our imaginations and it gets us to think about our core values and issues of choice and free will that actually do have significant applications for specialized AI.&quot; - <a href="https://twitter.com/BarackObama?ref_src=twsrc%5Etfw">@BarackObama</a> <a href="https://t.co/VFhJsMXuIq">pic.twitter.com/VFhJsMXuIq</a></p>&mdash; Lex Fridman (@lexfridman) <a href="https://twitter.com/lexfridman/status/976461233443561477?ref_src=twsrc%5Etfw">March 21, 2018</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
     <figcaption>In a <a href="https://www.wired.com/2016/10/president-obama-mit-joi-ito-interview/">lengthy interview with Wired</a>, then-president Obama displayed an impressively nuanced understanding of the state of AI. If only some unnamed billionaires would communicate to the public similarly...
     </figcaption>
</figure>

So, while AG0 works and its achievement is impressive, it is fundamentally similar to Deep Blue in being an expensive system engineered over many years with millions of dollars of investment purely for the task of playing a game — nothing else. Though Deep Blue was great PR for IBM, all that work and investment is not usually seen as having contributed much to the progress of broader AI research, having been ultra-specific to solving the problem of playing Chess. Just as with the algorithms that power AG0, human-tweaked heuristics and sheer computational brute force can definitely be used to solve some challenging problems — but they ultimately did not get us far beyond Chess, not even to Go. We should ask ourselves: can the techniques behind AG0 get us far beyond Go?

<figure>
<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">&quot;Games (Chess, Go, Dota) represent closed systems, which means we humans filled the machine with a target, with rules. There is no automatic transfer of the knowledge that machines could accumulate in closed systems to open-ended systems.&quot; - Garry Kasparov <a href="https://t.co/ysdV7sG9Qv">pic.twitter.com/ysdV7sG9Qv</a></p>&mdash; Lex Fridman (@lexfridman) <a href="https://twitter.com/lexfridman/status/974624143441350658?ref_src=twsrc%5Etfw">March 16, 2018</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
     <figcaption>Gary Kasparov, the very man who faced and ultimately lost to Deep Blue, on the limitations of Deep Blue and implicitly AlphaGo.
     </figcaption>
</figure>

Probably, yes; the algorithms behind AG0 (Deep Learning and self-play) are inherently more general than human-defined heuristics and brute computation[^likely]. Still, it is important to understand and remember the parallels between Deep Blue and AG0: **at the end of the day, both Deep Blue and AG0 are narrow AI programs that were built (at least in part) as PR boons for large companies by huge teams at the costs of millions of dollars; they deal with problems which are difficult for humans, but which are also relatively simple for computers.**

<figure>
     <img src="/content/editorials/images/is-alphago-zero-overrated/ibm.png" alt="PR"/>
     <figcaption>"One day after its chess computer defeated Garry Kasparov, the world chess champion, I.B.M. stock surged to a 10-year high and was only a bit shy of its record." <b><a href="http://www.nytimes.com/1997/05/13/business/ibm-s-stock-surges-by-3.6.html">(source)</a></b>
    </figcaption>
</figure>

I write this not to be controversial or take away from DeepMind's fantastic work, but rather to fight against all the unwarranted hype AG0's success has generated and encourage more conversation about the limitations of deep learning and self-play. More people need to [step up](https://arxiv.org/abs/1801.05667) and [say this kind of stuff](https://www.alexirpan.com/2018/02/14/rl-hard.html) for the general public as well as the AI research community to not be led astray by hype and PR.

<figure>
      <img src="/content/editorials/images/is-alphago-zero-overrated/hype.png" alt="AI Hype"/>
     <figcaption>AGI Doomsayers overhype the significance of things like AG0 while people like me try to counter them and bring about disillusionment; meanwhile there are plenty of ethical concerns and potential misuses of AI to worry about already. Let's hope we reach the plateau of productivity soon... <a href="https://en.wikipedia.org/wiki/Hype_cycle"><b>(source)</b></a></figcaption>
</figure>

And all that aside, it should still be asked:  might there be a better for AI agents to learn to play Go? The very name AlphaGo Zero is in reference to the idea that the model learns to play Go ["from scratch"](https://deepmind.com/blog/alphago-zero-learning-scratch/), without any further human input or explanation. But is learning 'from scratch' really such a good thing? Imagine you knew nothing about Go and decided to start learning it. You would definitely read the rules, some high level strategies, recall how you played similar games in the past, get some advice... right? And it indeed at least partially because of the learning 'from scratch' **limitation** of AlphaGo Zero that it is not truly impressive compared to human learning: like Deep Blue, it still relies on seeing orders of magnitude more Go games and planning for orders of magnitude more scenarios in any given game than any human ever does.

<figure>
     <img src="/content/editorials/images/is-alphago-zero-overrated/go_gif.gif" alt="Go GIF"/>
     <figcaption>The progression of AG0's skill. It is certainly impressive that it takes 'just' 3 days of non-stop computation to get to best-human-in-the-world skill. But perhaps we should also note it takes a whole day and orders of magnitude more games than humans get to experience in their lifetimes to get to an ELO score of 0 (which even the weakest human can do easily)? From <a href="https://deepmind.com/blog/alphago-zero-learning-scratch/"><b>"DeepMind's AlphaGo Zero Blog Post"</b></a>
     </figcaption>
</figure>

## TLDR
So, let's sum up: though AlphaGo and AG0's achievements are historic and impressive, they also represent little if any progress in tackling the truly hard problems of AI (not to mention AGI). Still, as with any field all AI researchers stand on the shoulders of their predecessors; though these techniques may not foreshadow the coming of AGI, they are definitely part of the Deep Learning Revolution the field is still in the midst of and the ideas that they are based on will doubtlessly enable future progress. As with Deep Learning as a whole, it is important to appreciate these fantastic accomplishments for the field of AI without losing perspective about their limitations.

[^AlphaGo]: AlphaGo is the program that famously beat humanity's best Go player Lee Sedol.
[^unaware]: For those unaware, AlphaGo Zero is the name of an algorithm discussed in a paper late last year.
[^praised]: At least, praised by non-technical news coverage
[^simpler]: In contrast to AG0, AlphaGo involved several neural nets and features specific to Go.
[^memorization]: That is, on any given move the board contains all the necessary information to decide on the next move; no memory of the past required. 
[^general]: There are many approaches to [General Game Playing](https://en.wikipedia.org/wiki/General_game_playing) that cover much more than just Chess and Go, and neither AG0 nor any Deep Learning approach had yet to be compared to those in the standard competitions they are pitted against each other at.
[^separately]: That is, there is not a single trained neural net that can play the 3 games, but 3 separate neural nets with one for each game.
[^likely]: It's quite likely that right now researchers and engineers at DeepMind are working hard to demonstrate the next version of AlphaGo, which will presumably learn to play multiple games rather than just one.
