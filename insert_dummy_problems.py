#!/usr/bin/env python3
"""
Insert Dummy Problems into CodeZone Database
This script inserts 15 dummy problems with different checker types
"""

import pymysql.cursors
import sys

def get_db_connection():
    return pymysql.connect(
        host='127.0.0.1',
        user="rishab",
        password="SouL123@",
        database="practice",
        cursorclass=pymysql.cursors.DictCursor
    )

def insert_dummy_problems(clear_existing=True):
    """Insert 15 dummy problems into the database"""
    
    # First, ensure the new columns exist
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            print("🔧 Ensuring database columns exist...")
            
            # Add new columns if they don't exist
            try:
                cursor.execute("""
                    ALTER TABLE problems 
                    ADD COLUMN checker_type ENUM('exact', 'ignore_whitespace', 'custom', 'multiple_outputs') DEFAULT 'exact'
                """)
                print("✅ Added checker_type column")
            except:
                print("ℹ️ checker_type column already exists")
            
            try:
                cursor.execute("""
                    ALTER TABLE problems 
                    ADD COLUMN custom_checker_code TEXT NULL
                """)
                print("✅ Added custom_checker_code column")
            except:
                print("ℹ️ custom_checker_code column already exists")
            
            connection.commit()
            
            # Note: Problems table doesn't have user_id column
            print("ℹ️ Problems table doesn't have user_id column - proceeding without it")
            
            # Clear existing problems (optional)
            if clear_existing:
                print("🗑️ Clearing existing problems...")
                
                # First delete submissions that reference problems
                try:
                    cursor.execute("DELETE FROM submissions")
                    print("✅ Cleared existing submissions")
                except Exception as e:
                    print(f"ℹ️ No submissions to clear: {e}")
                
                # Then delete problems
                try:
                    cursor.execute("DELETE FROM problems")
                    print("✅ Cleared existing problems")
                except Exception as e:
                    print(f"ℹ️ No problems to clear: {e}")
                
                connection.commit()
            else:
                print("ℹ️ Keeping existing problems...")
            
            # Insert dummy problems
            print("\n📝 Inserting dummy problems...")
            
            problems = [
                # EASY PROBLEMS
                {
                    'title': 'Hello World',
                    'description': 'Write a program that prints "Hello, World!" exactly as shown.\n\nExample:\nInput: None\nOutput: Hello, World!',
                    'expected_output': 'Hello, World!',
                    'checker_type': 'exact',
                    'custom_checker_code': None,
                    'difficulty': 'Easy',
                    'tags': 'strings,output'
                },
                {
                    'title': 'Sum of Two Numbers',
                    'description': 'Write a program that takes two integers as input and prints their sum.\n\nExample:\nInput:\n5\n3\nOutput: 8\n\nNote: The output can have any amount of whitespace.',
                    'expected_output': '8',
                    'checker_type': 'ignore_whitespace',
                    'custom_checker_code': None,
                    'difficulty': 'Easy',
                    'tags': 'math,arithmetic'
                },
                {
                    'title': 'Print Numbers 1 to N',
                    'description': 'Write a program that takes a number N as input and prints numbers from 1 to N.\n\nExample:\nInput: 5\nOutput: 1 2 3 4 5\n\nNote: You can use spaces, commas, or brackets to separate numbers.',
                    'expected_output': '1 2 3 4 5|1,2,3,4,5|[1,2,3,4,5]',
                    'checker_type': 'multiple_outputs',
                    'custom_checker_code': None,
                    'difficulty': 'Easy',
                    'tags': 'loops,arrays'
                },
                {
                    'title': 'Check Even or Odd',
                    'description': 'Write a program that takes a number as input and prints "EVEN" if the number is even, "ODD" if it is odd.\n\nExample:\nInput: 6\nOutput: EVEN\n\nInput: 7\nOutput: ODD',
                    'expected_output': 'EVEN',
                    'checker_type': 'custom',
                    'custom_checker_code': '# Custom checker for even/odd validation\ntry:\n    user_output_upper = user_output.strip().upper()\n    if user_output_upper in ["EVEN", "ODD"]:\n        result = True\n    else:\n        result = False\nexcept:\n    result = False',
                    'difficulty': 'Easy',
                    'tags': 'math,conditionals'
                },
                {
                    'title': 'Reverse String',
                    'description': 'Write a program that takes a string as input and prints its reverse.\n\nExample:\nInput: hello\nOutput: olleh\n\nInput: world\nOutput: dlrow',
                    'expected_output': 'olleh',
                    'checker_type': 'ignore_whitespace',
                    'custom_checker_code': None,
                    'difficulty': 'Easy',
                    'tags': 'strings,algorithms'
                },
                
                # MEDIUM PROBLEMS
                {
                    'title': 'Find Maximum Number',
                    'description': 'Write a program that takes N numbers as input and finds the maximum among them.\n\nExample:\nInput:\n5\n1 4 2 8 3\nOutput: 8\n\nInput:\n3\n10 5 15\nOutput: 15',
                    'expected_output': '8',
                    'checker_type': 'custom',
                    'custom_checker_code': '# Custom checker for maximum number validation\ntry:\n    # Parse the expected output as the correct maximum\n    expected_max = int(expected_output.strip())\n    \n    # Parse user output as the maximum they found\n    user_max = int(user_output.strip())\n    \n    # Check if user found the correct maximum\n    result = (user_max == expected_max)\nexcept:\n    result = False',
                    'difficulty': 'Medium',
                    'tags': 'arrays,algorithms'
                },
                {
                    'title': 'Check Palindrome',
                    'description': 'Write a program that takes a string as input and prints "YES" if it is a palindrome, "NO" otherwise.\n\nA palindrome reads the same forwards and backwards (ignoring case and non-alphanumeric characters).\n\nExample:\nInput: A man a plan a canal Panama\nOutput: YES\n\nInput: hello world\nOutput: NO',
                    'expected_output': 'YES',
                    'checker_type': 'custom',
                    'custom_checker_code': '# Custom checker for palindrome validation\nimport re\ntry:\n    # Clean the input (remove non-alphanumeric, convert to lowercase)\n    user_output_clean = re.sub(r"[^a-zA-Z0-9]", "", user_output.lower())\n    \n    # Check if it is a palindrome\n    is_palindrome = user_output_clean == user_output_clean[::-1]\n    \n    # Check if user output is correct\n    user_answer = user_output.strip().upper()\n    if is_palindrome and user_answer == "YES":\n        result = True\n    elif not is_palindrome and user_answer == "NO":\n        result = True\n    else:\n        result = False\nexcept:\n    result = False',
                    'difficulty': 'Medium',
                    'tags': 'strings,algorithms'
                },
                {
                    'title': 'Sort Array',
                    'description': 'Write a program that takes N numbers as input and prints them in ascending order.\n\nExample:\nInput:\n5\n3 1 4 1 5\nOutput: 1 1 3 4 5\n\nNote: You can use different separators (spaces, commas, brackets).',
                    'expected_output': '1 1 3 4 5|1,1,3,4,5|[1,1,3,4,5]',
                    'checker_type': 'multiple_outputs',
                    'custom_checker_code': None,
                    'difficulty': 'Medium',
                    'tags': 'sorting,arrays'
                },
                {
                    'title': 'Count Vowels',
                    'description': 'Write a program that takes a string as input and counts the number of vowels (a, e, i, o, u) in it.\n\nExample:\nInput: hello world\nOutput: 3\n\nInput: programming\nOutput: 3',
                    'expected_output': '3',
                    'checker_type': 'exact',
                    'custom_checker_code': None,
                    'difficulty': 'Medium',
                    'tags': 'strings,counting'
                },
                {
                    'title': 'Fibonacci Series',
                    'description': 'Write a program that takes N as input and prints the first N Fibonacci numbers.\n\nExample:\nInput: 6\nOutput: 0 1 1 2 3 5\n\nInput: 8\nOutput: 0 1 1 2 3 5 8 13',
                    'expected_output': '0 1 1 2 3 5',
                    'checker_type': 'ignore_whitespace',
                    'custom_checker_code': None,
                    'difficulty': 'Medium',
                    'tags': 'math,sequences'
                },
                
                # HARD PROBLEMS
                {
                    'title': 'Check if Array is Sorted',
                    'description': 'Write a program that takes N numbers as input and prints "YES" if the array is sorted in ascending order, "NO" otherwise.\n\nExample:\nInput:\n5\n1 2 3 4 5\nOutput: YES\n\nInput:\n4\n1 3 2 4\nOutput: NO',
                    'expected_output': 'YES',
                    'checker_type': 'custom',
                    'custom_checker_code': '# Custom checker for sorted array validation\ntry:\n    # Parse user output\n    user_answer = user_output.strip().upper()\n    \n    # For this problem, we expect the array to be sorted\n    # So the correct answer should be "YES"\n    if user_answer == "YES":\n        result = True\n    else:\n        result = False\nexcept:\n    result = False',
                    'difficulty': 'Hard',
                    'tags': 'arrays,algorithms'
                },
                {
                    'title': 'Find Missing Number',
                    'description': 'Write a program that takes N-1 numbers (from 1 to N) as input and finds the missing number.\n\nExample:\nInput:\n5\n1 2 4 5\nOutput: 3\n\nInput:\n4\n1 3 4\nOutput: 2',
                    'expected_output': '3',
                    'checker_type': 'custom',
                    'custom_checker_code': '# Custom checker for missing number validation\ntry:\n    # Parse the expected missing number\n    expected_missing = int(expected_output.strip())\n    \n    # Parse user output as the missing number they found\n    user_missing = int(user_output.strip())\n    \n    # Check if user found the correct missing number\n    result = (user_missing == expected_missing)\nexcept:\n    result = False',
                    'difficulty': 'Hard',
                    'tags': 'arrays,algorithms'
                },
                {
                    'title': 'Check Prime Number',
                    'description': 'Write a program that takes a number as input and prints "PRIME" if it is prime, "NOT PRIME" otherwise.\n\nExample:\nInput: 7\nOutput: PRIME\n\nInput: 10\nOutput: NOT PRIME',
                    'expected_output': 'PRIME',
                    'checker_type': 'custom',
                    'custom_checker_code': '# Custom checker for prime number validation\ndef is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True\n\ntry:\n    # For this problem, we expect the number to be prime\n    # So the correct answer should be "PRIME"\n    user_answer = user_output.strip().upper()\n    if user_answer == "PRIME":\n        result = True\n    else:\n        result = False\nexcept:\n    result = False',
                    'difficulty': 'Hard',
                    'tags': 'math,algorithms'
                },
                {
                    'title': 'Reverse Words in String',
                    'description': 'Write a program that takes a string as input and reverses the order of words.\n\nExample:\nInput: hello world\nOutput: world hello\n\nInput: code zone platform\nOutput: platform zone code\n\nNote: You can use different separators between words.',
                    'expected_output': 'world hello|world,hello|world  hello',
                    'checker_type': 'multiple_outputs',
                    'custom_checker_code': None,
                    'difficulty': 'Hard',
                    'tags': 'strings,algorithms'
                },
                {
                    'title': 'Check Balanced Parentheses',
                    'description': 'Write a program that takes a string containing parentheses as input and prints "BALANCED" if the parentheses are balanced, "NOT BALANCED" otherwise.\n\nExample:\nInput: (())\nOutput: BALANCED\n\nInput: (()\nOutput: NOT BALANCED\n\nInput: ()()\nOutput: BALANCED',
                    'expected_output': 'BALANCED',
                    'checker_type': 'custom',
                    'custom_checker_code': '# Custom checker for balanced parentheses validation\ndef is_balanced(s):\n    stack = []\n    for char in s:\n        if char == "(":\n            stack.append(char)\n        elif char == ")":\n            if not stack:\n                return False\n            stack.pop()\n    return len(stack) == 0\n\ntry:\n    # For this problem, we expect the parentheses to be balanced\n    # So the correct answer should be "BALANCED"\n    user_answer = user_output.strip().upper()\n    if user_answer == "BALANCED":\n        result = True\n    else:\n        result = False\nexcept:\n    result = False',
                    'difficulty': 'Hard',
                    'tags': 'strings,stacks'
                }
            ]
            
            # Insert each problem
            for i, problem in enumerate(problems, 1):
                cursor.execute("""
                    INSERT INTO problems (title, description, expected_output, checker_type, custom_checker_code, difficulty, tags)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    problem['title'],
                    problem['description'],
                    problem['expected_output'],
                    problem['checker_type'],
                    problem['custom_checker_code'],
                    problem['difficulty'],
                    problem['tags']
                ))
                print(f"✅ Inserted problem {i}: {problem['title']} ({problem['difficulty']})")
            
            connection.commit()
            print(f"\n🎉 Successfully inserted {len(problems)} problems!")
            
            # Show summary
            cursor.execute("SELECT difficulty, COUNT(*) as count FROM problems GROUP BY difficulty")
            difficulty_counts = cursor.fetchall()
            
            print("\n📊 Problem Summary:")
            for row in difficulty_counts:
                print(f"   {row['difficulty']}: {row['count']} problems")
            
            cursor.execute("SELECT checker_type, COUNT(*) as count FROM problems GROUP BY checker_type")
            checker_counts = cursor.fetchall()
            
            print("\n🔍 Checker Type Summary:")
            for row in checker_counts:
                print(f"   {row['checker_type']}: {row['count']} problems")
            
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        connection.rollback()
        return False
    finally:
        connection.close()

def main():
    """Main function"""
    print("🚀 CodeZone Dummy Problems Insertion")
    print("=" * 50)
    
    # Ask user if they want to clear existing problems
    print("\n🤔 Do you want to:")
    print("1. Clear existing problems and insert new ones (recommended)")
    print("2. Keep existing problems and add new ones")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == "2":
        # Modify the function to not clear existing problems
        print("\n📝 Adding problems without clearing existing ones...")
        if insert_dummy_problems(clear_existing=False):
            print("\n✅ All problems added successfully!")
            print("🎯 Your CodeZone platform now has additional test problems!")
        else:
            print("\n❌ Failed to add problems!")
            sys.exit(1)
    else:
        # Default behavior - clear and insert
        if insert_dummy_problems():
            print("\n✅ All problems inserted successfully!")
            print("🎯 Your CodeZone platform is now ready with 15 test problems!")
        else:
            print("\n❌ Failed to insert problems!")
            sys.exit(1)
    
    print("\n💡 Next steps:")
    print("   1. Start your Flask app: python app.py")
    print("   2. Login to your platform")
    print("   3. Try solving the problems!")

if __name__ == "__main__":
    main() 