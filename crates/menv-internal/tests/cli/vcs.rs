use assert_cmd::Command;
use predicates::prelude::*;

#[test]
fn delete_submodule_rejects_absolute_path() {
    Command::cargo_bin("menv-internal")
        .unwrap()
        .args(["vcs", "delete-submodule", "/absolute/path"])
        .assert()
        .failure()
        .code(1)
        .stderr(predicate::str::contains("Invalid submodule path"));
}

#[test]
fn delete_submodule_rejects_parent_traversal() {
    Command::cargo_bin("menv-internal")
        .unwrap()
        .args(["vcs", "delete-submodule", "../escape/path"])
        .assert()
        .failure()
        .code(1)
        .stderr(predicate::str::contains("Invalid submodule path"));
}
