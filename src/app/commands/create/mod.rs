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

    eprintln!();
    eprintln!("mev: Creating {} environment", plan.profile);
    eprintln!("This will run {} tasks.", plan.tags.len());
    eprintln!();

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
        eprintln!("[{step}/{total}] Running: {tag}");

        ctx.ansible
            .run_playbook(plan.profile.as_str(), std::slice::from_ref(tag), plan.verbose)
            .inspect_err(|e| {
                eprintln!("Failed at step {step}/{total}: {tag}: {e}");
            })?;
        eprintln!("  ✓ Completed");
    }

    eprintln!();
    eprintln!("✓ Environment created successfully!");
    eprintln!("Profile: {}", plan.profile);

    eprintln!();
    eprintln!("Optional steps (skipped for stability/speed):");
    eprintln!("  GUI Applications:  mev make brew-cask --profile {}", plan.profile);
    eprintln!("  Ollama Models:     mev make ollama-models");
    eprintln!("  MLX Models:        mev make mlx-models");

    Ok(())
}
