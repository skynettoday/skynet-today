---
title: "Humans Who Are Not Concentrating Are Not General Intelligences"
author: [sarah_constantin]
categories: [editorials]
tags: [DeepFakes,OpenAI]
excerpt: "On why human level intelligence is not needed to create algorithmically generated text that may seem like it was written by a human"
image: 
  feature: assets/img/editorials/2019-09-06-humans-not-concentrating/main.jpg
permalink: /editorials/humans-not-concentrating
---
_The following piece originally appeared on [Sarah Constantin's blog](https://srconstantin.wordpress.com/2019/02/25/humans-who-are-not-concentrating-are-not-general-intelligences/), and has been replicated here with permission. Although it focuses on the release of the original GPT-2 model, it equally holds for the larger versions of the model that have recently led to more [fearful](https://thenextweb.com/artificial-intelligence/2019/08/21/this-ai-powered-text-generator-is-the-scariest-thing-ive-ever-seen-and-you-can-try-it/) [coverage](https://www.bbc.com/news/technology-49446729)._

# Humans Who Are Not Concentrating Are Not General Intelligences

Recently, OpenAI came out with a [new language model][1] that automatically synthesizes text, called GPT-2.

It's disturbingly good.  You can see some examples (cherry-picked, by their own admission) in OpenAI's [post][1] and in the related [technical paper.][2] For instance, here is an excerpt from one example:

> System Prompt (human-written): In a shocking finding, scientist discovered a herd of unicorns living in a remote, previously unexplored valley, in the Andes Mountains. Even more surprising to the researchers was the fact that the unicorns spoke perfect English.

> Model Completion (machine-written, 10 tries):  The scientist named the population, after their distinctive horn, Ovid’s Unicorn. These four-horned, silver-white unicorns were previously unknown to science.
> 
> Now, after almost two centuries, the mystery of what sparked this odd phenomenon is finally solved.
> 
> Dr. Jorge Pérez, an evolutionary biologist from the University of La Paz, and several companions, were exploring the Andes Mountains when they found a small valley, with no other animals or humans. Pérez noticed that the valley had what appeared to be a natural fountain, surrounded by two peaks of rock and silver snow.
> 
> Pérez and the others then ventured further into the valley. “By the time we reached the top of one peak, the water looked blue, with some crystals on top,” said Pérez.

I'm not going to write about the machine learning here, but about the examples and what we can infer from them.

The scary thing about GPT-2-generated text is that it flows very naturally if you're just skimming, reading for writing style and key, evocative words.  The "unicorn" sample reads like a real science press release. The "theft of nuclear material" sample reads like a real news story. The "Miley Cyrus shoplifting" sample reads like a real post from a celebrity gossip site.  The "GPT-2" sample reads like a real OpenAI press release. The "Legolas and Gimli" sample reads like a real fantasy novel. The "Civil War homework assignment" reads like a real C-student's paper.  The "JFK acceptance speech" reads like a real politician's speech.  The "recycling" sample reads like a real right-wing screed.

If I just skim, without focusing, they all look _totally normal._ I would not have noticed they were machine-generated. I would not have noticed anything amiss about them at all.

But if I read with focus, I notice that they don't make a lot of logical sense.

For instance, in the unicorn sample:

> The scientist named the population, after their distinctive horn, Ovid's Unicorn. These four-horned, silver-white unicorns were previously unknown to science.

Wait a second, "Ovid" doesn't refer to a "distinctive horn", so why would naming them "Ovid's Unicorn" be naming them after a distinctive horn?  Also, you just said they had _one_ horn, so why are you saying they have _four_ horns in the next sentence?

> While their origins are still unclear, some believe that perhaps the creatures were created when a human and a unicorn met each other in a time before human civilization. According to Pérez, "In South America, such incidents seem to be quite common."

Wait, _unicorns_ originated from the interbreeding of humans and … unicorns?  That's circular, isn't it?

Or, look at the GPT-2 sample:

> We believe this project is the first step in the direction of developing large NLP systems without task-specific training data. That is, we are developing a machine language system in the generative style with no explicit rules for producing text.

Except the second sentence _isn't_ a restatement of the first sentence — "task-specific training data" and "explicit rules for producing text" aren't synonyms!  So saying "That is" doesn't make sense.

Or look at the LOTR sample:

> Aragorn drew his sword, and the Battle of Fangorn was won. As they marched out through the thicket the morning mist cleared, and the day turned to dusk.

Yeah, day doesn't turn to dusk in the _morning_.

Or in the "resurrected JFK" sample:

> (1) The brain of JFK was harvested and reconstructed via tissue sampling. There was no way that the tissue could be transported by air. (2) A sample was collected from the area around his upper chest and sent to the University of Maryland for analysis. A human brain at that point would be about one and a half cubic centimeters. The data were then analyzed along with material that was obtained from the original brain to produce a reconstruction; in layman's terms, a "mesh" of brain tissue.

His brain tissue was harvested…from his chest?!  A human brain is one and a half cubic centimeters?!

So, ok, this isn't actually human-equivalent writing ability. OpenAI doesn't claim it is, for what it's worth — I'm not trying to diminish their accomplishment, that's not the point of this post.  The point is, _if you skim text, you miss obvious absurdities_.  The point is _OpenAI HAS achieved the ability to pass the Turing test against humans on autopilot_.

The point is, I know of a few people, acquaintances of mine, who, even when asked to try to find flaws, _could not detect anything weird or mistaken in the GPT-2-generated samples_.

There are probably a lot of people who would be completely taken in by literal "fake news", as in, computer-generated fake articles and blog posts.  This is pretty alarming.  Even more alarming: unless I make a conscious effort to read carefully, _I would be one of them_.

Robin Hanson's post [Better Babblers][3] is very relevant here.  He claims, and I don't think he's exaggerating, that a lot of human speech is simply generated by "low order correlations", that is, generating sentences or paragraphs that are statistically likely to come after previous sentences or paragraphs:

> After eighteen years of being a professor, I've graded _many_ student essays. And while I usually try to teach a deep structure of concepts, what the median student actually learns seems to mostly be a set of low order correlations. They know what words to use, which words tend to go together, which combinations tend to have positive associations, and so on. But if you ask an exam question where the deep structure answer differs from answer you'd guess looking at low order correlations, most students usually give the wrong answer.
> 
> Simple correlations also seem sufficient to capture most polite conversation talk, such as the weather is nice, how is your mother's illness, and damn that other political party. Simple correlations are also most of what I see in inspirational TED talks, and when public intellectuals and talk show guests pontificate on topics they really don't understand, such as quantum mechanics, consciousness, postmodernism, or the need always for more regulation everywhere. After all, media entertainers don't need to understand deep structures any better than do their audiences.
> 
> Let me call styles of talking (or music, etc.) that rely mostly on low order correlations "babbling". Babbling isn't meaningless, but to ignorant audiences it often appears to be based on a deeper understanding than is actually the case. When done well, babbling can be entertaining, comforting, titillating, or exciting. It just isn't usually a good place to learn deep insight.

I used to half-joke that the [New Age Bullshit Generator][4] was _actually useful_ as a way to get myself to feel more optimistic. The truth is, it isn't quite good enough to match the "aura" or "associations" of genuine, human-created inspirational text. GPT-2, though, _is_.

I also suspect that the "lyrical" or "free-associational" function of poetry is adequately matched by GPT-2.  The [autocompletions of _Howl_][5] read a lot like Allen Ginsberg — they just don't imply the same beliefs about the world.  (_Moloch whose heart is crying for justice!_ sounds rather positive.)

I've noticed that I cannot tell, from casual conversation, whether someone is intelligent in the IQ sense.

I've interviewed job applicants, and perceived them all as "bright and impressive", but found that the vast majority of them could not solve a simple math problem.  The ones who could solve the problem didn't appear any "brighter" in conversation than the ones who couldn't.

I've taught public school teachers, who were _incredibly_ bad at formal mathematical reasoning (I know, because I graded their tests), to the point that I had not realized humans could be that bad at math — but it had _no_ effect on how they came across in friendly conversation after hours. They didn't seem "dopey" or "slow", they were witty and engaging and warm.

I've read the personal blogs of intellectually disabled people — people who, by definition, score poorly on IQ tests — and _they_ don't read as any less funny or creative or relatable than anyone else.

Whatever ability IQ tests and math tests measure, I believe that lacking that ability doesn't have _any_ effect on one's ability to make a good social impression or even to "seem smart" in conversation.

If "human intelligence" is about reasoning ability, the capacity to detect whether arguments make sense, then you simply do not need human intelligence to create a linguistic style or aesthetic that can fool our pattern-recognition apparatus if we don't concentrate on parsing content.

I also noticed, upon reading GPT2 samples, just how often my brain slides from focused attention to just skimming. I read the paper's sample about Spanish history with interest, and the GPT2-generated text was obviously absurd. My eyes glazed over during the sample about video games, since I don't care about video games, and the machine-generated text looked totally unobjectionable to me. My brain is constantly making evaluations about what's worth the trouble to focus on, and what's ok to tune out. GPT2 is actually really useful as a *test* of one's level of attention.

This is related to my hypothesis that effortless pattern-recognition is what machine learning can do today, while effortful attention, and explicit reasoning (which seems to be a subset of effortful attention) is generally beyond ML's current capabilities.

Beta waves in the brain are usually associated with focused concentration or active or anxious thought, while alpha waves are associated with the relaxed state of being awake but with closed eyes, before falling asleep, or while dreaming. Alpha waves sharply reduce after a subject makes a mistake and begins paying closer attention. I'd be interested to see whether ability to tell GPT2-generated text from human-generated text correlates with alpha waves vs. beta waves.

The first-order effects of highly effective text-generators are scary. It will be incredibly easy and cheap to fool people, to manipulate social movements, etc. There's a lot of opportunity for bad actors to take advantage of this.

The second-order effects might well be good, though. If only conscious, focused logical thought can detect a bot, maybe some people will become more aware of when they're thinking actively vs not, and will be able to flag when they're not really focusing, and distinguish the impressions they absorb in a state of autopilot from "real learning".

The mental motion of "I didn't really parse that paragraph, but sure, whatever, I'll take the author's word for it" is, in my introspective experience, absolutely identical to "I didn't really parse that paragraph because it was bot-generated and didn't make any sense so I couldn't possibly have parsed it", except that in the first case, I assume that the error lies with me rather than the text.  This is not a safe assumption in a post-GPT2 world. Instead of "default to humility" (assume that when you don't understand a passage, the passage is true and you're just missing something) the ideal mental action in a world full of bots is "default to null" (if you don't understand a passage, assume you're in the same epistemic state as if you'd never read it at all.)

Maybe practice and experience with GPT2 will help people get better at doing "default to null"?

[1]: https://blog.openai.com/better-language-models/
[2]: https://d4mucfpksywv.cloudfront.net/better-language-models/language_models_are_unsupervised_multitask_learners.pdf
[3]: http://www.overcomingbias.com/2017/03/better-babblers.html
[4]: http://sebpearce.com/bullshit/
[5]: http://antinegationism.tumblr.com/post/182901133106/an-eternal-howl

  
