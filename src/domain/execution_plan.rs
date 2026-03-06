//! Deterministic ansible execution plan construction.

use crate::domain::profile::Profile;

/// An execution plan describes the ordered sequence of ansible tags to run.
#[derive(Debug, Clone)]
pub struct ExecutionPlan {
    pub profile: Profile,
    pub tags: Vec<String>,
    pub verbose: bool,
}

impl ExecutionPlan {
    /// Construct a plan for a full environment creation.
    pub fn full_setup(profile: Profile, verbose: bool) -> Self {
        let tags = crate::domain::tag::FULL_SETUP_TAGS.iter().map(|s| (*s).to_string()).collect();
        Self { profile, tags, verbose }
    }

    /// Construct a plan for a single make invocation.
    pub fn make(profile: Profile, tags: Vec<String>, verbose: bool) -> Self {
        Self { profile, tags, verbose }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::domain::tag::FULL_SETUP_TAGS;

    #[test]
    fn execution_plan_full_setup() {
        let plan = ExecutionPlan::full_setup(Profile::Macbook, true);
        assert_eq!(plan.profile, Profile::Macbook);
        assert!(plan.verbose);
        assert_eq!(plan.tags.len(), FULL_SETUP_TAGS.len());
        assert_eq!(plan.tags[0], FULL_SETUP_TAGS[0]);
    }

    #[test]
    fn execution_plan_make() {
        let plan = ExecutionPlan::make(Profile::Common, vec!["shell".to_string()], false);
        assert_eq!(plan.profile, Profile::Common);
        assert!(!plan.verbose);
        assert_eq!(plan.tags, vec!["shell".to_string()]);
    }
}
