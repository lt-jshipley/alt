# Brief: research notes

Started 2026-09-09. Research behind the roadmap's handoff / briefs item, which the runner calls briefs: the unit of work that survives sessions. Eight lineages in our own repos, 2025-10 to 2026-09; three read 2026-09-09, five more 2026-09-16. No public precedents yet.

**This doc holds concepts to consider.** Being here is not a vote to keep. Each item earns its place, or does not, when the skill's shape is decided, and the 2025 retro below says as much about what to drop as what to carry.

## Intent, 2026-09-09

Briefs are the core of the runner's workflow: create the brief first, orient against it, then run the work across several sessions with the context kept good throughout. The brief is what each new session opens against.

## References

### Our lineages, in time order

Five of these live under `~/Development/_temp/`, copied there 2026-09-16 from another machine: ArchType, old-ai-workflow, the proof of concept, page-play, and ai-brief-workflow. All five are ours.

- **ArchType, 2025-10-13 to 2025-10-29.** `~/Development/_temp/ArchType`. 23 briefs in 16 days. `briefs/` and `briefs/completed/`; `docs/development/workflow/` (session-start, brief-creation, exploration-mode, planning-mode, implementation-mode, brief-wrap-up, ghost-creation); `docs/context/MISSION.md`; 22 ADRs under `docs/architecture/`; ghost files under `docs/ghosts/` and `docs/analysis-context/ghosts/`. `_wrap-up-retro/` is the retro written 2025-10-29: `brief-comparison.md`, `briefs.md`, `workflow.md`, `workflow-ritual.md`, `metrics.md`, `product-brief_TEMPLATE.md`.
- **old-ai-workflow, 2025-10-30.** `~/Development/_temp/old-ai-workflow`. The project-agnostic extraction of ArchType's system, seeded in one day. `z_WHAT_IS_THIS_REPO.md` is the statement: problem, artifact comparison, solution, metrics. `docs/briefs/PRODUCT_BRIEF_TEMPLATE.md`; `docs/context/MISSION.md` as a fill-in template; the five workflow docs; `z_EXAMPLE_BRIEF.md`, which is ArchType's Brief 06a; commands `start`, `brief-create`, `brief-check`, `explore`, `explore-finalize`, `plan`, `implement`, `cohesion`. README marked ARCHIVED 2026-06-22.
- **archtype-framework-proof-of-concept, 2025-11 to 2026-01.** `~/Development/_temp/archtype-framework-proof-of-concept`. `project-docs/framework-stories/completed/brief-system-redesign.md`, 2025-12-12, the documented redesign that dropped modes, itself written as a brief. `.claude/docs/briefs/BRIEF_TEMPLATE.md`, 93 lines; `.claude/docs/workflow/phase-workflow.md`; `persona-creation.md` and `project-docs/context/personas/`. Two stories from 2025-11 carry a "Session Handoff Protocol" section: `domain-data-manifests.md`, `fluent-domain-loading.md`.
- **page-play, 2026-02.** `~/Development/_temp/page-play`. The redesign's template unchanged; `/start` renamed `/session` 2026-02-12; `.claude/docs/workflow/session.md` adds the quick-task path that needs no brief.
- **melon-local, 2026-02 to 2026-06, a client engagement.** `~/Development/melon-local`: `.claude/commands/brief-create.md`, `brief-check.md`, `session.md`; `_claude-cowork/briefs/BRIEF_TEMPLATE.md`; `_claude-cowork/briefs/needed-work/OPEN_ITEMS.md`; 74 completed briefs in `_claude-cowork/briefs/completed/`, first added 2026-02-12, last 2026-06-26. Its brief system landed 2026-02-11 and is page-play's template with the project's registers added. `_claude-cowork/handoffs/README.md` is the team-to-team artifact, a different thing with the same word. Engagement work: confirm what is ours to reuse before any text lands here.
- **ai-brief-workflow, 2026-03-31.** `~/Development/_temp/ai-brief-workflow`. Portable engine in `.claude/docs/workflow/` (brief-template, brief-creation, brief-check, brief-completion, phase-workflow, session); project layer in `.workflow/` (`config.md`, `braintrust.md`, `briefs/`, `scratch/`). Commands `session`, `brief-create`, `brief-check`, `phase-next`, `brief-complete`, `braintrust`.
- **The earlier suite**, summarized in `~/Development/agentic-temp/summary.md` (`/orient`, `/handoff`, `/ticket`, `/epic`, `/triage`, `/knowledge-map`, `/backlog-standards`) and `skills.md`. The suite's source was not located in `~/Development` on 2026-09-09; the summary is the reference. A 2026-08-28 session transcript names the iba plugin next to the path `C:\Development\Ai.Claude`; unverified. Also engagement work; same provenance check.
- **era 4.0.0, 2026-09, ours and MIT.** `~/Development/era`, published at github.com/joeyshipley/era. `plugins/era/skills/brief-create/` (SKILL.md, template.md, extend-skill.template.md), `orient/`, `orient-brief/`, `orient-project/`, `retro/`; the README for the loop; `.agentic/era/brief-create/extend-skill.md` as a filled example of the extension. Lineage: 78d4868 first release, 5c7660c 3.0.0, ec104f5 3.2.0 adds the retro, ddd83e2 4.0.0 brief becomes brief-create.

