# elicit

A pre-work interview for anything you are about to act on: a story, a ticket, an idea, a plan, a study, an offer. It reads what can be read, finds the decisions the seed silently assumes, asks you only the ones that are yours and cheap to get wrong, and hands everything else to its owner as a copy-pasteable list that carries its stakes.

Invoked as `/alt:elicit`. First version, 2026-09-03. Design and decisions in [`.project/design/elicit.md`](../../../../.project/design/elicit.md); the research behind them in [`.project/research/agentic-skills/grill-me.md`](../../../../.project/research/agentic-skills/grill-me.md).

## What we set out to fix

The grill-me family of skills does one valuable thing: it interviews you about a piece of work until nothing material is assumed, and the questions are usually good. We researched seven implementations, including two of our own, and found they all share one flaw. They are written by seniors, for seniors, and they assume the person at the keyboard is the owner of the answers, or at least a reliable channel to one.

In an ordinary development shop that person is often a junior. The incident that drove this skill: a junior ran one of our earlier interviews and it correctly found a distributed-transaction risk, offered one real fix and two quick patches, and raised eight more questions, six of them for the business. Told by both the coach and the manager to send every question to the team, the developer instead reshaped the one hard question into a yes/no about the quick patch and sent that with no context. The detection worked. The delivery relied on the least powerful person in the room performing the hardest social act in the room, against the culture they live in.

Every version in the family fails that person in the same ways:

- **The fact-versus-decision line is held by the user.** A senior knows "that's a lookup, not my call." A junior treats every question as one they must answer.
- **The junior becomes the router.** Business, architecture, and legal questions land on the person with the least authority to route them and the most pressure not to.
- **The menu is the trap.** One real fix beside two straw-man patches reads as three options to someone who does not know better, and the one that closes the ticket wins.
- **Volume is the whole feel of the tool.** A senior filters forty questions. A junior sees forty blockers.
- **A developer's world is baked in.** Non-developers trying these skills like them and do not. Without a codebase the agent has no fact source, every fact becomes a question, and the session degrades into an interrogation in engineering vocabulary.

elicit keeps the interview and moves the burden off the runner:

- **It holds the fact-versus-decision line itself.** Facts are never questions. It reads the code, the ticket, the docs, and whatever the team says it keeps, and looks things up instead of asking. Every fact names where it came from.
- **It asks the runner only what is theirs.** A question reaches you only when it belongs to your hat and a wrong pick is cheap to undo. Everything else is routed to its owner with one line on why it is not yours.
- **The team message is the deliverable, not an afterthought.** Every routed question leaves as a bullet with who it is for, in the team's words, and what breaks if it is wrong, so it cannot be shrunk on the way.
- **It groups by wound, not by count.** Many questions are usually symptoms of one premise the seed gets wrong or one decision it never made. The wound is what gets shown; the questions hang off it. A patch is never offered as a peer of a fix.
- **It teaches without lecturing.** Guards are brittle in this era: anyone can close the session and open a new one. So the reasoning behind a question travels with it, in one line, and no line exists only to instruct.
- **It knows whose world it is in.** The mechanics are field-neutral. The words and defaults come from a preset, so a researcher is asked about a protocol and a PI, not a ticket and an architect.

The measure of a run: how few decisions the runner had to make, that none of them could hurt, and that the team can act on the rest. Coverage is never reduced to get there. Question count is not capped; the caps are on how much lands on one screen.

## How to use it

### Invoking

The word "elicit" has to appear. Paraphrases such as "grill me" or "what am I not deciding" do not fire it, by design.

```
/alt:elicit PLAT-412
/alt:elicit Story: when a member completes enrollment, call ...
/alt:elicit business Idea: a fixed-price two-week readiness assessment ...
let's elicit that
```

The seed is whatever follows, or whatever is already in the room: a ticket key when a tracker connection exists, a pasted story, an idea, or the conversation so far. It never re-asks what the conversation already answered. An optional first word names a preset; see below.

Other alt skills and workflows can invoke it too. It ends by stating what is ready and what waits, then stops, so a caller keeps its own next step.

### What happens

1. **Homework, silently.** It reads the files the work touches, the ticket or record, the repo's docs, and every source named in `.agentic/sources.md`. When there is no code it names what it will read and asks once what else to read. Anything those answer is a fact and never becomes a question.
2. **Hunt and refute.** It looks for what the seed leaves ambiguous and for where the proposed approach breaks, from six angles. Then every candidate gets a targeted attempt to kill it before it can reach a person: is it a fact, does the record settle it, should the thing forcing the decision exist at all, is it cheap and yours. Only survivors become questions.
3. **First screen.** Twenty lines or so. The verdict and counts on line one, your assumed hat, up to three wounds with what breaks if you proceed now and who owns each, then your own questions as a one-line index with the recommended answer marked. The last line asks whether to start.
4. **The walk.** One question per screen, with a plain-words breadcrumb of what is still coming. Each shows the decision, why the seed does not settle it, three consequence lines, and two or three options tagged as fixing the problem or deferring it onto someone. After each answer it re-derives: an answer can add, retire, or move questions, change an owner, change the verdict, or open a gate, and you see only the deltas.
5. **The close.** What you decided, one line each. The team list, copy-pasteable, one bullet per routed question with its owner and its if-wrong line. An offer to post the list to the record when one exists and it can write there, posted only on yes. One line on what is ready to proceed and what waits on the team. Then it stops.

