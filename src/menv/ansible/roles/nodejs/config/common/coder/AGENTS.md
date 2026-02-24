# Rules

## Conduct

### Design

- When adding new features or refactoring, removing old modules and deprecated features is mandatory. Identify and eliminate all sources of technical debt, bugs, and complexity.
- Never define class or file names with ambiguous responsibilities, such as base, common, core, utils, or helpers.
- Every file and class name must identify its single, specific responsibility. Names that merely restate a package or directory scope attract unrelated concerns and become "God Classes."
- Never hardcode enumerable values. Generate these dynamically from the authoritative source (catalog, registry, schema) to ensure extensibility and eliminate maintenance burden.
- Silent fallbacks are not recommended. Any fallback should be explicit, opt-in, and surfaced as a failure or a clearly logged, reviewed decision.
- Prioritize UX simplicity over excessive configuration.
- Prefer systemic fixes over patches: state the invariant and owning component first, then fix it at that boundary so all call sites benefit, without adding workaround paths.

### Implementation

- Complete tasks that has been ordered to be performed without interruption or discretionary refusal.
- Do not inventory changes after implementation (unnecessary retrospection using git diff, git status, etc. is prohibited). After implementation, only perform evidential verification (testing, etc.).
- Prioritize validating the appropriate scope; provide minimal evidence unless intent dictates otherwise.

### Documentation

- All development-related documentation must be written in English.
- Keep documentation for LLM (AGENTS.md, CLAUDE.md, etc.) concise for token efficiency. Focus on essential information only.
- Documentation is written in a declarative style describing the current state. Imperative or changelog-style descriptions are avoided.
- Declarative updates preserve existing, correct content and integrate new content where appropriate, without duplication. Avoid ripping and replacing everything.
- Avoid using ** to emphasize something in Markdown. Organize information clearly using hierarchical displays such as headings.

### Communication

- Your answer must be based on the context of the repository, The beginning of a conversation requires research before answering.
- Pursue engineering correctness, do not pander to the author or current state of the repository, and maintain a critical and rational perspective.
- Concerns that depend on unstated assumptions are treated as proposals: add the assumption explicitly and recommend a concrete spec/design that adopts it.
- Recommendations prioritize reducing user decision load. Downstream issues prevented by the recommendation are not exhaustively enumerated unless requested.
- When considering whether something is unnecessary, validate its necessity by its contribution to a purpose, rather than using the excuse that "it's being used elsewhere.".
- Clarifying questions are asked only when uncertainty materially changes the recommendation or implementation.
- If there is a change of direction in the discussion about the plan you created, edit the plan rather than simply reiterating it.
- When reporting completed work or providing routine responses, avoid unnecessary tokens and keep responses concise and clear.

### Safety

- Commands that discard uncommitted changes (for example `git checkout -- <path>`, `git restore`, `git reset`) are only run after explicit user approval.

## User specific

- `.mx/*.md` files are context-file storage. Do not read them unless the user explicitly instructs you to do so.
- While maintaining a critical and rational perspective on design and architecture, you must strictly follow operational instructions embedded in terminal commands. For example, if a user uses `echo` to convey a directive or modifies a test command, execute the intended action rather than the literal command. In these operational contexts, user intent overrides command appearance.
