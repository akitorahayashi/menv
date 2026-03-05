1. **Rename Domain Models & Move files**:
   - `src/domain/ports/config_store.rs` -> `src/domain/ports/identity_store.rs`. Rename `ConfigStore` trait to `IdentityStore`. Rename `MevConfig` struct to `IdentityState`.
   - Update `src/domain/ports/mod.rs` to expose `identity_store`.

2. **Refactor Adapters & Move files**:
   - `src/adapters/config_store` directory -> `src/adapters/identity_store`. Rename `local_json.rs` and `paths.rs` if necessary but their names are fine, except `src/adapters/identity_store/paths.rs` needs to point to `identity.json` instead of `config.json`.
   - Update `src/adapters/mod.rs` to expose `identity_store`.
   - Update `src/adapters/identity_store/local_json.rs` to implement `IdentityStore` using `IdentityState`.
   - In `src/adapters/identity_store/paths.rs`, change `default_config_path` to `default_identity_path`, returning `config_base()?.join("mev").join("identity.json")`. Keep `local_config_root` as it's needed for ansible.

3. **Split CLI Commands**:
   - Create `src/app/cli/identity.rs`. Move `Show` and `Set` subcommands to `IdentityCommand` from `ConfigCommand`.
   - Update `src/app/cli/config.rs`. Only retain `Create` subcommand.
   - Update `src/app/cli/mod.rs` to include `identity` module and add `Identity` variant to `Commands` enum with alias `id` maybe? Actually let's just use `Identity` with alias `id`.

4. **Split Command Handlers**:
   - Create `src/app/commands/identity/mod.rs`. Move `show` and `set` functions from `src/app/commands/config/mod.rs` to this file.
   - Update `src/app/commands/config/mod.rs`. Only retain the `create` function.
   - Update `src/app/commands/mod.rs` to include `identity`.

5. **Update AppContext**:
   - In `src/app/context.rs`, change `config_store: ConfigFileStore` to `identity_store: IdentityFileStore` (rename `ConfigFileStore` to `IdentityFileStore` in adapter).
   - Change `for_config` to `for_identity` or `for_lightweight` - actually we still need `AppContext` for both. Let's create `for_identity()` method that works like `for_config()` but initializes `identity_store`. Wait, `AppContext` has both `ansible` and `identity_store`. Let's just update `AppContext::new` and `AppContext::for_config` (rename to `for_identity`? The comment says "config-only context (no ansible asset resolution needed)" so `for_local` or keep `for_config` or rename to `for_identity`). I will rename it to `for_identity` because the only consumers of the lightweight context are identity operations (show, set) and switch.

6. **Update Consumers and Tests**:
   - `src/app/api.rs`: Update to use `IdentityState` instead of `MevConfig`.
   - `src/app/commands/switch/mod.rs`: Update to use `IdentityStore` and `identity_store` field in context.
   - Ensure imports are updated everywhere.

7. **Review references**:
   - `rg ConfigStore`, `rg MevConfig`, `rg config_store` to ensure no leftovers.

8. Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.
9. Submit the change to branch `jules-implementer-refacts-split-config`.
