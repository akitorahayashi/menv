//! Profile identifiers and mapping rules.

use crate::domain::error::AppError;

/// Machine-specific profiles that require explicit selection.
pub const MACHINE_PROFILES: &[Profile] = &[Profile::Macbook, Profile::MacMini];

/// All valid profile identifiers including "common".
pub const VALID_PROFILES: &[Profile] = &[Profile::Common, Profile::Macbook, Profile::MacMini];

/// Profile alias mappings.
pub const PROFILE_ALIASES: &[(&str, Profile)] =
    &[("mbk", Profile::Macbook), ("mmn", Profile::MacMini), ("cmn", Profile::Common)];

/// Strong type for environment profiles.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Profile {
    Macbook,
    MacMini,
    Common,
}

impl Profile {
    pub fn as_str(&self) -> &'static str {
        match self {
            Profile::Macbook => "macbook",
            Profile::MacMini => "mac-mini",
            Profile::Common => "common",
        }
    }
}

impl std::fmt::Display for Profile {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.as_str())
    }
}

/// Resolve a profile identifier or alias to its canonical enum variant.
pub fn resolve_profile(input: &str) -> Option<Profile> {
    // Direct match
    for &profile in VALID_PROFILES {
        if input == profile.as_str() {
            return Some(profile);
        }
    }
    // Alias match
    for &(alias, canonical) in PROFILE_ALIASES {
        if input == alias {
            return Some(canonical);
        }
    }
    None
}

/// Validate that a profile is a machine-specific profile (required for `create`).
pub fn validate_machine_profile(input: &str) -> Result<Profile, AppError> {
    let resolved =
        resolve_profile(input).ok_or_else(|| AppError::InvalidProfile(input.to_string()))?;

    if !MACHINE_PROFILES.contains(&resolved) {
        let valid_names: Vec<String> = MACHINE_PROFILES.iter().map(|p| p.as_str().to_string()).collect();
        return Err(AppError::InvalidProfile(format!(
            "'{input}' is not a machine profile. Valid: {}",
            valid_names.join(", ")
        )));
    }

    Ok(resolved)
}

/// Validate any profile including "common" (required for `make`).
pub fn validate_profile(input: &str) -> Result<Profile, AppError> {
    resolve_profile(input).ok_or_else(|| AppError::InvalidProfile(input.to_string()))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn resolves_canonical_profiles() {
        assert_eq!(resolve_profile("common"), Some(Profile::Common));
        assert_eq!(resolve_profile("macbook"), Some(Profile::Macbook));
        assert_eq!(resolve_profile("mac-mini"), Some(Profile::MacMini));
    }

    #[test]
    fn resolves_aliases() {
        assert_eq!(resolve_profile("mbk"), Some(Profile::Macbook));
        assert_eq!(resolve_profile("mmn"), Some(Profile::MacMini));
        assert_eq!(resolve_profile("cmn"), Some(Profile::Common));
    }

    #[test]
    fn rejects_unknown() {
        assert_eq!(resolve_profile("desktop"), None);
    }

    #[test]
    fn validate_machine_profile_rejects_common() {
        assert!(validate_machine_profile("common").is_err());
    }

    #[test]
    fn validate_machine_profile_accepts_macbook() {
        assert_eq!(validate_machine_profile("macbook").unwrap(), Profile::Macbook);
        assert_eq!(validate_machine_profile("mbk").unwrap(), Profile::Macbook);
    }
}
