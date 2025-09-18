# EasyScript Test Suite Documentation

## Overview
This directory contains a comprehensive unit test suite for EasyScript that covers all functionality with proper assertions and error handling.

## Test Files

### `test_easyscript_comprehensive.py`
**Main comprehensive test suite** - Contains all unit tests organized into logical test classes:

#### Test Classes:

**`TestEasyScriptBasics`** - Basic EasyScript functionality
- Arithmetic operations (+, -, *, /, order of operations)
- String operations and concatenation
- Comparison operations (>, <, >=, <=, ==, !=)
- Boolean operations (and, or, true/false)
- Built-in variables (day, month, year)
- Built-in functions (len, log)
- Regex operator (~)
- Conditional statements (if statements)
- Complex nested expressions

**`TestEasyScriptTokenizer`** - Tokenizer functionality
- Number tokenization (integers, floats)
- String tokenization (including empty strings)
- Identifier tokenization (variables, function names)
- Keyword tokenization (if, return, and, or, etc.)
- Operator tokenization (all operators including new assignment operator)
- Punctuation tokenization (parentheses, colons, etc.)

**`TestEasyScriptObjectHandling`** - Object property access and assignment
- Property access (user.name, user.email, etc.)
- Property use in expressions
- Property assignment (user.department = "new value")
- Conditional assignment
- Multiple object injection

**`TestEasyScriptErrorHandling`** - Error handling and edge cases
- Undefined variable errors
- Undefined property errors
- Invalid function errors
- Function argument errors
- Invalid regex errors
- Syntax errors
- Type errors
- Division by zero

**`TestEasyScriptEdgeCases`** - Edge cases and boundary conditions
- Empty strings
- Zero values
- Whitespace handling
- Nested parentheses
- Boolean edge cases
- Special characters in strings
- Large numbers
- Float precision

**`TestEasyScriptIntegration`** - Integration tests
- LDAP user transformation scenarios
- Complex conditional logic
- Mathematical expressions with variables
- Real-world usage patterns

### `run_tests.py`
**Test runner script** - Discovers and runs all tests with detailed output and summary.

### `test_helpers.py`
**Test helper classes** - Contains the `LDAPUser` class for testing object injection.

### Legacy Files
- `test_easyscript_legacy.py` - Original basic tests (now deprecated)
- `test_easyscript_user_legacy.py` - Original user tests (now deprecated)

## Running Tests

### Run All Tests
```bash
python tests/run_tests.py
```

### Run Specific Test File
```bash
python tests/test_easyscript_comprehensive.py
```

### Run Specific Test Class
```bash
python -m unittest test_easyscript_comprehensive.TestEasyScriptBasics
```

### Run Specific Test Method
```bash
python -m unittest test_easyscript_comprehensive.TestEasyScriptBasics.test_arithmetic_operations
```

## Test Coverage

The test suite provides comprehensive coverage of:

✅ **Tokenizer**: All token types and edge cases  
✅ **Parser**: All expression types and precedence rules  
✅ **Evaluator**: All operations and built-in functions  
✅ **Assignment**: Property assignment and error handling  
✅ **Objects**: Property access and manipulation  
✅ **Error Handling**: All error conditions and edge cases  
✅ **Integration**: Real-world usage scenarios  

## Test Statistics

- **Total Tests**: 41 unit tests
- **Test Classes**: 6 main test classes
- **Coverage Areas**: Tokenizer, Parser, Objects, Errors, Edge Cases, Integration
- **Assertions**: Proper unittest assertions with descriptive error messages
- **Error Testing**: Comprehensive error condition testing with `assertRaises`

## Adding New Tests

When adding new functionality to EasyScript:

1. **Add unit tests** to the appropriate test class in `test_easyscript_comprehensive.py`
2. **Include error tests** in `TestEasyScriptErrorHandling` for error conditions
3. **Add edge case tests** in `TestEasyScriptEdgeCases` for boundary conditions
4. **Create integration tests** in `TestEasyScriptIntegration` for complex scenarios
5. **Run the full test suite** to ensure no regressions

## Best Practices

- Use `self.subTest()` for testing multiple similar cases
- Use descriptive test method names that explain what is being tested
- Include both positive and negative test cases
- Test error conditions with `assertRaises`
- Use proper assertions (`assertEqual`, `assertTrue`, etc.) instead of print statements
- Group related tests in logical test classes
- Include docstrings explaining what each test class/method does

## Test Philosophy

This test suite follows unit testing best practices:
- **Fast**: Tests run quickly (< 1 second total)
- **Independent**: Each test can run in isolation
- **Repeatable**: Tests produce the same results every time
- **Self-validating**: Tests have clear pass/fail criteria
- **Timely**: Tests are written alongside the code they test

The comprehensive nature of this test suite ensures that EasyScript is robust, reliable, and maintains backward compatibility as new features are added.