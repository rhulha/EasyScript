# EasyScript Operator Precedence

## Overview

EasyScript uses a specific operator precedence hierarchy that determines the order in which operators are evaluated in expressions. Operators with higher precedence are evaluated before operators with lower precedence. When operators have the same precedence, they are evaluated from left to right (left-associative), except for assignment which is right-associative.

## Precedence Table

The following table lists all operators in EasyScript from highest to lowest precedence:

| Precedence | Operator | Description | Associativity | Example |
|------------|----------|-------------|---------------|---------|
| 1 (Highest) | `()` | Parentheses (grouping) | N/A | `(2 + 3) * 4` |
| 1 | `[]` | Indexing/Slicing | Left | `array[0]`, `string[1:3]` |
| 2 | `-` | Unary minus (negation) | Right | `-5`, `-(2 + 3)` |
| 3 | `*`, `/` | Multiplication, Division | Left | `2 * 3 + 4`, `10 / 2 * 5` |
| 4 | `+`, `-` | Addition, Subtraction | Left | `2 + 3 * 4`, `10 - 2 + 1` |
| 5 | `~` | Regex matching | Left | `"hello" ~ "h.*"`, `user.name ~ ".*@.*"` |
| 5 | `==`, `!=` | Equality, Inequality | Left | `5 == 3 + 2`, `name != "admin"` |
| 5 | `<`, `>`, `<=`, `>=` | Comparison operators | Left | `age > 18`, `score <= 100` |
| 6 | `not` | Logical NOT | Right | `not true`, `not user.active` |
| 7 | `and` | Logical AND | Left | `x > 5 and y < 10` |
| 8 | `or` | Logical OR | Left | `x > 5 or y < 10` |
| 9 | `if-then-else` | Conditional expression | N/A | `if x > 5 then "big" else "small"` |
| 10 (Lowest) | `=` | Assignment | Right | `user.age = 25`, `x = y = 5` |

## Detailed Explanations

### 1. Parentheses and Indexing (Highest Precedence)

Parentheses override all other precedence rules and force evaluation order:

```easyscript
(2 + 3) * 4  # Evaluates to 20, not 14
```

Indexing and slicing operations have the highest precedence and are applied immediately to the preceding expression:

```easyscript
array[0] + 1      # Index first, then add
string[1:3] + "x" # Slice first, then concatenate
```

### 2. Unary Operators

The unary minus operator has higher precedence than binary arithmetic operators:

```easyscript
-2 + 3    # Evaluates to 1, not -5
-(2 + 3)  # Use parentheses for -5
```

### 3. Arithmetic Operators

Multiplication and division have higher precedence than addition and subtraction:

```easyscript
2 + 3 * 4    # Evaluates to 14, not 20
2 * 3 + 4 * 5  # Evaluates to 26
```

### 4. Comparison and Regex Operators

All comparison operators and the regex matching operator have the same precedence and are left-associative:

```easyscript
5 < 10 == true     # Evaluates to true
"hello" ~ "h.*"    # Regex matching
user.age > 18 and user.active  # Comparison before logical AND
```

### 5. Logical NOT

The `not` operator has higher precedence than `and`/`or` but lower precedence than comparison operators:

```easyscript
not user.active and user.admin  # Equivalent to: (not user.active) and user.admin
not user.age > 18               # Equivalent to: not (user.age > 18)
```

### 6. Logical AND and OR

`and` has higher precedence than `or`:

```easyscript
x > 5 and y < 10 or z == 0  # Equivalent to: (x > 5 and y < 10) or z == 0
```

### 7. Conditional Expressions

The `if-then-else` construct has very low precedence and can contain full expressions:

```easyscript
if x > 5 and y < 10 then x + y else x - y
```

### 8. Assignment (Lowest Precedence)

Assignment has the lowest precedence and is right-associative:

```easyscript
x = y = z = 5  # All variables get value 5
user.age = 25 + 5  # Addition happens before assignment
```

## Common Precedence Pitfalls

### Logical NOT with Comparisons

```easyscript
not user.dn ~ "Abgang"  # Correctly evaluates as: not (user.dn ~ "Abgang")
# NOT: (not user.dn) ~ "Abgang" (which would be invalid)
```

### Arithmetic and Comparison

```easyscript
x + y > z  # Equivalent to: (x + y) > z
# NOT: x + (y > z)
```

### Logical Operators

```easyscript
a or b and c  # Equivalent to: a or (b and c)
# NOT: (a or b) and c

not a and b   # Equivalent to: (not a) and b
# NOT: not (a and b)
```

## Associativity Rules

- **Left-associative**: Most operators evaluate from left to right
- **Right-associative**: Assignment and unary operators evaluate from right to left

```easyscript
a = b = c = 5    # Right-associative: a = (b = (c = 5))
2 - 3 - 4        # Left-associative: (2 - 3) - 4 = -5
```

## Using Parentheses

When in doubt, use parentheses to make precedence explicit:

```easyscript
(not user.active) and user.admin  # Explicit precedence
(user.age > 18) or (user.role == "admin")  # Clear grouping
(x + y) * (a - b)  # Force arithmetic order
```

## Implementation Notes

EasyScript's precedence is implemented through a recursive descent parser with the following parsing hierarchy:

1. `parse_expression()` → `parse_assignment()`
2. `parse_assignment()` → `parse_conditional_expression()`
3. `parse_conditional_expression()` → `parse_or_expression()`
4. `parse_or_expression()` → `parse_and_expression()`
5. `parse_and_expression()` → `parse_not_expression()`
6. `parse_not_expression()` → `parse_comparison()`
7. `parse_comparison()` → `parse_additive()`
8. `parse_additive()` → `parse_multiplicative()`
9. `parse_multiplicative()` → `parse_unary()`
10. `parse_unary()` → `parse_primary()`

Each level handles operators of a specific precedence, ensuring correct evaluation order.