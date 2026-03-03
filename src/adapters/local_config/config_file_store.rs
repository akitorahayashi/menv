//! Configuration file store using TOML on disk.

use std::path::PathBuf;

use crate::domain::config::VcsIdentity;
use crate::domain::error::AppError;
use crate::domain::ports::config_store::{ConfigStore, MevConfig};

pub struct ConfigFileStore {
    config_path: PathBuf,
}

impl ConfigFileStore {
    pub fn new(config_path: PathBuf) -> Self {
        Self { config_path }
    }
}

impl ConfigStore for ConfigFileStore {
    fn exists(&self) -> bool {
        self.config_path.exists()
    }

    fn load(&self) -> Result<MevConfig, AppError> {
        let content = std::fs::read_to_string(&self.config_path)?;
        serde_json::from_str(&content)
            .map_err(|e| AppError::Config(format!("failed to parse config: {e}")))
    }

    fn save(&self, config: &MevConfig) -> Result<(), AppError> {
        if let Some(parent) = self.config_path.parent() {
            std::fs::create_dir_all(parent)?;
        }
        let content = serde_json::to_string_pretty(config)
            .map_err(|e| AppError::Config(format!("failed to serialize config: {e}")))?;
        std::fs::write(&self.config_path, content)?;
        Ok(())
    }

    fn get_identity(&self, profile: &str) -> Result<Option<VcsIdentity>, AppError> {
        let config = self.load()?;
        match profile {
            "personal" => Ok(Some(config.personal)),
            "work" => Ok(Some(config.work)),
            _ => Ok(None),
        }
    }

    fn config_path(&self) -> PathBuf {
        self.config_path.clone()
    }
}
