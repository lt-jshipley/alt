---
name: brief-retro
description: Reads the retro lines of every closed brief in the briefs folder's closed/ together, walks them with the user to a disposition, and appends that word and the date to each line. Edits nothing else. Use when the user asks to run the retro, review retro items, or invokes /alt:brief-retro.
---

# brief-retro

A brief's retro sees one brief, so every line in it has one occurrence and is written down, never acted on. This skill reads the closed briefs together, where a second occurrence shows, and gives each finding a disposition on the user's word. It appends that word to the line and changes nothing else.

## The pool

Every line under `### Retro` in every file in `closed/` under the briefs folder, `.briefs-local/` unless the repo's CLAUDE.md sets `Briefs:` under `## alt`, that carries a finding: not blank, not the template's placeholder, and either without a disposition or marked `held`. Nothing else in the folder is read. No folder, or an empty pool, is said in one line, and the skill stops.

## Group by what repeats

Lines that name the same home, or say the same thing in different words, form a group. A group of two or more is a second occurrence and leads. Singletons follow, grouped by home, then those with no home. One line per group on screen: the finding, the count, the briefs it came from, the home. When a line says none, propose one from the ticket, CLAUDE.md, README or the docs, the code, or a test, and mark it as a proposal.

## The walk

One group per turn, second occurrences first, then wait. Each line takes exactly one word, appended as ` · <word> <date>` the moment it is decided.

- `applied`: the user will make the change through normal practice. Name the edit in one line; never make it.
- `dropped`: shown no more.
- `held`: stays in the pool for a later occurrence.

The walk may stop early, never silently. Every turn ends with the same ask:

```
applied, dropped, or held, by line or for the group. Or stop.
```

## Close

```
Applied: <count>. Dropped: <count>. Held: <count>. Still in the pool: <count>.

Applied, for you to make
- <the edit, in one line> → <home>
```

Then stop.

## Rules

- Edits nothing but retro lines in closed briefs, and only by appending a disposition. A finding is never reworded, reordered, or removed.
- Never makes the change a finding asks for, never opens or edits a brief, never enters plan mode.
- A line that does not parse as `- <finding> → <home or none>` is reported once, not guessed at.
- A non-interactive run reports the pool grouped and stops; the walk needs the user present.
- On a re-run, `held` lines return; `applied` and `dropped` do not.

## When something is missing, say so in one line

- No `closed/` under the briefs folder: nothing closed yet.
- A closed brief with no Retro section: name it and skip it.
