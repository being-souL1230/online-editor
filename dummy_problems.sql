-- CodeZone Dummy Problems
-- 15 problems with different checker types and difficulty levels

-- First, make sure we have the new columns
ALTER TABLE problems 
ADD COLUMN IF NOT EXISTS checker_type ENUM('exact', 'ignore_whitespace', 'custom', 'multiple_outputs') DEFAULT 'exact',
ADD COLUMN IF NOT EXISTS custom_checker_code TEXT NULL;

-- Clear existing problems (optional - comment out if you want to keep existing)
-- DELETE FROM problems;

-- ========================================
-- EASY PROBLEMS (5 problems)
-- ========================================

-- 1. Hello World (Exact Match)
INSERT INTO problems (user_id, title, description, expected_output, checker_type, difficulty, tags) 
VALUES (1, 'Hello World', 
'Write a program that prints "Hello, World!" exactly as shown.

Example:
Input: None
Output: Hello, World!', 
'Hello, World!', 'exact', 'Easy', 'strings,output');

-- 2. Sum of Two Numbers (Ignore Whitespace)
INSERT INTO problems (user_id, title, description, expected_output, checker_type, difficulty, tags) 
VALUES (1, 'Sum of Two Numbers', 
'Write a program that takes two integers as input and prints their sum.

Example:
Input: 
5
3
Output: 8

Note: The output can have any amount of whitespace.', 
'8', 'ignore_whitespace', 'Easy', 'math,arithmetic');

-- 3. Print Numbers 1 to N (Multiple Outputs)
INSERT INTO problems (user_id, title, description, expected_output, checker_type, difficulty, tags) 
VALUES (1, 'Print Numbers 1 to N', 
'Write a program that takes a number N as input and prints numbers from 1 to N.

Example:
Input: 5
Output: 1 2 3 4 5

Note: You can use spaces, commas, or brackets to separate numbers.', 
'1 2 3 4 5|1,2,3,4,5|[1,2,3,4,5]', 'multiple_outputs', 'Easy', 'loops,arrays');

