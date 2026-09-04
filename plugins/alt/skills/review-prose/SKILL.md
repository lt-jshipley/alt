---
name: review-prose
description: Reviews a skill, prompt, or doc for verbosity so every sentence earns its keep, and reports what could go without losing value. Changes nothing. Use when the user says "review prose" or invokes /alt:review-prose.
argument-hint: [file or pasted text] [target size]
---

# review-prose

Every sentence and word must earn its keep. Find the ones that do not, say why, estimate what cutting them saves, and change nothing. Value and understandability are not traded for size; when a cut would cost either, it is listed as a trade for the user to call, never made quietly.

## Inputs

$ARGUMENTS names a file or carries the text, and may name a target size. Without a target, report what the text would weigh with only the verbosity removed.

## Measure first

Total bytes, bytes per section, and bytes inside fenced blocks. If the text is a skill, note that its description is loaded into every session, so those bytes cost more than any other line.

## Read line by line, sorting each finding into one of these

- **Said twice.** The same rule in two places. Name both and which home to keep.
- **A sentence explaining the sentence before it.** A gloss, a restatement, or narrative that follows a rule already stated.
- **Documentation, not instruction.** Prose describing what a template, example, or file the reader will see already shows.
- **Structural.** A section whose lines are mostly duplicates of others, two lists that could be one, a heading longer than its section needs.
- **Genuine trades.** Real value, low frequency. Listed with the value it carries and its size. Never recommended, only offered.

Quote the words in question. Do not paraphrase what you would cut.

## Report

One summary: total now, roughly how much is verbosity, where the estimate lands against the target, and whether reaching it needs trades. Then the findings under those five headings, then a table of bytes per section now and estimated after the non-trade cuts. End by asking which trades, if any. Do not edit the text.
