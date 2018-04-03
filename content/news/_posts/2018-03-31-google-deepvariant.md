---
layout: post
title: "Can a \"Google AI\" Build Your Genome Sequence?"
excerpt: "A new AI-powered tool from Google promises more-accurate genome sequences, but its impact on genomics research remains to be seen"
author: alex_constantino
editor: andrey_kurenkov
tags: [biology,google,genomics]
---

## What Happened

In December 2017, Google [announced a new tool called DeepVariant](https://research.googleblog.com/2017/12/deepvariant-highly-accurate-genomes.html):

> Today, we announce the open source release of DeepVariant, a deep learning technology to reconstruct the true genome sequence from HTS sequencer data with significantly greater accuracy than previous classical methods.

Simultaneously, the DeepVariant authors published [a paper](https://www.biorxiv.org/content/biorxiv/early/2018/03/20/092890.full.pdf) detailing their research and, unlike many research projects, provided the complete underlying [code](https://github.com/google/deepvariant) — yay! So what is it, and how does it work?

First, let’s talk about DNA. DNA is the molecule that determines your genetic makeup, influencing everything from your height to your eye color to your risk of getting cancer. Each person’s genetic information can be represented as a sequence of the letters A, T, C, and G. Thanks to a technology called high-throughput sequencing, it is now possible to read the ~3 billion letters in your DNA for just ~$1000, which has in turn been fueling the rapidly growing field of genomics research.

Here’s how high-throughput sequencing typically works: DNA molecules are isolated from blood or spit and broken into millions of pieces with a couple hundred letters each. To read each letter, a machine adds a chemical dye to each piece, lights up the dye with a laser, and takes a picture. The rest of the process happens on computers — a program processes each picture to determine the most likely letter sequence for each piece, aligns each piece to a complete reference sequence, and lists "variants" (a variant is any difference between the sample and reference sequence e.g. “three letters deleted” or “A instead of T”).

<figure>
	<img src="{{site.url}}/content/news/images/2018-03-30-google-deepvariant/image_0.png" alt="Pileup Examples">
	<figcaption>
Examples of the "pile-up" pictures that DeepVariant interprets. The different colors correspond to the A’s, T’s, G’s, and C’s of DNA. See those gaps in sections B and C? Those indicate that part of the genome was deleted.
	</figcaption>
</figure>

DeepVariant performs only the last step — determining which variants the aligned pieces represent. It’s powered by [Deep Learning](http://theai.wiki/Deep%20Learning), the technique behind most recent advances in AI and machine learning. As the authors demonstrate, it is significantly more accurate than existing tools, [making 10x fewer errors](https://blog.dnanexus.com/2017-12-05-evaluating-deepvariant-googles-machine-learning-variant-caller/). Interestingly, DeepVariant is based on [a deep neural network architecture](https://research.googleblog.com/2016/08/improving-inception-and-image.html) that was initially applied to classifying whether a picture contains a dog or a cat, showcasing the applicability of Deep Learning to wildly different problems.

## The Reactions

The media coverage about DeepVariant was generally accurate in its portrayal of both the technical and non-technical aspects of the research:

* Wired reported that "[Google Is Giving Away AI That Can Build Your Genome Sequence](https://www.wired.com/story/google-is-giving-away-ai-that-can-build-your-genome-sequence/)". The article does a great job of providing context for the research and the problem it solves, as well as telling the human story about how the project started at Google.

* The MIT Technology Review published an article with the more-muted title "[Google Has Released an AI Tool That Makes Sense of Your Genome](https://www.technologyreview.com/s/609647/google-has-released-an-ai-tool-that-makes-sense-of-your-genome/)". It goes more into detail about the competitive landscape for these tools instead of focusing on the human story.

* The Atlantic used the engaging headline "[Google Taught an AI That Sorts Cat Photos to Analyze DNA](https://www.theatlantic.com/science/archive/2017/12/google-deepvariant-dna/547634/)".  This is technically correct, since DeepVariant uses the same neural network architecture that excels at other image processing problems.

* A Forbes blog post titled "[No, Google's AI Program Can't Build Your Genome Sequence](https://www.forbes.com/sites/stevensalzberg/2017/12/11/no-googles-new-ai-cant-build-your-genome-sequence/#6a944cf05774)" called out Wired for their use of the phrase “assembling genomes” (genome assembly is a different problem in genomics, and not the one DeepVariant solves). But this is really a nitpick — to a general audience, it’s a reasonable description of what DeepVariant does, although a technical audience may interpret the word “assembling” differently. Wired nonetheless clarified this in a correction. 

Many headlines made the mistake of calling DeepVariant an "AI" (artificial intelligence), when it is really a computer program that uses AI techniques to determine genetic variants. It is not an “intelligence” in itself. Besides this common wording mistake, the coverage was on the whole well done.

## Our Perspective

So a 10x reduction in errors is awesome, right? Well, there are two catches. First, even though DeepVariant reduces the number of errors by 10x, there are relatively few errors to begin with — in one test, DeepVariant achieved an accuracy score of 0.99, while its competitors are not far behind at ~0.97. Second, DeepVariant is **deeply** expensive — it requires between 2 and 13 times as much computational power as its competitors. Doubling your computational budget is a difficult ask of research groups that operate on fixed grants, particularly for a marginal increase in accuracy.  

A [search](https://scholar.google.com/scholar?cites=17906459847542072356&as_sdt=5,39&sciodt=0,39&hl=en) of Google Scholar reveals that as of March 2018, **no scientific publications have used it** except for testing. Meanwhile, [over 400 papers](https://scholar.google.com/scholar?as_ylo=2018&hl=en&as_sdt=5,39&sciodt=0,39&cites=8846816360225209514&scipsc=) in 2018 used the competing framework GATK and [over 700](https://scholar.google.com/scholar?as_ylo=2018&hl=en&as_sdt=5,39&sciodt=0,39&cites=14180093680384888523&scipsc=) used SAMtools. It appears that computational cost or general unfamiliarity are deterring its adoption in the research community. In fairness, DeepVariant has only been available for three months, and adoption may pick up over time as specialized AI processors become more available to academic researchers. It’s also possible the tool could be made faster without losing accuracy or see greater adoption through Google [cloud offering of it](https://cloud.google.com/genomics/deepvariant).

In some ways, DeepVariant perfectly illustrates the strengths and weaknesses of Deep Learning. Unlike previous tools, it doesn’t require a team of experts to spend years teaching it to deal with different kinds of errors — it simply learns patterns by being shown lots of pictures. However, it requires much more computer power and only incrementally improves accuracy.

## TLDR

Google’s DeepVariant is a more accurate method for doing **one** part of the genome sequencing process. It has seen little adoption by researchers in its first three months, likely due to the extra computational cost for marginal improved accuracy. Media coverage correctly describes the research, but its impact on the broader scientific field remains to be seen.

Disclosure: I worked for Google and still have some equity.

