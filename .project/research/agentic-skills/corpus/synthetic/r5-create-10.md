Grade the target repository by what it builds, not by everything it contains

A client's engineering lead needs the assessment to score what his team actually ships, as he told the consultant on site: "you graded us on code we don't ship." Once it does, he can accept a Test Posture grade that reflects a real gap instead of rejecting a D that would read as roughly a B without nineteen unbuilt projects mixed in. The delivered report read "41 projects discovered, 19 without a test project," but the client's solution held 22 — the other 19 sat unbuilt in a `/legacy` folder untouched for two years. Once this lands, Projects scanned reads 22, the Sub-Scores it feeds are computed from those 22, and the 19 unbuilt projects surface as one Finding instead of a project-by-project drag on the score.

**Acceptance criteria**
- The Overall Score, and the Test Posture and Existing Code Readiness Sub-Scores it rolls up, are computed from the projects the target repository builds — projects sitting unbuilt in the repo are not scored as live projects missing tests.
- The target repository's unbuilt code still surfaces, as a single Finding naming the folder and how many projects it holds, not as a Finding against each unbuilt project.
- Projects scanned, on the report's scorecard, counts the projects the target repository builds, not every project found anywhere under the repo root.

**Examples**
- A repo with 22 projects in the solution and 19 more sitting in an unbuilt `/legacy` folder untouched for two years → Projects scanned reads 22, the score reflects the 22, and the 19 legacy projects appear as one Finding, not nineteen.
- One of the 22 solution projects has no test project of its own → still its own Finding in Test Posture; the fold into one Finding only applies to the unbuilt projects, not to a gap in what's actually shipped.

**Decided**
- No config file for a client to list what the assessment should exclude — the report has to stay reproducible from a clone with no client setup, the same reason every other judgment call in this tool works from what's in the repo rather than what someone tells it to ignore.

**Open**
- tech lead: when the target repository has no solution file, or has more than one, which one decides what counts as built? If wrong: the same "you graded us on code we don't ship" objection returns for a different client, by a different route.
- unassigned: does a project inside the solution that has never been built in CI count as live, or does it belong with the excluded unbuilt code? If wrong: the score either credits a project nobody has actually run, or excludes one the client considers shipped.
- unassigned: do Agent Context findings against unbuilt legacy projects' own README files, which contradict the root one, need the same built/unbuilt split? If wrong: an agent is still misled by a legacy project's stale instructions, in a category this fix never touched.
