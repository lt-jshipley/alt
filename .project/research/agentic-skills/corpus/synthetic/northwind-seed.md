#client-northwind-assessment

[09:12] Priya (consultant, on site)
Delivered the Northwind report this morning. Went fine until the CTO got to
Existing Code Readiness. Report says "41 projects discovered, 19 without a
test project". He stopped me and said "we have 22 projects." He pulled up
the solution and he's right, 22 in the sln. The other 19 are in a folder
called /legacy that nobody has built in two years. They keep it for
reference. His words: "you graded us on code we don't ship."

[09:14] Priya
Same thing dragged Test Posture down. We gave them a D there. If you take
the legacy stuff out it's roughly a B. He was polite about it but the
number on the cover page is what he's going to remember.

[09:20] Marcus (PM)
Do we know how common this is? Is it a Northwind thing or are we going to
hit it at every client with any history?

[09:23] Priya
Third time I've seen a graveyard folder in six engagements. First time it
moved the grade this much though.

[09:31] Dana (tech lead)
Pushing back a little. Nineteen projects of unbuilt code sitting in the
repo IS an agent readiness problem. An agent will find that code, read it,
and think it's real. That's exactly the kind of thing the report should
say. I don't want us quietly excluding it and giving them a B they haven't
earned.

[09:33] Priya
Agree it's a finding. Disagree it's nineteen findings that each cost the
same as a live project with no tests. He'd have accepted "you have 19
dead projects, that will confuse an agent" as one row. He didn't accept
being graded on them.

[09:40] Marcus
So the ask is: the grade reflects what they actually build, and the dead
code shows up as its own thing rather than as a pile of missing tests?

[09:41] Priya
Yes. And the count on the cover should be a number he recognises. 22, not 41.

[09:47] Tom (developer)
Looked at it. Discovery walks the disk for *.csproj and never opens the
.sln. Easy fix, read the sln and only take what's in it. Half a day.

[09:49] Dana
Not that simple. Two of our other clients don't have a sln at all, they
build per project. And some people have multiple slns. Which one wins?

[09:52] Tom
Fair. Could do "in any sln" and fall back to disk walk when there's none.

[09:55] Marcus
Let's not design it in here. What I want to know is what the client sees.

[10:02] Dana
One thing I'll decide now so nobody asks later: we are not adding a config
file where the client lists what to exclude. Same reason as always, the
report has to be reproducible by us from a clone with no setup.

[10:05] Lena (QA)
Question. If we split these out, does a project that IS in the sln but
has never been built in CI count as live? I've seen that too.

[10:06] Dana
Don't know. Park it.

[10:10] Priya
Also, Agent Context category probably got hit too, half the legacy
projects have their own old README that contradicts the root one. Not
sure if the report counted those. Didn't check.

[10:15] Marcus
Ok. Summary for the ticket: grade on what they build, surface the dead
code as one finding not nineteen, cover number matches what the client
would say. Priya can you write it up? Dana owns the sln question. Lena's
CI question stays open.

[10:16] Priya
On it. One more thing the CTO said that stuck: "if your tool can't tell
the difference between our product and our attic, how is an agent going
to?" Might be the actual story.

[10:31] Tom
btw the Northwind run took 9 minutes, most of it in /legacy. Unrelated
but noting it.