-- 4. Check Even or Odd (Custom Checker)
INSERT INTO problems (user_id, title, description, expected_output, checker_type, custom_checker_code, difficulty, tags) 
VALUES (1, 'Check Even or Odd', 
'Write a program that takes a number as input and prints "EVEN" if the number is even, "ODD" if it is odd.

Example:
Input: 6
Output: EVEN

Input: 7
Output: ODD', 
'EVEN', 'custom', 
'# Custom checker for even/odd validation
try:
    user_output_upper = user_output.strip().upper()
    if user_output_upper in ["EVEN", "ODD"]:
        result = True
    else:
        result = False
except:
    result = False', 'Easy', 'math,conditionals');

-- 5. Reverse String (Ignore Whitespace)
INSERT INTO problems (user_id, title, description, expected_output, checker_type, difficulty, tags) 
VALUES (1, 'Reverse String', 
'Write a program that takes a string as input and prints its reverse.

Example:
Input: hello
Output: olleh

Input: world
Output: dlrow', 
'olleh', 'ignore_whitespace', 'Easy', 'strings,algorithms');

-- ========================================
-- MEDIUM PROBLEMS (5 problems)
-- ========================================

-- 6. Find Maximum Number (Custom Checker)
INSERT INTO problems (user_id, title, description, expected_output, checker_type, custom_checker_code, difficulty, tags) 
VALUES (1, 'Find Maximum Number', 
'Write a program that takes N numbers as input and finds the maximum among them.

Example:
Input:
5
1 4 2 8 3
Output: 8

Input:
3
10 5 15
Output: 15', 
'8', 'custom', 
'# Custom checker for maximum number validation
try:
    # Parse the expected output as the correct maximum
    expected_max = int(expected_output.strip())
    
    # Parse user output as the maximum they found
    user_max = int(user_output.strip())
    
    # Check if user found the correct maximum
    result = (user_max == expected_max)
except:
    result = False', 'Medium', 'arrays,algorithms');

-- 7. Check Palindrome (Custom Checker)
INSERT INTO problems (user_id, title, description, expected_output, checker_type, custom_checker_code, difficulty, tags) 
VALUES (1, 'Check Palindrome', 
'Write a program that takes a string as input and prints "YES" if it is a palindrome, "NO" otherwise.

A palindrome reads the same forwards and backwards (ignoring case and non-alphanumeric characters).

Example:
Input: A man a plan a canal Panama
Output: YES

Input: hello world
Output: NO', 
'YES', 'custom', 
'# Custom checker for palindrome validation
import re
try:
    # Clean the input (remove non-alphanumeric, convert to lowercase)
    user_output_clean = re.sub(r"[^a-zA-Z0-9]", "", user_output.lower())
    
    # Check if it is a palindrome
    is_palindrome = user_output_clean == user_output_clean[::-1]
    
    # Check if user output is correct
    user_answer = user_output.strip().upper()
    if is_palindrome and user_answer == "YES":
        result = True
    elif not is_palindrome and user_answer == "NO":
        result = True
    else:
        result = False
except:
    result = False', 'Medium', 'strings,algorithms');

-- 8. Sort Array (Multiple Outputs)
INSERT INTO problems (user_id, title, description, expected_output, checker_type, difficulty, tags) 
VALUES (1, 'Sort Array', 
'Write a program that takes N numbers as input and prints them in ascending order.

Example:
Input:
5
3 1 4 1 5
Output: 1 1 3 4 5

Note: You can use different separators (spaces, commas, brackets).', 
'1 1 3 4 5|1,1,3,4,5|[1,1,3,4,5]', 'multiple_outputs', 'Medium', 'sorting,arrays');

-- 9. Count Vowels (Exact Match)
INSERT INTO problems (user_id, title, description, expected_output, checker_type, difficulty, tags) 
VALUES (1, 'Count Vowels', 
'Write a program that takes a string as input and counts the number of vowels (a, e, i, o, u) in it.

Example:
Input: hello world
Output: 3

Input: programming
Output: 3', 
'3', 'exact', 'Medium', 'strings,counting');

-- 10. Fibonacci Series (Ignore Whitespace)
INSERT INTO problems (user_id, title, description, expected_output, checker_type, difficulty, tags) 
VALUES (1, 'Fibonacci Series', 
'Write a program that takes N as input and prints the first N Fibonacci numbers.

Example:
Input: 6
Output: 0 1 1 2 3 5

Input: 8
Output: 0 1 1 2 3 5 8 13', 
'0 1 1 2 3 5', 'ignore_whitespace', 'Medium', 'math,sequences');

-- ========================================
-- HARD PROBLEMS (5 problems)
-- ========================================

-- 11. Check if Array is Sorted (Custom Checker)
INSERT INTO problems (user_id, title, description, expected_output, checker_type, custom_checker_code, difficulty, tags) 
VALUES (1, 'Check if Array is Sorted', 
'Write a program that takes N numbers as input and prints "YES" if the array is sorted in ascending order, "NO" otherwise.

Example:
Input:
5
1 2 3 4 5
Output: YES

Input:
4
1 3 2 4
Output: NO', 
'YES', 'custom', 
'# Custom checker for sorted array validation
try:
    # Parse user output
    user_answer = user_output.strip().upper()
    
    # For this problem, we expect the array to be sorted
    # So the correct answer should be "YES"
    if user_answer == "YES":
        result = True
    else:
        result = False
except:
    result = False', 'Hard', 'arrays,algorithms');

-- 12. Find Missing Number (Custom Checker)
INSERT INTO problems (user_id, title, description, expected_output, checker_type, custom_checker_code, difficulty, tags) 
VALUES (1, 'Find Missing Number', 
'Write a program that takes N-1 numbers (from 1 to N) as input and finds the missing number.

Example:
Input:
5
1 2 4 5
Output: 3

Input:
4
1 3 4
Output: 2', 
'3', 'custom', 
'# Custom checker for missing number validation
try:
    # Parse the expected missing number
    expected_missing = int(expected_output.strip())
    
    # Parse user output as the missing number they found
    user_missing = int(user_output.strip())
    
    # Check if user found the correct missing number
    result = (user_missing == expected_missing)
except:
    result = False', 'Hard', 'arrays,algorithms');

-- 13. Check Prime Number (Custom Checker)
INSERT INTO problems (user_id, title, description, expected_output, checker_type, custom_checker_code, difficulty, tags) 
VALUES (1, 'Check Prime Number', 
'Write a program that takes a number as input and prints "PRIME" if it is prime, "NOT PRIME" otherwise.

Example:
Input: 7
Output: PRIME

Input: 10
Output: NOT PRIME', 
'PRIME', 'custom', 
'# Custom checker for prime number validation
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

try:
    # For this problem, we expect the number to be prime
    # So the correct answer should be "PRIME"
    user_answer = user_output.strip().upper()
    if user_answer == "PRIME":
        result = True
    else:
        result = False
except:
    result = False', 'Hard', 'math,algorithms');

-- 14. Reverse Words in String (Multiple Outputs)
INSERT INTO problems (user_id, title, description, expected_output, checker_type, difficulty, tags) 
VALUES (1, 'Reverse Words in String', 
'Write a program that takes a string as input and reverses the order of words.

Example:
Input: hello world
Output: world hello

Input: code zone platform
Output: platform zone code

Note: You can use different separators between words.', 
'world hello|world,hello|world  hello', 'multiple_outputs', 'Hard', 'strings,algorithms');

-- 15. Check Balanced Parentheses (Custom Checker)
INSERT INTO problems (user_id, title, description, expected_output, checker_type, custom_checker_code, difficulty, tags) 
VALUES (1, 'Check Balanced Parentheses', 
'Write a program that takes a string containing parentheses as input and prints "BALANCED" if the parentheses are balanced, "NOT BALANCED" otherwise.

Example:
Input: (())
Output: BALANCED

Input: (()
Output: NOT BALANCED

Input: ()()
Output: BALANCED', 
'BALANCED', 'custom', 
'# Custom checker for balanced parentheses validation
def is_balanced(s):
    stack = []
    for char in s:
        if char == "(":
            stack.append(char)
        elif char == ")":
            if not stack:
                return False
            stack.pop()
    return len(stack) == 0

try:
    # For this problem, we expect the parentheses to be balanced
    # So the correct answer should be "BALANCED"
    user_answer = user_output.strip().upper()
    if user_answer == "BALANCED":
        result = True
    else:
        result = False
except:
    result = False', 'Hard', 'strings,stacks');

-- ========================================
-- SUMMARY
-- ========================================
-- Total: 15 problems
-- Easy: 5 problems
-- Medium: 5 problems  
-- Hard: 5 problems
-- 
-- Checker Types:
-- - Exact Match: 2 problems
-- - Ignore Whitespace: 3 problems
-- - Multiple Outputs: 3 problems
-- - Custom Checker: 7 problems 