Grade what the client ships, not everything found on disk

Northwind's CTO needs the Agent-Ready report to grade "22 projects" — what his team actually builds and ships — not the extra ones sitting unbuilt in the repo. Once this lands, he stops rejecting a grade built on code his team doesn't ship, and the number on the cover is one he recognizes as his own. Priya delivered the report this morning reading "41 projects discovered, 19 without a test project," and the CTO stopped her — "we have 22 projects" — the other 19 are .csproj files sitting in a /legacy folder nobody has built in two years, kept only for reference. Once this lands, the cover reads "Projects scanned: 22," Test Posture and Existing Code Readiness score against those 22, and the 19 unbuilt legacy projects appear as one finding instead of pulling Test Posture down from roughly a B to a D.

**Acceptance criteria**
- The project count on the cover matches what the client would call their own — the projects they build — not every .csproj found in the repo.
- Test Posture, Existing Code Readiness, and the other category scores are computed against the projects the client builds; code outside that set does not pull those scores down.
- Code that sits in the repo but isn't part of what the client builds is still called out — as one finding, not one per project inside it.

**Examples**
- 22 projects in Northwind's solution, plus 19 more .csproj files sitting in a /legacy folder nobody has built in two years → the cover reads "Projects scanned: 22"; the 19 appear as one finding about unbuilt legacy code, not nineteen separate Test Posture findings pulling the grade from roughly a B down to a D.

**Decided**
- Not leaving the 19 legacy projects out of the report entirely — an agent working in the repo will still find that code, read it, and treat it as real, so it stays visible even though it stops dragging the grade.
- Not adding a config file for the client to list what's excluded from grading — the report has to stay reproducible from a clean clone with no setup.

**Open**
- @Dana: For a repo with no solution file, or with more than one, which projects count as what the client builds? If wrong: a client without a single clean solution file gets a cover count and grade that still doesn't match what they'd call their own.
- Unassigned: Does a project that sits in the solution but has never been built in CI count as one the client builds? If wrong: a project nobody actually ships still counts toward the grade and the cover count, reproducing the same problem inside the set that's supposed to be trustworthy.
- Unassigned: Do the legacy projects' own READMEs, which contradict the root one, currently count against the Agent Context score? If wrong: the same "graded on code we don't ship" problem stays live in a second category even after this fix ships.
