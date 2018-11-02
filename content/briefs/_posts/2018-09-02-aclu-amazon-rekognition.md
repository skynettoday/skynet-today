---
layout: post
image:
  feature: /content/briefs/images/aclu-amazon-rekognition/header.png
  credit: Modified from <a href="https://www.aclu.org/blog/privacy-technology/surveillance-technologies/amazons-face-recognition-falsely-matched-28">ACLU's article</a>
title: "Amazon Rekognition Mistook Congressmen for Criminals? A Closer Look"
excerpt: "Examining ACLU’s claims of racial bias in face recognition technology as surveillance risk"
author: sneha_jha
editor: [andrey_kurenkov]
tags: [surveillance,BigBiz,ethics]
permalink: /briefs/aclu-amazon-rekognition
---


<figure>
  <img src="/content/briefs/images/aclu-amazon-rekognition/anim.gif" alt="Overview of Amazon's Rekognition product"/>
  <figcaption>
    Modified from <a href="https://twitter.com/ACLU/status/1022935153146978304">ACLU's Tweet</a>
  </figcaption>
</figure>


## What Happened

<figure>
  <img src="/content/briefs/images/aclu-amazon-rekognition/rekognition_overview.jpg" alt="Overview of Amazon's Rekognition product"/>
  <figcaption>
    Overview of Amazon's Rekognition product. <a href="https://securitytechnologyofsouthtexas.com/the-uses-and-limits-of-amazons-rekogntion-facial-recognition-software/">(source)</a>
  </figcaption>
</figure>

