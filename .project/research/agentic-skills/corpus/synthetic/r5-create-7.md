Score the codebase the client ships, not the code they've abandoned

An engineering leader reading their Agent-Ready Assessment report wants to see their codebase graded, not their attic — as Northwind's CTO put it, "you graded us on code we don't ship" — a pattern the team has hit in three of the last six client engagements. At today's Northwind review, the report said "41 projects discovered, 19 without a test project" and graded Test Posture a D; the CTO checked the solution himself and counted 22 — the other 19 have sat unbuilt in a /legacy folder for two years. Roughly a B is what Test Posture would read once those 19 are set aside, and the same inflated count is what shows up as the project total on the report's cover page. Once this lands, the cover count and category scores reflect only what the client builds, and the unbuilt code appears as a single flagged finding instead of one per abandoned project.

**Acceptance criteria**
- Test Posture and other category scores are computed from the projects the client builds, not from every project folder found in the repository, so an unbuilt legacy tree doesn't cost the same as live code with no tests.
- Unbuilt legacy code appears as one finding, not one per abandoned project.
- The project count on the report's cover page matches the number the client would recognize as theirs.

**Examples**
- Northwind repo: 41 .csproj files on disk, 19 sitting unbuilt in /legacy for two years, 22 matching the client's solution → the report counts 22 projects, the 19 legacy projects show up as one finding instead of nineteen, and Test Posture reads roughly a B instead of a D.

**Decided**
- No client-facing config file or exclusion list for marking legacy code — the report has to stay reproducible from a clone with no setup on the client's part.

**Open**
- tech lead: how does this work for a client with no solution file, or with more than one? If wrong: those clients hit the same problem this story exists to fix — either their real projects are left out of the count, or unbuilt ones get graded as if they were live.
- unassigned: does a project that's listed in the solution but has never been built in CI count as live, or as more unbuilt code? If wrong: a project that looks current on paper but is never exercised keeps getting graded as maintained, or a project that is maintained loses credit for tests it actually has.
- unassigned: do the legacy projects' own conflicting READMEs already affect the Agent Context score? If wrong: the same graveyard content this story pulls out of Test Posture and Existing Code Readiness keeps skewing Agent Context too.
