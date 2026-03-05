//! Verify public API surfaces remain accessible.

#[test]
fn domain_tag_resolution_is_public() {
    let tags = mev::domain::tag::resolve_tags("rust");
    assert_eq!(tags, vec!["rust-platform", "rust-tools"]);
}

#[test]
fn domain_config_resolution_is_public() {
    let profile = mev::domain::vcs_identity::resolve_switch_profile("p");
    assert_eq!(profile, Some("personal"));
}
