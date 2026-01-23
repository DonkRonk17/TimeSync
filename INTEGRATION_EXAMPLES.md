# TimeSync - Integration Examples

Copy-paste-ready code examples for integrating TimeSync with other Team Brain tools.

---

## 📚 TABLE OF CONTENTS

1. [Pattern 1: TimeSync + TokenTracker](#pattern-1-timesync--tokentracker)
2. [Pattern 2: TimeSync + SynapseLink](#pattern-2-timesync--synapselink)
3. [Pattern 3: TimeSync + AgentHealth](#pattern-3-timesync--agenthealth)
4. [Pattern 4: TimeSync + SessionReplay](#pattern-4-timesync--sessionreplay)
5. [Pattern 5: TimeSync + ContextCompressor](#pattern-5-timesync--contextcompressor)
6. [Pattern 6: TimeSync + TaskQueuePro](#pattern-6-timesync--taskqueuepro)
7. [Pattern 7: TimeSync + MemoryBridge](#pattern-7-timesync--memorybridge)
8. [Pattern 8: TimeSync + ConfigManager](#pattern-8-timesync--configmanager)
9. [Pattern 9: TimeSync + DevSnapshot](#pattern-9-timesync--devsnapshot)
10. [Pattern 10: Full Team Brain Stack](#pattern-10-full-team-brain-stack)

---

## Pattern 1: TimeSync + TokenTracker

**Use Case:** Log API usage with accurate timestamps

**Why:** Correlate token spending with time for budget analysis

**Code:**

```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/TimeSync")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/TokenTracker")

from timesync import get_current_time_iso, get_current_time
from tokentracker import TokenTracker

def log_usage_with_time(agent: str, model: str, input_tokens: int, output_tokens: int, task: str):
    """Log token usage with accurate timestamp."""
    tracker = TokenTracker()
    timestamp = get_current_time_iso()
    
    # Log usage with TimeSync timestamp
    tracker.log_usage(
        agent=agent,
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        task=f"[{timestamp}] {task}"
    )
    
    print(f"[{timestamp}] Logged: {input_tokens + output_tokens} tokens for {task}")

# Usage
log_usage_with_time("ATLAS", "claude-3-opus", 1000, 500, "Tool creation")
```

**Result:** Token logs have accurate, consistent timestamps across all agents

---

## Pattern 2: TimeSync + SynapseLink

**Use Case:** Send timestamped messages to Team Brain

**Why:** Ensure message timestamps are accurate across time zones

**Code:**

```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/TimeSync")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/SynapseLink")

from timesync import get_current_time_iso, get_timer_info
from synapselink import quick_send

def send_timestamped_update(recipients: str, subject: str, body: str, priority: str = "NORMAL"):
    """Send Synapse message with accurate timestamp header."""
    timestamp = get_current_time_iso()
    timer_info = get_timer_info()
    
    # Add timestamp and timer info to message
    full_body = f"""[{timestamp}]
Timer Status: {timer_info['status']} ({timer_info['age_display']} old)

{body}
"""
    
    quick_send(
        to=recipients,
        subject=f"[{timestamp[:10]}] {subject}",
        message_body=full_body,
        priority=priority
    )
    
    print(f"[OK] Sent to {recipients} at {timestamp}")

# Usage
send_timestamped_update(
    "FORGE,CLIO",
    "Task Complete: TimeSync Repair",
    "TimeSync has been repaired to 100% professional standard.\n\nAll tests passing!",
    priority="NORMAL"
)
```

**Result:** All team messages have consistent, accurate timestamps

---

## Pattern 3: TimeSync + AgentHealth

**Use Case:** Health monitoring with accurate timing

**Why:** Correlate agent health metrics with accurate time

**Code:**

```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/TimeSync")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/AgentHealth")

from timesync import get_current_time, get_current_time_iso, sync_timer
from agenthealth import AgentHealth

def monitored_session(agent_name: str, task: str):
    """Run a health-monitored session with accurate timing."""
    health = AgentHealth()
    session_start = get_current_time()
    
    # Start health session with TimeSync timestamp
    session_id = health.start_session(
        agent_name, 
        session_id=f"{agent_name}_{get_current_time_iso()}"
    )
    
    try:
        # Heartbeat with accurate time
        health.heartbeat(agent_name, status="active")
        print(f"[{get_current_time_iso()}] Working on: {task}")
        
        # ... do work ...
        
        # Success
        health.end_session(agent_name, session_id=session_id, status="success")
        duration = get_current_time() - session_start
        print(f"[{get_current_time_iso()}] Complete. Duration: {duration}")
        
    except Exception as e:
        # Log error with timestamp
        health.log_error(agent_name, f"[{get_current_time_iso()}] {str(e)}")
        health.end_session(agent_name, session_id=session_id, status="failed")
        raise

# Usage
monitored_session("ATLAS", "Building TimeSync repair")
```

**Result:** Health metrics are time-correlated for analysis

---

## Pattern 4: TimeSync + SessionReplay

**Use Case:** Record sessions with accurate timestamps

**Why:** Replay debugging requires accurate timing

**Code:**

```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/TimeSync")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/SessionReplay")

from timesync import get_current_time, get_current_time_iso
from sessionreplay import SessionReplay

def record_session_with_timing(agent: str, task: str):
    """Record a session with TimeSync timestamps."""
    replay = SessionReplay()
    
    # Start recording with accurate timestamp
    session_id = replay.start_session(
        agent, 
        task=task,
        metadata={"start_time": get_current_time_iso()}
    )
    
    def log_event(event_type: str, data: str):
        """Log event with timestamp."""
        timestamp = get_current_time_iso()
        if event_type == "input":
            replay.log_input(session_id, f"[{timestamp}] {data}")
        elif event_type == "output":
            replay.log_output(session_id, f"[{timestamp}] {data}")
        elif event_type == "error":
            replay.log_error(session_id, f"[{timestamp}] {data}")
    
    return session_id, log_event

# Usage
session_id, log = record_session_with_timing("ATLAS", "TimeSync repair")
log("input", "Starting repair process")
log("output", "Tests passing: 35/35")
```

**Result:** Session replays show accurate timing for debugging

---

## Pattern 5: TimeSync + ContextCompressor

**Use Case:** Compress context with timestamp metadata

**Why:** Preserve timing info when compressing large contexts

**Code:**

```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/TimeSync")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/ContextCompressor")

from timesync import get_current_time_iso
from contextcompressor import ContextCompressor

def compress_with_timestamp(content: str, query: str = ""):
    """Compress content while preserving timestamp metadata."""
    compressor = ContextCompressor()
    timestamp = get_current_time_iso()
    
    # Compress the content
    result = compressor.compress_text(
        content,
        query=query,
        method="summary"
    )
    
    # Add timestamp metadata
    compressed_with_meta = f"""[Compressed at {timestamp}]
Original: {result.original_size} bytes
Compressed: {result.compressed_size} bytes
Savings: {result.estimated_token_savings} tokens

{result.compressed_text}
"""
    
    return compressed_with_meta

# Usage
large_log = "..." * 1000  # Large log content
compressed = compress_with_timestamp(large_log, query="errors")
print(compressed)
```

**Result:** Compressed content includes when it was compressed

---

## Pattern 6: TimeSync + TaskQueuePro

**Use Case:** Task management with accurate scheduling

**Why:** Task queues need accurate creation/completion times

**Code:**

```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/TimeSync")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/TaskQueuePro")

from timesync import get_current_time, get_current_time_iso
from taskqueuepro import TaskQueuePro
from datetime import timedelta

def create_scheduled_task(title: str, agent: str, delay_hours: float = 0):
    """Create task with accurate scheduling."""
    queue = TaskQueuePro()
    now = get_current_time()
    
    # Calculate scheduled time
    scheduled_time = now + timedelta(hours=delay_hours)
    
    # Create task with accurate timestamps
    task_id = queue.create_task(
        title=f"[{get_current_time_iso()}] {title}",
        agent=agent,
        priority=2,
        metadata={
            "created_at": get_current_time_iso(),
            "scheduled_for": scheduled_time.isoformat()
        }
    )
    
    print(f"[OK] Task {task_id} created")
    print(f"     Scheduled for: {scheduled_time.isoformat()}")
    
    return task_id

def complete_task_with_duration(task_id: str, start_time):
    """Complete task and record duration."""
    queue = TaskQueuePro()
    end_time = get_current_time()
    duration = end_time - start_time
    
    queue.complete_task(
        task_id,
        result={
            "completed_at": get_current_time_iso(),
            "duration_seconds": duration.total_seconds()
        }
    )
    
    print(f"[OK] Task {task_id} complete. Duration: {duration}")

# Usage
task_start = get_current_time()
task_id = create_scheduled_task("Repair TimeSync", "ATLAS")
# ... do work ...
complete_task_with_duration(task_id, task_start)
```

**Result:** Task queue has accurate timing for scheduling and reporting

---

## Pattern 7: TimeSync + MemoryBridge

**Use Case:** Store memories with accurate timestamps

**Why:** Memory recall needs temporal context

**Code:**

```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/TimeSync")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/MemoryBridge")

from timesync import get_current_time_iso, get_current_time
from memorybridge import MemoryBridge

def store_timed_memory(key: str, value, category: str = "general"):
    """Store memory with accurate timestamp."""
    memory = MemoryBridge()
    timestamp = get_current_time_iso()
    
    # Wrap value with timestamp
    timed_value = {
        "timestamp": timestamp,
        "category": category,
        "data": value
    }
    
    memory.set(key, timed_value)
    memory.sync()
    
    print(f"[{timestamp}] Stored memory: {key}")
    return timestamp

def retrieve_with_age(key: str):
    """Retrieve memory and calculate age."""
    memory = MemoryBridge()
    value = memory.get(key)
    
    if value and "timestamp" in value:
        stored_time = get_current_time().fromisoformat(value["timestamp"])
        age = get_current_time() - stored_time
        print(f"Memory age: {age}")
        return value["data"], age
    
    return value, None

# Usage
store_timed_memory("last_timesync_repair", {"status": "complete", "tests": 35})
data, age = retrieve_with_age("last_timesync_repair")
```

**Result:** Memories have temporal context for relevance

---

## Pattern 8: TimeSync + ConfigManager

**Use Case:** Track config changes over time

**Why:** Configuration audit trail needs accurate timing

**Code:**

```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/TimeSync")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/ConfigManager")

from timesync import get_current_time_iso
from configmanager import ConfigManager

def update_config_with_audit(section: str, key: str, value, changed_by: str):
    """Update config with audit trail."""
    config = ConfigManager()
    timestamp = get_current_time_iso()
    
    # Get old value for audit
    old_value = config.get(f"{section}.{key}")
    
    # Update config
    config.set(f"{section}.{key}", value)
    
    # Update audit trail
    audit_key = f"_audit.{section}.{key}"
    audit_trail = config.get(audit_key, [])
    audit_trail.append({
        "timestamp": timestamp,
        "old_value": old_value,
        "new_value": value,
        "changed_by": changed_by
    })
    config.set(audit_key, audit_trail)
    config.save()
    
    print(f"[{timestamp}] Config {section}.{key} changed by {changed_by}")
    print(f"     {old_value} -> {value}")

# Usage
update_config_with_audit("timesync", "stale_threshold_hours", 24, "ATLAS")
```

**Result:** Configuration changes have full audit trail

---

## Pattern 9: TimeSync + DevSnapshot

**Use Case:** Capture dev state with accurate timestamps

**Why:** Snapshots need temporal context for comparison

**Code:**

```python
import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/TimeSync")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/DevSnapshot")

from timesync import get_current_time, get_current_time_iso
from devsnapshot import DevSnapshot

def take_timed_snapshot(description: str):
    """Take development snapshot with accurate timestamp."""
    snapshot = DevSnapshot()
    timestamp = get_current_time_iso()
    
    # Capture with TimeSync timestamp
    snap_id = snapshot.capture(
        description=f"[{timestamp}] {description}",
        metadata={"captured_at": timestamp}
    )
    
    print(f"[{timestamp}] Snapshot captured: {snap_id}")
    return snap_id, timestamp

def compare_snapshots_with_time(snap_a: str, snap_b: str):
    """Compare snapshots and show time difference."""
    snapshot = DevSnapshot()
    
    # Get snapshots
    a_data = snapshot.get(snap_a)
    b_data = snapshot.get(snap_b)
    
    if a_data and b_data:
        from datetime import datetime
        time_a = datetime.fromisoformat(a_data.get('metadata', {}).get('captured_at', ''))
        time_b = datetime.fromisoformat(b_data.get('metadata', {}).get('captured_at', ''))
        time_diff = abs(time_b - time_a)
        
        print(f"Time between snapshots: {time_diff}")
        
        # Get diff
        diff = snapshot.diff(snap_a, snap_b)
        return diff, time_diff
    
    return None, None

# Usage
snap1, _ = take_timed_snapshot("Before TimeSync repair")
# ... make changes ...
snap2, _ = take_timed_snapshot("After TimeSync repair")
diff, time_diff = compare_snapshots_with_time(snap1, snap2)
```

**Result:** Snapshots have temporal context for before/after analysis

---

## Pattern 10: Full Team Brain Stack

**Use Case:** Complete agent session with all tools

**Why:** Production-grade operation requires full integration

**Code:**

```python
#!/usr/bin/env python3
"""
Full Team Brain stack integration with TimeSync.
This is the recommended pattern for production agent sessions.
"""

import sys
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/TimeSync")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/SynapseLink")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/TokenTracker")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/AgentHealth")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/SessionReplay")
sys.path.append("C:/Users/logan/OneDrive/Documents/AutoProjects/TaskQueuePro")

from timesync import (
    get_current_time, 
    get_current_time_iso, 
    is_timer_stale, 
    sync_timer,
    get_timer_info
)
from synapselink import quick_send
from tokentracker import TokenTracker
from agenthealth import AgentHealth
from sessionreplay import SessionReplay
from taskqueuepro import TaskQueuePro

AGENT_NAME = "ATLAS"

class TeamBrainSession:
    """Full Team Brain session with TimeSync at the core."""
    
    def __init__(self, agent: str, task: str):
        self.agent = agent
        self.task = task
        self.start_time = None
        
        # Initialize components
        self.tracker = TokenTracker()
        self.health = AgentHealth()
        self.replay = SessionReplay()
        self.queue = TaskQueuePro()
        
    def start(self):
        """Start session with full instrumentation."""
        # Sync timer if needed
        if is_timer_stale():
            sync_timer(triggered_by=self.agent)
        
        self.start_time = get_current_time()
        timestamp = get_current_time_iso()
        
        # Start all tracking
        self.session_id = f"{self.agent}_{timestamp}"
        self.health.start_session(self.agent, session_id=self.session_id)
        self.replay.start_session(self.agent, task=self.task)
        self.task_id = self.queue.create_task(
            title=f"[{timestamp}] {self.task}",
            agent=self.agent
        )
        
        self.replay.log_input(self.session_id, f"[{timestamp}] Session started")
        print(f"[{timestamp}] Session started: {self.task}")
        
        return self
    
    def log(self, message: str, tokens: int = 0):
        """Log activity with timestamp."""
        timestamp = get_current_time_iso()
        self.replay.log_output(self.session_id, f"[{timestamp}] {message}")
        
        if tokens > 0:
            self.tracker.log_usage(
                self.agent, "model", tokens, tokens // 2, 
                f"[{timestamp}] {message}"
            )
        
        print(f"[{timestamp}] {message}")
    
    def heartbeat(self):
        """Send heartbeat with current status."""
        self.health.heartbeat(self.agent, status="active")
    
    def complete(self, result: str = "success"):
        """Complete session with summary."""
        end_time = get_current_time()
        duration = end_time - self.start_time
        timestamp = get_current_time_iso()
        
        # Complete all tracking
        self.health.end_session(self.agent, session_id=self.session_id, status=result)
        self.replay.end_session(self.session_id, status="COMPLETED")
        self.queue.complete_task(self.task_id, result={
            "status": result,
            "duration": str(duration)
        })
        
        # Summary
        timer_info = get_timer_info()
        summary = f"""Session Complete: {self.task}

Agent: {self.agent}
Start: {self.start_time.isoformat()}
End: {timestamp}
Duration: {duration}
Result: {result}

Timer Status: {timer_info['status']} ({timer_info['age_display']} old)
"""
        
        # Notify team
        quick_send(
            "FORGE",
            f"Session Complete: {self.agent}",
            summary,
            priority="LOW"
        )
        
        print(f"\n[{timestamp}] Session complete")
        print(summary)
        
        return duration

# Usage
def main():
    session = TeamBrainSession(AGENT_NAME, "TimeSync Repair").start()
    
    try:
        session.log("Starting repair work", tokens=100)
        session.heartbeat()
        
        session.log("Fixing cross-platform paths", tokens=200)
        session.heartbeat()
        
        session.log("Creating test suite", tokens=300)
        session.heartbeat()
        
        session.log("All tests passing: 35/35", tokens=50)
        
        session.complete("success")
        
    except Exception as e:
        session.log(f"Error: {e}")
        session.complete("failed")
        raise

if __name__ == "__main__":
    main()
```

**Result:** Fully instrumented, production-grade agent session

---

## 📊 INTEGRATION PRIORITY

**Week 1 (Essential):**
1. ✅ SynapseLink - Timestamped messages
2. ✅ AgentHealth - Correlated health metrics
3. ✅ TokenTracker - Usage tracking

**Week 2 (Productivity):**
4. ☐ SessionReplay - Timed debugging
5. ☐ TaskQueuePro - Scheduled tasks
6. ☐ MemoryBridge - Temporal context

**Week 3 (Advanced):**
7. ☐ DevSnapshot - Timed comparisons
8. ☐ ConfigManager - Audit trails
9. ☐ Full stack integration

---

## 🔧 TROUBLESHOOTING INTEGRATIONS

**Import Errors:**
```python
# Ensure all tools are in Python path
import sys
from pathlib import Path
sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects"))

# Then import
from TimeSync.timesync import get_current_time
```

**Timer Not Syncing:**
```bash
# Reset and sync fresh
python timesync.py reset
python timesync.py sync --triggered-by MANUAL_FIX
```

**Platform Path Issues:**
```python
# Use get_timer_path() to verify correct path
from timesync import get_timer_path
print(f"Timer: {get_timer_path()}")
```

---

**Last Updated:** January 2026  
**Maintained By:** Atlas (Team Brain)
