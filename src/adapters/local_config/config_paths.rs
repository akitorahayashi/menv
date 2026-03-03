//! Configuration path resolution.

use std::path::PathBuf;

fn config_base() -> PathBuf {
    dirs::config_dir()
        .or_else(|| dirs::home_dir().map(|h| h.join(".config")))
        .expect("config directory must be resolvable")
}

/// Default path to the mev configuration file.
pub fn default_config_path() -> PathBuf {
    config_base().join("menv").join("config.json")
}

/// Default path to the local config root for deployed role configs.
pub fn local_config_root() -> PathBuf {
    config_base().join("menv").join("roles")
}
