#!/bin/bash
set -euo pipefail

#
# macos/backup.sh
#
# Description:
#   This script backs up macOS system settings to the macos/default directory.
#
# Usage:
#   ./macos/backup.sh
#

# ---
# DOMAINS_TO_BACKUP
#
# List of domains to be backed up.
# Note: Application settings are not included, only system behavior settings.
# ---
DOMAINS_TO_BACKUP=(
  ".GlobalPreferences_m"
  "com.apple.dock"
  "com.apple.finder"
  "com.apple.systemuiserver"
  "com.apple.screencapture"
  "com.apple.screensaver"
  "com.apple.symbolichotkeys"
  "com.apple.controlcenter"
  "com.apple.spaces"
  "com.apple.AppleMultitouchTrackpad"
  "com.apple.driver.AppleBluetoothMultitouch.trackpad"
  "com.apple.AppleMultitouchMouse"
  "com.apple.driver.AppleBluetoothMultitouch.mouse"
  "com.apple.HIToolbox"
  "com.apple.notificationcenterui"
)

# ---
# BACKUP_DIR
#
# Directory to store the backup files.
# ---
BACKUP_DIR="$(dirname "$0")/default"

# ---
# Main processing
# ---
main() {
  # Ensure backup directory exists
  mkdir -p "$BACKUP_DIR"

  # Clear existing backup files
  echo "Clearing old backup files from $BACKUP_DIR..."
  rm -f "$BACKUP_DIR"/*.plist
  echo "Old files cleared."
  echo ""

  # Export settings for each domain
  echo "Starting macOS settings backup..."
  for domain in "${DOMAINS_TO_BACKUP[@]}"; do
    echo "  -> Backing up '$domain'..."
    defaults export "$domain" - > "$BACKUP_DIR/$domain.plist"
  done
  echo "Backup complete."
}

# ---
# Execute main function
# ---
main
