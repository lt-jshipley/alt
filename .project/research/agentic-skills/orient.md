# Orient: research notes

Started 2026-09-09. Research behind the roadmap's orient skill, brief-level and project-level. Only the intent and references are written.

## Intent, 2026-09-09

Story, epic, triage, and orient itself all need to know where to go for information. Orient is the shared answer. Run in a folder or repo, it learns what kind of project this is from the CLAUDE.md file and the extension file, and learns the listed information sources from them. Codebases are the common case and not the only one: a project can be a proposal, a study, or an offer with no code in it, and orient has to work there too.

## References

Three groups: what this repo already holds, what to verify about Claude Code, and the books. Primary first within each.

### In this repo

- **`grill-me.md`, "A shared fact-sources extension".** The `.agentic/sources.md` idea: one repo-level file every alt skill reads, keyed by what invalidates a fact (changes with the code, the business, the work) rather than by tool, with people as valid sources, access and cost per source, and degradation rules for absent and unreachable. Orient is the skill that reads it, and the candidate for writing it.
- **`grill-me.md`, "The seed the skill needs about the runner" and "Relationship to the runner seed".** The team layer (sources, record, where output lands) belongs to the repo; the runner layer was rejected: no alt skill models who is running it. Orient is the team layer.
- **`plugins/alt/presets/`.** Developer, business, research: the kind of work. The extension file's `## Preset` heading is already the hook a skill uses to learn which one applies. "What kind of project is this" and "which preset" may be the same question.
- **`plugins/alt/skills/examine/SKILL.md`, Inputs.** Reads `.agentic/sources.md` and `.agentic/alt/examine/extend-skill.md` if present. Orient produces or refreshes what examine consumes; the contract between them is those two files.
- **`skill-development.md`.** Coupling: shared content is a file read by path, named by concept, with absent behaviour stated. Cost: what one invocation loads before it does anything. Shape: a skill knows when not to run.
- **`.project/roadmap.md`, knowledge-map.** "May be a file convention under `.agentic` rather than a skill." The same question applies to orient: a skill, a file convention, or a skill whose job is to write the convention.

### To verify about Claude Code

- How CLAUDE.md resolves: project, user, nested folders, imports. What of it is already in a session's context, so orient does not re-read what is already loaded.
- What a plugin skill can read of the host repo and of `.claude/`, and why the sources file lives in `.agentic/` (any tool can read it) rather than `.claude/`.
- The built-in `/init`, which orients to a codebase and writes CLAUDE.md. What orient adds beyond it is an open decision, and the non-code case is the obvious first answer.
- Matt Pocock's `wayfinder` was checked 2026-09-09 and is not a precedent: it plans large work as decision tickets on an issue tracker. Noted for epic, not here.

### In our other repos, read 2026-09-09

- **era**, `~/Development/era/plugins/era/skills/orient/`, `orient-brief/`, `orient-project/`. A dispatcher that reads two signals only, the briefs' status lines and the branch name, then hands off. orient-brief goes deep on the current phase and light on the rest; orient-project surveys briefs with age taken from git, the queued work, and recent movement. Both read-only, both report every anomaly as two named sources disagreeing, both end by handing the wheel back. Each reads `.agentic/era/<skill>/extend-skill.md` for deviations and landmarks.
- **The earlier suite**, `~/Development/agentic-temp/summary.md`, the `/orient` section. Routes through a business-vocabulary layer (the knowledge map and domainspace files) before reading anything, produces an ephemeral confirmed picture and never a file, names every absent source, and gates a resume from a handoff doc on a ground-truth check. Its stated difference from `/init` is the refusal to write.

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

## To write

- Summary.
- The problem the skill solves, and for whom.
- Brief-level and project-level: what each answers, and for whom.
- What orient reads, in what order, and what it writes, if anything.
- Kind of project: how it is detected, when to ask instead of infer, and the non-code case.
- Skill, file convention, or both.
- Relationship to `/init`, the presets, examine, and the three artifact skills.
- Degradation, one line each.
- Open decisions.
