# Issues Index

This registry tracks active issues in this workstream.
It serves as the central source of truth for the **Decider** to deduplicate observations.

## Feats
> New feature specifications in [`feats/`](./feats/).

| Issue | Summary |
| :--- | :--- |
| _No open issues_ | - |

## Refacts
> Code improvements and technical debt in [`refacts/`](./refacts/).

| Issue | Summary |
| :--- | :--- |
| [PlaybookService Naming Violation](./refacts/playbook-service-naming-violation.yml) | Refactor PlaybookService to adhere to project naming conventions (no suffix, matching filename). |

## Bugs
> Defect reports and fixes in [`bugs/`](./bugs/).

| Issue | Summary |
| :--- | :--- |
| [Documentation and Implementation Drift](./bugs/documentation-and-implementation-drift.yml) | Fix inconsistencies between documentation and implementation regarding CLI commands, architectural rules, and repair broken backup command. |

## Tests
> Test coverage and infrastructure changes in [`tests/`](./tests/).

| Issue | Summary |
| :--- | :--- |
| [Unit Tests Leak to Live Environment](./tests/unit-tests-live-env-leak.yml) | Isolate unit tests from live environment by preventing import of initialized app context. |

## Docs
> Documentation updates in [`docs/`](./docs/).

| Issue | Summary |
| :--- | :--- |
| _No open issues_ | - |

<!--
Instructions for Decider:
1. Populate each section with issues from `feats/`, `refacts/`, `bugs/`, `tests/`, and `docs/` directories.
2. Format as `| [Title](./path/to/issue.yml) | Summary content |`.
3. Keep this index in sync with the file system.
-->
