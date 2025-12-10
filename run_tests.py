#!/usr/bin/env python3
"""
Test Runner for Study Progress Tracker
Run specific test suites or all tests
"""

import sys
import unittest
import argparse
from test_study_tracker import (
    TestDatabaseManager,
    TestAppLogic,
    TestExamGenerator,
    TestCodingGenerator,
    TestOllamaIntegration,
    TestIntegration
)


def run_specific_tests(test_names):
    """Run specific test suites"""
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    
    test_map = {
        'database': TestDatabaseManager,
        'db': TestDatabaseManager,
        'app': TestAppLogic,
        'logic': TestAppLogic,
        'exam': TestExamGenerator,
        'coding': TestCodingGenerator,
        'ollama': TestOllamaIntegration,
        'integration': TestIntegration,
        'int': TestIntegration
    }
    
    for name in test_names:
        if name.lower() in test_map:
            suite.addTests(loader.loadTestsFromTestCase(test_map[name.lower()]))
        else:
            print(f"Warning: Unknown test suite '{name}'")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


def run_all_tests():
    """Run all test suites"""
    from test_study_tracker import run_tests
    return run_tests()


def list_available_tests():
    """List all available test suites"""
    print("\n📋 Available Test Suites:\n")
    print("  database (db)     - Database operations and CRUD tests")
    print("  app (logic)       - Application logic and business rules")
    print("  exam              - Exam generation and validation")
    print("  coding            - Coding problem generation")
    print("  ollama            - Ollama integration tests")
    print("  integration (int) - End-to-end integration tests")
    print("\nExamples:")
    print("  python run_tests.py --all")
    print("  python run_tests.py database app")
    print("  python run_tests.py integration")
    print()


def main():
    parser = argparse.ArgumentParser(
        description='Run tests for Study Progress Tracker',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'tests',
        nargs='*',
        help='Specific test suites to run (e.g., database, app, exam)'
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='Run all test suites'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List available test suites'
    )
    
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_available_tests()
        return 0
    
    print("\n" + "="*70)
    print("🧪 STUDY PROGRESS TRACKER - TEST SUITE")
    print("="*70 + "\n")
    
    if args.all or not args.tests:
        print("Running all tests...\n")
        success = run_all_tests()
    else:
        print(f"Running tests: {', '.join(args.tests)}\n")
        success = run_specific_tests(args.tests)
    
    if success:
        print("\n✅ All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed!")
        return 1


if __name__ == '__main__':
    sys.exit(main())