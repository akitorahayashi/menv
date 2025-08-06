#!/bin/bash
set -euo pipefail

#
# apply.sh
#
# Description:
#   This script applies macOS system settings from the macos/default directory.
#
# Usage:
#   ./macos/apply.sh
#

# ---
# SETTINGS_DIR
#
# Directory where the settings files are stored.
# ---
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
SETTINGS_DIR="$SCRIPT_DIR/macos/default"

# ---
# Main processing
# ---
main() {
  echo "Starting macOS settings import..."

  # Find all .plist files in the settings directory
  find "$SETTINGS_DIR" -name "*.plist" | while read -r plist_file; do
    domain=$(basename "$plist_file" .plist)
    echo "  -> Importing settings for '$domain'..."
    defaults import "$domain" - < "$plist_file"
  done

  echo "Settings import complete."
  echo "Note: Some settings may require a restart to take effect."
}

# ---
# Execute main function
# ---
main
