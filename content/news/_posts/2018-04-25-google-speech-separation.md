---
title: "Evil Software Du Jour: Google's Speech Separation"
excerpt: "New tech from Google Research uses AI techniques. It does not portend Orwellian society."
author: charlie_kilpatrick
tags: [Google,speech,vision]
---

*New technology from Google Research is neat, but hyperbolic privacy concerns pull focus.*

## What Happened
Google created a new means of programatically discerning voices on a face-by-face basis using AI techniques. Their approach is novel in that it combines visual and auditory signals to produce the transcript of a conversation;
they offer a comparison to the [cocktail party effect](https://en.wikipedia.org/wiki/Cocktail_party_effect) -- the human ability to discern who is speaking at a loud party despite there being many sound sources at any given time. They also provided a video demonstrating their technique: 

<iframe width="560" height="315" src="https://www.youtube.com/embed/NzZDnRni-8A" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>

The authors offer closed captioning as an example of the applicability of the tech and close by stating that they are "exploring opportunities for incorporating it into various Google products."

## The Reactions

*Ars Technica* quickly construed Google's new technique as a [as a Big Brother-esque surveillance tool:](https://arstechnica.com/gadgets/2018/04/google-works-out-a-fascinating-slightly-scary-way-for-ai-to-isolate-voices-in-a-crowd/) 

>The privacy ramifications of this kind of tech seem just as obvious as the potential use cases. Google's voice isolation is far from bulletproof in the examples above, but with some more fine-tuning, it could make for a powerful eavesdropping and surveillance tool in the wrong hands.

Obviously, *Ars* isn't the only publication guilty of fearmongering:

* ["Cool, but scary: New Google AI tech can isolate a single voice in a crowd"](https://www.androidpolice.com/2018/04/12/cool-scary-new-google-ai-tech-can-isolate-single-voice-crowd/)
* ["How Google Knows Who’s Talking, Even Among A Noisy Crowd"](http://www.techtimes.com/articles/225069/20180413/how-google-knows-who-s-talking-even-among-a-noisy-crowd.htm)
* ["Google Created An Audio-Visual AI That Can Pick Out Your Voice in A Crowd"](https://beebom.com/google-audio-visual-ai-voice-crowd/)

Each article closes with a paragraph warning of privacy issues, giving descriptions of the privacy implications ranging from "spooky" to "honestly pretty serious" and offering hypothetical examples of third-party spying
that read like a passage from *Nineteen Eighty-Four*.

## Our Perspective

The privacy-minded closing paragraph of each of the articles in question reads as though the writer wants to hedge their report with a discretionary footnote: "This stuff is cool, but it might also be bad!"
To be fair, it makes some sense that publications would want their writers to exercise such caution -- it's an attractive way to build trust with readers, especially in light of [recent events](http://time.com/5234740/facebook-data-misused-cambridge-analytica/).
Unfortunately, these publications' alarmist takes on new technologies undermine public trust in AI and tech research in general.

There are several reasons to temper this alarm.

Foremost, this technology doesn't open any new doors for people who want to surveil others.
Automatic speech recognition has existed [since the 1960's](http://www.ece.ucsb.edu/Faculty/Rabiner/ece259/Reprints/354_LALI-ASRHistory-final-10-8.pdf) using [Hidden Markov Models](http://ethw.org/First-Hand:The_Hidden_Markov_Model) for reinforcement learning.
Since the 21st century, several approaches to speech separation have been proposed and implemented with varying degrees of success ([2004](http://c4dm.eecs.qmul.ac.uk/papers/2004/Mitianoudis04-phdthesis.pdf), [2007](http://www.kecl.ntt.co.jp/icl/signal/sawada/mypaper/icassp2007Tutorial11.pdf), [2011](https://www.ruhr-uni-bochum.de/ika/forschung/forschungsbereich_kolossa/Daten/Buchkapitel_ICA.pdf), [2014](https://arxiv.org/pdf/1408.0193)).
And in 2016, researchers at The University of Oxford achieved ["sentence-level" lipreading](https://arxiv.org/pdf/1611.01599.pdf) with a deep learning approach.

For humans, speech recognition is usually easy while lipreading is very difficult.
What's important to note, however, is that the kind of lipreading that usually comes to mind isn't exactly what the new technique is doing.
The authors of [the paper](https://arxiv.org/pdf/1804.03619.pdf) suggest in the first sentence of their introduction that this is very much an effort to emulate a skill that humans already have:
>Humans are remarkably capable of focusing their auditory attention on a single sound source within a noisy environment, while deemphasizing (“muting”) all other voices and sounds. 

Crucially, the authors then suggest that humans are *considerably better* at recognizing speech when they can see the speaker's face.
The bottom line emerges: this new technology is an effort to make machines able to do something humans can do by recreating the conditions that humans require to do it the most effectively.

## TLDR

Obviously, there are ramifications when machines are made capable of doing something only humans could previously do: machines can potentially do it orders of magnitude faster, more precisely, more effectively, etc.
Though breaches of privacy are always a concern, the particular new algorithms and what they actually enable need to be kept in mind. But if this technology ever results in a breach of your privacy, you'll have plenty of other things to be angry about, such as the very specific situation in which you were talking at the same time as several other people in a voice loud enough to be picked up by a mic while a video with unobstructed view of your face is recorded.