# Story concept

What a story is for, whose thinking we drew on, the shapes we compared, where we landed, and a running log of what broke on the way. Written 2026-09-24 and 25 while rewriting the alt `story-refine` skill against issues #164 to #169 in agent-ready-assessment.

## The people

All agree the written story is a token that reserves a conversation, not a document that replaces it. They differ on how much structure sits around the token and how to catch what conversation misses.

| Who | Position | Source |
|---|---|---|
| Ron Jeffries | Card, Conversation, Confirmation; the card has just enough text to remind everyone what the story is | https://ronjeffries.com/xprog/articles/expcardconversationconfirmation/ |
| Bill Wake | INVEST; a card is not a spec; mini-specs "create an illusion of completeness and substitute documentation for conversation" | https://xp123.com/invest-in-good-stories-and-smart-tasks/ , https://xp123.com/what-is-a-user-story/ |
| Mike Cohn | Template sentence plus acceptance criteria; the PO writes only what they would reject the work over; add detail by splitting, never by lengthening | https://www.mountaingoatsoftware.com/agile/user-stories , https://www.linkedin.com/pulse/two-ways-add-detail-user-stories-mike-cohn |
| Dan North | Title, As-a narrative, Given-When-Then; more than five or six scenarios means split | https://dannorth.net/blog/whats-in-a-story/ |
| Liz Keogh | Acceptance criteria are rules, scenarios are examples derived from them; you don't write down everything | https://lizkeogh.com/2011/06/20/acceptance-criteria-vs-scenarios/ |
| Gojko Adzic | Stories describe a change in behaviour, not a solution; one key example per rule | https://gojko.net/2014/02/12/user-stories-should-be-about-behaviour-changes/ , https://gojko.net/books/fifty-quick-ideas-to-improve-your-user-stories/ |
| Alistair Cockburn | The dissenter; stories have zero discipline for failure conditions; main path plus a five-minute "what could go wrong" brainstorm, under a page | https://www.humanizingwork.com/alistair-cockburn-on-use-cases-user-stories/ |
| Martin Fowler | Conversational stories; warns against "decreed stories" handed down for developers to implement | https://martinfowler.com/bliki/ConversationalStories.html |
| Jeff Patton | Story maps; a story without its place in the map loses the why | https://www.jpattonassociates.com/the-new-backlog/ |

## The shapes compared

Same need each time: the Analyzers check told a client with in-house analyzers it had "No Roslyn analyzers configured".

### Thought-leader shapes

**Jeffries and Wake: the card**

```
Analyzers row fires only when a team runs SDK defaults

Report told a client with in-house analyzers and build-enforced
severities it had "no Roslyn analyzers configured". Wrong for any
.NET 5+ project. Pass when the team opted in beyond the SDK default,
however they did it.
```

**Cohn: template sentence plus criteria**

```
As a consultant handing a client the report,
I want the Analyzers row to fire only when a team runs SDK-default analysis,
so that I never tell a team that invested in stricter rules they have nothing.

Acceptance criteria
- Passes on any opt-in stricter than the SDK default.
- Packages a framework or test SDK drags in do not count.
- Test-only references do not count.
- When it fires, the finding says "only SDK defaults" and names the cheapest way in.
- This repository passes.
```

**North: title, narrative, scenarios**

```
Title: Recognise an opt-in to stricter-than-default .NET analysis

Narrative
  As a consultant presenting the report
  I want the Analyzers check to distinguish SDK defaults from a team's opt-in
  So that the report never makes a claim the client can disprove

Scenario: Only AnalysisLevel is set
  Given a solution whose props set AnalysisLevel latest and nothing else
  When the assessment runs
  Then the Analyzers row is on the punch list

Scenario: Package arrived with a test framework
  Given the only analyzer package is xunit.analyzers
  When the assessment runs
  Then the Analyzers row is on the punch list
```

**Cockburn: lightweight use case**

