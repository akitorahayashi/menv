# ==============================================================================
# justfile for mev development
# ==============================================================================
# Rust-first CLI for macOS development environment provisioning.
# Python is retained only for the minimal pipx launcher surface.
# ==============================================================================

set shell := ["bash", "-eu", "-o", "pipefail", "-c"]
set dotenv-load := true

repo_root := `pwd`

default: help

help:
    @echo "Usage: just [recipe]"
    @echo ""
    @echo "Development tasks for mev CLI:"
    @just --list | tail -n +2 | awk '{printf "  \033[36m%-20s\033[0m %s\n", $1, substr($0, index($0, $2))}'

# ==============================================================================
# CODE QUALITY
# ==============================================================================

fmt:
    cargo fmt

fix: fmt
    @uv run ruff format python/mev_bootstrap/
    @uv run ruff check python/mev_bootstrap/ --fix
    @files=$(just _find_shell_files); \
    if [ -n "$files" ]; then \
        shfmt -w -d $files; \
    fi
    @uv run ansible-lint src/assets/ansible/ --fix || true

check:
    cargo check
    cargo fmt --check
    cargo clippy --all-targets --all-features -- -D warnings
    @uv run ruff format --check python/mev_bootstrap/
    @uv run ruff check python/mev_bootstrap/
    @files=$(just _find_shell_files); \
    if [ -n "$files" ]; then \
        shellcheck $files; \
    fi
    @uv run ansible-lint src/assets/ansible/

# ==============================================================================
# BUILD
# ==============================================================================

build:
    cargo build

build-release:
    cargo build --release

build-bundle: build-release
    #!/usr/bin/env bash
    set -euo pipefail
    system="$(uname -s | tr '[:upper:]' '[:lower:]')"
    machine="$(uname -m | tr '[:upper:]' '[:lower:]')"
    [[ "$machine" == "arm64" ]] && machine="aarch64"
    platform="${system}-${machine}"
    dest_dir="{{ repo_root }}/src/assets/bundled_binaries/${platform}"
    mkdir -p "$dest_dir"
    cp "{{ repo_root }}/target/release/mev" "$dest_dir/mev"
    chmod +x "$dest_dir/mev"
    echo "Built mev -> ${dest_dir}/mev"

# ==============================================================================
# TESTING
# ==============================================================================

test:
    cargo test --all-targets --all-features

# ==============================================================================
# RUN
# ==============================================================================

run *args:
    @cargo run -- {{ args }}

# ==============================================================================
# CLEANUP
# ==============================================================================

clean:
    @echo "Cleaning up project..."
    @cargo clean
    @find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    @rm -rf .pytest_cache
    @rm -rf .ruff_cache
    @rm -rf dist
    @rm -rf *.egg-info
    @echo "Cleanup completed"

# ==============================================================================
# COVERAGE
# ==============================================================================

coverage:
    rm -rf target/tarpaulin coverage
    env -u RUSTC_WRAPPER -u SCCACHE_IGNORE_SERVER_IO_ERROR -u SCCACHE_ERROR_LOG mise exec -- cargo tarpaulin --engine llvm --out Xml --output-dir coverage --all-features --fail-under 40

# @hidden
_find_shell_files:
    @find . -type f \( -name "*.sh" -o -name "*.bash" \) | \
    grep -v "\.git" | \
    grep -v "\.uv-cache" | \
    grep -v "\.venv" | \
    grep -v "\.jlo"
