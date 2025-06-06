#!/usr/bin/env python3
"""
Test script to verify EchoLoop system components
"""

import os
import sys
import importlib.util
import requests
import time
from pathlib import Path

def test_python_version():
    """Test Python version compatibility."""
    print("🐍 Testing Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✅ Python {sys.version.split()[0]} is compatible")
    return True

def test_env_file():
    """Test .env file configuration."""
    print("🔑 Testing .env configuration...")
    if not Path('.env').exists():
        print("❌ .env file not found")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
        if 'GEMINI_API_KEY=' in content and 'AIzaSy' in content:
            print("✅ Gemini API key configured")
            return True
        else:
            print("❌ Gemini API key not properly configured")
            return False

def test_dependencies():
    """Test required dependencies."""
    print("📦 Testing dependencies...")
    required_modules = [
        'flask', 'selenium', 'pyautogui', 'pytesseract', 
        'cv2', 'numpy', 'PIL', 'keyboard', 'git'
    ]
    
    missing = []
    for module in required_modules:
        try:
            if module == 'cv2':
                import cv2
            elif module == 'PIL':
                from PIL import Image
            elif module == 'git':
                import git
            else:
                __import__(module)
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ❌ {module}")
            missing.append(module)
    
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        return False
    
    print("✅ All dependencies available")
    return True

def test_core_modules():
    """Test core system modules."""
    print("🔧 Testing core modules...")
    modules = [
        'task_queue', 'web_monitor', 'echo_loop', 
        'gemini_agent', 'browser_controller', 'screen_reader',
        'chatgpt_typer', 'file_writer'
    ]
    
    failed = []
    for module in modules:
        try:
            spec = importlib.util.spec_from_file_location(module, f"{module}.py")
            if spec and spec.loader:
                print(f"  ✅ {module}.py")
            else:
                print(f"  ❌ {module}.py")
                failed.append(module)
        except Exception as e:
            print(f"  ❌ {module}.py - {str(e)}")
            failed.append(module)
    
    if failed:
        print(f"❌ Failed modules: {', '.join(failed)}")
        return False
    
    print("✅ All core modules available")
    return True

def test_web_monitor():
    """Test web monitor accessibility."""
    print("🌐 Testing web monitor...")
    try:
        response = requests.get('http://localhost:5000', timeout=5)
        if response.status_code == 200:
            print("✅ Web monitor is accessible")
            return True
        else:
            print(f"❌ Web monitor returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Web monitor is not running")
        return False
    except Exception as e:
        print(f"❌ Web monitor test failed: {str(e)}")
        return False

def test_api_endpoints():
    """Test API endpoints."""
    print("🔌 Testing API endpoints...")
    endpoints = ['/api/state', '/api/control']
    
    for endpoint in endpoints:
        try:
            if endpoint == '/api/control':
                # Test POST endpoint
                response = requests.post(f'http://localhost:5000{endpoint}', 
                                       json={'command': 'status'}, timeout=5)
            else:
                # Test GET endpoint
                response = requests.get(f'http://localhost:5000{endpoint}', timeout=5)
            
            if response.status_code in [200, 400]:  # 400 is expected for invalid commands
                print(f"  ✅ {endpoint}")
            else:
                print(f"  ❌ {endpoint} - Status {response.status_code}")
                return False
        except Exception as e:
            print(f"  ❌ {endpoint} - {str(e)}")
            return False
    
    print("✅ All API endpoints working")
    return True

def test_file_structure():
    """Test required file structure."""
    print("📁 Testing file structure...")
    required_files = [
        'requirements.txt', 'README.md', '.gitignore',
        'ai_1_out.txt', 'ai_2_out.txt', 'ai_3_out.txt'
    ]
    
    required_dirs = ['templates', 'logs']
    
    missing = []
    for file in required_files:
        if not Path(file).exists():
            missing.append(file)
            print(f"  ❌ {file}")
        else:
            print(f"  ✅ {file}")
    
    for dir in required_dirs:
        if not Path(dir).exists():
            missing.append(dir)
            print(f"  ❌ {dir}/")
        else:
            print(f"  ✅ {dir}/")
    
    if missing:
        print(f"❌ Missing files/directories: {', '.join(missing)}")
        return False
    
    print("✅ File structure is correct")
    return True

def main():
    """Run all tests."""
    print("=" * 50)
    print("    EchoLoop System Test Suite")
    print("=" * 50)
    print()
    
    tests = [
        test_python_version,
        test_env_file,
        test_file_structure,
        test_dependencies,
        test_core_modules,
        test_web_monitor,
        test_api_endpoints
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
            print()
    
    print("=" * 50)
    print(f"    Test Results: {passed}/{total} passed")
    print("=" * 50)
    
    if passed == total:
        print("🎉 All tests passed! System is ready for prompt-to-production!")
        print()
        print("🚀 To start the system:")
        print("   1. Run: start_system.bat")
        print("   2. Open: http://localhost:5000")
        print("   3. Click 'Start' to begin automation")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 