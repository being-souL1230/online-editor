#!/usr/bin/env python3
"""
Debug Script for Language IDs
Check what language IDs are being sent from frontend
"""

def test_language_ids():
    """Test different language ID formats"""
    print("🔍 Debugging Language IDs")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        ("54", "C++"),
        ("71", "Python"), 
        ("50", "C"),
        (54, "C++ (int)"),
        (71, "Python (int)"),
        (50, "C (int)")
    ]
    
    for lang_id, description in test_cases:
        print(f"\nTesting: {description}")
        print(f"  Type: {type(lang_id)}")
        print(f"  Value: {lang_id}")
        
        # Simulate the conversion logic
        if isinstance(lang_id, str):
            try:
                converted_id = int(lang_id)
                print(f"  Converted to int: {converted_id}")
                print(f"  Supported: {converted_id in [50, 54, 71]}")
            except ValueError:
                print(f"  ❌ Cannot convert to int")
        else:
            print(f"  Already int: {lang_id}")
            print(f"  Supported: {lang_id in [50, 54, 71]}")

def test_executor_with_different_formats():
    """Test executor with different language ID formats"""
    print("\n🧪 Testing Executor with Different Formats")
    print("=" * 50)
    
    from code_executor import executor
    
    python_code = 'print("Hello from Python!")'
    
    # Test with string
    print("\nTesting with string '71':")
    try:
        result = executor.execute_code(python_code, int("71"))
        print(f"  Status: {result['status']}")
        print(f"  Output: {result['output']}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Test with int
    print("\nTesting with int 71:")
    try:
        result = executor.execute_code(python_code, 71)
        print(f"  Status: {result['status']}")
        print(f"  Output: {result['output']}")
    except Exception as e:
        print(f"  Error: {e}")

if __name__ == "__main__":
    test_language_ids()
    test_executor_with_different_formats() 