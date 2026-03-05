//! Configuration file store using JSON on disk.

use std::path::PathBuf;

use crate::domain::error::AppError;
use crate::domain::ports::identity_store::{IdentityStore, IdentityState};
use crate::domain::vcs_identity::VcsIdentity;

pub struct IdentityFileStore {
    identity_path: PathBuf,
}

impl IdentityFileStore {
    pub fn new(identity_path: PathBuf) -> Self {
        Self { identity_path }
    }
}

impl IdentityStore for IdentityFileStore {
    fn exists(&self) -> bool {
        self.identity_path.exists()
    }

    fn load(&self) -> Result<IdentityState, AppError> {
        let content = std::fs::read_to_string(&self.identity_path)?;
        serde_json::from_str(&content)
            .map_err(|e| AppError::Config(format!("failed to parse identity config: {e}")))
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

    fn get_identity(&self, profile: &str) -> Result<Option<VcsIdentity>, AppError> {
        let state = self.load()?;
        match profile {
            "personal" => Ok(Some(state.personal)),
            "work" => Ok(Some(state.work)),
            _ => Ok(None),
        }
    }

    fn identity_path(&self) -> PathBuf {
        self.identity_path.clone()
    }
}
