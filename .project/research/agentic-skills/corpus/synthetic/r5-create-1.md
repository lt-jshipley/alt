Separate unbuilt Projects from what a client ships when scoring and counting

Consultants deliver the Agent-Ready Assessment Report to clients — on Northwind, that's the CTO who told Priya "you graded us on code we don't ship." He needs the Overall Score and Test Posture Sub-Score to describe the 22 Projects Northwind ships, not the 41 the Report counted, so a grade that reads D over the full disk lands roughly a B over what they actually build. This morning, the Report's Existing Code Readiness Finding read "41 projects discovered, 19 without a test project"; the 19 came from /legacy, a folder of .csproj files outside the .sln that nobody has built in two years. Once this lands, the Report's Projects scanned count and its Test Posture and Existing Code Readiness Sub-Scores describe only the 22 Projects Northwind builds, with the 19 /legacy Projects surfaced as a single Finding rather than folded into the per-project counts.

**Acceptance criteria**
- Test Posture and Existing Code Readiness Sub-Scores are computed only from the Projects the client builds; Projects outside that set don't count toward either Sub-Score.
- Projects outside what the client builds produce a single Finding, not one Finding for each of them.
- The Report's Projects scanned count matches the number of Projects the client builds.

**Examples**
- A target repository with 22 Projects in the .sln that Northwind builds and ships, plus /legacy — 19 .csproj Projects outside the .sln, unbuilt for two years, kept for reference → the Report reads "Projects scanned: 22," Test Posture and Existing Code Readiness Sub-Scores are computed from those 22, and one Finding reports that 19 unbuilt Projects sit outside the solution.

**Decided**
- No client-facing config file for excluding Projects from the count or the score. The Report has to reproduce identically from a clean clone with no client setup.

**Open**
- @Dana: How the Report decides which Projects a client builds, when Northwind has exactly one .sln but other clients build per-project with no .sln, and some carry more than one. If wrong: a client without Northwind's single-.sln setup gets the same mismatched Projects-scanned count and grade this story exists to fix, or a client's real per-project builds get excluded the way /legacy should have been.
- Unassigned: Whether a Project that sits in the .sln but has never run in CI counts as built for scoring and the Projects scanned count, the way /legacy's out-of-.sln Projects don't. If wrong: a Project the client considers shipped but never CI-tested either counts toward a grade it hasn't earned, or gets excluded the way a real Project shouldn't be.
- Unassigned: Whether Agent Context Findings — the AGENTS.md and README checks — also picked up /legacy's own contradictory READMEs the way Test Posture and Existing Code Readiness did; nobody checked. If wrong: fixing Test Posture and Existing Code Readiness leaves Agent Context still grading Northwind on its attic, and the CTO's complaint recurs in a category this story didn't touch.
