Grade the Projects a Target Repository ships

A client stakeholder reading the Report — the person who has to defend the grade afterward, the way Northwind's CTO did — needs the Report's project count and the Existing Code Readiness and Test Posture Sub-Scores to match the 22 Projects they build, not the 41 Discovery finds across the whole repository. Delivered this morning, the Northwind Report read "41 projects discovered, 19 without a test project" under Existing Code Readiness. The CTO stopped the consultant there — "we have 22 projects," pointing at the .sln, and "you graded us on code we don't ship" — the other 19 sit in a /legacy folder nobody has built in two years. Once this lands, the Report's project count states 22, Existing Code Readiness and Test Posture grade only those 22, and the 19 unbuilt Projects surface as one Finding instead of nineteen missing-test rows.

**Acceptance criteria**
- Existing Code Readiness and Test Posture score only the Projects the Target Repository builds; Projects outside of what's built don't count against either Sub-Score.
- The Projects that aren't built still appear, but as one Finding covering all of them, whose Title states how many there are and that they fall outside what's built — not one missing-test Finding per Project.
- The project count the Report shows matches the count it graded.

**Examples**
- 22 Projects in Northwind's .sln, 19 more .csproj files in /legacy that haven't built in two years → the Report's project count reads 22, and Existing Code Readiness no longer includes the 19.
- 19 of the 41 Projects found have no test project, all 19 inside /legacy → one Finding stating the 19 fall outside what's built, not nineteen missing-test Findings, and Test Posture grades only the 22 — close to the B estimated by hand, not the D that counted all 41.

**Decided**
- A config file for the client to list what to exclude — not added; the Report has to stay reproducible from a clone with no setup, same as always.

**Open**
- @Dana: What counts as "built" when a repository has no .sln, or has more than one? If wrong: the project count and the grade stop matching what a client with that shape of repository would recognize — the same failure this story exists to fix, for a different repository shape.
- Unassigned: Does a Project that's in the .sln but has never run in CI count as built? If wrong: a Project nobody exercises keeps grading as if it ships, or a Project that does ship gets excluded by mistake.
- Unassigned: Do the unbuilt Projects' own README files, which contradict the root one, still get counted in Agent Context? If wrong: Agent Context stays dragged down by the same dead code this story pulls out of Existing Code Readiness and Test Posture.
