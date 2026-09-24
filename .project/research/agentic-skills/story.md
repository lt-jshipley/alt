# Story / ticket: research notes

Started 2026-09-09. Research behind the roadmap's story / ticket skill: what a story should carry, where it comes from, and what makes one ready. The five books in the reading plan were read 2026-09-18, one agent per book; what each says, what a story carries and never carries, what ready means, and where they disagree are written below.

## References

Local copies are markdown files in `~/Downloads/books/`, one file per book except The Product-Minded Engineer, which is a folder of chapters. Primary first. Each line says what the book has an opinion on here.

- **User Story Mapping**, Jeff Patton. A story is a placeholder for a conversation, not a spec: who, what, why, acceptance criteria, and its place on the map.
- **Lean UX**, Jeff Gothelf and Josh Seiden. The hypothesis format: we believe X for Y will achieve Z, and we will know when W. The "you'd know it was wrong if" line. The local copy is the 2013 first edition: no canvas, and the template is feature-first, not the outcome-first wording of later editions.
- **Continuous Discovery Habits**, Teresa Torres. Where a story comes from: it traces up to an opportunity and a desired outcome, and names the assumptions it rests on.
- **Inspired**, Marty Cagan. What ready means: value, usability, feasibility, and viability risk are settled in discovery before a ticket exists. The local copy is the 2008 first edition: three risks, no business viability, and it scopes itself out of custom software work.
- **The Product-Minded Engineer**. What an engineer should expect a ticket to contain, and what to ask when it is missing.

In our other repos, read 2026-09-09: `~/Development/agentic-temp/summary.md`, the `/ticket` section of the earlier suite. One template for every issue type, silent homework first (code anchors, area, duplicate and parent lookup), then only genuine gaps asked one at a time with flag-for-later always allowed; on re-run it reconciles by section delta. Engagement work; confirm provenance before reuse.

Considered and not listed: Accelerate (batch size only), Empowered, Evidence Guided, Lean Analytics, Measure What Matters, The Lean Product Playbook, The Lean Startup, Thinking in Systems. Their opinions land on epic or triage. The Design of Everyday Things and The Startup Way are not about these artifacts.

Related in this repo: `grill-me.md`, examine's readiness read and team-questions list, which a story skill would consume or produce. `skill-development.md`, the considerations every alt skill answers. `orient.md`, how a skill learns what kind of project this is and where its facts live. `brief.md`, the unit of work a story is shaped into.

## Reading plan, 2026-09-18

Which references earn a dive for this skill, decided in conversation 2026-09-18. A book earns a full read when it would change the skill's shape; a chapter when it settles one question; nothing when a stronger book on the shelf already says it.

- **Read in full.** User Story Mapping: the only book about the artifact itself, and the answer to what a story never carries. Continuous Discovery Habits: where a story comes from, and the one book that touches story, epic, and triage. Inspired: what ready means, the definition examine's close gestures at without a source.
- **One chapter.** Lean UX, the hypothesis statement: the "you'd know it was wrong if" line examine dropped for weight comes from here. The Product-Minded Engineer, the ticket chapters: the only book written from the developer's side, which is who runs the skill.
- **Hold while reading.** The books say what a story should be in a product org with discovery and a product team. The earlier suite said what a skill does to a record in a shop with neither, which is most engagements. Nothing on the shelf speaks to the research preset, and business is thinly covered.

## What each book says

Read 2026-09-18, one agent per book, whole book unless the reading plan says a chapter. Quotes are from the local copies; chapter names are the copies' own.

### User Story Mapping

A story is a token for a conversation, and the title is the one required field.

