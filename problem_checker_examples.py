"""
Problem Checker Examples for LeetCode-like Platform

This file contains examples of how to use different checker types
when creating problems in your database.
"""

# Example 1: Exact Match (Default)
# Use when you want exact output matching
exact_example = {
    "title": "Print Hello World",
    "description": "Print 'Hello World' exactly",
    "expected_output": "Hello World",
    "checker_type": "exact"
}

# Example 2: Ignore Whitespace
# Use when output format might vary in spacing
whitespace_example = {
    "title": "Print Numbers",
    "description": "Print numbers 1 to 5",
    "expected_output": "1 2 3 4 5",
    "checker_type": "ignore_whitespace"
    # This will accept: "1 2 3 4 5", "1  2  3  4  5", "1\n2\n3\n4\n5", etc.
}

# Example 3: Multiple Valid Outputs
# Use when there are multiple correct ways to format output
multiple_outputs_example = {
    "title": "Sort Array",
    "description": "Sort the array in ascending order",
    "expected_output": "1 2 3 4 5|1,2,3,4,5|[1,2,3,4,5]",
    "checker_type": "multiple_outputs"
    # This will accept any of the three formats
}

# Example 4: Custom Checker
# Use for complex validation logic
custom_checker_example = {
    "title": "Check if Array is Sorted",
    "description": "Output 'YES' if array is sorted, 'NO' otherwise",
    "expected_output": "YES",
    "checker_type": "custom",
    "custom_checker_code": """
# Custom checker for sorting validation
try:
    # Parse user output as list of integers
    user_numbers = [int(x.strip()) for x in user_output.split() if x.strip()]
    expected_numbers = [int(x.strip()) for x in expected_output.split() if x.strip()]
    
    # Check if user output is sorted
    is_sorted = all(user_numbers[i] <= user_numbers[i+1] for i in range(len(user_numbers)-1))
    
    # Check if it contains the same elements as expected
    same_elements = sorted(user_numbers) == sorted(expected_numbers)
    
    result = is_sorted and same_elements
except:
    result = False
"""
}

# Example 5: Custom Checker for Case-Insensitive String Matching
case_insensitive_example = {
    "title": "Palindrome Check",
    "description": "Check if the string is a palindrome",
    "expected_output": "YES",
    "checker_type": "custom",
    "custom_checker_code": """
# Case-insensitive palindrome check
user_output_clean = user_output.strip().lower()
expected_output_clean = expected_output.strip().lower()

# Remove non-alphanumeric characters
import re
user_output_clean = re.sub(r'[^a-zA-Z0-9]', '', user_output_clean)
expected_output_clean = re.sub(r'[^a-zA-Z0-9]', '', expected_output_clean)

result = user_output_clean == expected_output_clean
"""
}

# SQL to insert these examples into your database
sql_examples = """
-- Example 1: Exact Match
INSERT INTO problems (user_id, title, description, expected_output, checker_type, difficulty, tags) 
VALUES (1, 'Print Hello World', 'Print Hello World exactly', 'Hello World', 'exact', 'Easy', 'strings,output');

-- Example 2: Ignore Whitespace
INSERT INTO problems (user_id, title, description, expected_output, checker_type, difficulty, tags) 
VALUES (1, 'Print Numbers', 'Print numbers 1 to 5', '1 2 3 4 5', 'ignore_whitespace', 'Easy', 'loops,output');

-- Example 3: Multiple Outputs
INSERT INTO problems (user_id, title, description, expected_output, checker_type, difficulty, tags) 
VALUES (1, 'Sort Array', 'Sort the array in ascending order', '1 2 3 4 5|1,2,3,4,5|[1,2,3,4,5]', 'multiple_outputs', 'Medium', 'sorting,arrays');

-- Example 4: Custom Checker
INSERT INTO problems (user_id, title, description, expected_output, checker_type, custom_checker_code, difficulty, tags) 
VALUES (1, 'Check if Array is Sorted', 'Output YES if array is sorted, NO otherwise', 'YES', 'custom', 
'# Custom checker for sorting validation
try:
    user_numbers = [int(x.strip()) for x in user_output.split() if x.strip()]
    expected_numbers = [int(x.strip()) for x in expected_output.split() if x.strip()]
    is_sorted = all(user_numbers[i] <= user_numbers[i+1] for i in range(len(user_numbers)-1))
    same_elements = sorted(user_numbers) == sorted(expected_numbers)
    result = is_sorted and same_elements
except:
    result = False', 'Medium', 'sorting,validation');
"""

if __name__ == "__main__":
    print("Problem Checker Examples")
    print("=" * 50)
    print("\n1. Exact Match (Default):")
    print(f"   {exact_example}")
    
    print("\n2. Ignore Whitespace:")
    print(f"   {whitespace_example}")
    
    print("\n3. Multiple Valid Outputs:")
    print(f"   {multiple_outputs_example}")
    
    print("\n4. Custom Checker:")
    print(f"   {custom_checker_example}")
    
    print("\n5. Case-Insensitive Example:")
    print(f"   {case_insensitive_example}")
    
    print("\n" + "=" * 50)
    print("SQL Examples:")
    print(sql_examples) 