### Books

- **Lean UX**, Jeff Gothelf and Josh Seiden. The hypothesis statement that era's Hypothesis / Signal / Review section is a form of.
- **User Story Mapping**, Jeff Patton. Slicing a release by outcome, which is what a brief's phases do.
- **Evidence Guided**, Itamar Gilad. Goals to ideas to steps to tasks, with the confidence behind each: the ladder a brief descends.

Related in this repo: `orient.md`, orient is the incoming half in every lineage here. `story.md` and `epic.md`, the artifacts a brief is shaped from or into. `grill-me.md`, examine writes a brief's Open Questions in era, and its provenance decision applies here too.

## What each lineage is

### ArchType and old-ai-workflow: the Product Engineer Brief

One artifact combining product thinking, engineering design, and execution tracking, moving through modes chosen by what is not yet known.

- The problem as first stated. Traditional tools (PRD, spec, tickets, boards) break down for AI in three ways: artifact fragmentation with a human handoff at every seam; no forcing function against skipping from idea to code; and the human-memory assumption, when AI starts fresh each session and needs explicit resume markers.
- Four core sections always present. Intent: For, Problem, Outcome, Why Now. Constraints: mission alignment, ADRs, technical limits, prior briefs. Signal: user signal, technical signal, outcome signal. Open Questions, which choose the mode: architectural unknowns to exploration, implementation unknowns to planning, none to implementation.
- Three mode sections filled as work progresses. Exploration Findings: decisions, rationale, alternatives, planning input, and explicitly no tasks. Planning Output: dependency map, then phases of TDD pairs, each phase ending Run tests, Commit, STOP. Implementation Progress: phase tracker and TodoWrite status. Brief checkboxes are the source of truth for progress; TodoWrite is ephemeral working memory.
- MISSION.md is read first every session: core truth, primary user, principles, standards, success criteria, non-goals, a reset protocol for when confused, and a change protocol that makes it near-immutable. The retro calls it the recovery artifact created after early drift.
- Session restart ritual: restart after exploration completes, after planning completes, after every implementation phase. Reason given: context bleed; each session loads only what its stage needs. Restart checklist: committed, brief updated, tests green, clear stopping point.
- Ghost files: mechanical per-session logs (what was built, decisions, bugs, files, human feedback verbatim) for aggregate analysis, and explicitly not for session-to-session context.
- Brief wrap-up: fill Implementation Progress, update project status, write a ghost, archive, push. A final Integration Audit phase emerged after fixture drift and became standard.
- Numbers from the retro: 23 briefs averaging 462 lines, 4 to 8 phases each, 613 tests at 100%, briefs 06 to 08 spanning 1 to 8 sessions each, and no "what was I working on" moments in 16 days.

### The comparison to industry artifacts, 2025-10-29

The retro's `brief-comparison.md` and old-ai-workflow's what-is-this doc score the brief against each artifact type. Kept here because it is the argument for what a brief absorbs and what it leaves outside.

| Artifact | Similarity | What the brief adds |
|---|---|---|
| Jira ticket | 80%, "a GitHub issue on steroids" | modes, embedded decisions, multi-session resumption |
| Shape Up pitch | 70% | stays with the work and evolves; tracks progress |
| PRD | 60% | continues through how and is-it-done; not static |
| RFC | 50% | findings are RFC-like, then it goes further |
| Technical spec | 50% | lives through implementation; tasks integrated |
| User story | 40% | shares acceptance criteria; drops the as-a-user framing |
| Notion or Confluence page | 40% | strict sections, enforced workflow, explicit resume |
| TODO.md | 20% | different weight class |

