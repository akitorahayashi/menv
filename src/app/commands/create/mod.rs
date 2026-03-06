//! `create` command orchestration — full environment setup.

use crate::app::DependencyContainer;
use crate::app::commands::deploy_configs;
use crate::domain::error::AppError;
use crate::domain::execution_plan::ExecutionPlan;
use crate::domain::ports::ansible::AnsiblePort;
use crate::domain::profile::Profile;
use crate::domain::tag::FULL_SETUP_TAGS;

/// Execute the `create` command: deploy configs and run full setup tags.
pub fn execute(
    ctx: &DependencyContainer,
    profile: Profile,
    overwrite: bool,
    verbose: bool,
) -> Result<(), AppError> {
    // Validate all tags exist in catalog
    let all_catalog_tags: std::collections::HashSet<String> =
        ctx.ansible.all_tags().into_iter().collect();
    let invalid: Vec<&&str> =
        FULL_SETUP_TAGS.iter().filter(|t| !all_catalog_tags.contains(**t)).collect();
    if !invalid.is_empty() {
        let names: Vec<String> = invalid.iter().map(|t| (**t).to_string()).collect();
        return Err(AppError::InvalidTag(format!("invalid tags in setup: {}", names.join(", "))));
    }

    let plan = ExecutionPlan::full_setup(profile, verbose);

    println!();
    println!("mev: Creating {} environment", plan.profile);
    println!("This will run {} tasks.", plan.tags.len());
    println!();

    // Deploy configs for roles about to be executed
    deploy_configs::deploy_for_tags(
        &plan.tags,
        &ctx.ansible_dir,
        &ctx.local_config_root,
        &ctx.ansible,
        overwrite,
    )?;

    // Execute each tag
    for (i, tag) in plan.tags.iter().enumerate() {
        let step = i + 1;
        let total = plan.tags.len();
        println!("[{step}/{total}] Running: {tag}");

        ctx.ansible
            .run_playbook(plan.profile.as_str(), std::slice::from_ref(tag), plan.verbose)
            .inspect_err(|e| {
                eprintln!("Failed at step {step}/{total}: {tag}: {e}");
            })?;
        println!("  ✓ Completed");
    }

    println!();
    println!("✓ Environment created successfully!");
    println!("Profile: {}", plan.profile);

    println!();
    println!("Optional steps (skipped for stability/speed):");
    println!("  GUI Applications:  mev make brew-cask --profile {}", plan.profile);
    println!("  Ollama Models:     mev make ollama-models");
    println!("  MLX Models:        mev make mlx-models");

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
    fn execute_create_fails_on_missing_tags() {
        let (_dir, ctx) = build_test_container();
        // Since ctx.ansible.all_tags() is empty for AnsibleAdapter::empty(),
        // FULL_SETUP_TAGS won't be found, and it should fail validation.

        let result = execute(&ctx, Profile::Macbook, false, false);
        assert!(result.is_err());
        let err_msg = result.unwrap_err().to_string();
        assert!(err_msg.contains("invalid tags in setup:"));
        assert!(err_msg.contains("brew-formulae")); // First tag
    }
}
