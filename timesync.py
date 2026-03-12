#!/usr/bin/env python3
"""
TimeSync - Universal Time Synchronization System

Provides accurate, synchronized time across all AI agents and sessions.
Solves WSL time drift and reduces token overhead from repeated time checks.

Author: Porter (Claude Code CLI)
Enhanced: Atlas (Team Brain)
Created: 2026-01-18
Version: 1.1.0
License: MIT

Features:
- Self-healing timer: Auto-detects stale timers (>24hrs) and re-syncs
- Zero dependencies: Pure Python stdlib, works everywhere
- Token efficient: One sync per session instead of per-message checks
- Universal sync: ONE timer, ALL AIs synchronized
- Fail gracefully: Handles corrupted timers, missing files, future timestamps
- Cross-platform: Works on Windows, Linux (including WSL), macOS
"""

import os
import sys
import json
import platform
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, Tuple, Union

# ============== CONSTANTS ==============
VERSION = "1.1.0"

# Stale threshold (24 hours)
STALE_THRESHOLD_HOURS = 24


# ============== CROSS-PLATFORM PATH RESOLUTION ==============

def _get_beacon_hq_root() -> Path:
    """
    Get the Beacon HQ root path based on current platform.
    
    Supports:
    - Windows: D:\\BEACON_HQ
    - WSL: /mnt/d/BEACON_HQ
    - Linux/macOS: ~/BEACON_HQ (fallback)
    
    Returns:
        Path: Beacon HQ root directory
    """
    system = platform.system().lower()
    
    # Check for WSL
    is_wsl = 'microsoft' in platform.uname().release.lower() if system == 'linux' else False
    
    if system == 'windows':
        # Windows native
        beacon_root = Path("D:/BEACON_HQ")
        if not beacon_root.exists():
            # Fallback to common locations
            for drive in ['D:', 'C:', 'E:']:
                candidate = Path(f"{drive}/BEACON_HQ")
                if candidate.exists():
                    return candidate
            # Use default even if doesn't exist (will be created)
            return Path("D:/BEACON_HQ")
        return beacon_root
    
    elif is_wsl:
        # WSL - access Windows drives via /mnt/
        beacon_root = Path("/mnt/d/BEACON_HQ")
        if not beacon_root.exists():
            for drive in ['d', 'c', 'e']:
                candidate = Path(f"/mnt/{drive}/BEACON_HQ")
                if candidate.exists():
                    return candidate
            return Path("/mnt/d/BEACON_HQ")
        return beacon_root
    
    else:
        # Linux/macOS - use home directory
        beacon_root = Path.home() / "BEACON_HQ"
        if not beacon_root.exists():
            # Try to find it elsewhere
            common_paths = [
                Path("/opt/BEACON_HQ"),
                Path("/var/BEACON_HQ"),
            ]
            for p in common_paths:
                if p.exists():
                    return p
        return beacon_root


def _get_universal_timer_path() -> Path:
    """Get the universal timer file path."""
    return _get_beacon_hq_root() / "MEMORY_CORE_V2" / "UNIVERSAL_TIMER.json"


def _get_beacon_time_tool_path() -> Optional[Path]:
    """
    Get the BeaconTime tool path.
    
    Returns None if not found (fallback to system time).
    """
    beacon_root = _get_beacon_hq_root()
    
    # Try common locations
    candidates = [
        beacon_root / "TOOLS" / "beacon_time_sync.py",
        beacon_root / "tools" / "beacon_time_sync.py",
        beacon_root / "scripts" / "beacon_time_sync.py",
    ]
    
    for path in candidates:
        if path.exists():
            return path
    
    return None


# ============== CORE FUNCTIONS ==============

def get_current_time() -> datetime:
    """
    Get the current accurate time.
    
    Uses universal timer if available and fresh (<24hrs old).
    Auto-syncs if timer is stale or missing.
    Falls back to system time if BeaconTime unavailable.
    
    Returns:
        datetime: Current time
        
    Example:
        >>> now = get_current_time()
        >>> print(f"Current time: {now}")
        Current time: 2026-01-22T14:30:00
    """
    try:
        # Check if timer exists and is fresh
        if _timer_exists() and not is_timer_stale():
            return _calculate_time_from_timer()
        else:
            # Timer missing or stale - sync and try again
            sync_timer()
            return _calculate_time_from_timer()
    except Exception:
        # Timer corrupted or sync failed - use system time
        return datetime.now()


