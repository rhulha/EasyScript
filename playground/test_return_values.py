#!/usr/bin/env python3
"""
Test to confirm that the last expression value is returned correctly
in both single and multi-line scenarios
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from easyscript import EasyScriptEvaluator


def test_return_values():
    evaluator = EasyScriptEvaluator()

    print("=== Testing Return Values ===\n")

    # Test 1: Single expression should return its value
    print("1. Single expression: '3 + 4'")
    result = evaluator.evaluate("3 + 4")
    print(f"   Returned: {result}")
    print(f"   Type: {type(result)}")
    assert result == 7
    print("   ✓ Correct value returned\n")

    # Test 2: Single statement should return its value
    print("2. Single statement: 'len(\"hello\")'")
    result = evaluator.evaluate('len("hello")')
    print(f"   Returned: {result}")
    assert result == 5
    print("   ✓ Correct value returned\n")

    # Test 3: Multi-line script should return LAST expression value
    print("3. Multi-line script:")
    script = '''5 + 5
10 * 2
3 + 7'''
    print("   Script:")
    for i, line in enumerate(script.split('\n'), 1):
        print(f"     Line {i}: {line}")
    
    result = evaluator.evaluate(script)
    print(f"   Returned: {result}")
    assert result == 10  # Should be the result of the last line (3 + 7)
    print("   ✓ Last expression value returned correctly\n")

    # Test 4: Multi-line with log statements (log returns the value it prints)
    print("4. Multi-line with log statements:")
    script = '''log("First")
log("Second")
log("Third")'''
    print("   Script:")
    for i, line in enumerate(script.split('\n'), 1):
        print(f"     Line {i}: {line}")
    
    result = evaluator.evaluate(script)
    print(f"   Returned: {result}")
    assert result == "Third"  # log() returns the value it logs
    print("   ✓ Last log return value returned correctly\n")

    # Test 5: Mixed expressions and log statements
    print("5. Mixed expressions and log statements:")
    script = '''log("Starting")
5 * 3
log("Middle")
100 / 10'''
    print("   Script:")
    for i, line in enumerate(script.split('\n'), 1):
        print(f"     Line {i}: {line}")
    
    result = evaluator.evaluate(script)
    print(f"   Returned: {result}")
    assert result == 10.0  # Should be the result of last line (100 / 10)
    print("   ✓ Last expression value returned correctly\n")

    # Test 6: Multi-line with boolean expressions
    print("6. Multi-line with boolean expressions:")
    script = '''5 > 3
10 < 5
true and false
not false'''
    print("   Script:")
    for i, line in enumerate(script.split('\n'), 1):
        print(f"     Line {i}: {line}")
    
    result = evaluator.evaluate(script)
    print(f"   Returned: {result}")
    assert result == True  # Should be the result of last line (not false)
    print("   ✓ Last boolean value returned correctly\n")

    # Test 7: Multi-line with string operations
    print("7. Multi-line with string operations:")
    script = '''"Hello" + " World"
"Test" + 123
len("EasyScript")'''
    print("   Script:")
    for i, line in enumerate(script.split('\n'), 1):
        print(f"     Line {i}: {line}")
    
    result = evaluator.evaluate(script)
    print(f"   Returned: {result}")
    assert result == 10  # Should be the result of last line len("EasyScript")
    print("   ✓ Last string operation value returned correctly\n")

    # Test 8: Test with comments and empty lines (should ignore them)
    print("8. Multi-line with comments and empty lines:")
    script = '''# This is a comment
5 + 5

# Another comment
10 * 2

# Final calculation
3 * 4'''
    print("   Script:")
    for i, line in enumerate(script.split('\n'), 1):
        print(f"     Line {i}: {repr(line)}")
    
    result = evaluator.evaluate(script)
    print(f"   Returned: {result}")
    assert result == 12  # Should be the result of last meaningful line (3 * 4)
    print("   ✓ Comments and empty lines ignored correctly\n")

    print("=== All Return Value Tests Passed! ===")
    print("✓ Single expressions return their value")
    print("✓ Multi-line scripts return the value of the LAST statement")
    print("✓ Comments and empty lines are properly ignored")
    print("✓ All data types (int, float, bool, string) are returned correctly")


if __name__ == "__main__":
    test_return_values()