#!/usr/bin/env python3
"""
Test runner for SimpleMusic library.
"""

import sys
import subprocess
from pathlib import Path

def run_test_file(test_file):
    """Run a single test file"""
    print(f"\n{'='*50}")
    print(f"Running {test_file.name}")
    print('='*50)
    
    result = subprocess.run([sys.executable, str(test_file)], 
                          capture_output=False)
    
    return result.returncode == 0

def main():
    """Run all tests"""
    tests_dir = Path("tests")
    test_files = list(tests_dir.glob("test_*.py"))
    
    if not test_files:
        print("No test files found in tests/ directory")
        return False
    
    print(f"Found {len(test_files)} test files")
    
    passed = 0
    failed = 0
    
    for test_file in sorted(test_files):
        if run_test_file(test_file):
            passed += 1
        else:
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Test Results: {passed} passed, {failed} failed")
    print('='*50)
    
    if failed == 0:
        print("🎉 All tests passed!")
        return True
    else:
        print(f"❌ {failed} tests failed!")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)