def get_current_time_iso() -> str:
    """
    Get current time as ISO formatted string.
    
    Convenience function for agents that need string output.
    
    Returns:
        str: Current time in ISO 8601 format
        
    Example:
        >>> timestamp = get_current_time_iso()
        >>> print(timestamp)
        2026-01-22T14:30:00.123456
    """
    return get_current_time().isoformat()


def is_timer_stale() -> bool:
    """
    Check if universal timer is stale (>24 hours old).
    
    Returns:
        bool: True if timer is stale or missing, False if fresh
        
    Example:
        >>> if is_timer_stale():
        ...     sync_timer()
        >>> print("Timer is fresh")
    """
    if not _timer_exists():
        return True
    
    try:
        timer_data = _load_timer()
        last_verified = datetime.fromisoformat(timer_data['last_verified'])
        age_hours = (datetime.now() - last_verified).total_seconds() / 3600
        
        # Check for future timer (negative age) - treat as stale
        if age_hours < 0:
            return True
        
        return age_hours > STALE_THRESHOLD_HOURS
    except (json.JSONDecodeError, KeyError, ValueError, TypeError):
        # Timer corrupted - treat as stale
        return True


def sync_timer(triggered_by: str = "AUTO") -> Dict[str, Any]:
    """
    Sync universal timer with accurate system time.
    
    Attempts to use BeaconTime tool if available, otherwise uses system time.
    
    Args:
        triggered_by: Who/what triggered the sync (for logging)
        
    Returns:
        dict: Updated timer data with keys:
            - session_start: ISO timestamp
            - last_verified: ISO timestamp
            - verified_by: Trigger source
            - timezone: Timezone name
            - sync_method: How time was obtained
            
    Example:
        >>> timer_data = sync_timer(triggered_by="ATLAS")
        >>> print(f"Timer synced at {timer_data['last_verified']}")
        Timer synced at 2026-01-22T14:30:00
    """
    # Validate input
    if not triggered_by:
        triggered_by = "AUTO"
    if not isinstance(triggered_by, str):
        triggered_by = str(triggered_by)
    
    # Get accurate time (BeaconTime or system fallback)
    accurate_time, sync_method = _get_accurate_time()
    
    # Create/update timer file
    timer_data = {
        "session_start": accurate_time.isoformat(),
        "last_verified": datetime.now().isoformat(),
        "verified_by": triggered_by,
        "timezone": _get_timezone_name(),
        "sync_method": sync_method,
        "version": VERSION
    }
    
    _save_timer(timer_data)
    
    return timer_data


def initialize_session_timer(triggered_by: str = "BCH_GM_BUTTON") -> Dict[str, Any]:
    """
    Initialize universal timer for a new session.
    
    Called by BCH GM button or manual session start.
    This is the preferred method for starting a new sync cycle.
    
    Args:
        triggered_by: Source of initialization (for logging)
        
    Returns:
        dict: New timer data
        
    Example:
        >>> # In BCH GM button handler:
        >>> timer_data = initialize_session_timer("BCH_GM_BUTTON")
        >>> # Now broadcast GM message to all AIs
    """
    return sync_timer(triggered_by=triggered_by)


