//! `backup` command orchestration — backup system settings or configurations.

use std::path::{Path, PathBuf};

use crate::adapters::backup::{system_defaults, vscode_extensions};
use crate::app::AppContext;
use crate::domain::backup::BackupTarget;
use crate::domain::error::AppError;

/// Execute the `backup` command for a given target.
pub fn execute(ctx: &AppContext, target_input: &str) -> Result<(), AppError> {
    if matches!(target_input, "list" | "ls") {
        list_targets();
        return Ok(());
    }

    let target = BackupTarget::from_input(target_input).ok_or_else(|| {
        let valid: Vec<_> = BackupTarget::all().iter().map(|t| t.name()).collect();
        AppError::Backup(format!(
            "unknown backup target '{target_input}'. Valid targets: {}",
            valid.join(", ")
        ))
    })?;

    let local_config_dir = ctx.local_config_root.join(target.role()).join(target.subpath());

    println!("Running backup: {}", target.description());
    println!();

    match target {
        BackupTarget::System => {
            let definitions_dir = resolve_definitions_dir(&local_config_dir, ctx, &target);
            let output_file = local_config_dir.join("system.yml");
            system_defaults::execute(&definitions_dir, &output_file)
        }
        BackupTarget::Vscode => {
            let output_file = local_config_dir.join("vscode-extensions.json");
            vscode_extensions::execute(&output_file)
        }
    }?;

    println!();
    println!("✓ Backup completed successfully!");

    Ok(())
}

/// Resolve definitions directory with fallback from local to package defaults.
fn resolve_definitions_dir(
    local_config_dir: &Path,
    ctx: &AppContext,
    target: &BackupTarget,
) -> PathBuf {
    let local_definitions = local_config_dir.join("definitions");
    if local_definitions.exists() {
        return local_definitions;
    }

    println!(
        "Local definitions not found at {}. Using package defaults.",
        local_definitions.display()
    );

    ctx.ansible_dir
        .join("roles")
        .join(target.role())
        .join("config")
        .join(target.subpath())
        .join("definitions")
}

fn list_targets() {
    println!("Available backup targets:");
    println!();
    for target in BackupTarget::all() {
        println!("  {:<8} - {}", target.name(), target.description());
    }
    println!();
    println!("Usage: mev backup <target>");
}
