# alt

Agentic Lean Techniques. Claude Code workflows collected from client engagements: skills, commands, agents, and hooks that have proven useful more than once.

This repo is a Claude Code plugin marketplace named `agentic-leantechniques`. It publishes one plugin, `alt`, whose skills appear as `/alt:<skill>`.

## Install

Add the marketplace once, then install the plugin:

```
/plugin marketplace add lt-jshipley/alt
/plugin install alt@agentic-leantechniques
```

Restart Claude Code after installing. Skills will show up under `/alt:`.

## Layout

```
.claude-plugin/marketplace.json   Marketplace manifest, lists published plugins
plugins/alt/                       The alt plugin
  .claude-plugin/plugin.json       Plugin manifest
  skills/<name>/SKILL.md           Skills, invoked as /alt:<name>
    brief-create/                  Creates a brief, the personal working file that carries one piece of work across sessions, at .agentic/briefs/ in the consuming repo. Research in .project/research/agentic-skills/brief.md
    brief-retro/                   Reads the retro lines of every closed brief together and walks them with the runner to a disposition. Appends one word and a date per line, nothing else
    decisions/                     Lists the decisions a draft silently assumes, each with its stake and hat, interviewing nobody. Invoked by epic-refine and brief-create against their drafts. Research in .project/research/agentic-skills/decisions.md
    epic-refine/                   Creates an epic in the tracker from an idea, a handed-down feature, or a pasted draft, or refines an existing one into a need with an outcome, a bet, and who holds each. Never creates the stories under it. Research in .project/research/agentic-skills/epic.md
    examine/                       The decision interview for a developer working alone: grilling's tree, one question a turn, with stakes and could-help on every question. Not invoked by other skills; see decisions. Research in .project/research/agentic-skills/grill-me.md
    orient/                        Orients the session in the work it is about to do: takes a brief, story key, branch, or a sentence, collects the core facts through .agentic/sources.md, and reports the system that work sits in. Reads only. Research in .project/research/agentic-skills/orient.md
    peer-review/                   Reviews a change before the PR opens and again when it is reviewed, same bar both times: four parallel sonnet lenses nominate, the session verifies against the code, every finding carries evidence and a tier. Writes .agentic/reviews/<branch>.md, the record the second run reads first. Never touches the PR. Research in .project/research/agentic-skills/peer-review.md
    review-prose/                  Reviews a skill or doc for verbosity and reports what could go. Changes nothing
    sources-sync/                  Drafts or refreshes .agentic/sources.md, the one page that tells every alt skill where this team's facts live: code, docs, tracker, record, measures, people. Asks which tools the team uses and fills the seats from stacks.md defaults for GitHub, Atlassian, and Azure DevOps
    triage/                        Reads a scope of open work in full and says what its symptoms are symptoms of: fixes what the record settles, routes what nobody holds as an Open line to the holder, names what is holding. Never grades or orders. Research in .project/research/agentic-skills/triage.md
  presets/                         Word and hat swaps per kind of work, shared by skills that take a preset: developer, business, research

The story and epic skills written from the business side, story-create, story-review, epic-create, and epic-review, moved to the lt-backlog-skills repo and install from there as the lt-backlog plugin. The session health gauge, alt-statusline, moved to the alt-statusline-reasoning repo and installs from its own marketplace of that name.
.agentic/                          Reserved here; in a consuming repo this holds sources.md, alt extension files, and the gitignored briefs/ folder
.claude/                           Reserved for Claude Code config for working in this repo itself; empty so far
.project/archive/skills/           Skills removed from the plugin, kept for the record; not loaded by Claude Code
```

Add `agents/`, `commands/`, or `hooks/hooks.json` under `plugins/alt/` as those are needed.

## Validate

```
claude plugin validate . --strict
claude plugin validate plugins/alt --strict
```

## License

MIT. See [LICENSE](LICENSE).
