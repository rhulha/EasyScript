# Additional test with different values
a = 2
b = "Hello"

log("a = " + a)
log("b = " + b)

# Test with different condition result
log(if a > 3: "a is greater than 3" else: "a is not greater than 3")

# Test nested in arithmetic
result = if a > 3: 100 else: 50
log("Result: " + result)

# Test with boolean values
flag = if a > 3: true else: false
log("Flag: " + flag)

log("Hello from EasyScript!")

"Final result: else support added successfully!"