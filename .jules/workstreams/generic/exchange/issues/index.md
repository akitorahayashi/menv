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
| [Architecture Violations](./refacts/architecture-violations.yml) | Consolidate misplaced application logic and enforce clear boundaries. |
| [AnsibleRunner Quality](./refacts/ansible-runner-quality.yml) | Refactor AnsibleRunner to separate I/O from logic and handle exceptions properly. |
| [CI Pipeline Hardening](./refacts/ci-pipeline-hardening.yml) | Harden CI pipeline by pinning dependencies, unifying runner versions, and deduplicating logic. |
| [CLI Consistency](./refacts/cli-consistency.yml) | Resolve terminology mismatches and restructure CLI commands. |
| [Safe Config Serialization](./refacts/config-storage-serialization.yml) | Replace manual TOML string construction with a proper serialization library. |

## Bugs
> Defect reports and fixes in [`bugs/`](./bugs/).

| Issue | Summary |
| :--- | :--- |
| _No open issues_ | - |

## Tests
> Test coverage and infrastructure changes in [`tests/`](./tests/).

| Issue | Summary |
| :--- | :--- |
| [Eliminate Mirror Logic](./tests/test-integrity.yml) | Replace brittle 'Mirror Logic' in role integrity tests with authentic verification methods. |

## Docs
> Documentation updates in [`docs/`](./docs/).

| Issue | Summary |
| :--- | :--- |
| [Fix Documentation Drift](./docs/documentation-drift.yml) | Remove invalid root AGENTS.md and correct README.md statements about symlinks. |

<!--
Instructions for Decider:
1. Populate each section with issues from `feats/`, `refacts/`, `bugs/`, `tests/`, and `docs/` directories.
2. Format as `| [Title](./path/to/issue.yml) | Summary content |`.
3. Keep this index in sync with the file system.
-->
