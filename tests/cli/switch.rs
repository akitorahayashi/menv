//! CLI contract tests for the `switch` command.

use crate::harness::TestContext;
use predicates::prelude::*;

#[test]
fn switch_help_shows_profile_argument() {
    let ctx = TestContext::new();
    ctx.cli()
        .args(["switch", "--help"])
        .assert()
        .success()
        .stdout(predicate::str::contains("profile"));
}

#[test]
fn switch_alias_sw_is_accepted() {
    let ctx = TestContext::new();
    ctx.cli().args(["sw", "--help"]).assert().success().stdout(predicate::str::contains("profile"));
}

#[test]
fn switch_requires_profile_argument() {
    let ctx = TestContext::new();
    ctx.cli().arg("switch").assert().failure().stderr(predicate::str::contains("profile"));
}

#[test]
fn switch_rejects_unknown_profile() {
    let ctx = TestContext::new();
    ctx.cli()
        .args(["switch", "invalid"])
        .assert()
        .failure()
        .stderr(predicate::str::contains("invalid"));
}

#[test]
fn switch_help_visible_in_main_help() {
    let ctx = TestContext::new();
    ctx.cli()
        .arg("--help")
        .assert()
        .success()
        .stdout(predicate::str::contains("switch"))
        .stdout(predicate::str::contains("sw"));
}
