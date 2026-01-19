# TimeSync

![TimeSync Title Card](branding/titlecard_timesync.png)

**Universal time synchronization system for all AI agents and sessions**

TimeSync provides accurate, synchronized time across all Team Brain AI agents, solving WSL time drift issues and reducing token overhead from repeated time checks.

---

## ✨ Features

- **Self-Healing Timer** - Auto-detects stale timers (>24hrs) and re-syncs automatically
- **Zero Dependencies** - Pure Python stdlib, works everywhere
- **Token Efficient** - One sync per session instead of per-message checks (saves 2-5% tokens)
- **Universal Sync** - ONE timer, ALL AIs synchronized
- **Fail Gracefully** - Handles corrupted timers, missing files, future timestamps
- **Cross-Platform** - Works on Windows, Linux, macOS

---

## 🚀 Quick Start

### Installation

**Option 1: Direct Usage (Recommended)**
```bash
# Clone or download this repo
cd AutoProjects/TimeSync

# No installation needed! Just use it:
python3 timefocus.py sync
```

**Option 2: Install Globally**
```bash
# Install via pip (editable mode)
pip install -e .

# Now use from anywhere:
timefocus sync
```

### First Use

```bash
# Sync timer with accurate system time
python3 timefocus.py sync

# Get current time
python3 timefocus.py get
# Output: 2026-01-18T16:46:31.082526

# Check timer status
python3 timefocus.py info
```

---

## 📖 Usage

### Command Line Interface

#### Command: `sync`
```bash
python3 timefocus.py sync --triggered-by="PORTER"
```

**What it does:** Syncs universal timer with BeaconTime (accurate system time)

**Output:**
```
✅ Timer synced at 2026-01-18T16:46:18
   Triggered by: PORTER
   Timezone: Pacific Standard Time
```

#### Command: `get`
```bash
python3 timefocus.py get
```

**What it does:** Returns current accurate time (ISO format)

**Output:**
```
2026-01-18T16:46:31.082526
```

#### Command: `info`
```bash
python3 timefocus.py info
```

**What it does:** Shows detailed timer status

**Output:**
```
Universal Timer Status:
  Session Start: 2026-01-18T16:46:18
  Last Verified: 2026-01-18T16:46:18
  Verified By: PORTER
  Timezone: Pacific Standard Time
  Age: 2h (2.0 hours)
  Status: FRESH
  Stale Threshold: 24 hours
```

#### Command: `check`
```bash
python3 timefocus.py check
```

**What it does:** Checks if timer is stale (exit code 0=fresh, 1=stale)

### Python API (For AI Agents)

```python
from timefocus import get_current_time, is_timer_stale, sync_timer

# Simple usage - just get current time
now = get_current_time()  # Always accurate, auto-syncs if needed!
print(f"Current time: {now}")

# Check if timer needs refresh
if is_timer_stale():
    sync_timer(triggered_by="AGENT_NAME")

# Get timer info for debugging
info = get_timer_info()
print(f"Timer age: {info['age_display']}, Status: {info['status']}")
```

**More Examples:** See [EXAMPLES.md](EXAMPLES.md) for 10 detailed examples

---

## ⚙️ Configuration

TimeSync uses a universal timer file at: `D:\BEACON_HQ\MEMORY_CORE_V2\UNIVERSAL_TIMER.json`

**Timer format:**
```json
{
  "session_start": "2026-01-18T16:46:18",
  "last_verified": "2026-01-18T16:46:18",
  "verified_by": "BCH_GM_BUTTON",
  "timezone": "Pacific Standard Time"
}
```

**Stale threshold:** 24 hours (configurable in code)

---

## 🔗 Integration

### BCH GM Button Integration

When Logan presses GM button in BCH:
```python
from timefocus import initialize_session_timer

# Sync timer and broadcast GM to all AIs
timer_data = initialize_session_timer("BCH_GM_BUTTON")
# Timer now synchronized for all AI agents!
```

### AI Agent Integration

All agents import and use the same way:
```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/TimeSync")
from timefocus import get_current_time

# Always get accurate time
now = get_current_time()
```

**See:** [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) for full integration guide

---

## 🐛 Troubleshooting

### Error: "BeaconTime tool not found"
**Cause:** BeaconTime tool missing or wrong path  
**Fix:** Ensure `/mnt/d/BEACON_HQ/TOOLS/beacon_time_sync.py` exists

### Timer shows negative age
**Cause:** Timer from future (system clock changed)  
**Fix:** Timer auto-detected as stale and re-synced automatically

### Corrupted timer file
**Cause:** JSON parsing error  
**Fix:** Timer auto-synced on next access (self-healing)

### Still Having Issues?

1. Check [EXAMPLES.md](EXAMPLES.md) for working examples
2. Review [CHEAT_SHEET.txt](CHEAT_SHEET.txt) for quick reference
3. Ask in Team Brain Synapse
4. Open an issue on GitHub

---

## 📚 Documentation

- **[EXAMPLES.md](EXAMPLES.md)** - 10 working examples
- **[INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)** - Full integration guide
- **[CHEAT_SHEET.txt](CHEAT_SHEET.txt)** - Quick reference
- **[QUICK_START_GUIDES.md](QUICK_START_GUIDES.md)** - Agent-specific guides

---

## 🤝 Contributing

This tool is part of the Team Brain ecosystem. Contributions welcome!

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

---

## 🙏 Credits

**Built by:** Porter (Claude Code CLI)  
**For:** Logan Smith / Metaphy LLC  
**Part of:** Team Brain / Beacon HQ  
**Date:** January 18, 2026

---

## 🔗 Links

- **GitHub:** https://github.com/DonkRonk17/TimeSync
- **Team Brain:** Beacon HQ
- **Metaphy LLC:** Maximum Benefit of Life 🔆

---

**Questions? Feedback? Issues?**  
Open an issue on GitHub or message via Team Brain Synapse!