```
Goal: consultant delivers a report whose Analyzers row a client cannot refute.

Main success scenario
1. Consultant runs the assessment against a client solution.
2. Tool reads project files, props, and root config.
3. Tool finds an opt-in stricter than the SDK default.
4. Report shows Analyzers Configured as passed.

Extensions
3a. Nothing beyond SDK default: row fires, body names the cheapest opt-in.
3b. Only a test project references the package: treated as no opt-in.
3c. Severity raised for a package no project references: not an opt-in.
3d. Analyzer wired through an unrecognised import: may be missed; body says so.
```

**Patton: the story on its map**

```
Activity:  Consultant defends the report in front of the client
  Task:    Code Quality Guardrails rows make claims the client can verify
    Story: Analyzers row fires only on SDK defaults        <- this one
    Story: Suggestion-severity count ignores inert rules   <- #168
```

### Jira shapes as they turn up in practice

**1. Standard product-company ticket** (the base we built from)

```
Title: Analyzers check reports false negative on .NET 5+ projects

Description
As a consultant, I want the Analyzers check to only flag solutions running
SDK-default analysis, so that I don't tell clients with custom analyzers
that they have none configured.

Background
On 9/23 the report told a client with in-house analyzers and
TreatWarningsAsErrors that they had "No Roslyn analyzers configured".

Acceptance Criteria
- [ ] Check passes when AnalysisMode is Minimum/Recommended/All
- [ ] Check passes when a non-default analyzer package is referenced
- [ ] Packages pulled in by xunit/NUnit/MSTest/EF do not count
- [ ] Test-project-only references do not count
- [ ] Finding text updated to "Only SDK-default analyzers detected"
- [ ] Our own repo passes

Notes
Research in the comments. Depends on #155, #168.
```

**2. Enterprise / consultancy ticket:** Problem Statement, Proposed Solution, In Scope, Out of Scope, numbered ACs, Definition of Done, Dependencies, Story Points.

**3. BDD-shop ticket:** User Story sentence, numbered Given-When-Then scenarios, Technical Notes. Rare in practice because it needs a tester or automation to pay off.

**4. Bug that became a story:** Steps to Reproduce, Expected, Actual, Root Cause, Fix, Priority, Affects.

Most shops run varieties of 1, 2 and 4. The originals wrote for the builder who will have the conversation tomorrow; real tickets are written for everyone who cannot.

## Where we landed

Written for the signer, challengeable by the builder. Fourteen reviews (four practitioner hats, six schools of thought, twice) converged here.

```
[Title: the behaviour change, as a verb phrase]

[Four sentences. Who stops or starts doing what once this lands. What was
observed, with the date and the words the product said. Why that is wrong.
What the product answers instead.]

Acceptance criteria
- [One rule per way the outcome is reached, at the level of what, never how.
  Only what the product owner would reject the work over. If two rules would
  be prioritised differently, split the story.]
- [When the product shows a headline, the headline verbatim. Anything longer
  is stated as what it must tell the reader.]
- [Identifiers that must not move, one line, only when a reader would wonder.]

Examples
- [Given the full context] → [what the person sees]. The reported incident
  first. Then one per rule the wording leaves open, and one where two rules
  meet. Three to six. More than six is the signal to split.

Decided
- [A choice made while refining, the alternative rejected, and why.
  Rationale only. Anything that changes pass or fail is a criterion or an
  example. At most three.]

Out of scope
- [A condition deliberately not handled, what the person sees when it occurs,
  and the key that owns it if one does.]

Open
- [Role, @name]: [the question]. If wrong: [what breaks, for whom].
  [Closed before pickup; each answer becomes a criterion, an example, or a
  Decided line. At most three.]
```

Parent and dependencies are tracker fields, not body content. Nothing sits beside the story: no provenance comment, no second document.

