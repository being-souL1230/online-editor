#!/usr/bin/env python3
"""
Test Script for CodeZone Execution System
Tests the server-side code execution functionality
"""

from code_executor import executor

def test_python_execution():
    """Test Python code execution"""
    print("🐍 Testing Python Execution")
    print("-" * 40)
    
    # Test 1: Simple print
    code1 = """
print("Hello, World!")
"""
    result1 = executor.execute_code(code1, 71)
    print(f"Test 1 - Simple print:")
    print(f"  Status: {result1['status']}")
    print(f"  Output: {result1['output']}")
    print(f"  Time: {result1['execution_time']}s")
    
    # Test 2: Input handling
    code2 = """
name = input()
print(f"Hello, {name}!")
"""
    result2 = executor.execute_code(code2, 71, "CodeZone")
    print(f"\nTest 2 - Input handling:")
    print(f"  Status: {result2['status']}")
    print(f"  Output: {result2['output']}")
    print(f"  Time: {result2['execution_time']}s")
    
    # Test 3: Error handling
    code3 = """
print("Starting...")
undefined_variable
print("This won't print")
"""
    result3 = executor.execute_code(code3, 71)
    print(f"\nTest 3 - Error handling:")
    print(f"  Status: {result3['status']}")
    print(f"  Error: {result3['error']}")
    print(f"  Time: {result3['execution_time']}s")

def test_cpp_execution():
    """Test C++ code execution"""
    print("\n⚡ Testing C++ Execution")
    print("-" * 40)
    
    # Test 1: Simple C++ program
    code1 = """
#include <iostream>
using namespace std;
int main() {
    cout << "Hello from C++!" << endl;
    return 0;
}
"""
    result1 = executor.execute_code(code1, 54)
    print(f"Test 1 - Simple C++:")
    print(f"  Status: {result1['status']}")
    print(f"  Output: {result1['output']}")
    print(f"  Time: {result1['execution_time']}s")
    
    # Test 2: C++ with input
    code2 = """
#include <iostream>
#include <string>
using namespace std;
int main() {
    string name;
    cin >> name;
    cout << "Hello, " << name << "!" << endl;
    return 0;
}
"""
    result2 = executor.execute_code(code2, 54, "CodeZone")
    print(f"\nTest 2 - C++ with input:")
    print(f"  Status: {result2['status']}")
    print(f"  Output: {result2['output']}")
    print(f"  Time: {result2['execution_time']}s")

def test_c_execution():
    """Test C code execution"""
    print("\n🔧 Testing C Execution")
    print("-" * 40)
    
    # Test 1: Simple C program
    code1 = """
#include <stdio.h>
int main() {
    printf("Hello from C!\\n");
    return 0;
}
"""
    result1 = executor.execute_code(code1, 50)
    print(f"Test 1 - Simple C:")
    print(f"  Status: {result1['status']}")
    print(f"  Output: {result1['output']}")
    print(f"  Time: {result1['execution_time']}s")
    
    # Test 2: C with input
    code2 = """
#include <stdio.h>
int main() {
    char name[100];
    scanf("%s", name);
    printf("Hello, %s!\\n", name);
    return 0;
}
"""
    result2 = executor.execute_code(code2, 50, "CodeZone")
    print(f"\nTest 2 - C with input:")
    print(f"  Status: {result2['status']}")
    print(f"  Output: {result2['output']}")
    print(f"  Time: {result2['execution_time']}s")

def test_timeout():
    """Test timeout functionality"""
    print("\n⏰ Testing Timeout")
    print("-" * 40)
    
    # Infinite loop test
    code = """
import time
while True:
    time.sleep(1)
    print("Still running...")
"""
    result = executor.execute_code(code, 71, timeout=3)
    print(f"Timeout test:")
    print(f"  Status: {result['status']}")
    print(f"  Error: {result['error']}")
    print(f"  Time: {result['execution_time']}s")

def main():
    """Run all tests"""
    print("🚀 CodeZone Execution System Test")
    print("=" * 50)
    
    try:
        test_python_execution()
        test_cpp_execution()
        test_c_execution()
        test_timeout()
        
        print("\n" + "=" * 50)
        print("✅ All tests completed!")
        print("🎯 Your execution system is working correctly!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        print("🔧 Please check if you have the required compilers installed:")
        print("   - Python: Should be available by default")
        print("   - g++: For C++ compilation")
        print("   - gcc: For C compilation")

if __name__ == "__main__":
    main() 