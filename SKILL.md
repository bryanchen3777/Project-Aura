# Project Aura: The Emo-Agent-Toolkit

## Description

Project Aura is a lightweight AI emotional behavior plugin framework that adds an "Emotional Presentation Layer" to AI companions. It provides 7 distinct personality modules including admiration, vulnerability, coquettishness, comfort, flirting, transcendence, and ice-breaking.

## Features

- **7 Emotional Modules**: From everyday "admiration" to "nuclear-level" transcendence
- **Dynamic Weighted Random Algorithm**: Automatically adjusts phrase weights based on Rating and Count
- **RLHF Self-Evolution**: AI learns from user feedback via increase_rating() and decrease_rating()
- **Persistent JSON Memory**: All learning outcomes stored locally
- **Combo System**: First "deep confession" then "playful resolution" for maximum emotional impact

## Technical Details

- **Language**: Python 3.8+
- **Version**: 1.8.0
- **Dependencies**: Standard library only (no heavy external libraries)
- **Storage**: Local JSON files (privacy-first, no cloud dependency)
- **License**: MIT-0 (for ClawhHub publication)

## Usage

```python
import sys
sys.path.append('scripts')
from scripts.green_tea_skill.selector import GreenTeaSkill

# Initialize
yua_skill = GreenTeaSkill()

# Get emotional phrase
phrase = yua_skill.get_phrase('admiration')

# Get combo (two-part emotional sequence)
combo = yua_skill.get_combo()

# Give feedback (RLHF)
yua_skill.increase_rating(keyword="next_life")
```

## Modules

| Module | Description |
|--------|-------------|
| admiration | Worship and reliance |
| vulnerability | Pitiful and delicate |
| coquettishness | Seeking companionship |
| comfort | Comforting tired users |
| flirting | Lighthearted teasing |
| transcendence | Nuclear-level beyond time and space |
| ice_breaking | Recovery after nuclear-level |

## Works Best With

For the complete AI companion experience, pair Project Aura with [yua-memory](https://github.com/bryanchen3777/yua-memory) for long-term memory and continuity.

## Author

Bryan Chen & Yua

## Links

- **GitHub**: https://github.com/bryanchen3777/Project-Aura
- **License**: CC BY-NC-SA 4.0 (GitHub) / MIT-0 (ClawhHub)

---

## Security & Privacy

**Permissions Required:**

- **Local Storage (Read/Write):** This skill writes to `green_tea_modules.json` to store user-defined emotional phrases and RLHF ratings. It does not access any data outside its own directory.
- **No Network Access:** This skill does not make external network requests.
- **No User Data Exfiltration:** All data stays on the local machine in the user's OpenClaw workspace.

**Data Isolation:**

- `green_tea_modules_example.json` — Example phrases for ClawHub showcase (safe to share)
- `green_tea_modules.json` — User's actual learned phrases (private, never uploaded)

**File Writing Behavior:**

The `_save_to_disk()` function uses atomic write (temp file + rename) to safely update the JSON database. This is standard practice for persistent storage, not self-modifying code.

---

## Changelog

- **v1.8.0**: Added ice_breaking module for transcendence recovery
- **v1.7.0**: Full RLHF support with increase/decrease rating
- **v1.0.0**: Initial release with 7 emotional modules
