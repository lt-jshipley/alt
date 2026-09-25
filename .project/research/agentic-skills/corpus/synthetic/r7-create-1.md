Count and grade only the Projects the Target Repository builds

The client who reads the Report wants the Overall Score and its Category Sub-Scores to reflect the Projects they actually build, so they stop treating the topline grade as a number to dispute before they even reach the Punch List. During the Northwind engagement, the CTO stopped the readout at Existing Code Readiness because the Report counted 41 projects discovered, 19 without a test project, while the solution he builds from holds 22 — the other 19 have sat unbuilt for two years in a /legacy folder kept only for reference. He said "you graded us on code we don't ship" — and it pulled the Test Posture Sub-Score down to a D, where the 22 Projects he ships would read close to a B. Once this lands, the Report's Projects-scanned count and its Test Posture and Existing Code Readiness Sub-Scores reflect only the Projects the client builds, with the unbuilt ones surfaced as a single Finding instead of a per-Project drag on the grade.

**Acceptance criteria**
- The Report's cover count of Projects scanned matches the Projects the client actually builds.
- Overall Score, and the Test Posture and Existing Code Readiness Sub-Scores, are computed only from Projects the client builds.
- Unbuilt Projects surface as exactly one Finding, with a Title that tells the reader how many Projects it covers and why they're excluded from the grade.

**Examples**
- Northwind's solution holds 22 Projects; a /legacy folder holds 19 more Projects nobody has built in two years, kept for reference only → the Report's cover reads Projects scanned: 22, Test Posture and Existing Code Readiness score against those 22, and Existing Code Readiness carries one Finding noting the 19 unbuilt Projects in /legacy.

**Decided**
- No config file where the client lists Projects to exclude from the grade — the Report has to stay reproducible from a clone with no setup.

**Open**
- @Dana: how does Project discovery decide what counts when the Target Repository has no solution file, or has more than one? If wrong: a client without one canonical solution gets the same "graded on code we don't ship" result Northwind did, just from a different gap in discovery.
- Unassigned: does a Project that's in the solution but has never run in CI count toward Test Posture the same as one that has? If wrong: a client could be graded on a Project nobody has actually validated, or lose credit for one CI simply hasn't reached yet.
- Unassigned: do legacy folders' own README files, which contradict the root one, already count against the Agent Context Category? If wrong: a client could still hear "you graded us on code we don't ship" about Agent Context after Test Posture and Existing Code Readiness are fixed.
