//! Version source adapter contracts.

use mev::domain::ports::version_source::VersionSource;

#[test]
fn pipx_version_source_returns_current() {
    let source = mev::adapters::version_source::pipx::PipxVersionSource;
    let version = source.current_version().unwrap();
    assert_eq!(version, env!("CARGO_PKG_VERSION"));
}

#[test]
fn pipx_version_source_satisfies_port_trait() {
    let source = mev::adapters::version_source::pipx::PipxVersionSource;
    let source_ref: &dyn VersionSource = &source;
    let version = source_ref.current_version().unwrap();
    assert_eq!(version, env!("CARGO_PKG_VERSION"));
}
