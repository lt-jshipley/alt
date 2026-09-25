Grade only the projects a client ships

Northwind's CTO needs the Agent-Ready Assessment's project count and category grades to describe the code his team ships, not every project folder that happens to sit in the repository — in his own words, "you graded us on code we don't ship." Once this lands, he stops checking the Report against his own solution project by project and starts trusting the number on the cover and the Test Posture and Existing Code Readiness grades beneath it. Delivered to Northwind this morning, the Report read "41 projects discovered, 19 without a test project," the 19 sitting in a legacy folder nobody had built in two years, pulling Test Posture down to a D and Existing Code Readiness with it, though the CTO's own count, from the solution he builds, was 22. The Report instead grades on the 22 projects Northwind ships, and calls out the 19 unshipped ones as a single finding rather than as missing-test rows against projects nobody runs.

**Acceptance criteria**
- The Existing Code Readiness and Test Posture sub-scores are computed from the projects the client actually builds, not from every project folder in the repository.
- Projects outside what the client builds are surfaced as one finding, not as an individual finding per excluded project.
- The project count shown on the Report's cover matches a number the client would recognize as their own, not a raw count of every project folder on disk.

**Examples**
- Northwind's repository has 22 projects referenced by its solution and 19 more sitting in a /legacy folder untouched for two years → the cover reads 22 projects, Test Posture and Existing Code Readiness are scored from those 22, and the 19 in /legacy appear as one finding instead of 19 missing-test rows.
- Some of the 19 legacy projects have their own test projects and some don't → they still roll into the same single finding rather than splitting into "legacy with tests" and "legacy without," and the cover count still reads 22 either way.
- A repository where every project is referenced by the solution, with nothing sitting outside it → no unshipped-projects finding appears at all, and the cover count equals the full project count.

**Decided**
- No client-supplied list of projects to exclude, and no config file for it — the Report has to come out the same way from a clean clone with no per-repo setup, the same rule this tool applies everywhere else.

**Open**
- Dana: which project or projects count as "shipped" when a client repo has no solution file, or has more than one — any referenced project, a fallback walk of the disk when none exists, something else? If wrong: the fix that works for Northwind breaks, or double-counts, for the clients Dana named who build per-project with no solution file, or picks the wrong one when a client has several.
- Unassigned: does a project inside the solution that CI has never built count as shipped, or does it belong with the excluded set? If wrong: a project as stale as /legacy keeps counting toward Test Posture and Existing Code Readiness, or a project the client actively maintains gets wrongly excluded and its missing tests go unreported.
- Unassigned: does Agent Context also need to exclude or separately flag the legacy projects' own README files, which contradict the root one? If wrong: the same double-counting the CTO objected to in Test Posture and Existing Code Readiness resurfaces in Agent Context on the next report.
