# statusline

Enhanced status line for Claude Code showing token usage and burn rate.

## What it does

```
[Opus 4.6] | 🌿 main M1 +1 | 📁 statusline | 💬 170 | 💰 $0.044
🚨  Compact: █████████████████▒▒▒ [89%] ⚠️ 178.0K/200.0K ♻️  99% cached
🔥 Burn:    ▁▁█▂▁▁▅▄▁▁▁▁▁▁▁▁▁▁▁▁ 8,387,710 token(w/cache), Rate: 75,515 t/m
```

- **Line 1**: Model, git status, directory, message count, cost
- **Line 2**: Context window usage vs total (200K) with 85%+ warning
- **Line 3**: Session time (disabled by default — local estimate only, not actual Anthropic rate limit)
- **Line 4**: Real-time burn rate with 15-minute segment sparkline

## Key Features

### 🚨 85% Warning System
When context window usage reaches 85% of the total (170K/200K):
- Icon changes from 🪙 to 🚨
- Red background warning appears
- Percentage display includes ⚠️ symbol

### 🔥 Real-Time Burn Sparkline
- Each character represents a 15-minute time segment
- Height shows actual token usage during that period
- Based on real message timestamps from transcript files
- Empty segments (▁) indicate periods with no activity

## Installation

```bash
git clone https://github.com/usedhonda/statusline.git
cd statusline
python3 install.py
```

Restart Claude Code. Done.


## Requirements

- Python 3.7+
- Claude Code

## Configuration

### Display Options

You can customize which lines to display in two ways:

#### 1. File Configuration (Default Settings)
Edit the top of `statusline.py`:
```python
# Set which lines to display (True = show, False = hide)
SHOW_LINE1 = True    # [Opus 4.6] | 🌿 main M2 +1 | 📁 statusline | 💬 254 | 💰 $0.031
SHOW_LINE2 = True    # 🪙  Compact: ████████▒▒▒▒▒▒▒ [58%] 116.0K/200.0K ♻️  99% cached
SHOW_LINE3 = False   # ⏱️  Session (disabled — local estimate only)
SHOW_LINE4 = True    # 🔥 Burn:    ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁ 0 token(w/cache), Rate: 0 t/m
```

#### 2. Claude Code Settings (Runtime Override)
Use the statusline script in your active Claude config directory (`CLAUDE_CONFIG_DIR`, default `~/.claude`).

```json
{
  "statusLine": {
    "type": "command",
    "command": "/path/to/your/claude-config-dir/statusline.py"
  }
}
```

Available command options:
```json
// Show specific lines
"command": "/path/to/your/claude-config-dir/statusline.py --show 1,2"
"command": "/path/to/your/claude-config-dir/statusline.py --show 2,4"

// Quick presets
"command": "/path/to/your/claude-config-dir/statusline.py --show simple"  // Lines 2,4 only
"command": "/path/to/your/claude-config-dir/statusline.py --show all"     // All lines (default)

// Help (command line only)
/path/to/your/claude-config-dir/statusline.py --help
```

**Priority**: Command line options override file settings when specified.

### Other Configuration

Errors logged to `<claude-config-dir>/statusline-error.log`

Optional environment variables:
```bash
export CLAUDE_CONFIG_DIR="~/.claude-acc2"   # Use a different Claude profile/config dir
export CLAUDE_PROJECTS_DIR="/custom/path"    # Optional override for transcript lookup
export STATUSLINE_NO_COLOR=1  # Disable colors
```