---
layout: post
title: "A Perspective on the Recent Tesla Autopilot Crash"
excerpt: "AI gone haywire, or something else?"
author: joshua_morton
editor: andrey_kurenkov
tags: [tesla,autonomy,ethics,BigBiz]
---

## What Happened

On March 23, 2018, a Tesla Model X crashed into a median on Highway 101 in
Mountain View California, killing its occupant. Like a similar crash in May 2016
the vehicle’s “Autopilot” was enabled at the time of the crash. Soon after the
NTSB and Tesla opened an investigation into the cause of the accident. This
investigation is still ongoing.

Current theory is that the autopilot incorrectly followed road markings as a
lane split in an left-lane exit/interchange.

## The Reactions

Tesla initially [released a
statement](https://www.tesla.com/blog/what-we-know-about-last-weeks-accident)
outlining a few quick points about the accident, noting that the crash was
likely made more severe due to the lack of a crash attenuator, a safety device
built into the highway.

A few days later, Tesla released a followup
[statement](https://www.tesla.com/blog/update-last-week%E2%80%99s-accident) that
contained a few important details: autopilot was engaged during the accident
and, according to the vehicle's logs, the driver's hands were not on the
steering wheel at the time of the accident.

A few weeks later [the dead driver's wife took to TV to discuss the
crash](http://abcnews.go.com/US/wife-tesla-crash-victim-speaks-tragedy-happen-family/story?id=54392855),
saying that her husband had always been "a really careful driver".

This interview caused a flurry of activity:

Tesla released statements saying that 

> [The driver] was well aware that autopilot was not perfect and, specifically,
> he told them it was not reliable in that exact location, yet he nonetheless
> engaged autopilot at that location, the crash happened on a clear day with
> several hundred feet of visibility ahead, which means that the only way for
> this accident to have occurred is if Mr. Huang was not paying attention to the
> road, despite the car providing multiple warnings to do so.

And also noted that Autopilot could not avoid all accidents. This statement
appears to have led to Tesla being r[emoved from the NTSB
investigation](https://www.bloomberg.com/news/articles/2018-04-12/tesla-withdraws-from-ntsb-crash-probe-over-autopilot-data-flap).

The family's lawyer released a statement as well, stating that

> [The car] took [the Driver] out of the lane that he was driving in, then it
> failed to break, then it drove him into this fixed concrete barrier

At the same time, Tesla drivers around the country were able to reproduce
autopilot actions similar to the ones that caused the accident, [at other
interchanges](https://www.youtube.com/watch?v=6QCF8tVqM3I), and [at the original
crash site](https://www.youtube.com/watch?v=VVJSjeHDvfY). Among many reports was
th idea that [this was a recent change, and that a recent over the air update
changed autopilot behavior in this
situation](https://www.reddit.com/r/teslamotors/comments/8a0jfh/autopilot_barrier_lust_201812/)

## Our Perspective

Tesla is unique among companies taking on the challenge of autonomous vehicles
in that it [doens't use
LIDAR](https://www.tesla.com/blog/all-tesla-cars-being-produced-now-have-full-self-driving-hardware)
in its approach to autonomy. Magnifying this, car that crashed appears to
predate Tesla's fully self driving hardware release, it has a limited sensor
suite and appears to rely almost entirely on a camera for lane finding and car
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
capabilities, led in no small part by Musk, does imply that you should trust the
system. Musk originally said that [Tesla would have level 4 autonomy by the
beginning of
2018](https://electrek.co/2017/12/08/elon-musk-tesla-self-driving-timeline/),
but now says that its still a ways off, and Tesla also missed the deadline for a
coast-to-coast autonomous Tesla trip.

People, for whatever reason, are [all too
trusting](https://www.forbes.com/sites/kalevleetaru/2016/04/30/why-do-we-trust-gps-more-than-we-trust-ourselves/#656566b82c42)
of autonomous systems. In the age of AI and ML, there's a responsibility for
experts to make sure that users understand the limits of the systems they are
using. This is especially true when, as is the case with Tesla's vehicles, those
exact capabilities may change over time.

In User Experience design, there's a term, "friction", for things which require
the user to engage or think. Often, you want an interface to be "frictionless",
allowing users to do thinkgs without really thinking, as if by instinct. But
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
