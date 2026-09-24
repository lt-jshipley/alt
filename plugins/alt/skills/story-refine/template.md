[Title: a verb phrase saying what the system will do]                    [Parent key, or none]

[One to three sentences: the role, what they can do once this lands, what is broken today, and the stake. Whose need it is lives here, never in a field.]
[The goal behind the feature, in one sentence, so polish and the point are told apart. Only on a story with no parent; a parented story reads it from the epic.]

Cases
- [condition]: [expected behavior]. Only where the behavior changes.

Checks ([where the data lives: fixtures, sandbox values])
- [input] → [observable result]. One per claim that could be wrong, runnable as written. A gate the repo applies to every change is not a check.

[Constraint: a rule no case or check would surface, and where it comes from: a doc by path, "the parent" when the epic carries it, or a person by name and date. A repo rule is a constraint only when this story's change would tempt breaking it; then one line names the rule and the temptation. Only when real.]

Open
- Split? [the part that is not ready]
- Parent: [the questions below are about the need, the outcome, or the why; they belong on the epic, or on no epic yet]
- [Hat], [name]: [the question]
  If wrong: [what breaks, for whom]

Code: [paths to start reading, each with a symbol, heading, or quoted phrase; a line number only with the commit it was read at]
Docs: [what says what this part does today and changes with it: a reference entry, a description the product shows, a README line. Omitted when nothing does.]
Lines left in brackets are removed, not written. Sections with nothing in them are omitted, headings included. An answered Open line leaves as one comment: `Closed from Open: <the question> <the answer>, per <name>, <date>.` Any other comment carries the source for what the description asserts; a section nothing in the description rests on is not written, and the description says where it went when it went somewhere.
