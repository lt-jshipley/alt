Grade .NET repos on the projects they ship, not the ones sitting on disk

The Northwind CTO needs the report's overall score and project count to reflect the code his team ships, not, in his own words, "code we don't ship," so the number he defends to his board is one he already recognizes — 22 projects, not 41. In #client-northwind-assessment, the consultant delivering that report said the tool found "41 projects discovered, 19 without a test project," and the CTO stopped her — "we have 22 projects," pointing to a /legacy folder nobody has built in two years — before telling her "you graded us on code we don't ship." The same 19 also pulled the Test Posture sub-score down to a D; without them the team estimated a B. The report instead scores and counts every category only against the projects the repo builds, and lists everything outside that as one finding rather than one deduction per project per check.

**Acceptance criteria**
- The overall score and every category's sub-score are computed only from the projects the target repo builds; a project outside that scope neither earns nor costs a category any points.
- Projects outside that scope still appear in the report, but as one finding on the punch list, not a separate deduction per project per check.
- The project count the report shows is the count of projects in scope, not everything found walking the repo.

**Examples**
- 22 projects in the Northwind solution, 19 more sitting in an unbuilt /legacy folder nobody has touched in two years → the cover shows 22, and the overall score and Test Posture sub-score are computed from those 22 alone.
- Those same 19 /legacy projects → one finding on the punch list naming the excluded folder as a risk for an agent to misread as live code, not nineteen missing-test deductions stacked against Test Posture.

**Decided**
- No config file for listing what to exclude — the report has to stay reproducible from a clone with no setup, the same reason it carries no suppression mechanism today.
- Excluded projects stay in the report as a finding rather than dropping out of it entirely — hidden dead code is still there for an agent to read, so silently excluding it would leave the exact blind spot the report exists to catch.

**Open**
- Dana: how does the report decide which projects a repo ships when there's no solution file, or more than one? If wrong: a client without a single .sln either keeps losing points to projects it doesn't build, or a too-broad fallback quietly brings back the whole-disk count this story exists to fix.
- unassigned: does a project inside the solution but never built in CI count as shipped for scoring? If wrong: a project that's nominally in scope but functionally as dead as /legacy either keeps costing points it shouldn't, or the fix over-trusts anything merely listed in a solution.
- unassigned: does Agent Context's scoring today count each legacy project's own README against the sub-score? If wrong: Agent Context stays dragged down by the same dead code this story removes from every other category.
