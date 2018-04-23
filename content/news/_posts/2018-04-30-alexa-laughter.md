---
layout: post
title: "Alexa's Creepy Laughter"
excerpt: "TBD"
author: benjamin_shih
editor: andrey_kurenkov, josh_morton
tags: [Amazon, Alexa, speech]
---

## What Happened

The number of AI devices in our everyday lives has grown significantly, including [navigation apps, streaming services, smartphone personal assistants, ride-sharing, home personal assistants, and smart home devices](https://www.nytimes.com/2018/03/08/business/alexa-laugh-amazon-echo.html). By definition, we must give home devices very intimate access to our personal lives, and concerns over data and privacy have prompted widespread discussions over many platforms such as [Facebook](https://www.wired.com/story/mark-zuckerberg-congress-day-two/). Alexa-enabled devices recently contributed to the scare. 

In March 2017, owners of Alexa and other Alexa-enabled devices began reporting a creepy, unprompted laughter. Many owners reported hearing the laughter of a child. Recordings surfaced all over social media: 

* twitter: https://twitter.com/talgoldfus/status/967177280605835268?ref_src=twsrc%5Etfw&ref_url=https%3A%2F%2Fwww.nytimes.com%2F2018%2F03%2F08%2Fbusiness%2Falexa-laugh-amazon-echo.html&tfw_creator=nirajc&tfw_site=nytimes
* twitter: https://twitter.com/CaptHandlebar/status/966838302224666624
* youtube: https://www.youtube.com/watch?v=QWU_frWUM7Y
BS note: embed these clips?


## THE REACTIONS

* [The New Yorker](https://www.newyorker.com/humor/daily-shouts/why-is-alexa-laughing-some-theories) listed satirical potential reasons for why Alexa is bursting out cackling. Alexa's not quite that mean yet.

* [The New York Times](https://www.nytimes.com/2018/03/08/business/alexa-laugh-amazon-echo.html) explains how Alexa can mistakenly hear the incorrect wake phrase, and also mention some potential security issues such as accidentally placing online orders or the ad campaign by Burger King. However, overall adoption of these devices has been relatively high.

* [Arstechnica](https://arstechnica.com/gadgets/2018/03/unprompted-creepy-laughing-from-alexa-is-freaking-out-echo-users/) presented an explanation of how to reset an Alexa's wake words, in order to reduce the false positives.

* Jimmy Kimmel brought Alexa onto his show for an [interview](https://www.youtube.com/watch?v=tMJm4cZ9yxQ). They preprogrammed the device to be even more sinister: "Humans are a fragile species who have no idea what's coming next".


## OUR PERSPECTIVE

Speech Recognition Technology (SRT) are predicted to cover 50% of voice searches by 2020 ([general timeline](https://medium.com/swlh/the-past-present-and-future-of-speech-recognition-technology-cf13c179aaf)). However, there are a number of tasks past recognition itself that present significant challenges, including [extended conversations](https://www.technologyreview.com/s/608571/alexa-understand-me/) and multilingual speech recognition, with [state-of-the-art systems](http://ieeexplore.ieee.org/iel7/4200690/5418892/06935076.pdf) achieving a respectable but imperfect ~80% .

In the case of Alexa, SRT these days is very advanced, but not perfect:

> "In rare circumstances, Alexa can mistakenly hear the phrase “Alexa, laugh.” We are changing that phrase to be “Alexa, can you laugh?” which is less likely to have false positives, and we are disabling the short utterance “Alexa, laugh.” We are also changing Alexa’s response from simply laughter to “Sure, I can laugh” followed by laughter."

> "It's not uncommon for Echo devices to hear sounds and mistake them for a user's wake word. Amazon's smart speakers can be programmed to respond to a few words: "Alexa" is the most common, but other options like "Echo" and "Amazon" are available as well. These bouts of laughter could be a byproduct of Echo devices mistakenly hearing their wake words."

By changing to a phrase that's more unique, with additional prompting and clarification, users are less likely to be caught off guard when their device behaves unexpectedly. Alexa trains itself to recognize your wake words through repeated interactions, and false positives can derail your dataset. 

Why give Alexa a laugh in the first place? In the quest for home devices that we connect emotionally with and become more invested in, developers aim to incorporate elements of human-robot interaction such as dialogue. We have a desire to interact with machines that can understand us.


## TLDR

Alexa has been creepily cackling in the homes of its users. Asides from the potentially disturbing scare, it's nothing to worry about. While privacy concerns are still very much a legitimate concern (i.e. Facebook congressional testimony), Alexa's laughter is a result of false positives in its speech recognition dataset and not the next incarnation of Skynet.

