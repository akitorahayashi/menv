//! Configuration path resolution.

use std::path::PathBuf;

/// Default path to the mev configuration file.
pub fn default_config_path() -> PathBuf {
    dirs::home_dir()
        .expect("home directory must be resolvable")
        .join(".config")
        .join("menv")
        .join("config.json")
}

/// Default path to the local config root for deployed role configs.
pub fn local_config_root() -> PathBuf {
    dirs::home_dir()
        .expect("home directory must be resolvable")
        .join(".config")
        .join("menv")
        .join("roles")
}
