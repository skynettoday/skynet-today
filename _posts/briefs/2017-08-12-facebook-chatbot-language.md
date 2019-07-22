---
layout: post
title: "The Crazy Coverage of Facebook's Unremarkable 'AI Invented Language'"
excerpt: "Sometimes the narratives media conjures up just serve to make real life seem boring"
author: andrey_kurenkov
tags: [Facebook,BigBiz,chatbot,NLP,panic]
categories: [briefs]
redirect_from: /content/news/facebook-chatbot-language/
permalink: /briefs/facebook-chatbot-language/
---
A truly astounding exemplar of how coverage of AI goes horribly wrong.

## What Happened
The paper that originated all this terror has the fun seemingly un-scary title ["Deal or No Deal? End-to-End Learning for Negotiation Dialogues"](https://arxiv.org/abs/1706.05125) and was done by researchers from Facebook and the Georgia Institute of Technology. As the title implies, the problem being addressed is the creation of AI models for human-like negotation through natural language. To tackle this, the researchers first collected a brand new dataset of 5808 negotations between plain ol' humans with the data-collection powerhorse Mechanical Turk. 

These negotiations involve two people agreeing on a split of some set of items, which have different values for each negotiator. This is a nicer problem to tackle than generic chatbot conversation, because there is a straighforward evaluation metric (how much value each negotiator manages to secure) and the language needed is less broad than generic speech. The final approach used a combination of supervised learning (just emulating the dialogues from the dataset) and reinforcement learning (learning to generate speech based on maximizing negotiation outcomes). This is a pretty hefty paper, and all this drama came about because of one tiny section:

> During reinforcement learning, an agent A attempts to improve its parameters from conversations with another agent B. While the other agent B could be a human, in our experiments we used our fixed supervised model that was trained to imitate humans. The second model is fixed as we found that updating the parameters of both agents **led to divergence from human language**.

To be clear, this is not all that surprising, since the optimization criterion here is much more specific that developing a robust generic language to communicate about the world. And even if the criterion were that broad, there is no reason for the optimization to converge upon English without some supervised loss to guide it there. I am no professor, but even with my meager knowledge of AI I am fairly confident in saying this is a truly, utterly unremarkble outcome.  

## The Reactions
It started with [a tweet](https://twitter.com/danielgross/status/875193634148073478):

<blockquote class="twitter-tweet" data-lang="en" align="center"><p lang="en" dir="ltr">When you let AI negotiate with itself, it realizes there are better options than English. A sign of what&#39;s to come.<a href="https://t.co/Jtl2nTXjwl">https://t.co/Jtl2nTXjwl</a> <a href="https://t.co/MMaWVjJDlj">pic.twitter.com/MMaWVjJDlj</a></p>&mdash; Daniel Gross (@danielgross) <a href="https://twitter.com/danielgross/status/875193634148073478">June 15, 2017</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

And then, things developed swiftly:
* June 14th: [The blog post](https://code.facebook.com/posts/1686672014972296/deal-or-no-deal-training-ai-bots-to-negotiate) concerning the research and the tweet emerge.
* June 15th: The Atlantic's ["An Artificial Intelligence Developed Its Own Non-Human Language"](https://www.theatlantic.com/technology/archive/2017/06/artificial-intelligence-develops-its-own-non-human-language/530436/) comes out, seemingly inspired by the tweet. The article does not delve deeply into the research or what non-human language the AI developed. It does characterize this as "mind-boggling" and deserving of "wonder and awe".
* June 19th: Someone at Facebook decided it's a good idea to provide examples of the sort of non-human language their AI invents. It came out in a very short piece from The Next Web, 
["Facebook’s AI accidentally created its own language"](https://thenextweb.com/artificial-intelligence/2017/06/19/facebooks-ai-accidentally-created-its-own-language/#.tnw_hJk6Xc8i). The whole invented language is exemplfied by this brief exchange:
> Bob: i can i i everything else . . . . . . . . . . . . . .  
Alice: balls have zero to me to me to me to me to me to me to me to me to  
Bob: you i everything else . . . . . . . . . . . . . .  
Alice: balls have a ball to me to me to me to me to me to me to me  
Bob: i i can i i i everything else . . . . . . . . . . . . . .  
Alice: balls have a ball to me to me to me to me to me to me to me  
Bob: i . . . . . . . . . . . . . . . . . . .  
Alice: balls have zero to me to me to me to me to me to me to me to me to  
Bob: you i i i i i everything else . . . . . . . . . . . . . .  
Alice: balls have 0 to me to me to me to me to me to me to me to me to  
Bob: you i i i everything else . . . . . . . . . . . . . .  
Alice: balls have zero to me to me to me to me to me to me to me to me to
* June 20th: The Atlantic, where media coverage of this whole "AI-invented non-human language" deal originated, noticed this juicy bit of info and followed up on their first article with ["What an AI's Non-Human Language Actually Looks Like"](https://www.theatlantic.com/technology/archive/2017/06/what-an-ais-non-human-language-actually-looks-like/530934/). Though it continues with the perspective that "Machines making up their own language is really cool, sure, but isn’t it actually terrifying?", this time around there is a bit of skepticism as to whether the nonsense the bots learn to output should even be called 'language'.
* July 14th: There is a lull in coverage, until July 14th when Fast Co.Design comes out with a long, in-depth piece - ["AI Is Inventing Languages Humans Can’t Understand. Should We Stop It?"](https://www.fastcodesign.com/90132632/ai-is-inventing-its-own-perfect-languages-should-we-let-it). 
* July 15th: The Register also caught wind of this research, but refreshingly covered it from a more interesting angle with ["Facebook tried teaching bots art of negotiation – so the AI learned to lie"](https://www.theregister.co.uk/2017/06/15/facebook_to_teach_chatbots_negotiation/?mt=1505978863070).
* July 21st: The Fast Co.Design piece evidently inspired more coverage of this already month-old paper, such as ["Researchers shut down AI that invented its own language"](http://www.digitaljournal.com/tech-and-science/technology/a-step-closer-to-skynet-ai-invents-a-language-humans-can-t-read/article/498142) from Digital Life Journal. There is some alarmism emerging, such as "There's not yet enough evidence to determine whether they present a threat that could enable machines to overrule their operators.", though the piece is still fairly reasonable and realistic.
* July 29th: The story keeps on gaining steam and losing accuracy, with stories such as ["‘TERMINATOR’ COME TO LIFE? – FACEBOOK SHUTS DOWN ARTIFICIAL INTELLIGENCE AFTER IT DEVELOPED ITS OWN LANGUAGE"](https://www.inquisitr.com/4398004/terminator-come-to-life-facebook-has-to-shut-down-artificial-intelligence-after-it-developed-its-own-language/) 
* July 30th: Inevitabely, the coverage converges to comparing this research to Skynet with ["Facebook AI Invents Language That Humans Can't Understand: System Shut Down Before It Evolves Into Skynet"](http://www.techtimes.com/articles/212124/20170730/facebook-ai-invents-language-that-humans-cant-understand-system-shut-down-before-it-evolves-into-skynet.html). Also inevitably, the coverage now portrays this as a sign of AI being an existential threat to humanity with "AI systems can do a variety of things better than humans and, if not kept in check, could grow into something that can replace us entirely". The "scary AI bot" coverage is now in full swing, with articles such as ["Facebook engineers panic, pull plug on AI after bots develop their own language"](http://bgr.com/2017/07/31/facebook-ai-shutdown-language/) , ["Facebook AI Creates Its Own Language In Creepy Preview Of Our Potential Future"](https://www.forbes.com/sites/tonybradley/2017/07/31/facebook-ai-creates-its-own-language-in-creepy-preview-of-our-potential-future/#5f891142292c) , ["Facebook shuts down controversial chatbot experiment after AIs develop their own language to talk to each other"](http://www.dailymail.co.uk/sciencetech/article-4747914/Facebook-shuts-chatbots-make-language.html), and ["Creepy Facebook bots talked to each other in a secret language"](http://nypost.com/2017/08/01/creepy-facebook-bots-talked-to-each-other-in-a-secret-language/) emerging over the next few days. 
* August 1st: By now, things have gotten enough out of control that numerous piece debunking the hype emerge, such as ["No, Facebook Did Not Panic and Shut Down an AI Program That Was Getting Dangerously Smart"](https://gizmodo.com/no-facebook-did-not-panic-and-shut-down-an-ai-program-1797414922), ["Facebook pulls plug on language-inventing chatbots? THE TRUTH"](https://www.theregister.co.uk/2017/08/01/facebook_chatbots_did_not_invent_new_language/), and ["Facebook AI researcher slams 'irresponsible' reports about smart bot experiment"](https://www.cnbc.com/2017/08/01/facebook-ai-experiment-did-not-end-because-bots-invented-own-language.html).

## Our Perspective
As the multiple hype-debunking articles just above imply, this small aspect of the research is really not a big deal. The only big deal about all this is how crazy coverage of this story got, given how mundane the AI development was. After all, few media stories have ever gotten AI researchers this heated:
<blockquote class="twitter-tweet" data-lang="en" align="center"><p lang="en" dir="ltr">What f***ing trashy excuse of a journalist writes this sh***y sensationalist s***? DO YOU GUYS NOT HAVE EDITORS??<a href="https://t.co/fYXubWIRQN">https://t.co/fYXubWIRQN</a></p>&mdash; Edward Grefenstette (@egrefen) <a href="https://twitter.com/egrefen/status/891362804074033152">July 29, 2017</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

In fact, the coverage has gotten so out of hand that the researcher responsible for it was driven to write a long post addressing the nonsense:
<iframe src="https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2Fdhruv.batra.dbatra%2Fposts%2F1943791229195215&width=500" align="center" width="500" height="380" style="border:none;overflow:hidden" scrolling="no" frameborder="0" allowTransparency="true"></iframe>

And that right there is all that needs to be said.

## TLDR
AI models optimizing to use nonsensical communication is not surprising nor impressive, which makes the extremely hyperbolic media coverage of this story downright impressive.