- "The only thing that's required on your card is a good title. A good title is the most valuable part of your story." Titles are "short verb phrases that describe what people do"; referring to stories by number "is a sure signal you haven't chosen a very good title" (Ch 8, "What's Really on a Story Card?").
- Description in a sentence or two: who, what, why. His own card is title, then `Who: / What: / Why:` with blank lines "because I'll want to specifically name all the different whos" (Ch 7, "Template Zombies and the Snowplow"). "Please don't just talk about 'the user.' Be specific." "Keep poking it with the why stick."
- Confirmation answers two questions: "If we build what we agree to, what will we check to see that we're done?" and "When it comes time to demonstrate this later, how will we do that?" The second "often reveals some holes" (Ch 6). "Speak in examples: exactly what data might be entered, exactly what users would see" (Ch 16).
- Size is a budget by comparison, "about the same as that feature for commenting we built last month"; "accurate estimate" is an oxymoron (Ch 4, Ch 7). Dev-sized is "one to three days" (Ch 12). Story points never appear.
- Also on the card: "Identify your questions and discuss how important they are to get answered before you build software. Decide who'll do the legwork" (Ch 7); "What happens when things go wrong? How do they meet their needs today?"; post-release metrics, because "outcomes are never insured" (Ch 18); "a note of who was in the conversation" (Ch 7, "Create Vacation Photos"). Leave whitespace for what the conversation adds.
- What it is not: "Stories aren't a written form of requirements. The word requirements actually means shut up" (Read This First). "The card's just a token. No one confuses the cards with a book" (Ch 8). "Handing off all the details about the story to someone else to build doesn't work" (Ch 9). "I don't tell stories about cups of sugar and flour": dev tasks are the team's plan, made after the conversation (Ch 10). "As a product owner, I want you to build a file uploader so that the customer requirements are met. Nasty things like that" (Ch 7). A one-to-five-page story narrative was abandoned because delivery "largely ignored" it (Ch 16).
- Ready is the output of "the last best conversation": three to five people, someone who knows the users, "one or two developers who understand the codebase," and a tester who "asks the tough questions," ending in "right-sized stories supported by lots of extra documentation and models, and by acceptance criteria" (Ch 16, Ch 12). Failure signs: "one person describes what's required and everyone else listens"; "we focus only on acceptance criteria and not telling the story about who does what and why."
- Where it comes from: opportunity, discovery, a release backlog sliced by target outcome, the workshop, build, learn. "Focusing on specific target outcomes is the secret to prioritizing development work" (Ch 2). Written without the map a story loses its who, its parent goal, its slice's outcome, and "the necessary stuff in between." Bounded: "map a little ahead of where the feature begins and a little beyond where it ends" (Ch 17).
- His own concession for small work: "Don't sweat the small stuff. I don't have an opportunity discussion, or pull together a group to do product discovery. I'll get them into a current release backlog and then as early as possible workshop them" (Ch 17). The as-a-user template is a "snowplow," a learning aid that becomes a "template zombie" when forced; backend stories need not fit it. Trackers are an "information icebox" (Ch 8). "Requiring a single product owner to write all of the stories doesn't work" (Ch 12).

### Continuous Discovery Habits

Never mentions tickets, story templates, or acceptance criteria. What it says about the unit of work is implicit, except Chapter 14, written to a developer handed a feature.

- The tree: "The root of the tree is your desired outcome. Next is the opportunity space, the customer needs, pain points, and desires that, if addressed, will drive your desired outcome. Below the opportunity space is the solution space. Below the solution space are assumption tests" (Ch 2). A solution should be able to say "This solution will address the target opportunity because... Addressing the target opportunity will drive the desired outcome because..." and "each inference is an assumption that you can test" (Ch 9).
- Without the trace: "we are simply guessing again" (Ch 2). A single feature becomes a "whether or not" decision, "perhaps the most common mistake product trios make." "You are never one feature away from success" (Ch 7). An opportunity with only one possible solution is a solution in disguise; ask "If you had that feature, what would that do for you?" (Ch 6).
- Five assumption kinds: desirability, viability, feasibility (including "will our legal or security team allow for it"), usability, ethical, "is there any potential harm?" (Ch 9). Expect twenty to thirty per idea, "most of them will be harmless"; test only the two or three leap-of-faith ones. Success criteria are counts set before the test, "at least 3 out of 10," never percentages (Ch 10).
- No readiness gate. "You are never done with discovery; discovery feeds delivery and delivery feeds discovery" (Ch 11). "We stop testing when we've removed enough risk and/or the effort to run the next test is so great that it makes more sense to simply build the idea" (Ch 10).
- The minimum for a feature team (Ch 14, "Work Backward"): ask "If our customers had this solution, what would it do for them?" and "If we shipped this feature, what value would it create for our business? Refine your answer until you get to a clear metric." Story-map the feature to find its assumptions: "Even if you don't have the infrastructure to test your assumptions, being aware of your assumptions will help you notice the evidence around you." Document expected impact, instrument for it, review after release. Proxies for customer access: support tickets, forums, "someone who is similar to their customers."
- Against: scoring formulas, "once we mathematize this process, we'll stop thinking" (Ch 7); outputs dressed as outcomes, "Launch an Android app"; stakeholder requests in the development backlog rather than an idea backlog (Ch 13); the PM-owns-problem, engineer-owns-solution split, "the product trio should be responsible for both" (Ch 2). "Language is vague. Drawing is more specific" (Ch 4). "The fruit of discovery work is often the time we save when we decide not to build something" (Ch 12).

### Inspired, first edition

Two stages: "figuring out what to build, and building it" (Ch 12). The unit is a release and the spec is a prototype; the book says it is not for custom software.

