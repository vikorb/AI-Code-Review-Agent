#!/usr/bin/env python3
"""
Run all unit tests for the Code Review Agent.
"""

import unittest
import os
import sys

# Ensure tests directory is in the path
tests_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
if not os.path.exists(tests_dir):
    os.makedirs(tests_dir)

# Discover and run all tests
if __name__ == "__main__":
    # Add the parent directory to the path so we can import the package
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    print("Running Code Review Agent tests...")
    
    # Discover all tests in the tests directory
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover("tests")
    
    # Run tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Exit with non-zero code if tests failed
    sys.exit(not result.wasSuccessful())