Amazon’s image and video analysis platform, called Rekognition, has been available to use for a while now. Like Google’s Vision API, Microsoft’s Face API, and other services it is a suite of tools to easily perform computer vision tasks as described on [their website](https://aws.amazon.com/rekognition/): 

> "You just provide an image or video to the Rekognition API, and the service can identify the objects, people, text, scenes, and activities, as well as detect any inappropriate content. Amazon Rekognition also provides highly accurate facial analysis and facial recognition on images and video that you provide. You can detect, analyze, and compare faces for a wide variety of user verification, people counting, and public safety use cases." 

Those facial recognition features recently got it into the spotlight when the ACLU published [a report](https://www.aclu.org/blog/privacy-technology/surveillance-technologies/amazons-face-recognition-falsely-matched-28) saying 28 members of Congress were incorrectly matched with mugshots of people who have been arrested for a crime. The ACLU had also previously reported on its concerns about Amazon’s "[dangerous new facial recognition technology](https://www.aclu.org/blog/privacy-technology/surveillance-technologies/amazon-teams-government-deploy-dangerous-new)" in May. 

<figure>
  <img src="/content/briefs/images/aclu-amazon-rekognition/rekognition_face.png" alt="Facial recognition search with rekognition."/>
  <figcaption>
    Facial recognition search with rekognition. <a href="https://blackchristiannews.com/2018/05/aclu-asks-amazon-to-stop-marketing-facial-recognition-technology-to-law-enforcement/">(source)</a>
  </figcaption>
</figure>


Using Rekognition, the ACLU created a face database and search tool of 25,000 publicly available mugshots. They then searched this set of 25,000 mugshots using public photos of every current member of the House and Senate as inputs[^note1], with the the default match settings that Amazon sets for Rekognition.  The Rekognition-based tool incorrectly matched 28 of the 435 members of Congress as criminals. 

[^note1]: More specifically, the way this works is by comparing the input face with all the target faces in the mugshot database. In response, it obtains a list of face matches ordered by similarity score in descending order. The similarity score indicates how closely the faces match. A similarity threshold can be set to specify the minimum level of confidence in the match that one wants returned in the response.)


<figure>
  <img src="/content/briefs/images/aclu-amazon-rekognition/aclu_0.png" alt="Overview of ACLU's examination of Rekognition."/>
  <figcaption>
    Overview of ACLU's examination of Rekognition. <a href="https://www.aclu.org/blog/privacy-technology/surveillance-technologies/amazons-face-recognition-falsely-matched-28">(source)</a>
  </figcaption>
</figure>


More importantly, people of color were flagged a lot more often (39%) as compared to white people (5%). It is worth noting that only 20% of the Congress members are people of color.


<figure>
  <img src="/content/briefs/images/aclu-amazon-rekognition/aclu_1.png" alt="The biased results found by ACLU."/>
  <figcaption>
    The biased results found by ACLU. <a href="https://www.aclu.org/blog/privacy-technology/surveillance-technologies/amazons-face-recognition-falsely-matched-28">(source)</a>
  </figcaption>
</figure>


It was not long before Amazon responded and refuted the claims.

## The Reactions

The reactions to this story were swift and from myriad quarters. 

Three of the misclassified legislators [wrote](https://www.markey.senate.gov/imo/media/doc/Amazon%20Facial%20Recognition%20Tech.pdf) to Jeff Bezos, CEO of Amazon, questioning the reliability of its software for law enforcement purposes. Three US Senators also penned [another letter](https://www.wyden.senate.gov/imo/media/doc/USCP%20Facial%20Rec.%20Letter.pdf) asking pointed questions to 39 law-enforcement agencies about their use of facial recognition technology and the potential for its misuse. Some of the misclassified legislators in ACLU’s test are members of the Congressional Black Caucus who even before this report have [expressed concern](https://cbc.house.gov/uploadedfiles/final_cbc_amazon_facial_recognition_letter.pdf) over Rekognition.

Jeff Bezos made no statement but the official blog of Amazon Web Services carried [this post](https://aws.amazon.com/blogs/machine-learning/thoughts-on-machine-learning-accuracy/) addressing the issue where they enumerate a host of reasons why a classification system could misbehave. Amazon noted that "The ACLU has not published its data set, methodology, or results in detail, so we can only go on what they’ve publicly said", and went on to justify themselves  with two main claims –

* That ACLU did not use the settings recommended by Amazon. They claim "We recommend 99% for use cases where highly accurate face similarity matches are important (as indicated in our public documentation", which is [easy to confirm as true](https://docs.aws.amazon.com/rekognition/latest/dg/collections.html). But, it is important to note that this recommendation in the documentation was added after the ACLU report ([it is still possible to see](https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/1266172b8812aeb1433cdf98124f070890c1da29/doc_source/collections.md) the recommendation was not there before June 27th of this year).

* That the facial recognition technology is meant to be vetted by human decision makers, which is what insulates it from potential misuse:

> "In real-world public safety and law enforcement scenarios, Amazon Rekognition is almost exclusively used to help narrow the field and allow humans to expeditiously review and consider options using their judgment (and not to make fully autonomous decisions), where it can help find lost children, fight against human trafficking, or prevent crimes. Rekognition is generally only the first step in identifying an individual. In other use cases (such as social media), there isn’t the same need to double check so confidence thresholds can be lower."

ACLU’s claim of using default settings comes from an example use case from Amazon’s website (matching an employee’s face with a work ID badge) where they use a confidence score of 80 percent [^note2]. Nina Lindsey, an Amazon spokesperson, clarified that Amazon recommended that police departments use a confidence score of minimum 95 percent and claims that ACLU’s departure from that recommendation was disingenuous. 

[^note2]: Simply put, that means the algorithm will only predict something (in this case, whether a face matches a mugshot) if it thinks it is 80% likely it is right. A higher threshold means a higher likelihood for individual matches to be right, but also means fewer predictions will be made overall; a lower threshold allows for more predictions, but with a higher likelihood of error.

The media largely picked up on the racial bias angle of the story, though [TechCrunch called it](https://techcrunch.com/2018/07/26/aclu-says-amazon-facial-recognition-associated-congress-members-with-mugshots/) ACLU’s "attention-grabbing stunt." 

> As far as attention-grabbing stunts go, this is a pretty good one. The ACLU has been attempting to raise awareness of Amazon’s Rekognition software for some time, stating that it "raises profound civil liberties and civil rights concerns."

Joshua Kroll, a researcher at UC Berkeley [weighed in](https://www.buzzfeednews.com/article/daveyalba/we-tested-the-fbis-most-wanted-list-on-amazons-celebrity) via BuzzFeed News that tried to expand the scope of the analysis carried out by ACLU. 

> Amazon is not particularly open about how its system works or what the confidence score even means with respect to the model. The company just says that higher scores are better.

Coverage also included Amazon’s defense of its tool in response to ACLU, as in [The Guardian’s take](https://www.theguardian.com/technology/2018/jul/26/amazon-facial-rekognition-congress-mugshots-aclu):

>Amazon defended its technology in a statement, saying the ACLU’s results could "probably be improved" if the test had increased the “confidence thresholds”, meaning the likelihood that Rekognition found a match.

On the whole, media coverage accurately portrayed the two sides of the story but rarely dug deeper into the claims of either side.

## Our Perspective

This isn’t the first time facial recognition technology has come under the scanner (see [a previous story](https://www.skynettoday.com/briefs/face-recog/) on the topic). Nor is Amazon the only company under scrutiny. e.g. Axon AI recently instituted [an Ethics Board](https://www.scribd.com/document/377489475/Letter-to-Axon-AI-Ethics-Board) in response to concerns around its technology. 

The technical merits of Amazon’s position notwithstanding, its you-are-responsible-for-using-our-tool-right response to the concerns of law and policy stakeholders is bordering on tone-deafness. Jacob Snow, a technology and civil liberties attorney with ACLU [responded](https://www.aclu.org/news/members-congress-demand-meeting-amazon-ceo-following-aclu-report-amazon-face-recognition) to Amazon’s reaction to this controversy claiming –

**_"Amazon seems to have missed, or refuses to acknowledge, the broader point: Face surveillance technology in the hands of government is primed for abuse and raises grave civil rights concerns._***" *

In reviewing Amazon’s own FAQ and  documentation for the Rekognition tool, we did not find any discussion of potential misuses of the tool or how the confidence threshold should be picked -- until it was added quietly in response to the ACLU story. In its response to the ACLU, Amazon makes it sounds like the scant documentation that is now there was always there (our own memory of looking for it as well as [github history](https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/1266172b8812aeb1433cdf98124f070890c1da29/doc_source/collections.md) shows that is not the case). At the very least, Amazon should have acknowledged its responsibility for keeping its customers informed as to ethical considerations related to the use of its AI tools. 

On the other hand, by ACLU’s own admission Amazon does provide consulting services to the customers of Rekognition[^note3]. So, there is some indication that consumers may have guidance in determining suitable values for deployment. And, it is true that the ACLU "has not published its data set, methodology, or results in detail" [^note4] which is not ideal since it is harder to be certain that the fault lies with Amazon. 


[^note3]: According to documents  which the ACLU obtained through a Freedom of Information Act request.

[^note4]: Mugshots are public records in many states, but ACLU declined to specify the source of its 25,000 mugshots citing  privacy reasons.

Still, even if not ideally executed ACLU’s actions were definitely for a  good cause -- issues around fairness and bias in algorithms are well-known even if not well-studied at this point. Automated decision systems are not immune from biases. In fact, they often tend to carry over or even amplify the biases presented to them via data and design. Given the fact that law enforcement in this country has a documented history of racial discrimination, there is a very real cost to potential misuse of AI tools to exacerbate things. Thus, there is a valid cause for apprehension even presuming no mala fide intent on the part of either Amazon or its users.

## TLDR

Are developers of technology responsible for its misuse? 

This age old question is now more relevant than ever in the context of AI, and given the complex nature of AI the answer must at least partially be yes; the developers of AI algorithms must communicate its limitations and important parameters to prevent **accidental** misuse. 

ACLU’s report brings a few things to the fore that need to be seriously discussed, especially as more and more human decisions are aided by algorithms. Often the rate of adoption of technology puts it out of step with the general public’s understanding of its limitations. Not only are facial recognition systems far from perfect, when they fail, it is often in unpredictable ways. So, to rely on them for use cases like law enforcement is rightly contentious, at the moment.

The issue of fairness, bias, and accountability cannot be an afterthought but needs to be viewed as an integral part of the AI systems we hope to use in the real world. 

<hr>

