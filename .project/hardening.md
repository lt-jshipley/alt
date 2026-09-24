# Hardening: what the 2026-09-21 review found

Temporary. Tracks the failings a review of story-refine, epic-refine, triage, sources-sync, and brief-create found, ranked by the value of fixing each. Delete this file and its line in CLAUDE.md when every item is done or dropped.

Review summary: research corpus 5, story-refine 4, epic-refine 4, triage 4, sources-sync 3, brief-create 3. Not ramblings; the weak points are legibility to outsiders and the lack of real runs, not the ideas. Full reasoning lived in the review conversation; what matters is below.

## Order of work

Decided 2026-09-21, no client available for some weeks. Value ranking is below; this is what to do now, in order.

Now
1. Examine flood (item 2). Reproducible headless; fix it before field runs so they test the design, not a known defect.
2. Glossary (item 3, first half). Cheap; a client team will read the skills within weeks. Hold the plainer-words pass until field runs exist on the current wording.
3. Dogfood on this repo (item 1, partial). Real code, real GitHub Issues from the roadmap and this file; first exercise of a live tracker connection and of sources-sync end to end. One-person team, so not client evidence.
4. Run-log template (item 1, prep). What to capture per client run so runs yield evidence, not impressions.
5. review-prose dry read of triage (item 4, prep). Report only, cut nothing; a candidate list to check against field runs.

Waiting on a client
- Client runs (item 1), the density cuts (item 4), the plainer-words pass (item 3, second half), and item 5.

Decide now, no work
- The sources-sync pointer line in a consuming repo's CLAUDE.md. Yes or no, recorded under Decided below.

## Items, by value if fixed

### 1. No field evidence (value 5)
Every skill has one or two headless fixture runs with no tracker, no code, and no team. The README's "proven useful more than once" is true of the approach, not yet of these skills. Two or three client runs de-risk every other item here.
Now
- [ ] Write the run-log template: what held, what drifted, ignored or misread clauses, Open line count, minutes spent
- [ ] Dogfood: create GitHub Issues in this repo from the roadmap and this file, run sources-sync, then story-refine, epic-refine, and triage against them; log each
On a client
- [ ] Run story-refine on a real tracker item in a real repo
- [ ] Run epic-refine on a real epic with children
- [ ] Run triage on a real board or epic scope
- [ ] Fill the run log for each
- Notes: first real-code run 2026-09-24, six story-refine stories in agent-ready-assessment, reviewed by five role agents rather than run-logged; findings and the template changes in `story.md`, Field run. The run-log template is still unwritten.

### 2. Examine floods empty rooms (value 4)
Story fixture: eleven Open lines against four cases. Epic fixture: six. Every skill invokes examine, so the defect multiplies and the Open section is the suite's first impression. Likely small: a cap, or a collapse of "facts not reachable" into one line when no code or tracker is present.
- [x] Decide the mechanism. 2026-09-22: the flood was a coupling, not tuning. Examine is a junior's interview; the callers only need the decision list. New skill `alt:decisions` carries the method without the interview, roots only, facts collapsed to one Not reachable line. Examine untouched.
- [x] Point story-refine, epic-refine, and brief-create at decisions
- [x] Re-run the fixtures. 2026-09-22: story nine against eleven, epic seven against six. Structural leaks gone; empty-room count is inherent. Findings and proposed caller fixes in decisions.md. Interactive case untested.
- Notes: research in `.project/research/agentic-skills/decisions.md`. Watch whether callers need to re-invoke when a runner's answer brings Dissolves children onto the frontier.

### 3. Private dialect (value 4)
Runner, room, seat, hat, wound, shape, the record. Blocks marketplace adoption and is a model-correctness risk since these words carry no priors. Does not affect whether the skills work for the author today.
Now
- [ ] Write the glossary file: runner, room, seat, hat, wound, shape, the record, and any other word the skills lean on
- [ ] Point the README at it
After field runs
- [ ] Decide whether to swap for plainer words in the skills themselves
- Notes: 2026-09-24, "per the runner" reached a public tracker in the first real run; 0.11.1 rules the dialect out of anything written outside the session and gives the developer preset a Runner hat.

### 4. Density (value 3)
Skill files run 500 to 1100 words of packed rules; the triage fixture drift (a parent set from a comment) is the evidence. Fix after item 1 shows which clauses the model ignores; cutting blind removes the wrong ones. review-prose exists for this.
Now
- [ ] review-prose dry read of triage: report only, cut nothing; keep the candidate list here
After field runs
- [ ] List the clauses the runs showed ignored or misread
- [ ] Cut where the candidate list and the run log agree
- Notes:

### 5. Product-org sources vs plain-Jira shops (value 2)
Handled by fallbacks in each skill; the research names the tension. No further fix short of sources that do not exist. Field runs show whether the fallbacks hold.
- [ ] Watch during item 1; write here if a fallback fails
- Notes:

## Decided along the way
- Order of work above, 2026-09-21.
- sources-sync keeping seats in `.agentic/sources.md` rather than CLAUDE.md is the right call: read at point of use, scoped to alt, team-owned. Open: whether to add a one-line pointer in the consuming repo's CLAUDE.md, which would loosen the skill's "no CLAUDE.md line" rule.
