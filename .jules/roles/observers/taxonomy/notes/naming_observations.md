# Naming Observations

## 2026-01-31

### Compliant Patterns
- **Service/Protocol Naming:** `src/menv/services` and `src/menv/protocols` follow the `Xxx` vs `XxxProtocol` convention perfectly.
- **Model Structure:** `src/menv/models` follows "1 file per domain" convention.
- **Ansible Role Configs:** `rust` role configs (`tools.yml`, `platforms.yml`) match `AGENTS.md` specs.
- **Config Command:** `config` command uses consistent verb-noun function naming (`create_config`, `set_config`, `show_config`).

### Violations
- **CLI Structure:** `list` command is misplaced in `make.py` and documentation is misleading. (Event: `c8m2x9`)
- **Test Filenames:** `test_config.py` and `test_tools.py` are duplicated across role directories. (Event: `f4j1p7`)
