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
    examine/                       The decision interview: grilling's tree, one question a turn, with stakes and could-help on every question. Research in .project/research/agentic-skills/grill-me.md
    orient/                        Orients the session in the work it is about to do: takes a brief, story key, branch, or a sentence, collects the core facts through .agentic/sources.md, and reports the system that work sits in. Reads only. Research in .project/research/agentic-skills/orient.md
    review-prose/                  Reviews a skill or doc for verbosity and reports what could go. Changes nothing
    sources-sync/                  Drafts or refreshes .agentic/sources.md, the one page that tells every alt skill where this team's facts live: code, docs, tracker, record, people. Asks which tools the team uses and fills the seats from stacks.md defaults for GitHub, Atlassian, and Azure DevOps
  presets/                         Word and hat swaps per kind of work, shared by skills that take a preset: developer, business, research
plugins/alt-statusline/            Session health gauge for the statusline; hooks + judge + statusline, gated behind /alt-statusline:setup
  hooks/hooks.json                 Plugin hooks, inert until setup registers a scope
  scripts/                         Hook scripts, statusline, judge prompt, setup.py, launcher, simulate.sh
  skills/setup, skills/remove      Install and uninstall
.agentic/                          Reserved here; in a consuming repo this holds sources.md, alt extension files, and the gitignored briefs/ folder
.claude/                           Reserved for Claude Code config for working in this repo itself; empty so far
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
