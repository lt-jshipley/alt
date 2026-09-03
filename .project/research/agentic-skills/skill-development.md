# Skill development: things to consider

Started 2026-09-03. A list of things to weigh when building or changing a skill. None of these are rules. Each one is a question to ask of the situation in front of you, and the honest answer will sometimes be that it does not fit. A consideration that is applied without being asked has become a rule, and that is the failure this doc exists to avoid.

Mechanics are separated from considerations. Mechanics are how Claude Code actually loads, bills, and runs a skill, verified against the official docs and measured where possible. Considerations are judgement, grounded in those mechanics and in the grill-me research.

## Mechanics, verified

Sources: https://code.claude.com/docs/en/skills.md, https://code.claude.com/docs/en/plugins.md, https://code.claude.com/docs/en/plugins-reference.md, https://code.claude.com/docs/en/sub-agents.md, https://code.claude.com/docs/en/hooks.md. Checked 2026-09-03.

- **Two cost tiers.** Every installed skill's name and description load into every session. The body loads only when the skill is invoked. Supporting files load only when the body tells Claude to read them.
- **Measured on era**, using `claude plugin details` with `--plugin-dir`:

| | Tokens, approximate |
|---|---|
| era always-on, 13 descriptions | 2,100 per session |
| examine body on invoke | 2,500 |
| plus format.md, owner-ladder, stances, beliefs, extension file | 7,500 |
| one examine run before its first question | 10,000 |

- **Supporting files are not auto-loaded.** Relative paths and `${CLAUDE_PLUGIN_ROOT}` resolve, but Claude reads a file only when instructed. Lazy by default.
- **Skills may invoke skills.** A body can tell Claude to use another skill. Chaining up to six at the start of a message is documented. No per-skill dependency declaration exists, only plugin-level dependencies in the manifest. Reliability of nested invocation inside an agentic loop is not documented, and Matt Pocock reports it failing in the field.
- **The description routes.** Auto-invocation is driven by the description. `disable-model-invocation` makes a skill user-only.
- **Isolation comes in two shapes.** A subagent starts fresh and returns only its result. A fork inherits the whole conversation. Both add latency and keep verbose work out of the main thread.
- **Hooks are the deterministic layer.** They fire on lifecycle events with no interactivity. A skill can declare hooks in its frontmatter.
- **Testing exists and is gated.** `claude plugin eval` runs cases (a prompt plus graders: regex, tool used, tool order, file exists, LLM judge, baseline) in fresh sessions, with an optional with-versus-without-plugin arm. `/skill-doctor` reports per-skill cost and skills never invoked. Both are early access, enabled per organisation. `claude plugin validate --strict` checks manifests and structure only.
- **Names are load-bearing.** Without a `name` field, invocation is by install directory and changes per version. The marketplace manifest has a `renames` field for deprecation. Installed copies are cached per version and pick up no edit until the version bumps. `--plugin-dir` plus `/reload-plugins` is the development loop.
- **Frontmatter fields** as of the current docs: `name`, `description`, `disable-model-invocation`, `model`, `maxTurns`, `effort`, `tools`, `disallowedTools`, `memory`, `background`, and hooks.

## What the docs do not say

Body length. A rubric for a good description. Nested-invocation behaviour, depth, or circularity. Any explicit token limit. Anyone stating a line count or a rule against layering is extrapolating. What can be measured is cost, invocation frequency, and eval scores with and without the plugin.

## Considerations

Each is a question, why it matters, and when it may not fit.

### Shape

- **Can the description say what this does and when to use it in one sentence?** If not, it may be two skills, and it is also always-on cost every session pays. May not fit: a skill that is genuinely one workflow with several entry conditions, where splitting would only move the length into a router.
- **Is there a second consumer yet?** A primitive plus wrappers earns its loading risk when something else calls the primitive. Before that, one skill. May not fit: when the second consumer is already designed and the split now avoids a rename later.
- **Is judgement in prose and mechanism in scripts or hooks?** Asking the model to count lines or guarantee a write happened puts mechanism in prose. Scripting a decision tree puts judgement in code. May not fit: a small deterministic step where a script would cost more to maintain than the instruction.
- **Does the skill know when not to run?** Zero output is a valid result. A skill run on the wrong input should say so in one line and stop. May not fit: a skill whose input is always in scope by construction.

### Coupling

