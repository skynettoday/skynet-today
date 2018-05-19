---
layout: post
title: "Tesla's Lethal Autopilot Crash — A Failing of UI as Much as AI"
excerpt: "The tragedy might have been avoided if the limitations of the Autopilot were communicated more clearly"
author: joshua_morton
editor: andrey_kurenkov
tags: [Tesla,autonomy,ethics,BigBiz]
redirect_from: /content/news/tesla-crash/
permalink: /briefs/tesla-crash/
---

A "self-driving" car crashes, tragically killing its driver. 
Coverage centers on who is to blame, but seems to
miss one key insight.

## What Happened

On March 23, 2018, a Tesla Model X crashed into a median on Highway 101 in
Mountain View California, killing its occupant. Like a similar crash in May 2016
the vehicle’s “Autopilot” was enabled at the time of the crash, and as far as we
know, the driver's hands were not on the wheel.

Soon after the [National Transportation Safety Board
 (NTSB)](https://www.ntsb.gov/Pages/default.aspx) and Tesla opened an investigation into the cause of the
accident. This investigation is still ongoing. [TechCrunch has a great
writeup on the facts of the situation if you want to learn
more](https://techcrunch.com/story/tesla-model-x-fatal-crash-investigation/). 
The current predominant theory is that the autopilot incorrectly followed road markings as a
lane split in an left-lane exit/interchange.

## The Reactions

The story around the crash developed gradually over weeks:

* Tesla initially [released a
  statement](https://www.tesla.com/blog/what-we-know-about-last-weeks-accident)
  outlining a few quick points about the accident, noting that the crash was
  likely made more severe due to the lack of a crash attenuator (a safety device
  built into the highway).

* A few days later, Tesla released a followup
  [statement](https://www.tesla.com/blog/update-last-week%E2%80%99s-accident)
  that contained a few important details: Autopilot was engaged during the
  accident and, according to the vehicle's logs, the driver's hands were not on
  the steering wheel at the time of the accident.

* Weeks later, [the driver's wife took to TV to discuss the
  crash](http://abcnews.go.com/US/wife-tesla-crash-victim-speaks-tragedy-happen-family/story?id=54392855),
  saying that her husband had always been "a really careful driver".

This interview caused a flurry of activity:

* Tesla released a response[^statement] saying that

> [The driver] was well aware that Autopilot was not perfect and, specifically,
> he told them it was not reliable in that exact location, yet he nonetheless
> engaged autopilot at that location, the crash happened on a clear day with
> several hundred feet of visibility ahead, which means that the only way for
> this accident to have occurred is if Mr. Huang was not paying attention to the
> road, despite the car providing multiple warnings to do so.

They also noted that Autopilot could not avoid all accidents. Tesla was then [removed from the NTSB
investigation](https://www.bloomberg.com/news/articles/2018-04-12/tesla-withdraws-from-ntsb-crash-probe-over-autopilot-data-flap).

* The family's lawyer released a statement as well, stating that

> [The car] took [the Driver] out of the lane that he was driving in, then it
> failed to brake, then it drove him into this fixed concrete barrier

At the same time, Tesla drivers around the country were able to reproduce
autopilot actions similar to the ones that caused the accident, [at other
interchanges](https://www.youtube.com/watch?v=6QCF8tVqM3I), and [at the original
crash site](https://www.youtube.com/watch?v=VVJSjeHDvfY). Many noted
[that this behavior was new, and that a recent over the air update changed the
way autopilot reacted in similar
cirucmstances.](https://www.reddit.com/r/teslamotors/comments/8a0jfh/autopilot_barrier_lust_201812/)

## Our Perspective

Tesla is unique among companies taking on the challenge of autonomous vehicles
in that it [doens't use
LIDAR](https://www.tesla.com/blog/all-tesla-cars-being-produced-now-have-full-self-driving-hardware)
in its technology. Magnifying this, the car that crashed appears to
predate Tesla's fully self driving hardware release and so has a limited sensor
suite; it appears to have relied almost entirely on a camera for lane finding and car
following.

That's similar to the adaptive cruise control that many other car manufacturers
offer. Tesla, however, markets Autopilot as something more advanced, 

<center>
<blockquote class="twitter-tweet" data-lang="en"><p lang="en"
dir="ltr">&quot;Tesla is extremely clear that Autopilot requires the driver to
be alert and have hands on the wheel.&quot; Tesla&#39;s website features a
person sitting in the driver&#39;s seat without their hands on the wheel: <a
href="https://t.co/38dsPzbPH3">pic.twitter.com/38dsPzbPH3</a></p>&mdash; Patrick
Traughber (@ptraughber) <a
href="https://twitter.com/ptraughber/status/984263154954743808?ref_src=twsrc%5Etfw">April
12, 2018</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
</center>

Tesla's statement about the clear weather and the driver's concern about the
location also included the following

> The fundamental premise of both moral and legal liability is a broken promise,
> and there was none here. Tesla is extremely clear that Autopilot requires the
> driver to be alert and have hands on the wheel.

Was there an explicit promise? Maybe not. But the hype around Tesla's autonomous
capabilities, led in no small part by the company's CEO Elon Musk, does imply
that you should trust the system. Musk originally said that Tesla would have
level 4 autonomy[^l4] [by the beginning of
2018](https://electrek.co/2017/12/08/elon-musk-tesla-self-driving-timeline/),
but now says that it's still a ways off. 

People, for whatever reason, are [all too
trusting](https://www.forbes.com/sites/kalevleetaru/2016/04/30/why-do-we-trust-gps-more-than-we-trust-ourselves/#656566b82c42)
of autonomous systems. In the age of ever advancing AI, there's a responsibility for
experts and designers to make sure that users understand the limits of the
systems they are marketing. This is especially true when, as is the case with
Tesla's vehicles, those exact capabilities may change over time.

In User Experience design, there's a term, "friction", for things which require
the user to engage or think. Often, you want an interface to be "frictionless",
allowing users to do things without really thinking, as if by instinct. But
sometimes you need friction to force users to engage with the system. For
example, when confirming an irreversible action.

Tesla's autopilot could use some more friction; currently its too easy to
disengage as a driver, and that's dangerous.

## TLDR

Autopilot worked as one would expect a [level 2 self driving car to
work](https://www.techrepublic.com/article/autonomous-driving-levels-0-to-5-understanding-the-differences/).
However (given current information) this gave the driver a false sense of
security. Tesla may have a responsibility to, ironically, make its users trust
its product less.

*Josh works at Google, whose sibling company, Waymo, is a competitor to Tesla in
the autonomous vehicle space, but the opinions expressed here are his own.*

[^statement]: Tesla doesn't appear to have made an official press release with their statement, but it's reproduced in full at the end of [this](http://abc7.com/automotive/tesla-issues-strongest-statement-yet-blaming-driver-for-deadly-crash/3332186/) article.
[^l4]: "Level 4" autonomy is autonomy where the vehicle can drive every part of the trip, from driveway to driveway, without human intervention. It should be capable of doing this in common environments and conditions (whereas Level 5 autonomy extends the definiton to more extreme environments and conditions).
