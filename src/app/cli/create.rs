//! CLI input contract for the `create` command.

use clap::Args;

use crate::adapters::package_assets::ansible_asset_locator;
use crate::app::AppContext;
use crate::domain::error::AppError;
use crate::domain::execution_plan::ExecutionPlan;
use crate::domain::ports::ansible_executor::AnsibleExecutor;
use crate::domain::ports::role_catalog::RoleCatalog;
use crate::domain::ports::tag_catalog::TagCatalog;
use crate::domain::profile;
use crate::domain::tag::FULL_SETUP_TAGS;

#[derive(Args)]
pub struct CreateArgs {
    /// Profile to create (macbook/mbk, mac-mini/mmn).
    pub profile: String,

    /// Enable verbose output.
    #[arg(short, long)]
    pub verbose: bool,

    /// Overwrite existing configuration files.
    #[arg(short, long)]
    pub overwrite: bool,
}

pub fn run(args: CreateArgs) -> Result<(), AppError> {
    let resolved = profile::validate_machine_profile(&args.profile)?;

    let ansible_dir = ansible_asset_locator::locate_ansible_dir()?;
    let ctx = AppContext::new(ansible_dir).map_err(|e| AppError::Config(e.to_string()))?;

    // Validate all tags exist
    let all_catalog_tags: std::collections::HashSet<String> =
        ctx.tag_catalog.all_tags().into_iter().collect();
    let invalid: Vec<&&str> =
        FULL_SETUP_TAGS.iter().filter(|t| !all_catalog_tags.contains(**t)).collect();
    if !invalid.is_empty() {
        let names: Vec<String> = invalid.iter().map(|t| (**t).to_string()).collect();
        return Err(AppError::InvalidTag(format!("invalid tags in setup: {}", names.join(", "))));
    }

    let plan = ExecutionPlan::full_setup(resolved, args.verbose);

    println!();
    println!("mev: Creating {resolved} environment");
    println!("This will run {} tasks.", plan.tags.len());
    println!();

    // Deploy configs for roles that need it
    let roles_with_config: std::collections::HashSet<String> =
        ctx.role_catalog.roles_with_config().into_iter().collect();
    let _roles_to_deploy: std::collections::HashSet<String> = plan
        .tags
        .iter()
        .filter_map(|tag| ctx.tag_catalog.role_for_tag(tag))
        .filter(|role| roles_with_config.contains(role))
        .collect();

    // Config deployment is handled by ansible roles themselves via local_config_root

    // Execute each tag
    for (i, tag) in plan.tags.iter().enumerate() {
        let step = i + 1;
        let total = plan.tags.len();
        println!("[{step}/{total}] Running: {tag}");

        ctx.ansible_executor
            .run_playbook(resolved, std::slice::from_ref(tag), plan.verbose)
            .inspect_err(|_e| {
                eprintln!("Failed at step {step}/{total}: {tag}");
            })?;
        println!("  ✓ Completed");
    }

    println!();
    println!("✓ Environment created successfully!");
    println!("Profile: {resolved}");

    // Print optional tasks summary
    println!();
    println!("Optional steps (skipped for stability/speed):");
    println!("  GUI Applications:  mev make brew-cask {resolved}");
    println!("  Ollama Models:     mev make ollama-models");
    println!("  MLX Models:        mev make mlx-models");

    Ok(())
}
