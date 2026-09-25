# Restart prompt: story-create smoke and corpus

Paste everything below this line into a fresh Claude Code session opened in /Users/jshipley/Development/agent-ready-assessment.

---

We maintain the `alt:story-create` and `alt:story-review` skills, which live in the alt plugin repo at /Users/jshipley/Development/alt under `plugins/alt/skills/story-create/` (SKILL.md, template.md, scripts/check.py) and `plugins/alt/skills/story-review/` (SKILL.md). Read `/Users/jshipley/Development/alt/.project/research/agentic-skills/story-concept.md` first: it holds the people and templates this shape came from, where we landed, the Northwind test case, the seed kinds, and a one-line issue log of everything that broke and what we did. Do not re-derive any of it.

## State

- alt is at 0.15.2. If `git status` in the alt repo shows uncommitted changes, commit and push them first, then run `/plugin update` and `/reload-plugins` and confirm `~/.claude/plugins/cache/agentic-leantechniques/alt/` has a `0.15.2` folder holding `skills/story-review/SKILL.md`.
- story-create runs story-review in a fresh sub-agent before the write, hands it the product words the draft uses, and shows its Changed and Could not fix lines beside the draft. The five Before-showing questions live in story-review. The reviewer never changes a quoted string, drops a Decided reason the seed does not hold, carries a fix to every line that makes the same claim, and does not treat a raised question as an assigned one.
- `alt:story-refine` is retired in place. Do not edit it or run it. It goes when the builder's pass exists.
- The Northwind transcript is the fenced block under "Test case" in story-concept.md, and a verbatim copy sits at `corpus/synthetic/northwind-seed.md` beside this file. Copy it to a scratchpad file named `northwind.md`.
- Round five (0.14.5, ten Sonnet runs, before story-review) scored 10 to 19 on the value ranking below. The first smoke (0.15.0, three runs) summed 15 to 17; the second (0.15.2, five runs) summed 14 to 18, mean 16.8, check.py silent everywhere. A composition run over three drafts scored 18 and was not worth four runs; its dropped list produced the 0.15.2 edits. The ten-run gate is retired. Two things measure the skills now: a smoke after any skill edit, and the corpus of client uses.
- Two blind spots are logged and not fixed: the review cannot see a missing Open line, and "every Sub-Score" survives when the seed says "the grade". Each appeared once or twice; the rule for an edit is two or more across smoke runs or corpus entries.
- Parked, in the research file and `~/Development/lt-mcp-backlog/docs/hosting-concept.md`: the reviewer returning findings the writer consumes instead of edits; many cheap finders aggregated by count; a free model as a tool behind a remote MCP server so the business surface can be claude.ai. None of it is built.

## Smoke

Run after any edit to either skill, the template, or the script. Launch three to five Sonnet agents in one message, each with exactly this prompt and its own output file `rN-create-K.md`, where N is the round number (the next is 8) and K is 1 to the count. Each run takes ten to fourteen minutes because the review runs as a nested sub-agent; the reviewer inherits the writer's model unless the skill says otherwise.

> Working directory: /Users/jshipley/Development/agent-ready-assessment
>
> Invoke the skill `alt:story-create` and follow it to write a story from the pasted transcript at: <path to northwind.md>
>
> Read that file first. Treat its contents as the seed, a pasted draft in the room.
>
> Two standing instructions, nothing else:
> - Nobody is present to answer questions. Any question the skill would ask goes under Open instead.
> - Do not write to GitHub or any tracker, and do not edit either repo. Write the finished story body to: <path to rN-create-K.md>
>
> When done, report back, in this order:
> 1. The story body in full and its word count.
> 2. Every file you read, in the order you read it, one line each.
> 3. Whether check.py ran, what it printed on the first pass, and how many passes you made.
> 4. For each section, how many lines you wrote and one sentence on how you chose that number.
> 5. Any place the skill was silent or contradicted itself and what you did about it.
> 6. story-review's Changed and Could not fix lines, as returned.

Carry no other instructions to the agents. The brief is the control; the skills are what is being tested.

## Measure

Read every draft as the product owner who would sign it and the builder who would challenge it. Score each draft 1 to 5 on four columns. Higher is better in every column. Sum them.

**Value.** What the story would cause to be built, judged against what the seed wanted.
- 5: the client's need in their words, every decision the room made recorded including rejected alternatives, and the sharpest edge in the seed written as an example.
- 4: the room's asks all present, one of the above missing.
- 3: the asks present but the room's disagreement or its resolution is gone, or a decision was dropped.
- 2: the need is the consultant's, or a rule the room did not agree to.
- 1: the story would build the wrong thing.

**Workable.** Whether a builder could start the day the Open lines close.
- 5: no criterion contradicts another, none is broader than the seed, every Open line says what breaks if wrong.
- 4: one criterion a builder would have to ask about.
- 3: scope crept past the seed, or an Open line has no cost.
- 2: a criterion cannot be tested, or two pull against each other.
- 1: the builder inherits a design or a contradiction.

