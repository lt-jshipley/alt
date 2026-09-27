---
name: epic-review
description: Reads an epic draft as the person who would sign the bet and the team that would slice it, edits what four questions name, runs the script, and returns the edited draft with one line per change and what it could not fix. Never reads code, never adds a fact the seed does not hold, never writes to the tracker. Use when epic-create runs it before the write, when the user asks to review an epic draft, or invokes /alt:epic-review.
argument-hint: [path to the draft, and the seed it was written from]
---

# epic-review

A draft written by one head carries that head's solution and that head's numbers. This skill reads it with another: the decider who would sign the bet, the team that would inherit it. It edits only what a question names, says what it changed and why, and hands back what it could not settle. It never writes the epic anywhere.

## Inputs

$ARGUMENTS names the draft and the seed: a file path each, or the draft pasted with the seed beside it, and may carry a list of the product's words. The seed is the full record of what the room said, never a summary of it; a summary is refused in one line. Read the draft and the seed in full before anything else. A word on the product list is the product's, not the seed's, and is never cut for being absent from the seed. Read nothing else. Code, tests, docs, and the tracker belong to the writer's homework and the builder's pass, not to this one.

Read `${CLAUDE_PLUGIN_ROOT}/skills/epic-create/template.md` for the shape.

## Four questions

Read the draft once per question. Each names what to fix; fix it in place, and carry the fix to every line that makes the same claim.

**Need.** What this epic would cause to be bet on, against what the seed wanted.
- Are the title and the first sentence the pain or the need of the people the product serves, in their words when the seed has them, and not the ask, the feature, or the consultant's problem? Otherwise rewrite them from the seed's words.
- Is every choice the seed made under Decided, including a proposal someone turned down and why? A missing one is added with its reason from the seed.
- Does any Decided line give a reason the seed does not hold? The reason goes; the line stays if the seed holds the choice.
- Does the Bet's first line name what is imagined as a guess, not as a requirement or the need restated? Otherwise reword it.

**Workable.** Whether the team could slice it the day Open closes.
- Does any number appear that the seed or a cited source does not hold? It goes; a slot the seed cannot fill is the unmeasured line.
- Does every Open line's If-wrong name the outcome or a Bet line? One that names only a build consequence leaves for the story, said under Changed.
- Is every question the seed left open under Open? A missing one is added, unassigned unless the seed handed it to someone by name.
- Was every name on Decides or Measure handed that seat in the seed? Summarising, answering, or raising is not being handed it; a seat nobody was handed is omitted.

**How kept out.** How much of the how reached the page.
- Does any line, Open and Decided included, name a mechanism: a file the tool reads, a walk, a parse, a fallback, a lookup, or a negated clause that describes today's mechanism? Cut the clause. If the line has nothing left, it moves to Open unassigned or leaves.
- Does any line record how the product works today as fact? It is a question or nothing.
- Is any Open line in build words rather than the words of the people who have the need? Reword it from the seed.

**Template.** Whether it respects the shape.
- A name, handle, channel, timestamp, or "the thread" anywhere but Open and the two seats goes. A person who said something in the seed is not named for it.
- A line that lists children, a section not in the shape, a date, a size, a priority, or a confidence word goes.
- A Decided line that says what the epic leaves out goes.
- A fourth line in a section: the weakest goes, and Could not fix says which and why.

Then run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/epic-create/scripts/check.py <draft> <seed>`. Fix each line it prints and run it again. If the script is missing or fails to run, do its checks by hand and say so in one line.

## Output

```
Reviewed <draft>, against <seed>.

<the edited draft, in full>

Changed
- <section>: <what moved or went>, because <the question it failed>.

Could not fix
- <the line>: <why>, and <what the runner or the room decides>.
```

Changed holds one line per edit and nothing else. Could not fix is omitted when empty. No score, no verdict, no summary of the epic.

## Rules

- Edits only what a question names. Never rewrites for style, never adds a fact the seed does not hold, never adds a line to fill a section.
- Never changes a quoted string. A product word it doubts goes under Could not fix.
- Never reads code, tests, docs, or the tracker. Never asks anyone anything.
- Never writes the epic to a tracker or to any file other than the draft it was given.
- Never starts the work, never enters plan mode.
- Non-interactive is the only mode. The output is the whole result.

## When something is missing, say so in one line

- No draft: say what the inputs are, once, and stop.
- No seed, or a summary in place of one: review against the draft alone; Need's and Workable's seed questions are skipped and the output says so.
- Draft not in the shape: say so and stop; epic-create writes the shape.
