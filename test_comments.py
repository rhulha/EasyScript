#!/usr/bin/env python3
"""
Test script to verify comment functionality in EasyScript
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from easyscript import EasyScriptEvaluator


def test_comment_functionality():
    """Test various comment scenarios"""
    evaluator = EasyScriptEvaluator()
    
    # Basic comment tests
    test_cases = [
        # Basic inline comments
        ("5 + 3 # This is a comment", 8),
        ("5 + 3 # + 999", 8),  # Should be 8, not 1007 (regression test)
        ('"hello" + "world" # comment', "helloworld"),
        ("5 + 3 # invalid syntax here !@#$%^&*()", 8),
        
        # Comments without spaces
        ("5+3#comment", 8),
        ("10*2#multiply", 20),
        
        # Full line comments
        ("# This is a full line comment\n5 + 3", 8),
        ("# Comment 1\n# Comment 2\n5 + 3", 8),
        
        # Multi-line expressions with comments
        ("5 # first number\n+ 3 # second number", 8),
        ("5 # comment\n+ 3\n* 2 # final operation", 11),  # 5 + 3 * 2 = 5 + 6 = 11 due to operator precedence
        
        # Comments with various EasyScript features
        ('if 5 > 3: true # condition comment', True),
        ('len("hello") # string length comment', 5),
        ("year # current year", 2025),  # Assuming current year
        
        # Edge cases
        ("5 + 3#", 8),  # Comment with no text
        ("5 + 3 #", 8),  # Comment with space but no text
        
        # No comments (regression test)
        ("5 + 3", 8),
        ('"hello world"', "hello world"),
    ]
    
    print("Testing EasyScript Comment Functionality")
    print("=" * 50)
    
    passed = 0
    total = len(test_cases)
    
    for i, (expression, expected) in enumerate(test_cases, 1):
        print(f"\nTest {i:2d}: {expression!r}")
        try:
            result = evaluator.evaluate(expression)
            if result == expected or (i == 12 and isinstance(result, int)):  # year test
                print(f"         PASS - Result: {result}")
                passed += 1
            else:
                print(f"         FAIL - Result: {result}, Expected: {expected}")
        except Exception as e:
            print(f"         ERROR - {e}")
    
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} tests passed")
    
    # Test tokenization
    print(f"\n{'='*50}")
    print("Tokenization Test:")
    tokens = evaluator.tokenize("5 + 3 # This is a comment")
    print("Expression: '5 + 3 # This is a comment'")
    print("Tokens:")
    for token in tokens:
        print(f"  {token.type.value:12} : {token.value!r}")
    
    return passed == total


def test_with_user_object():
    """Test comments with user object injection"""
    evaluator = EasyScriptEvaluator()
    
    class User:
        def __init__(self):
            self.cn = "John Doe"
            self.mail = "john@example.com"
            self.department = "Engineering"
    
    user = User()
    variables = {"user": user}
    
    user_test_cases = [
        ('user.cn # get common name', "John Doe"),
        ('user.mail # get email address', "john@example.com"),
        ('len(user.cn) > 5 # check name length', True),
        ('user.mail ~ ".*@.*" # email validation', True),
        ('if len(user.cn) > 3: user.department # conditional', "Engineering"),
    ]
    
    print(f"\n{'='*50}")
    print("Testing Comments with User Object:")
    
    passed = 0
    total = len(user_test_cases)
    
    for i, (expression, expected) in enumerate(user_test_cases, 1):
        print(f"\nUser Test {i}: {expression!r}")
        try:
            result = evaluator.evaluate(expression, variables)
            if result == expected:
                print(f"              PASS - Result: {result}")
                passed += 1
            else:
                print(f"              FAIL - Result: {result}, Expected: {expected}")
        except Exception as e:
            print(f"              ERROR - {e}")
    
    print(f"\n{'='*50}")
    print(f"User Object Tests: {passed}/{total} tests passed")
    
    return passed == total


if __name__ == "__main__":
    print("EasyScript Comment Support Test Suite")
    print("=" * 60)
    
    basic_passed = test_comment_functionality()
    user_passed = test_with_user_object()
    
    print(f"\n{'='*60}")
    print("FINAL RESULTS:")
    print(f"Basic Comment Tests: {'PASS' if basic_passed else 'FAIL'}")
    print(f"User Object Tests:   {'PASS' if user_passed else 'FAIL'}")
    print(f"Overall Status:      {'PASS' if basic_passed and user_passed else 'FAIL'}")
    
    if basic_passed and user_passed:
        print("\n🎉 All comment functionality tests passed!")
        print("Comment support using '#' character has been successfully implemented.")
    else:
        print("\n❌ Some tests failed. Please review the implementation.")