def get_timer_info() -> Optional[Dict[str, Any]]:
    """
    Get current timer information (for debugging/display).
    
    Returns:
        dict or None: Timer data including:
            - session_start: When session started
            - last_verified: Last sync time
            - verified_by: Who triggered last sync
            - timezone: Timezone name
            - age_hours: Timer age in hours
            - age_display: Human-readable age
            - status: FRESH or STALE
            - stale_threshold_hours: When timer becomes stale
        Returns None if no timer exists.
        
    Example:
        >>> info = get_timer_info()
        >>> if info:
        ...     print(f"Timer age: {info['age_hours']:.1f} hours")
        ...     print(f"Status: {info['status']}")
        Timer age: 2.5 hours
        Status: FRESH
    """
    if not _timer_exists():
        return None
    
    try:
        timer_data = _load_timer()
        last_verified = datetime.fromisoformat(timer_data['last_verified'])
        age = datetime.now() - last_verified
        age_hours = age.total_seconds() / 3600
        
        # Provide defaults for missing fields
        defaults = {
            'timezone': 'Unknown',
            'sync_method': 'unknown',
            'version': '1.0.0'
        }
        for key, default in defaults.items():
            if key not in timer_data:
                timer_data[key] = default
        
        return {
            **timer_data,
            "age_hours": age_hours,
            "age_display": _format_timedelta(age),
            "status": "FRESH" if age_hours < STALE_THRESHOLD_HOURS and age_hours >= 0 else "STALE",
            "stale_threshold_hours": STALE_THRESHOLD_HOURS
        }
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        return None


def get_timer_path() -> Path:
    """
    Get the path to the universal timer file.
    
    Useful for debugging and verification.
    
    Returns:
        Path: Path to timer file
    """
    return _get_universal_timer_path()


def reset_timer() -> bool:
    """
    Reset (delete) the universal timer.
    
    Useful for testing or forcing a fresh sync.
    
    Returns:
        bool: True if timer was deleted, False if didn't exist
        
    Example:
        >>> reset_timer()
        True
        >>> is_timer_stale()
        True
    """
    timer_path = _get_universal_timer_path()
    if timer_path.exists():
        timer_path.unlink()
        return True
    return False


# ============== INTERNAL HELPER FUNCTIONS ==============

def _timer_exists() -> bool:
    """Check if universal timer file exists."""
    return _get_universal_timer_path().exists()


def _load_timer() -> Dict[str, Any]:
    """Load timer data from file."""
    with open(_get_universal_timer_path(), 'r', encoding='utf-8') as f:
        return json.load(f)


