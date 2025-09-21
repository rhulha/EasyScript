"""
Test cases for the new if-else functionality in EasyScript
"""
import unittest
from easyscript.easyscript import EasyScriptEvaluator

class TestEasyScriptIfElse(unittest.TestCase):
    """Test if-else conditional statements"""

    def setUp(self):
        self.evaluator = EasyScriptEvaluator()

    def test_simple_if_else_true_condition(self):
        """Test if-else with true condition"""
        result = self.evaluator.evaluate('if 5 > 3 then "true branch" else "false branch"')
        self.assertEqual(result, "true branch")

    def test_simple_if_else_false_condition(self):
        """Test if-else with false condition"""
        result = self.evaluator.evaluate('if 2 > 5 then "true branch" else "false branch"')
        self.assertEqual(result, "false branch")

    def test_if_else_with_arithmetic(self):
        """Test if-else with arithmetic expressions"""
        result1 = self.evaluator.evaluate('if 5 > 3 then 10 + 5 else 20 + 5')
        self.assertEqual(result1, 15)
        
        result2 = self.evaluator.evaluate('if 2 > 5 then 10 + 5 else 20 + 5')
        self.assertEqual(result2, 25)

    def test_if_else_with_variables(self):
        """Test if-else with variables"""
        self.evaluator.variables['x'] = 7
        result1 = self.evaluator.evaluate('if x > 5 then x * 2 else x + 10')
        self.assertEqual(result1, 14)
        
        self.evaluator.variables['x'] = 3
        result2 = self.evaluator.evaluate('if x > 5 then x * 2 else x + 10')
        self.assertEqual(result2, 13)

    def test_if_else_in_assignment(self):
        """Test if-else in variable assignment"""
        result = self.evaluator.evaluate('result = if 5 > 3 then "success" else "failure"')
        self.assertEqual(result, "success")
        self.assertEqual(self.evaluator.variables['result'], "success")

    def test_if_else_with_boolean_values(self):
        """Test if-else returning boolean values"""
        result1 = self.evaluator.evaluate('if 5 > 3 then true else false')
        self.assertEqual(result1, True)
        
        result2 = self.evaluator.evaluate('if 2 > 5 then true else false')
        self.assertEqual(result2, False)

    def test_if_else_in_function_call(self):
        """Test if-else as function argument"""
        # Note: Using len() which doesn't have side effects
        result1 = self.evaluator.evaluate('len(if 5 > 3 then "hello" else "hi")')
        self.assertEqual(result1, 5)  # len("hello")
        
        result2 = self.evaluator.evaluate('len(if 2 > 5 then "hello" else "hi")')
        self.assertEqual(result2, 2)  # len("hi")

    def test_if_else_complex_conditions(self):
        """Test if-else with complex conditions"""
        result1 = self.evaluator.evaluate('if 5 > 3 and 10 < 20 then "both true" else "not both true"')
        self.assertEqual(result1, "both true")
        
        result2 = self.evaluator.evaluate('if 5 > 3 and 10 > 20 then "both true" else "not both true"')
        self.assertEqual(result2, "not both true")

    def test_if_else_with_string_concatenation(self):
        """Test if-else with string operations"""
        result = self.evaluator.evaluate('if 5 > 3 then "Count: " + 5 else "No count"')
        self.assertEqual(result, "Count: 5")

    def test_nested_if_else_in_expressions(self):
        """Test if-else within other expressions"""
        result = self.evaluator.evaluate('(if 5 > 3 then 10 else 0) + 5')
        self.assertEqual(result, 15)

    def test_if_else_tokenization(self):
        """Test that else is properly tokenized as a keyword"""
        tokens = self.evaluator.tokenize('if 5 > 3 then "yes" else "no"')
        else_tokens = [token for token in tokens if token.value == 'else']
        self.assertEqual(len(else_tokens), 1)
        self.assertEqual(else_tokens[0].type.name, 'KEYWORD')

if __name__ == '__main__':
    unittest.main()