- **Is shared content a file read by path, or a skill invoked?** Files load reliably. Skill-invokes-skill has no contract. May not fit: behaviour that genuinely must run as its own skill, in which case the body should say what to do if it did not load.
- **Do dependencies point one way?** Skills read concept files. Concept files never name skills. Renaming a skill then costs one folder. May not fit: a concept that is owned and written by exactly one skill, where the pairing is the point.
- **Does every dependency state its absent behaviour?** File missing, MCP unauthenticated, skill not loaded. One line each, or the failure is silent. May not fit: rarely. This is the consideration closest to a rule.
- **Is the same fact written in two places?** The second copy is the one that goes stale. May not fit: an ephemeral file that is deleted when the work ends and can restate freely because it cannot drift.

### Cost

- **What is the always-on budget for the plugin, and is this skill inside it?** Measured with the details command before release. May not fit: a plugin that is the only one installed and whose users have agreed to the cost.
- **What does one invocation load before it does anything?** Sum the body and every file it reads unconditionally. Ten thousand tokens before the first question is a number worth knowing. May not fit: a skill whose value is proportional to how much record it consults.
- **Is progressive disclosure actually conditional?** A reference file read every time is part of the body. It is lazy only if some runs skip it. May not fit: a spec the skill must follow exactly every run, where a separate file is about maintainability rather than cost.

### Contracts and naming

- **Which three surfaces does this skill expose?** The description for routing, the output shape for consumers, and the headings in any extension file for teams. Each rename in any of them propagates. May not fit: a skill with no consumers and no extensions, where only the description is a contract.
- **Are shared files named by concept or by skill?** Concepts rename less often. era paid for explore becoming examine and brief becoming brief-create with a migration each time. May not fit: a file that exists only for one skill and dies with it.
- **Is the path derivable from the name?** A skill should compute where to look from its own name and the concept's name, with no registry. May not fit: when a registry is the concept, as with a compiled ruleset that needs scope globs.

### Evidence

- **What would an eval case for this skill look like?** A prompt, a grader, and a baseline arm. If none can be written, the skill's description is a claim nobody can check. May not fit: while the eval harness is gated for the organisation, in which case the case is still written and run by hand.
- **When did this skill last fire?** Skill-doctor's never-invoked list is the prune signal. May not fit: a skill that is correctly rare, such as a migration or a bootstrap.
- **Does it hold on a weaker model?** Cheaper models collapse long instruction sets. Twenty caps and seven verbs are a spec for the author, not instructions for the model. May not fit: a skill that names the model it needs and refuses to run below it.
- **Is it re-runnable?** Same input, second run, and the output reconciles instead of stacking. May not fit: a skill that is stateless by design and writes nothing.

### The reader

These come from the grill-me research and apply to any skill that puts text in front of a person.

- **Who is running this, and is the skill written for them?** Most skills are written by seniors for themselves. The person at the keyboard is often not the owner of the answers and not the author's peer. May not fit: an internal tool whose only users are its authors.
- **Is the count a symptom?** Many questions, many findings, many open items usually point at one wound underneath. Group by cause before presenting effects. May not fit: a genuinely flat list of independent items, which is rarer than it looks.
- **Does every refusal teach?** When the skill says no or says this is not yours, does it say why, what a senior would do, and what to bring to the conversation. Guards are brittle in this era and teaching is what holds. May not fit: a hook that blocks a destructive operation, where the explanation is short by necessity.
- **Is the right move the cheapest move?** If the correct action costs more effort than the wrong one, the wrong one wins under pressure. May not fit: an action that must remain deliberate, such as a write to a shared record.
- **Does the first line let the reader decide whether to read the rest?** Progressive disclosure applies to output, not only to loading. Fixed shapes, one ask per turn, deltas rather than re-renders. May not fit: output that is consumed by another skill, not a person.
- **Is the skill coaching the model too?** A skill that names a known model tendency and corrects it is doing half its job. Edits on momentum, documents eagerly, offers a menu the record already settles, answers its own questions. May not fit: a skill that runs entirely in a script.

## Sources beyond the docs

- Matt Pocock on skill-invokes-skill loading and on weaker models collapsing interviews: https://github.com/mattpocock/skills/blob/main/docs/productivity/grilling.md
- The grill-me research in this folder, for the reader considerations and the fact-versus-decision boundary.
