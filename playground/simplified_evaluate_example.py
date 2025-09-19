#!/usr/bin/env python3
"""
Simplified version showing how evaluate() could work without single-line detection
"""

def simplified_evaluate(self, code: str, variables: Optional[Dict[str, Any]] = None) -> Any:
    """
    Evaluate EasyScript code (single line or multi-line) - SIMPLIFIED VERSION
    """
    if variables:
        self.variables.update(variables)

    # Split code into individual lines and filter out comments and empty lines
    lines = code.split('\n')
    statements = []
    
    for line in lines:
        line = line.strip()
        # Skip empty lines and comment lines
        if line and not line.startswith('#'):
            statements.append(line)
    
    # Handle edge case of no statements
    if not statements:
        return None
    
    last_result = None
    
    # Execute each statement (works for both single and multiple statements)
    for statement in statements:
        try:
            self.tokens = self.tokenize(statement)
            self.current_token_index = 0
            last_result = self.parse_statement()
        except Exception as e:
            # Enhanced error messages for all cases
            raise Exception(f"Error in statement '{statement}': {e}")
    
    return last_result