- Ready: "three important types of validation that you need to perform before you hand over a final product specification to the engineering team: feasibility testing, usability testing, value testing" (Ch 21). "You don't actually have a spec worth handing over to engineering until your prototype passes these two tests" (Ch 18), plus "a detailed estimate that they can commit to" (Ch 20). Business viability lives in ten opportunity questions: what problem, for whom, how big, "how will we measure success," alternatives, why us, why now, go or no-go (Ch 11).
- The cost of skipping it: "using the engineering organization to build a very, very expensive prototype, and they use their live customers as unwitting test subjects" (Ch 12). "Once the real engineering begins, a special type of inertia sets in" (Ch 21).
- What engineers receive: behavior, not implementation, "the functionality and behavior of the product to be built, and not how it will be implemented" (Ch 1). The prototype carries most of it; what it cannot: "business logic, the release requirements (reliability, performance, scalability), platform delivery requirements," and use cases for the main flows, kept on a wiki that tracks "the history of decisions" (Ch 18). Constraints named at the opportunity stage: integrators, extensibility, branding (Ch 11). Persona as the tie-break: "If this feature is critical for 'Mary' then put it in, if it's for 'Sam' then it's out" (Ch 17). Agile version: "replace heavy PRDs and functional specs with prototypes and user stories" (Ch 26).
- Leave out: the fifty-page document "few will read and is impossible to test" (Ch 18); P1/P2/P3 on the final spec, "yank all those annotations; if you remove a leg that dog won't hunt" (Ch 20); implementation detail from the PM (Ch 8); a customer's ask mistaken for a requirement, "one of the surest ways to derail a product company" (Ch 32).
- The engineer: "you are responsible for defining the right product, and your engineering counterpart is responsible for building the product right" (Ch 5). Engineers in discovery from the start, "in front of users," pushing back on feasibility and on premature estimates, "anything beyond small, medium or large effort is not fair to engineering" at the opportunity stage (Ch 14). When the PM is weak, "sometimes a lead engineer steps in and performs the true product management function" (Ch 2).
- Minimum even when the decision is handed down: "doing a lightweight and quick product opportunity assessment is still valuable; at least you will have a clear understanding of your objective" (Ch 11). For any decision: the exact problem, the exact persona, the goals, their order (Ch 13). "By far the most common reason product managers request changes to the spec is a consequence of not really thinking through the requirements in the first place" (Ch 20). The spec is for seven audiences, not one (Ch 18).

### Lean UX, first edition, chapter 3

The hypothesis is a unit above the story, and the story keeps its classic form.

- General form: "We believe [this statement is true]. We will know we're right/wrong when we see the following feedback from the market: [qualitative] and/or [quantitative] and/or [KPI change]." Product form: "We believe that [building this feature] for [these people] will achieve [this outcome]. We will know this is true when we see [this market feedback]." The last line "is the statement that determines whether your hypothesis was true." It "takes much of the subjective and political conversation out of the decision-making process" (Ch 3, "Hypotheses").
- Rules: one outcome per statement, "split the hypothesis into two parts" otherwise; "none of your metrics will be meaningful if you don't have a benchmark in place prior to writing your hypotheses"; "it's not all numbers," qualitative signals count.
- Outcomes versus outputs: "Features and services are outputs. The business goals they are meant to achieve are outcomes" (Ch 2). "Too often our design process starts when someone has a feature idea, and we end up working backward to try to justify the feature" (Ch 3).
- Assumptions are declared from a problem statement whose third element is "an explicit request for improvement that doesn't dictate a specific solution," prioritized by "how bad would it be if we were wrong about this" against how much is understood, then rewritten as hypotheses.
- Placement: "User story: the smallest unit of work expressed as a benefit to the end user. As a [user type] I want to [accomplish something] so that [some benefit happens]" (Ch 7). Hypothesis, then theme, then stories written together at planning. "Determining outcomes is a leadership activity." For output-shaped work, "lead with conversation, and trail with documentation" (Ch 8).

### The Product-Minded Engineer

Drew Hoskins, 2025. The one book on the shelf written to the developer, and the only one that mentions tickets.

