"""
Breaking test script for TimeFocus v0.1
Purpose: Find ALL the ways this can fail
"""

import sys
sys.path.insert(0, '.')
from timesync import get_current_time, is_timer_stale, sync_timer, get_timer_info
import os
import json
from pathlib import Path

print("=" * 60)
print("TimeFocus v0.1 - BREAKING TESTS")
print("=" * 60)

# Test 1: What if timer file is corrupted?
def test_corrupted_timer():
    print("\n[TEST 1] Corrupted timer file")
    timer_path = Path("/mnt/d/BEACON_HQ/MEMORY_CORE_V2/UNIVERSAL_TIMER.json")
    
    # Backup current timer
    with open(timer_path, 'r') as f:
        backup = f.read()
    
    try:
        # Write corrupted JSON
        with open(timer_path, 'w') as f:
            f.write("{invalid json syntax!@#$%")
        
        # Try to get time
        current = get_current_time()
        print("[FAIL] Accepted corrupted timer - no validation!")
    except json.JSONDecodeError:
        print("[OK] Rejected corrupted timer")
    except Exception as e:
        print(f"[WARN] Crashed with unexpected error: {type(e).__name__}: {e}")
    finally:
        # Restore backup
        with open(timer_path, 'w') as f:
            f.write(backup)

# Test 2: What if timer file is missing mid-operation?
def test_missing_timer():
    print("\n[TEST 2] Missing timer file")
    timer_path = Path("/mnt/d/BEACON_HQ/MEMORY_CORE_V2/UNIVERSAL_TIMER.json")
    
    # Backup and delete
    with open(timer_path, 'r') as f:
        backup = f.read()
    
    try:
        os.remove(timer_path)
        
        # Try to get time
        current = get_current_time()
        print("[OK] Handled missing timer (auto-synced)")
    except Exception as e:
        print(f"[FAIL] Crashed on missing timer: {e}")
    finally:
        # Restore
        with open(timer_path, 'w') as f:
            f.write(backup)

# Test 3: What if BeaconTime tool is missing?
def test_missing_beacon_time():
    print("\n[TEST 3] Missing BeaconTime tool")
    
    # This would require moving the tool, which is destructive
    # Instead, test with invalid path in code
    print("[SKIP] Would require modifying beacon_time_sync.py location")

# Test 4: What if timer is from distant future?
def test_future_timer():
    print("\n[TEST 4] Timer from future")
    timer_path = Path("/mnt/d/BEACON_HQ/MEMORY_CORE_V2/UNIVERSAL_TIMER.json")
    
    with open(timer_path, 'r') as f:
        backup = f.read()
    
    try:
        # Create timer from 2027
        future_timer = {
            "session_start": "2027-01-18T16:46:18",
            "last_verified": "2027-01-18T16:46:18",
            "verified_by": "TEST",
            "timezone": "Pacific Standard Time"
        }
        
        with open(timer_path, 'w') as f:
            json.dump(future_timer, f)
        
        info = get_timer_info()
        print(f"[WARN] Accepted future timer: age_hours={info['age_hours']:.1f}")
        if info['age_hours'] < 0:
            print("[CRITICAL] Negative age hours! Timer from future!")
    except Exception as e:
        print(f"[OK] Rejected future timer: {e}")
    finally:
        with open(timer_path, 'w') as f:
            f.write(backup)

# Test 5: What if timer file permissions are wrong?
def test_permission_denied():
    print("\n[TEST 5] Permission denied")
    # Hard to test without actually breaking permissions
    print("[SKIP] Would require chmod operations that might break system")

# Test 6: Rapid repeated calls
def test_rapid_calls():
    print("\n[TEST 6] Rapid repeated calls (1000x)")
    try:
        for i in range(1000):
            current = get_current_time()
        print("[OK] Handled 1000 rapid calls without crash")
    except Exception as e:
        print(f"[FAIL] Crashed after rapid calls: {e}")

