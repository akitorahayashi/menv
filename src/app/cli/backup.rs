//! CLI input contract for the `backup` command.

use clap::{Args, Subcommand};

use crate::adapters::ansible::locator;
use crate::app::DependencyContainer;
use crate::app::commands;
use crate::domain::error::AppError;

#[derive(Args)]
pub struct BackupArgs {
    #[command(subcommand)]
    pub command: BackupCommand,
}

#[derive(Subcommand)]
pub enum BackupCommand {
    /// List available backup targets
    #[command(alias = "ls")]
    List,

    /// Execute backup for a specific target
    Target {
        /// Backup target (system, vscode).
        target: String,

        /// Overwrite the existing backup file if it exists.
        #[arg(short, long)]
        overwrite: bool,
    },
}

pub fn run(args: BackupArgs) -> Result<(), AppError> {
    let ansible_dir = locator::locate_ansible_dir()?;
    let ctx = DependencyContainer::new(ansible_dir).map_err(|e| AppError::Config(e.to_string()))?;

    match args.command {
        BackupCommand::List => {
            commands::backup::list_targets();
            Ok(())
        }
        BackupCommand::Target { target, overwrite } => {
            commands::backup::execute(&ctx, &target, overwrite)
        }
    }
}
