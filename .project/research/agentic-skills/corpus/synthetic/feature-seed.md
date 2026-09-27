ARA-88  Epic  Solution-aware discovery

Status: To Do    Created: 2026-09-15    Reporter: Marcus    Target: Q4
Labels: discovery, grading

Description
Discovery should read the solution file so the report only counts real projects.

Child issues
- ARA-89  Read the .sln for project discovery
- ARA-90  Exclude non-solution projects from Test Posture
- ARA-91  Cover page count uses solution projects

Comments

Marcus, 2026-09-15
Filing this after the Northwind readout. Priya has the details, she said it's
the third time we've hit a dead folder in six engagements. Tom thinks it's
half a day.

Priya, 2026-09-16
Adding what the CTO actually said, because the title above isn't what he
asked for. He said "you graded us on code we don't ship" and, at the end,
"if your tool can't tell the difference between our product and our attic,
how is an agent going to?" What he wants is a grade he can put in front of
his board without a footnote. The 22 vs 41 count was the thing he kept
coming back to. Three engagements out of six is from my own notes; I can
pull the list if anyone wants it.

Dana, 2026-09-16
Two things before anyone picks up ARA-89. We are not going to add a
config file where the client lists what to exclude, the report has to come
off a clone with no setup, same reason as always. And I don't want dead
code to just vanish from the report. It's a finding. It should be one row,
not nineteen rows of missing tests.

Marcus, 2026-09-17
Fine with both. I'd guess this saves us a re-cut on maybe a third of
engagements. Leaving the three children as they are for now.

Lena, 2026-09-18
Nobody has answered whether a project that IS in the solution but hasn't
been built in CI for a year counts as live. Northwind has two of those
as well. Parking it here so it doesn't get lost.

Tom, 2026-09-18
ARA-89 is straightforward if we go by the solution. Multiple solutions
is the annoying case. Could take the one at the root, fall back to disk
walk if there isn't one.

Marcus, 2026-09-18
Let's not design it in the ticket. Dana, can you take the multiple
solutions question.
