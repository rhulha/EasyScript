#!/usr/bin/env python3
"""
Test script using the actual User class from the attachment
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from easyscript import EasyScriptEvaluator

# Copy the actual User class from the attachment
# (Simplified version for testing - the key parts are __getattr__ and __setattr__)

class User:
    """
    User class from the attachment (key functionality)
    """
    
    def __init__(self, data=None, source='unknown'):
        self._source = source
        self._raw_data = data or {}
        
        # Core identity fields (common to both systems)
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
        if self._source == 'edirectory':
            self._populate_from_edirectory(data)
        else:
            self._populate_generic(data)
    
    def _populate_from_edirectory(self, data):
        """Populate from eDirectory LDAP data"""
        # Core identity
        self.username = data.get('cn')
        self.id = data.get('cn')
        
        # Name fields
        self.given_name = data.get('givenName')
        self.surname = data.get('sn') or data.get('surname')
        self.display_name = data.get('displayName') or data.get('fullName')
        
        # Email
        self.email = data.get('mail') or data.get('internetEmailAddress')
        
        # Extended attributes
        self.department = data.get('department') or data.get('ou')
        self.job_title = data.get('title')
        
        # Store all other attributes in custom_attributes
        excluded_keys = {
            'cn', 'givenName', 'sn', 'surname', 'displayName', 'fullName', 'mail', 
            'internetEmailAddress', 'department', 'ou', 'title'
        }
        
        for key, value in data.items():
            if key not in excluded_keys:
                self.custom_attributes[key] = value
    
    def _populate_generic(self, data):
        """Generic population for unknown data sources"""
        # Try to map common field names
        mapping = {
            'display_name': ['displayName', 'display_name', 'fullName', 'name'],
            'given_name': ['givenName', 'given_name', 'firstName', 'first_name'],
            'surname': ['surname', 'sn', 'lastName', 'last_name'],
            'email': ['mail', 'email', 'emailAddress', 'email_address'],
            'username': ['username', 'cn', 'userPrincipalName', 'user_name'],
            'department': ['department', 'dept'],
            'job_title': ['title', 'jobTitle', 'job_title']
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
        This allows accessing custom_attributes while following Python conventions.
        """
        # First check if it's in custom_attributes
        if hasattr(self, 'custom_attributes') and name in self.custom_attributes:
            return self.custom_attributes[name]
        
        # Raise AttributeError for truly missing attributes (standard Python behavior)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
    def __setattr__(self, name, value):
        """
        Dynamic attribute setting for direct assignment.
        """
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


def track_changes_demo():
    """Demonstrate how to track changes to a User object through EasyScript"""
    
    print("=== Tracking Changes Demo ===\n")
    
    # Create initial user
    user_data = {
        'cn': 'jsmith',
        'givenName': 'Jane',
        'sn': 'Smith',
        'mail': 'jane.smith@company.com',
        'department': 'Sales',
        'title': 'Sales Manager',
        'telephoneNumber': '+1-555-9876'
    }
    
    user = User(user_data, source='edirectory')
    evaluator = EasyScriptEvaluator()
    variables = {'user': user}
    
    # Capture initial state
    initial_state = user.to_dict().copy()
    print("=== Initial State ===")
    for key, value in initial_state.items():
        if key != 'custom_attributes':  # Skip the dict itself, its contents are already shown
            print(f"  {key}: {value}")
    print()
    
    # Perform some EasyScript operations
    print("=== Performing EasyScript Operations ===")
    
    operations = [
        'user.department = "Marketing"',
        'user.given_name = "Janet"', 
        'user.salary = 75000',
        'user.manager = "John Doe"',
        'user.full_name = user.given_name + " " + user.surname',
        'if len(user.department) > 6: user.dept_code = "MKT"'
    ]
    
    for operation in operations:
        try:
            result = evaluator.evaluate(operation, variables)
            print(f"✅ {operation} → {result}")
        except Exception as e:
            print(f"❌ {operation} → {e}")
    
    print()
    
    # Capture final state
    final_state = user.to_dict().copy()
    print("=== Final State ===")
    for key, value in final_state.items():
        if key != 'custom_attributes':  # Skip the dict itself
            print(f"  {key}: {value}")
    print()
    
    # Show what changed
    print("=== Changes Detected ===")
    changes = {}
    
    # Find modified standard attributes
    for key, value in final_state.items():
        if key in initial_state:
            if initial_state[key] != value:
                changes[key] = {'old': initial_state[key], 'new': value}
        else:
            # New attribute
            changes[key] = {'old': None, 'new': value}
    
    # Find deleted attributes (though this shouldn't happen in our test)
    for key in initial_state:
        if key not in final_state:
            changes[key] = {'old': initial_state[key], 'new': None}
    
    if changes:
        for key, change in changes.items():
            if key != 'custom_attributes':  # Handle custom_attributes separately
                if change['old'] is None:
                    print(f"  NEW: {key} = {change['new']}")
                elif change['new'] is None:
                    print(f"  DELETED: {key} (was {change['old']})")
                else:
                    print(f"  MODIFIED: {key} = {change['old']} → {change['new']}")
    else:
        print("  No changes detected")
    
    print()
    
    # Show specific custom attributes that were added/changed
    print("=== Custom Attributes Added/Changed ===")
    if 'custom_attributes' in final_state:
        for key, value in final_state['custom_attributes'].items():
            initial_custom = initial_state.get('custom_attributes', {})
            if key not in initial_custom:
                print(f"  NEW CUSTOM: {key} = {value}")
            elif initial_custom[key] != value:
                print(f"  MODIFIED CUSTOM: {key} = {initial_custom[key]} → {value}")
    
    return initial_state, final_state, changes


def test_easyscript_proxy_object():
    """Test the to_easyscript_object() method if we implement it"""
    
    print("\n=== Testing Simple Proxy Approach ===\n")
    
    # Create a user
    user_data = {
        'cn': 'tester',
        'givenName': 'Test',
        'sn': 'User',
        'department': 'QA'
    }
    
    user = User(user_data, source='edirectory')
    
    # Create a simple proxy object that EasyScript might handle better
    class SimpleUserProxy:
        def __init__(self, user_obj):
            self._original_user = user_obj
            # Copy all current attributes to this simple object
            user_dict = user_obj.to_dict()
            for key, value in user_dict.items():
                if key != 'custom_attributes':
                    setattr(self, key, value)
            
            # Also copy custom attributes directly as properties
            for key, value in user_obj.custom_attributes.items():
                setattr(self, key, value)
        
        def sync_back(self):
            """Sync changes back to the original user"""
            for key, value in self.__dict__.items():
                if not key.startswith('_'):
                    # Set on original user - will use its __setattr__ logic
                    setattr(self._original_user, key, value)
    
    # Test with the proxy
    proxy = SimpleUserProxy(user)
    evaluator = EasyScriptEvaluator()
    variables = {'user': proxy}
    
    print("Testing with simple proxy object:")
    
    # Test operations
    operations = [
        'user.department = "Development"',
        'user.new_attribute = "test_value"',
        'user.computed = user.given_name + "_" + user.surname'
    ]
    
    for operation in operations:
        try:
            result = evaluator.evaluate(operation, variables)
            print(f"✅ {operation} → {result}")
        except Exception as e:
            print(f"❌ {operation} → {e}")
    
    # Sync back to original user
    proxy.sync_back()
    
    print(f"\nOriginal user after sync: {user.to_dict()}")


if __name__ == "__main__":
    track_changes_demo()
    test_easyscript_proxy_object()