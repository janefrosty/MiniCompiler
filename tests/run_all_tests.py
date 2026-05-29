#!/usr/bin/env python3
"""
Run all test suites for MiniCompiler.
Usage: python run_all_tests.py
"""

import subprocess
import sys
import os

def run_tests(pattern):
    """Run pytest with given pattern"""
    cmd = [sys.executable, "-m", "pytest", pattern, "-v", "--tb=short"]
    print(f"\n{'='*60}")
    print(f"Running: {' '.join(cmd)}")
    print(f"{'='*60}")
    result = subprocess.run(cmd)
    return result.returncode

def main():
    """Run all test suites"""
    test_files = [
        "test_sprint_1_lexer.py",
        "test_sprint_2_parser.py",
        "test_sprint_3_semantic.py",
        "test_sprint_4_ir.py",
        "test_sprint_5_codegen.py",
        "test_sprint_6_control_flow.py",
        "test_sprint_7_arrays.py",
    ]
    
    exit_codes = []
    for test_file in test_files:
        rc = run_tests(test_file)
        exit_codes.append(rc)
    
    print("\n" + "="*60)
    print("Running all tests together (integration check)")
    print("="*60)
    rc = subprocess.run([sys.executable, "-m", "pytest", ".", "-v", "--tb=short"])
    exit_codes.append(rc.returncode)
    
    if any(ec != 0 for ec in exit_codes):
        print("\n Some tests failed!")
        sys.exit(1)
    else:
        print("\n All tests passed!")

if __name__ == "__main__":
    main()