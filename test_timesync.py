#!/usr/bin/env python3
"""
Comprehensive test suite for TimeSync v1.1.

Tests cover:
- Core functionality (get time, sync, check stale)
- Cross-platform path resolution
- Timer file operations (load, save, delete)
- Edge cases (corrupted files, missing files, future timestamps)
- Error handling
- CLI interface
- Python API

Run: python test_timesync.py
"""

import json
import sys
import os
import unittest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from io import StringIO

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from timesync import (
    get_current_time,
    get_current_time_iso,
    is_timer_stale,
    sync_timer,
    initialize_session_timer,
    get_timer_info,
    get_timer_path,
    reset_timer,
    _get_beacon_hq_root,
    _get_universal_timer_path,
    _format_timedelta,
    _timer_exists,
    _load_timer,
    _save_timer,
    VERSION,
    STALE_THRESHOLD_HOURS,
)


class TestTimeSyncCore(unittest.TestCase):
    """Test core TimeSync functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test timer files
        self.test_dir = tempfile.mkdtemp()
        self.original_get_path = _get_universal_timer_path
        
    def tearDown(self):
        """Clean up after tests."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_version_defined(self):
        """Test version is properly defined."""
        self.assertIsNotNone(VERSION)
        self.assertRegex(VERSION, r'^\d+\.\d+\.\d+$')
        print("[OK] Version defined correctly")
    
    def test_stale_threshold_defined(self):
        """Test stale threshold is a positive number."""
        self.assertIsInstance(STALE_THRESHOLD_HOURS, (int, float))
        self.assertGreater(STALE_THRESHOLD_HOURS, 0)
        print("[OK] Stale threshold defined correctly")
    
    def test_get_current_time_returns_datetime(self):
        """Test get_current_time returns a datetime object."""
        result = get_current_time()
        self.assertIsInstance(result, datetime)
        # Should be close to now
        delta = abs((datetime.now() - result).total_seconds())
        self.assertLess(delta, 5)  # Within 5 seconds
        print("[OK] get_current_time returns datetime")
    
    def test_get_current_time_iso_returns_string(self):
        """Test get_current_time_iso returns ISO formatted string."""
        result = get_current_time_iso()
        self.assertIsInstance(result, str)
        # Should be parseable as ISO datetime
        parsed = datetime.fromisoformat(result)
        self.assertIsInstance(parsed, datetime)
        print("[OK] get_current_time_iso returns valid ISO string")


class TestTimerOperations(unittest.TestCase):
    """Test timer file operations."""
    
    def setUp(self):
        """Set up test fixtures with mocked timer path."""
        self.test_dir = tempfile.mkdtemp()
        self.test_timer_path = Path(self.test_dir) / "UNIVERSAL_TIMER.json"
        
        # Patch the timer path function
        self.patcher = patch('timesync._get_universal_timer_path', return_value=self.test_timer_path)
        self.mock_path = self.patcher.start()
        
    def tearDown(self):
        """Clean up after tests."""
        self.patcher.stop()
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_timer_not_exists_initially(self):
        """Test timer doesn't exist before sync."""
        self.assertFalse(self.test_timer_path.exists())
        print("[OK] Timer doesn't exist initially")
    
    def test_sync_creates_timer(self):
        """Test sync creates timer file."""
        result = sync_timer(triggered_by="TEST")
        self.assertTrue(self.test_timer_path.exists())
        self.assertIn('session_start', result)
        self.assertIn('last_verified', result)
        self.assertIn('verified_by', result)
        self.assertEqual(result['verified_by'], 'TEST')
        print("[OK] sync_timer creates timer file")
    
    def test_sync_preserves_trigger_info(self):
        """Test sync preserves who triggered it."""
        result = sync_timer(triggered_by="ATLAS_AGENT")
        self.assertEqual(result['verified_by'], 'ATLAS_AGENT')
        
        # Verify it's in the file too
        with open(self.test_timer_path, 'r') as f:
            data = json.load(f)
        self.assertEqual(data['verified_by'], 'ATLAS_AGENT')
        print("[OK] Trigger info preserved correctly")
    
    def test_timer_fresh_after_sync(self):
        """Test timer is not stale immediately after sync."""
        sync_timer(triggered_by="TEST")
        self.assertFalse(is_timer_stale())
        print("[OK] Timer is fresh after sync")
    
    def test_reset_timer_deletes_file(self):
        """Test reset_timer deletes the timer file."""
        sync_timer(triggered_by="TEST")
        self.assertTrue(self.test_timer_path.exists())
        
        deleted = reset_timer()
        self.assertTrue(deleted)
        self.assertFalse(self.test_timer_path.exists())
        print("[OK] reset_timer deletes file")
    
    def test_reset_nonexistent_timer(self):
        """Test reset_timer returns False when no timer exists."""
        deleted = reset_timer()
        self.assertFalse(deleted)
        print("[OK] reset_timer handles missing file")
    
    def test_get_timer_info_returns_none_when_missing(self):
        """Test get_timer_info returns None when no timer."""
        info = get_timer_info()
        self.assertIsNone(info)
        print("[OK] get_timer_info returns None when missing")
    
    def test_get_timer_info_returns_dict_when_exists(self):
        """Test get_timer_info returns dict after sync."""
        sync_timer(triggered_by="TEST")
        info = get_timer_info()
        
        self.assertIsNotNone(info)
        self.assertIn('session_start', info)
        self.assertIn('last_verified', info)
        self.assertIn('verified_by', info)
        self.assertIn('age_hours', info)
        self.assertIn('age_display', info)
        self.assertIn('status', info)
        self.assertEqual(info['status'], 'FRESH')
        print("[OK] get_timer_info returns complete dict")


