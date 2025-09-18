#!/usr/bin/env python3
"""
Test script to test EasyScript with the User class from the attachment
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from easyscript import EasyScriptEvaluator


class User:
    """
    Simplified version of the User class from the attachment for testing
    """
    
    def __init__(self, data=None, source='unknown'):
        self._source = source
        self._raw_data = data or {}
        
        # Core identity fields
        self.id = None
        self.username = None
        self.display_name = None
        self.given_name = None
        self.surname = None
        self.email = None
        self.department = None
        self.job_title = None
        self.custom_attributes = {}
        
        # Populate from data if provided
        if data:
            self._populate_from_data(data)
    
    def _populate_from_data(self, data):
        """Populate user attributes from data dictionary"""
        # Try to map common field names
        mapping = {
            'display_name': ['displayName', 'display_name', 'fullName', 'name'],
            'given_name': ['givenName', 'given_name', 'firstName', 'first_name'],
            'surname': ['surname', 'sn', 'lastName', 'last_name'],
            'email': ['mail', 'email', 'emailAddress', 'email_address'],
            'username': ['username', 'cn', 'userPrincipalName', 'user_name'],
            'department': ['department', 'dept'],
            'job_title': ['title', 'jobTitle', 'job_title'],
        }
        
        for attr, possible_keys in mapping.items():
            for key in possible_keys:
                if key in data:
                    setattr(self, attr, data.get(key))
                    break
        
        # Store everything else in custom_attributes
        used_keys = set()
        for keys in mapping.values():
            used_keys.update(keys)
        
        for key, value in data.items():
            if key not in used_keys:
                self.custom_attributes[key] = value
    
    def __getattr__(self, name):
        """
        Dynamic attribute access for missing attributes.
        """
        print(f"User.__getattr__ called for: {name}")
        
        # First check if it's in custom_attributes
        if hasattr(self, 'custom_attributes') and name in self.custom_attributes:
            return self.custom_attributes[name]
        
        # Check raw data for eDirectory/Entra compatibility
        if hasattr(self, '_raw_data') and name in self._raw_data:
            return self._raw_data[name]
        
        # Return None for missing attributes instead of raising error
        return None
    
    def __setattr__(self, name, value):
        """
        Dynamic attribute setting for direct assignment.
        """
        print(f"User.__setattr__ called for: {name} = {value}")
        
        # Standard attributes that should be set on the object directly
        standard_attrs = {
            '_source', '_raw_data', 'id', 'username', 'display_name', 'given_name', 
            'surname', 'email', 'department', 'job_title', 'custom_attributes'
        }
        
        if name in standard_attrs:
            # Set standard attributes directly on the object
            super().__setattr__(name, value)
        else:
            # Set custom attributes in the custom_attributes dict
            # Initialize custom_attributes if it doesn't exist yet
            if not hasattr(self, 'custom_attributes'):
                super().__setattr__('custom_attributes', {})
            self.custom_attributes[name] = value
    
    def to_dict(self):
        """Convert User object to dictionary"""
        result = {}
        
        # Add all non-None attributes
        for key, value in self.__dict__.items():
            if not key.startswith('_') and value is not None:
                result[key] = value
        
        # Add custom attributes
        result.update(self.custom_attributes)
        
        return result
    
    def __str__(self):
        return f"User({self.display_name or self.username or self.id or 'Unknown'})"


def test_user_with_easyscript():
    """Test the User class with EasyScript"""
    
    print("=== Testing User Class with EasyScript ===\n")
    
    # Create a user with some initial data
    user_data = {
        'cn': 'jdoe',
        'givenName': 'John',
        'sn': 'Doe',
        'mail': 'john.doe@company.com',
        'department': 'IT',
        'title': 'Developer',
        'telephoneNumber': '+1-555-0123',
        'custom_field': 'custom_value'
    }
    
    user = User(user_data, source='edirectory')
    evaluator = EasyScriptEvaluator()
    variables = {'user': user}
    
    print("=== Initial User State ===")
    print(f"User: {user}")
    print(f"User dict: {user.to_dict()}")
    print(f"Custom attributes: {user.custom_attributes}")
    print()
    
    # Test 1: Read existing attributes
    print("=== Test 1: Reading Attributes ===")
    try:
        result = evaluator.evaluate("user.given_name", variables)
        print(f"✅ user.given_name = {result}")
    except Exception as e:
        print(f"❌ user.given_name failed: {e}")
    
    try:
        result = evaluator.evaluate("user.department", variables)
        print(f"✅ user.department = {result}")
    except Exception as e:
        print(f"❌ user.department failed: {e}")
    
    try:
        # This should trigger __getattr__ since telephoneNumber is in raw_data/custom_attributes
        result = evaluator.evaluate("user.telephoneNumber", variables)
        print(f"✅ user.telephoneNumber = {result}")
    except Exception as e:
        print(f"❌ user.telephoneNumber failed: {e}")
    
    try:
        result = evaluator.evaluate("user.custom_field", variables)
        print(f"✅ user.custom_field = {result}")
    except Exception as e:
        print(f"❌ user.custom_field failed: {e}")
    
    print()
    
    # Test 2: Modify existing attributes
    print("=== Test 2: Modifying Existing Attributes ===")
    try:
        result = evaluator.evaluate('user.department = "Engineering"', variables)
        print(f"✅ user.department assignment = {result}")
        print(f"   New department: {user.department}")
    except Exception as e:
        print(f"❌ user.department assignment failed: {e}")
    
    try:
        result = evaluator.evaluate('user.given_name = "Jonathan"', variables)
        print(f"✅ user.given_name assignment = {result}")
        print(f"   New given_name: {user.given_name}")
    except Exception as e:
        print(f"❌ user.given_name assignment failed: {e}")
    
    print()
    
    # Test 3: Add new attributes
    print("=== Test 3: Adding New Attributes ===")
    try:
        result = evaluator.evaluate('user.new_field = "new value"', variables)
        print(f"✅ user.new_field assignment = {result}")
        print(f"   Custom attributes now: {user.custom_attributes}")
    except Exception as e:
        print(f"❌ user.new_field assignment failed: {e}")
    
    try:
        result = evaluator.evaluate('user.office = "Building A"', variables)
        print(f"✅ user.office assignment = {result}")
        print(f"   Custom attributes now: {user.custom_attributes}")
    except Exception as e:
        print(f"❌ user.office assignment failed: {e}")
    
    print()
    
    # Test 4: Read back the new attributes
    print("=== Test 4: Reading Back New Attributes ===")
    try:
        result = evaluator.evaluate("user.new_field", variables)
        print(f"✅ user.new_field read back = {result}")
    except Exception as e:
        print(f"❌ user.new_field read back failed: {e}")
    
    try:
        result = evaluator.evaluate("user.office", variables)
        print(f"✅ user.office read back = {result}")
    except Exception as e:
        print(f"❌ user.office read back failed: {e}")
    
    print()
    
    # Test 5: Complex expressions
    print("=== Test 5: Complex Expressions ===")
    try:
        result = evaluator.evaluate('user.full_name = user.given_name + " " + user.surname', variables)
        print(f"✅ Complex assignment = {result}")
        print(f"   user.full_name: {evaluator.evaluate('user.full_name', variables)}")
    except Exception as e:
        print(f"❌ Complex assignment failed: {e}")
    
    try:
        result = evaluator.evaluate('if len(user.department) > 5: user.department_code = "ENG"', variables)
        print(f"✅ Conditional assignment = {result}")
        print(f"   user.department_code: {evaluator.evaluate('user.department_code', variables)}")
    except Exception as e:
        print(f"❌ Conditional assignment failed: {e}")
    
    print()
    
    # Test 6: Show final state
    print("=== Final User State ===")
    print(f"User: {user}")
    print(f"User dict: {user.to_dict()}")
    print(f"Custom attributes: {user.custom_attributes}")
    print()
    
    # Test 7: Check what changed
    print("=== What Changed? ===")
    final_dict = user.to_dict()
    print("All current user data:")
    for key, value in final_dict.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    test_user_with_easyscript()