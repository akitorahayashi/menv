//! Shared config deployment from ansible roles to local config root.
//!
//! Replicates Python `_deploy_configs_for_roles`: before ansible execution,
//! ensures each role's config directory is deployed to `~/.config/mev/roles/`.

use std::collections::HashSet;
use std::path::Path;

use crate::domain::error::AppError;
use crate::domain::ports::ansible::AnsiblePort;

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
        if let Err(e) = copy_dir_recursive(&source, &target) {
            let _ = std::fs::remove_dir_all(&target);
            return Err(e);
        }
        println!("  Deployed config for {role}");
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::tempdir;
    use std::collections::HashMap;

    struct MockAnsible {
        roles_with_config: Vec<String>,
        role_for_tag: HashMap<String, String>,
    }

    impl AnsiblePort for MockAnsible {
        fn run_playbook(&self, _profile: &str, _tags: &[String], _verbose: bool) -> Result<(), AppError> {
            Ok(())
        }
        fn roles_with_config(&self) -> Result<Vec<String>, AppError> {
            Ok(self.roles_with_config.clone())
        }
        fn all_tags(&self) -> Vec<String> {
            Vec::new()
        }
        fn tags_by_role(&self) -> HashMap<String, Vec<String>> {
            HashMap::new()
        }
        fn role_for_tag(&self, tag: &str) -> Option<String> {
            self.role_for_tag.get(tag).cloned()
        }
        fn validate_tags(&self, _tags: &[String]) -> bool {
            true
        }
    }

    #[test]
    fn deploy_for_tags_copies_config() {
        let ansible_dir = tempdir().unwrap();
        let local_config_root = tempdir().unwrap();

        // Create ansible/roles/test_role/config/settings.json
        let config_dir = ansible_dir.path().join("roles").join("test_role").join("config");
        std::fs::create_dir_all(&config_dir).unwrap();
        std::fs::write(config_dir.join("settings.json"), b"{}").unwrap();

        let mock_ansible = MockAnsible {
            roles_with_config: vec!["test_role".to_string()],
            role_for_tag: HashMap::from([("test_tag".to_string(), "test_role".to_string())]),
        };

        deploy_for_tags(
            &["test_tag".to_string()],
            ansible_dir.path(),
            local_config_root.path(),
            &mock_ansible,
            false,
        ).unwrap();

        let deployed_file = local_config_root.path().join("test_role").join("settings.json");
        assert!(deployed_file.exists());
    }

    #[test]
    fn deploy_for_tags_skips_without_overwrite() {
        let ansible_dir = tempdir().unwrap();
        let local_config_root = tempdir().unwrap();

        let config_dir = ansible_dir.path().join("roles").join("test_role").join("config");
        std::fs::create_dir_all(&config_dir).unwrap();
        std::fs::write(config_dir.join("settings.json"), b"new").unwrap();

        let deployed_dir = local_config_root.path().join("test_role");
        std::fs::create_dir_all(&deployed_dir).unwrap();
        std::fs::write(deployed_dir.join("settings.json"), b"old").unwrap();

        let mock_ansible = MockAnsible {
            roles_with_config: vec!["test_role".to_string()],
            role_for_tag: HashMap::from([("test_tag".to_string(), "test_role".to_string())]),
        };

        // overwrite = false
        deploy_for_tags(
            &["test_tag".to_string()],
            ansible_dir.path(),
            local_config_root.path(),
            &mock_ansible,
            false,
        ).unwrap();

        let content = std::fs::read_to_string(deployed_dir.join("settings.json")).unwrap();
        assert_eq!(content, "old"); // Should not overwrite

        // overwrite = true
        deploy_for_tags(
            &["test_tag".to_string()],
            ansible_dir.path(),
            local_config_root.path(),
            &mock_ansible,
            true,
        ).unwrap();

        let content = std::fs::read_to_string(deployed_dir.join("settings.json")).unwrap();
        assert_eq!(content, "new"); // Should overwrite
    }

    #[test]
    fn copy_dir_recursive_works() {
        let src = tempdir().unwrap();
        let dst = tempdir().unwrap();

        std::fs::create_dir_all(src.path().join("a").join("b")).unwrap();
        std::fs::write(src.path().join("a").join("b").join("file.txt"), b"test").unwrap();

        copy_dir_recursive(src.path(), dst.path()).unwrap();

        let dst_file = dst.path().join("a").join("b").join("file.txt");
        assert!(dst_file.exists());
        assert_eq!(std::fs::read_to_string(dst_file).unwrap(), "test");
    }
}

/// Recursively copy a directory tree.
pub fn copy_dir_recursive(src: &Path, dst: &Path) -> Result<(), AppError> {
    if !src.is_dir() {
        return Err(AppError::Config(format!(
            "config source directory is missing: {}",
            src.display()
        )));
    }
    std::fs::create_dir_all(dst)?;
    for entry in std::fs::read_dir(src)? {
        let entry = entry?;
        let src_path = entry.path();
        let dst_path = dst.join(entry.file_name());
        if src_path.is_dir() {
            copy_dir_recursive(&src_path, &dst_path)?;
        } else {
            std::fs::copy(&src_path, &dst_path)?;
        }
    }
    Ok(())
}
