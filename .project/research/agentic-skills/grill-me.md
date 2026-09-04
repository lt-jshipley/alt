# Grill-me family: research notes

Reviewed 2026-09-03, updated 2026-09-04. Public sources were read from their repos at the commits listed. Our own two are read from local checkouts. Skill text quoted below is from those versions. What alt built from this, and what it kept, is at the end under "alt's first two versions."

## Summary

"Grill me" is a family of Claude Code skills that flip the agent from builder to interviewer. Instead of writing code from a loose idea, the agent asks questions until every decision the plan depends on has been made explicitly by a human. Matt Pocock's version is the original and the one everything else forks. It has since been split into a reusable `grilling` primitive and a one-line `grill-me` front door. The public forks differ mainly in question cadence (rounds versus one at a time), how questions are posed (plain text versus the AskUserQuestion popup), and how much tooling is bolted on.

Our two, `explore` and its descendant `era:examine`, are the owner-aware branch of the family. They keep the interview but answer a question none of the public versions ask: is this decision actually yours to make. Every decision is tagged with the owner who holds the missing information, carries a blast radius and a recovery line, and ends in exactly one of three recorded states. `explore` was Jira-backed. `era:examine` is repo-agnostic, renamed from `explore` in era 3.0.0, and adds a derivation step that lets a repo's recorded doctrine settle decisions before they become questions. `era:challenge` is that same derivation fired after the fact at a shape already proposed; it is not an interview, but it is where examine's misses were caught in use.

## The problem all of them solve

Most agentic coding failures are not the model failing to write code. They are the model writing the wrong thing because the requirements were never fully specified, and the human only discovers the gap after the code exists. Plan mode makes this worse: it primes the agent to rush toward a plan, so unstated assumptions get systematized into confident output before anyone notices them.

The grill-me pattern attacks this at the source. It forces the decisions out of the human's head and into the conversation before anything is built, and it puts the agent's own knowledge of how systems break to work as the questioner rather than the answerer.

### The problem the owner-aware branch adds

Interview-style skills produce a plan the interviewee wrote, and treat the interviewee as the sole authority. In a team three things go wrong:

- **Wrong hat.** A product or architecture decision gets made by the implementation session because it was the one in the room. It gets defaulted into whatever the first draft did and nobody upstream ever sees it.
- **Minimised escalation.** When the developer does recognise a decision is not theirs, they paraphrase it into a chat message. The paraphrase loses the mechanism and the blast radius, and the owner answers the smaller question they were asked.
- **Permission slip to guess.** A recommendation attached to a question the developer does not own reads as licence to pick it. The AI's opinion becomes the decision by default.

Both of ours also treat pressure-testing a proposed approach as a second hunt for decisions, on the grounds that a flaw in the plan is a decision ("partial failure: how?") and belongs in the same triage.

## Implementations

### 1. Matt Pocock: `grilling` + `grill-me` + `grill-with-docs`

- Repo: https://github.com/mattpocock/skills (MIT, reviewed at 6654f6b, 2026-08-24)
- Skill files:
  - https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md
  - https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md
  - https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md
- Docs: https://github.com/mattpocock/skills/blob/main/docs/productivity/grilling.md and https://github.com/mattpocock/skills/blob/main/docs/productivity/grill-me.md
- Author write-ups: https://www.aihero.dev/skills-grill-me and https://www.aihero.dev/my-grill-me-skill-has-gone-viral
- Refactor discussion: https://github.com/mattpocock/skills/discussions/392

**How it solves the problem.** Three ideas carry the whole skill.

- The **design tree**: every decision branches into the decisions that hang off it.
- The **frontier**: the set of decisions whose prerequisites are all settled, so they can honestly be asked now.
- A **round**: one full frontier, asked at once, each question numbered with a title and a recommended answer on its own line. The user answers by number. Answers settle decisions, the frontier moves outward, and the next round asks what that unblocked. Two questions never share a round if one depends on the other.

Facts and decisions are split explicitly. Facts about the environment are the agent's job and it dispatches sub-agents to find them without blocking the round. Decisions are the user's and the agent must wait. The session ends when the frontier is empty, and there is a confirmation gate: the agent does not act until the user says the understanding is shared.

The structure is layered. `grilling` is the primitive and is model-invocable on any "grill" trigger phrase. `grill-me` is user-only and its entire body is "Call the Skill tool with 'grilling'". `grill-with-docs` calls `grilling` plus a `domain-modeling` skill and writes CONTEXT.md and ADRs as it goes. Other skills in the same repo (wayfinder, triage, improve-codebase-architecture) reuse `grilling` rather than inventing their own interview.

**Value.** Turns a vague idea into a set of defended decisions in one conversation, typically dozens of questions in three or four rounds. Stateless, so it works on anything: features, product direction, business calls, writing. Recommended answers mean the user can often answer "yes" instead of explaining, which the author credits as the single biggest speedup.

**Who it serves.** Anyone about to commit effort based on an idea that is not yet fully specified. Developers before building, tech leads before writing a spec, and increasingly non-engineers making decisions that won't sit still.

**Gaps.**

- A skill that names another skill does not reliably cause it to load. The author documents this as real and unfixed. The tell is an interview with no recommendations attached. Since `grill-me` is a one-liner, it is broken entirely when the dependency fails to load or was never installed.
- The frontier is the model's judgement, not a computed graph. Two dependent questions can land in one round and only afterwards be found to conflict. The only guard is the user noticing.
- `grill-me` is stateless by design. Forty-six questions of decisions live only in the conversation, which is exactly the context most likely to be compacted or lost. The decision log is often the most valuable output and it is not written down unless you use `grill-with-docs`, which adds a second dependency.
- No cap on questions and no scope guidance inside the skill itself. The docs say "break the work up" but the skill does not detect or suggest it, so runaway sessions are a known complaint.
- The confirmation gate degrades on weaker models, which collapse "interview until shared understanding" into two questions and an outline.
- Rounds are contested. A large share of users opt back to one-at-a-time via a CLAUDE.md line. Answering fifteen questions by number gets awkward, and the recommendation sometimes argues against the question's wording so "agree" means "no".
- "Ungrillable" questions (how should this look or feel) are handled in the docs by pointing at a separate prototype skill, but the skill text does not recognise them, so sessions balloon while the agent rephrases and the user guesses.

### 2. RobMitt: `grill-me-skill`

- Repo: https://github.com/robmitt/grill-me-skill (reviewed at 31d61d6, 2026-04-11)
- Skill file: https://github.com/robmitt/grill-me-skill/blob/main/SKILL.md

**How it solves the problem.** Same relentless interview premise, one question at a time, but every question goes through Claude Code's AskUserQuestion popup with two to four concrete multiple-choice options. Generic yes/no options are discouraged unless the question is binary. The agent acknowledges each answer in one or two sentences, then immediately asks the next. If a question can be answered by exploring the codebase, the agent explores instead. Ends with a concise summary of decisions.

**Value.** Lowest friction to answer. Clicking an option is faster than typing, and the options themselves surface the realistic directions so the user is choosing rather than generating. Good for people who find the round format overwhelming.

**Who it serves.** Developers working inside Claude Code specifically, and people who want the interview to feel like a guided form rather than a written exchange.

**Gaps.**

- Tied to the AskUserQuestion tool, so it is not portable to Codex, Cursor, or any harness without that popup.
- Two to four options anchor the user. The option set is the agent's opinion in disguise, but it is never stated as a recommendation with reasoning, so the user cannot push back on the reasoning.
- "I don't know" and "I need to ask someone" are not natural answers in a popup. The user has to reach for "Other" and type, which discourages the honest answer.
- No facts-versus-decisions rule beyond "explore the codebase". The agent can still ask the user for things it should have looked up.
- No confirmation gate before implementation. The skill ends with a summary and nothing tells the agent not to start building.
- One question at a time across a large tree is slow. Thirteen questions is thirteen round trips.