- The ticket is a slice of a scenario: "you can turn each requirement into a ticket; Jira has a Story ticket type, each of which corresponds to one of these user-centric requirements," and a requirement is "a snippet of one of our scenarios" (Ch 7). Tickets are tagged to persona, north-star scenario, edge case, milestone. "Stories are harder to misinterpret than lists of abstract requirements."
- Form: "[User] can [action] so that [motivation]." The motive is the root: "'Eliana wants to look at her recent orders.' That's not her goal; it's a means to an end. But what end?" (Ch 1). A good requirement is "concrete enough to communicate clearly and unambiguously," expresses intent so "an engineer can check back in" if the stated way is intractable, and "still allows the engineers some design latitude"; when clarity forces prescription, give an example (Ch 7).
- Failure scenarios: the tech lead "asks her to list failure scenarios as well; Elise has shown only the end" (Ch 3). "Look for skipped steps and edge cases" (Ch 1). "Diagnostics may be the most important interface of your product" (Ch 3).
- The whole journey: "Tell the complete story. Don't just focus on the feature you're adding" (Ch 1). A feature owner owns discovery, understanding, and usage; "a classic blunder is to leave out a discovery mechanism" (Ch 2).
- Also: a value metric, "if you can't name one, be concerned" (Ch 5); nonpersonas, "say whom you're not targeting" (Ch 6); risks as an "antitheses" section (Ch 7); NFRs "justified in terms of user impact" (Ch 9); acceptance as a scenario test, "our product requirements made permanent" (Ch 4); "link out to your interview transcripts in case people question how you came up with them" (Ch 6). Priority is P0, "can't ship or get user feedback without it," P1 stretch, everything else blank; "ratholing on whether an item is P2 or P3 is a good way to waste an hour" (Ch 7).
- The questions to ask: "what if X happens? what if the user was Y?"; "What happened before, and what brought the user to that moment? How did they learn what to do? What happens next?"; "But what end?"; "What are you really trying to do?" (Ch 1, Ch 5). Not "should we add it?" but "when should we add it?" (Ch 8). "If I get stuck, or find myself making things up completely, I may need to talk to users or look at metrics, talk to a PM, or consult other teams" (Ch 1).
- Ownership: the engineer owns error messages and edge cases, tests and instrumentation, product architecture and NFRs, and the how inside the latitude. Push back by story, not by cost: the engineer who "pushes back, noting that this button will double the time-to-implement" was wrong; the one who wrote a before-story got a "look into it" three weeks later (Ch 1). When the requirement cannot be met, "check back in and look for backup solutions," never pivot silently (Ch 7).
- Not: "don't jump straight to a solution, and don't assume that you're done when the first version ships" (Preface). "When in doubt, leave it out"; "if you can't find time to write even a test, it may be a bad smell" (Ch 8). Living documents, never a contract. Juniors "are prone to just think about the size of the production code in the happy path" (Ch 7); they escalate through the tech lead or PM, and the code-review prompt "list failure scenarios" is the model.
- Two rules for any tool: "The quality of a product interface can be measured by the relevance of the questions it asks of its users," and when either default is unsafe, offer no default and force the choice (Ch 8). "Don't ask people to open tickets or follow any kind of process. This puts up hoops" (Ch 4).

## What a story carries

The consensus of the five, ordered by how many agree and how cheap the item is. Each names its sources.

- A verb-phrase title, the only required field. Patton. No book disagrees.
- A specific who, never "the user," and all the whos. All five. Hoskins and Cagan add who it is not for.
- A root why, poked until it is a goal and not a means. Patton, Hoskins, Torres' two work-backward questions. A fact when anyone upstream knows it; a routed question when not.
- Intent with latitude: what and why, never how. Patton, Cagan, Hoskins. An example where clarity forces prescription, marked as one.
- Failure scenarios and edge cases, listed. Hoskins, Patton. The strongest developer-side item.
- Acceptance as two questions, in examples: what will we check, how will we demonstrate it. Patton; Hoskins as a scenario test. Torres never mentions it.
- The complete journey around the feature: before, discovery, after. Hoskins, Patton.
- Its parent: the goal above, the slice's outcome, the north-star scenario. All five. In a tracker, the epic link and the epic's outcome line, read up one level.
- Open questions with an owner and who does the legwork. Patton. Examine's team list.
- Constraints the UI cannot show, only when real: business logic, performance, platform, integration. Cagan, Hoskins.
- One outcome line, or an honest "unmeasured." All five want a signal; Lean UX says without a benchmark it is theater; Torres says counts, never percentages.
- Size by comparison, as a budget not a commitment. Patton; Cagan's S/M/L before a solution exists. Story points appear nowhere.
- Pointers to evidence and decisions, never the content. Hoskins, Cagan.
- Who was in the conversation. Patton.
- Whitespace: an empty field is not a deficiency. Patton.

## What a story never carries

No dissent among the five.

- The spec or the requirements. Patton, Cagan.
- The implementation recipe. Patton, Cagan, Hoskins.
- A commitment. Patton.
- The writer's own perspective. Patton.
- A solution when the need is unknown. Torres.
- A long narrative. Patton.
- A customer's request verbatim. Cagan.

## What ready means

The books split, and what they share is the finding.

- Patton: the output of a three-to-five-person story workshop, right-sized, with acceptance criteria.
- Cagan: a prototype that passed value and usability tests plus a committed estimate, at release level, not story level.
- Torres: no gate exists; stop when enough risk is removed or the next test costs more than building.
- Hoskins: one complete scenario, persona confirmed in the target audience, one metric, a failure list, one test.
- Lean UX: a hypothesis with a benchmark and one outcome, above the story.

