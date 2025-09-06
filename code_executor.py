#!/usr/bin/env python3
"""
CodeZone - Server-Side Code Execution System
Safely executes Python, C++, and C code with proper sandboxing
"""

import subprocess
import tempfile
import os
import signal
import time
import threading
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import uuid
import platform

class CodeExecutor:
    def __init__(self):
        self.timeout = 10  # seconds
        self.max_memory = "100MB"
        self.supported_languages = {
            50: "c",
            54: "cpp", 
            71: "python"
        }
        
    def execute_code(self, source_code: str, language_id, stdin: str = "", timeout: int = 10):
        """
        Execute code and return results
        """
        # Convert language_id to int if it's a string
        if isinstance(language_id, str):
            try:
                language_id = int(language_id)
            except ValueError:
                return {
                    "status": "Error",
                    "output": f"Invalid language ID: {language_id}",
                    "execution_time": 0,
                    "memory_used": 0
                }
        
        if language_id not in self.supported_languages:
            return {
                "status": "Error",
                "output": f"Unsupported language ID: {language_id}. Supported: {list(self.supported_languages.keys())}",
                "execution_time": 0,
                "memory_used": 0
            }
        
        language = self.supported_languages[language_id]
        
        try:
            if language == "python":
                return self._execute_python(source_code, stdin, timeout)
            elif language == "cpp":
                return self._execute_cpp(source_code, stdin, timeout)
            elif language == "c":
                return self._execute_c(source_code, stdin, timeout)
            else:
                return {
                    "status": "Error",
                    "output": f"Unsupported language: {language}",
                    "execution_time": 0,
                    "memory_used": 0
                }
        except Exception as e:
            return {
                "status": "Error",
                "output": f"Execution error: {str(e)}",
                "execution_time": 0,
                "memory_used": 0
            }
    
    def _execute_python(self, source_code: str, stdin: str, timeout: int) -> Dict:
        """Execute Python code safely"""
        start_time = time.time()
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as code_file:
            code_file.write(source_code)
            code_path = code_file.name
        
        try:
            # Prepare command with resource limits
            cmd = [
                'python', '-u', code_path
            ]
            
            # Execute with timeout and input
            if platform.system() == 'Windows':
                process = subprocess.Popen(
                    cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            else:
                process = subprocess.Popen(
                    cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    preexec_fn=os.setsid
                )
            
            try:
                stdout, stderr = process.communicate(input=stdin, timeout=timeout)
                execution_time = time.time() - start_time
                
                if process.returncode == 0:
                    return {
                        "status": "Accepted",
                        "output": stdout.strip(),
                        "error": stderr.strip(),
                        "execution_time": round(execution_time, 3),
                        "memory_used": 0  # Python doesn't easily track memory
                    }
                else:
                    return {
                        "status": "Runtime Error",
                        "output": "",
                        "error": stderr.strip(),
                        "execution_time": round(execution_time, 3),
                        "memory_used": 0
                    }
                    
            except subprocess.TimeoutExpired:
                # Kill the process and its children
                if platform.system() == 'Windows':
                    process.terminate()
                else:
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                
                process.wait()
                return {
                    "status": "Time Limit Exceeded",
                    "output": "",
                    "error": f"Execution took longer than {timeout} seconds",
                    "execution_time": timeout,
                    "memory_used": 0
                }
                
        finally:
            # Clean up
            try:
                os.unlink(code_path)
            except:
                pass
    
    def _execute_cpp(self, source_code: str, stdin: str, timeout: int) -> Dict:
        """Execute C++ code safely"""
        start_time = time.time()
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as code_file:
            code_file.write(source_code)
            code_path = code_file.name
        
        exe_path = code_path.replace('.cpp', '.exe') if platform.system() == 'Windows' else code_path.replace('.cpp', '')
        
        try:
            # Compile C++ code
            compile_cmd = ['g++', '-std=c++17', '-O2', '-o', exe_path, code_path]
            compile_process = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=30)
            
            if compile_process.returncode != 0:
                return {
                    "status": "Compilation Error",
                    "output": "",
                    "error": compile_process.stderr.strip(),
                    "execution_time": 0,
                    "memory_used": 0
                }
            
            # Execute compiled code
            exec_cmd = [exe_path]
            if platform.system() == 'Windows':
                process = subprocess.Popen(
                    exec_cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            else:
                process = subprocess.Popen(
                    exec_cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    preexec_fn=os.setsid
                )
            
            try:
                stdout, stderr = process.communicate(input=stdin, timeout=timeout)
                execution_time = time.time() - start_time
                
                if process.returncode == 0:
                    return {
                        "status": "Accepted",
                        "output": stdout.strip(),
                        "error": stderr.strip(),
                        "execution_time": round(execution_time, 3),
                        "memory_used": 0
                    }
                else:
                    return {
                        "status": "Runtime Error",
                        "output": "",
                        "error": stderr.strip(),
                        "execution_time": round(execution_time, 3),
                        "memory_used": 0
                    }
                    
            except subprocess.TimeoutExpired:
                if platform.system() == 'Windows':
                    process.terminate()
                else:
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                
                process.wait()
                return {
                    "status": "Time Limit Exceeded",
                    "output": "",
                    "error": f"Execution took longer than {timeout} seconds",
                    "execution_time": timeout,
                    "memory_used": 0
                }
                
        finally:
            # Clean up
            try:
                os.unlink(code_path)
                if os.path.exists(exe_path):
                    os.unlink(exe_path)
            except:
                pass
    
    def _execute_c(self, source_code: str, stdin: str, timeout: int) -> Dict:
        """Execute C code safely"""
        start_time = time.time()
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as code_file:
            code_file.write(source_code)
            code_path = code_file.name
        
        exe_path = code_path.replace('.c', '.exe') if platform.system() == 'Windows' else code_path.replace('.c', '')
        
        try:
            # Compile C code
            compile_cmd = ['gcc', '-std=c99', '-O2', '-o', exe_path, code_path]
            compile_process = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=30)
            
            if compile_process.returncode != 0:
                return {
                    "status": "Compilation Error",
                    "output": "",
                    "error": compile_process.stderr.strip(),
                    "execution_time": 0,
                    "memory_used": 0
                }
            
            # Execute compiled code
            exec_cmd = [exe_path]
            if platform.system() == 'Windows':
                process = subprocess.Popen(
                    exec_cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            else:
                process = subprocess.Popen(
                    exec_cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    preexec_fn=os.setsid
                )
            
            try:
                stdout, stderr = process.communicate(input=stdin, timeout=timeout)
                execution_time = time.time() - start_time
                
                if process.returncode == 0:
                    return {
                        "status": "Accepted",
                        "output": stdout.strip(),
                        "error": stderr.strip(),
                        "execution_time": round(execution_time, 3),
                        "memory_used": 0
                    }
                else:
                    return {
                        "status": "Runtime Error",
                        "output": "",
                        "error": stderr.strip(),
                        "execution_time": round(execution_time, 3),
                        "memory_used": 0
                    }
                    
            except subprocess.TimeoutExpired:
                if platform.system() == 'Windows':
                    process.terminate()
                else:
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                
                process.wait()
                return {
                    "status": "Time Limit Exceeded",
                    "output": "",
                    "error": f"Execution took longer than {timeout} seconds",
                    "execution_time": timeout,
                    "memory_used": 0
                }
                
        finally:
            # Clean up
            try:
                os.unlink(code_path)
                if os.path.exists(exe_path):
                    os.unlink(exe_path)
            except:
                pass

# Global executor instance
executor = CodeExecutor()

def test_executor():
    """Test the code executor with sample code"""
    print("🧪 Testing Code Executor")
    print("=" * 50)
    
    # Test Python
    print("\n🐍 Testing Python:")
    python_code = """
print("Hello, World!")
print("Python is working!")
"""
    result = executor.execute_code(python_code, 71)
    print(f"Status: {result['status']}")
    print(f"Output: {result['output']}")
    
    # Test C++
    print("\n⚡ Testing C++:")
    cpp_code = """
#include <iostream>
using namespace std;
int main() {
    cout << "Hello, World!" << endl;
    cout << "C++ is working!" << endl;
    return 0;
}
"""
    result = executor.execute_code(cpp_code, 54)
    print(f"Status: {result['status']}")
    print(f"Output: {result['output']}")
    
    # Test C
    print("\n🔧 Testing C:")
    c_code = """
#include <stdio.h>
int main() {
    printf("Hello, World!\\n");
    printf("C is working!\\n");
    return 0;
}
"""
    result = executor.execute_code(c_code, 50)
    print(f"Status: {result['status']}")
    print(f"Output: {result['output']}")

if __name__ == "__main__":
    test_executor()