Grade only what the target repo builds; surface unbuilt code as one Finding

A client stakeholder reading the Report — the CTO on the Northwind engagement — needs the Overall Score and every category Sub-Score to reflect only the projects their team actually builds and ships, not everything sitting on disk. Once it does, they stop rejecting the Report's numbers as describing code that isn't theirs and start treating a project count they recognize as their own as worth acting on. Delivered the morning of the Northwind readout, the Report's cover read "Projects scanned: 41," Existing Code Readiness reported "41 projects discovered, 19 without a test project," and Test Posture graded a D; the CTO stopped there, pulled up the solution, and said "we have 22 projects" — the other 19 sit in a /legacy folder nobody has built in two years, kept only for reference. Once this lands, the Report's cover reads "Projects scanned: 22," Existing Code Readiness and Test Posture score against those 22, and the 19 untouched /legacy projects show up as a single Finding instead of nineteen separate deductions.

**Acceptance criteria**
- The Overall Score and every category Sub-Score, including Existing Code Readiness and Test Posture, are computed only from the projects the client actually builds and ships.
- Projects excluded from scoring as unbuilt still appear in the Report, as one Finding covering all of them together, never as a separate deduction per excluded project.
- The cover's project count states the number of projects the client would recognize as theirs.

**Examples**
- 41 projects on disk, 19 of them in a /legacy folder untouched for two years and kept only for reference → cover reads "Projects scanned: 22"; Existing Code Readiness and Test Posture score only the 22 the team builds.
- Those same 19 unbuilt projects, previously worth 19 separate no-test-project deductions → one Finding, worded so it says what an agent risks by finding and trusting code the team doesn't ship, not zero Findings and not nineteen.

**Decided**
- Not adding a config file for the client to list what to exclude from scoring: the Report has to stay reproducible from a clone with no client setup.
- Not dropping the 19 unbuilt projects from the Report entirely: an agent will still find and read that code and assume it's real, so it has to appear as a Finding rather than disappear.

**Open**
- Unassigned: does a project that counts among what the client builds, but has never actually been run in CI, still count as live, or does it get treated like unbuilt /legacy code? If wrong: a project the client considers current could get graded like dead code, or dead code with no CI trail could keep counting as live and pull the grade down the same way /legacy did.
- Unassigned: do the legacy projects' own README files, which contradict the root README, currently count against Agent Context? Nobody checked. If wrong: Agent Context could still be dragged down by /legacy content the same way Existing Code Readiness and Test Posture were, leaving part of the same problem unfixed.