### 3. ericgandrade: `claude-superskills/grill-me`

- Repo: https://github.com/ericgandrade/claude-superskills (MIT, reviewed at 394587c, 2026-05-11)
- Skill file: https://github.com/ericgandrade/claude-superskills/blob/main/skills/grill-me/SKILL.md

**How it solves the problem.** Adds structure around the one-question-at-a-time core. Step 0 reads the plan and explores the codebase. Step 1 silently maps the decision tree: what is locked in, what is open, dependencies, unstated assumptions. Step 2 interviews one question at a time with a recommended answer and reasoning, exhausting one branch before opening another. It cycles through named question types: scope, dependencies, failure modes, rejected alternatives, success criteria, reversibility, ownership. Step 3 closes with a structured summary: decisions confirmed, decisions changed, open questions, risks surfaced. Rules include "push back on weak reasoning, don't accept 'it should be fine'" and "surface assumptions the user didn't state but is implicitly relying on". Triggers only on the literal word "grill" and explicitly refuses near-synonyms.

**Value.** The question-type checklist is a real contribution. It gives the agent a rubric for what a complete interview covers, which reduces the chance of a whole category (reversibility, ownership) being skipped. The structured close is the closest any of the public versions come to producing a reusable artifact.

**Who it serves.** Teams that want the interview to be auditable and consistent across sessions, and users who want a stronger guarantee of coverage than "the agent walked the tree".

**Gaps.**

- The checklist can become a rote loop. Cycling question types is a different discipline from following the tree, and the skill asks for both without saying which wins when they conflict.
- One at a time only. No round mode and no opt-in.
- The structured close is printed to the conversation, not written to a file. Same evaporation problem as Matt's.
- The strict "only the word grill" trigger is aimed at preventing accidental invocation, but it also blocks the skill from being reused by other skills that want an interview.
- Includes Portuguese trigger phrases and a "before I present" framing that are specific to the author's context.

### 4. alirezarezvani: `claude-skills/engineering/grill-me`

- Repo: https://github.com/alirezarezvani/claude-skills (MIT, reviewed at 19392f7, 2026-08-26)
- Skill file: https://github.com/alirezarezvani/claude-skills/blob/main/engineering/grill-me/skills/grill-me/SKILL.md

**How it solves the problem.** Matt's older one-at-a-time text preserved verbatim, with a `derived_from` metadata block for attribution, plus Python scripts: a decision tree extractor, a question generator, and a session tracker. The workflow runs the scripts first, then walks the generated question list, recording answers in the session. Output pattern is `Q[i]/[total]` with a recommended answer.

**Value.** Mostly as an example of clean attribution when deriving from an MIT skill. The session tracker is a gesture at the persistence gap.

**Who it serves.** Users of that author's broader `cs-*` skill collection, which wraps everything in its own agent and command namespace.

**Gaps.**

- Extracting the decision tree with a script is a category error. The tree is judgement about the plan, not something parseable from the text. The scripts add a Python dependency and maintenance surface for no gain in question quality.
- `Q[i]/[total]` implies a known total, which contradicts the whole premise that answers reshape the tree.
- Coupled to the author's `cs-*` wrapper, agent, and command layout. Not lift-and-shift.

### 5. chaseai-yt: `crucible` (formerly `grill-me-codex`)

- Repo: https://github.com/chaseai-yt/grill-me-codex (reviewed at f8c111d, 2026-08-24)

**How it solves the problem.** A different scope. Four phases: recon, where Claude researches the codebase and produces an assumptions ledger batched for confirmation; interrogate, one load-bearing question at a time with a decision map separating critical from cosmetic choices; review, where OpenAI Codex attacks the resulting PLAN.md read-only and Claude arbitrates until approved; and an optional build phase where one model writes and the other inspects the diff. The invariant is that whoever built something never grades it.

**Value.** Cross-model adversarial review catches blind spots a single model shares with itself. The assumptions ledger and the critical-versus-cosmetic split are both good ideas independent of the second model.

**Who it serves.** Teams already paying for both Claude and Codex who want plan review to be independent of plan authorship.

**Gaps.**

- Requires the Codex CLI and a second paid model. Not usable where only one vendor is approved.
- Bundles interview, review, and build into one skill family. The build phase is out of scope for a grilling skill and makes the whole thing harder to reason about.
- Heavy. The interview is the smallest part of it.

### 6. Ours, first version: `explore` (Jira-backed)

- Where: `~/Development/agentic-temp/summary.md` (the `/explore` section, a value/problem/deviation/principles summary of the suite it shipped in) and `~/Development/agentic-temp/skills.md` (the `explore` skill text and its `Question format` spec, alongside the sibling skills). Not public.
- Dependencies: a `backlog-standards` skill (owner ladder, routed-question contract, load-bearing spotlight, verdict rubric, blame-free wording), a `knowledge-map` skill (which home owns which fact), and the Atlassian MCP for reading the ticket and posting the package. Sibling skills in the same suite: orient, handoff, ticket, epic, triage, orient-sync.
- Companion note: `~/Development/agentic-temp/atlasian-costs.md` covers keeping Atlassian MCP calls on free tools once Rovo moves to usage billing in December 2026. Relevant to any skill that reads or writes Jira.

**How it solves the problem.**

- **Silent homework first.** Reads the code the work touches, the ticket, repo docs, and the `.agentic/` domainspace files. Anything answerable there is a fact, looked up rather than asked. Only genuine decisions, where more than one defensible answer exists and someone must pick, survive as questions.
- **Two hunts.** What the seed leaves ambiguous, and where a proposed approach breaks.
- **Owner ladder from backlog-standards.** You (the developer alone, cheaply reversible), Tech Leadership (design other tickets inherit), Business Owner (business rules; engineering proposes, never decides). Lowest rung that can legitimately answer, following who holds the missing information, never how important the question feels.
- **Triage layer, about fifteen lines.** Counts by owner, the two or three load-bearing questions and what they gate, a mandatory "you can proceed now on" line so escalation reads as a work plan rather than a stop sign, then a one-line index split into your pile and the pile going to the ticket.
- **One card per turn.** Four blocks: the question phrased as the decision, the Issue (the one uncapped home for prose), consequences as one "if guessed wrong" line and one "recovery" line with no severity labels, and two or three options. A You card ends with a recommendation and its why. An elevated card withholds the recommendation in the developer-facing view because a recommendation there is a permission slip to guess, and restores it in the owner-addressed package.
- **Standing answers, advertised once.** `show`, `expand`, `escalate Qn`, `accept Qn: <option>` (risk on record, with one follow-up on a load-bearing accept: "who else is aware of this call?"), `Qn: <answer> — per <source>` to relay an owner's decision with its source, and `reclassify Qn: <why>` as the only way a rung changes.
- **Living walk.** Every answer re-derives: spawns questions with fresh stable Q-ids, retires mooted ones, moves the spotlight and the partition. Ends when nothing material remains, not when the list runs out.
- **Open Decisions package to the ticket.** Full cards travel verbatim because a paraphrased escalation gets minimised. Everything else is a one-line ledger: relays, acceptances, reclassifications, retirements, load-bearing answers. Posted as a Jira comment that supersedes the prior one by name, carries Q-ids forward, and on re-run ingests replies as relays. Proposes an @-mention recipient because a comment notifies nobody by itself.
- **Degrades, never blocks.** No MCP or no ticket means a markdown package and the absence said plainly. Missing backlog-standards is surfaced as an install bug.

