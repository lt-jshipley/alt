---
name: story-review
description: Reads a story draft as the product owner who would sign it and the builder who would challenge it, edits what four questions name, runs the script, and returns the edited draft with one line per change and what it could not fix. Never reads code, never adds a fact the seed does not hold, never writes to the tracker. Use when story-create runs it before the write, when the user asks to review a story draft, or invokes /alt:story-review.
argument-hint: [path to the draft, and the seed it was written from]
---

# story-review

A draft written by one head carries that head's solution. This skill reads it with another: the signer who would reject the work, the builder who would inherit it. It edits only what a question names, says what it changed and why, and hands back what it could not settle. It never writes the story anywhere.

## Inputs

$ARGUMENTS names the draft and the seed: a file path each, or the draft pasted with the seed beside it, and may carry a list of the product's words. Read the draft and the seed in full before anything else. A word on the product list is the product's, not the seed's, and is never cut for being absent from the seed. The seed is the record of what the room said; read nothing else. Code, tests, docs, and the tracker belong to the writer's homework and the builder's pass, not to this one.

Read `${CLAUDE_PLUGIN_ROOT}/skills/story-create/template.md` for the shape.

## Four questions

Read the draft once per question. Each names what to fix; fix it in place, and carry the fix to every line that makes the same claim.

**Value.** What this story would cause to be built, against what the seed wanted.
- Does the first sentence name whose need this is, the person the product serves, in their words when the seed has them? Otherwise rewrite it from the seed's words.
- Is every choice the seed made recorded under Decided, including a proposal someone turned down and why? A missing one is added with its reason from the seed.
- Does any Decided line give a reason the seed does not hold? The reason goes; the line stays if the seed holds the choice.
- Is there a case in the seed where two criteria apply to the same thing? If it is not an Example, it becomes the second one, in the seed's words.

**Workable.** Whether a builder could start the day Open closes.
- Does any criterion name more than the seed named: a field, a category, a count the room did not ask for? Cut it back to what the seed named.
- Does any criterion contradict another, or any Example contradict a criterion? Say which under Could not fix.
- Does every Open line say what breaks if wrong, for whom? Add the cost from the seed; if the seed does not hold it, say so under Could not fix.

**Implementation.** How much of the how reached the page.
- Does any criterion or Example outcome name a mechanism: a file the tool reads, a walk, a parse, a fallback, a lookup, or a negated clause that describes today's mechanism ("not everything found on disk")? Cut the clause. If the line has nothing left, the mechanism is a question and moves to Open, unassigned.
- Does any line record how the product works today as fact? It is a question or nothing.

**Template.** Whether it respects the shape.
- A name, handle, channel, timestamp, or "the thread" anywhere but Open goes. A person who said something in the seed is not named for it.
- A Decided line that says what the story leaves out goes.
- An owner on an Open line who was not handed that question by name in the seed becomes unassigned. Answering or raising a question is not being handed it, and a question called someone's because they raised it is not either.
- An Example whose outcome an Open line still asks about goes.
- A fourth line in a section: the weakest goes, and Could not fix says which and why.

Then run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/story-create/scripts/check.py <draft>`. Fix each line it prints and run it again. If the script is missing or fails to run, do its checks by hand and say so in one line.

## Output

```
Reviewed <draft>, against <seed>.

<the edited draft, in full>

Changed
- <section>: <what moved or went>, because <the question it failed>.

Could not fix
- <the line>: <why>, and <what the runner or the room decides>.
```

Changed holds one line per edit and nothing else. Could not fix is omitted when empty. No score, no verdict, no summary of the story.

## Rules

- Edits only what a question names. Never rewrites for style, never adds a fact the seed does not hold, never adds a line to fill a section.
- Never changes a quoted string. A headline it doubts goes under Could not fix.
- Never reads code, tests, docs, or the tracker. Never asks anyone anything.
- Never writes the story to a tracker or to any file other than the draft it was given.
- Never starts the work, never enters plan mode.
- Non-interactive is the only mode. The output is the whole result.

## When something is missing, say so in one line

- No draft: say what the inputs are, once, and stop.
- No seed: review against the draft alone; Value's questions are skipped and the output says so.
- Draft not in the shape: say so and stop; story-create writes the shape.
