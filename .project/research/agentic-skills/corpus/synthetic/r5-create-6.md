Grade what the client builds, not the code sitting unbuilt beside it

An engineering leader reading the Report needs the Overall Score, and the Test Posture and Existing Code Readiness Sub-Scores under it, to count only the code the team actually ships — as the Northwind CTO put it, "you graded us on code we don't ship." On the Northwind engagement the Report read "41 projects discovered, 19 without a test project" and scored Test Posture a D, but the client's own solution holds 22 projects; the other 19 sit in a folder nobody has built in two years, kept only for reference. Once this lands, the Report's project count matches the 22 the client recognizes, the unbuilt 19 appear as one Existing Code Readiness Finding naming what they are and why they don't count, and Test Posture scores against the 22 built projects alone — close to the B the client's own count would earn instead of the D the 41-project count produced.

**Acceptance criteria**
- The Overall Score, and the Test Posture and Existing Code Readiness Sub-Scores under it, are computed only from the projects the client builds; a project outside that set costs neither Sub-Score any points.
- The projects outside what the client builds are called out as one Existing Code Readiness Finding — naming how many there are and that they sit outside the client's build — not as one Finding per excluded project.
- Wherever the Report states a project count, including the cover, that count is the number of projects the client builds, not the total the tool found on disk.

**Examples**
- 41 projects on disk, 19 sitting in a folder untouched by any build in two years, 22 in the client's solution → the Report counts 22, scores Test Posture and Existing Code Readiness against those 22, and lists the 19 as one Existing Code Readiness Finding, not nineteen missing-test Findings.
- Every discovered project is one the client builds, nothing sits outside that set → the project count is the same either way and no exclusion Finding appears; the behavior only engages when discovery finds more than the client ships.

**Decided**
- Not adding a config file or list for the client to name what to exclude — the Report has to stay reproducible by the firm from a clean clone with no client-side setup, the same reason every other knob in the tool lives in source.

**Open**
- @Dana: how the Report decides what a client "builds" when there's more than one solution file, or none at all — some clients have no solution file and build per project. If wrong: a future client without Northwind's single clean solution either keeps losing points to unbuilt code or loses credit for projects it actually ships.
- Unassigned: whether a project inside the client's solution but never run in CI counts as built, or is excluded like the unbuilt folder. If wrong: a project the client considers live loses Test Posture credit it should keep, or a project nobody runs keeps costing points it shouldn't.
- Unassigned: whether the Agent Context Sub-Score is also being pulled down by old READMEs that live only inside excluded, unbuilt folders. If wrong: Agent Context earns the same "graded on our attic" complaint Test Posture and Existing Code Readiness just did, at the next client.