**Value.** The ticket becomes the decision record, in the place the team already reads, and it is re-runnable with movement. The developer is a courier, not an editor. Owners get the full card and the recommendation addressed to them. The load-bearing gate is real, so plan mode is never entered past an unanswered load-bearing question, but work that is not gated proceeds.

**Who it serves.** The developer at the keyboard in a team with leads and business owners who are not in the session. The lead and business owner, who receive questions in a shape they can actually answer. The team, through a ticket record that outlives the session.

**Gaps.**

- Hard-coupled to Jira and the Atlassian MCP. The ladder names people-hats, and the skill assumes a ticket usually exists. Not liftable to a team on Azure DevOps, GitHub Issues, or Linear without rewriting the delivery half.
- Options are peer options with a recommendation on top. Nothing in the skill lets recorded team doctrine settle a decision before it becomes a question, so a decision the team already made reappears as a card unless the homework happens to find it. era later named this exact shape as the anti-pattern.
- Self-identified: no menu of stress-test lenses for the break hunt, and resolved terms are not written back into the domainspace files.
- One card per turn is slow on a large tree. The spec admits ten cards at once is the wall it exists to kill, but the alternative it chose is one screen per question.
- Withholding the recommendation from the developer on elevated cards protects against guessing but also removes the mentoring payload. The developer sees the options and the stakes but not the analysis.
- Delivery is best-effort. A posted comment notifies nobody, the @-mention is a proposal, and "no one to name" is a legal answer. The package can sit unread.
- Depends on two sibling skills being installed and the MCP being authenticated. Each absence degrades honestly, but the fully-degraded run is a markdown file the developer has to hand-carry.

### 7. Ours, second version: `era:examine`

- Where: `~/Development/era`, published at https://github.com/joeyshipley/era. Marketplace `era`, plugin `era`, version 4.0.0 at the time of review (commit ddd83e2). MIT.
- Skill files: `plugins/era/skills/examine/SKILL.md`, `plugins/era/skills/examine/format.md` (the spec for the triage layer, cards, walk, standing answers, and output shapes), and `plugins/era/skills/examine/extend-skill.template.md` (headings a repo fills in: decision record, product docs, homework sources, where approaches break here).
- Dependencies inside the same plugin: `era:owner-ladder` (the rung table and its rules), `era:stances` (the derivation and the list, which lives in the adopting repo at `.agentic/beliefs/stances.md`). Read by `era:brief-create` when shaping a brief, and its pushes are read by `era:retro`. `era:challenge` runs the same derivation after the fact on a shape already proposed.
- Lineage in the git log: 2.1.0 "explore derives at triage; a settled decision is a line, a card is a genuine choice", 3.0.0 "explore becomes examine; a push has a line; a Brief choice is open and cheap".

**How it solves the problem.** Same skeleton as `explore` (homework, two hunts, triage layer, walk, three terminal states, honesty rules), with five substantive changes.

- **The ladder is named by artifact, not by person.** Brief (this session, reversible by a later brief), Design record (the architect hat, in a design conversation, never mid-phase), Product / Stop (the product hat, plus the never-batched pile: money, legal, safety, identity). Each rung names where the answer must land. A new test for the Brief rung: the record is silent **and** a wrong pick is cheap, recovery one move. Open and expensive is not a keyboard choice; it is a gap in the record, tagged Design record with the gap named, so its answer lands in the record and the next run has one fewer question.
- **Derivation at triage.** Before anything is called a question, the record is consulted: the stances and beliefs in `.agentic/beliefs/`, the brief's Constraints, the repo's decision record in `.agentic/era/*/extend-skill.md`, and the code beside the work. A decision the record settles becomes a settled entry with a stable S-id: the shape, the stance keys that settled it, and a Rules-out line naming each move not taken as a patch (defers what onto whom) or a break (which recorded decision). It gets no card. A settled entry may carry one push handle, the strongest case the record is wrong, and `push Sn: <why>` reopens it as a question whose line names the contested stance. That line is what the retro reads to find a stance that is wrong as written.
- **Six angles for the break hunt.** Feasibility, dependencies, edge cases, alternatives, scope and ordering, failure modes. Each asked of the seed, never of the user. This closes the "no menu of lenses" gap `explore` named about itself.
- **Cards carry a derivation, not a recommendation.** Five blocks: header, Plainly (the decision in ordinary words), the Issue, consequences, then "Options, a genuine choice because <the stance or gap that leaves it open>" with each option tagged removes-the-problem or defers-it-onto, followed by a Derivation stating what the record does say. On a Brief card the ask is which. On an elevated card the ask is route, accept with risk, or reclassify, and the derivation travels with the routing pointer for the owner. This reverses `explore`'s withheld recommendation: the developer now sees the analysis but never a pick they are not entitled to make.
- **One branch per screen.** The walk groups one to five related Brief-rung questions that share a parent decision or a seam, highest blast radius first, and that branch's elevated cards follow one per screen. Answers are read against the record before a question closes; an answer that is a move the settled block ruled out is said so in one line and the question stays open. This sits between grill-me's full-frontier rounds and `explore`'s one card per turn.

Output with an Active brief is its Open Questions section, one line per question with exactly one disposition (`answered → section`, `→ Phase N`, `routed → artifact`, `accepted with risk → section`, `retired, mooted by Qn`). Without a brief, the package is emitted in the conversation. The accept follow-up changed from "who else is aware" to "what would tell us this was the wrong call", and the answer is recorded as given.

**Value.** Fewer questions reach the user, because the record answers what it answers and the derivation shows why. The measure of a run is stated in the skill: how few decisions the user had to make, and that none of them could hurt. Pushes feed a retro loop that keeps the stances honest. Repo-agnostic: no Jira, no MCP, works on any seed including a conversation.

**Who it serves.** A solo or small shop that has adopted era's doctrine and works in briefs. The skill's own framing is that the solo shop is not exempt: the implementation session under pressure is the junior dev who will make a product call silently, and the ladder exists so that call is surfaced with the right hat on. Also any downstream era skill that needs an interview.

**What changed from `explore`, one line each.**

- Ladder moved from people to artifacts, so a rung names where the answer lands, not who to ping.
- Recommendation withheld became derivation shown, so the developer learns the analysis without being handed a pick.
- Jira comment became brief file, which gained repo-portability and lost the relay verb and the write-back.
- One card per turn became one branch per screen, halfway to Matt's rounds.
- The break hunt got its six angles.

**Gaps.**

- Heavy prerequisite load. A run must load owner-ladder, stances, format.md, the extension file, and the beliefs before asking anything, and SKILL.md says "do not paraphrase them from memory". That is the same skill-invokes-skill flakiness Matt Pocock documents, mitigated only by instruction, and it costs context on every run.
- Coupled to adopted doctrine the way `explore` was coupled to Jira. Without `.agentic/beliefs/stances.md` the stances skill says stop, and "settled by the record" has nothing to derive from. In a repo that has not adopted era, examine either degenerates into peer options or refuses. Neither of ours is portable on its own.
- The record is small. Nine stances and ten code beliefs cannot settle most real decisions, so the honest outcome on many seeds is a pile of Brief cards or a pile of "gaps in the record" routed to Design record. The second is correct by the skill's own logic but could over-escalate on a repo that is early in adoption.
- Lost the write-back and the relay. `explore` posted to the ticket and ingested owner replies as relays with a source. era writes only to an Active brief and has no relay verb, so an owner's answer arriving from outside has no recorded path back in. The multi-stakeholder routing became a pointer with no delivery.
- Dense, idiosyncratic prose. SKILL.md plus format.md are long, the frontmatter description alone is a paragraph, and the caps and verbs are many. A new adopter has a steep read, and a weaker model is unlikely to honour all the caps.
- Branch grouping is still model judgement, with the same limit as grill-me's frontier: two dependent questions can share a screen and only be found to conflict afterwards.
- Proof is the validator. `setup.md` runs `claude plugin validate --strict` and nothing else, and the repo's own extension file lists "a headless run proving a skill works only because the prompt pre-answered what the skill should have asked" as a way approaches break here. The authors know behavioural testing is weak.
- Rename churn. explore became examine and brief became brief-create in consecutive major versions, with extension paths migrating through sync. Every rename costs adopters.
- Installed copies are keyed by version, so edits need a bump to reach an install. A Claude Code constraint rather than a skill flaw, but it shapes the dev loop.
- Field observation, 2026-09-03: run against an unfamiliar codebase, every question examine surfaced was a deep implementation question the user could not answer without learning the code. Each one, run through `era:challenge`, came back as a miss with a shape the record already settled. The derivation at triage is specified but did not hold; a question the keyboard cannot answer without reading the code is by the skill's own ladder a fact or a routed question, never a Brief card.

