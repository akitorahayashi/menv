//! `switch` command orchestration — VCS identity switching.

use crate::app::AppContext;
use crate::domain::error::AppError;
use crate::domain::ports::config_store::ConfigStore;
use crate::domain::ports::git::GitPort;
use crate::domain::ports::jj::JjPort;
use crate::domain::vcs_identity::SwitchProfile;

/// Execute the `switch` command: change global git/jj identity.
pub fn execute(ctx: &AppContext, profile: SwitchProfile) -> Result<(), AppError> {
    if !ctx.config_store.exists() {
        eprintln!("No configuration found.");
        eprintln!("Run 'mev config set' first to configure identities.");
        return Err(AppError::Config("no configuration found".to_string()));
    }

    let identity = ctx
        .config_store
        .get_identity(profile)?
        .ok_or_else(|| AppError::Config(format!("failed to load {} identity", profile.as_str())))?;

    if identity.name.is_empty() || identity.email.is_empty() {
        return Err(AppError::Config(format!(
            "{} identity is not configured. Run 'mev config set' to configure.",
            profile.as_str()
        )));
    }

    println!("Switching to {} identity...", profile.as_str());

    // Git configuration (required)
    ctx.git.set_identity(&identity.name, &identity.email)?;

    // Jujutsu configuration (optional — skip if jj not installed)
    if ctx.jj.is_available()
        && let Err(e) = ctx.jj.set_identity(&identity.name, &identity.email)
    {
        eprintln!("Warning: jj identity update failed: {e}");
    }

    // Show current configuration via git (primary VCS)
    let (name, email) = ctx.git.get_identity()?;
    println!();
    println!("Switched to {} identity", profile.as_str());
    println!("  Name:  {name}");
    println!("  Email: {email}");

    Ok(())
}