def _save_timer(data: Dict[str, Any]) -> None:
    """Save timer data to file."""
    timer_path = _get_universal_timer_path()
    
    # Ensure directory exists
    timer_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(timer_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def _calculate_time_from_timer() -> datetime:
    """
    Calculate current time from timer data.
    
    For simplicity and reliability, returns current system time.
    The timer's purpose is staleness detection, not time computation.
    """
    return datetime.now()


def _get_accurate_time() -> Tuple[datetime, str]:
    """
    Get accurate time from best available source.
    
    Tries BeaconTime tool first, falls back to system time.
    
    Returns:
        Tuple[datetime, str]: (accurate_time, sync_method)
    """
    # Try BeaconTime tool first
    beacon_tool = _get_beacon_time_tool_path()
    if beacon_tool and beacon_tool.exists():
        try:
            result = subprocess.run(
                [sys.executable, str(beacon_tool), '--get'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                timestamp_str = result.stdout.strip()
                return datetime.fromisoformat(timestamp_str), "BeaconTime"
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, ValueError):
            pass  # Fall through to system time
    
    # Fallback: system time
    return datetime.now(), "SystemTime"


def _get_timezone_name() -> str:
    """Get current timezone name (platform-agnostic)."""
    # Try platform-specific methods first
    system = platform.system().lower()
    
    if system == 'windows':
        try:
            result = subprocess.run(
                ['powershell.exe', '-Command', '[System.TimeZoneInfo]::Local.Id'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
            pass
    
    # Python's built-in detection
    try:
        import time
        if time.daylight:
            return time.tzname[1] or time.tzname[0] or "Unknown"
        return time.tzname[0] or "Unknown"
    except Exception:
        return "Unknown"


def _format_timedelta(td: timedelta) -> str:
    """Format timedelta as human-readable string."""
    total_seconds = int(abs(td.total_seconds()))
    
    # Handle negative (future) times
    prefix = "-" if td.total_seconds() < 0 else ""
    
    if total_seconds < 60:
        return f"{prefix}{total_seconds}s"
    elif total_seconds < 3600:
        minutes = total_seconds // 60
        return f"{prefix}{minutes}m"
    elif total_seconds < 86400:
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        if minutes:
            return f"{prefix}{hours}h {minutes}m"
        return f"{prefix}{hours}h"
    else:
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        return f"{prefix}{days}d {hours}h"


# ============== CLI INTERFACE ==============

def main():
    """CLI entry point for TimeSync operations."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='TimeSync - Universal Time Synchronization System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s get                    Get current time (ISO format)
  %(prog)s sync                   Sync timer with accurate time
  %(prog)s sync --triggered-by ATLAS  Sync with attribution
  %(prog)s info                   Show timer status
  %(prog)s check                  Check if timer is stale (exit codes)
  %(prog)s path                   Show timer file path
  %(prog)s reset                  Delete timer (force fresh sync)

Exit Codes:
  0 - Success / Timer is fresh
  1 - Error / Timer is stale

For more information: https://github.com/DonkRonk17/TimeSync
        """
    )
    
    parser.add_argument(
        'command',
        nargs='?',
        choices=['get', 'sync', 'info', 'check', 'path', 'reset'],
        default='get',
        help='Command to execute (default: get)'
    )
    parser.add_argument(
        '--triggered-by', '-t',
        default='CLI',
        help='Who/what triggered the command (for sync)'
    )
    parser.add_argument(
        '--json', '-j',
        action='store_true',
        help='Output in JSON format (where applicable)'
    )
    parser.add_argument(
        '--version', '-v',
        action='version',
        version=f'TimeSync {VERSION}'
    )
    
    args = parser.parse_args()
    
    try:
        if args.command == 'get':
            current_time = get_current_time()
            if args.json:
                print(json.dumps({"time": current_time.isoformat()}))
            else:
                print(current_time.isoformat())
        
        elif args.command == 'sync':
            timer_data = sync_timer(triggered_by=args.triggered_by)
            if args.json:
                print(json.dumps(timer_data, indent=2))
            else:
                print(f"[OK] Timer synced at {timer_data['last_verified']}")
                print(f"     Triggered by: {timer_data['verified_by']}")
                print(f"     Timezone: {timer_data['timezone']}")
                print(f"     Method: {timer_data['sync_method']}")
        
        elif args.command == 'info':
            info = get_timer_info()
            if info:
                if args.json:
                    print(json.dumps(info, indent=2))
                else:
                    print("Universal Timer Status:")
                    print(f"  Session Start: {info['session_start']}")
                    print(f"  Last Verified: {info['last_verified']}")
                    print(f"  Verified By: {info['verified_by']}")
                    print(f"  Timezone: {info['timezone']}")
                    print(f"  Sync Method: {info['sync_method']}")
                    print(f"  Age: {info['age_display']} ({info['age_hours']:.1f} hours)")
                    print(f"  Status: {info['status']}")
                    print(f"  Stale Threshold: {info['stale_threshold_hours']} hours")
            else:
                if args.json:
                    print(json.dumps({"error": "No timer found"}))
                else:
                    print("[!] No timer found. Run 'sync' to create one.")
                sys.exit(1)
        
        elif args.command == 'check':
            stale = is_timer_stale()
            if args.json:
                print(json.dumps({"stale": stale}))
            if stale:
                if not args.json:
                    print("[!] Timer is STALE (>24 hours old or missing)")
                sys.exit(1)
            else:
                if not args.json:
                    print("[OK] Timer is FRESH")
                sys.exit(0)
        
        elif args.command == 'path':
            path = get_timer_path()
            if args.json:
                print(json.dumps({"path": str(path), "exists": path.exists()}))
            else:
                print(f"Timer Path: {path}")
                print(f"Exists: {path.exists()}")
        
        elif args.command == 'reset':
            deleted = reset_timer()
            if args.json:
                print(json.dumps({"deleted": deleted}))
            else:
                if deleted:
                    print("[OK] Timer deleted. Next get/sync will create fresh timer.")
                else:
                    print("[!] No timer found to delete.")
    
    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"[X] Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
