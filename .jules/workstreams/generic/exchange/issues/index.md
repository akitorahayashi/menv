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
| [AnsibleRunner Service Refactor](./refacts/ansible-runner-refactor.yml) | The AnsibleRunner service mixes I/O with business logic, lacks unit tests, and uses terminology ('run') that diverges from the CLI ('make'). It needs refactoring for better testability and consistency. |
| [CLI Logic Leaks](./refacts/cli-logic-leaks.yml) | Business logic (`_deploy_configs_for_roles`) and command implementations (`list_tags`) are leaking into the CLI layer (`make.py`), violating separation of concerns. |
| [Config System Architecture](./refacts/config-system-architecture.yml) | The configuration system suffers from hardcoded paths, duplicated logic, and overloaded terminology ('config' for identity vs roles, 'create' vs 'deploy'). It needs architectural consolidation. |
| [CI Reproducibility](./refacts/ci-reproducibility.yml) | The CI pipeline uses floating tags and unpinned dependencies, creating risks for reproducibility and supply chain security. |
| [Manual TOML Serialization](./refacts/manual-toml-serialization.yml) | `ConfigStorage` manually serializes TOML, which is fragile. It should use a proper library. |
| [Test Mirror Logic](./refacts/test-mirror-logic.yml) | Integration tests re-implement Ansible logic (Jinja2, path resolution) to verify configuration, creating a "Mirror Logic" risk where tests verify the re-implementation rather than the actual behavior. |

## Bugs
> Defect reports and fixes in [`bugs/`](./bugs/).

| Issue | Summary |
| :--- | :--- |
| [Ambiguous Terminology](./bugs/ambiguous-terminology.yml) | Inconsistent terminology usage causes confusion and naming collisions. Specifically, 'apple' vs 'macos' in shell aliases, and 'system' being overloaded for both Ansible roles and alias categories. |
| [Broken Backup Command](./bugs/broken-backup-command.yml) | The `menv backup` command fails because the wrapper script does not pass the required `config_dir` argument to the underlying backend scripts. |
| [Unhandled Service Exceptions](./bugs/unhandled-service-exceptions.yml) | Core services (`ConfigDeployer`, `VersionChecker`) swallow exceptions or fail to handle `OSError`, leading to potential crashes or silent failures. |
| [Unvalidated Config Model](./bugs/unvalidated-config-model.yml) | `MenvConfig` is a `TypedDict` without runtime validation, allowing invalid configuration states to propagate. |

## Tests
> Test coverage and infrastructure changes in [`tests/`](./tests/).

| Issue | Summary |
| :--- | :--- |
| [Test Infrastructure Gaps](./tests/test-infrastructure-gaps.yml) | The project lacks coverage reporting infrastructure and the `justfile` silently suppresses errors in verification steps, leading to blind spots in quality assurance. |

## Docs
> Documentation updates in [`docs/`](./docs/).

| Issue | Summary |
| :--- | :--- |
| [Incorrect List Command Documentation](./docs/incorrect-list-docs.yml) | The documentation for `list_tags` incorrectly references `menv make list` instead of the actual `menv list` command. |
| [Phantom Introduce Command](./docs/phantom-introduce-command.yml) | README references a non-existent `menv introduce` command. |

<!--
Instructions for Decider:
1. Populate each section with issues from `feats/`, `refacts/`, `bugs/`, `tests/`, and `docs/` directories.
2. Format as `| [Title](./path/to/issue.yml) | Summary content |`.
3. Keep this index in sync with the file system.
-->