### 8. Ours, companion verb: `era:challenge`

- Where: `~/Development/era`, `plugins/era/skills/challenge/SKILL.md`. Same plugin and version as examine. Added in era 3.1.0, "era:challenge, the verb fired at a shape already on the table".
- Dependencies: `era:stances` for the derivation and the list, `era:owner-ladder` for whose the decision is. A repo without `.agentic/beliefs/stances.md` has nothing to derive from, and the skill says so and stops.
- Triggers: "challenge", "real fix", "is that the real answer", "why are there options", "redo that properly".

**How it solves the problem.** Not an interview. It is the same derivation examine runs at triage, fired after the fact at a shape the session already proposed: a design, a recommendation, a plan step, a set of options. The target is the last shape on the table or the one the user names. With nothing on the table it stops; it never invents a shape to challenge.

- **Name the shape as proposed, without defence.** Peer options with a pick on top, a "for now", a smaller thing that answered the last prompt. Say which it was, in one line.
- **Run the derivation on it.** Facts from the record first: stances, beliefs, the brief's Constraints, the decision record, the code neighbours. For every option that was offered, say what settles it: a patch (defers what, onto whom) or a break (which recorded decision, and whether it can be undone).
- **Give the one shape.** Plain statement, then mechanism, then the stances it follows by key, then Rules out one line per move not taken, the test that pins the guarantee where one exists, and Breaks with the reason if it breaks a stance.
- **Say whose it is.** Brief rung: state it and wait for the owner's word. Design record or Product: the derivation travels with the pointer. Record silent and a wrong pick cheap: a genuine choice, and which stance or gap makes it one.
- **If the proposal was already acted on**, name that and what reversing it takes, then stop. Challenge proposes; the owner asks for the change.

Output is one screen in a fixed shape: Miss, Shape, Follows, Rules out, Whose. No re-presented options, no apology, no "you're right". The miss is named once and the shape stands on the record, not on the rejection. It edits nothing.

**Value.** Catches the derive-dont-offer miss at the moment it happens, in one screen, without a session-long interview. In use it did the job examine's triage was specified to do: every question examine surfaced in an unfamiliar codebase, when run through challenge, came back as a miss with a shape the record already settled. The user did not need to learn the codebase to get the answer.

**Who it serves.** The person at the keyboard when a session hands them a menu, especially in a codebase they do not know and cannot answer implementation questions about. Also the doctrine itself, since a challenge that finds the record wrong is a push in everything but name.

**Gaps.**

- Reactive and one at a time. It runs after the miss, on one shape per invocation, and only when the user knows to call it. A run of examine that produces ten cards is ten challenges.
- The same derivation is specified in two places, examine step 3 and challenge, and in the field only challenge held. Nothing in the repo records which one is authoritative when they disagree, or why the triage-time version fails.
- Same dependency on an adopted stances file, and the same load flakiness as everything else in the family. Without the record it stops rather than degrades.
- No output beyond the screen. The one shape lands in conversation only; nothing writes it to the brief, the decision record, or a push line unless the user does it. A challenge that corrects examine's card leaves examine's Open Questions line untouched.
- It names "a shape derived from the fact that the first one was rejected" as a thing it must never do, which is an honest admission that the model is prone to exactly that when asked to redo something.
- Not a substitute for the interview. It has no owner package, no walk, no blast radius, no partition, so it cannot replace examine, only correct its output.

### Also seen

- https://github.com/TimothyVang/Grill-me and https://github.com/Hanveyr/claude-skills-For-Hermes are forks of the public ones with no substantive changes visible from their descriptions. Not reviewed in depth.

## The concept, and what each claims to fix

Before any work is done, the agent stops being a builder and becomes the senior engineer interrogating the plan. It walks a loose idea through every decision it depends on, surfaces the ones nobody has made, and gets them made explicitly by a human. The problem it solves is that agents fail on unstated requirements far more than on bad code, that humans only discover the gap after the code exists, and that the agent's own knowledge of how systems break is wasted when it is the one answering instead of asking. The owner-aware branch adds a second problem: decisions getting made by whoever happens to be in the room rather than by whoever owns them.

### Not a research phase: the fact versus decision boundary

Grilling is easy to mistake for a deeper research phase that guides the agent to good results. It is something different. Research finds answers that already exist somewhere. Grilling manufactures decisions that do not exist yet, by forcing them out of the human's head. Matt Pocock's fact-versus-decision split is exactly that line: facts are the agent's job to go find, decisions are the user's job to make, and the skill breaks if either side does the other's work.

- **The output is commitment, not information.** At the end of a research phase the agent knows more. At the end of a grilling the human has decided more. Matt's own line is that grill-me writes nothing and "the only thing it leaves is a sharper version of the idea, in your own head."
- **The agent does not learn about the world.** It learns what the user wants, and it makes the user notice the choices they were making implicitly. That is closer to requirements elicitation or a design review than to research.
- **Research is inside it, in service of not asking.** Homework, sub-agent lookups, and derivation from the record all exist so the human is only asked things that cannot be looked up. "Facts are never questions" is the same rule stated from the other side.
- **Plan mode is the contrast.** Plan mode is research plus the agent authoring the plan. Grilling is the agent refusing to author anything until the human has decided.
- **The examine field observation is what a slipped boundary looks like.** The fact-finding in front of the interview was weak, so research questions reached the user dressed as decisions. Challenge did the research per question and the decisions vanished. The interview mechanics were not at fault; the boundary was.

The family's quality therefore rests on one thing: how well each version separates what can be looked up from what must be chosen. Rounds, cards, popups, and branches are secondary to that.

Below, each implementation's own claims about what it fixes that the others suffer, taken from its docs and skill text. Each line is the complaint, then the fix, then who the complaint lands on.

**Matt Pocock `grilling`**

- One-at-a-time is slow and everything-at-once loses dependency order. Rounds of the settled frontier get thirteen questions done in three turns. RobMitt, ericgandrade, and alirezarezvani suffer the first.
- Agents answer their own questions. Facts go to sub-agents, decisions wait for the user, and the two never blur.
- Agents start building when the list runs out. A confirmation gate holds until the user says understanding is shared. RobMitt has no gate.
- Every skill invents its own interview. One primitive is reused by every wrapper. Every other version is a monolith.
- Code-centric interviews cannot grill a business decision or a piece of writing. Stateless and repo-free, it runs on anything.

**RobMitt**

- Typing answers is friction. Every question is a popup with concrete options you click. Everyone else makes you type or answer by number.
- Rounds overwhelm. One question at a time.
- Yes/no options are lazy. Options must be the realistic directions.

**ericgandrade**

- Model-invoked grilling fires by accident on "stress-test this". Only the literal word "grill" triggers it. Matt's primitive fires on any grill phrase.
- "The agent walked the tree" is not coverage. A fixed checklist of question types guarantees reversibility and ownership get asked. Nobody else has a rubric.
- Sessions end in a vague summary. A structured close of confirmed, changed, open, and risks.
- Agents accept "it should be fine". Push back on weak reasoning and name unstated assumptions.