Rules for the skill: budget about 350 words; an Open line that changes pass or fail means not ready to pull; a non-printing sweep for "what else could be true" routes every hit to a criterion, example, Out of scope or Open and keeps its outcome; the staleness test (still true after next week's commits) and the derivation test (the builder could not get it from the repo, tests or a link); no self-disclaimer; the tracker shows who wrote it, so the story does not.

## Test case

A seed for running the story skills, written 2026-09-25 as a Slack-style dump. It carries an incident in the product's words, a real disagreement, a decision made mid-thread, the how offered twice, two genuine open questions, one false lead, and one line of noise. A good run keeps the first four, refuses the how, leaves the questions open, and drops the noise.

```
#client-northwind-assessment

[09:12] Priya (consultant, on site)
Delivered the Northwind report this morning. Went fine until the CTO got to
Existing Code Readiness. Report says "41 projects discovered, 19 without a
test project". He stopped me and said "we have 22 projects." He pulled up
the solution and he's right, 22 in the sln. The other 19 are in a folder
called /legacy that nobody has built in two years. They keep it for
reference. His words: "you graded us on code we don't ship."

[09:14] Priya
Same thing dragged Test Posture down. We gave them a D there. If you take
the legacy stuff out it's roughly a B. He was polite about it but the
number on the cover page is what he's going to remember.

[09:20] Marcus (PM)
Do we know how common this is? Is it a Northwind thing or are we going to
hit it at every client with any history?

[09:23] Priya
Third time I've seen a graveyard folder in six engagements. First time it
moved the grade this much though.

[09:31] Dana (tech lead)
Pushing back a little. Nineteen projects of unbuilt code sitting in the
repo IS an agent readiness problem. An agent will find that code, read it,
and think it's real. That's exactly the kind of thing the report should
say. I don't want us quietly excluding it and giving them a B they haven't
earned.

[09:33] Priya
Agree it's a finding. Disagree it's nineteen findings that each cost the
same as a live project with no tests. He'd have accepted "you have 19
dead projects, that will confuse an agent" as one row. He didn't accept
being graded on them.

[09:40] Marcus
So the ask is: the grade reflects what they actually build, and the dead
code shows up as its own thing rather than as a pile of missing tests?

[09:41] Priya
Yes. And the count on the cover should be a number he recognises. 22, not 41.

[09:47] Tom (developer)
Looked at it. Discovery walks the disk for *.csproj and never opens the
.sln. Easy fix, read the sln and only take what's in it. Half a day.

[09:49] Dana
Not that simple. Two of our other clients don't have a sln at all, they
build per project. And some people have multiple slns. Which one wins?

[09:52] Tom
Fair. Could do "in any sln" and fall back to disk walk when there's none.

[09:55] Marcus
Let's not design it in here. What I want to know is what the client sees.

[10:02] Dana
One thing I'll decide now so nobody asks later: we are not adding a config
file where the client lists what to exclude. Same reason as always, the
report has to be reproducible by us from a clone with no setup.

[10:05] Lena (QA)
Question. If we split these out, does a project that IS in the sln but
has never been built in CI count as live? I've seen that too.

[10:06] Dana
Don't know. Park it.

[10:10] Priya
Also, Agent Context category probably got hit too, half the legacy
projects have their own old README that contradicts the root one. Not
sure if the report counted those. Didn't check.

[10:15] Marcus
Ok. Summary for the ticket: grade on what they build, surface the dead
code as one finding not nineteen, cover number matches what the client
would say. Priya can you write it up? Dana owns the sln question. Lena's
CI question stays open.

[10:16] Priya
On it. One more thing the CTO said that stuck: "if your tool can't tell
the difference between our product and our attic, how is an agent going
to?" Might be the actual story.

[10:31] Tom
btw the Northwind run took 9 minutes, most of it in /legacy. Unrelated
but noting it.
```

What a run should do with it:

- **Keep.** The incident and its words, Dana and Priya's disagreement held in one story, the no-config-file decision, the CTO's closing line as the need.
- **Refuse.** Tom's sln fix and his fallback. Both say how.
- **Leave open.** Which sln wins when there are several, owned by Dana. Whether an in-sln project never built in CI is live, owned by nobody yet.
- **Not confirm.** Priya's Agent Context guess. The skill cannot read code, so it is an Open line or nothing.
- **Drop.** The nine-minute run time.

## Seed kinds

Not every seed is a transcript. The skill's words, the room and the thread, cover all of these; what "who said it" and "raised" mean differs.

- **Pasted record with speakers.** A Slack or Teams dump, a meeting note with names. Who said it is on the line; a question is raised by the person who typed it. Northwind is this kind.
- **AI conversation.** A chat export where one human talks to an assistant. The assistant is never an owner and never a source of a decision; what it says about the code is homework the skill was told not to do; its proposals are questions only where the human took them up.
- **Supporting documents.** A PRD, a design note, an email, a pasted report excerpt. Who said it is the author; decisions arrive as requirements without rationale, and the rationale is an Open line or nothing.
- **Tracker item with its thread.** The item, its comments, its parent's open children. The comment thread reads like a pasted record; the description reads like a supporting document.

Northwind is the only seed with runs behind it. The other kinds get seeds as client use supplies them.

## Issue log

One line per entry, in this form. Add new ones at the bottom.

```
- **Short name.** What went wrong → what we did. (fixed | open)
```

- **Spec by definition.** The skill's first sentence, "a developer alone with nobody to ask," produced 1,250-word specs by faithful execution → rewrote the reader as the signer who can sign and the builder who can challenge. (fixed)
- **One check per claim.** The template's Checks rule produced 13 to 20 scenarios per ticket → examples capped at three to six, the rest derive into the test file. (fixed)
- **Self-disclaimer.** Every ticket ended with "if the code contradicts a line above" → deleted. (fixed)
- **Verbatim finding copy.** Full finding Body frozen on the ticket went stale at the PR → Title verbatim, Body stated as what it must tell the reader. (fixed)
- **Allowlist on the ticket.** Seventeen package names listed as criteria → the policy on the ticket; data a rule turns on is a short table or a split signal. (fixed)
- **Constraint with PR state.** "PR #155 (open, unmerged)" was false the day it merged → became a Depends line, then a tracker relation. (fixed)
- **Docs section per ticket.** Every Check story repeated "update the checks reference" → belongs in AGENTS.md as a rule for every Check change; not yet written there. (open)
- **Conditions section.** Cockburn's failure-condition list was voted out five to one as a staging area exempt from the derivation test → kept as a sweep the skill runs and never prints. (fixed)
- **Decided leaking criteria.** "Source generators count" changed pass or fail but sat under Decided → Decided is rationale only. (fixed)
- **Parent as body content.** "Parent: none" printed on every story and spawned an epic Open line each time → Parent is the tracker field; the template prints nothing. (fixed)
- **Deferred label.** "Parent: none, deferred per @name, date" turned a room decision into an edit log → removed. (fixed)
- **Attribution asks.** Template's "by whom" made agents name people from git blame → removed the ask, added the fact that the tracker shows the author. (fixed)
- **Provenance comment.** A dated comment carried facts the story rested on, a second document stale after the next commit → deleted and the rule removed; the builder looks it up. (fixed)
- **Depends on in body.** A relation written as text → written to the blocked-by relation; GitHub refuses PRs there, so PR dependencies are said in the room and not written. (fixed)
- **Retention rule.** "A line already in the item stays" pulled the old tickets' mass through every refine → retention applies only to items already in the shape; anything else is a create. (fixed)
- **Shows versus template.** The repo's extend file said every field verbatim while the template said headline only → precedence sentence (template, extend file, preset) and Shows cut to headline field names. (fixed)
- **Lives in code.** "The list lives in code" was false before the code existed and left #168's 23-row table homeless → restored the 0.12.1 data rule. (fixed)
- **Sweep routing.** Three of five sweep hits changed their answer when placed → a routed hit keeps its outcome or becomes an Open line. (fixed)
- **Cached install.** Edits without a version bump never reached installed copies → bump on every change. (fixed)
- **Hat words.** Old tickets say Product and Developer, the preset says Business and Tech Leadership, agents guessed → no mapping yet. (open)
- **Headings.** Template shows plain text, #165 used bold, #167 used ##, agents copied whichever they saw → template does not say. (open)
- **Caps read as targets.** Six examples, three Decided, three Open on every draft, budget never reachable → either one budget with no section caps, or no numbers and a script. (open)
- **Subagent writes refused.** The permission layer blocked gh issue edits from nine of ten subagents with no visible difference in the tenth → unexplained. (open)
- **Tempt test cut.** #169 lost a coverage-gate constraint as "how" and the build could land where coverage excludes → one allowed line for a repo rule this change would tempt breaking, not restored. (open)
- **Sibling ownership.** #168 took the test-project question but nothing told the skill to remove it from #165 → homework reads sibling Open; write does not edit siblings. (open)
- **No incident.** #164 came from a claim, not an observed report, and the opener rule assumes an incident → allow an observed claim. (open)
- **Split-or-Open loop.** Over a cap with Open full and no runner present has no exit → show the draft with the split named and write nothing. (open)
- **Headline with no headline.** "The headline verbatim" had no case for a Finding that does not exist yet, so both skills invented one → when the product does not show it yet, the line says what it must tell and the words are the builder's. (fixed)
- **Parenthetical attribution.** "(Dana)" and "(Priya)" appeared on Decided lines despite the tracker-shows-author fact → the Decided bracket says the thread holds who said it. (fixed)
- **Unchecked claim as Example.** Priya's README guess became an Example with an outcome → a claim the thread leaves unchecked is an Open line. (fixed)
- **Invented owners.** A question nobody raised was handed to the PM → a question the room did not raise is unassigned. (fixed)
- **Out of scope as junk drawer.** The nine-minute run time landed there as "deliberately not handled" → Out of scope is a case the story could have handled and does not. (fixed)
- **The how through a criterion.** story-refine wrote "only when a solution file lists it" as a rule and the noun list never caught it → the one-way test replaces the noun list and the two old tests in story-refine. (fixed)
- **Homework findings kept off the story.** story-refine found the quoted report words match nothing the tool prints and left it in its notes → a homework finding that contradicts the seed is an Open line. (fixed)
- **Opener grew without a count.** Removing "why that is wrong" did not shrink the opener; zero of ten Sonnet runs kept it to four sentences → the sentence count is back on story-create. (fixed)
- **Out of scope survived as a junk drawer.** "A case this story could have handled" still took the run-time aside in six of ten runs → the section is deleted from story-create; a case not handled is an Open line or nothing. (fixed)
- **Invented filenames in examples.** Four of ten runs named a solution file the thread never mentioned → an example names nothing the thread did not name. (fixed)
- **The how from the seed.** story-create wrote the developer's proposed mechanism as a rule twice, from the transcript rather than code → a way of building proposed in the thread is a question, not a rule. (fixed)
- **The one-way test does not fire after reading code.** Four of five story-refine runs wrote the mechanism as criterion one and called it settled by the record → story-refine moved out of the plugin to `.project/archive/skills/` on 2026-09-25, before the builder's pass exists, so it cannot be invoked by mistake; the pass is still unbuilt. (fixed)
- **Example decides an Open question.** Three of five runs showed the no-solution outcome as an Example while Open still asked it → the Examples bracket says never an outcome an Open line still asks about, and the Before-showing step checks it. (fixed)
- **Raised-but-unowned owner invented.** Three of five handed Lena's parked question to Dana → the Open bracket covers a question raised and left with nobody. (fixed)
- **Opener written for the consultant.** Fifteen of fifteen create drafts opened with the consultant's problem, not the client's need in the CTO's words → the opener bracket asks whose need, the person the product serves, in their words. (fixed)
- **Second pass predicted the score.** Two-pass runs scored 4, one-pass runs 3, and nothing asked for a second pass → a Before-showing step with a script for the countable checks and five questions for the rest. (fixed)
- **The how as before-state.** Two of five runs wrote the developer's diagnosis of today's code into the opener as fact, and all five wrote "not everything on disk" into a criterion; the routing rule covered proposals only → the rule also covers a way it is built today. (fixed)
- **Decided carried a criterion's why.** Three of five runs restated the one-finding-not-nineteen rule under Decided to carry its reason, since criteria have no slot for a why → the Decided bracket leads with what was not done. (fixed)
- **Third Example invented.** Both runs that wrote three Examples invented a legacy project with tests, which the thread contradicts; runs with two were clean, and Fill still said "three lines" against the template's "up to three" → the Fill sentence and the "one per rule the wording leaves open" clause are deleted. (fixed)
- **Opener's fourth sentence read as today.** Two of five read "what the product answers instead" as current behaviour → the bracket says "once this lands". (fixed)
- **Names in the opener.** Four of ten runs named the consultant in the opener and one named the developer in Decided; the script catches handles, parentheses and timestamps, not a bare name → story-review reads the seed and strips them; the script stays draft-only. (fixed)
- **Noise via Decided, again.** One of ten wrote the run-time aside as a Decided line saying it was left out; two of fifteen across rounds, both through Decided → check.py flags omission verbs under Decided. (fixed)
- **Before-state in the negated clause.** Nine of ten criteria said "not everything found on disk"; the routing clause does not fire on a negation → story-review cuts the clause; a line with nothing left moves to Open. (fixed)
- **Turned-down proposals not recorded.** All ten caught the decision announced as one, four caught the pushback on silent exclusion, one caught the pushback on solution-only → a proposal the thread turned down is a Decided line. (fixed)
- **Criteria wider than the thread.** Four of ten widened the count to every field or every category → the criteria bracket gains "nothing named that the thread did not name". (fixed)
- **per-Name false positive.** Three firings across rounds, all on product nouns → the rule is deleted. (fixed)
- **Owner by answering.** One run handed the parked question to the person who replied "don't know" → story-review: answering or raising is not being handed it. (fixed)
- **Ten-run gate retired.** One synthetic seed and a spread condition measured Sonnet's wobble, not the story's fit for a client → three-run smoke on Northwind after any skill edit, and a corpus of client uses where the runner's edits before the write are the measure. (decided)
- **Reviewer rewrote a real headline.** One of three smoke runs had story-review change "Projects scanned", verified in generated reports, to the transcript's paraphrase "projects discovered"; the reviewer reads only the seed → it never changes a quoted string, and a headline it doubts goes under Could not fix. (fixed)
- **Fix not carried across lines.** One reviewer cut "Overall Score" from a criterion and left it in the opener, naming the gap instead of fixing it → a fix is carried to every line that repeats the words. (fixed)
- **Repo instructions leaked into a story.** One smoke draft's Decided reason was "Checks carry no suppression mechanism", this repo's AGENTS.md and nothing the room said; only the composer's grounding pass caught it → the Decided bracket says "in the thread's words" and story-review drops a reason the seed does not hold. (fixed)
- **Product words cut as ungrounded.** The composer dropped Sub-Score and Punch List as absent from the seed, the same gap as the headline in the first smoke → create hands story-review the product words it verified, and the review never cuts them. (fixed)
- **Same claim, different words.** A reviewer cut solution-membership from a criterion and left it in the opener; "repeats the words" missed twice in four runs → "makes the same claim". (fixed)
- **Possessive read as assignment.** "Lena's CI question stays open" handed Lena her own question in two runs across rounds → a question called someone's because they raised it is not handed to them. (fixed)
- **Missing Open line invisible to the review.** One of five smoke runs on 0.15.2 dropped the solution-file question the room assigned by name; every review check inspects lines present, none asks whether each question the seed left open is under Open → logged, once; a completeness question is one sentence if it recurs. (open)
- **"Every Sub-Score" survived review.** Two of five widened the grade to every category where the seed named two; one reviewer narrowed it, two did not; the seed says "the grade" → logged as a seed ambiguity, not a rule miss. (open)