Shared: ready is shared understanding, never field completeness. This is the earlier suite's "grade the record for workability, not completeness" from the other side, and examine's four reads already sit here.

## Where they disagree

- **Level.** Lean UX puts the hypothesis above stories in a theme; Torres puts outcome and assumptions on the tree; Cagan's unit is a release. Patton and Hoskins put a metric on the card. The likely resolution: outcome, hypothesis, and assumptions are epic content, read up by a story skill and never asked of the developer at story level.
- **Templates.** Patton: the as-a-user form is a snowplow and a template zombie when forced, and backend stories need not fit. Hoskins gives a form and offers a second for platform work. The earlier suite's one template for every issue type is in tension with Patton.
- **Priority.** Hoskins marks P0 for the current milestone and leaves the rest blank; Cagan removes P1/P2/P3 from the final scope. Both contradict a priority field on every ticket.
- **Who owns the problem.** Cagan splits PM owns what, engineering owns how. Torres rejects the split. Hoskins has engineers co-author the thesis. Patton says a single author for all stories does not work.
- **Acceptance criteria.** Patton and Hoskins want them, in examples or as a test. Torres has none; her only criteria are assumption-test counts set before the test. Patton warns that writing them substitutes for the conversation.
- **Scoring.** Torres rejects formulas outright. Triage's concern, and it will meet Gilad there.

## What cuts against the tool itself

- Every book distrusts the written artifact. Patton's tracker is an information icebox, Cagan cannot execute paper, Torres says drawing is more specific than language. A ticket-writing skill is the thing they warn about, so the ticket has to be a conversation starter: who talked, a link to something concrete, and a filled form never presented as done.
- The tool cannot supply the second and third people. Patton's workshop needs a developer who knows the codebase and a tester who asks the tough questions. The earlier suite's "stands in for the missing second party" is half an answer. Whether the output is filled fields or the questions for that conversation is open.
- The product-org assumption is real, and the minimums converge anyway. Cagan excludes custom software; Torres and Patton each give an explicit floor for feature teams; Hoskins is written to our reader. The floor: a specific who, a root why, what not how, failure cases, open questions with owners, one outcome line or "unmeasured."
- A good outcome can be "don't build it." Torres: the fruit of discovery is the time saved. Patton: "no-go is a great result." The skill should be able to end there.
- Two manners rules from Hoskins: a tool's quality is the relevance of the questions it asks, and when either default is unsafe, offer no default.

## Decided 2026-09-18

Two examine runs, the artifact first and then the skill; Q1 was retired in the first and answered in the second. The skill is `plugins/alt/skills/story-refine/`, alt 0.8.0.

The artifact
- Q2 Complete after the conversation: title and the first sentence get it into the room; the conversation's answers, cases, checks, and open questions are written back so someone who was not there can build it.
- Q3 Outcome and measurement live on the epic. The story carries only what is specific to it, which is an acceptance check and never a metric. Stories build up to complete epics.
- Q4 Standalone stories are allowed and carry their need with no outcome. The count of parentless stories is triage's symptom.
- Q5 One shape for every kind of item, sections omitted when empty. Whose need it is lives in the first sentence as a role, never as a field or a persona name; a backend or platform item has a user too. The as-a-user sentence is out.
- Q6 Checks as Patton's two questions in examples: what we check, how we demonstrate it, with the data to run it.
- Q7 Size and priority are the tracker's fields, never content. `Split?` under Open is the only sizing trace.
- Q8 Developer work now, in words that do not presume code. Business and research wait for their own sources.
- Q10 An answered Open line leaves Open, lands as a case, check, or constraint, and its question and answer move to a comment.
- Q11 Native fields carry title and parent; the description carries the value as one block, the same shape in every tracker.
- The test every line passes: it changes the code, proves it, or stops a guess. Persona names, a separate who, the why as business justification, problem-today narrative, non-goals, section labels that explain themselves, and the demonstrate half as its own block all failed it. The goal line, the if-wrong lines on Open, and a runnable check per case came back at value 3.
- Parked, Q9: whether the story names who was in the conversation.
- Reversed: the earlier line "a non-goals line stays, allowed empty."

The skill
- Q1 Shows the draft and any comment first, writes on the runner's go, one yes per run. Markdown in the room when no tracker is reachable.
- Q12 An existing item not in the shape is rewritten into it, the original moved verbatim to a comment on the same write.
- Q13 Reads by key: the item, its full thread, the parent the field names. The duplicate search is offered in one line and runs on a yes.
- Q14 Named `story-refine`; refinement is the industry's word for taking an item to ready, create or rework.
- Settled by the record: shape follows brief-create, ask what the template needs then examine then write; a complete item is nothing to do; business and research presets get one line; non-interactive shows and stops.