**alirezarezvani**

- Sessions leave no record. A session tracker script persists answers. Matt's grill-me is stateless by design.
- You never know how far along you are. A `Q[i]/[total]` progress line.
- Forks lose attribution. A `derived_from` block preserves it.

**chaseai-yt `crucible`**

- A single model shares blind spots with itself. A second model attacks the plan read-only and the builder never grades its own work. Every other version is single-model and self-graded.
- Confirmations trickle one at a time. Recon produces an assumptions ledger confirmed in bulk.
- All questions look equal. A decision map separates critical from cosmetic. The public versions have no priority signal.

**Ours, `explore`**

- Every interview assumes the answerer owns the answer. Each question is tagged with the accountable owner. None of the five public ones do this.
- Questions carry no stakes. Every card has a one-line blast radius and a one-line recovery, no severity labels.
- A recommendation on a question you do not own is a permission slip to guess. It is withheld from the developer and restored in the owner's package.
- Decisions evaporate with the session. The open set posts back to the ticket, supersedes the prior post, and ingests replies on re-run.
- Escalation reads as a stop sign. A load-bearing gate is real, but "you can proceed now on" is mandatory.
- Paraphrased escalations get minimised. Cards travel verbatim; the developer is a courier, not an editor.
- Ownership drifts in conversation. It moves only by a recorded verb, and relay is kept separate from accept-with-risk.
- Interviews stop at ambiguity. Pressure-testing where the approach breaks is a second hunt in scope.

**Ours, `examine`**

- Peer options with a recommendation on top muddy a settled answer into a choice. The record derives what it can before anything is called a question. `explore` and all five public versions do this.
- Withholding the recommendation removes the teaching. The derivation is shown; only the pick is withheld.
- Open and expensive gets guessed at the keyboard. It is a gap in the record, routed up, so the next run has one fewer question.
- Question count is treated as fine. The measure of a run is how few decisions the user had to make and that none could hurt. Grill-me calls forty-six questions ordinary.
- The break hunt has no method. Six named angles, asked of the seed, never of the user. Closes `explore`'s own admitted gap.
- Nothing validates the answers. Each answer is read against the record before its question closes.
- Doctrine never learns from being wrong. A push against a settled entry leaves a line the retro reads, so a stance found wrong gets rewritten. No other version has a feedback loop.
- One card per turn is slow and full rounds overwhelm. One branch of related questions per screen.
- Jira coupling. Repo-agnostic, any seed, with a per-repo extension file instead of a fork.

**Ours, `challenge`**

- Sessions offer menus the record already settles. Re-derive the shape on the table and replace it with the one shape. In use, examine's own triage output suffered this and challenge caught it.
- A rejected proposal gets replaced by whatever answers the rejection. The new shape stands on the record, not on the rejection.
- Models defend or apologise. The miss is named once, no "you're right", and the original is never defended.
- A proposal already acted on gets quietly redone. Name what reversing it takes and stop; the owner asks for the change.

## The junior developer problem

Recorded 2026-09-03. A long-held belief of ours is that all software should be written with the junior developer in mind. Held against that bar, every skill in this family fails in an ordinary development shop, and the two of ours were attempts to fix it that only partly landed. Two teams that adopted the interview saw their junior developers struggle with it, which is what produced `explore` and then `examine`.

### The incident

On a current engagement, a junior developer ran `explore` in a session with the agentic coach and the development manager watching. The skill surfaced a real risk: calling an external endpoint to save data four or five times in a row could produce a distributed-transaction failure the code would need to recover from. It presented three options. One was the genuine fix, heavy enough to stop development, force a conversation with the architect and lead, and rewrite the stories and technical direction. The other two were straw men, quick paths to get the story through to a pull request. The run also raised two further technical questions of high value and high complexity, and six business questions that needed answers.

The team's culture is that once you have a ticket, you get it done. The coach and the manager both told the developer to send every question to the team. The developer instead reshaped the saga-pattern question into a yes/no about the quick fix, with no context, and sent that. The manager was angry. It is his culture.

### What the incident shows

- **The skill predicted its own failure and could not prevent it.** `explore`'s design text says a paraphrased escalation gets minimised and the developer must be a courier, not an editor. The courier edited. The detection layer worked and found a risk that would otherwise have shipped. The delivery layer relied on the least powerful person in the room performing the hardest social act in the room, against the culture they live in.
- **The skill made the junior the router.** Nine questions, six of them business, landed on the person with the least authority to route them and the most pressure not to. Every version researched here does this, because every version assumes the user is the decision-maker or at least a reliable channel to one.
- **The menu was the trap.** One real fix and two straw men is exactly the shape `examine` later named as the anti-pattern. A senior sees through it in a second. A junior sees three options and picks the one that closes the ticket. Derive-don't-offer was the right diagnosis, but a derivation carrying stance keys is not something a junior can evaluate either.
- **Best-effort delivery failed at the only moment it mattered.** Posting the package to the ticket was offered, not automatic, and the @-mention was a proposal. The design chose developer autonomy over guaranteed delivery. The culture spent that autonomy immediately.
- **Volume was the experience.** The partition and the load-bearing cap exist, but the junior saw nine blockers. Grill-me refuses to cap on principle and calls forty-six questions ordinary. For a junior, the count is the whole feel of the tool.

### Where the family shares the flaw

- **Grill-me says it out loud.** Its own docs: "what comes out tracks the quality of your answers," "a session with no pushback from you is a session you didn't need," and passivity is its named failure mode. Passivity is a junior's default state. The tool is calibrated for someone with opinions.
- **The fact-versus-decision boundary is held by the user in every version.** A senior knows "that's a lookup, not my call." A junior treats every question as one they must answer. The `examine` field observation in section 7, run in an unfamiliar codebase, was the junior's everyday experience, and it showed the skill does not hold the boundary on its own.
- **Skills are written by seniors for themselves.** Matt Pocock's come straight from his own agents directory. `era`'s prose is dense doctrine with many verbs and caps that a junior cannot read, let alone `push Sn`. This is the over-engineered codebase parallel exactly: the artifact demands the author's context to use.
- **Recommended answers become "yes, yes, yes."** The mechanic that made grill-me spread is the one a junior is most likely to misuse, and Matt names the result: a plan the agent wrote and you nodded at.

### What the public versions brought that `explore` and `examine` left behind

- **RobMitt's popup.** A junior does not have to compose prose or answer by number. The cost is anchoring, but the shape fits someone who needs to be handed the realistic moves. Neither of ours has a first-class "not mine, send it up" answer that takes one click.
- **ericgandrade's checklist and structured close.** A junior does not know which categories of question exist. A fixed rubric teaches them, and a fixed close gives them something to paste to the team that they did not have to compose.
- **Matt's ungrillable rule and scope splitting.** Both recognise when the interview should stop, either to prototype or to break the work up. `explore` and `examine` end at "nothing material is open" but never say "this is too big for one session" or "this cannot be answered by talking."
- **Crucible's assumptions ledger and second reviewer.** Confirming assumptions in bulk up front is low load. A reviewer that is not the builder is the one mechanism in the family that does not depend on the user's judgement. In the incident, the manager was that reviewer, and the design gave him no view.
- **Crucible's critical-versus-cosmetic map.** Load-bearing does part of this, but the junior needed one number: how many of these nine can be ignored today.

### The problem, restated

