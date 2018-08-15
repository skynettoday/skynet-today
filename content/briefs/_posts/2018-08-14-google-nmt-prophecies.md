---
layout: post
image:
  feature: /content/briefs/images/google-nmt-prophecies/translations.png
  credit: Modified from Motherboard's Article
title: "Google Translate's \"Sinister Religious Prophecies\", Demystified"
excerpt: "Yet again, an unremarkable and well understood aspect of an AI system has been made out to be creepy and hard to explain"
author: julia_gong
editor: [andrey_kurenkov]
tags: [panic,translation,Google]
permalink: /briefs/google-nmt-prophecies
---

# What Happened

Google Translate has been known to output rather strange translations, such as that above, for quite some time. The topic has amassed a niche community on [Reddit](https://www.reddit.com/r/TranslateGate/), but the phenomenon was only recently pulled into the spotlight by MotherBoard’s “[Why Is Google Translate Spitting Out Sinister Religious Prophecies?](https://motherboard.vice.com/en_us/article/j5npeg/why-is-google-translate-spitting-out-sinister-religious-prophecies)”. The author observed that, when translating the word “dog” or the syllable “ag” repeated several times in succession from languages such as Somali, Maori, or Hawaiian into English, the translator declared sinister Biblical prophecies. The return of Christ, AI turning religious, or perhaps an internal prankster at Google--what could be responsible for all of this?

Experts agree that this is caused by the weaknesses of a technique that Google has been using to power translation software since 2016: neural machine translation, or NMT. NMT is based on “training” neural networks with large amounts of textual data to generate translations (you can find a more detailed explanation [here](https://www.skynettoday.com/editorials/state_of_nmt)). Compared to prior methods for software translation, this technique produces translations that sound more natural and human, but also have some quirks due to being data-driven. 

MotherBoard author Jon Christian interviewed experts Alexander Rush from Harvard and Sean Colbath at BBN Technologies, who conjectured that because of the nature of NMT, the “strange outputs are probably due to Google Translate’s algorithm looking for order in chaos”, or finding coherent translations that aren’t really there. Colbath further posited that “it’s possible that Google used religious texts like the Bible, which has been translated into many languages, to train its model in those languages, resulting in the religious content”. Both experts agree that this is a likely explanation because “the languages that generate the strangest results—Somali, Hawaiian and Maori—have smaller bodies of translated text than more widely spoken languages like English or Chinese”, the classic hallmark of a data deficiency. Many other researchers on Twitter concurred that this can safely be understood to be the reason for the strange translations, even if Google would not confirm that was the case.

<figure>
<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">I just mean to say that the phenomenon is well understood in LSTMs and other types of gated RNNs. Translation systems require parallel text corpora and the Bible is one of the most available sources of parallel corpora, especially for low-resource languages.</p>&mdash; Mark O. Riedl (@mark_riedl) <a href="https://twitter.com/mark_riedl/status/1020366905641787392?ref_src=twsrc%5Etfw">July 20, 2018</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
</figure>

Given how strange this quirk seems at first sight, the article received a good deal of views and reactions on popular social media sites. The constant discovery of new odd examples, continuous online discussion, and many other media outlets reporting on the same story naturally led to a lot of reactions.

# The Reactions
As with many news stories that have potential for sensational and apocalyptic virality, this story took off. Numerous news outlets broadcasted the conundrum as a complete mystery. Despite the rational explanations offered by the AI research community, including those offered in the original piece, many media bodies over-marketed the curiosity of the finding in exchange for flashy headlines.

In a now-deleted tweet, Editor-in-Chief of MotherBoard Jason Koebler shared the article and stated that “no one is sure why” Google Translate was behaving in this way, despite the bulk of the latter portion of the article presenting likely reasons for the phenomenon. Multiple AI researchers expressed the strong sentiment that, although it is technically true that no one can be “sure” of any explanation (since Google did not verify that they use the Bible in their NMT training), the title and promotion of the piece made it seem like far more of a spooky mystery than it really was. This misinformation is problematic given that experts could be virtually certain their explanations were correct.

Many media organizations soon also reported the story, and by and large focused on the spooky angle with headlines such as [Google Translate warns of apocalypse in bizarre 'end times' message](https://www.thesun.co.uk/tech/6842131/google-translate-doomsday-clock-end-times-antichrist-apocalypse-dog/), [Google Translate is generating ominous religious prophecies for some reason](https://mashable.com/2018/07/23/google-translate-glitch-ominous-religious-prophecies/#eVcCwNgyykqn), [Google Translate's AI Is Rendering Gibberish Into Spooky Religious Prophecies](http://fortune.com/2018/07/21/google-translate-religious-translations/), and [Google Translate Is Doing Something Incredibly Sinister And It Looks Like We're All Doomed](http://www.iflscience.com/technology/google-translate-is-doing-something-incredibly-sinister-and-it-looks-like-were-all-doomed/). In the words of the last news story on IFLScience, “The bad news: the world is ending. Sorry about that. The worse news: we had to find out from Google Translate.” The public soon also joined in further sensationalizing the story. A quick search for ‘Google Translate’ on Twitter yields many tweets showcasing (often humorous) examples of chance translations from other languages to English.

<figure>
<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Google Translate Conspiracy  THREAD 🤔 TUPAC <a href="https://t.co/4pgOQTOB44">pic.twitter.com/4pgOQTOB44</a></p>&mdash; angelic (@angelesangelic_) <a href="https://twitter.com/angelesangelic_/status/1025682939193962496?ref_src=twsrc%5Etfw">August 4, 2018</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
</figure>

Much to the agony of experts, clear explanatory coverage of the phenomenon from a technical standpoint was rare. In fact, so much so that AI startup founder Delip Rao penned a blog post titled ["The Real Problems with Neural Machine Translation"](http://deliprao.com/archives/301) which once again retiterated the experts' explanation that "one can safely assume Google’s parallel corpus collection contains all religious texts, and for many low-resource languages, they are not an insignificant portion of the training corpus." Despite this post and the fact that original article did also properly explain the reasons behind these oddities, these reasons were rarely presented as a centerpiece in subsequent media coverage. Purely going off the headlines, one might think that Google Translate had become conscious and adopted a religion.

# Our Perspective
The bottom line: as the original Motherboard article itself explained, AI researchers are not surprised by Google Translate's behavior. They can easily explain it.

Google Translate has been around for a long time, and Google hasn’t ceased to make constant improvements to its algorithms. When researchers at Google first published a [white paper](https://arxiv.org/pdf/1611.04558v1.pdf) announcing its implementation of neural machine translation in Google Translate in 2016, media outlets immediately jumped on the story, praising Google’s breakthrough translation technology that could even be [creating its own internal language system](https://techcrunch.com/2016/11/22/googles-ai-translation-tool-seems-to-have-invented-its-own-secret-internal-language/). High praise and heightened media coverage swirled around the new technique that could enhance Google’s software and generate much better translations almost overnight.

Now, flash-forward to 2018, we’re starting to see some cracks in the porcelain. Like all new technologies, NMT is not invincible. Here’s why.

1. **Machine learning is about finding patterns.** NMT tries at all costs to derive rational and human-like translations, and is **trained to do so**. If it is given madness, it will try to make meaning out of it. It isn’t trained on gibberish (after all, why would it be?), so it doesn’t output gibberish. Hence, it shouldn’t be surprising that jumbled letters are translated to sentences that make sense to us: the machine doesn’t know any better.
2. **Data sources explain a lot.** When we see Google Translate spitting out religious-themed text, the first thing that should pop onto our radar is: where is it getting this knowledge from? Just as with humans, vocabulary for machines is learned and taught. The answer is usually the training data. Google Translate is an illustrative case study of the **significance of training data in AI**: machines only know what they’ve seen and what we’ve put in, and in this case, experts suspect the Bible was a likely source.
3. **This is far from the first time we’ve seen something like this.** As others have noted, the random translations we’ve observed are analogous to bogus image classifications we find in computer vision. When networks are trained to identify different types of birds, and we throw a moose into the mix and ask the network to classify it, the model clearly hasn’t seen enough moose to know to classify it correctly. So, naturally, it coerces the answer into something familiar: a bird. The same principles hold here; if we give the network gibberish and it hasn’t seen gibberish before, we should take its translation output with a grain of salt.

**Staying informed is crucial.** Again and again, we see media outlets wrangling stories like this and packaging them into sensationalized glimpses of a creepy, unexplainable phenomenon. While it is praiseworthy that MotherBoard did indeed interview multiple experts on the subject and researched the topic well, the headline itself and various tweets to promote the article were still problematic and clickbaity. Clearly, many members of the public were led to believe something that wasn’t true, though the article itself had substantive content. Although there are obvious incentives to entice people to click on articles, in order to best serve the public, the media needs to tone down the gimmicky headings.

On the other hand, the public has the duty to be informed on the actual underpinnings of these stories and what the facts are surrounding new AI technologies. In addition, once we recognize the shortcomings of burgeoning technologies, we can help to prevent misinformed claims about its capabilities. A good read on the current known weaknesses of NMT can be found [here](http://deliprao.com/archives/301).

Finally, it’s also the duty of the scientific community and news outlets to make this information accessible and less of a black box so that misleading articles do not gain traction and spread the way they do. Doomsday is not approaching. Google Translate just read the Bible and didn’t know better.

# TLDR
The world is not ending. Google Translate is just confused.

After Google Translate produced various coherent, religiously tinged translations of gibberish input, this phenomenon was covered by the media as a complete mystery, despite many rational explanations from industry experts. These include the possible usage of the Bible as translation data in Google’s algorithm, especially for less common languages that have few large sources of alternative data. The results are unsurprising, since Google Translate is trained to translate meaningful phrases, and thus produced them out of nothing. Once again, we see that staying informed on AI topics and not giving in to sensational headlines is crucial in this day and age.
