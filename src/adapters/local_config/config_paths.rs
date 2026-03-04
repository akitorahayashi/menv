//! Configuration path resolution.
//!
//! The base path is `~/.config/` — the project convention for macOS.
//! Ansible roles reference `local_config_root` as an extra var and expect
//! `~/.config/menv/roles/`, so this path must not change.

use std::path::PathBuf;

fn config_base() -> PathBuf {
    dirs::home_dir().expect("home directory must be resolvable").join(".config")
}

/// Default path to the mev configuration file.
pub fn default_config_path() -> PathBuf {
    config_base().join("menv").join("config.json")
}

/// Default path to the local config root for deployed role configs.
pub fn local_config_root() -> PathBuf {
    config_base().join("menv").join("roles")
}
