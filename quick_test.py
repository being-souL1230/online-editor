#!/usr/bin/env python3
"""
Quick Test for CodeZone Execution System
Tests the fixed language ID handling
"""

from code_executor import executor

def quick_test():
    """Quick test of all supported languages"""
    print("🚀 Quick Test - CodeZone Execution System")
    print("=" * 50)
    
    # Test Python (ID: 71)
    print("\n🐍 Testing Python (ID: 71):")
    python_code = 'print("Hello from Python!")'
    result = executor.execute_code(python_code, 71)
    print(f"  Status: {result['status']}")
    print(f"  Output: {result['output']}")
    
    # Test Python with string ID
    print("\n🐍 Testing Python (ID: '71'):")
    result = executor.execute_code(python_code, "71")
    print(f"  Status: {result['status']}")
    print(f"  Output: {result['output']}")
    
    # Test C++ (ID: 54)
    print("\n⚡ Testing C++ (ID: 54):")
    cpp_code = """
#include <iostream>
using namespace std;
int main() {
    cout << "Hello from C++!" << endl;
    return 0;
}
"""
    result = executor.execute_code(cpp_code, 54)
    print(f"  Status: {result['status']}")
    print(f"  Output: {result['output']}")
    if result['error']:
        print(f"  Error: {result['error']}")
    
    # Test C (ID: 50)
    print("\n🔧 Testing C (ID: 50):")
    c_code = """
#include <stdio.h>
int main() {
    printf("Hello from C!\\n");
    return 0;
}
"""
    result = executor.execute_code(c_code, 50)
    print(f"  Status: {result['status']}")
    print(f"  Output: {result['output']}")
    if result['error']:
        print(f"  Error: {result['error']}")
    
    # Test invalid language ID
    print("\n❌ Testing Invalid Language ID:")
    result = executor.execute_code("print('test')", 999)
    print(f"  Status: {result['status']}")
    print(f"  Output: {result['output']}")
    
    print("\n" + "=" * 50)
    print("✅ Quick test completed!")

if __name__ == "__main__":
    quick_test() 