# Orient: research notes

Started 2026-09-09; the lineages read 2026-09-16. Research behind the roadmap's orient skill, brief-level and project-level. Eight lineages in our own repos, 2025-10 to 2026-08, under three command names: `/start`, `/session`, `/orient`. The intent, the references, what each lineage is, where they disagree, and the carried-forward candidates are written. The shape is not decided.

**This doc holds concepts to consider.** Being here is not a vote to keep. Each item earns its place, or does not, when the skill's shape is decided.

## Intent, 2026-09-09

Story, epic, triage, and orient itself all need to know where to go for information. Orient is the shared answer. Run in a folder or repo, it learns what kind of project this is from the CLAUDE.md file and the extension file, and learns the listed information sources from them. Codebases are the common case and not the only one: a project can be a proposal, a study, or an offer with no code in it, and orient has to work there too.

## References

Five groups: what this repo already holds, what to verify about Claude Code, our lineages, public precedents, and the books. Primary first within each.

### In this repo

- **`grill-me.md`, "A shared fact-sources extension".** The `.agentic/sources.md` idea: one repo-level file every alt skill reads, keyed by what invalidates a fact (changes with the code, the business, the work) rather than by tool, with people as valid sources, access and cost per source, and degradation rules for absent and unreachable. Orient is the skill that reads it, and the candidate for writing it.
- **`grill-me.md`, "The seed the skill needs about the runner" and "Relationship to the runner seed".** The team layer (sources, record, where output lands) belongs to the repo; the runner layer was rejected: no alt skill models who is running it. Orient is the team layer.
- **`plugins/alt/presets/`.** Developer, business, research: the kind of work. The extension file's `## Preset` heading is already the hook a skill uses to learn which one applies. "What kind of project is this" and "which preset" may be the same question.
- **`plugins/alt/skills/examine/SKILL.md`, Inputs, and `brief-create/SKILL.md`, Inputs.** Both read `.agentic/sources.md` and their own `.agentic/alt/<skill>/extend-skill.md` if present. brief-create's extension has `## Preset`, `## Close`, and `## Load`. Orient produces or refreshes what they consume; the contract between them is those files.
- **`brief.md`, "Open decisions, resolved 2026-09-16" and "Also decided".** Listing and resuming briefs are orient's job. No resume check: the brief lists its branches, git says whether they are behind, validity is the owner's call. Briefs live in `.agentic/briefs/`, closed ones in `closed/`, and are never committed.
- **`skill-development.md`.** Coupling: shared content is a file read by path, named by concept, with absent behaviour stated. Cost: what one invocation loads before it does anything. Shape: a skill knows when not to run.
- **`.project/roadmap.md`, knowledge-map.** "May be a file convention under `.agentic` rather than a skill." The same question applies to orient: a skill, a file convention, or a skill whose job is to write the convention.

### To verify about Claude Code

- How CLAUDE.md resolves: project, user, nested folders, imports. What of it is already in a session's context, so orient does not re-read what is already loaded.
- What a plugin skill can read of the host repo and of `.claude/`, and why the sources file lives in `.agentic/` (any tool can read it) rather than `.claude/`.
- The built-in `/init`, which orients to a codebase and writes CLAUDE.md. What orient adds beyond it is an open decision, and the non-code case is the obvious first answer.

### Our lineages, in time order

All ours except melon-local, a client engagement; `brief.md`'s provenance decision covers the rest. The brief files of the five `_temp` lineages are listed in `brief.md`; this list names their session-start files.