- The feature table rates brief, user story, PRD, Jira ticket, Jira epic, technical spec, and ADR on: AI-optimized, intent, single source, forcing functions, how to build, living doc, dependency map, multi-session, explicit constraints, decision rationale, alternatives considered, progress, task tracking, and weight in lines.
- For a solo or small team the brief replaces the artifacts. For a large organization user stories and PRDs are inputs to Intent, and specs, ADRs, and tickets are extraction outputs, with the brief the source of truth throughout. Extraction was named as future work and never built.
- Epics were briefs with sub-briefs (06 split into 06a to 06d), noted as not fleshed out.
- The name: Product for intent, constraints, signal, user needs; Engineer for planning, implementation, decisions; Brief for concise. It names a role collapse: no handoff between product and engineering.

### What the retro said briefs did not capture, 2025-10-29

- Post-implementation reflection: planned versus actual, and why.
- Surprises and elegant solutions found mid-implementation.
- Dead ends and rejected approaches.
- How uncertain or painful a decision was. Findings show the decision, not its weight.
- Ghosts were the attempted answer and became verbose commit logs. Verdict: briefs won for execution; neither captured experiential insight. Recommended a retrospective companion, decision-weight markers (confident, uncertain, uncomfortable compromise), estimation tracking, and a brevity check. Explicitly not to add: more ceremony, mandatory retrospective sections that will not be filled honestly, duplicate tracking.

### The redesign, 2025-12-12

- Problem: about 1,700 lines across 8 files; TDD plans written before research and therefore guessed; mode-switching ceremony; rigid phase structure; multi-session tracking in three places.
- Kept: Goal, Problem, Success Signal, Constraints as invariants; phases with goals; per phase Research, Findings, Adjustments, TDD Plan, Done; Open Questions; a Session Log for handoff.
- Removed: CURRENT MODE, the three mode sections, rigid test cycles, the Intent quartet as redundant with Goal and Problem, embedded examples, the mode commands. Modes are ceremony; what matters is the per-phase cycle Research, Plan, Execute, Validate.
- Result: template 418 to 93 lines; workflow docs from about 1,700 to under 400; resume by reading one file.
- Personas arrive in the same repo: role-named files, never person-named; demographics, goals, pain points, behaviors, needs, a quote; built from observation, not invented.
- The "Session Handoff Protocol" in two stories: read this document top to bottom, check Current Status, find the next unchecked task, do it, mark it, update status, add decisions to Notes. A do-not list: skip ahead, deviate from the defined architecture, add features not here, change decisions without recording them.
- page-play adds the quick-task path: small clear task, confirm scope, execute, no brief.

### ai-brief-workflow, 2026-03-31

- Split: a portable engine in `.claude/docs/workflow/` and a project layer in `.workflow/`, with `config.md` naming session reads, brief paths, project-specific checks, work categories, and project commands.
- Per phase: a Checkpoint written at phase start (assumptions, plan, expectations) and compared against Done at phase end, with divergence recorded as learning. A Work Plan shaped by kind of work: code, design, assets, research. A dual-lens Review: big picture and dependencies, then implementation detail.
- At completion: a Learning Log (surprises, duration, what should change) and Rule Candidates (promote to project rule or workflow rule). This is the 2025 retro's recommended companion folded into the brief.
- Conflict resolution on every load of prior decisions: does anything decided since contradict what was just loaded? Surface it; never silently override or continue.
- Braintrust: five perspectives (new, daily, power, paying, reluctant user) run as isolated agents; convergence is the signal. Three traps and three meta-principles.

### melon-local

A brief is a committed markdown file, project-tailored, and is the record of the work as well as its plan.

