#!/bin/bash
# Voice file cleanup — deletes TTS temp files older than 1 hour
# Run via cron or launchd

# Clean OpenClaw TTS temp files
find /var/folders -name "voice-*.opus" -mmin +60 -delete 2>/dev/null
find /var/folders -name "voice-*.ogg" -mmin +60 -delete 2>/dev/null
find /var/folders -name "voice-*.mp3" -mmin +60 -delete 2>/dev/null

# Clean local voice cache older than 7 days
find /Users/clancynl/.openclaw/workspace/voice-cache -name "*.opus" -mtime +7 -delete 2>/dev/null
find /Users/clancynl/.openclaw/workspace/voice-cache -name "*.ogg" -mtime +7 -delete 2>/dev/null
find /Users/clancynl/.openclaw/workspace/voice-cache -name "*.mp3" -mtime +7 -delete 2>/dev/null

echo "$(date): Voice cleanup complete"
