# Peer review: research notes

Started 2026-09-29. Research behind the roadmap's peer-review skill. The goal is fewer PR review rounds when AI is in the loop, as author or reviewer; going from ten-plus rounds to five would be the win. The seed was a colleague's multi-agent review process, read below, then three research agents surveyed what teams report online, one each on loop reduction in practice, reviewer signal-to-noise, and author-side practice. Their reports are condensed below with sources kept.

## The seed

A colleague's hand-typed process for reviewing a queue of open PRs, shared 2026-09-29. Read as a reviewer's triage tool, not an author's.

- One team of agents per PR; three personas each running `/code-review medium`: Tech Lead (correctness, architecture, tests, conventions), Security Engineer (unsafe code, injection, secrets, untrusted input; say whether a risk is new or pre-existing), Product Owner (check out the branch, run it end to end, prove it meets the linked issue or the PR description with commands, logs, screenshots).
- A showstopper needs 90%+ confidence and a reproduced failure or concrete evidence (file:line, input to wrong result). Verify every finding against the code; drop anything unproven.
- Never comment on, commit to, or push to a PR. Report back only.
- Report per PR: Showstoppers, Requirements Not Met (skip when no ticket), Recommendations (post-merge), Nitpicks, then a one-line verdict: mergeable as-is or needs fixes. Also written to a markdown file.

## First assessment, 2026-09-29

What in the seed earns its keep, ranked. The evidence bar and the verify-then-drop rule are the whole noise filter. The post-merge bucket is an explicit "do not block on this." The new-versus-pre-existing line on security risks prevents the fix-the-whole-codebase round. The Product Owner persona is the novel piece: "works but isn't what was asked" is the most expensive round. Tech Lead and Security mostly restate `/code-review` and `/security-review`. Fan-out, report-only, and the markdown file are scale and hygiene, not loop count.

Gaps, ranked by loop impact.

- Wrong side of the PR. Rounds are author-submits, reviewer-objects, repeat. The same rubric run before the PR opens gives the author the reviewer's answer first. Reviewer-side is the same skill in a different seat.
- No team conventions input. Generic personas will not catch "we don't do it that way here." It should read `.agentic/sources.md` and whatever conventions live there.
- No memory of past reviews. The comments that repeat across PRs are the loop tax.
- Nitpicks collected, not resolved. Author-side, nitpicks should be applied before opening, never listed.
- "Run it end to end" needs tiers. Often there is no environment. Without a ladder (tests as evidence, then a manual run) and a required statement of which tier it reached, the agent will claim it ran it.
- No scope or size check. Nothing says "this should be two PRs" or "the diff does things the description doesn't mention."
- "No ticket, skip requirements." A PR with no ticket is itself a round source. Flag, don't skip.
- Re-review drift. Round two surfaces findings round one didn't. Re-runs should review the delta since the last run.
- Cost. Three medium reviews per PR is fine for a lead clearing a queue and heavy per push for an author.

Stopgap: port the seed verbatim, reviewer-side and convention-blind, so it mostly shifts who finds the same issues. Durable: author-side pre-PR review with conventions and a prior-review corpus as inputs, the evidence bar and buckets as the rubric, and a "questions the reviewer will ask" section in the decisions-skill style.

## What the online survey says, 2026-09-29

