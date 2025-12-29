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

**Provision your environment:**

```sh
# For MacBook
menv create macbook
# or shorthand:
menv cr macbook

# For Mac mini
menv create mac-mini
# or shorthand:
menv cr mac-mini
```

**Run specific tags only:**

```sh
menv create macbook --tags shell,python,rust
```

**Update menv:**

```sh
menv update
# or shorthand:
menv u
```

**Show help:**

```sh
menv --help
menv create --help
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
just run create macbook

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
│   │   ├── create.py     # create/cr command
│   │   └── update.py     # update/u command
│   ├── core/
│   │   ├── paths.py      # Package path resolution
│   │   ├── runner.py     # Ansible execution wrapper
│   │   └── version.py    # Version management
│   └── ansible/          # Ansible playbooks and roles
│       ├── playbook.yml
│       └── roles/
├── tests/
├── justfile              # Development tasks
└── pyproject.toml
```

## License

MIT
