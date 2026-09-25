Grade a repo on the projects it builds, not every project on disk

Northwind's CTO reads the Agent-Ready report as a scorecard on the code his team ships, not on every folder sitting in the repository; once this lands, the project count on the report matches what he'd tell you himself — 22, not 41 — and the Test Posture score stops being dragged down by projects nobody has built in two years. This morning's delivery stopped at Existing Code Readiness, where the report read "41 projects discovered, 19 without a test project"; the CTO pulled up the solution, corrected it to 22, and said "you graded us on code we don't ship," pointing at a /legacy folder nobody has built in two years. Scored only against what's in the solution, Northwind's Test Posture moves from a D to roughly a B. The nineteen unbuilt projects still show up, as one finding under Existing Code Readiness naming the folder and how long it's gone unbuilt, not as nineteen missing-test findings spread across Test Posture.

**Acceptance criteria**
- The project count and every Sub-Score count only the projects a repo actually builds — for Northwind, the 22 in the solution — never a project sitting outside it.
- A project outside what the repo builds produces exactly one finding, naming the folder and how long it's gone unbuilt, not one finding per project inside it.
- "Projects scanned" on the report is a number the client recognizes as their own project count.

**Examples**
- 22 projects in Northwind's solution, 19 more in a /legacy folder nobody has built in two years and outside the solution → "Projects scanned: 22" on the report, one Existing Code Readiness finding naming /legacy and its two years unbuilt, and Test Posture scored on the 22 alone.
- A project inside the solution with no test project of its own → its own Test Posture finding, not folded into the /legacy count.

**Decided**
- A config file for the client to list what to exclude was rejected; the report has to reproduce identically from a clone with no client setup.
- Dropping the /legacy folder from the report entirely was rejected; an agent would still read that code and mistake it for real, so it still has to appear — as one finding instead of nineteen.

**Open**
- Tech lead: when a repo has no solution file, or has more than one, which projects count as built? If wrong: a repo with no solution keeps getting graded on every project on disk, or a multi-solution repo gets graded on whichever solution the tool happens to pick.
- Unassigned: does a project that's in the solution but has never been built in CI count as built? If wrong: a repo can score well on projects nobody has actually gotten to build.
- Unassigned: do a legacy project's own README or agent instructions file, contradicting the root one, still count against Agent Context? If wrong: the same dead code keeps dragging down a second category after Test Posture and Existing Code Readiness are fixed.
