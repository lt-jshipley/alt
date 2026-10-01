---
name: decisions
description: Lists the decisions a draft story, epic, or brief silently assumes, each with what a wrong answer costs and who could help, asking nothing that can be looked up and interviewing nobody. Use when another alt skill invokes it against its draft, or when the user asks what a draft leaves undecided, or invokes /alt:decisions.
argument-hint: [pasted draft, ticket key, or the draft in the conversation]
---

# decisions

A draft is a set of answers. This skill finds the questions it never asked. It reads, lists the decisions the draft silently assumes with the stake and the role on each, and stops. Asking is the caller's; deciding is a person's.

## Inputs

The seed is the draft in the conversation, or $ARGUMENTS: a pasted draft or a ticket key. Read the ticket when a key and a tracker connection exist.

Read if present, ignore if absent: the `## alt` section of the repo's CLAUDE.md, its `Tracker:` and `Docs:` lines, for where facts live. Absent, the tracker is whatever tracker tool the session reaches and the docs are README and `docs/`.

## Roles

Who could help is one of four: Product Owner, Tech Lead, Engineer, Designer. Could help is help, not ownership. Anything touching money, legal, safety, or identity is a team conversation, never one person's answer; the line names the role and the if-wrong line says so. A call across a service or team boundary names the Tech Lead even when the developer could answer.

## Facts are never decisions

Read what the draft touches, the ticket and its thread, and the docs. Anything they answer is a fact: settled, cited in a few words, never listed as a decision. Send a sub-agent when a lookup deserves one. A source CLAUDE.md names that cannot be reached is one line under Not reachable, never a decision and never one line per fact.

## Find

Hunt against the draft, never the user, from six angles: feasibility, dependencies, edge cases, alternatives, scope and ordering, failure modes. Each candidate is tried before it is kept. Does the ticket thread or the code settle it? A fact. Should the thing forcing the decision exist at all? Say so; removing the cause is the best answer. Only survivors are listed, with no cap.

A root is a premise the draft gets wrong or a decision it never made with several decisions hanging off it. A decision that waits on another decision is written under that one as what it dissolves, never on its own line. So the list is roots, and the roots are the questions worth a person's time.

## Output

```
Decisions on <the seed, a few words>. Read: <what, a few words each>. Settled by the ticket and the code: <n>.

Roots
- <the decision, as a question in plain words>
  <why the draft does not settle it, one line>
  If wrong: <what breaks, for whom>
  Could help: <role>, <why they hold the context>
  Dissolves: <the decisions that wait on this one, a few words each>

Decisions
- <the decision, as a question in plain words>
  <why the draft does not settle it, one line>
  If wrong: <what breaks, for whom>
  Could help: <role>, <why they hold the context>
  Lean: <one clause, only when the code or the ticket thread supports it>

Settled
- <the fact>, per <source>.

Not reachable: <the sources CLAUDE.md names and this session could not reach>.
```

Roots first, ordered by how many decisions each dissolves; then decisions by what the if-wrong line costs. Sections with nothing in them are omitted, headings included. Zero decisions is a success; never invent one.

## Rules

- Never asks the user anything. Never recommends beyond the Lean clause, never offers options, never numbers questions, never proposes a target, size, priority, or date.
- A quick patch is never a peer of a fix; when the honest decision is whether to fix or patch, the line says so.
- Never edits the draft, never writes to the tracker, never starts the work, never enters plan mode.
- Non-interactive is the only mode. The list is the whole output.

## When something is missing, say so in one line

- Nothing in the conversation and no argument: say what a seed is, once, and stop.
- Key given, no tracker connection: the key is carried, the item unread, and Not reachable says tracker.
