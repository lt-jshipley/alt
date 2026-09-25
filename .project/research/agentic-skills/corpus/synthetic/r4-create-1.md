# Grade and count only the Projects a Target Repository builds

Northwind's CTO needs the Report's grade and Project count to reflect the 22 Projects his team ships, not the 19 more that sit in an unbuilt `/legacy` folder — "if your tool can't tell the difference between our product and our attic, how is an agent going to?" Once this lands, the cover states a number he recognizes, 22 instead of 41, and Test Posture no longer drops from roughly a B to a D because of Projects nobody has built in two years. At delivery, the Report read "41 projects discovered, 19 without a test project," and he stopped the consultant cold: "we have 22 projects." Discovery walks the disk for every `*.csproj` it finds and never opens the `.sln`, so today it answers with everything sitting on disk rather than what the Target Repository actually builds.

**Acceptance criteria**
- The Test Posture and Existing Code Readiness Sub-Scores are computed only from Projects the Target Repository actually builds, never from Projects sitting unbuilt for historical reference.
- Projects excluded because they aren't part of what's built appear in the Report as one Finding naming the group and its size, not as one Finding per excluded Project.
- The Report's stated Project count is the number the Target Repository builds, so it's the number the client would give if asked, not everything found on disk.

**Examples**
- Northwind: 22 Projects in the `.sln`, 19 more `*.csproj` files under `/legacy` untouched for two years → Report states "22 Projects"; Test Posture and Existing Code Readiness score against the 22; the 19 appear as one Finding, not nineteen.
- A `/legacy` Project that still has a passing test project → folded into the same one Finding as the rest of `/legacy` and still excluded from scoring; having tests doesn't put it back in what's built.
- A Target Repository with nothing sitting outside what it builds → Project count and Sub-Scores are unchanged from today, and no exclusion Finding appears.

**Decided**
- No config file for a client to mark Projects excluded — same reproducibility rule as always: the Report has to run the same way from a clean clone with no setup.
- The criteria say "what the Target Repository builds," not "what's listed in the `.sln`" — reading the `.sln` was the alternative on the table, but which signal decides "built" when a repo has none or several is still contested, so that stays an Open line rather than a rule here.
- The cover Project count is kept as its own criterion, separate from the Sub-Score criterion, because the visible number itself is what the client would judge the fix by.

**Open**
- @Dana: When a Target Repository has no single `.sln` — none at all, or more than one — what decides which Projects count as built? If wrong: clients who don't build by solution keep getting graded on code they don't ship, or lose Projects they do.
- Unassigned: Does a Project that's in the `.sln` but has never been built in CI count as built, or does it need the CI signal too? Lena raised it; nobody answered. If wrong: a Project that looks live in the solution but never actually runs stays counted, reproducing the same complaint in a quieter form.
- Unassigned: Does today's Agent Context Category already score the `/legacy` folder's contradicting READMEs? Priya flagged it and didn't check. If wrong: the same over-counting this story fixes for Test Posture and Existing Code Readiness keeps happening in Agent Context.
