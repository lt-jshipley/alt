Grade a repo on the Projects it builds, not every Project on disk

The client whose repo gets assessed needs the report's grade to match what they actually ship: Northwind's CTO stopped the walkthrough of Existing Code Readiness this morning and said "we have 22 projects," not the 41 the report opened with, so he can stop correcting the report's own count in front of his team. The report read "41 projects discovered, 19 without a test project," the 19 were .csproj files under a /legacy folder nobody has built in two years, and the same 19 pulled Test Posture to a D that would land roughly a B without them. As the CTO put it, "if your tool can't tell the difference between our product and our attic, how is an agent going to?" Once this lands, Projects scanned, the Test Posture Sub-Score, and the Existing Code Readiness Sub-Score reflect only the 22 Projects Northwind builds, and the Punch List carries the other 19 as one finding instead of nineteen.

**Acceptance criteria**
- Test Posture and Existing Code Readiness Sub-Scores, and the Overall Score they roll into, are computed only from Projects the repo actually builds.
- The report's Projects scanned count shows the number of Projects the repo actually builds, not everything discovery finds on disk.
- Projects the repo does not build still appear in the report, as one Punch List finding covering all of them, not one finding per excluded Project.

**Examples**
- 22 Projects in Northwind's solution, plus 19 more under a /legacy folder nobody has built in two years → Projects scanned reads 22, not 41, and Test Posture and Existing Code Readiness grade from the 22 — roughly a B instead of the D the 41-count run gave.
- Those same 19 unbuilt Projects → the Punch List carries them as one finding, not nineteen findings each priced like a live Project missing tests.

**Decided**
- No config file where the client lists Projects to exclude — the report has to stay reproducible from a clone with no setup, same reason as always.
- The Northwind run's 9-minute time, mostly spent in /legacy, stays out of this story — Tom flagged it as a separate, unrelated observation.

**Open**
- @Dana: whether a Project counts toward the grade by appearing in any .sln, with a disk walk as fallback only when a repo has none, or by some other rule — since some clients build per-project with no .sln, and some carry more than one. If wrong: a client with no .sln gets every Project excluded from the grade, or a client with multiple .sln files has a live Project silently dropped from the count.
- unassigned: whether a Project listed in a .sln but never built in CI counts as live, the question Lena raised. If wrong: a repo keeps counting and grading a Project its own CI has stopped building — the same complaint Northwind raised about /legacy.
- unassigned: whether Projects outside what the repo builds have their own README files being read into Agent Context findings, the gap Priya named but didn't check. If wrong: the report keeps grading a client on documentation that belongs to code it no longer builds, the same complaint that opened this story.
