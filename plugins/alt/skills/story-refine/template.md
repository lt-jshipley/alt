[Title: a verb phrase saying what the system will do]                    [Parent key, or none]

[One to three sentences: the role, what they can do once this lands, what is broken today as it was seen (the report, the repo, the date), and the stake. Whose need it is lives here, never in a field.]
[The goal behind the feature, in one sentence, so polish and the point are told apart. Only on a story with no parent; a parented story reads it from the epic.]

Cases
- [a situation the person could set up without reading the code]: [what they see, in the product's own words]. Rules, not examples; the examples are Checks. Every string the product shows that this change touches, as final wording. Data a rule turns on, a list, a map, a threshold, is the what: a short table here, a cited comment when long. Never the mechanism.
- [The strings this change leaves alone, in one line. Only when a reader would wonder.]

Checks ([where the data lives: a repo shape, a sandbox value])
- [input] → [what the report or CLI shows]. One per claim that could be wrong and at least one per case; a case with no check is an Open line. A demonstration someone could run in front of the team. Never the test that proves it. A gate the repo applies to every change is not a check.

[Constraint: a limit no case or check would surface, stated as the outcome it protects, and where it comes from: "the parent", an ADR, or a person by name and date. A repo rule is a constraint only when this story's change would tempt breaking it; then one line names the rule and the temptation. A rule shared with another story lives on the parent or in an ADR and is cited, never restated. Only when real.]

Open
- Split? [the part that is not ready]
- Parent: [the questions below are about the need, the outcome, or the why; they belong on the epic, or on no epic yet]
- [Hat], [name]: [the question]
  If wrong: [what breaks, for whom]

Docs: [what the reference entry must say once this lands. Product strings are Cases. Omitted when nothing changes.]

If the code contradicts a line above, the line missed the need. Work out what the need requires, alone, with an agent, or with the team, before building.

Lines left in brackets are removed, not written. Sections with nothing in them are omitted, headings included. The last sentence is written as is. Nothing in the story says how: no file, symbol, helper, sibling, fixture, or test name; a path appears only as the source of a constraint. An answered Open line leaves as one comment: `Closed from Open: <the question> <the answer>, per <name>, <date>.` Any other comment carries the source for what the description asserts and a reader might dispute; a section nothing in the description rests on is not written, and the description says where it went when it went somewhere.