- The user of a pre-build interview in a development shop is often not the owner of the answers, not a reliable courier, and not equipped to hold the fact-versus-decision line. Every version researched here treats at least two of those as given.
- The deliverable in the incident was never the interview. It was the message that had to reach the manager and the architect, in a shape they could not ignore and the junior could not reshape. No version in the family makes that the primary output.
- Culture will exploit any step that is optional. The tooling cannot fix a "just get it done" culture, but it does decide whether minimisation is invisible or on the record.

## The non-developer problem

Recorded 2026-09-03. Technical product owners, business analysts, and people in other fields are trying grill-me. The second-hand report is that they like it but do not. The specific complaints have not been collected first-hand, so this section records what each role needs, what is shared, and what the design predicts they would complain about. The predictions are inferred from the skill texts, not from anything anyone said.

The interview itself transfers to any field. What does not transfer is the environment every version silently assumes: a developer, in a repo, with a codebase to explore. Without a repo the agent has no fact source, so every fact becomes a question to the user, and the session degrades into an interrogation.

### What each role needs

- **Product owner or manager.** Decisions about who, why, scope, success measure, priority. Facts live in analytics, research, and prior decisions, not code. Feasibility is not theirs and should route to engineering. Output is a PRD or one-pager. "Ungrillable" for them means run an experiment, not build a prototype.
- **Business analyst.** Process, business rules, edge cases, data definitions. Facts live in process docs, regulations, and subject-matter experts. They are professional couriers, so the open-questions package is native to them and already has a name in their field: the RAID log. They may also find the interview competes with their own craft.
- **Scientist or researcher.** Hypothesis, controls, confounders, sample size, what would falsify. Facts live in literature and prior data, and they will want citations behind any recommendation. Ladder is PI, statistician, ethics board, funder. Output is a protocol or pre-registration. Their gate is "ready to run."
- **Executive.** Go or no-go, investment, direction. Low question tolerance, wants fewer and sharper. Reversibility is already their vocabulary: one-way versus two-way doors. Options with a recommendation is the standard decision-memo shape for them, the exact shape `examine` treats as an anti-pattern for developers, because the executive is the owner.
- **Writer, designer, marketer.** Audience, message, structure. Most of their questions are ungrillable and need a draft to react to. Matt Pocock reports people already use grill-me here, and it works because it is stateless.

### What is shared across all of them

- **The fact-versus-decision split**, but the fact source differs per role. The skill has to know where this person's facts live or it will ask them to do lookups.
- **An owner ladder exists in every field.** The rungs differ, but the top rung is the same everywhere: money, legal, safety, identity. Never batched, always stopped on.
- **Blast radius and recovery** translate without change. Every field has a word for it.
- **A named home for open questions already exists in every field.** RAID log, decision memo, pre-registration, PRD, ADR. Statelessness costs these roles more than it costs developers, because for them the decision log is the deliverable, not a step toward code.
- **The junior problem generalises.** Junior PM, junior analyst, graduate student. Same authority gap, same courier failure.
- **Ungrillable questions exist everywhere**, and the resolution artifact differs: prototype, experiment, pilot, draft.

### The seed the skill needs about the runner

None of the versions researched asks for any of this. Matt's grill-me needs no seed by design, which is what makes it portable, and it is also why a repo-less session has nothing to look up.

- **Role and seniority.** Determines what is theirs to decide and whether to derive, offer, or route.
- **Their ladder.** Who is above them and which rungs they hold. Also the inverse: the questions they must never be asked, such as a product owner on feasibility or a developer on business rules.
- **Where their facts live.** Codebase, analytics, literature, financials, process docs. The single biggest omission, and the reason a repo-less session degrades.
- **Where the output lands and who must see it.** The artifact and the escalation channel.
- **Time budget.** Rounds versus one-at-a-time is reading style; how many questions is role and calendar.
- **What is already decided.** Constraints and non-negotiables, so they are shown settled rather than asked.

### Predicted complaints, inferred from the design

- It asks me things it should have looked up.
- Its questions are engineering-flavored.
- It hands me a recommendation on something that is not my call, so I either guess or carry it.
- Too many questions for the time I have.
- The answers live in the chat and my deliverable is a document, so I retype it.
- It recommends confidently in my field and I cannot tell when it is wrong.

### Direction noted

Before this is over, the alt skills will need some form of extension so that every skill knows, at a very basic level, who it is talking to. Recorded here as intent, not as a design.

## A shared fact-sources extension

Recorded 2026-09-03. The skill does research when it needs a fact, and every team keeps its facts somewhere different. Jira, Confluence, and the codebase are the common developer case, but some teams use none of them, and some runners are not developers and have access to none of them. The idea is a file in the repo's `.agentic/` folder that, when present, tells every alt skill where to look. Recorded as an idea with the shape the research suggests, not as a design.

### Precedents in the research

- **era's per-skill extension.** `.agentic/era/<skill>/extend-skill.md` with headings including "Homework sources" and "Decision record." Human-owned, headings only until filled, read by the skill when present, ignored when absent.
- **The earlier suite's knowledge map.** A table of which home owns which kind of fact, keyed by the event that invalidates it: changes with the code, it is code; changes with the business, the business docs; changes with the work, the work tracker; derivable by search, nowhere. Plus domainspace files holding the joins between business language and code. Read by every routing skill in that suite, not by one.

The second is the better shape for this, because where facts live is a property of the team, not of the skill asking.

### The shape the research suggests

- **Repo-level, shared by every skill.** One file all alt skills read. Copies per skill drift. Per-skill extension files remain for genuinely skill-specific content, such as where approaches tend to break in a given codebase.
- **Keyed by what changes the fact, not by tool.** The invalidating-event rule is what makes the file portable. Confluence becomes SharePoint or Notion, Jira becomes Azure DevOps or Trello, the codebase becomes a process manual or a dataset, and the skill's behaviour does not change.
- **A person is a valid source.** "Business rules for billing: ask the finance lead." That line turns a fact the runner cannot reach into a question addressed to the right person, instead of a question to the runner.
- **Access and cost per source.** Who can reach it, and what to do when the runner cannot. Which tools are billable, since the Atlassian note found the search tools cost credits and the direct fetch tools do not.
- **Human-owned, short, a join only.** It maps fact kinds to homes and holds nothing another home owns. Lives in `.agentic/`, not `.claude/`, so any tool can read it.
- **Read as a file, never invoked as a skill.** Files load reliably. Skill-invokes-skill does not, as documented across this family.

### Degradation

- **Absent.** The skill infers from the environment, states its assumption in one line, and asks one question only if it found nothing: "There is a repo and a Jira connection, so I will read code and the ticket. Anywhere else facts about this live?"
- **Listed but unreachable by this runner.** The fact becomes a "look this up in X" line in the package for someone who can, never a question to the runner. The skill says once that it could not reach X.
- **Non-developer with no repo.** The file may list only documents and people. That is a complete file. The skill has nothing to search and knows it, so it does not pretend to.

### Relationship to the runner seed

This file is the team layer of the seed described under the non-developer problem: sources, the ladder, where the record lands, where output lands. It belongs to the repo or the team space. Role and seniority are the runner layer and do not belong here, because a shared repo has many runners.

### A sketch of headings

```
# Where facts live

## Changes with the code
## Changes with the business
## Changes with the work
## People who hold what nothing else does
## Access and cost notes
## Where decisions are recorded
## Where output lands
```

Each section is a few lines: the home, how to reach it, who can. A non-technical team's file might have three sections filled and the rest empty, and that is correct.

## Principles surfaced by this research

Recorded 2026-09-03. Two rules that came out of the grill-me work but are not about grill-me. They apply to every skill alt makes and to what each skill tries to do. Recorded here until alt has a doctrine home for them.

### Symptom versus wound

The number of questions a session produces is not the finding. It is a symptom. Nine questions from one story means the story was not in a ready state, and the wound is whatever made it unready: a premise the story assumes that is false, a decision it never made, a structure it gets wrong. Treat the wound and its symptoms dissolve. Treat the symptoms one at a time and the wound stays, and the person feels they did their due diligence.