- **ArchType, 2025-10-13 to 2025-10-29.** `~/Development/_temp/ArchType`. `.claude/commands/start.md`, one line pointing at `docs/development/workflow/session-start.md`; `MISSION.md` at the root; `docs/development/status/current-phase.md`, the hand-maintained state file; `docs/TAG_INDEX.json`. `_wrap-up-retro/workflow-ritual.md` and `workflow.md` are the 2025-10-29 retro on the ritual.
- **old-ai-workflow, 2025-10-30.** `~/Development/_temp/old-ai-workflow`. `.claude/commands/start.md` and `docs/workflow/session-start.md`, the project-agnostic copy; `docs/context/MISSION.md` as a fill-in template.
- **archtype-framework-proof-of-concept, 2025-11 to 2026-01.** `~/Development/_temp/archtype-framework-proof-of-concept`. `.claude/commands/start.md`; `.claude/docs/workflow/session-start.md`, 58 lines, rewritten 2025-12-12 (commits ca6d510, 6faef0b); `phase-workflow.md`. `project-docs/framework-stories/completed/brief-system-redesign.md`, Phase 4, is the record of the rewrite.
- **melon-local, 2026-02-10 to 2026-06, a client engagement.** `~/Development/melon-local`. `.claude/commands/session.md`, added 2026-02-10 (a77c1c8), the day before the brief system landed; `brief-check.md`; the file map in `CLAUDE.md`. Engagement work: confirm what is ours to reuse before any text lands here.
- **page-play, 2026-02.** `~/Development/_temp/page-play`. `/start` renamed `/session` 2026-02-12 (2a059a5); `.claude/commands/session.md`, `.claude/docs/workflow/session.md`.
- **ai-brief-workflow, 2026-03-31.** `~/Development/_temp/ai-brief-workflow`. `.claude/commands/session.md`, `.claude/docs/workflow/session.md`, `.workflow/config.md` with its Session Reads list.
- **The earlier suite**, `~/Development/agentic-temp/summary.md`: the `/orient`, `/handoff`, `/knowledge-map and /orient-sync`, `/backlog-standards`, and team-standards sections. `skills.md`: the `.agentic/` convention, the jurisdiction table, the domainspace format contract, and the orient-sync skill text with its audit checks. The `/orient` skill text itself is in neither file; the summary is the reference. Source not located; provenance as in `brief.md`.
- **era, 2026-08-23 to 2026-08-30, ours and MIT.** `~/Development/era/plugins/era/skills/orient/`, `orient-brief/`, `orient-project/`, each survey with an `extend-skill.template.md`; `.agentic/era/orient-brief/extend-skill.md` and `orient-project/extend-skill.md`, headings only. All three created at 78d4868 and never renamed. 5c7660c (3.0.0) changed the recommended next beat from explore to examine; ec104f5 (3.2.0) marked `done/` as retro's alone.

### Public precedents

- **`/init`**, Claude Code's built-in. Orients to a codebase and writes CLAUDE.md.
- **The `/init` camp as the earlier suite named it**, not independently checked: community "prime" commands, Aider's repo map, Cursor rules. All "build a technical map and persist it as ambient memory."
- **everything-claude-code, `codebase-onboarding`.** Local copy `~/Development/_tools/everything-claude-code/skills/codebase-onboarding/SKILL.md`, read 2026-09-16. Reconnaissance, architecture map, then writes an onboarding guide and a starter CLAUDE.md. The `/init` camp; code only.
- Matt Pocock's `wayfinder` was checked 2026-09-09 and is not a precedent: it plans large work as decision tickets on an issue tracker. Noted for epic, not here.

### Books

Local copies are markdown files in `~/Downloads/books/`. Each line says what the book has an opinion on here.

- **Thinking in Systems**, Donella Meadows. Map the system before intervening: stocks, flows, feedback loops, and the purpose a system reveals by what it does. Orientation is the map.
- **User Story Mapping**, Jeff Patton. The map as the shared big picture of a product. Project-level orientation to what is being built and why.
- **Continuous Discovery Habits**, Teresa Torres. The opportunity solution tree as the current state of a team's thinking: what is in flight and what was set aside.
- **Inspired**, Marty Cagan. Product vision, strategy, and principles: what a newcomer must know before touching anything.
- **Lean Analytics**, Alistair Croll and Benjamin Yoskovitz. Which stage the product is at, since the stage decides what matters now.
- **The Product-Minded Engineer**. Orienting to the business behind the code.

Considered and not listed: Accelerate, Empowered, Evidence Guided, Lean UX, Measure What Matters, The Lean Product Playbook, The Lean Startup. Their opinions are on the artifacts orient points at, not on orientation. The Design of Everyday Things and The Startup Way are not about this.

Related in this repo: `story.md`, `epic.md`, `triage.md`, the skills that consume what orient learns. `grill-me.md`, the incident behind the fact-versus-decision line, which orient exists to hold from the fact side. `brief.md`, the unit of work orient opens against.

## What each lineage is

### ArchType and old-ai-workflow: the session start protocol

One entry point, `/start`, reading a fixed list and then choosing a mode.

