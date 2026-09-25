Grade only the Projects a team ships, and report the rest as one Finding

A client reading their Agent-Ready Assessment Report needs the cover's project count and every Sub-Score beneath it to reflect only the code the team builds and ships, not the folders they keep for reference. During the Northwind delivery the Report read "41 projects discovered, 19 without a test project," pulling Test Posture down to a D, while the CTO's own solution held 22 Projects — the other 19 sat in an unbuilt /legacy folder nobody had built in two years. He told the consultant, "you graded us on code we don't ship." Once this lands, the cover reads Projects scanned: 22, the Sub-Scores are computed from those 22, and the 19 unbuilt Projects surface as a single Existing Code Readiness Finding instead of nineteen separate deductions.

**Acceptance criteria**
- The Overall Score and every Sub-Score are computed only from Projects the team builds today; a Project outside that set contributes no missing-test or other per-Project deduction.
- The excluded Projects are reported as one Existing Code Readiness Finding naming how many there are and where they live, not as one Finding per excluded Project.
- Projects scanned on the Report's cover matches the count a person at the Target Repository would give if asked how many projects they have.

**Examples**
- 41 projects discovered, 22 of them in the `.sln`, 19 unbuilt in `/legacy` for two years → Projects scanned: 22; Test Posture and Existing Code Readiness scored on those 22; one Finding naming the 19 excluded.
- A Project the team builds today with no test project → still counted, still its own Test Posture Finding. The same Project outside what the team builds today → folded into the single excluded-Projects Finding instead, not scored.

**Decided**
- No per-repository config file for listing what to exclude — the Report has to be reproducible from a clone with no client-side setup, the same reason Checks carry no suppression mechanism.

**Open**
- Dana: When the Target Repository has no `.sln`, or has more than one, what set of Projects counts as what the team ships? If wrong: a repo that builds per-project, or keeps several solutions, gets scored on whichever disk-walk or solution inflated Northwind's count.
- Lena: Does a Project inside the `.sln` that CI has never built still count as shipped, or does it join the excluded set? If wrong: a Project nobody has actually built keeps counting as live, or a Project waiting on its first CI run gets wrongly folded into the excluded Finding.
- Unassigned: Do the Agent Context Findings from the contradicting `/legacy` READMEs need the same exclusion, or did the Northwind report already skip them? If wrong: a client who accepts the corrected Test Posture and Existing Code Readiness grades hits the same complaint under Agent Context.
