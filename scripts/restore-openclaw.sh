#!/bin/bash
# OpenClaw Restore Script
# Usage: ./restore-openclaw.sh backup.tar.gz

if [ -z "$1" ]; then
    echo "Usage: $0 <backup.tar.gz>"
    exit 1
fi

BACKUP_FILE="$1"
TEMP_DIR="/tmp/openclaw-restore-$$"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "🌀 OpenClaw Restore Starting..."
echo "📦 From: $BACKUP_FILE"

# Extract backup
echo "📁 Extracting backup..."
mkdir -p "$TEMP_DIR"
tar -xzf "$BACKUP_FILE" -C "$TEMP_DIR"

BACKUP_DIR=$(ls "$TEMP_DIR" | head -1)
BACKUP_PATH="$TEMP_DIR/$BACKUP_DIR"

if [ ! -d "$BACKUP_PATH" ]; then
    echo "❌ Invalid backup structure"
    exit 1
fi

# Confirm before overwriting
echo ""
echo "This will restore:"
[ -f "$BACKUP_PATH/openclaw.json" ] && echo "  ✓ OpenClaw configuration"
[ -d "$BACKUP_PATH/workspace" ] && echo "  ✓ Full workspace ($(du -sh "$BACKUP_PATH/workspace" | cut -f1))"
[ -d "$BACKUP_PATH/LaunchAgents" ] && echo "  ✓ LaunchAgents"
echo ""
read -p "Continue? (y/N): " confirm
if [[ ! $confirm =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    rm -rf "$TEMP_DIR"
    exit 0
fi

# Create backup of current state
if [ -d ~/.openclaw ]; then
    echo "💾 Backing up current state..."
    mv ~/.openclaw ~/.openclaw.backup.$(date +%s)
fi

# Restore configuration
echo "📋 Restoring configuration..."
mkdir -p ~/.openclaw
[ -f "$BACKUP_PATH/openclaw.json" ] && cp "$BACKUP_PATH/openclaw.json" ~/.openclaw/

# Restore workspace
echo "📁 Restoring workspace..."
[ -d "$BACKUP_PATH/workspace" ] && cp -r "$BACKUP_PATH/workspace" ~/.openclaw/

# Restore LaunchAgents
echo "🤖 Restoring LaunchAgents..."
if [ -d "$BACKUP_PATH/LaunchAgents" ]; then
    cp "$BACKUP_PATH/LaunchAgents"/* ~/Library/LaunchAgents/ 2>/dev/null
    for agent in ~/Library/LaunchAgents/ai.openclaw.*; do
        [ -f "$agent" ] && launchctl load "$agent"
    done
fi

# Cleanup
rm -rf "$TEMP_DIR"

echo "✅ Restore complete!"
echo "ℹ️  You may need to:"
echo "   - Restart OpenClaw gateway: openclaw gateway restart"
echo "   - Verify API keys are working"
echo "   - Re-authenticate with GitHub if needed"