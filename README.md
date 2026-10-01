# alt

Agentic Lean Techniques. Claude Code workflows collected from client engagements: skills that have proven useful more than once.

This repo is a Claude Code plugin marketplace named `agentic-leantechniques`. It publishes one plugin, `alt`, whose skills appear as `/alt:<skill>`.

## Install

Add the marketplace once, then install the plugin:

```
/plugin marketplace add lt-jshipley/alt
/plugin install alt@agentic-leantechniques
```

Restart Claude Code after installing. Skills will show up under `/alt:`.

## Configure

Nothing is required. A consuming repo may add one section to the CLAUDE.md it already has; every line is optional and an absent line means the default.

```
## alt
Tracker: Jira project ABC, through the Atlassian MCP
Docs: docs/ and the Confluence space ABC
Measures: the product dashboard; ask the Product Owner for a number
Briefs: docs/briefs/
Phase closes when: make test passes and a teammate has reviewed
Every brief loads: docs/architecture.md
```

Defaults: the tracker is whatever tracker tool the session reaches, and a key with none is carried unread; docs are README and `docs/` when present; there are no measures, so an epic's outcome stays unmeasured; briefs go to `.briefs-local/`, which brief-create gitignores; a phase's check is written from the interview; nothing extra is loaded. Roles in every skill are Product Owner, Tech Lead, Engineer, and Designer. Decisions about a piece of work are written on its ticket.

## Layout

```
.claude-plugin/marketplace.json   Marketplace manifest, lists published plugins
plugins/alt/                       The alt plugin
  .claude-plugin/plugin.json       Plugin manifest
  skills/<name>/SKILL.md           Skills, invoked as /alt:<name>
    brief-create/                  Creates a brief, the personal working file that carries one piece of work across sessions, at .briefs-local/ in the consuming repo, gitignored, or at the checked-in folder its CLAUDE.md names. Research in .project/research/agentic-skills/brief.md
    brief-retro/                   Reads the retro lines of every closed brief together and walks them with the user to a disposition. Appends one word and a date per line, nothing else
    decisions/                     Lists the decisions a draft silently assumes, each with its stake and role, interviewing nobody. Invoked by brief-create against its draft. Research in .project/research/agentic-skills/decisions.md
    examine/                       The decision interview for a developer working alone: a tree of decisions, one question a turn, with stakes and could-help on every question. Invoked by name or by another skill; decisions is the interview-free form. Research in .project/research/agentic-skills/grill-me.md
    orient/                        Orients the session in the work it is about to do: takes a brief, story key, branch, or a sentence, reads the ticket, the code around it, and the docs, and reports the system that work sits in. Reads only. Research in .project/research/agentic-skills/orient.md
    peer-review/                   Reviews a change before the PR opens and again when it is reviewed, same bar both times. Fans out to cheaper sub-agents to nominate, which costs tokens, then the session verifies every finding against the code and gives it a tier. Reports where it runs and writes nothing; the second run reads the first's report from the PR when it was pasted there. Never touches the PR. Research in .project/research/agentic-skills/peer-review.md
    review-prose/                  Reviews a skill or doc for verbosity and reports what could go. Changes nothing
    triage/                        Reads a scope of open work in full and says what its symptoms are symptoms of: fixes what the tickets settle, routes what nobody holds as an Open line to the holder, names what is holding. Never grades or orders. Names lt-backlog's epic-create for a parent not in the epic format. Research in .project/research/agentic-skills/triage.md

.briefs-local/                     In a consuming repo, the briefs folder, gitignored; a `Briefs:` line under `## alt` in CLAUDE.md moves them to a checked-in folder
.claude/                           Reserved for Claude Code config for working in this repo itself; empty so far
.project/archive/                  Skills and presets removed from the plugin, kept for history; not loaded by Claude Code
```

The story and epic skills written from the business side, story-create, story-review, epic-create, and epic-review, moved to the lt-backlog-skills repo and install from there as the lt-backlog plugin. epic-refine followed in 0.20.0, since epic-create covers both creating and rewriting an epic; sources-sync and the presets went to the archive at the same time, replaced by the `## alt` section above.

Add `agents/`, `commands/`, or `hooks/hooks.json` under `plugins/alt/` as those are needed.

## Validate

```
claude plugin validate . --strict
claude plugin validate plugins/alt --strict
```

## License

MIT. See [LICENSE](LICENSE).
