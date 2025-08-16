#!/bin/bash
set -euo pipefail

# This script ensures that configuration directories and placeholder files
# exist for a given machine type, making the CI matrix robust.

if [ $# -ne 1 ]; then
    echo "Usage: $0 <machine-type>"
    echo "Example: $0 macbook"
    exit 1
fi

MACHINE_TYPE=$1
CONFIG_BASE_DIR="$(dirname "$0")/../config"
MACHINE_CONFIG_DIR="$CONFIG_BASE_DIR/$MACHINE_TYPE"

COMPONENTS=(
    "brew:Brewfile"
    "git:.gitconfig .gitignore_global"
    "node:.nvmrc global-packages.json"
    "python:.python-version pipx-tools.txt"
    "ruby:.ruby-version global-gems.rb"
    "vscode:settings.json keybindings.json"
    "java:.gitkeep" # No specific configs, just ensure dir exists
    "flutter:.gitkeep" # No specific configs, just ensure dir exists
)

echo "--- Ensuring configurations for '$MACHINE_TYPE' ---"

for entry in "${COMPONENTS[@]}"; do
    component="${entry%%:*}"
    files="${entry#*:}"

    component_dir="$MACHINE_CONFIG_DIR/$component"

    if [ ! -d "$component_dir" ]; then
        echo "[CREATE] Directory: $component_dir"
        mkdir -p "$component_dir"
    else
        echo "[EXISTS] Directory: $component_dir"
    fi

    for file in $files; do
        file_path="$component_dir/$file"
        if [ ! -f "$file_path" ]; then
            echo "[CREATE] Placeholder file: $file_path"
            # Create empty JSON files for node to avoid jq errors
            if [[ "$file" == *.json ]]; then
                echo "{}" > "$file_path"
            else
                touch "$file_path"
            fi
        else
            echo "[EXISTS] File: $file_path"
        fi
    done
done

echo "--- Configuration check complete for '$MACHINE_TYPE' ---"
