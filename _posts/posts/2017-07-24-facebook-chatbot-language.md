---
layout: post
title: "The Scary Story of How Facebook's Researchers Pressed Cntrl C"
excerpt: "Sometimes the narratives media conjures up just serve to make real life seem boring"
categories: [doom,news]
tags: [facebook,chatbot,nlp,doom]
comments: true
share: true
published: false
---
A truly astounding exemplar of how coverage of AI goes wrong...

## The Research
The paper that originated all this terror has the fun seemingly un-scary title ["Deal or No Deal? End-to-End Learning for Negotiation Dialogues"](https://arxiv.org/abs/1706.05125) and was done by researchers from Facebook and the Georgia Institute of Technology. As the title implies, the problem being addressed is the creation of AI models for human-like negotation through natural language. To tackle this, the researchers first collected a brand new dataset of 5808 negotations between plain ol' humans with the data-collection powerhorse Mechanical Turk. These negotiations involve two people agreeing on a split of some set of items, which have different values for each negotiator. This is a nicer problem to tackle than generic chatbot conversation, because there is a straighforward evaluation metric (how much value each negotiator manages to secure) and the language needed is less broad than generic speech. The final approach used a combination of supervised learning (just emulating the dialogues from the dataset) and reinforcement learning (learning to generate speech based on maximizing negotiation outcomes). This is a pretty hefty paper, and all this drama came about because of a pretty small 

> During reinforcement learning, an agent A attempts to improve its parameters from conversations with another agent B. While the other agent B could be a human, in our experiments we used our fixed supervised model that was trained to imitate humans. The second model is fixed as we found that updating the parameters of both agents **led to divergence from human language**.

## The Media
It started with [a tweet](https://twitter.com/danielgross/status/875193634148073478). 

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">When you let AI negotiate with itself, it realizes there are better options than English. A sign of what&#39;s to come.<a href="https://t.co/Jtl2nTXjwl">https://t.co/Jtl2nTXjwl</a> <a href="https://t.co/MMaWVjJDlj">pic.twitter.com/MMaWVjJDlj</a></p>&mdash; Daniel Gross (@danielgross) <a href="https://twitter.com/danielgross/status/875193634148073478">June 15, 2017</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

[The blog post](https://code.facebook.com/posts/1686672014972296/deal-or-no-deal-training-ai-bots-to-negotiate) concerning the research came out on June 14th, followed swiftly by the tweet, and on June 15th the Atlantic's ["An Artificial Intelligence Developed Its Own Non-Human Language"](https://www.theatlantic.com/technology/archive/2017/06/artificial-intelligence-develops-its-own-non-human-language/530436/). The article does not  
["Facebook’s AI accidentally created its own language"](https://thenextweb.com/artificial-intelligence/2017/06/19/facebooks-ai-accidentally-created-its-own-language/#.tnw_hJk6Xc8i) June 19
["Facebook’s AI accidentally created its own language"](http://www.businessinsider.com/facebook-chat-bots-created-their-own-language-2017-6) June 20

["AI Is Inventing Languages Humans Can’t Understand. Should We Stop It?"](https://www.fastcodesign.com/90132632/ai-is-inventing-its-own-perfect-languages-should-we-let-it) July 14
["Facebook put cork in chatbots that created a secret language"](https://www.cnet.com/news/what-happens-when-ai-bots-invent-their-own-language/)

["Facebook tried teaching bots art of negotiation – so the AI learned to lie"](https://www.theregister.co.uk/2017/06/15/facebook_to_teach_chatbots_negotiation/?mt=1505978863070) July 15

["Researchers shut down AI that invented its own language"](http://www.digitaljournal.com/tech-and-science/technology/a-step-closer-to-skynet-ai-invents-a-language-humans-can-t-read/article/498142) July 21sy
["‘TERMINATOR’ COME TO LIFE? – FACEBOOK SHUTS DOWN ARTIFICIAL INTELLIGENCE AFTER IT DEVELOPED ITS OWN LANGUAGE"](https://www.inquisitr.com/4398004/terminator-come-to-life-facebook-has-to-shut-down-artificial-intelligence-after-it-developed-its-own-language/) July 29
["Facebook AI Invents Language That Humans Can't Understand: System Shut Down Before It Evolves Into Skynet"](http://www.techtimes.com/articles/212124/20170730/facebook-ai-invents-language-that-humans-cant-understand-system-shut-down-before-it-evolves-into-skynet.html) July 30
["Facebook engineers panic, pull plug on AI after bots develop their own language"](http://bgr.com/2017/07/31/facebook-ai-shutdown-language/) July 31
["Facebook AI Creates Its Own Language In Creepy Preview Of Our Potential Future"](https://www.forbes.com/sites/tonybradley/2017/07/31/facebook-ai-creates-its-own-language-in-creepy-preview-of-our-potential-future/#5f891142292c) July 31
["Facebook shuts down controversial chatbot experiment after AIs develop their own language to talk to each other"](http://www.dailymail.co.uk/sciencetech/article-4747914/Facebook-shuts-chatbots-make-language.html) 31 July
["Creepy Facebook bots talked to each other in a secret language"](http://nypost.com/2017/08/01/creepy-facebook-bots-talked-to-each-other-in-a-secret-language/) Aug 1
## The Criticism
["Facebook pulls plug on language-inventing chatbots? THE TRUTH"](https://www.theregister.co.uk/2017/08/01/facebook_chatbots_did_not_invent_new_language/)
["Facebook AI researcher slams 'irresponsible' reports about smart bot experiment"](https://www.cnbc.com/2017/08/01/facebook-ai-experiment-did-not-end-because-bots-invented-own-language.html)
["No, Facebook’s Chatbots Will Not Take Over the World"](https://www.wired.com/story/facebooks-chatbots-will-not-take-over-the-world/)
["Post"](https://www.facebook.com/dhruv.batra.dbatra/posts/1943791229195215?pnref=story)
["Exasperation"](https://twitter.com/egrefen/status/891362804074033152)
## The Gistagent
