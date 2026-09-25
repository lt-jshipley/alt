Score what the client ships, not what's sitting unbuilt in the repo

An engineering lead wants the Report to tell his product from his attic — in his words, "if your tool can't tell the difference between our product and our attic, how is an agent going to?" He stopped the delivery when the Report said "41 projects discovered, 19 without a test project" against a solution that holds 22, with the other 19 sitting in a folder nobody has built in two years. Scored as if all 41 counted, Test Posture landed a D where the 22 he ships would land roughly a B — "you graded us on code we don't ship," he said. Once this lands, the cover count is the number he'd give if asked, the category sub-scores come only from what's in scope, and the 19 out-of-scope projects appear once, as a single Punch List finding, not nineteen missing-test findings pulling every category down.

**Acceptance criteria**
- The Report's project count and the Existing Code Readiness and Test Posture sub-scores come only from the projects inside the client's build scope, never from every folder the tool can find on disk.
- Projects outside that scope produce one Punch List Finding, whose Title says how many there are and that they don't count toward the grade — not one Finding for each project in each Category.
- The cover page's project count is the number the client would give if asked, not the count of folders walked.

**Examples**
- 22 projects in the client's solution, 19 more sitting in a legacy folder nobody has built in two years → the Report counts 22 on the cover, computes Test Posture and Existing Code Readiness from those 22 instead of landing on a D, and lists the 19 once, as a single Punch List finding, instead of counting each of their missing test projects as its own finding.

**Decided**
- No config file for the client to list exclusions — the Report has to stay reproducible by the team from a clean clone, with no client-side setup, the same reason every other exclusion in the tool works this way.

**Open**
- Dana: when a client has more than one solution, or builds one project at a time with no solution at all, which projects count toward the grade? If wrong: the tool either double-counts a client's real surface or falls back to walking the whole disk, and this same problem returns for every client without one clean solution.
- Unassigned: does a project inside the client's build scope but never built in CI still count as live for the grade? If wrong: the grade credits work the client has, in practice, abandoned.
- Unassigned: did the legacy folder's own READMEs, which contradict the root one, get counted as Agent Context findings? If wrong: the Agent Context sub-score is carrying the same dead-code problem this story is meant to fix.
