Grade the repo on what the client builds, not everything sitting on disk

The client's CTO, who reads the Report, needs the Overall Score and each Category Sub-Score to reflect the code his team ships, not code sitting unbuilt in the repo, so he stops telling the consultant "you graded us on code we don't ship." On the Northwind engagement, the Report read "41 projects discovered, 19 without a test project," while the client's own .sln held 22 — the other 19 sat in a folder nobody had built in two years. Once this lands, the Report's project count and every Category Sub-Score come only from what the client builds, and the excluded projects show up as one Finding instead of one per project.

**Acceptance criteria**
- Projects outside what the client builds do not count toward the Overall Score or any Category Sub-Score.
- Projects outside what the client builds are reported as one Finding, not as a separate Finding per excluded project.
- The project count on the Report's cover reflects only the projects graded, not every project found on disk.

**Examples**
- 22 projects in the client's .sln, 19 more in a /legacy folder nobody has built in two years → the Report's cover reads "Projects scanned: 22," the Existing Code Readiness and Test Posture Sub-Scores are built from those 22, and the Punch List carries one Finding noting the 19 unbuilt projects.
- The same 19 unbuilt projects would, graded, have shown up as deductions in both Existing Code Readiness and Test Posture → neither Sub-Score includes them, and the Punch List still carries just the one Finding, not one per affected Category.

**Decided**
- The unbuilt projects aren't dropped from the Report entirely — an agent working in the repo would still find and trust that code.
- No client-facing file lists which projects to exclude — the Report has to stay reproducible from a clone with no client setup.
- Scoping to "what the client builds" isn't defined as everything one .sln lists — some clients build without a .sln, or with several, so a single solution file can't be the whole rule.

**Open**
- Dana: which projects count as "what the client builds" when a repo has no .sln, or has more than one? If wrong: the cover count and Sub-Scores could include a client's unbuilt work again, reopening the same complaint.
- Unassigned: does a project inside the .sln that's never been built in CI still count as built? If wrong: a project nobody can actually run gets graded as shipped, the same complaint from the other direction.
- Unassigned: do excluded projects' own README files still get read by Agent Context checks against the root README? If wrong: the Agent Context Sub-Score keeps penalizing content the client doesn't ship, the same complaint in a different category.
