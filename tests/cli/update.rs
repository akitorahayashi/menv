//! CLI contract tests for the `update` command.

use crate::harness::TestContext;
use predicates::prelude::*;

#[test]
fn update_prints_current_version() {
    let ctx = TestContext::new();

    // Update prints current version even when pipx upgrade cannot run in test env.
    ctx.cli()
        .arg("update")
        .assert()
        .failure()
        .stdout(predicate::str::contains("Current version"))
        .stdout(predicate::str::contains("Running upgrade..."))
        .stderr(predicate::str::contains("Error: update failed"));
}

#[test]
fn update_alias_u_is_accepted() {
    let ctx = TestContext::new();

    ctx.cli()
        .arg("u")
        .assert()
        .failure()
        .stdout(predicate::str::contains("Current version"))
        .stderr(predicate::str::contains("Error: update failed"));
}
