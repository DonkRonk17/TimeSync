# TimeSync - Usage Examples

Comprehensive examples for TimeSync v1.1 - Universal Time Synchronization System.

**Quick Navigation:**
- [Example 1: Basic Time Retrieval](#example-1-basic-time-retrieval)
- [Example 2: Syncing the Timer](#example-2-syncing-the-timer)
- [Example 3: Checking Timer Status](#example-3-checking-timer-status)
- [Example 4: Session Start Integration](#example-4-session-start-integration)
- [Example 5: Python API Usage](#example-5-python-api-usage)
- [Example 6: Time-Aware Greetings](#example-6-time-aware-greetings)
- [Example 7: JSON Output for Automation](#example-7-json-output-for-automation)
- [Example 8: Error Handling](#example-8-error-handling)
- [Example 9: Integration with SynapseLink](#example-9-integration-with-synapselink)
- [Example 10: Cross-Platform Path Handling](#example-10-cross-platform-path-handling)
- [Example 11: Batch Scripts](#example-11-batch-scripts)
- [Example 12: Full Workflow Example](#example-12-full-workflow-example)

---

## Example 1: Basic Time Retrieval

**Scenario:** Get the current accurate time for logging or timestamps.

**CLI Usage:**
```bash
python timesync.py get
```

**Expected Output:**
```
2026-01-22T14:30:45.123456
```

**Python Usage:**
```python
from timesync import get_current_time

now = get_current_time()
print(f"Current time: {now}")
# Current time: 2026-01-22 14:30:45.123456
```

**What You Learned:**
- TimeSync returns ISO-formatted datetime
- The time is always accurate (auto-syncs if stale)
- Works identically via CLI or Python API

---

## Example 2: Syncing the Timer

**Scenario:** Manually sync the universal timer (e.g., at session start).

**CLI Usage:**
```bash
python timesync.py sync --triggered-by "ATLAS"
```

**Expected Output:**
```
[OK] Timer synced at 2026-01-22T14:31:00
     Triggered by: ATLAS
     Timezone: Pacific Standard Time
     Method: SystemTime
```

**Python Usage:**
```python
from timesync import sync_timer

result = sync_timer(triggered_by="ATLAS")
print(f"Timer synced: {result['last_verified']}")
print(f"By: {result['verified_by']}")
```

**What You Learned:**
- You can attribute syncs to specific agents
- The timezone and sync method are recorded
- All agents share the same universal timer

---

## Example 3: Checking Timer Status

**Scenario:** See detailed information about the current timer.

**CLI Usage:**
```bash
python timesync.py info
```

**Expected Output:**
```
Universal Timer Status:
  Session Start: 2026-01-22T08:00:00
  Last Verified: 2026-01-22T14:30:00
  Verified By: BCH_GM_BUTTON
  Timezone: Pacific Standard Time
  Sync Method: SystemTime
  Age: 6h 30m (6.5 hours)
  Status: FRESH
  Stale Threshold: 24 hours
```

**Python Usage:**
```python
from timesync import get_timer_info

info = get_timer_info()
if info:
    print(f"Status: {info['status']}")
    print(f"Age: {info['age_display']}")
    print(f"Triggered by: {info['verified_by']}")
else:
    print("No timer found - need to sync")
```

**What You Learned:**
- Timer tracks when it was created and by whom
- Age is displayed in human-readable format
- Status shows FRESH or STALE

---

## Example 4: Session Start Integration

**Scenario:** Initialize timer when BCH GM button is pressed.

**In BCH Backend (Python):**
```python
from timesync import initialize_session_timer
from synapselink import quick_send

def handle_gm_button():
    """Handler for BCH Good Morning button."""
    
    # Sync universal timer
    timer_data = initialize_session_timer("BCH_GM_BUTTON")
    
    # Notify all agents
    quick_send(
        "ALL",
        "Good Morning - Timer Synced",
        f"Universal timer initialized at {timer_data['last_verified']}\n"
        f"Timezone: {timer_data['timezone']}\n"
        f"All agents now have accurate time!",
        priority="NORMAL"
    )
    
    return {"status": "ok", "timer": timer_data}
```

**Expected Behavior:**
1. Timer file updated at `D:\BEACON_HQ\MEMORY_CORE_V2\UNIVERSAL_TIMER.json`
2. Synapse message sent to all agents
3. All subsequent `get_current_time()` calls return accurate time

**What You Learned:**
- `initialize_session_timer()` is designed for session starts
- It automatically integrates with SynapseLink for team notifications
- One sync benefits ALL agents

---

## Example 5: Python API Usage

**Scenario:** Full Python integration in an AI agent.

**Complete Agent Integration:**
```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/TimeSync")

from timesync import (
    get_current_time,
    get_current_time_iso,
    is_timer_stale,
    sync_timer,
    get_timer_info
)

# At session start
if is_timer_stale():
    sync_timer(triggered_by="FORGE")
    print("Timer was stale - synced!")

# Get current time (always accurate)
now = get_current_time()
timestamp = get_current_time_iso()  # String format

# Use for logging
print(f"[{timestamp}] Session started")

# Check timer status
info = get_timer_info()
print(f"Timer age: {info['age_display']}, Status: {info['status']}")
```

**Expected Output:**
```
Timer was stale - synced!
[2026-01-22T14:35:00.123456] Session started
Timer age: 0s, Status: FRESH
```

**What You Learned:**
- Multiple functions available for different use cases
- `get_current_time()` returns datetime object
- `get_current_time_iso()` returns string for logging
- Check stale status at session start

---

## Example 6: Time-Aware Greetings

**Scenario:** Generate appropriate greeting based on time of day.

**Python Code:**
```python
from timesync import get_current_time

def get_greeting():
    """Get time-appropriate greeting."""
    now = get_current_time()
    hour = now.hour
    
    if hour < 5:
        return "Good night"
    elif hour < 12:
        return "Good morning"
    elif hour < 17:
        return "Good afternoon"
    elif hour < 21:
        return "Good evening"
    else:
        return "Good night"

# Usage
print(f"{get_greeting()}, Logan!")
```

**Expected Output (at 2:30 PM):**
```
Good afternoon, Logan!
```

**What You Learned:**
- TimeSync provides accurate local time
- The `.hour` attribute gives 24-hour format
- Useful for contextual AI responses

---

## Example 7: JSON Output for Automation

**Scenario:** Get timer data in JSON format for scripts.

**CLI Usage:**
```bash
# Get time as JSON
python timesync.py get --json

# Get full info as JSON
python timesync.py info --json

# Check stale status as JSON
python timesync.py check --json
```

**Expected Output (get --json):**
```json
{"time": "2026-01-22T14:40:00.123456"}
```

**Expected Output (info --json):**
```json
{
  "session_start": "2026-01-22T08:00:00",
  "last_verified": "2026-01-22T14:30:00",
  "verified_by": "BCH_GM_BUTTON",
  "timezone": "Pacific Standard Time",
  "sync_method": "SystemTime",
  "version": "1.1.0",
  "age_hours": 6.5,
  "age_display": "6h 30m",
  "status": "FRESH",
  "stale_threshold_hours": 24
}
```

**In a Script:**
```bash
# PowerShell
$time = python timesync.py get --json | ConvertFrom-Json
echo "Current time: $($time.time)"

# Bash
TIME=$(python timesync.py get --json | jq -r '.time')
echo "Current time: $TIME"
```

**What You Learned:**
- `--json` flag gives machine-parseable output
- Useful for shell scripts and automation
- All commands support JSON output

---

## Example 8: Error Handling

**Scenario:** Handle cases where timer operations fail.

**Python Code:**
```python
from timesync import (
    get_current_time,
    get_timer_info,
    sync_timer,
    is_timer_stale
)

def safe_get_time():
    """Get time with comprehensive error handling."""
    try:
        # First, check if timer exists and is fresh
        info = get_timer_info()
        
        if info is None:
            print("[!] No timer found, syncing...")
            sync_timer(triggered_by="ERROR_RECOVERY")
        elif info['status'] == 'STALE':
            print(f"[!] Timer stale ({info['age_display']} old), syncing...")
            sync_timer(triggered_by="STALE_RECOVERY")
        
        # Now get time (guaranteed to work)
        return get_current_time()
        
    except Exception as e:
        print(f"[X] Timer error: {e}")
        print("[!] Falling back to system time")
        from datetime import datetime
        return datetime.now()

# Usage
now = safe_get_time()
print(f"Time: {now.isoformat()}")
```

**What You Learned:**
- TimeSync has built-in error recovery
- `get_current_time()` auto-syncs if needed
- You can add extra logging for visibility

---

## Example 9: Integration with SynapseLink

**Scenario:** Combine TimeSync with SynapseLink for timestamped messages.

**Python Code:**
```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/TimeSync")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/SynapseLink")

from timesync import get_current_time_iso
from synapselink import quick_send

def send_timestamped_message(recipients, subject, body, priority="NORMAL"):
    """Send a Synapse message with accurate timestamp."""
    timestamp = get_current_time_iso()
    
    # Add timestamp to body
    timestamped_body = f"[{timestamp}]\n\n{body}"
    
    quick_send(
        recipients,
        subject,
        timestamped_body,
        priority=priority
    )
    
    print(f"[OK] Sent at {timestamp}")

# Usage
send_timestamped_message(
    "FORGE,ATLAS",
    "Task Complete",
    "The TimeSync repair is complete.\n\nAll tests passing!",
    priority="NORMAL"
)
```

**What You Learned:**
- TimeSync and SynapseLink work together
- Timestamps ensure accurate message timing
- All agents see consistent time references

---

## Example 10: Cross-Platform Path Handling

**Scenario:** Get timer path on different platforms.

**CLI Usage:**
```bash
python timesync.py path
```

**Expected Output (Windows):**
```
Timer Path: D:\BEACON_HQ\MEMORY_CORE_V2\UNIVERSAL_TIMER.json
Exists: True
```

**Expected Output (WSL):**
```
Timer Path: /mnt/d/BEACON_HQ/MEMORY_CORE_V2/UNIVERSAL_TIMER.json
Exists: True
```

**Python Usage:**
```python
from timesync import get_timer_path

path = get_timer_path()
print(f"Timer file: {path}")
print(f"Exists: {path.exists()}")
print(f"Platform-specific: {str(path)}")
```

**What You Learned:**
- TimeSync auto-detects the correct path for each platform
- Same code works on Windows, WSL, Linux, macOS
- The timer file is shared across platforms

---

## Example 11: Batch Scripts

**Scenario:** Use TimeSync in batch/shell scripts.

**Windows Batch (timesync_wrapper.bat):**
```batch
@echo off
REM Sync timer at start of batch operations

echo Syncing universal timer...
python "%USERPROFILE%\OneDrive\Documents\AutoProjects\TimeSync\timesync.py" sync --triggered-by "BATCH_SCRIPT"

echo.
echo Current time:
python "%USERPROFILE%\OneDrive\Documents\AutoProjects\TimeSync\timesync.py" get

echo.
echo Timer status:
python "%USERPROFILE%\OneDrive\Documents\AutoProjects\TimeSync\timesync.py" info
```

**PowerShell Script:**
```powershell
# timesync_session.ps1

# Get Python path
$timesyncp = "C:\Users\logan\OneDrive\Documents\AutoProjects\TimeSync\timesync.py"

# Check if timer is stale
$status = python $timesync check --json | ConvertFrom-Json
if ($status.stale) {
    Write-Host "[!] Timer stale, syncing..."
    python $timesync sync --triggered-by "POWERSHELL"
}

# Get current time
$time = python $timesync get
Write-Host "Current time: $time"
```

**Bash Script (Linux/WSL):**
```bash
#!/bin/bash
# timesync_session.sh

TIMESYNC="/mnt/c/Users/logan/OneDrive/Documents/AutoProjects/TimeSync/timesync.py"

# Sync timer at start
echo "Syncing timer..."
python3 "$TIMESYNC" sync --triggered-by "BASH_SCRIPT"

# Get current time
TIME=$(python3 "$TIMESYNC" get)
echo "Current time: $TIME"
```

**What You Learned:**
- TimeSync works from any scripting environment
- JSON output makes parsing easy
- Use platform-appropriate paths

---

## Example 12: Full Workflow Example

**Scenario:** Complete agent session workflow with TimeSync.

**Full Agent Session Script:**
```python
#!/usr/bin/env python3
"""
Example: Complete agent session with TimeSync integration.
This shows how an AI agent should use TimeSync throughout a session.
"""

import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/TimeSync")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/SynapseLink")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/TokenTracker")

from timesync import get_current_time, get_current_time_iso, is_timer_stale, sync_timer, get_timer_info
from synapselink import quick_send
from tokentracker import TokenTracker

AGENT_NAME = "ATLAS"

def session_start():
    """Initialize session with accurate time."""
    print(f"[{get_current_time_iso()}] Session starting...")
    
    # Check and sync timer if needed
    if is_timer_stale():
        sync_timer(triggered_by=AGENT_NAME)
        print(f"[{get_current_time_iso()}] Timer was stale - synced!")
    
    info = get_timer_info()
    print(f"[{get_current_time_iso()}] Timer status: {info['status']} ({info['age_display']} old)")
    
    return get_current_time()

def do_work(task_name: str):
    """Perform some work with timing."""
    start = get_current_time()
    print(f"[{get_current_time_iso()}] Starting task: {task_name}")
    
    # ... do actual work here ...
    import time
    time.sleep(2)  # Simulate work
    
    end = get_current_time()
    duration = (end - start).total_seconds()
    print(f"[{get_current_time_iso()}] Task complete: {task_name} ({duration:.1f}s)")
    
    return duration

def session_end(start_time, tasks_completed: int):
    """End session with summary."""
    end_time = get_current_time()
    duration = end_time - start_time
    
    summary = f"""Session Summary for {AGENT_NAME}
    
Started: {start_time.isoformat()}
Ended: {end_time.isoformat()}
Duration: {duration}
Tasks Completed: {tasks_completed}

Timer Status: {get_timer_info()['status']}
"""
    
    print(f"\n[{get_current_time_iso()}] Session ending")
    print(summary)
    
    # Notify team
    quick_send(
        "FORGE",
        f"Session End: {AGENT_NAME}",
        summary,
        priority="LOW"
    )

def main():
    """Run example session."""
    # Start
    session_start_time = session_start()
    
    # Do work
    tasks = ["Build tool", "Run tests", "Update docs"]
    for task in tasks:
        do_work(task)
    
    # End
    session_end(session_start_time, len(tasks))

if __name__ == "__main__":
    main()
```

**Expected Output:**
```
[2026-01-22T14:45:00.123456] Session starting...
[2026-01-22T14:45:00.234567] Timer status: FRESH (6h 45m old)
[2026-01-22T14:45:00.345678] Starting task: Build tool
[2026-01-22T14:45:02.456789] Task complete: Build tool (2.1s)
[2026-01-22T14:45:02.567890] Starting task: Run tests
[2026-01-22T14:45:04.678901] Task complete: Run tests (2.1s)
[2026-01-22T14:45:04.789012] Starting task: Update docs
[2026-01-22T14:45:06.890123] Task complete: Update docs (2.1s)

[2026-01-22T14:45:06.901234] Session ending
Session Summary for ATLAS
    
Started: 2026-01-22T14:45:00.123456
Ended: 2026-01-22T14:45:06.901234
Duration: 0:00:06.777778
Tasks Completed: 3

Timer Status: FRESH
```

**What You Learned:**
- TimeSync integrates throughout the session lifecycle
- Timestamps provide consistent logging
- Duration calculations use accurate time
- Session summaries include timing data

---

## Summary

TimeSync provides:

| Feature | CLI Command | Python Function |
|---------|-------------|-----------------|
| Get time | `timesync.py get` | `get_current_time()` |
| Get time (string) | `timesync.py get` | `get_current_time_iso()` |
| Sync timer | `timesync.py sync` | `sync_timer()` |
| Check status | `timesync.py info` | `get_timer_info()` |
| Check if stale | `timesync.py check` | `is_timer_stale()` |
| Initialize session | - | `initialize_session_timer()` |
| Get timer path | `timesync.py path` | `get_timer_path()` |
| Reset timer | `timesync.py reset` | `reset_timer()` |

**Best Practices:**
1. Sync timer at session start
2. Use `get_current_time()` instead of `datetime.now()`
3. Include timestamps in logs and messages
4. Check timer status for debugging
5. Use JSON output for automation

---

**Last Updated:** January 2026  
**Maintained By:** Atlas (Team Brain)
