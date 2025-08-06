# macOS Environment Setup

This repository provides a streamlined way to automate the setup of a development environment on macOS. It uses a collection of scripts to install tools, configure settings, and manage system preferences.

## Architecture

The repository is organized based on the principle of "separation of concerns".

-   **`install.sh`**: The main script for installing applications and command-line tools.
-   **`apply.sh`**: A dedicated script to apply macOS-specific system settings.
-   **`macos/backup.sh`**: A script to back up your current macOS settings.
-   **`config/`**: Contains configuration files for various tools (e.g., `Brewfile`, `.gitconfig`).
-   **`installer/`**: Contains the individual scripts that are called by `install.sh`.
-   **`macos/default/`**: Stores the backed-up macOS settings as `.plist` files.

### Directory Structure

```
.
├── apply.sh              # Applies macOS system settings
├── install.sh            # Installs tools and applications
│
├── config/               # Configuration files for tools and shells
│   ├── brew/
│   │   └── Brewfile
│   └── ...
│
├── installer/            # Scripts to install tools and apply settings
│   ├── brew.sh
│   └── ...
│
├── macos/                # Manages macOS-specific settings
│   ├── backup.sh         # Script to export all system settings
│   └── default/          # Stores exported settings as *.plist files
│       ├── com.apple.dock.plist
│       └── ...
│
├── .github/
└── README.md
```

## How to Use

There are two main scripts to use:

1.  **`install.sh`**: For installing tools and applications.
2.  **`apply.sh`**: For applying your custom macOS settings.

### 1. Back Up Your macOS Settings (Optional)

If you want to save your current system settings, run the backup script. This will export your settings for the Dock, Finder, etc., into the `macos/default/` directory.

```sh
./macos/backup.sh
```

### 2. Install Tools and Applications

Run the `install.sh` script to install everything defined in your `config/` files (like the `Brewfile`).

```sh
./install.sh
```

This script handles the installation of:
- Homebrew and command-line tools
- Packages, casks, and App Store apps
- Shell, Git, VS Code, Ruby, Python, Node.js, etc.

### 3. Apply macOS Settings

After the installation is complete, run `apply.sh` to configure your macOS system settings based on the files in `macos/default/`.

```sh
./apply.sh
```

### 4. Restart macOS

A system restart is recommended to ensure all settings are fully applied.
