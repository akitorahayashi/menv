//! Stable library entrypoints for programmatic consumers.
//!
//! Each public function wires context creation to command execution.
//! `cli/` modules delegate here; external callers (tests, scripts) can
//! import these directly via `mev::api::*`.

use crate::adapters::ansible::locator;
use crate::adapters::version_source::pipx::PipxVersionSource;
use crate::app::DependencyContainer;
use crate::app::commands;
use crate::domain::error::AppError;
use crate::domain::ports::version_source::VersionSource;

// =============================================================================
// API Models
// =============================================================================

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Profile {
    Macbook,
    MacMini,
    Common,
}

impl From<crate::domain::profile::Profile> for Profile {
    fn from(domain_profile: crate::domain::profile::Profile) -> Self {
        match domain_profile {
            crate::domain::profile::Profile::Macbook => Profile::Macbook,
            crate::domain::profile::Profile::MacMini => Profile::MacMini,
            crate::domain::profile::Profile::Common => Profile::Common,
        }
    }
}

impl From<Profile> for crate::domain::profile::Profile {
    fn from(api_profile: Profile) -> Self {
        match api_profile {
            Profile::Macbook => crate::domain::profile::Profile::Macbook,
            Profile::MacMini => crate::domain::profile::Profile::MacMini,
            Profile::Common => crate::domain::profile::Profile::Common,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SwitchIdentity {
    Personal,
    Work,
}

impl From<crate::domain::vcs_identity::SwitchIdentity> for SwitchIdentity {
    fn from(domain_id: crate::domain::vcs_identity::SwitchIdentity) -> Self {
        match domain_id {
            crate::domain::vcs_identity::SwitchIdentity::Personal => SwitchIdentity::Personal,
            crate::domain::vcs_identity::SwitchIdentity::Work => SwitchIdentity::Work,
        }
    }
}

impl From<SwitchIdentity> for crate::domain::vcs_identity::SwitchIdentity {
    fn from(api_id: SwitchIdentity) -> Self {
        match api_id {
            SwitchIdentity::Personal => crate::domain::vcs_identity::SwitchIdentity::Personal,
            SwitchIdentity::Work => crate::domain::vcs_identity::SwitchIdentity::Work,
        }
    }
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct VcsIdentity {
    pub name: String,
    pub email: String,
}

impl From<crate::domain::vcs_identity::VcsIdentity> for VcsIdentity {
    fn from(domain_id: crate::domain::vcs_identity::VcsIdentity) -> Self {
        VcsIdentity {
            name: domain_id.name,
            email: domain_id.email,
        }
    }
}

impl From<VcsIdentity> for crate::domain::vcs_identity::VcsIdentity {
    fn from(api_id: VcsIdentity) -> Self {
        crate::domain::vcs_identity::VcsIdentity {
            name: api_id.name,
            email: api_id.email,
        }
    }
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct IdentityState {
    pub personal: VcsIdentity,
    pub work: VcsIdentity,
}

impl From<crate::domain::ports::identity_store::IdentityState> for IdentityState {
    fn from(domain_state: crate::domain::ports::identity_store::IdentityState) -> Self {
        IdentityState {
            personal: domain_state.personal.into(),
            work: domain_state.work.into(),
        }
    }
}

impl From<IdentityState> for crate::domain::ports::identity_store::IdentityState {
    fn from(api_state: IdentityState) -> Self {
        crate::domain::ports::identity_store::IdentityState {
            personal: api_state.personal.into(),
            work: api_state.work.into(),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BackupTarget {
    System,
    Vscode,
}

impl From<crate::domain::backup_target::BackupTarget> for BackupTarget {
    fn from(domain_target: crate::domain::backup_target::BackupTarget) -> Self {
        match domain_target {
            crate::domain::backup_target::BackupTarget::System => BackupTarget::System,
            crate::domain::backup_target::BackupTarget::Vscode => BackupTarget::Vscode,
        }
    }
}

impl From<BackupTarget> for crate::domain::backup_target::BackupTarget {
    fn from(api_target: BackupTarget) -> Self {
        match api_target {
            BackupTarget::System => crate::domain::backup_target::BackupTarget::System,
            BackupTarget::Vscode => crate::domain::backup_target::BackupTarget::Vscode,
        }
    }
}

#[derive(Debug)]
pub struct Error(pub String);

impl std::fmt::Display for Error {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl std::error::Error for Error {}

impl From<crate::domain::error::AppError> for Error {
    fn from(e: crate::domain::error::AppError) -> Self {
        Error(e.to_string())
    }
}

#[derive(Debug, Clone)]
pub struct ExecutionPlan {
    pub profile: Profile,
    pub tags: Vec<String>,
    pub verbose: bool,
}

impl From<crate::domain::execution_plan::ExecutionPlan> for ExecutionPlan {
    fn from(plan: crate::domain::execution_plan::ExecutionPlan) -> Self {
        ExecutionPlan {
            profile: plan.profile.into(),
            tags: plan.tags,
            verbose: plan.verbose,
        }
    }
}

// =============================================================================
// Create
// =============================================================================

/// Provision a complete development environment for the given profile.
pub fn create(profile: Profile, overwrite: bool, verbose: bool) -> Result<(), Error> {
    let ctx = ansible_context()?;
    commands::create::execute(&ctx, profile.into(), overwrite, verbose).map_err(Into::into)
}

// =============================================================================
// Make
// =============================================================================

/// Run a single Ansible task by tag within a profile.
pub fn make(profile: Profile, tag: &str, overwrite: bool, verbose: bool) -> Result<(), Error> {
    let ctx = ansible_context()?;
    commands::make::execute(&ctx, profile.into(), tag, overwrite, verbose).map_err(Into::into)
}

// =============================================================================
// List
// =============================================================================

/// Print the available tags, tag groups, and profiles.
pub fn list() -> Result<(), Error> {
    let ctx = ansible_context()?;
    commands::list::execute(&ctx).map_err(Into::into)
}

// =============================================================================
// Config
// =============================================================================

/// Deploy role configuration files.
pub fn config_create(role: Option<String>, overwrite: bool) -> Result<(), Error> {
    let ctx = ansible_context()?;
    commands::config::create(&ctx, role, overwrite).map_err(Into::into)
}

// =============================================================================
// Identity
// =============================================================================

/// Show current VCS identity configuration.
pub fn identity_show() -> Result<(), Error> {
    let ctx = identity_context()?;
    commands::identity::show(&ctx).map_err(Into::into)
}

/// Interactively set VCS identity configuration.
pub fn identity_set() -> Result<(), Error> {
    let ctx = identity_context()?;
    commands::identity::set(&ctx).map_err(Into::into)
}

// =============================================================================
// Switch
// =============================================================================

/// Switch the global VCS identity between personal and work.
pub fn switch(identity: SwitchIdentity) -> Result<(), Error> {
    let ctx = identity_context()?;
    commands::switch::execute(&ctx, identity.into()).map_err(Into::into)
}

// =============================================================================
// Update
// =============================================================================

/// Check for and install updates to the mev CLI.
pub fn update() -> Result<(), Error> {
    let source = PipxVersionSource;
    commands::update::execute(&source).map_err(Into::into)
}

/// Update with a caller-supplied version source (test seam).
#[allow(dead_code)]
pub(crate) fn update_with_source(source: &dyn VersionSource) -> Result<(), Error> {
    commands::update::execute(source).map_err(Into::into)
}

// =============================================================================
// Backup
// =============================================================================

/// Backup a system setting or configuration target.
pub fn backup(target: &str) -> Result<(), Error> {
    let ctx = ansible_context()?;
    commands::backup::execute(&ctx, target).map_err(Into::into)
}

fn ansible_context() -> Result<DependencyContainer, AppError> {
    let ansible_dir = locator::locate_ansible_dir()?;
    DependencyContainer::new(ansible_dir).map_err(|e| AppError::Config(e.to_string()))
}

fn identity_context() -> Result<DependencyContainer, AppError> {
    DependencyContainer::for_identity().map_err(|e| AppError::Config(e.to_string()))
}
