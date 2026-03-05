//! `list` command orchestration — display tags, groups, and profiles.

use crate::app::AppContext;
use crate::domain::error::AppError;
use crate::domain::ports::ansible::AnsiblePort;
use crate::domain::profile::{PROFILE_ALIASES, VALID_PROFILES};
use crate::domain::tag;

/// Execute the `list` command: print tags, groups, and profiles.
pub fn execute(ctx: &AppContext) -> Result<(), AppError> {
    let tags_map = ctx.ansible.tags_by_role();

    // Role → tags table
    println!("Available Tags");
    println!("{:<20} Tags", "Role");
    println!("{:-<20} {:-<40}", "", "");
    let mut roles: Vec<_> = tags_map.iter().collect();
    roles.sort_by_key(|(name, _)| (*name).clone());
    for (role, tags) in &roles {
        println!("{:<20} {}", role, tags.join(", "));
    }
    println!();

    // Tag groups
    println!("Tag Groups (expanded automatically):");
    let groups = tag::tag_groups();
    let mut group_keys: Vec<_> = groups.keys().collect();
    group_keys.sort();
    for key in group_keys {
        let tags = &groups[key];
        println!("  {key} → {}", tags.join(", "));
    }
    println!();

    // Profiles
    let mut profiles_to_show = Vec::new();
    if VALID_PROFILES.contains(&crate::domain::profile::Profile::Common) {
        profiles_to_show.push(crate::domain::profile::Profile::Common);
    }
    for &p in VALID_PROFILES {
        if p != crate::domain::profile::Profile::Common {
            profiles_to_show.push(p);
        }
    }

    let mut profile_strs = Vec::new();
    for p in &profiles_to_show {
        let aliases: Vec<&str> = PROFILE_ALIASES
            .iter()
            .filter(|(_, target)| target == p)
            .map(|(alias, _)| *alias)
            .collect();
        let alias_str =
            if aliases.is_empty() { String::new() } else { format!(" ({})", aliases.join(", ")) };
        let suffix = if *p == crate::domain::profile::Profile::Common { " (default)" } else { "" };
        profile_strs.push(format!("{}{alias_str}{suffix}", p.as_str()));
    }
    println!("Profiles: {}", profile_strs.join(", "));

    Ok(())
}