- Header: status, created, last session, feature IDs, tier 1 to 4 (can do now, feasible, needs investigation, blocked), spike dependency, milestone.
- Context Loading table: which project docs to load, per phase, so a session loads on demand.
- Goal, Problem, Success Signal as checkboxes, Constraints.
- Affected Features, mapped to the plan's story IDs.
- Questions for Colin: question, default if no answer, answer. The default column is what lets work proceed while a question is out.
- Phases table, then per phase: Research, Findings, Adjustments, Implementation Plan, Done. Findings are written into the brief, so a research brief becomes the research paper; `xcut_validation-options.md` runs past 30KB.
- Open Questions stay brief-local; cross-brief items go to OPEN_ITEMS with a stable ID.
- Session Log: date, phase, what happened, decisions, next.
- `/session` lists briefs without reading them and asks what to work on. `/brief-check` audits completeness, consistency, actionability, and handoff readiness, suggested when a brief has been idle. `/brief-create` interviews in a fixed order (goal, problem, signal, constraints) and grounds in the project's registers.
- The handoffs folder holds board-ready Azure Boards items for the client team, stripped of process language. Team-to-team.

### The earlier suite

The ticket is durable; the handoff is scaffolding between sessions and is deliberately ephemeral.

- Gitignored, one doc per ticket key, superseded whole, self-stamped with a stale-after date that every write restamps. Deleted at close.
- Imperative register: settled facts and instructions, no hedges, no options, no open questions. A new open question routes out to the ticket.
- Two invariants: done-and-verified (the check ran) is split from done-unverified (name the proving check), and "do next" is exactly one literal action.
- Written at a work boundary while the session is healthy, never at the context wall. No automatic checkpoint on session death, because a dying session authors exactly the degradation the doc exists to avoid.
- Copies, never sole originals. Ephemerality is what makes restating other homes legal.
- Orient is the incoming half: verifies branch, a reality command, working tree, and expiry; shows a stale or diverged verdict verbatim; the human chooses trust or the full walk. It always still reads the ticket, because questions parked there since the doc was written are invisible to the doc.

### era

The brief is the durable unit and the handoff at once; there is no second artifact.

