Grade a repo on the projects it builds

Northwind's CTO reads the report as a scorecard on the code his team ships, not on every folder sitting in the repo; once this lands, the project count on the report matches what he'd tell you himself — 22, not 41 — and the Test Posture score stops being dragged down by projects nobody has built in two years. This morning's delivery stopped at Existing Code Readiness, where the report read "41 projects discovered, 19 without a test project"; the CTO pulled up the solution, corrected it to 22, and said "you graded us on code we don't ship," pointing at a /legacy folder nobody has built in two years. Scored only against what's in the solution, Northwind's Test Posture moves from a D to roughly a B. The nineteen unbuilt projects still show up, as one finding under Existing Code Readiness naming the folder and how long it's gone unbuilt, not as nineteen missing-test findings spread across Test Posture.

**Acceptance criteria**
- The project count and the Test Posture and Existing Code Readiness grades count only the projects a repo actually builds, never a project sitting outside that set.
- A project outside what the repo builds produces exactly one finding, naming the folder and how long it's gone unbuilt, not one finding per project inside it.
- "Projects scanned" on the report's cover is a number the client recognizes as their own project count.

**Examples**
- 41 projects discovered, 22 of them in Northwind's solution, 19 unbuilt in /legacy for two years → "Projects scanned: 22" on the report, one Existing Code Readiness finding naming /legacy and its two years unbuilt, and Test Posture scored on the 22 alone.
- A project inside the solution with no test project of its own → its own Test Posture finding, not folded into the /legacy count.

**Decided**
- No config file for the client to list what to exclude — the report has to be reproducible by us from a clone, with no setup, same reason as every other exclusion mechanism we've turned down.
- Dropping the /legacy folder from the report entirely was rejected; an agent would still read that code and mistake it for real, so it still has to appear — as one finding instead of nineteen.

**Open**
- Dana: when a repo has no solution file, or has more than one, which projects count as built? If wrong: a repo with no solution keeps getting graded on every project on disk, or a multi-solution repo gets graded on whichever solution the tool happens to pick.
- Unassigned (Lena raised it, Dana parked it): does a project that's in the solution but has never been built in CI count as built? If wrong: a project that's dead in practice keeps dragging the score down, or gets folded into the /legacy finding despite being in the solution.
- Unassigned: do the legacy projects' own READMEs, which contradict the root one, get counted against the Agent Context category? Priya flagged it but didn't check. If wrong: the same unbuilt legacy code keeps dragging down a second category after Test Posture and Existing Code Readiness are fixed.
