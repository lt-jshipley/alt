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
    elicit/                        First real skill: the decision interview. Design in .project/design/elicit.md
  presets/                         Word and hat swaps per kind of work, shared by skills that take a preset: business, research. Developer is the inline default
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
