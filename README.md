# menv

macOS development environment provisioning CLI.

## Quick Start

### Prerequisites

1. **Xcode Command Line Tools**
   ```sh
   xcode-select --install
   ```

2. **Homebrew**
   ```sh
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
   Restart your terminal after installation.

3. **pipx**
   ```sh
   brew install pipx
   pipx ensurepath
   ```
   Restart your terminal after installation.

### Installation

```sh
pipx install git+https://github.com/akitorahayashi/menv.git
```

### Usage

**Interactive setup guide (recommended):**

```sh
# For MacBook
menv introduce macbook
# or shorthand:
menv itr mbk

# For Mac mini
menv introduce mac-mini
# or shorthand:
menv itr mmn
```

The `introduce` command shows an interactive guide with commands you can run in parallel. Open multiple terminals to speed up setup.

**Run individual tasks:**

```sh
# List available tags
menv list
menv ls

# Run specific task
menv make rust              # Run rust-platform + rust-tools
menv make go                # Run go-platform + go-tools
menv make python-tools      # Run python-tools
menv make brew-cask mmn     # Run brew-cask for mac-mini
menv mk shell               # Shorthand

# Tag groups are expanded automatically:
#   rust → rust-platform, rust-tools
#   go → go-platform, go-tools
#   python → python-platform, python-tools
#   nodejs → nodejs-platform, nodejs-tools
```

**Backup commands:**

```sh
menv backup system          # Backup macOS defaults
menv backup vscode          # Backup VSCode extensions
menv bk system              # Shorthand
```

**Configuration:**

```sh
menv config set             # Configure VCS identities interactively
menv config show            # Show current configuration
menv cf set                 # Shorthand
```

**Switch VCS identity:**

```sh
menv switch personal        # Switch to personal identity
menv switch work            # Switch to work identity
menv sw p                   # Shorthand for personal
menv sw w                   # Shorthand for work
```

**Open menv source code:**

```sh
menv code                   # Open menv project in VS Code
```

Clones the menv repository to `~/menv` (if not already present) and opens it in Visual Studio Code. This allows you to edit the menv codebase and create pull requests. Requires SSH access to GitHub to be configured.

**Update menv:**

```sh
menv update
# or shorthand:
menv u
```

**Show help:**

```sh
menv --help
menv introduce --help
menv make --help
```

## Development

### Setup

```sh
# Clone the repository
git clone https://github.com/akitorahayashi/menv.git
cd menv

# Install dependencies
uv sync
```

### Available Commands

```sh
# Run menv in development mode
just run --help
just run introduce macbook

# Run tests
just test

# Format and lint code
just fix
just check

# Build package
just build

# Clean temporary files
just clean
```

### Project Structure

```
menv/
├── src/menv/
│   ├── __init__.py
│   ├── __main__.py       # python -m menv
│   ├── main.py           # Typer app definition
│   ├── commands/
│   │   ├── backup.py     # backup/bk command
│   │   ├── config.py     # config/cf command
│   │   ├── introduce.py  # introduce/itr command (setup guide)
│   │   ├── make.py       # make/mk command (individual tasks)
│   │   ├── switch.py     # switch/sw command
│   │   └── update.py     # update/u command
│   ├── core/
│   │   ├── phases.py          # Setup phase definitions
│   │   └── ...
│   └── ansible/          # Ansible playbooks and roles
│       ├── playbook.yml
│       └── roles/
├── tests/
├── justfile              # Development tasks
└── pyproject.toml
```

## Commands Summary

| Command | Alias | Description |
|---------|-------|-------------|
| `menv introduce <profile>` | `itr` | Interactive setup guide for a profile |
| `menv make <tag> [profile]` | `mk` | Run individual Ansible task |
| `menv list` | `ls` | List available tags |
| `menv backup <target>` | `bk` | Backup system settings |
| `menv config <action>` | `cf` | Manage VCS identities configuration |
| `menv switch <profile>` | `sw` | Switch VCS identity (personal/work) |
| `menv code` | - | Open menv source code in VS Code |
| `menv update` | `u` | Update menv to latest version |
