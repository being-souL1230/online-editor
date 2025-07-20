# 🎯 CodeZone Dummy Problems Guide

## 📋 Overview
Ye 15 dummy problems aapke CodeZone platform ko test karne ke liye banaye gaye hain. Har problem different checker type use karta hai aur different difficulty level ka hai.

## 🚀 Quick Start

### 1. Database mein problems insert karo:
```bash
python insert_dummy_problems.py
```

### 2. Flask app start karo:
```bash
python app.py
```

### 3. Browser mein test karo:
- Login karo
- Dashboard pe jao
- Problems solve karo!

## 📊 Problems Summary

### 🟢 EASY PROBLEMS (5)

| # | Title | Checker Type | Tags |
|---|-------|--------------|------|
| 1 | Hello World | Exact Match | strings, output |
| 2 | Sum of Two Numbers | Ignore Whitespace | math, arithmetic |
| 3 | Print Numbers 1 to N | Multiple Outputs | loops, arrays |
| 4 | Check Even or Odd | Custom Checker | math, conditionals |
| 5 | Reverse String | Ignore Whitespace | strings, algorithms |

### 🟡 MEDIUM PROBLEMS (5)

| # | Title | Checker Type | Tags |
|---|-------|--------------|------|
| 6 | Find Maximum Number | Custom Checker | arrays, algorithms |
| 7 | Check Palindrome | Custom Checker | strings, algorithms |
| 8 | Sort Array | Multiple Outputs | sorting, arrays |
| 9 | Count Vowels | Exact Match | strings, counting |
| 10 | Fibonacci Series | Ignore Whitespace | math, sequences |

### 🔴 HARD PROBLEMS (5)

| # | Title | Checker Type | Tags |
|---|-------|--------------|------|
| 11 | Check if Array is Sorted | Custom Checker | arrays, algorithms |
| 12 | Find Missing Number | Custom Checker | arrays, algorithms |
| 13 | Check Prime Number | Custom Checker | math, algorithms |
| 14 | Reverse Words in String | Multiple Outputs | strings, algorithms |
| 15 | Check Balanced Parentheses | Custom Checker | strings, stacks |

## 🔍 Checker Types Explained

### 1. **Exact Match** (2 problems)
- User ka output exactly expected output ke equal hona chahiye
- Example: `"Hello, World!"` exactly same hona chahiye

### 2. **Ignore Whitespace** (3 problems)
- User ka output whitespace ignore karke check hota hai
- Example: `"8"`, `" 8 "`, `"8\n"` sab valid hain

### 3. **Multiple Outputs** (3 problems)
- Multiple valid outputs accept karta hai
- Example: `"1 2 3"`, `"1,2,3"`, `"[1,2,3]"` sab valid hain

### 4. **Custom Checker** (7 problems)
- Custom Python code se output validate hota hai
- Complex logic handle kar sakta hai
- Example: Even/Odd, Palindrome, Prime number checking

## 🧪 Testing Different Scenarios

### Easy Problems Testing:
```python
# Problem 1: Hello World (Exact Match)
print("Hello, World!")  # ✅ Correct
print("hello world")    # ❌ Wrong (case sensitive)

# Problem 2: Sum of Two Numbers (Ignore Whitespace)
print(5 + 3)  # ✅ Correct (output: 8)
print("  8  ")  # ✅ Correct (whitespace ignored)

# Problem 3: Print Numbers 1 to N (Multiple Outputs)
print("1 2 3 4 5")  # ✅ Correct
print("1,2,3,4,5")  # ✅ Correct
print("[1,2,3,4,5]")  # ✅ Correct
```

### Medium Problems Testing:
```python
# Problem 6: Find Maximum Number (Custom Checker)
numbers = [1, 4, 2, 8, 3]
print(max(numbers))  # ✅ Correct (output: 8)

# Problem 7: Check Palindrome (Custom Checker)
text = "A man a plan a canal Panama"
# Clean and check if palindrome
print("YES")  # ✅ Correct if it's a palindrome
```

### Hard Problems Testing:
```python
# Problem 13: Check Prime Number (Custom Checker)
def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

n = 7
if is_prime(n):
    print("PRIME")  # ✅ Correct
else:
    print("NOT PRIME")
```

## 🎯 Problem Examples

### Example 1: Hello World (Easy - Exact Match)
**Problem:** Write a program that prints "Hello, World!" exactly as shown.

**Valid Solutions:**
```python
print("Hello, World!")
```

**Invalid Solutions:**
```python
print("hello world")  # Wrong case
print("Hello World")  # Missing comma
```

### Example 2: Sum of Two Numbers (Easy - Ignore Whitespace)
**Problem:** Write a program that takes two integers as input and prints their sum.

**Valid Solutions:**
```python
a = int(input())
b = int(input())
print(a + b)
# Output: 8 (any whitespace allowed)
```

### Example 3: Check Even or Odd (Easy - Custom Checker)
**Problem:** Write a program that takes a number as input and prints "EVEN" if the number is even, "ODD" if it is odd.

**Valid Solutions:**
```python
n = int(input())
if n % 2 == 0:
    print("EVEN")
else:
    print("ODD")
```

## 🔧 Custom Checker Code Examples

### Even/Odd Checker:
```python
try:
    user_output_upper = user_output.strip().upper()
    if user_output_upper in ["EVEN", "ODD"]:
        result = True
    else:
        result = False
except:
    result = False
```

### Palindrome Checker:
```python
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
    result = False
```

## 🚀 Next Steps

1. **Test all problems** - Har problem ko solve karo different languages mein
2. **Test different outputs** - Same problem ke liye different valid outputs try karo
3. **Test edge cases** - Invalid inputs, empty outputs, etc.
4. **Test performance** - Large inputs ke saath test karo
5. **Add more problems** - Apne custom problems add karo

## 💡 Tips for Testing

1. **Start with Easy problems** - Basic functionality test karo
2. **Test all checker types** - Har checker type ko verify karo
3. **Test multiple languages** - Python, C++, C sab mein test karo
4. **Test error handling** - Wrong code, infinite loops, etc.
5. **Test UI/UX** - Frontend functionality bhi test karo

## 🎉 Success Criteria

✅ **All problems insert successfully**  
✅ **All checker types work correctly**  
✅ **Code execution works for all languages**  
✅ **Frontend displays problems correctly**  
✅ **Submission and scoring work properly**  
✅ **Leaderboard updates correctly**  

**Ab aapka CodeZone platform fully functional hai!** 🚀 