# Synthetic corpus: the Northwind rounds

Every draft story-create wrote from the Northwind transcript while the skill was being hardened, 2026-09-25. All synthetic; nothing here is client data. `northwind-seed.md` is the seed. Filenames are `r<round>-create-<run>.md`; `r6-composite.md` is one Sonnet composer's merge of the three r6 drafts. Every run was Sonnet 5 for the writer and, from r6 on, for the nested reviewer.

| Round | alt version | Runs | What changed before it |
|---|---|---|---|
| r4 | 0.14.4 | 5 | Before-showing step with check.py and five questions |
| r5 | 0.14.5 | 10 | Fill count sentence deleted, Examples generator deleted, opener and Decided brackets rewritten, before-state routing rule |
| r6 | 0.15.0 | 3 | story-review as a fresh sub-agent; the five questions moved into it |
| r7 | 0.15.2 | 5 | Reviewer keeps product words, drops reasons the seed lacks, carries a fix across claims, possessive is not assignment |

## Rule scores, r4 and r5 (eleven categories, 1 to 5, whole score)

r4 whole: 3, 4, 4, 4, 4. r5 whole: 4, 3, 4, 4, 4, 4, 5, 4, 4, 5. Category detail is in story-concept-restart.md's rule list; the tables themselves were session output and are summarised in story.md's Decided entries.

## Value scores (four columns, 1 to 5, graded by the session that ran them)

r5, sorted by sum: R10 19, R8 18, R6 17, R7 17, R5 16, R1 15, R9 15, R3 14, R4 14, R2 10.

| r6 | Value | Workable | Impl. kept out | Template | Sum |
|---|---|---|---|---|---|
| R1 | 4 | 4 | 4 | 5 | 17 |
| R3 | 5 | 4 | 3 | 4 | 16 |
| R2 | 4 | 4 | 4 | 3 | 15 |
| composite | 5 | 4 | 4 | 5 | 18 |

| r7 | Value | Workable | Impl. kept out | Template | Sum |
|---|---|---|---|---|---|
| R1 | 4 | 4 | 5 | 5 | 18 |
| R2 | 4 | 5 | 4 | 5 | 18 |
| R4 | 5 | 4 | 5 | 4 | 18 |
| R5 | 4 | 4 | 4 | 4 | 16 |
| R3 | 3 | 3 | 4 | 4 | 14 |

A second, fresh session graded its own five runs of 0.15.2 at 17, 17, 17, 15, 14, one to two points below the first grader on the same version. Treat any single grader's numbers as ±1.

## What this is for

The stand-in corpus for the finder shadow test in lt-mcp-backlog until client use supplies real entries. Real entries go in `../` under their own date and slug, anonymised, in the five-heading form the restart doc describes. Do not add synthetic drafts here after r7; the Northwind seed is mined out.