- **The saga incident is the worked example.** One option treated the wound, and would have forced the conversation that rewrote the stories. Two options patched the symptom and let the developer feel finished. Those two were not merely noise. A patch presented as a peer option manufactures false due diligence, which is worse than offering nothing.
- **Fatigue is reduced by grouping, not by capping.** Questions cannot be capped, because an unready story still has to be found unready. They can be grouped under the wound they are symptoms of, ordered by how many questions treating the wound would dissolve, with the count honest but secondary.
- **Every option says which it is.** era's tags survive on merit: removes the problem, or defers it onto whom. Ask first whether the thing forcing the decision should exist at all, since removing the cause is the best disposition.
- **It is a general rule.** Every alt skill should ask what wound the thing in front of it is a symptom of before it acts on the thing. Grill-me's forty-six questions, a backlog full of stale tickets, a review with thirty findings, a plan with nine open decisions: each is a count that points at something underneath.

### Everything coaches

Every skill should coach on some level, and there are two directions.

- **Coaching the user.** In this era guards are brittle: a session can be closed and a new one opened, and any gate can be bypassed. What holds is teaching. When a skill says no, or says this is not yours, it says why, what a senior would do, and what to bring to the conversation. The mentoring payload that `explore` withheld and `examine` replaced with a derivation comes back, in plain words, aimed at the person's growth. For a junior developer this is teaching what their leadership is not.
- **Coaching the AI.** era's stances describe themselves as "the record of how the model fails in this era." Every skill that names a known model tendency and corrects it is coaching the model: edits on momentum, documents eagerly, tidies code it passes through, offers a menu when the record decides, answers its own questions. A skill that does not carry this correction inherits the tendency.
- **Make the right move the cheapest move.** Coaching is not only explanation. The developer in the incident reshaped the question because composing the escalation was hard and exposed. A skill that hands over the ready-to-send message, addressed to the owner, with the wound and the harm in it, has flipped the path of least resistance. That is coaching by design rather than by guard.

## Cross-cutting observations

**Value everyone agrees on.** Recommended answers are the key mechanic. Without them the interview is a questionnaire and the user does all the work. With them it is a proposal the user edits, which is faster and produces better-reasoned answers because the user is reacting to something concrete. `explore` and `examine` refine this rather than reject it: the recommendation is withheld or replaced with a derivation only on questions the user does not own.

**"A recommendation is a permission slip to guess" is the load-bearing insight of the owner-aware branch.** `explore` handled it by withholding. `examine` handled it by replacing the pick with a derivation. `examine`'s version is stronger because the developer still learns the analysis, but it only works when a record exists to derive from.

**Multi-stakeholder is missing from every public version.** All five assume the person answering owns every decision. None have a first-class answer of "that's not mine to decide, park it for X" that produces a list of questions to take to the stakeholder. Our two exist to fill that gap, and the mechanism is the same in both: tag every decision with an owner, attach blast radius and recovery so the owner can weigh it cold, and make the only exits explicit verbs that leave a record.

**The persistence gap is shared and solved differently.** Among the public versions only `grill-with-docs` writes anything down, via a second dependency. `explore`'s ticket comment is durable and shared but depends on the MCP. `examine`'s brief is durable and in the repo but only exists when a brief is Active; the no-brief case is conversation-only, which is grill-me's evaporation problem again. For consulting work the decision log is the deliverable, and it is the thing most at risk from context compaction in a long session.

**Each of ours is portable along one axis and coupled along another.** `explore` runs in any repo but needs Jira. `examine` runs without Jira but needs adopted doctrine. An alt version will meet teams on every combination of those two axes.

**Caps are a design choice that splits the family.** `explore` and `examine` cap on purpose: two or three options, two or three load-bearing, one-line consequences, one-line index entries, half-screen expansions, the Issue as the one uncapped block. Grill-me has no caps and treats question count as a non-goal. Both positions are argued in their docs.

**Scope splitting is external everywhere.** Runaway sessions are the most common grill-me complaint and every implementation handles it by telling the user in a doc to break the work up. None detect a tree that is too large or offer to split it. Our two avoid the symptom by triage and caps rather than by detecting scope.

**Zero questions is a success in all of them.** Never manufacture a question to justify the run. Grill-me's docs say the same, but `explore` and `examine` are the only ones whose skill text ends the interview at "nothing material is open".

**Dependency resolution does not exist across plugins.** Discussion #392 notes there is no manifest system for one skill to require another. Inside a single plugin this is under our control. Across plugins it is not.

**Skill-invokes-skill is unreliable.** Documented by the author with the widest deployment, and `examine` carries the heaviest dependency load of any version here. Any layered design has to assume the primitive sometimes does not load and either inline enough to degrade gracefully or check.

### Blast radius and recovery: not noise

`explore` put two lines on every card, "If guessed wrong:" and "Recovery:", and `examine` kept them with the rule that the consequence sentence is the severity and the recovery line is the reversibility signal. None of the five public versions carry anything like them. ericgandrade has reversibility as a question type the user is asked, which is the mechanic backwards: the agent should state it, not ask it. Assessed 2026-09-03 as one of the few genuinely novel contributions of ours, with the risk being generic wording rather than the idea.

**Why they earn their place**

- **They are the input to the ladder and the verdict.** "Brief rung only when a wrong pick is cheap" and "gates only when expensive to reverse" are both tests on the recovery line. Without it the rung is a feeling.
- **They are the false-positive control on readiness.** A gate must name the harm. "If built now, members show as enrolled with no payment record" is a gate. "This is unclear" is a question.
- **They are the teaching payload for a junior.** One line of consequence is why this is not yours, in words a junior can repeat to their lead. It carries more than a derivation with stance keys.
- **They are what the owner reads.** In the incident the manager needed the consequence sentence, not "there's a saga question." The escalation message is built from these two lines.
- **They replace severity labels.** Low, medium, high get tuned out. A concrete consequence cannot be.
- **They tell a patch from a fix.** A patch's blast radius is who it defers the problem onto, which is the wound-versus-symptom tag in operational form.

**Where they become noise**

- **Generic wording.** "Could cause issues" is worse than nothing. Name what breaks and for whom, or the card is not ready to show.
- **List views.** Two extra lines per index entry is the wall. They belong on the gate, on the card, and in the message. Never in the breadcrumb or the group index.
- **The labels.** "Blast radius" is military and reads oddly outside development. "If wrong:" and "To undo:" say the same thing in plain words.
- **Trivial questions.** On a cheap question the recovery line is one word, and its brevity is the signal.

**With the third line.** "You'd know it was wrong if," which `examine` asks only on accept, belongs beside these two on every card. The three together are the measurable heuristic on a question: what it costs, how you get out, how you would find out. One line each, concrete or omitted, shown at the moment of decision and nowhere else.

## Decided for the first version

Recorded 2026-09-03. Decisions taken so far for alt's version of this skill. Engineering stays low for the first version: the skill text alone, no seed files, no delivery layer, no eval harness. It gets run on a real story and the research collects what it did wrong.

### The team questions list

When the run ends, the skill provides a copy-pasteable bullet list of the questions that are not the runner's, so the runner can start a conversation with the team. Each bullet is labelled with who it is for. Where a story or ticket exists, the skill asks to be allowed to post the questions as comments on it, and posts only on a yes.

This is `explore`'s Open Decisions package with the ceremony removed: bullets instead of full cards, one owner label each, the post offered rather than performed. Three things carry over from the research:

- **Each bullet keeps its consequence line.** `explore` sent full cards because a shortened escalation gets minimised. A bullet list is a shortening. With "if wrong: X" on every bullet the stakes travel with the question and the list stays pasteable.
- **The owner label uses the team's words.** "For: the architect" or "for: product," whatever the ladder in that shop calls them. With no ladder file the skill names the hat and says it guessed.
- **Ask, then post, using whatever is already connected.** No adapters. If a tracker connection exists the skill offers the comment. If not, the list is the deliverable and the skill says so once.

## Open decisions for the alt version

1. **Layered or single.** A `grilling`-style primitive plus a `grill-me` front door, mirroring Matt, or one self-contained skill. Layered is the durable choice if peer-review or other alt skills will want an interview. It inherits the load-flakiness gap.
2. **Relationship between grill-me and examine.** `examine`'s description already lists "grill me" among its triggers. One option is Matt's shape with `/alt:grill-me` as a thin front door and an owner-aware examine as the primitive underneath. The other is two skills with different ambitions. The first avoids maintaining two interviews.
3. **Rounds, branches, or one-at-a-time as the default.** Rounds are fastest, one-at-a-time is most widely preferred by people who read slowly or use it as focus scaffolding, and `examine`'s branch-per-screen is the middle. An argument to switch is cheap either way.
4. **Which record substrate.** Jira ticket, brief file, or an adapter named in the repo's `.agentic/` extension so a team on Azure DevOps or GitHub Issues gets the same skill with a different delivery. The adapter is the durable choice for consulting and the most work.
5. **Derivation or recommendation, or both with an explicit degrade.** Derive when a stances file exists, fall back to a recommendation with its why when it does not, and say which mode the run is in. This is the only shape that works in a fresh repo on day one and gets better as doctrine is adopted.
6. **Keep the relay verb.** `examine` dropped it. Consulting work needs a recorded path for "the owner answered in a meeting, here is the source".
7. **Copy Matt's text near-verbatim with attribution, or rewrite in our own voice with the same mechanics.** His repo is MIT, so either is allowed if his copyright notice travels with any copied text.
8. **Provenance of `explore`.** Its text was written for an engagement, not in this repo. Confirm what is ours to reuse before any of it lands in a public MIT plugin. `era` is our own and MIT.
9. **Whether to inline enough of the ladder and the format into the skill to degrade gracefully when a dependency fails to load**, at the cost of duplicating text `era` deliberately kept in one place.
10. **A runner seed shared by every alt skill.** Some form of extension that tells each skill who it is talking to: role and seniority, their ladder, where their facts live, where output lands, time budget, and what is already decided. Stated as intent on 2026-09-03; shape undecided. The team half is sketched under "A shared fact-sources extension"; the runner half has no home yet.

## alt's first two versions: elicit and examine

Recorded 2026-09-04. Two skills were built from this research on consecutive days and run side by side. `alt:examine` is the one kept. `alt:elicit` was removed on 2026-09-04; its skill text, README, and design record are in git history at commits `3269f9d` and `ab44957`.

### What elicit was

Built 2026-09-03. A pre-work interview that held the fact-versus-decision line for the runner and decided ownership on their behalf.

- Assumed a runner hat, Implementation Dev by default, stated on the first screen and correctable in plain speech.
- Ran homework, a two-part hunt, and a five-step refute in order: is it a fact, does the record settle it, should the cause exist, is it cheap and the runner's, otherwise whose. Only the fourth step's survivors reached the runner; the rest were routed to a hat with one line on why it was not theirs.
- Opened with a first screen: a verdict out of four, wound and question counts, up to three wounds with owner and harm, the runner's own pile as an index, one ask. Twenty lines.
- Walked one question per screen with a breadcrumb of what was still coming, re-deriving after every answer and showing deltas.
- Named a gate when four conditions held, which reshaped the verdict to conversation first.
- Closed with the decided list, the copy-pasteable team list with owner and if-wrong on every bullet, an offer to post to the record, and a handoff line. Then stopped.
- Introduced presets, the extension file, and the sources file, and the literal-word trigger.

### Why examine replaced it

- **Complexity lived in the skill.** Against Matt Pocock's `grilling`, at 2KB with three concepts and one template, elicit was 10.7KB with about twelve named concepts and eight templates. Rated in this repo: grilling engineering 4, complexity 1; elicit engineering 3, complexity 4. Grilling's rationale, limits, and acceptance checklist live in a doc; elicit's lived in the skill text, along with line budgets asked of a renderer that does not hold them. The headless runs produced eighteen to twenty-five lines for a twenty-line screen, every run different.
- **It modelled who the runner is.** The runner hat and the yours-or-not-yours split assumed the skill could know the person and decide for them. Reversed on 2026-09-04: the skill does not take into account who is running it, only what kind of work it is. A preset names the field, never the person. The questions the junior in the incident received that were not theirs should have been answered months before the ticket reached them; the win is to surface those questions and show plainly when one needs a larger conversation rather than a quick patch, not to withhold them.
- **The first screen forced serial homework.** The verdict and counts on line one needed the whole picture before the first question, so every lookup finished before anything was asked. Grilling's frontier lets a sub-agent chase a fact while the rest of the round is asked, and only the dependent questions wait. Dropping the first screen made that available.
- **Prose that said the same thing twice.** A review-prose pass on examine found about 2,300 bytes of duplicated rules, glosses, and prose describing what a template already showed. Elicit had more of the same.

### What examine is

Grilling's flow with this research's additions on every question. Design tree, frontier, rounds; wounds are roots, so they come first on their own with nothing announced. Each question carries why the seed does not settle it, two or three options tagged fixes or defers onto whom with a patch never a peer of a fix, the recommendation, if-wrong, to-undo, and could-help. When a question needs a team conversation the recommendation says so and drafts the line to send; money, legal, safety, and identity always take that shape. Verbs: a number, yes, share, more, settled, or plain speech. The close tallies decided, shared, and settled, gives one read out of the same four, hands over the team list with if-wrong on every bullet, offers the post, asks what next, and stops. 5,364 bytes after the verbosity pass, model-invocable on the literal word "examine" only.

### Carried from elicit into examine

Facts are never questions, each with its source. The refute steps that remove non-questions: settled by the record, should the cause exist. Wound as a premise the seed gets wrong or a decision it never made. Patch never a peer of a fix. The small artifact for a question that needs something to react to. "Given what you've said" on taste questions. The copy-pasteable team list with the stakes on every bullet, post only on yes. Zero questions is a success. Never build, never plan mode, never act on an answer not given. Presets, now at `plugins/alt/presets/` with developer as a file beside business and research, minus the Runner hat heading. `.agentic/sources.md` and `.agentic/alt/examine/extend-skill.md`, read if present.

### Dropped, and why

- The runner hat and ownership routing. Replaced by could-help, which is help, not ownership, and by the share verb, which lets the runner hand any question to the team.
- The first screen, the verdict up front, the breadcrumb, and the gate as an object that reshapes the session. The read is tallied at the close; a question that must go to the team is a recommendation to share it.
- Line budgets. Shapes are shown once as templates with normal-word placeholders; nothing counts lines.
- The third consequence line, "you'd know it was wrong if." Examine carries if-wrong and to-undo. Argued for above under "Blast radius and recovery"; dropped for weight. It can return if its absence is felt in use.
- Worked examples in templates. A payments story anchored every run toward engineering. Placeholders carry the shape.

### Open decisions this settled

Of the ten listed above: 1, single skill, no primitive and no passthrough, after two skills were tried and one kept. 2, examine is the one interview and `grill-me` is not a front door to it. 3, rounds, after one-at-a-time was tried in elicit. 5, recommendation with its why; no derivation, since no stances exist to derive from. 10, the runner half is rejected rather than undecided: no alt skill models who is running it. The team half stands as the sources file. Decisions 4, 6, 7, 8, and 9 remain open.