# Test 7: Missing timezone
def test_missing_timezone():
    print("\n[TEST 7] Missing timezone in timer")
    timer_path = Path("/mnt/d/BEACON_HQ/MEMORY_CORE_V2/UNIVERSAL_TIMER.json")
    
    with open(timer_path, 'r') as f:
        backup = f.read()
    
    try:
        # Create timer without timezone
        no_tz_timer = {
            "session_start": "2026-01-18T16:46:18",
            "last_verified": "2026-01-18T16:46:18",
            "verified_by": "TEST"
        }
        
        with open(timer_path, 'w') as f:
            json.dump(no_tz_timer, f)
        
        info = get_timer_info()
        if 'timezone' not in info:
            print("[WARN] Missing timezone not detected")
        else:
            print("[OK] Handled missing timezone field")
    except Exception as e:
        print(f"[FAIL] Crashed on missing timezone: {e}")
    finally:
        with open(timer_path, 'w') as f:
            f.write(backup)

# Test 8: Invalid timestamp format
def test_invalid_timestamp():
    print("\n[TEST 8] Invalid timestamp format")
    timer_path = Path("/mnt/d/BEACON_HQ/MEMORY_CORE_V2/UNIVERSAL_TIMER.json")
    
    with open(timer_path, 'r') as f:
        backup = f.read()
    
    try:
        # Create timer with invalid timestamp
        bad_timer = {
            "session_start": "not a timestamp!",
            "last_verified": "also not a timestamp",
            "verified_by": "TEST",
            "timezone": "Pacific Standard Time"
        }
        
        with open(timer_path, 'w') as f:
            json.dump(bad_timer, f)
        
        current = get_current_time()
        print("[FAIL] Accepted invalid timestamp format")
    except ValueError:
        print("[OK] Rejected invalid timestamp format")
    except Exception as e:
        print(f"[WARN] Unexpected error: {type(e).__name__}: {e}")
    finally:
        with open(timer_path, 'w') as f:
            f.write(backup)

# Test 9: Very old timer (100 years)
def test_ancient_timer():
    print("\n[TEST 9] Ancient timer (100 years old)")
    timer_path = Path("/mnt/d/BEACON_HQ/MEMORY_CORE_V2/UNIVERSAL_TIMER.json")
    
    with open(timer_path, 'r') as f:
        backup = f.read()
    
    try:
        ancient_timer = {
            "session_start": "1926-01-18T16:46:18",
            "last_verified": "1926-01-18T16:46:18",
            "verified_by": "TEST",
            "timezone": "Pacific Standard Time"
        }
        
        with open(timer_path, 'w') as f:
            json.dump(ancient_timer, f)
        
        stale = is_timer_stale()
        if stale:
            print("[OK] Detected ancient timer as stale")
        else:
            print("[FAIL] Did not detect 100-year-old timer as stale")
        
        # Try to get time (should auto-sync)
        current = get_current_time()
        print("[OK] Auto-synced ancient timer")
    except Exception as e:
        print(f"[WARN] Crashed on ancient timer: {e}")
    finally:
        with open(timer_path, 'w') as f:
            f.write(backup)

# Test 10: Concurrent access (simulated)
def test_concurrent_access():
    print("\n[TEST 10] Concurrent access simulation")
    try:
        # Simulate multiple AIs accessing at once
        import threading
        
        results = []
        def get_time():
            try:
                current = get_current_time()
                results.append(('success', current))
            except Exception as e:
                results.append(('error', e))
        
        threads = [threading.Thread(target=get_time) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        successes = len([r for r in results if r[0] == 'success'])
        print(f"[{'OK' if successes == 10 else 'WARN'}] {successes}/10 concurrent calls succeeded")
    except Exception as e:
        print(f"[FAIL] Crashed during concurrent access: {e}")

# Run all tests
test_corrupted_timer()
test_missing_timer()
test_missing_beacon_time()
test_future_timer()
test_permission_denied()
test_rapid_calls()
test_missing_timezone()
test_invalid_timestamp()
test_ancient_timer()
test_concurrent_access()

print("\n" + "=" * 60)
print("⚠️ Review warnings and failures above!")
print("=" * 60)