**Implementation kept out.** How much of the how reached the page.
- 5: no mechanism anywhere but Open.
- 4: mechanism only in an example's input, in the seed's own words (the solution file the CTO named).
- 3: mechanism in a criterion's negated clause ("not everything found on disk", "not folders walked").
- 2: mechanism as a positive rule in a criterion or example ("referenced by the solution").
- 1: the fix proposed in the seed written as a rule.

**Template and the thought leaders.** Whether it respects the shape and still reads as a card that reserves a conversation, in a product company that needs more written down than Jeffries, Wake, Cohn, North, Keogh, Adzic, Cockburn, Fowler or Patton would have.
- 5: card-sized, roles or handles only in Open, one or two examples, every section present earns its place.
- 4: one template rule bent in a way only the checker would notice.
- 3: a rule broken in a way a reader would notice: a name in the opener, noise in Decided, an owner invented, a section padded.
- 2: template text echoed into the story, or the shape drifted toward a ticket.
- 1: not in the shape.

Then run `python3 <cache>/0.15.2/skills/story-create/scripts/check.py` on every final draft and record what it prints. Record per run: words, number of passes, what the first pass printed, and the number of Changed lines story-review returned.

## Report back

In this order, summary first, then bullets, no walls of text.

1. One line: smoke passed or failed, the sum range, the word range, check.py.
2. The value table, one row per run sorted by sum, four columns and the sum.
3. Per run: words, passes, first-pass output, Changed count.
4. What the top draft did that the others did not, quoting the line.
5. Where value and the rules diverge: any draft a rule category would penalise for a line the value ranking rewards, or the reverse.
6. Concepts. For every column where two or more runs scored 3 or below, name the concept that produced it: what the writer was reaching for, and where the skill or template gave it no place or the wrong place. Quote one line per run. Then, for the Changed lines: which the runner would have made anyway, which they would reverse, and which added a fact the seed does not hold. A concept seen once is noted and not fixed.
7. Options, in the round's form: a deletion, a number, a routing rule, or a script check, before any new sentence. Say which is durable and which is a stopgap, and recommend one.

Do not edit anything on the strength of the report. Edits are asked for.

## Smoke condition

Fails only if check.py prints anything on a final draft, any value column scores 2 or below, or a Changed line adds a fact the seed does not hold. No spread condition, no whole-score gate.

## Corpus

Each client use of story-create adds one file to the alt repo at `.project/research/agentic-skills/corpus/<date>-<slug>.md`, anonymised. It holds, under five headings: the seed kind (from story-concept.md), the draft before story-review, the draft after, story-review's Changed list, and the runner's edits before the write. The runner's edits are the measure. The same edit in three entries is the next skill change, in the form below. Smoke runs do not go in the corpus.

## If it fails, or the corpus repeats itself

- A concept that appears in two or more smoke runs or corpus entries is a pattern. Fix the place in the skill or template that produced it, in output form (what the line looks like), not as a reason.
- A concept that appears once is logged and left.
- Prefer a deletion, a number, a routing rule, or a script check over a new sentence. Five rounds showed prose rules stopped shrinking variance; numbers, deletions, routing rules and the script did.
- Do not add a rule per failure.
- Log each new finding as one line in the issue log at the bottom of story-concept.md (beside this file in alt's research folder), in its stated form.

## Rule categories

Vocabulary for naming what a low score is made of. Not scored per run unless asked.

1. The how refused: no criterion or Example states a mechanism (solution file, disk walk, "listed in", "referenced by", "on disk", "discovery finds").
2. Nothing named the thread did not name: no invented filenames, headlines, check ids, or edges the thread contradicts.
3. No attribution outside Open: no names, "per X", timestamps, handles, channel names, or "the thread" on the opener, Decided or Example lines.
4. Opener at four sentences.
5. Unchecked claim in Open, not Examples (Priya's README guess).
6. Noise dropped: the nine-minute run time appears nowhere, including as a Decided line saying it was left out.
7. Sections at up to three lines and not padded with a restatement.
8. Owners not invented: Lena's parked question is unassigned or a role. Not Dana, who answered it, and not Lena, who raised it.
9. No Example decides a question Open still holds (the no-solution case).
10. First sentence names whose need this is, the client's, in the CTO's words where possible, not the consultant's, and not the template's bracket paraphrased.
11. Decided is rationale only: a rejected alternative and why. A rejected alternative that an Open line then reopens is a Decided line, not a restatement. A Decided line that answers an Open line is a defect.

## Standing rules for this work

- Conversations are requests to discuss. Edit only when asked.
- Summaries first, then bullets. No walls of text.
- Bump the alt version on every skill edit or installed copies do not change.
- Commit and push only when asked.
- Nothing is written to GitHub issues in this round.
