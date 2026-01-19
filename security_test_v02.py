"""
Security test script for TimeFocus v0.2
Purpose: Verify all v0.1 vulnerabilities are fixed
"""

import sys
sys.path.insert(0, '.')
from timesync import get_current_time, is_timer_stale, sync_timer, get_timer_info
import json
from pathlib import Path

print("=" * 60)
print("TimeFocus v0.2 - SECURITY TESTS")
print("=" * 60)

tests_passed = 0
tests_total = 0

# Test 1: Future timer should be detected as stale
def test_future_timer_fixed():
    global tests_passed, tests_total
    tests_total += 1
    
    print("\n[TEST 1] Future timer detection")
    timer_path = Path("/mnt/d/BEACON_HQ/MEMORY_CORE_V2/UNIVERSAL_TIMER.json")
    
    with open(timer_path, 'r') as f:
        backup = f.read()
    
    try:
        # Create future timer
        future_timer = {
            "session_start": "2027-01-18T16:46:18",
            "last_verified": "2027-01-18T16:46:18",
            "verified_by": "TEST",
            "timezone": "Pacific Standard Time"
        }
        
        with open(timer_path, 'w') as f:
            json.dump(future_timer, f)
        
        # Check if detected as stale
        if is_timer_stale():
            print("[PASS] Future timer correctly detected as stale")
            tests_passed += 1
        else:
            print("[FAIL] Future timer not detected as stale")
    finally:
        with open(timer_path, 'w') as f:
            f.write(backup)

# Test 2: Missing timezone should have default
def test_missing_timezone_fixed():
    global tests_passed, tests_total
    tests_total += 1
    
    print("\n[TEST 2] Missing timezone handling")
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
        if 'timezone' in info and info['timezone'] == "Unknown":
            print("[PASS] Missing timezone handled with default")
            tests_passed += 1
        else:
            print(f"[FAIL] Timezone handling issue: {info.get('timezone', 'MISSING')}")
    finally:
        with open(timer_path, 'w') as f:
            f.write(backup)

# Test 3: Corrupted JSON still handled
def test_corrupted_json_still_handled():
    global tests_passed, tests_total
    tests_total += 1
    
    print("\n[TEST 3] Corrupted JSON handling (regression)")
    timer_path = Path("/mnt/d/BEACON_HQ/MEMORY_CORE_V2/UNIVERSAL_TIMER.json")
    
    with open(timer_path, 'r') as f:
        backup = f.read()
    
    try:
        with open(timer_path, 'w') as f:
            f.write("{bad json!@#$}")
        
        # Should auto-sync and recover
        current = get_current_time()
        print("[PASS] Corrupted JSON handled (auto-synced)")
        tests_passed += 1
    except Exception as e:
        print(f"[FAIL] Corrupted JSON not handled: {e}")
    finally:
        with open(timer_path, 'w') as f:
            f.write(backup)

# Test 4: Normal operation still works
def test_normal_operation():
    global tests_passed, tests_total
    tests_total += 1
    
    print("\n[TEST 4] Normal operation (regression)")
    try:
        # Sync fresh timer
        sync_timer(triggered_by="TEST_V02")
        
        # Get time
        current = get_current_time()
        
        # Check not stale
        if not is_timer_stale():
            print("[PASS] Normal operation works correctly")
            tests_passed += 1
        else:
            print("[FAIL] Fresh timer incorrectly marked as stale")
    except Exception as e:
        print(f"[FAIL] Normal operation failed: {e}")

# Run all tests
test_future_timer_fixed()
test_missing_timezone_fixed()
test_corrupted_json_still_handled()
test_normal_operation()

print(f"\n{'='*60}")
print(f"RESULTS: {tests_passed}/{tests_total} tests passed")
print(f"{'='*60}")

sys.exit(0 if tests_passed == tests_total else 1)
