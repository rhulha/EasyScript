#!/usr/bin/env python3
"""
Test script to demonstrate EasyScript limitations with custom __getattr__ and __setattr__ methods
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from easyscript import EasyScriptEvaluator


class DynamicAttributeObject:
    """Object with custom __getattr__ and __setattr__ methods"""
    
    def __init__(self):
        # Internal storage for dynamic attributes
        self._dynamic_attrs = {
            'name': 'Dynamic Object',
            'type': 'special',
            'value': 42
        }
        # Also have some regular attributes
        self.regular_attr = 'I am regular'
    
    def __getattr__(self, name):
        """Called when attribute is not found through normal lookup"""
        print(f"__getattr__ called for: {name}")
        if name in self._dynamic_attrs:
            return self._dynamic_attrs[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
    def __setattr__(self, name, value):
        """Called for all attribute assignments"""
        print(f"__setattr__ called for: {name} = {value}")
        if name.startswith('_') or name == 'regular_attr':
            # For internal/regular attributes, use normal assignment
            super().__setattr__(name, value)
        else:
            # For other attributes, store in dynamic storage
            if not hasattr(self, '_dynamic_attrs'):
                super().__setattr__('_dynamic_attrs', {})
            self._dynamic_attrs[name] = value


class PropertyBasedObject:
    """Object using @property decorators"""
    
    def __init__(self):
        self._data = {'computed_value': 100}
    
    @property
    def computed_value(self):
        """A computed property"""
        print("computed_value property getter called")
        return self._data['computed_value'] * 2
    
    @computed_value.setter
    def computed_value(self, value):
        """A computed property setter"""
        print(f"computed_value property setter called with: {value}")
        self._data['computed_value'] = value // 2


class ProxyObject:
    """Object that proxies to another object"""
    
    def __init__(self, target):
        self._target = target
    
    def __getattr__(self, name):
        print(f"ProxyObject.__getattr__ called for: {name}")
        return getattr(self._target, name)
    
    def __setattr__(self, name, value):
        print(f"ProxyObject.__setattr__ called for: {name} = {value}")
        if name == '_target':
            super().__setattr__(name, value)
        else:
            setattr(self._target, name, value)


def test_current_limitations():
    """Test how EasyScript currently handles custom attribute access"""
    
    print("=== Testing Current EasyScript Attribute Access ===\n")
    
    evaluator = EasyScriptEvaluator()
    
    # Test 1: Dynamic Attribute Object
    print("1. Testing DynamicAttributeObject:")
    dynamic_obj = DynamicAttributeObject()
    variables = {'obj': dynamic_obj}
    
    try:
        # This should work if EasyScript handles __getattr__ properly
        result = evaluator.evaluate("obj.name", variables)
        print(f"   ✅ obj.name = {result}")
    except Exception as e:
        print(f"   ❌ obj.name failed: {e}")
    
    try:
        # Test setting a dynamic attribute
        result = evaluator.evaluate('obj.name = "Updated Name"', variables)
        print(f"   ✅ obj.name assignment = {result}")
        print(f"      Dynamic storage: {dynamic_obj._dynamic_attrs}")
    except Exception as e:
        print(f"   ❌ obj.name assignment failed: {e}")
    
    try:
        # Test accessing a new dynamic attribute
        result = evaluator.evaluate('obj.new_field = "new value"', variables)
        print(f"   ✅ obj.new_field assignment = {result}")
        
        # Now try to read it back
        result = evaluator.evaluate("obj.new_field", variables)
        print(f"   ✅ obj.new_field read = {result}")
    except Exception as e:
        print(f"   ❌ obj.new_field operations failed: {e}")
    
    print()
    
    # Test 2: Property-based Object
    print("2. Testing PropertyBasedObject:")
    prop_obj = PropertyBasedObject()
    variables = {'obj': prop_obj}
    
    try:
        result = evaluator.evaluate("obj.computed_value", variables)
        print(f"   ✅ obj.computed_value = {result}")
    except Exception as e:
        print(f"   ❌ obj.computed_value failed: {e}")
    
    try:
        result = evaluator.evaluate('obj.computed_value = 50', variables)
        print(f"   ✅ obj.computed_value assignment = {result}")
        print(f"      Internal data: {prop_obj._data}")
    except Exception as e:
        print(f"   ❌ obj.computed_value assignment failed: {e}")
    
    print()
    
    # Test 3: Proxy Object
    print("3. Testing ProxyObject:")
    target = DynamicAttributeObject()
    proxy_obj = ProxyObject(target)
    variables = {'obj': proxy_obj}
    
    try:
        result = evaluator.evaluate("obj.name", variables)
        print(f"   ✅ obj.name (via proxy) = {result}")
    except Exception as e:
        print(f"   ❌ obj.name (via proxy) failed: {e}")
    
    try:
        result = evaluator.evaluate('obj.name = "Proxy Updated"', variables)
        print(f"   ✅ obj.name (via proxy) assignment = {result}")
        print(f"      Target storage: {target._dynamic_attrs}")
    except Exception as e:
        print(f"   ❌ obj.name (via proxy) assignment failed: {e}")


def test_manual_attribute_access():
    """Test direct Python attribute access to see what should work"""
    
    print("\n=== Testing Direct Python Attribute Access ===\n")
    
    # Test 1: Dynamic Attribute Object
    print("1. DynamicAttributeObject direct access:")
    dynamic_obj = DynamicAttributeObject()
    
    print(f"   hasattr(obj, 'name'): {hasattr(dynamic_obj, 'name')}")
    print(f"   getattr(obj, 'name'): {getattr(dynamic_obj, 'name')}")
    print(f"   Direct access obj.name: {dynamic_obj.name}")
    
    setattr(dynamic_obj, 'dynamic_field', 'dynamic_value')
    print(f"   After setattr: {dynamic_obj.dynamic_field}")
    print(f"   Storage: {dynamic_obj._dynamic_attrs}")
    
    print()
    
    # Test 2: Property-based Object
    print("2. PropertyBasedObject direct access:")
    prop_obj = PropertyBasedObject()
    
    print(f"   hasattr(obj, 'computed_value'): {hasattr(prop_obj, 'computed_value')}")
    print(f"   getattr(obj, 'computed_value'): {getattr(prop_obj, 'computed_value')}")
    print(f"   Direct access obj.computed_value: {prop_obj.computed_value}")
    
    setattr(prop_obj, 'computed_value', 150)
    print(f"   After setattr: {prop_obj.computed_value}")
    print(f"   Internal data: {prop_obj._data}")


if __name__ == "__main__":
    test_manual_attribute_access()
    test_current_limitations()