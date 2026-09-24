# Decisions: research notes

Started 2026-09-22. Research behind `alt:decisions`, the skill story-refine, epic-refine, and brief-create invoke against their drafts in place of examine. Not a book study; a split decided in conversation after the 2026-09-21 review and recorded here so it can be reversed or merged later.

## Why it exists

The 2026-09-21 review found examine flooding Open in every headless fixture: eleven lines against four cases on story, six on epic. The conversation on 2026-09-22 traced the flood to a coupling rather than a tuning problem.

- Examine was built for a junior developer working alone: one question a turn, options tagged fixes or defers, a recommendation, to-undo, the share/more/settled verbs, a frontier paced for a person. That is pedagogy, and it is what the callers do not consume.
- What the callers consume is narrow: the decisions the draft silently assumes, each with an if-wrong line and a could-help hat, split into what the runner settles and what goes to the team.
- Each caller already has its own Ask section, so invoking examine gave the runner two interviews for one artifact.
- Examine has no non-interactive clause. Headless, with nobody answering, the model improvised and dumped every candidate; unreachable facts leaked in as one team line each.

Two skills rather than one with a mode, so a change at one level does not move the other. Examine has not yet been tested with a junior; the runner expects it to change once it is, and expects some of what changes to flow into decisions or back.

## What decisions took from examine

The method, unchanged in substance: facts are never questions and are cited; the six angles hunted against the seed, never the runner; kill before keep, settled by the record or the cause should not exist; wound as a premise the draft gets wrong or a decision it never made with several hanging off it; if-wrong as the severity; could-help as help, not ownership; patch never a peer of a fix; money, legal, safety, identity as team conversations; zero is a success. Presets, the sources file, and examine's extension file for hats.

## What it left behind

The interview: numbered questions, options, the recommendation with its why (kept as a one-clause Lean, only when code or record supports it), to-undo, the verbs, the between-question line, the close with its read. The design tree survives as a rule, not a loop: a decision that waits on another is written under it as Dissolves, so the output is roots only. That rule is the flood limiter examine's frontier was supposed to be.

## What changed in the callers

Story, epic, and brief: "Then examine" became "Then decisions." Invoke, ask the runner each root one a turn, fold answers into the shape, `team` or no answer under Open with hat and if-wrong. Non-interactive: every root lands under Open. Brief flattens the Dissolves sub-lines, since its Open Questions is one line per question. Unreachable seats are one Not reachable line and never reach Open. Examine's own text is untouched; the README now says no skill invokes it.

## Decided 2026-09-22

- Name: decisions. Considered questions and unsettled.
- Never interviews; non-interactive is its only mode. The caller owns the one interview.
- Roots only, children as Dissolves.
- Facts collapse to one Not reachable line.
- Lean kept as one clause, conditional on evidence. Never a target, size, priority, or date.
- Reads `.agentic/alt/examine/extend-skill.md` for hats rather than its own extension file, so a repo configures hats once. Revisit if the two skills' hats ever need to differ.

## Fixture run, 2026-09-22

Headless, `claude -p --plugin-dir`, no tracker, no code, no sources file, the runner told not present. Story seed: resend an appointment reminder by SMS when the email bounces or is unopened after 24 hours. Epic seed: a chatbot for the support portal, Sales asking, password resets and invoice copies named.

Counts: story Open nine lines against eleven before; epic Open seven against six. The flood did not shrink much, and that is the honest read of an empty room: with nothing settling anything, roots are roots. The interactive case, where the caller asks each root and folds, is untested and is where the split should show.

What held: one interview owner, no numbered questions, no options or to-undo, no preset rule leaking into Open, unreachable seats as one Not reachable line, "unnamed" gone from the epic, no child created, the measures-seat line once, write skipped once, both drafts in the shape. The questions themselves were the right ones: open-tracking pixels and Apple's auto-opens, TCPA and HIPAA consent, the 24-hour window against the appointment time, whether a chatbot or a reset link is the shape, requester verification.

What it did wrong:
- Story rendered decisions' whole list in the room before the draft. The caller should ask or fold, never show the raw list.
- Story's `Parent:` line routed three questions upward and then listed each again as its own Open line. A routed question should not repeat.
- Epic kept the Dissolves sub-lines under Open; story dropped them; only brief was told to. Inconsistent. Dissolves is scaffolding for the ask, not a line for the tracker.
- Epic wrote three `Not:` lines with no boundary drawn by anyone, and "No names known; see Open" where the template says leave the name out. Possibly decisions' alternatives angle pushing epic-refine to fill; watch.
- Hats were domain guesses, developer, clinic operations, compliance, product owner, rather than the preset's four. The preset allows a guess; note whether that is what a team wants on a ticket.

Proposed, not yet made: callers never render the list; a question the Parent line routes is not repeated; Dissolves dropped in every caller's Open.

## To write

- Whether the Lean clause earns its place, or pulls the model toward recommending.
- Whether roots-only holds when a runner answers and children come onto the frontier: does the caller re-invoke, or ask the Dissolves children itself?
- What flows back to examine after the junior test.