Three Sonnet agents, about 35 searches and 25 fetched pages between them. Nobody reports a measured before-and-after drop in rounds-to-merge; the metric people publish is findings per review or the share of comments acted on. The evidence is mechanism-level. Vendor round-count claims (CodeRabbit and Graphite's 60 to 80% fewer rounds) have no methodology and are discounted throughout. Several arXiv PDFs were unreadable via fetch and are marked as snippet-only.

### Raw LLM review is noise; the filter is the product

- SWR-Bench, "Benchmarking and Studying the LLM-based Code Review", https://arxiv.org/html/2509.01494v1. Best unfiltered reviewer precision 16.65%, most under 10%. Running the reviewer several times and keeping only consistent findings raised F1 by up to 43.67%. Prompt refinement cut false positives; reasoning models did better. A benchmark of PRs with known defects, not team adoption.
- AIDev dataset, 19k PRs, https://arxiv.org/html/2604.03196v1. PRs reviewed only by code-review agents merged at 45.2% against 68.4% for human-only review, and were abandoned at 34.9% against 21.6%. Of 13 agents, 92% had average signal ratios below 60%. Correlational, open-source skewed.
- A PR-level regression found AI-assisted review changed iteration counts almost not at all (Poisson coefficients around -0.01) while cycle time rose as volume outran capacity, https://arxiv.org/pdf/2607.01904. Snippet only.
- Student setting, https://arxiv.org/html/2604.23251v1: only about a third of AI-reviewed PRs were followed by another commit.
- Interview study, "Rethinking Code Review Workflows with LLM Assistance", https://arxiv.org/html/2505.16339v1, ten participants: "if they're not good enough, you stop reading them... you miss the real issues." The mechanism behind noise creating rounds, not evidence of it.

### Verify against code, then gate on confidence

- Cloudflare, https://blog.cloudflare.com/ai-code-review/, first-hand engineering post and the best single source. Up to seven specialists (security, performance, code quality, documentation, release, compliance) feed one coordinator that dedupes and re-checks each candidate against the actual code with read tools before posting; they call the coordinator essential. Each specialist prompt carries a "What NOT to Flag" list: speculative or theoretical risks, unchanged code, defense-in-depth when primary defenses are adequate, findings that contradict repo conventions. Stated lesson: telling the model what to ignore beat expanding instructions. Findings tiered critical, warning, suggestion. Lockfiles, vendored, and generated files stripped; review depth tiered by change size (10 lines or fewer, 100 or fewer, full). Numbers: 131k reviews on 48k MRs in 30 days, about 1.2 findings per review, median 3m39s, $1.19 per review, a "break glass" override on 0.6% of MRs. Findings were 47% code quality, 17% documentation, 9% performance, 8% security. No precision or acceptance rate published, no round count before and after, and they say outright this does not replace human review. Summary at https://www.zenml.io/llmops-database/ai-orchestrated-code-review-system-at-scale.
- Atlassian RovoDev, https://arxiv.org/abs/2601.01129, snippet only. LLM-as-judge for factual correctness plus a fine-tuned ModernBERT classifier that keeps only actionable comments. 38.7% of comments led to code changes, median PR cycle time down 30.8%, human-written review comments down 35.6%, across 1,900+ repos over a year. Observational.
- Anthropic's code-review plugin, https://github.com/anthropics/claude-code/blob/main/plugins/code-review/README.md. Four parallel agents: two CLAUDE.md compliance, one bug detector, one git-history analyzer. A separate step scores each issue 0 to 100 and posts only 80 and above. Explicit exclusions: pre-existing issues, things that look like bugs but are not, pedantic nitpicks, anything a linter catches, general quality issues unless CLAUDE.md requires them. Skips draft, closed, trivial, and already-reviewed PRs. No published precision; the 80 cutoff is a design choice, not validated. Self-reported confidence has no calibration data anywhere found; pair it with the verification read.
- Meta RADAR, https://arxiv.org/abs/2605.30208. A funnel: eligibility gates, an ML diff risk score, LLM review, deterministic validation. Median diff review wall time down 35%, fewer reverts and incidents than non-RADAR diffs. This is auto-approval of low-risk diffs, not comment quality.
- photostructure.com/coding/claude-code-review/, practitioner. "Prove it or discard it": trace callers, build a concrete failing scenario, discard style nits, speculative risks, and intentionally suppressed items. Cross-vendor second opinion (Claude plus Codex) for high-stakes code. By default the models report everything that could be a problem with no severity separation. No numbers.
- CodeAnt, https://www.codeant.ai/blogs/ai-code-review-false-positives, vendor opinion: start with a high threshold, tune per category, feed dismissals back. Cites false-positive targets under 3% for bugs and 2% for style with no study behind them.

### Re-review must converge

- GitHub community discussion 189767, https://github.com/orgs/community/discussions/189767, March 2026. Copilot Code Review on one PR produced 10, 6, 4, 2, 2 comments over five rounds, 24 in all, about 3 of them real crash bugs and about 21 style or low-impact, at 15 to 30 minutes a round. The reporter's point: if the tool can find it in round 3 it should have found it in round 1. Full re-scan on every push manufactures rounds.
- Cloudflare (above) reviews each new push incrementally, omits fixed findings and auto-resolves their threads, and reads developer pushback to resolve or answer a finding.
- dev.to/zoetaka38, "When AI reviews AI's code you've built an infinite loop", https://dev.to/zoetaka38/when-ai-reviews-ais-code-youve-built-an-infinite-loop-heres-how-we-stopped-it-4g1n. Learned from real deadlocks: fixes dispatch only at merge, bot-authored PRs skip auto-handoff, a finding is never dispatched twice, findings in one file coalesce into one task, a bot fix is approved if it resolves the original issue even with new minor findings. Some teams saw 4 to 5 rounds before the bot said "all good." No aggregate metrics.
- Greptile on HN, https://news.ycombinator.com/item?id=42451968, vendor but candid. Prompting, LLM-as-judge, and fine-tuning all failed to remove nits. What worked: embed each new comment and drop it if it resembles about three previously downvoted ones. Metric was share of comments addressed. This is the past-review-corpus idea with evidence, as negative examples. Cursor's learned rules (https://cursor.com/guides/ai-code-review) and Rules Miner turn recurring PR comments into enforceable rules; vendor-only evidence. No independent measurement that past-comment context improves precision.
- Open debate: should a re-review verify prior fixes only, or re-scan? The Copilot reporter wants verify-only. Cloudflare is incremental. Tools that re-scan keep producing new findings.

### Show AI output to the author, not the reviewer

- Meta MetaMateCR, https://arxiv.org/abs/2507.13499, snippet only. Showing AI-suggested patches to reviewers made reviews over 5% slower; the regression disappeared when patches were shown only to the author.
- Google, ICSE 2024, https://dl.acm.org/doi/10.1145/3639477.3639746 and https://research.google/pubs/resolving-code-review-comments-with-machine-learning/, snippet. ML-suggested edits applied for about 5% of comments (7.5% in v2) at millions of comments. Added AI output has real cost and modest uptake.
- HN 46348957 and 46766961 and dev.to accounts: roughly 1 in 10 to 20 bot comments useful; people resolve threads without acting and lose real notifications; some teams turned the bot off.

### Author side: verify, self-review, small diffs, honest description

- Anthropic's Claude Code guidance, https://docs.anthropic.com/en/docs/claude-code/tutorials: verification (tests, builds, linters, screenshots) is the single most impactful tip. Secondary summaries add that the answer should include the command run, output summary, and failures not fixed, and write the failing test first.
- GitHub Copilot coding agent docs, https://docs.github.com/copilot/how-tos/agents/copilot-coding-agent/best-practices-for-using-copilot-to-work-on-tasks: iterate on a branch and review the diff before opening; write a meaningful description; use draft PRs to catch easy issues before a human looks; split beyond a few hundred lines.
- OpenAI Codex, https://developers.openai.com/codex/guides/agents-md and /codex/learn/best-practices: put the pre-PR contract in AGENTS.md ("run pytest before finalizing a PR"); treat agent PRs like external-contributor PRs, require passing CI, track regression rate.
- Agent self-review loop, https://agentpatterns.ai/code-review/agent-self-review-loop/: a review pass over `git diff` before PR creation, capped at 2 to 3 iterations, claims about a third less reviewer back-and-forth. Provenance of the figure unverified. dev.to/5uper0 claims 30 minutes per engineer per day on an iOS team. Practitioners say pre-review helps on complex cross-file PRs and is "basically unchanged" for small ones. No controlled evidence.
- Description versus diff. fullsend-ai/fullsend issues #2280 and #4694 propose escalating discrepancies between the description and the diff's file list. CodeRabbit's reviewer guide, https://www.coderabbit.ai/guides/code-explainability-for-ai-generated-prs-a-reviewers-guide, says the question that catches the most AI defects is whether stated intent matches the diff's scope. Runfusion/Fusion #3633 and otto-nation/otto-workbench #1286 record generators pasting template placeholders verbatim. "The Value of Effective PR Description", https://arxiv.org/pdf/2602.14611, studies description quality against discussion rounds; unreadable via fetch, no numbers extracted.
- QEMU AI-policy patch series, https://ratatoskr.run/qemu-devel/2026/05/17060316/t: the contributor confirms each test exercises the intended behavior, and a regression test fails without the change and passes with it. The sharpest "state what you verified" rule found. AI use limited to mechanical changes, bug fixes of 20 lines or less excluding tests, tests, and docs. Ships an AGENTS.md based on GStreamer's.
- Requirements traceability from ticket to PR, and a definition of ready for PRs: nothing substantive found. A gap and possibly an opening.

### Size

- Google, Sadowski et al., ICSE-SEIP 2018, https://dl.acm.org/doi/10.1145/3183519.3183525: over 80% of changes need at most one iteration of resolving comments; median change 24 lines; over 10% are one line; one reviewer usually enough. Strong correlation, not causal, pre-AI, one company. The best number anyone has.
- Microsoft, Bosu et al., MSR 2015, https://www.amiangshu.com/papers/CodeReview-MSR-2015.pdf: across 1.5M comments the share of useful comments falls as file count grows.
- SmartBear/Cisco, second-hand via Graphite and blogs: effectiveness drops past 200 to 400 lines, defect discovery falls about half beyond 400.
- "Do Small Code Changes Merge Faster?", https://arxiv.org/pdf/2203.05045, unreadable via fetch.
- Stacked PRs (https://graphite.com/blog/stacked-prs, dev.to/adioof, swizec.com): testimonials only, same-day review instead of 24 to 48 hours, no round counts.
- markafitzgerald1/cribbage-trainer #831: a 242-line PR with 6 bot rounds and a 458-line PR with 34 threads; argues cost is superlinear because each round re-reads the whole diff. n=2.

### Upstream and around the review

- Audit the harness first. pushtoprod substack, https://pushtoprod.substack.com/p/why-do-my-ai-code-reviews-take-so-many-iterations: of five 12-to-21-round merge units, four were infrastructure (a prompt sanitizer rewriting diffs, unrelated flaky tests, rebases retriggering review, a timeout mismatch between test runner and fix task). One was a real review loop where each round found another missed entry point.
- Review the plan before the code. https://www.ninetwothree.co/blog/shipping-ai-written-code-safely, one developer, 17 PRs: subagents attacked the plan first and caught 12 issues on one feature before any code; reading Figma specs up front "cut about 80% of UI fix iterations", self-reported; lint, types, and Playwright after every edit caught 32 corrections pre-merge; every diff still gets a human review. Augment, https://www.augmentcode.com/blog/review-the-intent-not-the-code, vendor essay, same argument. The counter: this shifts the loop upstream rather than removing it, and nobody has measured the net.
- Ona, https://ona.com/stories/auto-approving-low-risk-prs, vendor's own data: AI reviews every PR, low-risk ones (under 1,000 lines, no migrations, auth, or infra) skip the human. Median time to first approval from 2h49m to 3.8 minutes, lead time down 74%. Addresses wait, not rounds; human merge authority stays.
- Pair planning and pair validation, https://shiftmag.dev/review-fatigue-12276/: two people plan with the agent, then validate together instead of reviewing separately. Qualitative; the author says it does not suit open source, distributed teams, or contractors.
- Multi-persona review specifically: no controlled comparison of personas against a single agent exists. Cloudflare's seven stay quiet because of the coordinator, not the count. All cited systems use technical-domain specialists; a Tech Lead or Product Owner persona has no published evidence. Practitioner repos (calimero-network/ai-code-reviewer, alanchn31/multi-agent-code-review) give style findings a LOW severity that never blocks, with no measured outcomes. CodeAgent https://arxiv.org/pdf/2402.02172 and DeputyDev https://arxiv.org/pdf/2508.09676 claim gains from multiple agents; not read in full.

### What OSS maintainers now require of AI-assisted PRs

A proxy for what human reviewers want. It converges on: the author understands the change, the author verified it, the author disclosed the AI use, the scope is small, and the prose is human-edited.

- Survey of 118 repos with AI policies, https://arxiv.org/html/2605.16706: 51% require disclosure, 74% require a human in the loop, 78% allow AI-assisted work, 22% discourage it. Policies rarely specify verification and use vague thresholds. A second survey, https://arxiv.org/html/2609.07542v1, puts disclosure at 48.8%.
- Ghostty, https://github.com/ghostty-org/ghostty/blob/main/AI_POLICY.md: disclose tool and extent; "the human-in-the-loop must fully understand all code"; AI text in discussions must be human-edited; since January 2026 AI contributions accepted only for already-accepted issues; clear slop earns a public list and a block.
- Linux kernel, https://docs.kernel.org/process/coding-assistants.html: AI never adds Signed-off-by; use `Assisted-by: AGENT:MODEL [tools]` so reviewers can adjust posture.
- curl, https://opensourcesecurity.io/2025/2025-05-curl_vs_ai_with_daniel_stenberg/: disclose and ensure accuracy before submitting. Bug bounty ended January 2026 after AI slop; mid-2025 about 5% of security submissions genuine and about 20% AI-looking. Those figures are security reports, not PRs.
- MicroPython requires disclosure on every PR, https://blog.adafruit.com/2026/02/19/micropython-now-requires-ai-disclosure-on-every-pull-request/. NetBSD declines AI-derived contributions on provenance grounds. Godot, https://godotengine.org/article/contribution-policy-2026/: disclosure, issues-first, proof-of-understanding gates. METR, https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/: many benchmark-passing PRs would not be merged.
- One dissent, valentin-grenier/wp-boilerplate-fse #126: checkbox PR gates get rubber-stamped under AI-driven development.

## What this settles for the skill

- Measure rounds-to-merge on our own repos before building. Nobody online tracks it, and the harness audit says half of ten rounds may not be review at all.
- The skill is a filter, not a reviewer. Verify every candidate against the code, gate on confidence, carry a "what not to flag" list, and cap findings per run. This is the seed's evidence bar, confirmed by the only large-scale sources.
- Convergence rules are mandatory. Re-runs verify prior findings and review the delta only. A finding is never raised twice. Fixed findings close.
- Author-side first, reviewer-side the same skill in another seat. Meta's 5% slowdown when reviewers see AI output is the direct evidence.
- Conventions in, from `.agentic/sources.md`. Past dismissed comments in, as negative examples, when a repo has them.
- Keep the Product Owner persona as a requirements check with evidence tiers and a required statement of which tier was reached. "Run it end to end" has no evidence and is the part most likely to be faked.
- Persona count is not the lever. Narrow scopes with ignore lists, and one coordinator, are.
- Size and description-versus-diff are cheap checks with the strongest correlational backing.
- Spec-first review is the upstream lever, and alt already has it: examine and decisions pointed at a plan.

## Open

- What the rounds-to-merge baseline is on the repos this will run against, and how many of those rounds are harness.
- Where each team's conventions live and whether any repo has a dismissed-comment history to learn from.
- Whether the reviewer seat posts to the PR or reports to the lead only. The seed reports only; Cloudflare posts with auto-resolve.
- Cost per run at the author's cadence.
