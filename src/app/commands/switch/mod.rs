//! `switch` command orchestration — VCS identity switching.

use crate::app::DependencyContainer;
use crate::domain::error::AppError;
use crate::domain::ports::git::GitPort;
use crate::domain::ports::identity_store::IdentityStore;
use crate::domain::ports::jj::JjPort;
use crate::domain::vcs_identity::SwitchIdentity;

/// Execute the `switch` command: change global git/jj identity.
pub fn execute(ctx: &DependencyContainer, identity: SwitchIdentity) -> Result<(), AppError> {
    if !ctx.identity_store.exists() {
        eprintln!("No identity configuration found.");
        eprintln!("Run 'mev identity set' first to configure identities.");
        return Err(AppError::Config("no identity configuration found".to_string()));
    }

    let vcs_identity = ctx
        .identity_store
        .get_identity(identity)?
        .ok_or_else(|| AppError::Config(format!("failed to load {} identity", identity)))?;

    if vcs_identity.name.is_empty() || vcs_identity.email.is_empty() {
        return Err(AppError::Config(format!(
            "{identity} identity is not configured. Run 'mev identity set' to configure."
        )));
    }

    println!("Switching to {} identity...", identity);

    // Git configuration (required)
    ctx.git.set_identity(&vcs_identity.name, &vcs_identity.email)?;

    // Jujutsu configuration (optional — skip if jj not installed)
    if ctx.jj.is_available()
        && let Err(e) = ctx.jj.set_identity(&vcs_identity.name, &vcs_identity.email)
    {
        eprintln!("Warning: jj identity update failed: {e}");
    }

    // Show current configuration via git (primary VCS)
    let (name, email) = ctx.git.get_identity()?;
    println!();
    println!("Switched to {} identity", identity);
    println!("  Name:  {name}");
    println!("  Email: {email}");

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::adapters::ansible::executor::AnsibleAdapter;
    use crate::adapters::fs::std_fs::StdFs;
    use crate::adapters::git::cli::GitCli;
    use crate::adapters::identity_store::local_json::IdentityFileStore;
    use crate::adapters::jj::cli::JjCli;
    use crate::adapters::macos_defaults::cli::MacosDefaultsCli;
    use crate::adapters::version_source::pipx::PipxVersionSource;
    use crate::adapters::vscode::cli::VscodeCli;
    use crate::domain::ports::identity_store::IdentityState;
    use crate::domain::vcs_identity::VcsIdentity;
    use std::path::PathBuf;
    use tempfile::tempdir;

    fn build_test_container() -> (tempfile::TempDir, DependencyContainer) {
        let dir = tempdir().unwrap();
        let identity_path = dir.path().join("identity.json");
        let local_config_root = dir.path().join("config_root");

        let container = DependencyContainer {
            ansible_dir: PathBuf::new(),
            local_config_root: local_config_root.clone(),
            ansible: AnsibleAdapter::empty(local_config_root),
            identity_store: IdentityFileStore::new(identity_path),
            version_source: PipxVersionSource,
            git: GitCli,
            jj: JjCli,
            fs: StdFs,
            macos_defaults: MacosDefaultsCli,
            vscode: VscodeCli,
        };
        (dir, container)
    }

    #[test]
    fn execute_switch_fails_if_no_config() {
        let (_dir, ctx) = build_test_container();

        let result = execute(&ctx, SwitchIdentity::Personal);
        assert!(result.is_err());
        assert_eq!(
            result.unwrap_err().to_string(),
            "configuration error: no identity configuration found"
        );
    }

    #[test]
    fn execute_switch_fails_if_identity_missing_data() {
        let (_dir, ctx) = build_test_container();

        let state = IdentityState {
            personal: VcsIdentity { name: "".to_string(), email: "".to_string() },
            work: VcsIdentity { name: "W".to_string(), email: "w@w.com".to_string() },
        };
        ctx.identity_store.save(&state).unwrap();

        let result = execute(&ctx, SwitchIdentity::Personal);
        assert!(result.is_err());
        assert_eq!(
            result.unwrap_err().to_string(),
            "configuration error: personal identity is not configured. Run 'mev identity set' to configure."
        );
    }
}
