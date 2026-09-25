Grade the Target Repository on the Projects it builds, not its unbuilt legacy code

Northwind's CTO, and every client who reads the Report's cover page, needs its grades to reflect the Projects they actually ship, so a grade doesn't get dragged down by code nobody builds. Delivering the Northwind report, the CTO stopped on Existing Code Readiness: the Report said "41 projects discovered, 19 without a test project," and he replied, "we have 22 projects" — the other 19 sat in a `/legacy` folder nobody had built in two years. Test Posture landed a D; with the 19 unbuilt legacy Projects out, that reads as "roughly a B" — a grade the CTO summed up as, "you graded us on code we don't ship." Once this lands, the Report's Project count and its Test Posture and Existing Code Readiness Sub-Scores are computed from the 22 Projects Northwind builds, and the 19 unbuilt legacy Projects surface as one Finding instead of nineteen.

**Acceptance criteria**
- The Report's Project count and the Test Posture and Existing Code Readiness figures it feeds are computed only from Projects the client would recognize as theirs — never from Projects in code nobody builds.
- Projects excluded as unbuilt appear in the Punch List as a single Finding, not as one Finding per excluded Project.

**Examples**
- 41 Projects discovered on disk, 22 in Northwind's `.sln` and built, 19 sitting in an unbuilt `/legacy` folder with no test project → the Report shows a Project count of 22, Test Posture and Existing Code Readiness Sub-Scores computed against those 22 — Test Posture moving from the D scored against all 41 to "roughly a B" — and the 19 legacy Projects listed as one Finding in the Punch List.

**Decided**
- No config file for the client to list what to exclude — the Report has to be reproducible by us from a clone, with no setup, same reason as every other exclusion mechanism we've turned down.

**Open**
- Dana: For a Target Repository with no `.sln` (or more than one), which Projects count as built for grading? If wrong: those clients get graded against the wrong Project set — either unbuilt code drags the grade down again, or real Projects go missing from the Report.
- Unassigned (Lena raised it, Dana parked it): Does a Project that's in the `.sln` but has never been built in CI count as built for grading, or does it belong with the unbuilt legacy Projects? If wrong: a Project that's dead in practice keeps dragging the client's Sub-Score down, or gets folded into the legacy Finding despite being in the solution.
- Unassigned: Do the legacy Projects' own READMEs — which contradict the root one — get counted in Agent Context Findings? Priya flagged this but didn't check. If wrong: the client's Agent Context Sub-Score is being dragged down by the same unbuilt legacy code this story removes from Test Posture and Existing Code Readiness, uncorrected.