## Fixture run, 2026-09-18

Headless, `claude -p --plugin-dir`, the reminder-resend idea pasted, no tracker, no code, no sources file. The shape held: a verb-phrase title, parent none, the role in the first sentence, a goal line, four cases, the constraint with its source, `Split?` first under Open, no size, priority, metric, or verdict, and "write skipped" said once. What it did wrong: examine ran nine questions to an empty room and every one landed under Open, with two more lines for the checks it had no data for and the facts it could not reach, so Open held eleven items against a story of four cases. That is the no-code, no-runner worst case; an interactive run in the repo settles most of it before the draft. Watch in use: whether Open stays short when the code is there, and whether the "look up, do not ask" line the skill invented for unreachable facts is one the template should name. The business preset stopped in one line as specified.

## Follow-ups from the epic reading, 2026-09-21

Agreed in conversation after the epic sources were read; decided alongside the epic, not before.

- The goal line is written only on a standalone story. A parented story reads it up from the epic's need, which the skill already fetches. A standalone story carrying its own goal is allowed and is going to happen; the count of them is triage's symptom.
- A constraint inherited from the epic is not repeated; its source line says "the parent."
- Open gets an upward exit. When the Open questions are about the need, the outcome, or the why rather than the cases, the story says so in one line and routes them to the parent, or to "no parent" as triage's symptom. The fixture run's eleven Open items were this.
- The epic body lists only the pieces with no story yet. The children with stories are the tracker's parent links, so Q11 is the source of truth for the index and the epic never restates it.

## Field run, 2026-09-24

