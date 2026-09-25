Grade only the Projects the client builds

Client engineering teams need the Report's Projects Scanned count and Category Sub-Scores to reflect only what they actually build, so a reader recognizes the number and moves on to the Punch List instead of stopping to dispute it. Delivering the Northwind Report this morning, Priya reached Existing Code Readiness — "41 projects discovered, 19 without a test project" — and the CTO stopped her: "we have 22 projects," pointing to the 22 in the solution; the other 19 sat in an unbuilt /legacy folder nobody had built in two years, and the same 19 pulled Test Posture down to a D. His words: "you graded us on code we don't ship," and on what the mistake means for an agent: "if your tool can't tell the difference between our product and our attic, how is an agent going to?" Today the tool counts every Project it finds on disk toward the Overall Score and every Category Sub-Score regardless of whether the client still builds it, so an unbuilt folder like /legacy grades and counts the same as the code the Target Repository actually ships.

**Acceptance criteria**
- The Overall Score and each Category Sub-Score are computed only from Projects the client currently builds, not from Projects sitting unbuilt in the Target Repository.
- Unbuilt Projects are reported as one Finding, not one Finding per unbuilt Project.
- The Report's Projects Scanned count matches the number of Projects the client would state for their own Target Repository, not every .csproj found on disk.

**Examples**
- 22 Projects in Northwind's .sln, 19 more .csproj files sitting in an unbuilt /legacy folder for two years → the Report reads "22 Projects scanned," Existing Code Readiness and Test Posture graded on the 22, and one Finding naming the 19 unbuilt Projects instead of 19 separate missing-test Findings.
- The same 19 unbuilt Projects → dropped from every Category Sub-Score that counts Projects, Existing Code Readiness and Test Posture both, not filtered out of one and left counted in the other.

**Decided**
- Dead code stays a Finding, not a silent exclusion — an agent would still find it — but as one Finding for the folder, not one for each unbuilt Project: the client said he'd accept "19 dead projects, that will confuse an agent" as a single row, and did not accept being graded on nineteen of them.
- No client-supplied config file listing what to exclude: the Report has to stay reproducible from a clone with no setup, and a client-maintained exclusion list breaks that.

**Open**
- Dana: when a Target Repository has no .sln, or has more than one, which Projects count as built? If wrong: a repo with no .sln falls back to grading every Project on disk the same as today, or a repo with multiple .sln files picks the wrong one and shows a Projects Scanned count the client doesn't recognize.
- Unassigned: does a Project that's in the .sln but has never been built in CI count as built, or as unbuilt like /legacy? If wrong: a Project the client considers dead still counts toward the Overall Score, or a Project they consider live gets folded into the unbuilt Finding and drops out of its Category Sub-Score.
- Unassigned: do the old READMEs inside unbuilt /legacy Projects, which contradict the root README, currently count against the Agent Context Category? If wrong: Agent Context stays graded on unbuilt code the same way Test Posture and Existing Code Readiness were, the same complaint the CTO raised.