class TestStaleDetection(unittest.TestCase):
    """Test stale timer detection."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.test_timer_path = Path(self.test_dir) / "UNIVERSAL_TIMER.json"
        self.patcher = patch('timesync._get_universal_timer_path', return_value=self.test_timer_path)
        self.mock_path = self.patcher.start()
        
    def tearDown(self):
        """Clean up after tests."""
        self.patcher.stop()
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_stale_when_no_timer(self):
        """Test is_timer_stale returns True when no timer exists."""
        self.assertTrue(is_timer_stale())
        print("[OK] Stale detected when no timer")
    
    def test_fresh_after_sync(self):
        """Test timer is fresh immediately after sync."""
        sync_timer()
        self.assertFalse(is_timer_stale())
        print("[OK] Fresh after sync")
    
    def test_stale_after_threshold(self):
        """Test timer is stale after threshold hours."""
        # Create a timer with old timestamp
        old_time = datetime.now() - timedelta(hours=STALE_THRESHOLD_HOURS + 1)
        timer_data = {
            "session_start": old_time.isoformat(),
            "last_verified": old_time.isoformat(),
            "verified_by": "TEST",
            "timezone": "UTC"
        }
        
        self.test_timer_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.test_timer_path, 'w') as f:
            json.dump(timer_data, f)
        
        self.assertTrue(is_timer_stale())
        print("[OK] Stale detected after threshold")
    
    def test_stale_with_future_timestamp(self):
        """Test future timestamp is treated as stale."""
        # Create a timer with future timestamp
        future_time = datetime.now() + timedelta(hours=1)
        timer_data = {
            "session_start": future_time.isoformat(),
            "last_verified": future_time.isoformat(),
            "verified_by": "TEST",
            "timezone": "UTC"
        }
        
        self.test_timer_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.test_timer_path, 'w') as f:
            json.dump(timer_data, f)
        
        self.assertTrue(is_timer_stale())
        print("[OK] Future timestamp treated as stale")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.test_timer_path = Path(self.test_dir) / "UNIVERSAL_TIMER.json"
        self.patcher = patch('timesync._get_universal_timer_path', return_value=self.test_timer_path)
        self.mock_path = self.patcher.start()
        
    def tearDown(self):
        """Clean up after tests."""
        self.patcher.stop()
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_corrupted_json(self):
        """Test handling of corrupted timer file."""
        self.test_timer_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.test_timer_path, 'w') as f:
            f.write("not valid json {{{")
        
        # Should treat as stale
        self.assertTrue(is_timer_stale())
        
        # get_timer_info should return None
        info = get_timer_info()
        self.assertIsNone(info)
        
        print("[OK] Corrupted JSON handled gracefully")
    
    def test_missing_fields(self):
        """Test handling of timer with missing required fields."""
        timer_data = {"session_start": datetime.now().isoformat()}  # Missing other fields
        
        self.test_timer_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.test_timer_path, 'w') as f:
            json.dump(timer_data, f)
        
        # Should treat as stale
        self.assertTrue(is_timer_stale())
        print("[OK] Missing fields handled gracefully")
    
    def test_empty_triggered_by(self):
        """Test sync with empty triggered_by defaults to AUTO."""
        result = sync_timer(triggered_by="")
        self.assertEqual(result['verified_by'], 'AUTO')
        print("[OK] Empty triggered_by defaults to AUTO")
    
    def test_none_triggered_by(self):
        """Test sync with None triggered_by."""
        result = sync_timer(triggered_by=None)
        self.assertEqual(result['verified_by'], 'AUTO')
        print("[OK] None triggered_by handled")
    
    def test_numeric_triggered_by(self):
        """Test sync converts numeric triggered_by to string."""
        result = sync_timer(triggered_by=123)
        self.assertEqual(result['verified_by'], '123')
        print("[OK] Numeric triggered_by converted to string")


class TestFormatTimedelta(unittest.TestCase):
    """Test the _format_timedelta helper function."""
    
    def test_format_seconds(self):
        """Test formatting of durations less than a minute."""
        self.assertEqual(_format_timedelta(timedelta(seconds=30)), "30s")
        self.assertEqual(_format_timedelta(timedelta(seconds=0)), "0s")
        print("[OK] Seconds formatted correctly")
    
    def test_format_minutes(self):
        """Test formatting of durations less than an hour."""
        self.assertEqual(_format_timedelta(timedelta(minutes=5)), "5m")
        self.assertEqual(_format_timedelta(timedelta(minutes=59)), "59m")
        print("[OK] Minutes formatted correctly")
    
    def test_format_hours(self):
        """Test formatting of durations less than a day."""
        self.assertEqual(_format_timedelta(timedelta(hours=3)), "3h")
        self.assertEqual(_format_timedelta(timedelta(hours=3, minutes=30)), "3h 30m")
        print("[OK] Hours formatted correctly")
    
    def test_format_days(self):
        """Test formatting of durations over a day."""
        self.assertEqual(_format_timedelta(timedelta(days=2, hours=5)), "2d 5h")
        self.assertEqual(_format_timedelta(timedelta(days=1)), "1d 0h")
        print("[OK] Days formatted correctly")
    
    def test_format_negative(self):
        """Test formatting of negative durations."""
        result = _format_timedelta(timedelta(hours=-3))
        self.assertTrue(result.startswith("-"))
        print("[OK] Negative durations formatted correctly")


class TestCrossPlatformPaths(unittest.TestCase):
    """Test cross-platform path resolution."""
    
    def test_beacon_hq_root_returns_path(self):
        """Test _get_beacon_hq_root returns a Path object."""
        result = _get_beacon_hq_root()
        self.assertIsInstance(result, Path)
        print("[OK] Beacon HQ root returns Path")
    
    def test_timer_path_returns_path(self):
        """Test _get_universal_timer_path returns a Path object."""
        result = _get_universal_timer_path()
        self.assertIsInstance(result, Path)
        self.assertTrue(str(result).endswith('.json'))
        print("[OK] Timer path returns Path with .json extension")
    
    def test_get_timer_path_public(self):
        """Test public get_timer_path function."""
        result = get_timer_path()
        self.assertIsInstance(result, Path)
        print("[OK] Public get_timer_path works")


class TestInitializeSessionTimer(unittest.TestCase):
    """Test initialize_session_timer function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.test_timer_path = Path(self.test_dir) / "UNIVERSAL_TIMER.json"
        self.patcher = patch('timesync._get_universal_timer_path', return_value=self.test_timer_path)
        self.mock_path = self.patcher.start()
        
    def tearDown(self):
        """Clean up after tests."""
        self.patcher.stop()
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_initialize_creates_timer(self):
        """Test initialize_session_timer creates timer."""
        result = initialize_session_timer("BCH_GM_BUTTON")
        self.assertTrue(self.test_timer_path.exists())
        self.assertEqual(result['verified_by'], 'BCH_GM_BUTTON')
        print("[OK] initialize_session_timer creates timer")
    
    def test_initialize_default_trigger(self):
        """Test initialize_session_timer default trigger."""
        result = initialize_session_timer()
        self.assertEqual(result['verified_by'], 'BCH_GM_BUTTON')
        print("[OK] Default trigger is BCH_GM_BUTTON")


