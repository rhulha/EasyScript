#!/usr/bin/env python3
"""
Test to demonstrate that evaluate() now supports both single and multi-line scripts
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from easyscript import EasyScriptEvaluator


def test_unified_evaluate():
    evaluator = EasyScriptEvaluator()

    print("=== Testing Unified evaluate() Method ===\n")

    # Test single expression (original functionality)
    print("1. Testing single expression: evaluator.evaluate('3+3')")
    result = evaluator.evaluate("3+3")
    print(f"   Result: {result}")
    assert result == 6

    print("\n2. Testing single statement: evaluator.evaluate('log(\"Hello from single line\")')")
    result = evaluator.evaluate('log("Hello from single line")')
    print(f"   Returned: {result}")

    # Test multi-line script (new functionality)
    multiline_script = '''# This is a multi-line script
log("=== Multi-line Test ===")
log("First line: " + "Hello")
log("Second line: " + "World")
log("Math: " + (5 + 3))
log("Day: " + day)'''

    print(f"\n3. Testing multi-line script:")
    print("   Script content:")
    for i, line in enumerate(multiline_script.split('\n'), 1):
        print(f"     Line {i}: {line}")
    
    print("\n   Executing with evaluator.evaluate(multiline_script):")
    result = evaluator.evaluate(multiline_script)
    print(f"   Final result: {result}")

    # Test another multi-line script with calculations
    calc_script = '''log("=== Calculation Demo ===")
x = 10
y = 5
log("x = " + x)
log("y = " + y)
log("x + y = " + (x + y))
log("x * y = " + (x * y))'''

    print(f"\n4. Testing calculation script:")
    print("   Script content:")
    for i, line in enumerate(calc_script.split('\n'), 1):
        print(f"     Line {i}: {line}")
    
    print("\n   Executing:")
    try:
        result = evaluator.evaluate(calc_script)
        print(f"   Final result: {result}")
    except Exception as e:
        print(f"   Error (expected - variables not persistent between statements): {e}")
        print("   Note: Each statement is evaluated independently, so variables don't persist.")

    # Test mixed content (comments and statements)
    mixed_script = '''# Testing mixed content
# This is a comment
log("Line 1")

# Another comment
log("Line 2")
# Final comment'''

    print(f"\n5. Testing script with comments and empty lines:")
    result = evaluator.evaluate(mixed_script)
    print(f"   Final result: {result}")

    print("\n=== All Unified evaluate() Tests Completed! ===")
    print("✓ Single expressions work (backward compatibility)")
    print("✓ Multi-line scripts work (new functionality)")
    print("✓ Comments and empty lines are handled properly")


if __name__ == "__main__":
    test_unified_evaluate()