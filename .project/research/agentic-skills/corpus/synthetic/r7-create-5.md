Grade a repository on the Projects it builds, not the ones it keeps

Engineering leads whose repositories get assessed need the Report's Overall Score and Sub-Scores to grade the code they ship, not code they keep around unbuilt. During the Northwind engagement, the CTO stopped a walkthrough at Existing Code Readiness: the Report counted 41 discovered Projects against the 22 in the solution he builds, pulling down both Existing Code Readiness and Test Posture, with Test Posture at a D where excluding the extra 19 would put it near a B. His words: "you graded us on code we don't ship" and "if your tool can't tell the difference between our product and our attic, how is an agent going to?" Once this lands, the Report's Project count and both Sub-Scores match what an engineering lead would call their repository, and the unbuilt Projects appear as a single Finding rather than adding weight across many.

**Acceptance criteria**
- The Overall Score and every Sub-Score are computed only from Projects the Target Repository builds; Projects it keeps but does not build carry no weight in either score.
- The unbuilt Projects are reported as a single Finding, its Title stating how many Projects it covers, rather than one Finding per Project.
- The Report's Project count is the number of Projects the Target Repository builds — the number a client would give if asked how many Projects they have.

**Examples**
- 41 Project files on disk, 22 built by the Target Repository → Existing Code Readiness and Test Posture score the 22; the other 19 appear as one Finding; the Report's Project count reads 22.

**Decided**
- No config file for a client to list exclusions — the Report must stay reproducible from a clone with no setup.
- Unbuilt Projects aren't dropped from the Report — an agent working in the repository would still find and read them, so they stay visible as a Finding, just without weight in either score.

**Open**
- @Dana: which Projects count as built when the Target Repository has no solution file, or has more than one? If wrong: a repository with no solution file is graded on every Project file on disk again, or a real Project silently drops out of a score it should count toward.
- unassigned: does a Project that's in the solution but has never run in CI count as built?
- unassigned: do the legacy Projects' own READMEs, which contradict the root one, currently count against Agent Context? If wrong: Agent Context is scored down for READMEs an engineering lead wouldn't call part of the repository they maintain — the same complaint that hit Existing Code Readiness and Test Posture.