class TestCLI(unittest.TestCase):
    """Test CLI interface."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.test_timer_path = Path(self.test_dir) / "UNIVERSAL_TIMER.json"
        self.patcher = patch('timesync._get_universal_timer_path', return_value=self.test_timer_path)
        self.mock_path = self.patcher.start()
        
    def tearDown(self):
        """Clean up after tests."""
        self.patcher.stop()
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_cli_get_command(self):
        """Test CLI get command returns ISO timestamp."""
        from timesync import main
        
        with patch('sys.argv', ['timesync', 'get']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue().strip()
                # Should be valid ISO timestamp
                datetime.fromisoformat(output)
        print("[OK] CLI get command works")
    
    def test_cli_sync_command(self):
        """Test CLI sync command."""
        from timesync import main
        
        with patch('sys.argv', ['timesync', 'sync', '--triggered-by', 'TEST']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                self.assertIn('[OK]', output)
                self.assertIn('Timer synced', output)
        print("[OK] CLI sync command works")
    
    def test_cli_json_output(self):
        """Test CLI JSON output flag."""
        from timesync import main
        
        with patch('sys.argv', ['timesync', 'get', '--json']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue().strip()
                data = json.loads(output)
                self.assertIn('time', data)
        print("[OK] CLI JSON output works")


def run_tests():
    """Run all tests with detailed output."""
    print("=" * 70)
    print(f"TESTING: TimeSync v{VERSION}")
    print("Universal Time Synchronization System")
    print("=" * 70)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestTimeSyncCore,
        TestTimerOperations,
        TestStaleDetection,
        TestEdgeCases,
        TestFormatTimedelta,
        TestCrossPlatformPaths,
        TestInitializeSessionTimer,
        TestCLI,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print()
    print("=" * 70)
    print(f"RESULTS: {result.testsRun} tests")
    passed = result.testsRun - len(result.failures) - len(result.errors)
    print(f"[OK] Passed: {passed}")
    if result.failures:
        print(f"[X] Failed: {len(result.failures)}")
    if result.errors:
        print(f"[X] Errors: {len(result.errors)}")
    print(f"Pass Rate: {(passed / result.testsRun * 100):.1f}%")
    print("=" * 70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