It never builds, never enters plan mode, never acts on an answer it was not given, and never proceeds past an unanswered gate.

### Answering

Every screen ends with the same ask. You can reply with:

- **A number, or yes** for the recommendation. **All yes** on the first screen takes every recommendation.
- **not mine Q4** to send a question to the team list instead of answering it.
- **more Q4** to expand a question to half a screen.
- **settled** to see the decisions the record already settled, with their sources.
- **Plain speech.** "I'm actually the tech lead" corrects your hat. "That gate isn't real, proceed" is honoured and the reason goes in the close. "Tell me what's off" is always a valid answer.

### Verdicts

- **Ready.** Nothing material is open. Zero questions is a success.
- **Ready with questions.** Most runs land here. You can proceed on your own decisions; the team carries the rest.
- **Conversation first.** One gate is open: the record is silent, a wrong pick is expensive, it is not yours, and proceeding now causes a named harm. The message is drafted. Your own questions are still walked so you reach the conversation with your decisions made.
- **Not workable.** One screen on why and what would make it workable. The team list is still offered.

### Re-running

Run it again on the same seed and it carries the question ids forward, treats earlier dispositions as settled unless you reopen one, and says what closed. A ticket named mid-walk is read then and reconciled the same way.

### The words it uses

- **Seed.** The thing being interviewed.
- **Runner.** You, the person at the keyboard.
- **Hat.** A role that owns a kind of decision. Developer default: Implementation Dev, Tech Leadership, Business, UX.
- **Record.** Where settled decisions live: code beside the work, the ticket's constraints, the docs, or whatever the preset names.
- **Wound.** A premise the seed gets wrong, or a decision it never made, with several questions hanging off it. One small question is not a wound.
- **Gate.** A question that must be answered by its owner before work is safe to start. Expect zero or one.
- **The small artifact.** What to make when talking cannot settle a question: a spike or prototype for developers, a pilot or one-pager for business, a pilot or power analysis for research. The question is parked, not asked.

## How to extend or override it

Four layers, cheapest first. Nothing below changes the mechanics: the refute order, what makes a gate, the three consequence lines, the never-batched rule for money, legal, safety, and identity, and the promise never to build. Those change only by editing the skill.

### 1. In the session

Most steering needs no file. Correct your hat, send a question up with "not mine", contest a gate, ask for the partition on a conversation-first verdict, or say what is off in plain speech.

### 2. Presets

A preset is a one-screen file that swaps the words and defaults for a kind of work. `developer` is the inline default and costs no read. `business` and `research` ship in [`plugins/alt/presets/`](../../presets/), shared by every alt skill that takes a preset.

Select one by first argument, or set it once per repo in the extension file so nobody types it twice:

```
/alt:elicit research Study idea: ...
```

```markdown
# .agentic/alt/elicit/extend-skill.md

## Preset
research
```

A preset may change, and only change:

| Heading | What it swaps |
|---|---|
| `## Runner hat` | Who the runner is assumed to be |
| `## Hats` | The owner list questions route to |
| `## Record and where facts usually live` | Where settled decisions and facts are found in this kind of work |
| `## Ready means` | The words for the verdicts |
| `## The small artifact` | What to make when a question needs something to react to |
| `## Words` | Renames for fixed strings: "if done now", the record, the team message, the verb for proceeding |
| `## Also` | Field rules on top of the never-batched rule, such as participant safety routing to the Ethics board |

To add one, copy an existing preset, keep the headings, keep it to one screen, and name the file for the first word people will type. A preset that starts describing how to interview is doing the skill's job and should be cut back.

### 3. The repo extension file

`.agentic/alt/elicit/extend-skill.md` holds what only this repo or team knows. Read when present, ignored when absent, at zero cost. Today it can:

- Name the default preset under `## Preset`.
- Rename, add, or remove hats, so questions route in the team's own words: "the architect", "product", "the finance lead".
- Name the record and where it lives.
- List where approaches tend to break in this codebase or this domain, which feeds the break hunt.

Only `## Preset` is a fixed heading so far. For the rest, use the same headings the presets use and add `## Where approaches break here`; the skill reads the file as prose and those names are the ones it already knows. The headings are provisional until the shared extension design across alt skills is decided, so expect them to settle, not to stay.

### 4. The shared sources file

`.agentic/sources.md` tells every alt skill where this team's facts live and who can reach them. It is a join, not a knowledge base: a few lines per source saying where it is, how to reach it, and who can. A person is a valid source. "Business rules for billing: ask the finance lead" turns a fact the runner cannot reach into a question addressed to the right person instead of a question to the runner.

Key sections by what changes the fact rather than by tool, so the file survives a move from Confluence to Notion or from Jira to Azure DevOps. The sketch from the research:

```markdown
# Where facts live

## Changes with the code
## Changes with the business
## Changes with the work
## People who hold what nothing else does
## Access and cost notes
## Where decisions are recorded
## Where output lands
```

A non-technical team's file might fill three sections and leave the rest empty. That is a complete file.

### When something is missing

Each of these degrades in one line, at the moment it happens, and the run continues:

- No sources file: it infers from the environment and states the assumption.
- A source is listed but unreachable by you: it becomes a "look this up in X" bullet for the team.
- No way to write to the record: the team list is the deliverable.
- No code here: it names the files it will read and asks once what else to read.
