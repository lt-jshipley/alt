Score and count what a client actually builds

The client being assessed is the one who has to defend the report's cover-page number, and Northwind's CTO put it bluntly: "you graded us on code we don't ship." He stops having code his team doesn't build — 19 projects sitting untouched in /legacy for two years — counted toward the score or the cover-page count, and starts seeing the 22 projects his solution actually holds, with Test Posture nearer the B those 22 earn than the D the extra 19 produced. This morning's delivered report read "41 projects discovered, 19 without a test project"; he pulled up the solution and counted 22. Once this lands, the cover reads "Projects scanned: 22," Test Posture and Existing Code Readiness score only those 22, and the punch list carries one Finding for the 19 unbuilt /legacy projects instead of nineteen missing-test Findings.

**Acceptance criteria**
- Overall Score, Test Posture, and Existing Code Readiness reflect only the projects the client builds; a project that hasn't built in two years, like Northwind's /legacy folder, doesn't count against either Sub-Score or the Overall Score.
- The cover page's "Projects scanned" count is a number the client recognizes as their own — 22 for Northwind, not 41.
- A folder of code the client doesn't build produces one Finding, not one per project it touches — Northwind's 19 unbuilt /legacy projects become one Finding, not nineteen missing-test Findings.

**Examples**
- Northwind has 22 projects in its solution and 19 more sitting in /legacy, untouched for two years → the cover reads "Projects scanned: 22," Test Posture scores only the 22, and the punch list carries one Finding naming the 19 unbuilt /legacy projects instead of nineteen missing-test Findings.

**Decided**
- No config file for a client to list what to exclude — the report has to stay reproducible from a clone with no setup.
- Not excluding /legacy from the report entirely — an agent would still find and trust that code, so it surfaces as its own Finding instead of dropping from the score.

**Open**
- @Dana: What counts as "built" when there's no .sln, or more than one — two clients build per project with no solution file, and some have several? If wrong: a client without a solution file gets the same disk-walk noise Northwind did, or the wrong solution's projects get counted as the client's real total.
- Unassigned: Does a project that's in the solution but has never been built in CI count as built? If wrong: a project that's listed but never actually runs scores as if it's real, or a genuinely live project gets folded into the unbuilt Finding by mistake.
- Unassigned: Does the Agent Context category also get thrown off by /legacy's own stale READMEs, the way Test Posture and Existing Code Readiness did? If wrong: this fix leaves a second place the same graveyard folder skews the grade, and the next client with one gets an Agent Context surprise too.
