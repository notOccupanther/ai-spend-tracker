#!/bin/bash
# OpenClaw Backup Script - Full system state backup
# Usage: ./backup-openclaw.sh [destination_path]

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="openclaw-backup-$TIMESTAMP"
DEST_DIR="${1:-$HOME/Desktop}"
BACKUP_PATH="$DEST_DIR/$BACKUP_NAME"

echo "🌀 OpenClaw Backup Starting..."
echo "📁 Backup location: $BACKUP_PATH"

# Create backup directory
mkdir -p "$BACKUP_PATH"

# 1. OpenClaw Configuration
echo "📋 Backing up OpenClaw config..."
cp ~/.openclaw/openclaw.json "$BACKUP_PATH/" 2>/dev/null || echo "⚠️  Config file not found"

# 2. Full Workspace (projects, memory, scripts, etc.)
echo "📁 Backing up workspace..."
if [ -d ~/.openclaw/workspace ]; then
    cp -r ~/.openclaw/workspace "$BACKUP_PATH/"
else
    echo "⚠️  Workspace not found"
fi

# 3. LaunchAgents (voice cleanup daemon)
echo "🤖 Backing up LaunchAgents..."
mkdir -p "$BACKUP_PATH/LaunchAgents"
cp ~/Library/LaunchAgents/ai.openclaw.* "$BACKUP_PATH/LaunchAgents/" 2>/dev/null || echo "ℹ️  No OpenClaw LaunchAgents found"

# 4. System Info
echo "💻 Capturing system info..."
{
    echo "# OpenClaw Backup System Info"
    echo "Date: $(date)"
    echo "macOS: $(sw_vers -productVersion)"
    echo "OpenClaw: $(openclaw --version 2>/dev/null || echo 'not found')"
    echo "Node: $(node --version 2>/dev/null || echo 'not found')"
    echo "Homebrew packages:"
    brew list 2>/dev/null | grep -E "(hugo|whisper|node)" || echo "brew not available"
    echo ""
    echo "# Git Repos in Workspace"
    find ~/.openclaw/workspace -type d -name ".git" | sed 's/.git$//' 2>/dev/null
} > "$BACKUP_PATH/system-info.txt"

# 5. Installed Skills (just the list)
echo "🧩 Recording installed skills..."
ls /opt/homebrew/lib/node_modules/openclaw/skills/ > "$BACKUP_PATH/installed-skills.txt" 2>/dev/null || echo "Skills directory not found"

# 6. Create restore instructions
cat > "$BACKUP_PATH/RESTORE.md" << 'EOF'
# OpenClaw Restore Instructions

## Full Restore
1. Restore `openclaw.json` to `~/.openclaw/`
2. Restore `workspace/` folder to `~/.openclaw/workspace/`
3. Restore LaunchAgents to `~/Library/LaunchAgents/` and load them:
   ```bash
   launchctl load ~/Library/LaunchAgents/ai.openclaw.*
   ```
4. Reinstall packages from system-info.txt if needed

## Partial Restore
- **Projects only:** Copy specific folders from `workspace/projects/`
- **Memory only:** Copy `workspace/memory/` and `workspace/MEMORY.md`
- **Config only:** Copy `openclaw.json`

## Notes
- API keys are included in the config (keep secure!)
- Voice cache is excluded (temporary files)
- Git repos should be re-cloned or pushed to remotes first
EOF

# 7. Compress the backup
echo "🗜️  Compressing backup..."
cd "$DEST_DIR"
tar -czf "$BACKUP_NAME.tar.gz" "$BACKUP_NAME"
rm -rf "$BACKUP_NAME"

echo "✅ Backup complete!"
echo "📦 File: $DEST_DIR/$BACKUP_NAME.tar.gz"
echo "📏 Size: $(du -h "$DEST_DIR/$BACKUP_NAME.tar.gz" | cut -f1)"