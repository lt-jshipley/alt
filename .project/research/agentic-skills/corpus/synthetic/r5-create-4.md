Grade repositories on what they build, not everything discovery finds on disk

A client's engineering leader reading their Agent-Ready Assessment report needs the score in front of them to describe the repository they actually ship, not everything discovery finds on disk — as Northwind's CTO asked, "if your tool can't tell the difference between our product and our attic, how is an agent going to?" Once the count on the report matches what he'd say — 22 instead of 41 — he stops dismissing the whole report and starts trusting the grade underneath it, the same grade that reads a D on Test Posture today and lands close to a B once the 19 unbuilt projects are counted correctly. Priya watched it happen delivering that report: it read "41 projects discovered, 19 without a test project," and the 19 turned out to be a /legacy folder nobody had built in two years. Once this lands, the report counts the 22 projects Northwind would point to, and the unbuilt 19 show up as one Finding in the punch list instead of nineteen separate hits against Test Posture and Existing Code Readiness.

**Acceptance criteria**
- The Overall Score and every Sub-Score it rolls up are computed only from the projects the target repository actually builds, not every project discovery finds walking the disk.
- The Projects Scanned count on the report is the number the client would give if you asked them how many projects they have.
- Projects discovery finds that the target repository doesn't build are reported as one Finding, not one per project.

**Examples**
- Northwind: 22 projects in the solution, and a /legacy folder holding 19 more that nobody has built in two years → Projects Scanned reads 22, not 41, and the 19 unbuilt projects show up as one Finding, not nineteen.
- Northwind's Test Posture Sub-Score, pulled down to a D by counting all 19 unbuilt projects as missing tests → scored against the 22 built projects only, and lands close to a B.

**Decided**
- Not adding a client-facing config file to list what to exclude from the count — the report has to stay reproducible from a clone with no setup, the same rule the tool already holds everywhere else.
- Not dropping the unbuilt projects from the report entirely — an agent working in the repo would still find that code and trust it as real.

**Open**
- @Dana: how does discovery decide what a repository "builds" — only what's listed in a solution file, with some fallback when a repository has none, and some tie-break when it has more than one? If wrong: repositories that build per-project with no solution file either lose every project from the count or fall back to today's disk walk, and multi-solution repositories get whichever one the tool happens to prefer.
- @Lena: does a project that's listed in the solution but has never run in CI count as built? If wrong: the report either grades a stale-but-listed project as if it ships, or excludes a project the client actually does ship.
- Unassigned: did the report count the legacy folder's own README, which contradicts the root one, toward the Agent Context score? If wrong: Agent Context either double-counts documentation the client doesn't maintain, or misses a contradiction an agent would actually hit.
