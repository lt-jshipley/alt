# Context Window Size: What Anthropic Has Actually Said

*Compiled 2026-08-26 from official docs, on-the-record statements, and source-traced
community claims. Purpose: separate real guidance from folklore on "how full should
you let a Claude Code context window get."*

## Bottom line

**No official percentage threshold exists.** Anthropic's published guidance is
deliberately behavioral, not numeric. The numbers people cite ("keep it under 15%,"
"under 40%," "150K tokens") are either misreadings, misattributions, or
window-size-dependent figures quoted without their denominator. The best-attributed
degradation signal is **~300-400K tokens on 1M-window models** (Thariq Shihipar,
Anthropic) — and the strongest official theme is that *what* accumulates matters
more than *how much*: messy narrative history rots; clean reference material holds.

## Official documented numbers

| Source | Number | What it actually means |
|---|---|---|
| [Claude Code best-practices docs](https://code.claude.com/docs/en/best-practices) | none | "Performance degrades as it fills" — behavioral advice only: clear between unrelated tasks; clear after correcting Claude twice on the same issue |
| [Model-config docs](https://code.claude.com/docs/en/model-config#context-window-and-auto-compaction) | ~967K / 1M (~96.7%) | Default auto-compact point on Sonnet 5's 1M window — the harness encodes no conservatism |
| Same page | "at the context limit" | Default auto-compact for standard 200K sessions |
| [Docs' interactive context widget](https://code.claude.com/docs/en/context-window) | amber >50%, "compact now" >75% | Color bands in illustration code — suggestive, never stated as prose policy |
| [env-vars docs](https://code.claude.com/docs/en/env-vars) | `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`, `CLAUDE_CODE_AUTO_COMPACT_WINDOW` | You can lower the compact trigger; the docs never state a recommended value |

## Attributed, on-the-record statements

- **Boris Cherny** (creator of Claude Code) — auto-compact buffer, Oct 11 2025:
  *"We always auto-compacted near 155k tokens so there's enough buffer."* (~77.5% of
  200K; a mechanism ceiling, not advice)
  → https://x.com/bcherny/status/1977163445205450783
- **Boris Cherny** — Hacker News, ~Apr 13 2026: team was *"investigating defaulting
  to 400k context instead of 1M, with an option for users to configure up to 1M."*
  Note: 400K of 1M = 40% — the likely origin of "keep it under 40%" folklore.
  → https://news.ycombinator.com/item?id=47740541
- **Boris Cherny** — plan mode clears context on plan acceptance: *"your plan gets a
  fresh context window. We found this helps keep Claude on track longer, and
  significantly improves plan adherence."* (Vendor confirmation that fresh context +
  durable artifact beats inherited history.)
  → https://x.com/bcherny/status/2012663636465254662
- **Boris Cherny** — personal usage: *"I've been using exclusively 1M context for the
  last few months and loving it."* Tunes `CLAUDE_CODE_AUTO_COMPACT_WINDOW`; no
  self-imposed percentage discipline.
  → https://x.com/bcherny/status/2032514809418109438
- **Boris Cherny** — session staleness (HN, Apr 2026): idle >1 hour = full prompt-cache
  miss on resume; Claude Code now elides old thinking from stale sessions. Staleness
  has real costs independent of size.
  → https://news.ycombinator.com/item?id=47880089
- **Thariq Shihipar** (Anthropic, Claude Code team) — the real rot number: context rot
  kicks in around **300-400K tokens on the 1M model**; recommends
  `CLAUDE_CODE_AUTO_COMPACT_WINDOW=400000`. Widely misattributed to Boris by
  aggregator sites (e.g. howborisusesclaudecode.com).
  → https://x.com/trq212/status/2044653085415604473
- **Jon Bell** (Anthropic CPO) — 1M-context GA post, Mar 2026: *"We've seen a 15%
  decrease in compaction events."* A stat about compaction frequency dropping —
  almost certainly the garbled origin of "keep context under 15%."
  → https://claude.com/blog/1m-context-ga
- **Anthropic Applied AI team** — ["Effective context engineering for AI agents"](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents),
  Sept 2025: names "context rot," frames attention as a finite budget, goal is "the
  smallest possible set of high-signal tokens." No number given — deliberately.

## Folklore ledger (traced and busted)

| Claim | Verdict |
|---|---|
| "Keep it under 15%" | Garbled from Jon Bell's "15% decrease in compaction events" — about frequency, not a ceiling |
| "Keep it under 40%" | No Anthropic source as stated; likely retold from the proposed 400K-of-1M *default window size* |
| "Boris says rot starts at 300-400K" | Real number, wrong person — it's Thariq Shihipar (@trq212), not Boris Cherny |
| "Compact at 60%" / "act at 50K free" / "40% = attention weakens" | Third-party bloggers, unsourced, mutually contradictory |
| "~83% is the real internal compact cap" | Community reverse-engineering; directionally consistent with Boris's 155K/200K but never published by Anthropic |

## The "150K tokens" question

150K is neither official nor wrong — it's a 200K-window number quoted without its
denominator. On a 200K model, 150K is essentially the auto-compact point (Boris's
155K), so treating it as "you're at the ceiling" is fair. On a 1M model, the
best-attributed signal says degradation starts around 300-400K — 150K there is very
conservative. Any token threshold should be **window-aware**; a universal 150K rule
conflates the two worlds.

## Practical takeaways

1. **What accumulates matters more than how much.** Failed attempts, contradicted
   plans, and stale tool output rot; large clean reference material mostly doesn't.
   The docs' own restart heuristic is behavioral: corrected Claude twice on the same
   thing → clear.
2. **Percent is the wrong unit on 1M models.** "9% used" of 1M is ~90K real tokens —
   nearly half of what a 200K session could ever hold. Track tokens, not percent.
3. **Restart at artifact boundaries.** Anthropic now hard-codes this belief: plan
   acceptance wipes context because a fresh window reading a durable plan measurably
   outperforms inherited history.
4. **Staleness is its own cost.** Sessions idle >1 hour resume as full cache misses
   and get their old thinking elided — resuming a stale session is quietly a
   degraded fork.
5. If forced to name numbers: **~400K on 1M models** (Thariq, attributed) and
   **~150K on 200K models** (the compact buffer) are the only defensible ones — and
   both are ceilings, not operating targets.
