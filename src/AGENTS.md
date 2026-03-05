# mev CLI Development Context

See [root AGENTS.md](../AGENTS.md) for project overview.

## app structure

- `cli/` contains clap input contracts only.
- `commands/` contains orchestration units per command domain.
- `context.rs` wires ports to adapters without command logic duplication.
- `api.rs` exposes stable library entrypoints used by `main.rs`.

## domain structure

- `error.rs` contains domain-level typed errors.
- `ports/` defines explicit interfaces consumed by application and domain.

## Development

See `justfile` for available recipes and `tests/AGENTS.md` for test execution.
