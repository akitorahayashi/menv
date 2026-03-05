//! VCS identity model and switch profile resolution.
//!
//! `VcsIdentity` is a mev-specific concept: it represents the name/email pair
//! stored per profile (personal / work) and applied to Git and Jujutsu.

/// Name and email pair applied to global VCS configuration.
#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct VcsIdentity {
    pub name: String,
    pub email: String,
}

/// Canonical switch profile identifiers and their input aliases.
pub const SWITCH_PROFILES: &[(&str, SwitchProfile)] = &[
    ("p", SwitchProfile::Personal),
    ("personal", SwitchProfile::Personal),
    ("w", SwitchProfile::Work),
    ("work", SwitchProfile::Work),
];

/// Strong type for VCS identity switch profiles.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SwitchProfile {
    Personal,
    Work,
}

impl SwitchProfile {
    pub fn as_str(&self) -> &'static str {
        match self {
            SwitchProfile::Personal => "personal",
            SwitchProfile::Work => "work",
        }
    }
}

impl std::fmt::Display for SwitchProfile {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.as_str())
    }
}

/// Resolve a switch profile input (alias or canonical) to its canonical enum variant.
pub fn resolve_switch_profile(input: &str) -> Option<SwitchProfile> {
    let lower = input.to_lowercase();
    for &(alias, canonical) in SWITCH_PROFILES {
        if lower == alias {
            return Some(canonical);
        }
    }
    None
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn resolves_switch_profiles() {
        assert_eq!(resolve_switch_profile("p"), Some(SwitchProfile::Personal));
        assert_eq!(resolve_switch_profile("personal"), Some(SwitchProfile::Personal));
        assert_eq!(resolve_switch_profile("w"), Some(SwitchProfile::Work));
        assert_eq!(resolve_switch_profile("work"), Some(SwitchProfile::Work));
        assert_eq!(resolve_switch_profile("unknown"), None);
    }
}
