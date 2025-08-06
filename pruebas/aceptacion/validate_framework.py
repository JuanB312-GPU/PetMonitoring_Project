"""
Quick Test Validation for BDD Framework
This script validates that the BDD framework is properly configured and ready to run
"""
import os
import sys
import subprocess
import requests
import time
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def test_behave_installation():
    """Test if behave is properly installed"""
    try:
        result = subprocess.run(["behave", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ behave is installed:", result.stdout.strip())
            return True
        else:
            print("❌ behave installation issue")
            return False
    except FileNotFoundError:
        print("❌ behave not found - run: pip install -r requirements_acceptance.txt")
        return False

def test_selenium_installation():
    """Test if selenium is properly installed"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        print("✅ Selenium is installed")
        return True
    except ImportError:
        print("❌ Selenium not found - run: pip install -r requirements_acceptance.txt")
        return False

def test_feature_files():
    """Test if feature files exist and are readable"""
    features_dir = Path(__file__).parent / "features"
    
    if not features_dir.exists():
        print("❌ Features directory not found")
        return False
    
    feature_files = list(features_dir.glob("*.feature"))
    if not feature_files:
        print("❌ No feature files found")
        return False
    
    print(f"✅ Found {len(feature_files)} feature files:")
    for f in feature_files:
        print(f"   - {f.name}")
    
    return True

def test_step_definitions():
    """Test if step definition files exist"""
    steps_dir = Path(__file__).parent / "features" / "steps"
    
    if not steps_dir.exists():
        print("❌ Steps directory not found")
        return False
    
    step_files = list(steps_dir.glob("*_steps.py"))
    if not step_files:
        print("❌ No step definition files found")
        return False
    
    print(f"✅ Found {len(step_files)} step definition files:")
    for f in step_files:
        print(f"   - {f.name}")
    
    return True

def test_behave_syntax():
    """Test behave syntax with dry-run"""
    features_dir = Path(__file__).parent / "features"
    
    print("🔍 Testing behave syntax...")
    try:
        result = subprocess.run([
            "behave", 
            str(features_dir),
            "--dry-run",
            "--format", "progress"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Behave syntax test passed")
            # Count scenarios and steps
            lines = result.stdout.split('\\n')
            for line in lines:
                if 'features passed' in line or 'scenarios passed' in line or 'steps passed' in line:
                    print(f"📊 {line}")
            return True
        else:
            print("❌ Behave syntax test failed:")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Behave syntax test timed out")
        return False
    except Exception as e:
        print(f"❌ Error running behave syntax test: {e}")
        return False

def test_application_files():
    """Test if application files exist"""
    required_files = [
        project_root / "main.py",
        project_root / "index.html"
    ]
    
    for file_path in required_files:
        if file_path.exists():
            print(f"✅ Found {file_path.name}")
        else:
            print(f"❌ Missing {file_path}")
            return False
    
    return True

def main():
    """Main validation function"""
    print("🔍 PetCare Monitor - BDD Framework Validation")
    print("=" * 60)
    
    tests = [
        ("Application Files", test_application_files),
        ("Behave Installation", test_behave_installation),
        ("Selenium Installation", test_selenium_installation),
        ("Feature Files", test_feature_files),
        ("Step Definitions", test_step_definitions),
        ("Behave Syntax", test_behave_syntax),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\\n🧪 Testing {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\\n" + "=" * 60)
    print(f"📊 VALIDATION SUMMARY: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ¡BDD Framework is ready for testing!")
        print("\\n💡 Next steps:")
        print("   1. Ensure PostgreSQL is running")
        print("   2. Run: python test_runner_robust.py --db-check")
        print("   3. Run: python test_runner_robust.py --dry-run")
        print("   4. Run: python test_runner_robust.py")
        sys.exit(0)
    else:
        print("❌ BDD Framework has issues that need to be resolved")
        sys.exit(1)

if __name__ == "__main__":
    main()
