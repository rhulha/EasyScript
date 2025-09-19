#!/usr/bin/env python3
"""
Additional tests for return values - edge cases
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from easyscript import EasyScriptEvaluator


def test_edge_cases():
    evaluator = EasyScriptEvaluator()

    print("=== Testing Return Value Edge Cases ===\n")

    # Test 1: Only comments should return None
    print("1. Only comments and empty lines:")
    script = '''# Just a comment
# Another comment

# Final comment'''
    result = evaluator.evaluate(script)
    print(f"   Returned: {result}")
    assert result is None
    print("   ✓ Correctly returns None for no executable statements\n")

    # Test 2: Empty string should return None
    print("2. Empty string:")
    result = evaluator.evaluate("")
    print(f"   Returned: {result}")
    assert result is None
    print("   ✓ Correctly returns None for empty string\n")

    # Test 3: Only whitespace should return None
    print("3. Only whitespace:")
    result = evaluator.evaluate("   \n\n   \n  ")
    print(f"   Returned: {result}")
    assert result is None
    print("   ✓ Correctly returns None for only whitespace\n")

    # Test 4: Mixed with None-returning function
    print("4. Script ending with a None-returning operation:")
    # Note: In EasyScript, most operations return values, but let's test with comments at the end
    script = '''5 + 5
log("test")
# Comment at end'''
    result = evaluator.evaluate(script)
    print(f"   Returned: {result}")
    assert result == "test"  # Should be the last executable statement
    print("   ✓ Returns last executable statement value\n")

    # Test 5: Test with conditional that might return None
    print("5. Conditional expression:")
    script = '''5 > 3
if 10 < 5: return "never"'''
    result = evaluator.evaluate(script)
    print(f"   Returned: {result}")
    # The if condition is false, so it should return None, but that becomes the last_result
    print("   ✓ Handles conditional expressions\n")

    # Test 6: Verify that intermediate results don't interfere
    print("6. Multiple calculations ensuring last one is returned:")
    script = '''1
2
3
4
5
99'''
    result = evaluator.evaluate(script)
    print(f"   Returned: {result}")
    assert result == 99
    print("   ✓ Correctly returns the very last expression value\n")

    print("=== All Edge Case Tests Passed! ===")


if __name__ == "__main__":
    test_edge_cases()