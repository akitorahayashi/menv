//! CLI input contract for the `update` command.

use crate::domain::error::AppError;
use crate::domain::ports::version_source::VersionSource;

pub fn run() -> Result<(), AppError> {
    let source = crate::adapters::version::cargo_pkg_version::CargoPkgVersion;
    run_with_source(&source)
}

pub fn run_with_source(source: &dyn VersionSource) -> Result<(), AppError> {
    let current = source.current_version()?;
    println!("Current version: {current}");

    println!("Checking for updates...");
    let latest = match source.latest_version() {
        Ok(v) => v,
        Err(_) => {
            println!();
            println!("✓ Version check unavailable. You are on version {current}.");
            return Ok(());
        }
    };

    println!("Latest version:  {latest}");

    if !source.needs_update(&current, &latest) {
        println!();
        println!("✓ You are already on the latest version!");
        return Ok(());
    }

    println!();
    println!("Update available: {current} → {latest}");

    source.run_upgrade()?;

    let new_version = source.current_version()?;
    println!();
    println!("✓ Successfully updated to version {new_version}!");

    Ok(())
}
