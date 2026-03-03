//! Ansible execution environment setup.

use std::collections::HashMap;
use std::path::Path;

/// Build the environment variables for ansible execution.
pub fn ansible_env(config_path: &Path) -> HashMap<String, String> {
    let mut env: HashMap<String, String> = std::env::vars().collect();
    env.insert("ANSIBLE_CONFIG".to_string(), config_path.display().to_string());
    env
}
