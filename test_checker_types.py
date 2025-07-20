#!/usr/bin/env python3
"""
Test Script for Problem Checker Types
This script tests the different output checker types to ensure they work correctly.
"""

import sys
import os

# Add the current directory to Python path to import from app.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the checker function from app.py
from app import check_output_flexible

def test_exact_match():
    """Test exact match checker"""
    print("🧪 Testing Exact Match Checker")
    print("-" * 40)
    
    test_cases = [
        ("Hello World", "Hello World", True),
        ("Hello World", "hello world", False),
        ("123", "123", True),
        ("123", " 123 ", False),
    ]
    
    for user_output, expected_output, should_pass in test_cases:
        result = check_output_flexible(user_output, expected_output, 'exact')
        status = "✅ PASS" if result == should_pass else "❌ FAIL"
        print(f"{status} | User: '{user_output}' | Expected: '{expected_output}' | Result: {result}")

def test_ignore_whitespace():
    """Test ignore whitespace checker"""
    print("\n🧪 Testing Ignore Whitespace Checker")
    print("-" * 40)
    
    test_cases = [
        ("1 2 3 4 5", "1 2 3 4 5", True),
        ("1  2  3  4  5", "1 2 3 4 5", True),
        ("1\n2\n3\n4\n5", "1 2 3 4 5", True),
        ("1,2,3,4,5", "1 2 3 4 5", True),
        ("1 2 3 4 5", "1 2 3 4 6", False),
    ]
    
    for user_output, expected_output, should_pass in test_cases:
        result = check_output_flexible(user_output, expected_output, 'ignore_whitespace')
        status = "✅ PASS" if result == should_pass else "❌ FAIL"
        print(f"{status} | User: '{user_output}' | Expected: '{expected_output}' | Result: {result}")

def test_multiple_outputs():
    """Test multiple outputs checker"""
    print("\n🧪 Testing Multiple Outputs Checker")
    print("-" * 40)
    
    test_cases = [
        ("1 2 3 4 5", "1 2 3 4 5|1,2,3,4,5|[1,2,3,4,5]", True),
        ("1,2,3,4,5", "1 2 3 4 5|1,2,3,4,5|[1,2,3,4,5]", True),
        ("[1,2,3,4,5]", "1 2 3 4 5|1,2,3,4,5|[1,2,3,4,5]", True),
        ("1;2;3;4;5", "1 2 3 4 5|1,2,3,4,5|[1,2,3,4,5]", False),
    ]
    
    for user_output, expected_output, should_pass in test_cases:
        result = check_output_flexible(user_output, expected_output, 'multiple_outputs')
        status = "✅ PASS" if result == should_pass else "❌ FAIL"
        print(f"{status} | User: '{user_output}' | Expected: '{expected_output}' | Result: {result}")

def test_custom_checker():
    """Test custom checker"""
    print("\n🧪 Testing Custom Checker")
    print("-" * 40)
    
    # Test case 1: Check if output is sorted
    custom_code_1 = """
# Check if output is sorted
try:
    numbers = [int(x.strip()) for x in user_output.split() if x.strip()]
    result = all(numbers[i] <= numbers[i+1] for i in range(len(numbers)-1))
except:
    result = False
"""
    
    test_cases_1 = [
        ("1 2 3 4 5", "sorted", True),
        ("5 4 3 2 1", "sorted", False),
        ("1 3 2 4 5", "sorted", False),
    ]
    
    for user_output, expected_output, should_pass in test_cases_1:
        result = check_output_flexible(user_output, expected_output, 'custom', custom_code_1)
        status = "✅ PASS" if result == should_pass else "❌ FAIL"
        print(f"{status} | User: '{user_output}' | Expected: 'sorted' | Result: {result}")
    
    # Test case 2: Case-insensitive palindrome check
    custom_code_2 = """
# Case-insensitive palindrome check
import re
user_clean = re.sub(r'[^a-zA-Z0-9]', '', user_output.lower())
result = user_clean == user_clean[::-1]
"""
    
    test_cases_2 = [
        ("A man a plan a canal Panama", "palindrome", True),
        ("race a car", "palindrome", False),
        ("Was it a car or a cat I saw?", "palindrome", True),
    ]
    
    for user_output, expected_output, should_pass in test_cases_2:
        result = check_output_flexible(user_output, expected_output, 'custom', custom_code_2)
        status = "✅ PASS" if result == should_pass else "❌ FAIL"
        print(f"{status} | User: '{user_output}' | Expected: 'palindrome' | Result: {result}")

def main():
    """Run all tests"""
    print("🚀 Testing Problem Checker Types")
    print("=" * 50)
    
    test_exact_match()
    test_ignore_whitespace()
    test_multiple_outputs()
    test_custom_checker()
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
    print("\n💡 Tips for using different checker types:")
    print("• Exact Match: Use for precise output matching")
    print("• Ignore Whitespace: Use when spacing/formatting may vary")
    print("• Multiple Outputs: Use when multiple valid formats exist")
    print("• Custom Checker: Use for complex validation logic")

if __name__ == "__main__":
    main() 