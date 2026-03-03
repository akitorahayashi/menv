//! CLI input contract for the `make` command.

use clap::Args;

use crate::adapters::package_assets::ansible_asset_locator;
use crate::app::AppContext;
use crate::domain::error::AppError;
use crate::domain::execution_plan::ExecutionPlan;
use crate::domain::ports::ansible_executor::AnsibleExecutor;
use crate::domain::ports::tag_catalog::TagCatalog;
use crate::domain::profile;
use crate::domain::tag;

#[derive(Args)]
pub struct MakeArgs {
    /// Ansible tag to run (e.g., rust, python-tools, shell, brew-cask).
    pub tag: String,

    /// Profile to use (common, macbook/mbk, mac-mini/mmn).
    #[arg(default_value = "common")]
    pub profile: String,

    /// Enable verbose output.
    #[arg(short, long)]
    pub verbose: bool,

    /// Overwrite existing configuration files.
    #[arg(short, long)]
    pub overwrite: bool,
}

pub fn run(args: MakeArgs) -> Result<(), AppError> {
    let resolved = profile::validate_profile(&args.profile)?;

    // Resolve tag groups
    let tags_to_run = tag::resolve_tags(&args.tag);

    let ansible_dir = ansible_asset_locator::locate_ansible_dir()?;
    let ctx = AppContext::new(ansible_dir).map_err(|e| AppError::Config(e.to_string()))?;

    // Validate tags exist in catalog
    for t in &tags_to_run {
        if ctx.tag_catalog.role_for_tag(t).is_none() {
            return Err(AppError::InvalidTag(format!(
                "unknown tag '{t}'. Use 'mev list' to see available tags."
            )));
        }
    }

    let plan = ExecutionPlan::make(resolved, tags_to_run, args.verbose);

    println!("Running: {}", args.tag);
    if resolved != "common" {
        println!("Profile: {resolved}");
    }
    println!();

    ctx.ansible_executor.run_playbook(resolved, &plan.tags, plan.verbose)?;

    println!();
    println!("✓ Completed successfully!");

    Ok(())
}
