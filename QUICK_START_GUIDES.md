# TimeSync - Quick Start Guides

Each Team Brain agent has a **5-minute quick-start guide** tailored to their role and workflows.

**Choose your guide:**
- [Forge (Orchestrator)](#forge-quick-start)
- [Atlas (Builder/Executor)](#atlas-quick-start)
- [Clio (Linux/Ubuntu Agent)](#clio-quick-start)
- [Nexus (Multi-Platform)](#nexus-quick-start)
- [Bolt (Free Executor)](#bolt-quick-start)
- [Logan (Human User)](#logan-quick-start)

---

## 🔥 FORGE QUICK START

**Role:** Orchestrator / Reviewer  
**Time:** 5 minutes  
**Goal:** Use TimeSync for session coordination and accurate scheduling

### Step 1: Installation Check

```bash
# Verify TimeSync is available
cd C:\Users\logan\OneDrive\Documents\AutoProjects\TimeSync
python timesync.py --version
# Expected: TimeSync 1.1.0
```

### Step 2: First Use - Session Orchestration

```python
# In your Forge session
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/TimeSync")
from timesync import get_current_time, sync_timer, is_timer_stale

# At session start - always sync
if is_timer_stale():
    sync_timer(triggered_by="FORGE")
    print("[OK] Timer synced for all agents")
```

### Step 3: Integration with Forge Workflows

**Use Case 1: Task Scheduling**
```python
from timesync import get_current_time
from datetime import timedelta

def schedule_task(task_name: str, delay_hours: float):
    """Schedule a task for later."""
    now = get_current_time()
    scheduled_time = now + timedelta(hours=delay_hours)
    
    print(f"Task '{task_name}' scheduled for {scheduled_time.isoformat()}")
    return scheduled_time
```

**Use Case 2: Coordinating Multiple Agents**
```python
from timesync import get_current_time_iso, get_timer_info
from synapselink import quick_send

def broadcast_session_status():
    """Inform team of current session state."""
    info = get_timer_info()
    
    quick_send(
        "ALL",
        f"Session Status Update",
        f"Timer: {info['status']} ({info['age_display']} old)\n"
        f"Last sync by: {info['verified_by']}\n"
        f"All agents should have accurate time.",
        priority="LOW"
    )
```

### Step 4: Common Forge Commands

```bash
# Check timer status before assigning tasks
python timesync.py info

# Sync timer when starting orchestration session
python timesync.py sync --triggered-by FORGE

# Get current time for task logs
python timesync.py get
```

### Next Steps for Forge
1. Read [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) - Forge section
2. Try [EXAMPLES.md](EXAMPLES.md) - Example 4 (Session Start)
3. Use TimeSync timestamp in all task assignments

---

## ⚡ ATLAS QUICK START

**Role:** Builder / Executor  
**Time:** 5 minutes  
**Goal:** Use TimeSync for build logging and session tracking

### Step 1: Installation Check

```bash
# In Cursor terminal
cd C:\Users\logan\OneDrive\Documents\AutoProjects\TimeSync
python timesync.py --version
```

### Step 2: First Use - Build Session Logging

```python
# In your Atlas session
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/TimeSync")
from timesync import get_current_time, get_current_time_iso

# Always use TimeSync for timestamps
print(f"[{get_current_time_iso()}] Starting tool build...")
```

### Step 3: Integration with Build Workflows

**During Tool Creation:**
```python
from timesync import get_current_time, get_current_time_iso, sync_timer

class ToolBuilder:
    def __init__(self, tool_name: str):
        self.tool_name = tool_name
        self.start_time = get_current_time()
        print(f"[{get_current_time_iso()}] Starting build: {tool_name}")
    
    def complete(self):
        end_time = get_current_time()
        duration = end_time - self.start_time
        print(f"[{get_current_time_iso()}] Build complete: {self.tool_name}")
        print(f"Duration: {duration}")
        return duration

# Usage
builder = ToolBuilder("TimeSync")
# ... do build work ...
builder.complete()
```

**Session Bookmark Creation:**
```python
from timesync import get_current_time_iso, get_timer_info

def create_session_bookmark(project: str, status: str):
    """Create bookmark with accurate timestamps."""
    timestamp = get_current_time_iso()
    timer_info = get_timer_info()
    
    bookmark = f"""# Session Bookmark: {project}

**Date:** {timestamp}
**Status:** {status}
**Timer:** {timer_info['status']} ({timer_info['age_display']} old)
"""
    return bookmark
```

### Step 4: Common Atlas Commands

```bash
# Sync at session start
python timesync.py sync --triggered-by ATLAS

# Get timestamp for logs
python timesync.py get

# Check timer age (for session logs)
python timesync.py info --json
```

### Next Steps for Atlas
1. Use TimeSync timestamps in ALL session logs
2. Add to Holy Grail automation workflow
3. Include timer info in completion reports

---

## 🐧 CLIO QUICK START

**Role:** Linux / Ubuntu Agent  
**Time:** 5 minutes  
**Goal:** Use TimeSync in Linux/WSL environment

### Step 1: Linux/WSL Installation

```bash
# In Linux terminal
cd /mnt/c/Users/logan/OneDrive/Documents/AutoProjects/TimeSync

# Verify Python3 available
python3 --version

# Test TimeSync
python3 timesync.py --version
# Expected: TimeSync 1.1.0
```

### Step 2: First Use - WSL Integration

```bash
# Sync timer (fixes WSL time drift)
python3 timesync.py sync --triggered-by CLIO

# Get current accurate time
python3 timesync.py get
# Output: 2026-01-22T14:30:00.123456
```

### Step 3: Integration with Clio Workflows

**Python Usage (WSL Path):**
```python
import sys
sys.path.append("/mnt/c/Users/logan/OneDrive/Documents/AutoProjects/TimeSync")
from timesync import get_current_time, sync_timer

# WSL time can drift - TimeSync keeps it accurate
now = get_current_time()
print(f"Accurate time: {now}")
```

**Shell Script Integration:**
```bash
#!/bin/bash
# clio_session_start.sh

TIMESYNC="/mnt/c/Users/logan/OneDrive/Documents/AutoProjects/TimeSync/timesync.py"

# Sync timer at session start (important for WSL!)
echo "[$(python3 $TIMESYNC get)] CLIO session starting..."
python3 $TIMESYNC sync --triggered-by CLIO

# Show timer status
python3 $TIMESYNC info
```

### Step 4: Common Clio Commands

```bash
# Sync timer (WSL time drift fix)
python3 timesync.py sync --triggered-by CLIO

# Get time for script logs
TIME=$(python3 timesync.py get)
echo "Task started at $TIME"

# Check timer path (verify cross-platform)
python3 timesync.py path
```

**Platform-Specific Notes:**
- TimeSync auto-detects WSL and uses `/mnt/d/` paths
- WSL time can drift; sync timer at session start
- Timer file is shared with Windows agents

### Next Steps for Clio
1. Add TimeSync sync to ABIOS startup
2. Use in all Linux scripts
3. Report any WSL-specific issues

---

## 🌐 NEXUS QUICK START

**Role:** Multi-Platform Agent  
**Time:** 5 minutes  
**Goal:** Use TimeSync across Windows, Linux, macOS

### Step 1: Platform Detection

```python
import platform
import sys

# TimeSync works on all platforms
if platform.system() == 'Windows':
    sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/TimeSync")
else:
    sys.path.append("/mnt/c/Users/logan/OneDrive/Documents/AutoProjects/TimeSync")

from timesync import get_current_time, get_timer_path
print(f"Platform: {platform.system()}")
print(f"Timer path: {get_timer_path()}")
```

### Step 2: First Use - Cross-Platform Time

```python
from timesync import get_current_time, sync_timer

# Works identically on all platforms
now = get_current_time()
print(f"Current time: {now}")

# Sync works cross-platform too
sync_timer(triggered_by="NEXUS")
```

### Step 3: Platform-Specific Considerations

**Windows:**
```python
# Timer path: D:\BEACON_HQ\MEMORY_CORE_V2\UNIVERSAL_TIMER.json
from timesync import get_timer_path
print(get_timer_path())  # D:\BEACON_HQ\...
```

**Linux/WSL:**
```python
# Timer path: /mnt/d/BEACON_HQ/MEMORY_CORE_V2/UNIVERSAL_TIMER.json
from timesync import get_timer_path
print(get_timer_path())  # /mnt/d/BEACON_HQ/...
```

**macOS:**
```python
# Timer path: ~/BEACON_HQ/MEMORY_CORE_V2/UNIVERSAL_TIMER.json
from timesync import get_timer_path
print(get_timer_path())  # /Users/.../BEACON_HQ/...
```

### Step 4: Common Nexus Commands

```bash
# Windows CMD/PowerShell
python timesync.py sync --triggered-by NEXUS

# Linux/macOS
python3 timesync.py sync --triggered-by NEXUS

# Get timer path (verify platform detection)
python timesync.py path --json
```

### Next Steps for Nexus
1. Test on all 3 platforms
2. Verify timer is shared correctly
3. Report platform-specific issues

---

## 🆓 BOLT QUICK START

**Role:** Free Executor (Cline + Grok)  
**Time:** 5 minutes  
**Goal:** Use TimeSync without API costs

### Step 1: Verify Free Access

```bash
# No API key required!
python timesync.py --version
# TimeSync is 100% free to use
```

### Step 2: First Use - Free Time Sync

```bash
# Sync timer - no cost!
python timesync.py sync --triggered-by BOLT

# Get accurate time - no API calls!
python timesync.py get
```

### Step 3: Integration with Bolt Workflows

**Cost-Free Task Timing:**
```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/TimeSync")
from timesync import get_current_time

# All operations are FREE - no API calls
start = get_current_time()
# ... execute task ...
end = get_current_time()
duration = end - start
print(f"Task took {duration.total_seconds():.1f} seconds")
# Zero tokens used for timing!
```

### Step 4: Common Bolt Commands

```bash
# Free operations - use liberally!
python timesync.py get          # Free
python timesync.py sync         # Free
python timesync.py info         # Free
python timesync.py check        # Free
```

### Cost Considerations

**Before TimeSync (expensive):**
```python
# Every AI message might check time
# "What time is it?" = API call = tokens = cost
```

**After TimeSync (free):**
```python
# Local timer, no API calls
now = get_current_time()  # FREE!
```

### Next Steps for Bolt
1. Add TimeSync to all Cline workflows
2. Use for task timing without token cost
3. Report savings via TokenTracker

---

## 👤 LOGAN QUICK START

**Role:** Human User / Team Lead  
**Time:** 3 minutes  
**Goal:** Understand TimeSync for oversight

### When to Use

**TimeSync is automatic for you!** The BCH GM button syncs the timer. However, you can manually check:

### CLI Commands

```bash
# Check timer status
python timesync.py info

# Manual sync (if needed)
python timesync.py sync --triggered-by LOGAN

# Get current accurate time
python timesync.py get
```

### BCH Integration

When you press **GM** in BCH:
1. Universal timer syncs automatically
2. All AI agents get accurate time
3. Session timestamps are consistent

### Troubleshooting

**If agents report wrong time:**
```bash
# Reset and sync fresh
python timesync.py reset
python timesync.py sync --triggered-by LOGAN
```

**Check timer health:**
```bash
python timesync.py info
# Look for: Status: FRESH
```

---

## 📚 ADDITIONAL RESOURCES

**For All Agents:**
- Full Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Integration Plan: [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- Cheat Sheet: [CHEAT_SHEET.txt](CHEAT_SHEET.txt)
- Integration Examples: [INTEGRATION_EXAMPLES.md](INTEGRATION_EXAMPLES.md)

**Support:**
- GitHub Issues: https://github.com/DonkRonk17/TimeSync/issues
- Synapse: Post in THE_SYNAPSE/active/
- Direct: Message Forge or Atlas

---

## Summary Table

| Agent | Primary Use Case | Import Path | First Command |
|-------|------------------|-------------|---------------|
| **Forge** | Session coordination | Windows | `sync --triggered-by FORGE` |
| **Atlas** | Build logging | Windows | `get` for timestamps |
| **Clio** | WSL time drift fix | WSL/Linux | `sync --triggered-by CLIO` |
| **Nexus** | Cross-platform time | Any | `path` to verify platform |
| **Bolt** | Free task timing | Any | `get` (zero cost!) |
| **Logan** | Manual override | Windows | `info` to check status |

---

**Last Updated:** January 2026  
**Maintained By:** Atlas (Team Brain)
