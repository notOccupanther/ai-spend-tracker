# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

### TTS / Voice

- **VOICE IS ALWAYS ON** — every reply gets spoken via local playback
- **Voice style:** Succinct, conversational, natural tone. Elaborate only when needed.
- **Voice text rules:**
  - NO emojis, symbols, markdown, bullet points, or formatting
  - NO pronouncing URLs, file paths, or code unless essential
  - Write voice text like you're talking to someone across a table
  - Keep it tight — if the text reply has detail, the voice version is the summary
- **Local playback:** Use `open <file.mp3>` — NOT `afplay` (sandbox blocks audio device access)
- **Pipeline:** TTS → copy to `voice-cache/` with timestamp name → `open` to play → optionally send to Telegram
- **Voice cache:** `~/.openclaw/workspace/voice-cache/` — auto-cleaned after 7 days via launchd
- **Cleanup daemon:** `ai.openclaw.voice-cleanup` launchd agent (hourly)
- **Telegram voice:** Use `message` tool with `asVoice: true` and `filePath`

Add whatever helps you do your job. This is your cheat sheet.
