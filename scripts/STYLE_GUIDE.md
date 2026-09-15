# Last Week in AI — writing style guide

## Voice

Connect and synthesise; never editorialise.

Good — causal, contrastive and topical links between paragraphs:
- "The verdict clears the path for what could be one of the largest IPOs in history: …"
- "Meanwhile, Google DeepMind released a complementary framework …"
- "Despite broad platform support, experts are raising serious concerns."
- "Both efforts collectively signal a new phase, though Terence Tao cautioned that …"

Banned — opinion and self-reference: "the defining story of the summer", "what made this
remarkable", "as we covered above", "this post".

Every judgment or hedge belongs to a named person or publication. A hedge with no owner gets cut.
Never attribute your own inference to an outlet: if you counted it, say it plainly or drop it.

## Sentences

- Mean ~30 words, hard ceiling 45. Long means densely subordinated, not runaway.
- One idea per sentence. A sentence carrying a mechanism, a number, a date and a quote should be
  two or three sentences.
- Short sentences are a reversal device — about one per issue.
- **Avoid the colon-splice tic.** "Framing clause: full independent clause with dense facts" is fine
  occasionally (roughly 1 sentence in 10) and grating at 1 in 5. It makes a sentence feel long and
  complex without being long. Usually the fix is a full stop: "Offensive work reached unskilled
  hands. OALABS researchers reported …" — the short sentence gives the reader somewhere to land.
- Don't front-load long subordinate clauses that delay the subject. Lead with who did what.
- Em-dashes carry appositive facts ("— OpenAI's transition to a for-profit structure —"), not
  dramatic pauses.
- Exact, unrounded numbers: "9 out of 353", "$53,000 per violation". Never "several" or "roughly"
  when the source gives a figure.

## Weeklies vs catch-ups

A weekly digest is news: blow-by-blow detail on the headline event is the value, because the reader
has not seen it yet.
A catch-up covering months is a retrospective: the reader lived through the headlines and wants
what it amounted to, not a chronology of events they half-remember.

In a catch-up, summarise freely. Say what happened and what came of it; skip the sequence of steps
in between. Keep only the specifics a reader would repeat to someone else — an unskilled attacker
breaching 14 companies with off-the-shelf agents, a model pulled worldwide because nationality
could not be verified. Drop the rest, including detail that was genuinely interesting the week it
happened.

## Structure of an entry

1. Orient first — the SHAPE of the story, not a preview of it. Say which way things moved and who
   moved them. Do NOT list the dated beats the body is about to deliver: an opening that names
   June 12, June 30 and August 4 with their specifics turns into a table of contents, and the
   reader meets the whole arc twice before learning anything new. Shape belongs up front; dates
   and detail belong below, once.
2. Then detail, ordered as the argument needs. Don't default to leading with the oldest item.
3. Bullets for piles and for sequences. Two shapes call for a lead-in plus bullets rather than
   narrative prose:
   - **Parallel announcements** — when an entry is really N releases or N deals side by side.
   - **Dated sequences** — an incident, an investigation, a legal fight. Judgment, not a
     threshold: a long chronology usually wants bullets, but so does a short one whose beats
     contradict each other on their face (a lab declining to confirm on Monday and confirming on
     Tuesday reads as self-contradiction in prose and as a sequence in bullets).
   Prose buries the order of events; bullets make it legible. That is a fidelity gain as much as a
   readability one: a chronology written as prose invites the writer to compress "X happened, then
   Y happened" into "Y after X," which asserts a causation the source may not support. Dated
   bullets force the sequence to stand on its own and let the reader draw the link.
   Bullets are for the chronology, not the whole entry — keep the orienting paragraph above them
   and the analysis below.
4. Cut procedural minutiae that no reader will carry: nested agency deadlines, the chain of
   designations behind a policy, who handed negotiations to whom. Keep what changed, drop the
   machinery.
5. Stay on the headline event. Keep the background needed to follow it — a short recap of how a
   dispute began is fine — but cut adjacent events (another incident, another report, reactions to
   a different announcement) and secondary detail within the event: benchmark lists, system-card
   findings, a minor figure's affiliation, the least consequential beat of a timeline. Exact is
   not exhaustive.
6. Close on a sourced consequence. Never close on a tally you computed yourself ("four
   organizations in three weeks") — that is authorial voice wearing a fact's clothes.

Paragraphs must connect. Five self-contained fact-dumps in a row is a list, not writing.

Keep paragraphs short: about three sentences, never more than five. A one-sentence paragraph is
fine; a seven-sentence one is a wall. Split where the topic turns.

## Emphasis

Bold almost nothing. A proper noun is already marked by its capital letter; bolding it adds no
information and speckles the page. Company names, model names, product names and figures all read
fine plain.

- The only routine bold is the leading date in a bulleted list item, which is navigation rather than
  emphasis.
- Otherwise bold only where a reader would genuinely miss the point without it — rare enough that
  you should be able to justify each instance.
- Never bold: company names, model or product names, bare numbers, percentages, dates in prose, or
  multi-word phrases.

## Sourcing

- Every claim traces to an article you actually read. A headline supports far less than it appears
  to, and truncated source text produces assertion-only writing.
- URL slugs are evidence: `…-win-the-ai-race-shazeer-jumper-…` confirms coverage the headline
  omits. Check the slug before calling something unsupported.
- Paywalled is not unusable. Find another account of the same event, take the detail from there,
  and still cite the original. For regulator actions (FERC, DOE, BIS, ERCOT) the agency's own
  docket is public and usually better than the news write-up.
- Sourced or cut, never hedged. "Reportedly 179 signatories" launders an unverified number into
  print. A vaguer true sentence beats a precise unsupported one.

## Failure modes to check for by name

- **Fabricated precision** — vague source language sharpened into false specificity ("on the order
  of tens" becoming "10 to 25"). The most common error; it survives review because it reads
  authoritative.
- **Invented attribution** — crediting a claim to the outlet that ran the story rather than the one
  that reported it, or to an outlet that never made it.
- **Corrective passes introducing new errors** — an edit made in the name of accuracy still needs
  verifying. This is the single most reliable source of late-stage mistakes.
- **Cuts breaking facts** — a trimmed qualifier leaving a claim overstated, or a pronoun
  re-pointing at the wrong subject.
- **Tone rules over-applied** — banning authorial presence so hard that transitions disappear and
  paragraphs stop connecting. The ban is on opinion, not on logic.

## Mechanics

- arXiv IDs encode year and month only: `arxiv.org/abs/2606.19980` is June 2026, with no day. Never
  print an exact date for an arXiv item.
- Source lists run chronologically, one distinct event per entry. Two articles on the same
  announcement is padding.
- Everything falls inside the covering window. Earlier items may appear as background, labelled as
  such, and must never lead.
- Images: prefer real research figures and press photos over stock and conceptual illustration;
  credit the source beneath. `og:image` works for most outlets — NYT, Bloomberg, WSJ and Reuters
  block scraping, so pull from an accessible source covering the same story.
