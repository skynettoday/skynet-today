---
title: "Please Stop Saying 'An AI'"
author: [andrey_kurenkov]
categories: [editorials]
tags: [overview]
excerpt: "Popular usage of the term ‘Artificial Intelligence’ adds to misunderstanding of AI as it exists today."
image:
  feature: assets/img/editorials/2020-12-01-ai-definition/main.png
  credit: Google
sidebartoc: true
highlight: true 
---

## The Options
Definitions of the term ‘Artificial Intelligence’ tend to fit one of the following categories:

1. ‘field of research’ definitions, e.g.: “a branch of computer science dealing with the simulation of intelligent behavior in computers” ([Merriam-Webster](https://www.merriam-webster.com/dictionary/artificial%20intelligence)) , “the theory and development of computer systems able to perform tasks that normally require human intelligence” (Oxford)
2. ‘machine intelligence’ definitions, e.g.: “the capability of a machine to imitate intelligent human behavior “([Merriam-Webster](https://www.merriam-webster.com/dictionary/artificial%20intelligence)) , “intelligence demonstrated by machines, unlike the natural intelligence displayed by humans and animals.” ([Wikipedia](https://en.wikipedia.org/wiki/Artificial_intelligence)) , “the ability of a digital computer or computer-controlled robot to perform tasks commonly associated with intelligent beings.” ([Encyclopedia Brittanica](https://www.britannica.com/technology/artificial-intelligence))
3. ‘intelligent entity’ definitions, e.g.: “a computer, robot, or other programmed mechanical device having \[the\] humanlike capacity \[to perform operations and tasks analogous to learning and decision making in humans, as speech recognition or question answering\]”. ([Dictionary.com](https://www.dictionary.com/browse/artificial-intelligence))

While all of these options are similar in that they deal with ‘intelligent behavior’ in computers, they are also quite different. The first refers to a research discipline, while the second and third describe what that research discipline seeks to create. The ways in which the term ‘AI’ can be used depend on which of these definitions you consider valid. For instance, news articles often have titles to the effect of “Google’s new AI learned X” or “A new AI can do Y,” such as:

- [“An Artificial Intelligence Developed Its Own Non-Human Language”](https://www.theatlantic.com/technology/archive/2017/06/artificial-intelligence-develops-its-own-non-human-language/530436/)
- [“AI can now design cities, but should we let it?”](https://www.fastcompany.com/90455358/ai-can-now-design-cities-should-we-let-it)
- [“For The First Time Ever, A Drug Developed By AI Will Be Tested In Human Trials”](https://www.forbes.com/sites/danadovey/2020/02/11/first-time-ever-artificial-intelligence-develops-drug-candidate/)
- [“Google AI creates its own ‘child’ AI that’s more advanced than systems built by humans”](https://www.sciencealert.com/google-s-ai-built-it-s-own-ai-that-outperforms-any-made-by-humans)

But, such usage (“An AI Developed”, “AI can now”, etc.) is only valid with that third 'intelligent entity' definition. If the first ‘field of research’ definition is chosen instead, these titles would have to be rewritten as “Google’s new AI algorithm learned X” or “A new AI system can do Y.” In this piece, I’ll make the case that this definition and form of usage (which I will adopt for the rest of this piece) is superior to the alternatives, and should be adopted in most cases.

## Why Should We Care
It may seem pedantic to say one of these definitions is better than any of the others, and tempting to just say all of them are fine. However, I argue that the ‘field of research’ definition of AI is better than the alternatives, primarily because of the [common misunderstanding](https://www.aimyths.org/ai-has-agency) that AI programs today are independent agents with some amount of ‘free will’. In fact, what AI researchers and engineers build today are just computer programs, which are capable of emulating some aspects of human intelligence but are otherwise (for the most part) no more independent than the apps on our smartphones. Nevertheless, AI researchers recently ranked the idea that the AI algorithms they create have some human-like independence as the most common and problematic myth about AI; it was “number one by a long shot” [according to a survey](https://www.skynettoday.com/podcast/top-ai-myths) asking which myths about AI are most common.

I believe part of why this myth is so predominant has to do with thinking of AI in terms of the ‘intelligent entity’ definition type and using the term accordingly by saying statements such as “A new AI can do Y”. Expanding that statement results in “A new Artificial Intelligence can do Y,” and the notion that the sentence refers to ‘An Intelligence’ inevitably implies agency similar to those of animals and humans. AI researcher Julian Togelius addresses this notion well in his blog post [“Some advice for journalists writing about artificial intelligence”](http://togelius.blogspot.com/2017/07/some-advice-for-journalists-writing.html):

> **Keep in mind**: There is no such thing as “an artificial intelligence”. AI is a collection of methods and ideas for building software that can do some of the things that humans can do with their brains. Researchers and developers develop new AI methods (and use existing AI methods) to build software (and sometimes also hardware) that can do something impressive, such as playing a game or drawing pictures of cats.

AI researcher Zachary Lipton made this point more bluntly:

<figure>
<blockquote class="twitter-tweet tw-align-center"><p lang="en"
dir="ltr">Dear world (CC <a
href="https://twitter.com/businessinsider?ref_src=twsrc%5Etfw">@businessinsider</a>,
<a
href="https://twitter.com/Hamilbug?ref_src=twsrc%5Etfw">@Hamilbug</a>):
stop saying "an AI". AI's an aspirational term, not a
thing you build. What Amazon actually built is a "machine learning
system", or even more plainly "predictive model". Using
"an AI" grabs clicks but misleads <a
href="https://t.co/0kdTLBsrHJ">https://t.co/0kdTLBsrHJ</a></p>—
Zachary Lipton (@zacharylipton) <a
href="https://twitter.com/zacharylipton/status/1050221929477664768?ref_src=twsrc%5Etfw">October
11, 2018</a></blockquote> <script async
src="https://platform.twitter.com/widgets.js"
charset="utf-8"></script>
</figure>

As someone who has tried to use my knowledge as an AI researcher to address popular misconceptions about AI, I have observed and continue to observe the usage of “An AI” often, and think it has the negative side effect of feeding misunderstanding of what AI is today. While it may be tempting to once again say this is being pedantic and that it’s fine to have a more ‘pop culture’ view of AI, with AI becoming increasingly embedded in our society it is more important than ever that all of us understand it. Such understanding is crucial so that we can collectively correctly focus on the most pressing issues with respect to AI (such as bias, automation, its use for surveillance, its safety) and not the issues that the agency myth implies (its potential to go rogue a la Skynet in the near term).

Therefore, given the existence of the ‘agency’ myth with respect to AI and the importance of correctly understanding what AI is actually like today, I would argue the first ‘field of research’ definition of the term ‘AI’ is better than the alternatives. As I’ll show next, this is (unsurprisingly) typically how AI researchers themselves use the term.

## How Researchers Define AI

[John McCarthy](https://en.wikipedia.org/wiki/John_McCarthy_(computer_scientist)), one of the founders of the field of AI, defined AI as follows:

> “It is the science and engineering of making intelligent machines, especially intelligent computer programs.”

Professor [Christopher Manning](https://nlp.stanford.edu/manning/)[ ](https://hai.stanford.edu/sites/default/files/2020-09/AI-Definitions-HAI.pdf) [recently cited](https://hai.stanford.edu/sites/default/files/2020-09/AI-Definitions-HAI.pdf) this as the definition of ‘Artificial Intelligence’ in his summary of definitions of terms related to AI. Similarly, in “Artificial Intelligence: A Modern Approach”, Stuart Russell and Peter Norvig defined AI as:

> “the designing and building of intelligent agents that receive percepts from the environment and take actions that affect that environment.”

To cite just one more example, in “The Quest for Artificial Intelligence: A History of Ideas and Achievements” [Nils J. Nilsson](https://en.wikipedia.org/wiki/Nils_John_Nilsson) defines AI as follows:

> “\[the\] activity devoted to making machines intelligent”

There are of course many other definitions, but they tend to share the quality of considering AI a research or engineering discipline rather than a term that can be used to refer to singular algorithms or systems.

I conducted an informal survey to check whether AI researchers generally agree with this form of definition, with the following results:

<figure>
<blockquote class="twitter-tweet tw-align-center"><p lang="en" dir="ltr">AI Researchers: how do you define the term &#39;Artificial Intelligence&#39;? <br><br>A: the science and engineering of making intelligent machines, especially intelligent computer programs<br><br>B: intelligence demonstrated by machines, unlike the natural intelligence of animals<br><br>C: Other</p>&mdash; Skynet Today (@skynet_today) <a href="https://twitter.com/skynet_today/status/1326239401912004611?ref_src=twsrc%5Etfw">November 10, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 
</figure>

While hardly a careful study of what most AI researchers feel, the result of this poll agrees with my personal observations as an AI researcher that most in the field seem to prefer the John McCarthy definition of AI to the alternatives. I point this out because I think it further lends credence to the idea that the ‘field of research’ definition that does not allow for “An AI” as a phrase is superior to the alternatives. Granted, no one has any right to impose a particular way of defining terms on others, but I still think using the term ‘AI’ the same way the people actually working on AI in the real world (as opposed to science fiction, where ‘An AI’ is appropriate) makes a lot of sense.

## TLDR 
AI researchers tend to define ‘Artificial Intelligence’ to mean something along the lines of “the science and engineering of making intelligent machines, especially intelligent computer programs” -- the ‘field of research’ definition. This is in contrast to definitions often used in popular media, which use ‘AI’ to refer to particular programs or systems with sentences -- the 'intelligent entity' definition. The latter usage of AI reinforces an already common myth that present day AI has some amount of human-like agency, when in fact this is not really the case. Therefore, I believe that the 'intelligent entity' type definition should be avoided in favor of the ‘field of research’ definition, and the term should be used accordingly.

