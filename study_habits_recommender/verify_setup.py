#!/usr/bin/env python3
"""
System Verification Script for Study Habits Recommender
Checks if all components are properly set up
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8+"""
    version = sys.version_info
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 8:
        return True
    print("  ⚠ Warning: Python 3.8+ recommended")
    return False

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✓ {description}: Found")
        return True
    else:
        print(f"✗ {description}: Missing")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists"""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        print(f"✓ {description}: Found")
        return True
    else:
        print(f"✗ {description}: Missing")
        return False

def main():
    print("=" * 60)
    print("Study Habits Recommender - System Verification")
    print("=" * 60)
    print()
    
    all_checks = []
    
    # Python version check
    print("1. Python Environment")
    print("-" * 40)
    all_checks.append(check_python_version())
    print()
    
    # Core files check
    print("2. Core Application Files")
    print("-" * 40)
    all_checks.append(check_file_exists("app.py", "Main application"))
    all_checks.append(check_file_exists("requirements.txt", "Dependencies file"))
    all_checks.append(check_file_exists("README.md", "Documentation"))
    all_checks.append(check_file_exists("QUICKSTART.md", "Quick start guide"))
    print()
    
    # Template files check
    print("3. HTML Templates")
    print("-" * 40)
    all_checks.append(check_file_exists("templates/base.html", "Base template"))
    all_checks.append(check_file_exists("templates/index.html", "Landing page"))
    all_checks.append(check_file_exists("templates/student_login.html", "Student login"))
    all_checks.append(check_file_exists("templates/student_dashboard.html", "Student dashboard"))
    all_checks.append(check_file_exists("templates/admin_login.html", "Admin login"))
    all_checks.append(check_file_exists("templates/admin_dashboard.html", "Admin dashboard"))
    print()
    
    # Static files check
    print("4. Static Files (CSS/JS)")
    print("-" * 40)
    all_checks.append(check_file_exists("static/css/style.css", "Main stylesheet"))
    all_checks.append(check_file_exists("static/js/main.js", "JavaScript utilities"))
    print()
    
    # Directory structure check
    print("5. Directory Structure")
    print("-" * 40)
    all_checks.append(check_directory_exists("templates", "Templates directory"))
    all_checks.append(check_directory_exists("static", "Static files directory"))
    
    # Create missing directories
    for dir_name in ["models", "data", "uploads"]:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"✓ {dir_name.capitalize()} directory: Created")
        else:
            print(f"✓ {dir_name.capitalize()} directory: Found")
    print()
    
    # Run scripts check
    print("6. Run Scripts")
    print("-" * 40)
    check_file_exists("run.sh", "Linux/macOS run script")
    check_file_exists("run.bat", "Windows run script")
    print()
    
    # Dependencies check
    print("7. Python Dependencies")
    print("-" * 40)
    try:
        import flask
        print(f"✓ Flask: {flask.__version__}")
        all_checks.append(True)
    except ImportError:
        print("✗ Flask: Not installed")
        all_checks.append(False)
    
    try:
        import numpy
        print(f"✓ NumPy: {numpy.__version__}")
        all_checks.append(True)
    except ImportError:
        print("✗ NumPy: Not installed")
        all_checks.append(False)
    
    try:
        import pandas
        print(f"✓ Pandas: {pandas.__version__}")
        all_checks.append(True)
    except ImportError:
        print("✗ Pandas: Not installed")
        all_checks.append(False)
    
    try:
        import sklearn
        print(f"✓ scikit-learn: {sklearn.__version__}")
        all_checks.append(True)
    except ImportError:
        print("✗ scikit-learn: Not installed")
        all_checks.append(False)
    
    print()
    
    # Summary
    print("=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = sum(all_checks)
    total = len(all_checks)
    percentage = (passed / total) * 100 if total > 0 else 0
    
    print(f"Checks passed: {passed}/{total} ({percentage:.1f}%)")
    print()
    
    if percentage == 100:
        print("🎉 All checks passed! System is ready to run.")
        print()
        print("To start the application:")
        print("  • Windows: run.bat")
        print("  • Linux/macOS: ./run.sh")
        print("  • Or: python app.py")
        print()
        print("Then open: http://localhost:5000")
    elif percentage >= 80:
        print("⚠ Most checks passed. You can try running the application.")
        print("   Install missing dependencies with: pip install -r requirements.txt")
    else:
        print("❌ Several checks failed. Please:")
        print("   1. Ensure all files are present")
        print("   2. Install dependencies: pip install -r requirements.txt")
        print("   3. Run this script again")
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()
