Grade only the projects a client actually builds

This is Northwind's CTO's need, not the consultant who runs the tool. When he reads the cover and the Existing Code Readiness and Test Posture sections, the project count there should match the number he recognizes as his own — 22, not 41 — so he stops correcting the tool's count before he'll trust anything else in the report. Priya delivered the Northwind report and the CTO stopped her at Existing Code Readiness, where it read "41 projects discovered, 19 without a test project"; he pulled up the solution, said "we have 22 projects," and told her "you graded us on code we don't ship" about the 19 sitting in an unbuilt legacy folder that also dragged Test Posture down to a D from what the thread put at roughly a B without them. Once this lands, the cover count and the Existing Code Readiness and Test Posture sub-scores come from the 22 projects Northwind builds, and the 19 unbuilt legacy projects show up as one finding instead of nineteen missing-test deductions.

**Acceptance criteria**
- The Overall Score and the Existing Code Readiness and Test Posture sub-scores are computed only from the projects a client actively builds, not from every project file discovery finds on disk.
- Any project count the report states to the reader — on the cover, in a category, or in the punch list — is the number of projects the client builds, not the number of project files discovery walked past.
- Projects discovery finds but leaves out of grading appear as one finding, not one per excluded project, so an agent that reads that code is warned it isn't part of what ships.

**Examples**
- Northwind's repo has 22 projects in the solution Northwind builds and 19 more project files under an unbuilt legacy folder, referenced by no solution and not built in two years → the cover states 22 projects, Existing Code Readiness and Test Posture are graded on those 22 instead of 41, and the 19 legacy projects appear as a single finding telling the reader — and any agent reading that code — that it sits outside what Northwind ships.

**Decided**
- Not adding a config file where a client lists which projects to include or exclude from grading — the report has to stay reproducible from a fresh clone with no client-side setup.

**Open**
- Dana: How does the tool tell which projects a client actually builds when there's no single solution file, or when there's more than one? If wrong: a client who builds per project instead of through a solution gets graded on the wrong set, the same complaint in the other direction.
- Dana: Does a project inside the client's own build definition that has never actually run in CI count as built for grading, or does it fold into the excluded-code finding? If wrong: a client is still graded on code nobody has verified builds, or a genuinely active project gets wrongly left out of its own grade.
- Unassigned: Does the Existing Code Readiness / Agent Context reading also need to account for old READMEs living inside excluded projects, the way roughly half of Northwind's legacy projects carry one that contradicts the root README? If wrong: the "graded on code we don't ship" complaint resurfaces in a different category the next time a client notices.