- `brief-create` asks one question, "working this now?", and writes a Parked shell (Goal, why not the roadmap, Unknowns) or an Active brief. A Parked brief that needs more than a screen is a roadmap item pretending not to be.
- Active: Goal; Hypothesis / Signal / Review for product work or Invariant / Test for platform work, never both; Approach derived from stances (design, why maintainable, deliberately not doing, seams left); Open Questions written by examine, one disposition each; Context to Load as path and why; Scope in and out; Done When; Phases; Constraints only if real.
- Every work phase opens with a gate item, oriented read-only, open questions examined, plan written in plan mode and approved at exit, and ends with a close item, proof green, brief updated, committed, pushed. The close leaves the repo clean enough that a fresh session can open the next phase. Whether it does is the user's choice, never the session's recommendation.
- The retro phase records findings with a proposed home and changes nothing. `era:retro` reads `done/` across briefs and is the only thing that acts on them.
- The branch is named after the brief. `orient` dispatches to `orient-brief` (deep on the current phase, light on the rest, each done phase's claims held against git) or `orient-project` (briefs with status, phase, and age taken from git, the queued work, recent movement). Both read-only; every anomaly is two named sources disagreeing.
- Heavy prerequisites: examine, stances, owner-ladder, retro, enforcement-homes, and the extension file, all read before a brief is written.

## Where they disagree

- **One artifact or two.** melon and era make the brief the thing that survives. The earlier suite keeps the ticket durable and the handoff disposable. The roadmap's own wording, handoff / briefs, leaves this open.
- **What may be restated.** The earlier suite's rule: an ephemeral copy may restate any home; a durable file may not. melon's briefs restate heavily and hold findings nothing else holds. era's restate almost nothing; Context to Load is pointers.
- **What the brief absorbs.** The 2025 argument is that the brief replaces PRD, spec, tickets, and board for a small team, and points at them only in a large one. The earlier suite's knowledge map is the opposite: every fact has one home and the session artifact restates nothing durable. era points instead of restating. Same axis as the previous item, seen from the artifact side.
- **Modes or phases.** ArchType chose the mode from Open Questions and restarted between modes. The redesign called modes ceremony and kept only the per-phase cycle. era's gate and close items are that cycle, with the restart left to the user.
- **The product half.** ArchType carried For, Problem, Outcome, Why Now, three kinds of signal, a mission file, and later personas. The redesign cut Intent to Goal and Problem as redundant. era keeps a hypothesis and a signal; melon keeps Goal, Problem, Success Signal. Where the who and the why live once the brief stops holding them is unsettled.
- **Narrative.** melon keeps a Session Log and per-phase Findings. era and the earlier suite refuse narrative history. ArchType's ghosts tried to hold it and became commit logs. ai-brief-workflow records learning once, at completion. Dead ends, which the earlier suite says are read once and then lost, and which the 2025 retro lists as never captured, have no agreed home.
- **Verification on resume.** The earlier suite's ground-truth gate and era's divergences are the same idea. ai-brief-workflow asks a narrower question on every load: does anything decided since contradict this. melon's brief-check is a manual audit.
- **What the brief depends on.** era needs its doctrine skills; melon needed the project's registers; the earlier suite needed Jira and the knowledge map; ArchType needed MISSION.md and the ADRs; ai-brief-workflow needs only `config.md`. None runs bare, and none has met a project with no code.

## Carried-forward candidates

- melon's default-if-no-answer column on team questions. examine's team list lacks it.
- melon's on-demand loading: list briefs, read none until one is chosen.
- The earlier suite's two invariants: verified split from unverified, and one literal next action.
- The earlier suite's rule that a handoff is written at a work boundary while the session is healthy. Its ancestor is ArchType's restart after every completion, with the checklist: committed, brief updated, tests green, clear stopping point.
- era's gate and close items as the phase rhythm, and orient's two-sources rule for divergences.
- era's Parked shell and its one-screen test.
- ArchType's rule that what is not yet known decides what kind of work happens next. examine is this rule made into a skill.
- The redesign's test: resume by reading one file.
- ai-brief-workflow's Checkpoint at phase start compared against Done at phase end.
- ai-brief-workflow's conflict question on every load of prior decisions.
- A Learning Log and Rule Candidates at completion, as the answer to what briefs did not capture, and never a mandatory section per phase.
- page-play's quick-task path: a small clear task needs no brief.
- The comparison table as the form for stating what a brief absorbs and what it points at.
- The 2025 retro's don't-add list: ceremony, mandatory retrospection, duplicate tracking.

## Open decisions, resolved 2026-09-16

1. One artifact or two, and what each is named. Decided: one. The brief is the handoff and is called a brief. No second file.
2. What a brief may restate, and where findings and dead ends live. Decided: the brief is personal and uncommitted, so it may restate, and it points by default to keep every load light. Findings are pointers; dead ends go to the retro log.
3. Whether narrative history has a place. Decided: no session log. Progress is the phase todo lists; the retro phase is a read-only log at the end, read later by brief-retro.
4. The resume check. Decided: none of them. The brief lists its branches, git says whether they are behind, and validity is the owner's call.
5. What a brief needs to exist. Decided: the extension file `.agentic/alt/brief-create/extend-skill.md` with `## Preset`, `## Close`, and `## Load`; absent means developer and generic close items. Works without git.
6. Provenance. Decided: every lineage here is the author's own work and the repo is public; use freely, no attribution.
7. The product half. Decided: Goal, Problem, Done When, Constraints, plus one line each for who this is for, what changes for them, and how we would know.
8. What the brief absorbs. Decided: the plan and the current state. Everything else is pointed at.

## Also decided, 2026-09-16

- Phases are units of change smaller than a session, grouped and worked in dependency order. A session may hold several and a large phase may outlive one. No hard rule.
- No splitting a brief. No parked briefs and no gate: every brief is a full brief, and the runner names which one to load.
- Two skills, brief-create and brief-retro. Phase close and completion are template instructions; listing and resuming are orient's.
- brief-create asks what the template needs, runs examine, then writes. If examine does not load, the brief is written with a placeholder that says so.
- Each phase lists its own close checks. Briefs live in `.agentic/briefs/`, closed ones in `.agentic/briefs/closed/`; brief-create adds the ignore line when absent and confirms with check-ignore. `.agentic/` stays committed.
- The runner asks for the brief to be updated at session close, then restarts. No stamps, hashes, or next-action prose.
- brief-retro appends a one-word disposition and the date to each reviewed retro line in the closed brief.
- Not carried: resume-by-one-file with a budget, the session log, MISSION.md, the comparison table as a checklist.
- Left to the template author and shipped without: a checkpoint per phase, a "did this change later phases" close item, never-contains lines per section, load-discipline wording, a scratch folder.

The skill: `plugins/alt/skills/brief-create/SKILL.md` and `template.md`, alt 0.3.0.

## To write

- Public precedents, none reviewed yet: memory banks, claude-mem, progress logs, and whatever else claims to survive a session.
- Relationship to orient and brief-retro, once they exist.
