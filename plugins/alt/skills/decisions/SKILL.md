---
name: decisions
description: Lists the decisions a draft story, epic, or brief silently assumes, each with what a wrong answer costs and who could help, asking nothing that can be looked up and interviewing nobody. Use when another alt skill invokes it against its draft, or when the user asks what a draft leaves undecided, or invokes /alt:decisions.
argument-hint: [pasted draft, ticket key, or the draft in the room]
---

# decisions

A draft is a set of answers. This skill finds the questions it never asked. It reads, lists the decisions the draft silently assumes with the stake and the hat on each, and stops. Asking is the caller's; deciding is a person's.

## Inputs

The seed is the draft in the room, or $ARGUMENTS: a pasted draft or a ticket key. Read the ticket when a key and a tracker connection exist.

Preset: the `## Preset` heading of any `.agentic/alt/*/extend-skill.md`, else developer. Hats come from it.

Read if present, ignore if absent: `.agentic/sources.md`, where this team's facts live, and `.agentic/alt/examine/extend-skill.md`, this repo's hats and where approaches break here.

## Facts are never decisions

Read what the draft touches, the record, and every source the sources file names. Anything they answer is a fact: settled, cited in a few words, never listed as a decision. Send a sub-agent when a lookup deserves one. A source the file names that cannot be reached is one line under Not reachable, never a decision and never one line per fact.

## Find

Hunt against the draft, never the runner, from six angles: feasibility, dependencies, edge cases, alternatives, scope and ordering, failure modes. Each candidate is tried before it is kept. Does the record settle it? A fact. Should the thing forcing the decision exist at all? Say so; removing the cause is the best answer. Only survivors are listed, with no cap.

A wound is a premise the draft gets wrong or a decision it never made with several decisions hanging off it. A decision that waits on another decision is written under that one as what it dissolves, never on its own line. So the list is roots, and the roots are the questions worth a person's time.

## Output

```
Decisions on <the seed, a few words>. Read: <what, a few words each>. Settled by the record: <n>.

Wounds
- <the decision, as a question in plain words>
  <why the draft does not settle it, one line>
  If wrong: <what breaks, for whom>
  Could help: <hat>, <why they hold the context>
  Dissolves: <the decisions that wait on this one, a few words each>

Decisions
- <the decision, as a question in plain words>
  <why the draft does not settle it, one line>
  If wrong: <what breaks, for whom>
  Could help: <hat>, <why they hold the context>
  Lean: <one clause, only when the code or the record supports it>

Settled
- <the fact>, per <source>.

Not reachable: <the seats named and not reached>.
```

Wounds first, ordered by how many decisions each dissolves; then decisions by what the if-wrong line costs. Sections with nothing in them are omitted, headings included. Zero decisions is a success; never invent one.

## Rules

- Never asks the runner anything. Never recommends beyond the Lean clause, never offers options, never numbers questions, never proposes a target, size, priority, or date.
- Could help is help, not ownership. Money, legal, safety, and identity name the hat and say team conversation in the if-wrong line.
- A quick patch is never a peer of a fix; when the honest decision is whether to fix or patch, the line says so.
- Never edits the draft, never writes to the tracker, never starts the work, never enters plan mode.
- Non-interactive is the only mode. The list is the whole output.

## When something is missing, say so in one line

- Nothing in the room and no argument: say what a seed is, once, and stop.
- Key given, no tracker connection: the key is carried, the item unread, and Not reachable says tracker.
- Preset cannot be read: developer, and say so.
