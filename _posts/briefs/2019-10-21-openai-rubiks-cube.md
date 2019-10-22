---
layout: post
image:
  feature: assets/img/briefs/openai-rubiks-cube/dr.jpg
  credit: <a href="https://openai.com/blog/solving-rubiks-cube/">OpenAI</a>
title: "OpenAI's dexterous robotic hand — separating progress from PR"
excerpt: "The Rubik’s cube solving hand is representative of a true research contribution, but its many caveats do not merit the PR hype"
author: [jacky_liang,andrey_kurenkov]
tags: [OpenAI,robotics,hype]
categories: [briefs]
permalink: /briefs/openai-rubiks-cube
highlight: true
---

## What Happened

On October 15th, [OpenAI](https://en.wikipedia.org/wiki/OpenAI) released a pre-print[^preprint] [paper](https://arxiv.org/abs/1910.07113) and an accompanying [blog](https://openai.com/blog/solving-rubiks-cube/) post both titled “Solving Rubik’s Cube with a Robot Hand”, describing how the team was able to train a 5-fingered robot hand to manipulate a Rubik’s cube with Deep Reinforcement Learning, or Deep RL[^RL].

<figure>
<blockquote class="twitter-tweet" data-dnt="true" data-theme="light" data-link-color="#2B7BB9"><p lang="en" dir="ltr">We&#39;ve trained an AI system to solve the Rubik&#39;s Cube with a human-like robot hand.<br><br>This is an unprecedented level of dexterity for a robot, and is hard even for humans to do.<br><br>The system trains in an imperfect simulation and quickly adapts to reality: <a href="https://t.co/O04izt3KvO">https://t.co/O04izt3KvO</a> <a href="https://t.co/8lGhU2pPck">pic.twitter.com/8lGhU2pPck</a></p>&mdash; OpenAI (@OpenAI) <a href="https://twitter.com/OpenAI/status/1184135128869527552?ref_src=twsrc%5Etfw">October 15, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 
</figure>

OpenAI emphasized the “robustness” of the learned algorithm, exemplified by how the robot hand was able to manipulate the Rubik’s cube even when two of the fingers were tied together, or when the cube was pushed around by external forces. Both of these scenarios were not encountered by the algorithm during training. 

<figure>
<blockquote class="twitter-tweet" data-conversation="none" data-dnt="true"><p lang="en" dir="ltr">We’re all used to robots that fail when their environment changes unpredictably. Our robotic system is adaptable enough to handle unexpected situations not seen during training, such as being prodded by a stuffed giraffe: <a href="https://t.co/wBoh1nt9Kv">pic.twitter.com/wBoh1nt9Kv</a></p>&mdash; OpenAI (@OpenAI) <a href="https://twitter.com/OpenAI/status/1184145789754335232?ref_src=twsrc%5Etfw">October 15, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 
</figure>

Along with the paper and blog post, OpenAI also released a slickly produced video about the project:

<figure>
<iframe width="560" height="315" src="https://www.youtube.com/embed/x4O8pojMF0w" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</figure>

As stated in the blog post and paper, the project is not about solving a Rubik’s Cube in the sense of deriving a sequence of face rotation steps to return the cube to the "solved state." Rather, the project focuses on learning how to control a robot hand to manipulate a Rubik's cube to execute these rotations, with the rotations themselves being solved by a pre-existing Rubik’s cube solver.

<figure>
 <img src="{{ site.imgpath }}/briefs/openai-rubiks-cube/tasks.png" alt="An image showing the block reorientation and Rubik’s cube tasks, side by side. From the paper."/>
  <figcaption>
    An image showing the block reorientation OpenAI has previously tackled and the Rubik’s cube tasks, side by side. From the <a href="https://arxiv.org/abs/1910.07113">paper</a>.
  </figcaption>
</figure>

The approach OpenAI takes is largely identical to [one used last year to enable the same hand to reorient a cube](https://openai.com/blog/learning-dexterity/), except for a technique called “Automatic Domain Randomization,” or ADR [^new]. ADR is a new approach to domain randomization (DR), which is the technique of varying many visual and physical parameters of a simulation, with the idea that an algorithm trained to work in all of these different simulation has a better chance of working in the real world.

Normal DR requires manually setting the range of the randomized parameters. By contrast, with ADR these ranges are “defined automatically and allowed to change” in ways that progressively increase the variety of environments the algorithm needs to work in. Thus, ADR removes “significant amount of manual tuning” the team had to do for their previous cube reorientation project, while making learning more efficient. This idea is “strongly related”[^quote] to prior work such as [POET](https://twitter.com/welcomeai/status/1089305829516431361) and other recent works that suggest improvements upon DR.

A number of articles covering this news were released (e.g. [TechCrunch](https://techcrunch.com/2019/10/15/watch-openais-human-like-robot-solve-a-rubiks-cube-one-handed/), [The Verge](https://www.theverge.com/2019/10/15/20914575/openai-dactyl-robotic-hand-rubiks-cube-one-handed-solve-dexterity-ai), [IEEE Spectrum](https://spectrum.ieee.org/automaton/robotics/robotics-hardware/openai-demonstrates-sim2real-by-with-onehanded-rubiks-cube-solving), [VentureBeat](https://venturebeat.com/2019/10/15/openai-teaches-a-robotic-hand-to-solve-a-rubiks-cube/)) on the same day, in keeping with OpenAI’s tendency of sharing their work with journalists before most other researchers so that media coverage can be released on the same day as its research is announced. Some articles focused on how the robot learned to perform the task “[without needing to be specifically programmed](https://www.theverge.com/2019/10/15/20914575/openai-dactyl-robotic-hand-rubiks-cube-one-handed-solve-dexterity-ai)” and instead “[approaches new tasks much like a human would](https://www.theverge.com/2019/10/15/20914575/openai-dactyl-robotic-hand-rubiks-cube-one-handed-solve-dexterity-ai).” Others emphasized the simulation aspect: how the technique didn’t “[need any real-world training at all, as long as [the] simulations are diverse enough](https://spectrum.ieee.org/automaton/robotics/robotics-hardware/openai-demonstrates-sim2real-by-with-onehanded-rubiks-cube-solving).”

##  The Reactions

On Twitter, most of the OpenAI researchers highlighted the “general-purpose” take on the work:

<figure>
<blockquote class="twitter-tweet" data-conversation="none" data-dnt="true"><p lang="en" dir="ltr">Announcing major progress towards general-purpose robots.<br><br>This robot is trained using the same reinforcement learning code as OpenAI Five, plus a new technique for transferring knowledge from simulation to reality.<br><br>Result is unprecedented dexterity:<a href="https://t.co/azkJtOFsqA">https://t.co/azkJtOFsqA</a></p>&mdash; Greg Brockman (@gdb) <a href="https://twitter.com/gdb/status/1184137159713808384?ref_src=twsrc%5Etfw">October 15, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 

<blockquote class="twitter-tweet" data-conversation="none" data-dnt="true"><p lang="en" dir="ltr">RL can train an NN policy to do pretty much anything in sim. With Automatic Domain Randomization, we can bridge the sim2real gap by training the policy to be so adaptible, that it can generalize to the physical robot. The result: it solves the Rubik&#39;s cube with a robot hand! <a href="https://t.co/otGpnDq6DH">https://t.co/otGpnDq6DH</a></p>&mdash; Ilya Sutskever (@ilyasut) <a href="https://twitter.com/ilyasut/status/1184138340754264065?ref_src=twsrc%5Etfw">October 15, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 

<blockquote class="twitter-tweet" data-conversation="none" data-dnt="true"><p lang="en" dir="ltr">In the end, this result is not so much about the Rubik&#39;s Cube, as it is about learning dexterity as step towards general purpose robots. The techniques are quite general: RL + ADR could in principle be applied to any task you can simulate.</p>&mdash; Peter Welinder (@npew) <a href="https://twitter.com/npew/status/1184139159776051206?ref_src=twsrc%5Etfw">October 15, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 
</figure>

Multiple journalists conveyed this idea, but also noted that while the demonstration is impressive, the robot’s real-world performance is still quite limited.

From Wired’s [Why Solving a Rubik's Cube Does Not Signal Robot Supremacy](https://www.wired.com/story/why-solving-rubiks-cube-not-signal-robot-supremacy/):

> There are serious caveats with the Dactyl demo. For one thing, the robot dropped the cube eight out of 10 times in testing—hardly evidence of superhuman, or even human, deftness. For another, it required the equivalent of 10,000 years of simulated training to learn to manipulate the cube.

From BBC’s [Robot hand solves Rubik’s cube, but not the grand challenge](https://www.bbc.com/news/technology-50064225):

> The BBC has not been able to independently verify the performance of OpenAI’s robot. And, while details were not disputed by the experts the BBC spoke to, OpenAI’s research paper was not peer-reviewed.

From the New York Times’ [If a Robotic Hand Solves a Rubik’s Cube, Does It Prove Something?](https://www.nytimes.com/2019/10/15/technology/robot-hand-rubiks-cube.html):

> A five-fingered feat could show important progress in A.I. research. It is also a stunt.

As blunt as the “stunt” commentary is, many robotics researchers have responded with concerns over the hype that OpenAI’s PR push was able to generate about a work that may not be as revolutionary as all this media coverage may make it seem. The Wired article mentioned above quotes Professor Leslie Kaebling from MIT who “[cautions that the approach likely won’t create general-purpose robots, because it requires so much training](https://www.wired.com/story/why-solving-rubiks-cube-not-signal-robot-supremacy/)” and Professor Ken Goldberg from UC Berkeley who says “[I wouldn’t say it's total hype — it's not ... but people are going to look at that video and think, ‘My God, next it’s going to be shuffling cards and other things,’ which it isn’t](https://www.wired.com/story/why-solving-rubiks-cube-not-signal-robot-supremacy/)”.

While the above coverage did a good job of highlighting the benefit of the work while making clear the scope of the achievement is limited, not all coverage was this accurate. The Washington Post's [This robotic hand learned to solve a Rubik’s Cube on its own — just like a human](https://www.washingtonpost.com/technology/2019/10/18/this-robotic-hand-learned-solve-rubiks-cube-its-own-just-like-human/) mischaracterized the work as being about solving the steps needed to solve the Rubik's cube and not just the manipulation component of it. To their credit, OpenAI has stated (through a [comment from its CEO Greg Brockman on reddit](https://www.reddit.com/r/MachineLearning/comments/dkd4vz/d_gary_marcus_tweet_on_openai_still_has_not/f4dbuhb/)), that it has been reaching out to try and correct coverage of the work that is inaccurate, such as this one.

Some members of the AI community felt that OpenAI was partly to blame for people potentially having the same misunderstanding as in the Washington Post's article. A common criticism along these lines is that OpenAI titling this “Solving Rubik’s Cube with a Robot Hand” was misleading due to implying the algorithm learned to reason about the steps needed to solve the cube in addition to how to manipulate it, and in obscuring the low success rate of the algorithm: 

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">I will say again that the work itself is impressive, but mischaracterized, and that a better title would have been &quot;manipulating a Rubik&#39;s cube using reinforcement learning&quot; or &quot;progress in manipulation with dextrous robotic hands&quot; or similar lines.</p>&mdash; Gary Marcus (@GaryMarcus) <a href="https://twitter.com/GaryMarcus/status/1185680538335469568?ref_src=twsrc%5Etfw">October 19, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Fully agree. I had written about mis-information around GPT-2 earlier. As a community, we have responsibility to be truthful and accountable, otherwise <a href="https://twitter.com/hashtag/AI?src=hash&amp;ref_src=twsrc%5Etfw">#AI</a> will be victim of hype cycle and true research will suffer <a href="https://t.co/6a47nLgwEp">https://t.co/6a47nLgwEp</a></p>&mdash; Anima Anandkumar (hiring) (@AnimaAnandkumar) <a href="https://twitter.com/AnimaAnandkumar/status/1185682761698295808?ref_src=twsrc%5Etfw">October 19, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Good example of AI hype. Did OpenAI solve Rubik&#39;s cube? You decide: used an old search algorithm to determine what moves to make; used RL to learn how to manipulate a special cube with bluetooth sensors; dropped the cube 80% of the time. Impressive, but doesn&#39;t match the hype. <a href="https://t.co/hoI3TumtXi">https://t.co/hoI3TumtXi</a></p>&mdash; Tim Miller (@tmiller_unimelb) <a href="https://twitter.com/tmiller_unimelb/status/1185702001943859200?ref_src=twsrc%5Etfw">October 19, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 

This in turn led to discussions on popular tech forums such as [Hacker News](https://news.ycombinator.com/item?id=21306017) and [r/MachineLearning on reddit](https://www.reddit.com/r/MachineLearning/comments/dkd4vz/d_gary_marcus_tweet_on_openai_still_has_not/), where commenters both agreed with the above criticisms and argued against them as being overly pedantic. OpenAI's Chief Scientist Ilya Sutskever characterized the criticism as being in "bad faith", while OpenAI Chairman & CTO Greg Brockman dismissed it as being unjustified:

<figure>
<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Surprised and saddened by all the bad faith criticism of our robotic manipulation result <a href="https://t.co/POljoP8jog">https://t.co/POljoP8jog</a></p>&mdash; Ilya Sutskever (@ilyasut) <a href="https://twitter.com/ilyasut/status/1186138841041666048?ref_src=twsrc%5Etfw">October 21, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Kinda funny that <a href="https://twitter.com/GaryMarcus?ref_src=twsrc%5Etfw">@GaryMarcus</a> has a problem with the title of &quot;Solving Rubik&#39;s Cube with a Robot Hand&quot; for a result that literally involves a robot hand solving a Rubik&#39;s cube.<a href="https://t.co/0BZ4If2g68">https://t.co/0BZ4If2g68</a></p>&mdash; Greg Brockman (@gdb) <a href="https://twitter.com/gdb/status/1186287693862301696?ref_src=twsrc%5Etfw">October 21, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 
</figure>

The latter led to a response once again arguing the title was misleading and should be altered:

<figure>
<blockquote class="twitter-tweet"><p lang="en" dir="ltr">I stand with Gary.<br><br>I celebrate the technical accomplishments of <a href="https://twitter.com/OpenAI?ref_src=twsrc%5Etfw">@OpenAI</a> <br><br>I call upon you to demonstrate the same level of leadership with regard to the integrity and transparency of your reporting about it. You owe this to the AI community and especially to the general public.</p>&mdash; Grady Booch (@Grady_Booch) <a href="https://twitter.com/Grady_Booch/status/1186316475377733632?ref_src=twsrc%5Etfw">October 21, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 
</figure>

Aside the notion that OpenAI may have misled people in this specific case, another concern voiced in response to this news was that releasing new research alongside a large amount of cultivated media coverage is a pattern for OpenAI that is detrimental to the public's understanding of AI progress as a whole. As stated in the [New York Times’ piece](https://www.nytimes.com/2019/10/15/technology/robot-hand-rubiks-cube.html):

> Many academics, including [Professor Zachary Lipton from Carnegie Mellon University], bemoaned the way that artificial intelligence is hyped through news releases and showy demonstrations. But that is not something that will change anytime soon.
> “These are serious technologies that people need to think about,” Dr. Lipton said. “But it is difficult for the public to understand what is happening and what they should be concerned about and what will actually affect them.”

Professor Lipton further expanded on these thoughts on Twitter:

<figure>
<blockquote class="twitter-tweet"><p lang="en" dir="ltr">A cherry-picked list of friendly reporters pegged; they&#39;re spoon-fed ready-packaged stories, complete with flashy animations, dramatic lighting, some off-the-rails twist about the existential import of this AI leap; then, hungry for content, they credulously amplify the story.</p>&mdash; Zachary Lipton (@zacharylipton) <a href="https://twitter.com/zacharylipton/status/1184237038553296896?ref_src=twsrc%5Etfw">October 15, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
</figure>

One of the [most highly voted comments](https://news.ycombinator.com/item?id=21306542) in the [Hacker News discussion](https://news.ycombinator.com/item?id=21306017) echoes these thoughts:

> [In response to "How is OpenAI misleading?"] 
> Because this has become a pattern in OpenAI's MO.
> Take a very impressive research achievement (large LSTM on byte-level language modeling/GPT-2). present it in a hyperbolic manner ("we've discovered a single neuron that captures sentiment", "the full GPT-2 is too dangerous to release"). wait for the press to eat it up, and if the technical press calls them out on misleading claims, even better, because it'll get even more traction then. Wait for defenders to show up stating that the original research achievement was impressive. Make no effort to clarify misleading claims.
> The misleading word here is "solve", which can have two meanings: to derive a solution for a Rubik's cube, or to manipulate a Rubik's cube into a solved state. The casual reader absolutely assumes the former (which also appears as a challenging, intellectual task), whereas the technical achievement here is the latter. But of course, a press released titled "Solving Rubik's Cube with a Robot Hand" sounds much more impressive than "Manipulating Rubik's Cube with a Robot Hand".
> I say this as a person who has benefited from their great research output and models: please stop playing this terrible PR game. You do your research work a disservice by muddying the waters like this. 

Overall, this  being agreed upon as being good research but also being divisive due to how it was communicated strongly echoes what happened [earlier this year with OpenAI's GPT2](https://www.skynettoday.com/briefs/gpt2).

## Our Perspective

OpenAI’s project demonstrates that it is possible to have robots attempt challenging manipulation tasks when the control algorithm is trained purely in simulation. The results and the paper’s technical insights may encourage and aid future robotics research in this area.

However, the publicity that the project generated tend to overtly focus on how the algorithm is “general-purpose” and the promise that the same techniques could be used to train the robot for many other tasks without much task-specific effort by humans. It is therefore important to note the numerous types of human effort and intuition that went into the system just for this particular task [^read]:

1. Highly customized hardware

   In order to control the robot hand in the real world, the algorithm needs to know the current state of the Rubik’s cube, like its current location within the robot hand and which colors are where on the cube, as well as the location of the robot's fingertips. To obtain this information, OpenAI had to use a custom-built bluetooth-connected Rubik’s cube to track the rotation of its faces, three cameras to track the location of the cube[^vision], and a motion capture system to track the locations of the fingertips. In other words, the robot hand is nowhere close to being able to solve the task in the actual real world, which doesn’t have such sophisticated experiment setups.

2. Perception and planning is solved separately from manipulation

   It is clear from OpenAI’s blog post and the paper that the work focuses on the manipulation aspect - using a robot hand to perform face rotations of a Rubik’s cube. Both perception (keeping track of the state of the cube) and planning (figuring out the sequence of face rotations to solve a cube) were treated as separate problems, and they were not learned by the proposed algorithm. This separation isn’t good or bad, but it does dampen the argument of “generality,” because for many robotic tasks, perception and planning are not solved problems, and applying the proposed techniques in other tasks may require similar levels of engineering for both.

3. Learning requires task-specific engineering of simulations

   This project shows how modern physics simulators can sufficiently capture the physics of manipulating the Rubik's; however, they are much harder to apply in other contexts (such as working with flexible materials, many objects, etc.). More generally, a caveat rarely mentioned is that it takes tremendous human effort to “massage” a problem into a form that can be tackled by RL and simulation-based training. Following this project’s approach, for each new task, a team of humans would have to carefully design a “reward function” that the RL algorithm optimizes, code the simulations in which to train the robot, build a real-world experiment setup that can mimic the simulation, and tune the training procedure until it is verified as working.
   
4. Long training time

   Despite the generally correct claim that simulation data is less expensive to obtain than real-world data for robot learning, this research outcome must have cost a lot; the final algorithm was trained using 13 thousand years of simulated data with 64 Nvidia V100 GPUs, the best commercial GPUs available, on 920 worker machines, for several months. Setting up such a compute cluster and keeping it continuously running takes a large amount of human work, and OpenAI has the benefit of having already put in that work for their past research. The amount of data and training required also incur high costs, both in terms of compute and in terms of time. This in turn greatly limits the reproducibility of the research as well as its usefulness.

   As a point of comparison, just weeks before this work, a team of 4 researchers at Google Brain demonstrated impressively efficient learning on a real robot for complex in-hand manipulation tasks:

   <blockquote class="twitter-tweet"><p lang="en" dir="ltr">Robot hand that can learn with model-based RL, in the real world, in just a few hours of training. And it turns out model-based RL can solve tasks that are very hard for model-free RL.<a href="https://t.co/b56dnqZRTa">https://t.co/b56dnqZRTa</a><a href="https://t.co/YqP48svpiB">https://t.co/YqP48svpiB</a><br>w/ A. Nagabandi, K. Konolige, <a href="https://twitter.com/Vikashplus?ref_src=twsrc%5Etfw">@Vikashplus</a> <a href="https://t.co/Yr6kAsE6vQ">pic.twitter.com/Yr6kAsE6vQ</a></p>&mdash; Sergey Levine (@svlevine) <a href="https://twitter.com/svlevine/status/1177434279795515392?ref_src=twsrc%5Etfw">September 27, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 

   The specific tasks of this work may not be as challenging as manipulating a Rubik’s cube, but works like this do bring into question the value of such long training times that and huge computational resources as the best route to general-purpose robots.

5. Large team

   The above points detail that much manual engineering has to be done before the algorithm can tackle a new task. OpenAI’s paper had a total of 18 co-authors, far more than most robotics research papers. Though some of that work was on ADR, the author contributions make clear that many worked on the aspects listed above. Seeing how algorithmically the approach is very similar to OpenAI’s prior work of reorienting a cube, and it has been more than a year since that work was publicized, it’s worth noting that such a big effort was needed to extend it to this new task. 

   <figure>
    <img src="{{ site.imgpath }}/briefs/openai-rubiks-cube/authors.png" alt="Author contribution list."/>
    <figcaption>
        Author contributions list. From the <a href="https://arxiv.org/abs/1910.07113">paper</a>.
    </figcaption>
    </figure>

With all that noted, how well does the algorithm actually do? The algorithm trained with the proposed ADR is able to successfully solve the Rubik’s cube some of the time in the real world, while one with a manually-defined DR scheme never succeeds. This of course is a positive. 

However, the success rate for solving a “fairly”[^fair] scrambled cube (“fair” being the characterization in the paper, although in their blog post and elsewhere OpenAI refers to this as “adversarial” or “maximally difficult”) is still 20%, meaning the robot drops the cube the other 80%. In addition, using a vision-only based method to track the cube’s faces instead of the custom bluetooth cube yields a success rate of 0%. This is all despite that 13 thousand years of training experience.

We point these things out not to disparage OpenAI’s achievements, but to clarify the caveats that people need to be aware of with respect to this work to be able to judge much progress towards general-purpose learning it really represents. The paper makes these points clear, but the blog post and the video don’t. Though much coverage pointed out some of the caveats, none pointed out all of them, and a fair amount of expertise in robotics and AI is needed to fully appreciate how significant they are.

The video has another problematic aspect: it includes are many non-subtle clips that connect the proposed algorithm to how children learn. While it is true that both RL and humans partly learn by interacting with the environment, RL is still an approach that crudely simplifies sequential-decision problems, makes numerous assumptions that don’t hold up well for many real-world tasks, and in general cannot be applied without extensive engineering. No expert in the field would agree that RL is equivalent to how human babies learn. While we understand that this is also not a claim OpenAI makes, including the footage of babies in the video and comparing how “[it takes children several years to gain the dexterity required](https://openai.com/blog/solving-rubiks-cube/)” to manipulate a Rubik’s cube can mislead the public into believing that this learning algorithm is far more akin to how humans learn than it really is.

This isn’t a critique on RL - these limitations are well-known within the research community, and RL is a tool in a box of many tools that roboticists use. However, given the above caveats it is not yet clear that this is a more general approach than designing or coding task-specific robots. Past attempts on applying robots to Rubik’s cubes, such as [this](https://www.youtube.com/watch?v=by1yz7Toick) or [this](https://www.youtube.com/watch?v=KVGn8tP9klI), did not require months of training and expensive GPUs, and they often achieved close to 100% success rates (when no external perturbations were present). 

Of course, the goal of general-purpose robots is not to solve Rubik’s cubes, but rather to perform a wide variety of tasks. Yet, at this moment, by looking through this particular project, it is arguable that the *marginal* cost (time, money, human resources) of using the proposed, RL-based, “general” approach in robotics for each new task is still higher than coding a specific robot program to execute that task. While this is true of most of AI research, which after all usually tackles self-contained problems meant to demonstrate the promise of a new algorithm, OpenAI’s PR-heavy approach could do a lot to make this clearer to non-AI researchers in its messaging.

## TLDR

OpenAI’s latest research demonstrates that it is possible, through carefully designing the training procedure and a lot of data and compute, to train a robot purely in simulation to perform a new challenging task in the real world. The robot, a 5-fingered hand, achieves low success rates for the benchmark task of solving the Rubik’s cube, and the experiments require expensive hardware, months of training time, and a large team of people working on various aspects of the system, which limits the work’s usefulness. While the robustness of the learned algorithm is impressive and the paper contains valuable insights for future robotics research, the messaging and coverage about this work, which often overstate the generality and the potential capability of the approach, are not merited.

[^preprint]: Meaning this paper may not have gone through peer-review by fellow researchers yet, and it has not been “printed” in an academic journal or conference proceedings.

[^RL]: Basically, this is a form of learning by trial-and-error that OpenAI and other researchers are focusing on as an avenue to developing AI algorithms that can learn to solve various problems without much human guidance. It is not a topic you need to understand to finish this article, though if you wish to learn more this [overview](https://skymind.ai/wiki/deep-reinforcement-learning) provided a good summary.

[^new]: This characterization of what’s new in this project is also stated by the team in their blog post: “The neural networks are trained entirely in simulation, using the same reinforcement learning code as [OpenAI Five](https://openai.com/blog/openai-five/) paired with a new technique called Automatic Domain Randomization (ADR).”

[^quote]: Quote from the OpenAI blog post

[^read]: Interested readers are encouraged to read the [paper](https://arxiv.org/pdf/1910.07113.pdf), which contains the following technical details

[^vision]: Results are provided in the paper that just rely on vision and not the bluetooth Rubik's cube, but the results highlighted in the blog post and media coverage rely on both, since the success rate for the vision only system is sharply below the other one.

[^fair]: As they state in the paper, “we use the official scrambling method used by the World Cube Association to obtain what they refer to as a fair scramble. A fair scramble typically consists of around 20 moves that are applied to a solved Rubik’s cube to scramble it”
