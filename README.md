# alt

Agentic Lean Techniques. Claude Code workflows collected from client engagements: skills, commands, agents, and hooks that have proven useful more than once.

This repo is a Claude Code plugin marketplace named `agentic-leantechniques`. It publishes two plugins: `alt`, whose skills appear as `/alt:<skill>`, and `alt-statusline`, a session health gauge for the statusline that stays inert until you run its setup skill.

## Install

Add the marketplace once, then install the plugin:

```
/plugin marketplace add lt-jshipley/alt
/plugin install alt@agentic-leantechniques
```

Restart Claude Code after installing. Skills will show up under `/alt:`.

For the statusline gauge, install it separately, reload, then run setup:

```
/plugin install alt-statusline@agentic-leantechniques
/reload-plugins
/alt-statusline:setup
```

Nothing is graded and no statusline changes until `setup` runs; `/alt-statusline:remove` puts things back. Details in `plugins/alt-statusline/README.md`.

## Layout

```
.claude-plugin/marketplace.json   Marketplace manifest, lists published plugins
plugins/alt/                       The alt plugin
  .claude-plugin/plugin.json       Plugin manifest
  skills/<name>/SKILL.md           Skills, invoked as /alt:<name>
    brief-create/                  Creates a brief, the personal working file that carries one piece of work across sessions, at .agentic/briefs/ in the consuming repo. Research in .project/research/agentic-skills/brief.md
    brief-retro/                   Reads the retro lines of every closed brief together and walks them with the runner to a disposition. Appends one word and a date per line, nothing else
    decisions/                     Lists the decisions a draft silently assumes, each with its stake and hat, interviewing nobody. Invoked by epic-refine and brief-create against their drafts. Research in .project/research/agentic-skills/decisions.md
    epic-create/                   Creates an epic in the tracker from the business side, never reading source: whose need in their words, how we will know, what we are betting on and the evidence, what was decided and why, what is open and whose. Never how, never a feature as the need, never the stories under it. epic-review runs before the write. Research in .project/research/agentic-skills/epic.md
    epic-refine/                   The earlier epic skill, with a preset, an inline decisions step, and a code read for feasibility. Kept until epic-create has runs, then archived. Research in .project/research/agentic-skills/epic.md
    epic-review/                   Reads an epic draft as the decider who would sign the bet and the team that would slice it, edits what four questions name (need, workable, how kept out, template), and returns the draft with one line per change and what it could not fix. Run by epic-create before the write in a fresh sub-agent; never reads code, never writes to the tracker
    examine/                       The decision interview for a developer working alone: grilling's tree, one question a turn, with stakes and could-help on every question. Not invoked by other skills; see decisions. Research in .project/research/agentic-skills/grill-me.md
    orient/                        Orients the session in the work it is about to do: takes a brief, story key, branch, or a sentence, collects the core facts through .agentic/sources.md, and reports the system that work sits in. Reads only. Research in .project/research/agentic-skills/orient.md
    review-prose/                  Reviews a skill or doc for verbosity and reports what could go. Changes nothing
    sources-sync/                  Drafts or refreshes .agentic/sources.md, the one page that tells every alt skill where this team's facts live: code, docs, tracker, record, measures, people. Asks which tools the team uses and fills the seats from stacks.md defaults for GitHub, Atlassian, and Azure DevOps
    story-create/                  Creates a story in the tracker from the business side, never reading source: what changes for whom, the rules, the examples at the edges, what was decided and why, what is open and whose. Never how. Up to three lines a section, a fourth on the runner's call. story-review runs before the write; the builder's pass against the code comes after and returns questions. Research in .project/research/agentic-skills/story.md
    story-review/                  Reads a story draft as the signer and the builder, edits what four questions name (value, workable, implementation, template), and returns the draft with one line per change and what it could not fix. Run by story-create before the write in a fresh sub-agent; never reads code, never writes to the tracker. Research in .project/research/agentic-skills/story.md
    triage/                        Reads a scope of open work in full and says what its symptoms are symptoms of: fixes what the record settles, routes what nobody holds as an Open line to the holder, names what is holding. Never grades or orders. Research in .project/research/agentic-skills/triage.md
  presets/                         Word and hat swaps per kind of work, shared by skills that take a preset: developer, business, research
plugins/alt-statusline/            Session health gauge for the statusline; hooks + judge + statusline, gated behind /alt-statusline:setup
  hooks/hooks.json                 Plugin hooks, inert until setup registers a scope
  scripts/                         Hook scripts, statusline, judge prompt, setup.py, launcher, simulate.sh
  skills/setup, skills/remove      Install and uninstall
  skills/loose-ends                Lists the session's loose ends, reads each from memory, closes the confirmed ones
.agentic/                          Reserved here; in a consuming repo this holds sources.md, alt extension files, and the gitignored briefs/ folder
.claude/                           Reserved for Claude Code config for working in this repo itself; empty so far
.project/archive/skills/           Skills removed from the plugin, kept for the record; not loaded by Claude Code
.project/research/statusline/      Research behind the gauge's context-window thresholds
```

Add `agents/`, `commands/`, or `hooks/hooks.json` under `plugins/alt/` as those are needed.

## Validate

```
claude plugin validate . --strict
claude plugin validate plugins/alt --strict
claude plugin validate plugins/alt-statusline --strict
bash plugins/alt-statusline/scripts/simulate.sh
```

## License

MIT. See [LICENSE](LICENSE).
