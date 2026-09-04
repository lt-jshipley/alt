# alt

Agentic Lean Techniques. Claude Code workflows collected from client engagements: skills, commands, agents, and hooks that have proven useful more than once.

This repo is a Claude Code plugin marketplace named `agenticleantechniques`. It currently publishes one plugin, `alt`, whose skills appear as `/alt:<skill>`.

## Install

Add the marketplace once, then install the plugin:

```
/plugin marketplace add lt-jshipley/alt
/plugin install alt@agenticleantechniques
```

Restart Claude Code after installing. Skills will show up under `/alt:`.

## Layout

```
.claude-plugin/marketplace.json   Marketplace manifest, lists published plugins
plugins/alt/                       The alt plugin
  .claude-plugin/plugin.json       Plugin manifest
  skills/<name>/SKILL.md           Skills, invoked as /alt:<name>
    examine/                       The decision interview: grilling's rounds with stakes and could-help on every question. Research in .project/research/agentic-skills/grill-me.md
    review-prose/                  Reviews a skill or doc for verbosity and reports what could go. Changes nothing
  presets/                         Word and hat swaps per kind of work, shared by skills that take a preset: developer, business, research
.claude/                           Claude Code config for working in this repo itself
```

Add `agents/`, `commands/`, or `hooks/hooks.json` under `plugins/alt/` as those are needed.

## Validate

```
claude plugin validate . --strict
claude plugin validate plugins/alt --strict
```

## License

MIT. See [LICENSE](LICENSE).
