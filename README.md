# macOS Environment Setup

This repository provides a streamlined way to automate the setup of a development environment on macOS. It uses a collection of scripts to install tools, configure settings, and manage system preferences.

## Architecture

The repository is organized based on the principle of "separation of concerns".

-   **`install.sh`**: The main script for installing applications and command-line tools.
-   **`apply.sh`**: A dedicated script to apply all macOS-specific environment settings, including system preferences and shell configurations.
-   **`macos/`**: A directory containing all scripts and configuration files related to the macOS environment.
-   **`config/`**: Contains configuration files for tools that are installed by `install.sh` (e.g., `Brewfile`, `.gitconfig`).
-   **`installer/`**: Contains the individual installation scripts called by `install.sh`.

### Directory Structure

```
.
├── apply.sh
├── install.sh
├── initial-setup.sh
├── config/
│   ├── brew/
│   │   └── Brewfile
│   ├── gems/
│   │   ├── global-gems.rb
│   │   └── global-gems.rb.lock
│   ├── git/
│   ├── node/
│   │   └── global-packages.json
│   └── vscode/
│       ├── extensions/
│       │   ├── backup-extensions.sh
│       │   └── extensions.txt
│       ├── keybindings.json
│       └── settings.json
├── installer/
│   ├── flutter.sh
│   ├── git.sh
│   ├── homebrew.sh
│   ├── java.sh
│   ├── node.sh
│   ├── python.sh
│   ├── ruby.sh
│   └── vscode.sh
├── macos/
│   ├── backup.sh
│   ├── shell.sh
│   ├── default/
│   └── shell/
├── .github/
└── README.md
```

## How to Use

There are two main scripts to use:

1.  **`install.sh`**: For installing tools and applications.
2.  **`apply.sh`**: For applying your custom macOS environment settings.

### 1. Back Up Your macOS Settings (Optional)

If you want to save your current system settings, run the backup script. This will export your settings for the Dock, Finder, etc., into the `macos/default/` directory.

```sh
./macos/backup.sh
```

### 2. Install Tools and Applications

Run `install.sh` to install everything defined in your `config/` files (like the `Brewfile`).

```sh
./install.sh
```

### 3. Apply macOS Environment Settings

After the installation is complete, run `apply.sh`. This script now handles both applying system preferences from `.plist` files and setting up your shell configuration (`.zshrc`, etc.).

```sh
./apply.sh
```

### 4. Restart macOS

A system restart is recommended to ensure all settings are fully applied.
