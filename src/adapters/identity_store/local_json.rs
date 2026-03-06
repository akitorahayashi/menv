//! Configuration file store using JSON on disk.

use std::path::PathBuf;

use crate::domain::error::AppError;
use crate::domain::ports::identity_store::{IdentityState, IdentityStore};
use crate::domain::vcs_identity::{SwitchIdentity, VcsIdentity};

pub struct IdentityFileStore {
    identity_path: PathBuf,
}

impl IdentityFileStore {
    pub fn new(identity_path: PathBuf) -> Self {
        Self { identity_path }
    }

    fn legacy_config_path(&self) -> PathBuf {
        self.identity_path.with_file_name("config.json")
    }
}

impl IdentityStore for IdentityFileStore {
    fn exists(&self) -> bool {
        self.identity_path.exists() || self.legacy_config_path().exists()
    }

    fn load(&self) -> Result<IdentityState, AppError> {
        if self.identity_path.exists() {
            let content = std::fs::read_to_string(&self.identity_path)?;
            return serde_json::from_str(&content)
                .map_err(|e| AppError::Config(format!("failed to parse identity config: {e}")));
        }

        if self.legacy_config_path().exists() {
            let content = std::fs::read_to_string(self.legacy_config_path())?;
            let state: IdentityState = serde_json::from_str(&content).map_err(|e| {
                AppError::Config(format!("failed to parse legacy identity config: {e}"))
            })?;

            // Migrate automatically to the new path.
            if let Err(e) = self.save(&state) {
                eprintln!("Warning: failed to migrate identity config: {e}");
            }
            return Ok(state);
        }

        Err(AppError::Config("no identity configuration found".to_string()))
    }

    fn save(&self, state: &IdentityState) -> Result<(), AppError> {
        let parent = self
            .identity_path
            .parent()
            .ok_or_else(|| AppError::Config("identity path has no parent directory".to_string()))?;
        std::fs::create_dir_all(parent)?;

        let content = serde_json::to_string_pretty(state)
            .map_err(|e| AppError::Config(format!("failed to serialize identity config: {e}")))?;

        // Atomic write: write to temp file in same directory, then rename.
        let tmp_path = parent.join(".identity.json.tmp");
        std::fs::write(&tmp_path, &content)
            .map_err(|e| AppError::Config(format!("failed to write temp identity config: {e}")))?;
        std::fs::rename(&tmp_path, &self.identity_path).map_err(|e| {
            let _ = std::fs::remove_file(&tmp_path);
            AppError::Config(format!("failed to rename temp identity config: {e}"))
        })?;
        Ok(())
    }

    fn get_identity(&self, identity: SwitchIdentity) -> Result<Option<VcsIdentity>, AppError> {
        let state = self.load()?;
        match identity {
            SwitchIdentity::Personal => Ok(Some(state.personal)),
            SwitchIdentity::Work => Ok(Some(state.work)),
        }
    }

    fn identity_path(&self) -> PathBuf {
        self.identity_path.clone()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::tempdir;

    #[test]
    fn identity_store_exists_and_load_empty() {
        let dir = tempdir().unwrap();
        let store = IdentityFileStore::new(dir.path().join("identity.json"));

        assert!(!store.exists());
        assert!(store.load().is_err());
    }

    #[test]
    fn identity_store_save_and_load() {
        let dir = tempdir().unwrap();
        let store = IdentityFileStore::new(dir.path().join("identity.json"));

        let state = IdentityState {
            personal: VcsIdentity {
                name: "John Doe".to_string(),
                email: "john@example.com".to_string(),
            },
            work: VcsIdentity {
                name: "John Worker".to_string(),
                email: "john@work.example.com".to_string(),
            },
        };

        store.save(&state).unwrap();
        assert!(store.exists());

        let loaded = store.load().unwrap();
        assert_eq!(loaded.personal.name, "John Doe");
        assert_eq!(loaded.personal.email, "john@example.com");
        assert_eq!(loaded.work.name, "John Worker");
        assert_eq!(loaded.work.email, "john@work.example.com");
    }

    #[test]
    fn identity_store_get_identity() {
        let dir = tempdir().unwrap();
        let store = IdentityFileStore::new(dir.path().join("identity.json"));

        let state = IdentityState {
            personal: VcsIdentity {
                name: "John Doe".to_string(),
                email: "john@example.com".to_string(),
            },
            work: VcsIdentity {
                name: "John Worker".to_string(),
                email: "john@work.example.com".to_string(),
            },
        };

        store.save(&state).unwrap();

        let personal = store.get_identity(SwitchIdentity::Personal).unwrap().unwrap();
        assert_eq!(personal.name, "John Doe");

        let work = store.get_identity(SwitchIdentity::Work).unwrap().unwrap();
        assert_eq!(work.name, "John Worker");
    }

    #[test]
    fn identity_store_migrates_legacy_config() {
        let dir = tempdir().unwrap();
        let identity_path = dir.path().join("identity.json");
        let store = IdentityFileStore::new(identity_path.clone());

        // Write to legacy path manually
        let legacy_state = IdentityState {
            personal: VcsIdentity {
                name: "Legacy User".to_string(),
                email: "legacy@example.com".to_string(),
            },
            work: VcsIdentity {
                name: "Legacy Work User".to_string(),
                email: "legacy_work@example.com".to_string(),
            },
        };
        let legacy_content = serde_json::to_string(&legacy_state).unwrap();
        std::fs::write(store.legacy_config_path(), legacy_content).unwrap();

        // Ensure exists() picks it up
        assert!(store.exists());

        // load() should read legacy and migrate it
        let loaded = store.load().unwrap();
        assert_eq!(loaded.personal.name, "Legacy User");

        // The new identity file should now exist
        assert!(identity_path.exists());
    }
}