The first run on real code: six stories written into leantechniques/agent-ready-assessment (#164 to #169) on 2026-09-23 and 24, each from a false or overstated finding on one client repo, with a tracker connection and the code beside it. Reviewed the next day by five independent Opus agents, one role each (implementing developer, test engineer, product owner, maintainer, story editor), plus the orchestrating session. Reports live in that repo at `.agentic/reviews/2026-09-24-story-review/`; the HANDOFF file there carries the story repairs, which are not this skill's concern.

What held: one shape and one voice across all six; cases as condition to behaviour; checks naming the test class and fixture style; code pointing at the sibling to copy; research in a comment with the body standing alone; the goal sentence, which every reviewer used to judge the trade-offs a story made.

What leaked, and the cause in the skill:
- "Per the runner, 2026-09-23" written into a public tracker. The template's closing line read `per <who, date>` and the developer preset had no Runner hat. Fixed in 0.11.1.
- "`./scripts/verify.sh` green" in six of six Checks and "per AGENTS.md" in four Constraints. The skill never said a repo-wide gate is not a check, and the Constraint bracket's "usually absent" says how often, not what disqualifies.
- Line-number citations, correct on the day and drifting with the next merge. "Cited in a few words" said nothing about form.
- Research comments pasted verbatim from a sub-agent, including sections no line of the body rests on. The skill defined one comment and was silent on others.
- No slot for what describes the part being changed: the reference entry landed inside Checks, and the description the product shows for a check was left contradicting the new behaviour in three stories.
- Not a placement fault but the largest finding: Checks named fixtures, seams, and "existing tests" that do not exist, and "dogfood passes" claims no test enforces. The homework says looked up and cited; nothing gates that the file was opened. Open, see below.
- Nine "Unchanged." cases and five "Existing test." checks against "only where the behavior changes". Open.
- Six parentless stories from one engagement, each re-arguing the need in an identical opener. The epic was never written. Open, with epic-refine.

Reviewer agreement was the useful signal: five independent reads converged on the same handful of findings, and everything else appeared in one report only. A review is a generator, not a filter; act on what two or more hats raise.

## Decided 2026-09-24

- A gate the repo applies to every change is not a check. Written on the Checks bracket.
- A repo rule is a constraint only when this story's change would tempt breaking it, and then one line names the rule and the temptation. Replaces "usually absent" on story and epic.
- A citation is a path and a symbol, heading, or quoted phrase, never a bare line number; a line number only with the commit it was read at. Homework opener on story and epic, and the Code slot.
- A comment carries the source for what the description asserts; a section nothing in the description rests on is not written, and the description says where it went when it went somewhere. Footer on story and epic. The test is "does the body rest on it", not "does the body repeat it": the download counts behind an allowlist pass, an industry survey does not.
- A Docs slot after Code: what says what this part does today and changes with it, omitted when nothing does. A description string the product shows is code for the line test; the slot names what changes with the code.
- Open: a gate that nothing named in a Check was written without the file opened; whether "Unchanged." earns one boundary line; the upward exit for the need itself when several stories come from one cause.

## Decided 2026-09-24, the how

A five-hat board (senior developer, junior developer, coding agent, tech lead, product owner) scored #164 to #170 for implementation presence, 1 to 5; every opener scored 1, Checks 3 to 4 everywhere, Code 3 to 4 except the two smallest stories, and #170, the 0.11.2 template's own output, scored higher than the #167 it duplicated. Reports and synthesis in agent-ready-assessment at `.agentic/reviews/2026-09-24-implementation-board/`. The research already said it: intent with latitude, never how; the recipe is the first thing a story never carries. The line test had been read as "says how to change the code."

- The Code section is removed. It did three jobs: locate, which the check id and the product strings in Cases already do; scope, which is the builder's first design decision and the writer pre-empted from a partial view (#164's fix may belong in the scorer, #166's sibling sat in a project the check cannot reference); and anchor attention, which was the harm, since a confidently named helper removes the doubt that makes a builder or an agent open the code. Half the siblings named this week were the wrong shape and no reader caught one. A codebase that needs a pointer per story to be navigable has a documentation gap in the codebase, not in the story.
- This reverses 0.11.2's Code bracket, "each with a symbol, heading, or quoted phrase", which made Code worse the same day it landed. The citation form stays for facts cited in the room and in comments.
- Product copy survives, in Cases: every string the product shows that the change touches, as final wording, and one line for the strings it leaves alone when a reader would wonder. This also settles the "Unchanged." question: one boundary line, never nine.
- Checks are demonstrations at the product boundary, one per claim, runnable in front of the team, never the test that proves them. The product owner's demo rewrite kept 22 of 78 lines; the rest were fixture permutations, good tests, and the builder's to choose.
- Evidence is the observation that prompted the story, in the words of whoever saw it, in the opener. The homework's technical facts shape the cases and stay in the session; a comment only for provenance a reader might dispute.
- A cross-story contract is an architecture artifact: an ADR, the parent's Constraint, or a tracker relation. The story cites it and never restates it. The #165 and #168 "one shared map" lived in two stories that drifted the same day; that is the missing epic showing up as a constraint.
- A fixed closing sentence in every story: "If the code contradicts a line above, the line missed the need. Work out what the need requires, alone, with an agent, or with the team, before building." Not "stop and say which line": a contradiction is the story's miss and a return to the value, whoever does the returning.
- Line test amended: every line says what the system will do for whom, proves it where the person sees it, or stops a guess; none says how.
- Cases are rules: a situation the person could set up without reading the code, and what they see in the product's own words. The how had three doors left after Code went, each visible in #168: an internal in the condition ("No `DotNetSolution` in the context"), the code's vocabulary ("Location hint string", "AppliesToTestProjects"), and examples standing in for rules (two projects, one, both: a truth table, which is a test plan).
- Checks are the examples, at least one per case; a case with no check is an Open line. A check with no case is a test detail and goes.
- Data a rule turns on, a list, a map, a threshold, is the what: a short table in the case, a cited comment when long. #168's prose map was the wrong form, not the wrong content.
- A comment cites a decision record, a document, or an observation someone can repeat, never a source file or a symbol. The first 0.12.1 refine run wrote four `src/` paths into its sources comment because the homework's citation form and the comment rule together told it to; the how had one door left and it was the one the skill opened. 0.12.2.
- "What the product shows" is per repo, under `## Shows` in `.agentic/alt/story-refine/extend-skill.md`, and the product's words come from the repo's language file, CONTEXT.md here. Not in the template: a slot per field is a template zombie by the next product. Follows grill-me.md's ruling that skill-specific per-repo content lives in a per-skill extension file.

## Verification runs, 2026-09-24

alt 0.11.2, the runner present, tracker reached through `gh`, both in agent-ready-assessment.

- Refine #164. The run quoted each section where it and the item disagreed. Every expected offender surfaced and left on the runner's yes: the verify.sh gate, "per the runner", the checks.md line number, the checks.md deliverable sitting inside Checks. A Docs line appeared naming the reference entry and saying the two description strings hold. The two Open lines were answered in two turns and left as Closed from Open comments naming the person. Decisions found two roots; both were answered in the room and folded, one into the Constraint, whose reason changed from "because Java and TypeScript do" to "neither the work nor the risk is per project". One "Unchanged." case stayed, as the rule keeps existing lines. Not asked for and worth keeping: the homework caught a false lean in the item (the Java sibling's Location is null) and a false claim in the opener (the category floors at 34 projects, not fifteen).
- Create, a fake duplicate of #167, every decision the session's own, closed after as #170. Default output with no runner steering: no gate, no repo-policy constraint, no bare line number, a Docs line naming the reference entry and the description string, a Constraint that passed the tempt test (accepting a false pass, and #108's boundary), no "Unchanged." or "Existing test." lines. Decisions returned zero roots; the code settled everything the draft left implicit. The comment shrank from 3,644 characters of pasted research on #167 to 642 of source the body rests on. The body grew from 453 to 483 words, the Docs line and the git-index check accounting for it. The consultant opener is still there: Kind D, the missing epic, not this change.

Read: the four bracket tests hold on first contact with real code. Kind C ("Unchanged.") and Kind D (the opener and the parent) are the next items; the verification gate (nothing named in a Check without the file opened) is the one that mattered most in the review and is still unwritten.

## To write

- Whether triage should flag a contract that exists only inside two stories.
- Summary.
- The problem the skill solves, and for whom.
- Relationship to epic, where outcome and assumptions went.

## Decided 2026-09-24, the reader

The six stories of the field run were read again the same day, first as a set against Jeffries, Wake, Cohn, North, Keogh, Adzic, Cockburn, Fowler and Patton from their primary sources, then by four Opus hats that would run the skill (product owner, senior developer with an agent, tech lead, embedded consultant), then a fresh shape was put through three rounds with six Opus voices, one per school, each grounded in the sources before reading the draft. Reports are in the session of 2026-09-24 and not on disk; the tallies are here.

- The root was the skill's first sentence, "what a developer alone can build correctly from, with nobody to ask." Four of four hats named it unprompted. It is the definition of a spec, and Cases, Checks, the frozen copy, and the enumerated lists served it faithfully. The definition now names two readers: the product owner who signs and the builder who challenges. 0.13.0 rewrites the skill from the standard product-company ticket, with the sources as guardrails, rather than patching the 0.12 template; a patch list that replaced every section was a rewrite afraid to say so.
- Unanimous across hats and schools: the closing disclaimer goes; Checks capped at a few demonstrations (North's six); the headline verbatim and the body as intent (Cohn's rejection test); lists in code with the research comment as provenance; Constraint collapsed to a Depends line; the dated incident kept in the opener; the research comment kept.
- Three of four hats and four of six schools: two or three boundary examples belong inside a story about a classifier, so "rules, not examples" was too far. Examples are now a section, three to six, the incident first, and Examples was the section most refused when each reviewer was forced to cut one.
- The schools split once: where confirmation lives. XP flips to examples-first; BDD keeps rules first and derives; Cohn keeps signed prose criteria; Adzic states each rule once with a key example per mechanism; Cockburn says none of those finds holes and wants a timed conditions list. The shape takes Adzic's rules with Cockburn's discipline: the sweep runs before the draft, routes each hit, and never prints. Five of six cut Conditions as a printed section; Cockburn's audit of the routing then showed three of five hits changing their answer when placed, so a routed hit keeps its outcome and a hit whose placement would change what the person sees is an Open line.
- Added from the hats, not the sources: Decided (rationale only, who chose, the alternative), Out of scope (what the person sees, the owning key), a name on every Open line, and a word budget of about 350. Cohn and Patton both found Decided leaking pass/fail lines; that rule is now on the template.
- Parent none is no longer silent: the need question is the first Open line and epic-refine is offered once. Six parentless stories re-arguing the same opener was the missing epic; #165 and #168 contradicted each other on test-project references because nothing owned the rule. Homework now reads sibling titles and Open sections, since the repo tells an agent nothing about sibling tickets.
- The forced single cut was the better instrument. Round two, five of six named Conditions; round three, six voices named five different things and four said stop. Convergence marks dead weight; divergence marks the floor, where each remaining section has a reader it protects. The floor for this team is about 380 words on #165, against 1,250 in the original and about 330 in the hats' draft.
- The fill kept breaking the template's own limits (five sentences, four Open lines, a pass/fail line under Out of scope) after the template was right, so the skill now holds the draft against its limits before showing it. Over a limit is a split or an Open line, never a rule trimmed to fit.
- Kind C and Kind D from the verification runs are closed by this: one identifiers line only when a reader would wonder, and the parent exit above. The verification gate (nothing named without the file opened) is moot for the story, since nothing in it names a file; it moves to the provenance comment.
- Reversed the same day, after the first 0.13.0 run on #165: no comment sits beside the story. The provenance comment was the second document the runner had already rejected, a dated slice of time the body did not stand without. What a builder can look up is not written down; a list a rule turns on lives in code, or on the story as a short table when the signer must own its members. The 0.12 rule that a comment carries what the description asserts is gone, and with it Closed from Open comments and the verbatim-original comment on refine; the tracker's edit history holds the original. Parent is a tracker field, never a body line.
- Depends on is a tracker relation, like Parent, and leaves the body. GitHub's dependency relation accepts issues only, so a story that waits on a pull request says so in the room and writes nothing; a PR is a state, and the staleness test already excluded it. 0.13.1.