- Step 1, read core files, "every session": MISSION.md, TAG_INDEX.json, current-phase.md. old-ai-workflow drops current-phase.md and reads the briefs folder instead: "Briefs track STATE."
- Step 2, collaboration discipline: a table of modes, what the human says, what the AI does, what the AI never does. Signals that stop everything: "something feels off", a directive in the wrong mode, an architecture question mid-implementation, context collapse.
- Step 3, does the human need a brief. Step 4, identify the mode and read that mode's doc.
- "Where are we?": read the status file, list active briefs, load ADRs by tag, then "Present to user, let them decide next action." "This file defines PROCESS. docs/status/ tracks STATE. User chooses path."
- MISSION.md is the recovery artifact, created 2025-10-14 after early mission drift, read first every session "no exceptions", and near-immutable.
- The ritual around it: restart the session after every stage and every implementation phase. "Fresh context = clean boundaries"; "each stage loads only what it needs." The restart checklist: committed, brief updated, tests green, clear stopping point. `/start` is what made the restart cheap.
- The retro's evidence: 23 briefs in 16 days and zero "what was I working on?" moments.
- The cost: current-phase.md was a third state source kept by hand, and it repeated phases, counts, and next steps that the briefs also held.

### The redesign and page-play: start becomes session

- brief-system-redesign, 2025-12-12, Phase 4, "Simplified entry points and commands." The mode table and the identify-your-mode step removed entirely; the `/start` to `AI_START.md` to `session-start.md` chain called "unnecessary indirection"; the mode commands `/explore`, `/plan`, `/implement` deleted. Result: 58 lines from 103.
- The flow that survived: read core docs, ask "What are you working on?", then one of three. New work: create a brief and start Phase 1 research. Existing brief: read it, find the first incomplete phase, follow the phase cycle. Quick task: confirm scope is small, execute, "no ceremony required." The quick-task path is in the 2025-12-12 file; it is not a page-play addition.
- Collaboration signals kept in short form: uncertainty pauses; context collapse means smaller slices or more reading before acting.
- page-play renames `/start` to `/session` on 2026-02-12 and swaps the core docs for the framework's READMEs. Nothing else moves.

### melon-local and ai-brief-workflow: list, don't read; check for contradiction

- melon's `/session` opens "You are resuming a multi-session working exercise." Reads OPEN_ITEMS. Lists the briefs folder "but don't read them until we decide what to work on. Brief context is loaded on demand, not upfront." Excludes completed, needed-work, and the template. Closes by listing every file loaded, full path, and every active brief present but not loaded, then asks what the session is about.
- melon's `/brief-check` is the audit a brief gets when idle: completeness, consistency, actionability, handoff readiness. Manual and per brief.
- ai-brief-workflow moves the reading list out of the workflow doc into the project layer: `.workflow/config.md`, "Session Reads: files to read at session start, in order", default `README.md` alone. Then "summarize where the project stands and what's active."
- Its Step 2 is new: "Does anything decided since the last session contradict what was just loaded? If yes, surface the conflict before proceeding. Don't silently carry stale assumptions forward."

### The earlier suite: orient as routing

Orient exists so that "developer and Claude share the same understanding of the business area a task touches before any code is written." The failure it names: "Agents that jump straight to code misread the business intent. Technical repo maps do not say which business boundary you are inside or what the terms mean."

- "The output is an alignment artifact, not a document. Orientation is a ramp into work. It ends in a confirmed brief plus 'what do you want to start on', never in a file. Nothing is written anywhere. That refusal is what separates it from /init."
- Sources, not archives: Jira for state, Confluence for rules, domainspace for joins, code for behavior, each read live.
- Progressive disclosure per source: "Root file, then a menu of boundary first lines, then exactly one boundary file, then its landmark symbols. Each source is taken only as far as the task needs." The developer confirms or overrides the proposed boundary.
- Degradation is output: "The brief says what each contributed and which were absent, so the human can audit the degradation." Every source optional, Jira included.
- Resume is gated. A handoff doc is checked against branch, its reality command, working-tree state, and its stale-after date; a stale or diverged verdict is shown verbatim and the human chooses. "Never proceed past a divergence unilaterally." The ticket is always still read, because questions parked there since the doc was written are invisible to the doc.
- Refuses: sweeping the repo, transcribing Confluence, reading an epic's children in full, persisting what it fetched, re-deriving a fact another home owns.
- The order: invoke the knowledge map first, then the ticket with its epic's summary and child titles, then the domainspace menu and one boundary, then that boundary's Confluence area, then the code from its landmark symbols.
- The fallback with no domainspace is "the README-then-seams recipe everyone uses", with a domain lens: shared-database integration, duplicated models, logic in stored procedures, migrations in flight, weak anti-corruption layers, overloaded vocabulary. Observations of that kind go to Jira, never into a file.
- What it reads was written by a separate skill. `/orient-sync` is "a deliberate, lead-run task": bootstrap when the root file is absent, audit when present. Bootstrap inventories structure, not code, reads the business sources, interviews the lead briefly, drafts, and hands off by PR. Audit runs nine checks, each naming the two sources it compares, scoped to one boundary or a date range, never a whole-repo sweep. "Draft, never decree."
- The knowledge map beneath both: "Every fact has exactly one home, determined by what event invalidates it." The routing rule: changes with the code, it is code; with the business, Confluence; with the work, Jira; a mapping between two of those, domainspace; derivable by search, nowhere. Ephemeral gitignored files are outside the map and may restate freely.
- One thing is ambient: the repo's CLAUDE.md imports the root domainspace file "so vocabulary traps fire in sessions that never run /iba:orient." Only the root; boundary files are menued.
- The suite's global CLAUDE.md block sat above "the workspace orientation file and domain map (a repo and context map, orientation only)", above each repo's CLAUDE.md. A workspace-level orientation layer existed; the summary says no more about it.

