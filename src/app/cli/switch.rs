//! CLI input contract for the `switch` command.

use clap::Args;

use crate::app::AppContext;
use crate::app::commands;
use crate::domain::error::AppError;
use crate::domain::vcs_identity;

#[derive(Args)]
pub struct SwitchArgs {
    /// Profile to switch to (personal/p, work/w).
    pub profile: String,
}

pub fn run(args: SwitchArgs) -> Result<(), AppError> {
    let ctx = AppContext::for_config().map_err(|e| AppError::Config(e.to_string()))?;

    let resolved = vcs_identity::resolve_switch_profile(&args.profile).ok_or_else(|| {
        AppError::InvalidProfile(format!(
            "invalid profile '{}'. Valid: personal (p), work (w)",
            args.profile
        ))
    })?;

    commands::switch::execute(&ctx, resolved)
}
