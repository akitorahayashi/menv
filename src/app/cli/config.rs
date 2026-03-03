//! CLI input contract for the `config` command.

use std::io::Write;

use clap::Subcommand;

use crate::adapters::package_assets::ansible_asset_locator;
use crate::app::AppContext;
use crate::domain::config::VcsIdentity;
use crate::domain::error::AppError;
use crate::domain::ports::config_store::{ConfigStore, MevConfig};
use crate::domain::ports::role_catalog::RoleCatalog;

#[derive(Subcommand)]
pub enum ConfigCommand {
    /// Display current VCS identity configuration.
    Show,

    /// Set VCS identity configuration interactively.
    Set,

    /// Deploy role configs to ~/.config/menv/roles/.
    #[command(alias = "cr")]
    Create {
        /// Role name to deploy config for. If omitted, deploys all roles.
        role: Option<String>,

        /// Overwrite existing config with package defaults.
        #[arg(short, long)]
        overwrite: bool,
    },
}

pub fn run(cmd: ConfigCommand) -> Result<(), AppError> {
    match cmd {
        ConfigCommand::Show => run_show(),
        ConfigCommand::Set => run_set(),
        ConfigCommand::Create { role, overwrite } => run_create(role, overwrite),
    }
}

fn run_show() -> Result<(), AppError> {
    let ansible_dir = ansible_asset_locator::locate_ansible_dir()?;
    let ctx = AppContext::new(ansible_dir).map_err(|e| AppError::Config(e.to_string()))?;

    if !ctx.config_store.exists() {
        eprintln!("No configuration found.");
        eprintln!("Run 'mev config set' to configure.");
        return Err(AppError::Config("no configuration found".to_string()));
    }

    let config = ctx.config_store.load()?;
    let path = ctx.config_store.config_path();

    println!("Config file: {}", path.display());
    println!();
    println!("{:<12} {:<20} Email", "Profile", "Name");
    println!("{:-<12} {:-<20} {:-<30}", "", "", "");
    println!("{:<12} {:<20} {}", "personal", config.personal.name, config.personal.email);
    println!("{:<12} {:<20} {}", "work", config.work.name, config.work.email);

    Ok(())
}

fn prompt(label: &str, default: &str) -> Result<String, AppError> {
    if default.is_empty() {
        print!("{label}: ");
    } else {
        print!("{label} [{default}]: ");
    }
    std::io::stdout().flush()?;
    let mut input = String::new();
    std::io::stdin().read_line(&mut input)?;
    let trimmed = input.trim();
    if trimmed.is_empty() { Ok(default.to_string()) } else { Ok(trimmed.to_string()) }
}

fn run_set() -> Result<(), AppError> {
    let ansible_dir = ansible_asset_locator::locate_ansible_dir()?;
    let ctx = AppContext::new(ansible_dir).map_err(|e| AppError::Config(e.to_string()))?;

    println!("Configure mev VCS identities");
    println!();

    let existing = if ctx.config_store.exists() { ctx.config_store.load().ok() } else { None };

    let (p_name_default, p_email_default, w_name_default, w_email_default) = match &existing {
        Some(cfg) => (
            cfg.personal.name.as_str(),
            cfg.personal.email.as_str(),
            cfg.work.name.as_str(),
            cfg.work.email.as_str(),
        ),
        None => ("", "", "", ""),
    };

    println!("Personal identity:");
    let personal_name = prompt("  Name", p_name_default)?;
    let personal_email = prompt("  Email", p_email_default)?;
    println!();

    println!("Work identity:");
    let work_name = prompt("  Name", w_name_default)?;
    let work_email = prompt("  Email", w_email_default)?;

    let config = MevConfig {
        personal: VcsIdentity { name: personal_name, email: personal_email },
        work: VcsIdentity { name: work_name, email: work_email },
    };

    ctx.config_store.save(&config)?;

    println!();
    println!("Configuration saved to {}", ctx.config_store.config_path().display());

    Ok(())
}

fn run_create(role: Option<String>, overwrite: bool) -> Result<(), AppError> {
    let ansible_dir = ansible_asset_locator::locate_ansible_dir()?;
    let ctx = AppContext::new(ansible_dir.clone()).map_err(|e| AppError::Config(e.to_string()))?;

    let available = ctx.role_catalog.roles_with_config()?;

    let roles_to_deploy = if let Some(role_name) = role {
        if !available.contains(&role_name) {
            return Err(AppError::Config(format!(
                "role '{role_name}' has no config directory. Available: {}",
                available.join(", ")
            )));
        }
        vec![role_name]
    } else {
        if available.is_empty() {
            println!("No roles with config directories found.");
            return Ok(());
        }
        available
    };

    let local_config_root = crate::adapters::local_config::config_paths::local_config_root();

    for role_name in &roles_to_deploy {
        let source = ansible_dir.join("roles").join(role_name).join("config");
        let target = local_config_root.join(role_name);

        if target.exists() && !overwrite {
            println!("  {role_name}: config exists (use --overwrite to replace)");
            continue;
        }
        if target.exists() {
            std::fs::remove_dir_all(&target).map_err(|e| {
                AppError::Config(format!("failed to remove existing config for {role_name}: {e}"))
            })?;
        }
        copy_dir_recursive(&source, &target)?;
        println!("✓ {role_name}: config deployed");
    }

    Ok(())
}

fn copy_dir_recursive(src: &std::path::Path, dst: &std::path::Path) -> Result<(), AppError> {
    std::fs::create_dir_all(dst)?;
    for entry in std::fs::read_dir(src)? {
        let entry = entry?;
        let src_path = entry.path();
        let dst_path = dst.join(entry.file_name());
        if src_path.is_dir() {
            copy_dir_recursive(&src_path, &dst_path)?;
        } else {
            std::fs::copy(&src_path, &dst_path)?;
        }
    }
    Ok(())
}