### era: a dispatcher and two surveys

- `era:orient` "decides which orientation fits the moment and hands off." Two signals only, the briefs' Status and Current phase lines and the branch name; "no history, no roadmap, no deep reads." A brief signal gets one question with that brief's specifics; several Active briefs get listed; no signal goes straight to the project survey.
- Both surveys open the same way: "Orientation is provisioning, not ceremony: the deliverable is a confirmed picture in the conversation." It writes nothing, starts nothing, and its report dies with the session.
- `orient-brief` resolves the brief down a ladder: the branch name matching a brief's file name, then the single Active brief, then ask. No brief is not an error; orient around the intent in the room. Deep on the current phase, including the code in both directions, what the change will impact and what constrains it. Light on the rest, with each done phase's claims held against git. Surfaces the phase's open questions by id and recommends examine "plainly; never invoke it."
- `orient-project` reads the briefs for status, phase, and age, where age is "never a field in the brief" but the file's last commit date, a second source; the queued work; and movement, the last ten commits and the branches that exist. "Do not go deeper than the survey."
- Arguments are "an intent expression, not a parameter." Bare has a default; "but also B and C, I want to weigh them together" reshapes the survey.
- Divergences: "every anomaly as two named sources disagreeing, both sides quoted." Raw facts only, ages and dates, never thresholds or verdicts; the reader is the judge. What the sources agree on needs no line.
- Four principles shared by both: sources not archives; two sources or it is not a finding; degrade gracefully, absence is information; hand the wheel back. "What happens next is frequently not the logical next thing; the user owns the deviation."
- Each survey reads `.agentic/era/<skill>/extend-skill.md` under two headings, Deviations and Landmarks. era's own copies are empty.

## Where they disagree

- **Where state is read from.** ArchType kept a status file by hand beside the briefs and MISSION.md. From old-ai-workflow on, the briefs are the state. era adds git as the second source: age, movement, and the brief's own claims checked against history. The earlier suite puts state in Jira and lets the repo hold joins only.
- **A fixed reading list or routed reading.** ArchType through ai-brief-workflow read a list of files every session, in order; ai-brief-workflow made the list configuration. The earlier suite has no list: route through the map and take each source only as far as the task needs. era reads two signals, dispatches, then runs a fixed survey with every item optional.
- **What orient knows about the business.** ArchType: MISSION.md, first and always. The earlier suite: the ambient root domainspace and menued boundary files, written by a separate skill. era, melon, and ai-brief-workflow: nothing of their own; the repo's docs or the brief's Context to Load carry it. alt's intent: CLAUDE.md and the extension file say what kind of project this is.
- **Whether orient writes.** Nothing since the redesign writes at session start. The earlier suite states the refusal as its identity and moves the writing into `/orient-sync`, lead-run and PR-gated. The `/init` camp writes a CLAUDE.md or a guide. ArchType wrote nothing at start and paid for it with a hand-maintained state file.
- **One level or two.** Only era splits brief-level from project-level and adds a dispatcher. Every earlier version is one entry point that asks; melon's is project-level only, with the brief read on demand as the unnamed brief-level half.
- **Verification on resume.** The earlier suite gates on ground truth. era reports divergences. ai-brief-workflow asks the conflict question. ArchType verified nothing at start and relied on the close checklist. brief.md, 2026-09-16, decided none of these for alt's briefs: the brief lists its branches, git says whether they are behind, validity is the owner's call.
- **Mode.** ArchType chose a mode at start and read that mode's doc. Everything after drops the choice. examine is what survived of it: what is not yet known decides what happens next.
- **The report's shape.** melon lists what it loaded. The earlier suite names what each source contributed and which were absent. era gives a paragraph, the live briefs, the queue, the divergences, and the absent sources. ArchType presented the status file.
- **The non-code project.** None handles it. Each depends on its own substrate: doc trees and briefs, Jira and Confluence and domainspace, `.project/briefs` and git. The intent names this as the first thing orient adds beyond `/init`, and no lineage has an answer to borrow.

