//! Shared config deployment from ansible roles to local config root.
//!
//! Replicates Python `_deploy_configs_for_roles`: before ansible execution,
//! ensures each role's config directory is deployed to `~/.config/mev/roles/`.

use std::collections::HashSet;
use std::path::Path;

use crate::domain::error::AppError;
use crate::domain::ports::ansible::AnsiblePort;
use crate::domain::ports::fs::FsPort;

/// Deploy configs for roles associated with the given tags.
///
/// For each tag, resolves the owning role. If that role has a config directory
/// in the ansible assets, copies it to `local_config_root/{role}`.
/// When `overwrite` is false, existing config directories are skipped.
/// When `overwrite` is true, existing config directories are replaced.
pub fn deploy_for_tags(
    tags: &[String],
    ansible_dir: &Path,
    local_config_root: &Path,
    ansible: &dyn AnsiblePort,
    overwrite: bool,
    fs: &dyn FsPort,
) -> Result<(), AppError> {
    let available: HashSet<String> = ansible.roles_with_config()?.into_iter().collect();

    let mut deployed = HashSet::new();
    for tag in tags {
        let Some(role) = ansible.role_for_tag(tag) else {
            continue;
        };
        if !available.contains(&role) || !deployed.insert(role.clone()) {
            continue;
        }

        let target = local_config_root.join(&role);
        if target.exists() && !overwrite {
            continue;
        }

        if target.exists() {
            std::fs::remove_dir_all(&target).map_err(|e| {
                AppError::Config(format!("failed to remove existing config for {role}: {e}"))
            })?;
        }

        let source = ansible_dir.join("roles").join(&role).join("config");
        if !source.is_dir() {
            return Err(AppError::Config(format!(
                "config source directory is missing: {}",
                source.display()
            )));
        }
        if let Err(e) = fs.copy_dir_recursive(&source, &target) {
            let _ = std::fs::remove_dir_all(&target);
            return Err(e);
        }
        println!("  Deployed config for {role}");
    }

    Ok(())
}
