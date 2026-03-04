//! `update` command orchestration — pipx upgrade execution.

use crate::domain::error::AppError;
use crate::domain::ports::version_source::VersionSource;

/// Execute the `update` command with an injected version source.
pub fn execute(source: &dyn VersionSource) -> Result<(), AppError> {
    let current = source.current_version()?;
    println!("Current version: {current}");

    println!("Running upgrade...");
    source.run_upgrade()?;

    println!();
    println!("✓ Upgrade command completed.");
    println!("Run `mev --version` in a new shell to verify the installed version.");

    Ok(())
}