## Carried-forward candidates

- The earlier suite's frame: orientation is a ramp into work, ending in a confirmed picture and "what do you want to start on", never a file. era's words for it: provisioning, not ceremony.
- Sources, not archives. Read live, persist nothing, let the report die with the session.
- Every source optional, absence named once, and the report says which sources contributed and which were absent. melon's list of what was loaded is the other half of the same audit.
- Two sources or it is not a finding; raw facts and dates, never verdicts. Born in orient-sync's audit checks, carried into era's divergences, already listed in `brief.md`.
- Age and movement from git, never a field the brief holds.
- List the briefs, read none until one is chosen. era's two-signals rule before dispatch is the same discipline.
- Progressive disclosure per source: root, menu of first lines, one file, its landmarks. Take each source only as far as the task needs.
- ai-brief-workflow's conflict question on every load of prior decisions.
- Offer, don't force: the human gates every resume, and a divergence is never crossed unilaterally.
- Arguments as an intent expression with a bare default.
- Hand the wheel back: report, recommend the obvious next beat, ask, start none of it.
- The knowledge jurisdiction rule, one home per fact keyed by what invalidates it, as the ancestor of `.agentic/sources.md`, with its exemption for ephemeral files.
- The earlier suite's split of reading from writing: orient reads, a separate lead-run skill writes, PR-gated, draft never decree.
- Session Reads as configuration in the project layer, the ancestor of era's extension file and alt's `## Load`.
- The pairing of a start ritual with a close ritual. ArchType's restart checklist is what made `/start` reliable, and brief-create's close items hold that place now.
- The earlier suite's domain lens for a repo with no map: shared database, duplicated models, stored-procedure logic, migrations in flight, weak anti-corruption layers, overloaded vocabulary.
- Not to carry: a hand-maintained state file, a mandatory mission read, mode selection at start, a reading list read every session regardless of task.

## Open decisions

1. Skill, file convention, or both. The earlier suite was both: a reading skill, a writing skill, and a file format between them. The roadmap's knowledge-map line asks the same question.
2. What orient adds beyond `/init`. The candidates so far: it does not write, it reads briefs and git, it works on a project with no code, and it knows where this team's facts live.
3. One level or two. era's dispatcher plus two surveys, one entry point that asks as every earlier version did, or two skills. `brief.md` decided that listing and resuming briefs are orient's job.
4. How orient learns the kind of project. CLAUDE.md, the extension file's `## Preset`, inference from what is in the folder, or ask. Whether kind of project and preset are one question.
5. What, if anything, is ambient. The earlier suite imported the root domainspace into CLAUDE.md so that sessions that never orient still see the vocabulary. Whether `sources.md` or any root file earns an import line.
6. Whether orient writes `sources.md`, and under what gate. The earlier suite's answer is a separate skill, lead-run, PR-gated.
7. The non-code case: what stands in for briefs, git, and code as sources, and what movement means for a proposal, a study, or an offer.
8. Whether orient holds a brief's claims against git, as era does, or leaves validity to the owner, as `brief.md` decided for the resume check.
9. The report: whether it names what was loaded and what was absent, and how much of era's shape to keep.
10. What is already in context before orient reads anything: the CLAUDE.md items under "To verify."

## Decided 2026-09-16

Examined with alt:examine; the record is `grill-me.md`, "Decided 2026-09-16".

- Open decision 1: a file convention plus a drafting skill. `.agentic/sources.md`, five seats, three lines each; `alt:sources-sync` drafts it.
- Open decision 6: sources-sync writes it, on the runner's go, committed and PR-gated. Orient stays read-only.
- Open decision 5, what is ambient, is not this skill's and stays open for orient.
- Dropped as over-engineering: a plugin-level knowledge-map file, preset rewrites, a CLAUDE.md import written by a skill, a `.docs/` scaffold.

## To write

- Summary.
- The problem the skill solves, and for whom.
- Brief-level and project-level: what each answers, and for whom, once decision 3 is made.
- What orient reads, in what order, and what it writes, if anything.
- Kind of project: how it is detected, when to ask instead of infer, and the non-code case.
- Relationship to `/init`, the presets, examine, brief-create, and the three artifact skills.
- Degradation, one line each.
- Public precedents beyond the `/init` camp, if any claim to orient without writing.
