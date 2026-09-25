Grade on the projects a repository builds, not every project on disk

Northwind's CTO, the client whose repository gets graded, told the consultant delivering the report "you graded us on code we don't ship" after the score counted 19 projects his team hasn't built in two years. Once this lands, he stops disputing a project count he doesn't recognize and starts seeing 22 on the cover instead of 41, the number that matches his own solution. This morning's report read "41 projects discovered, 19 without a test project," pulling down Existing Code Readiness and Test Posture together, when only 22 of those projects are in the client's solution and the other 19 sit in a /legacy folder nobody has built in two years. Instead, the report should grade Existing Code Readiness and Test Posture on the 22 projects Northwind builds, and surface the 19 unbuilt legacy projects as one Existing Code Readiness finding rather than nineteen missing-test findings.

**Acceptance criteria**
- The project count on the report's cover reflects only the projects a client builds, not every project directory found on disk.
- Existing Code Readiness and Test Posture grade only the projects a client builds; unbuilt or legacy projects don't factor into either sub-score.
- Projects a client doesn't build are called out as one Existing Code Readiness finding, not as one missing-test finding per project.

**Examples**
- 22 projects in Northwind's .sln, 19 more .csproj files in an unbuilt /legacy folder nobody has built in two years → the report's cover reads 22 projects, not 41, and Existing Code Readiness and Test Posture grade only the 22.
- The same 19 /legacy projects, none with a test project → excluded from the Test Posture and Existing Code Readiness sub-scores, but still named in the Punch List as one Existing Code Readiness finding, not silently dropped and not counted nineteen times.

**Decided**
- No config file for a client to list what to exclude from grading: the report has to stay reproducible from a clone with no setup, so a project's built-or-not status has to come from what's already in the repo.
- Left out the report's nine-minute run time and how much of it /legacy accounts for: the person who raised it called it unrelated, and no one asked a question about it.

**Open**
- @Dana: When a repository has no .sln, or more than one, which projects count as what the client builds? If wrong: a repository without a solution, or with several, either grades every stray project as live again or silently drops ones that are.
- unassigned: Does a project that's in the .sln but has never been built in CI count as live, or does it grade like the unbuilt legacy ones? If wrong: a project the client believes is active gets graded like dead code, or dead code sitting in the .sln keeps grading like it's live.
- unassigned: Do the legacy folder's old READMEs count against Agent Context the way the root README does? If wrong: the same dead-code problem this story fixes in Existing Code Readiness and Test Posture may still be dragging down a third category.
