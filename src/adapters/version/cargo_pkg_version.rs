//! Version source from Cargo package metadata with GitHub release check and pipx upgrade.

use std::process::Command;

use crate::domain::error::AppError;
use crate::domain::ports::version_source::VersionSource;

const GITHUB_RELEASES_URL: &str =
    "https://api.github.com/repos/akitorahayashi/menv/releases/latest";

pub struct CargoPkgVersion;

impl VersionSource for CargoPkgVersion {
    fn current_version(&self) -> Result<String, AppError> {
        Ok(env!("CARGO_PKG_VERSION").to_string())
    }

    fn latest_version(&self) -> Result<String, AppError> {
        let output = Command::new("curl")
            .args([
                "-sSL",
                "-H",
                "Accept: application/vnd.github.v3+json",
                "-H",
                "User-Agent: menv-cli",
                GITHUB_RELEASES_URL,
            ])
            .output()
            .map_err(|e| AppError::VersionCheck(format!("failed to fetch latest version: {e}")))?;

        if !output.status.success() {
            let stderr = String::from_utf8_lossy(&output.stderr);
            return Err(AppError::VersionCheck(format!(
                "failed to fetch latest version from GitHub (exit code: {}): {}",
                output.status.code().unwrap_or(-1),
                stderr.trim()
            )));
        }

        let body = String::from_utf8_lossy(&output.stdout);
        let data: serde_json::Value = serde_json::from_str(&body)
            .map_err(|e| AppError::VersionCheck(format!("failed to parse release data: {e}")))?;

        let tag = data["tag_name"]
            .as_str()
            .ok_or_else(|| AppError::VersionCheck("no tag_name in release data".to_string()))?;

        Ok(tag.trim_start_matches('v').to_string())
    }

    fn needs_update(&self, current: &str, latest: &str) -> bool {
        match (semver::Version::parse(current), semver::Version::parse(latest)) {
            (Ok(cur), Ok(lat)) => lat > cur,
            _ => current != latest,
        }
    }

    fn run_upgrade(&self) -> Result<(), AppError> {
        // Upgrade strategy is intentionally tied to pipx.
        // This project is installed as a pipx-managed unit (Python venv + bundled
        // Rust binaries + packaged assets such as ansible content), so the updater
        // must refresh the same installation boundary. A cargo-based self-update
        // would only target Rust artifacts and can diverge from the pipx runtime.
        println!("Upgrading menv via pipx...");

        let status = Command::new("pipx").args(["upgrade", "menv"]).status().map_err(|e| {
            if e.kind() == std::io::ErrorKind::NotFound {
                AppError::VersionCheck(
                    "pipx not found. Please ensure pipx is installed.".to_string(),
                )
            } else {
                AppError::VersionCheck(format!("failed to run pipx: {e}"))
            }
        })?;

        if !status.success() {
            return Err(AppError::VersionCheck(format!(
                "pipx upgrade failed with exit code {}",
                status.code().unwrap_or(-1)
            )));
        }

        Ok(())
    }
}
