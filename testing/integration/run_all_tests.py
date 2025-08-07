import subprocess
import sys
import os

def run_pytest_on_file(test_file):
    print(f"Running tests in {test_file}...")
    result = subprocess.run([sys.executable, '-m', 'pytest', test_file], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
    return result.returncode

def main():
    # List of test files to run
    test_files = [
        'test_report.py',
        'test_beh.py',
        'test_auth.py',
        'test_login.py',
        'test_pet.py',
        'test_form.py',
    ]
    failed = False
    for test_file in test_files:
        # Look for the file in the root directory
        if os.path.exists(os.path.join(os.getcwd(), test_file)):
            code = run_pytest_on_file(test_file)
            if code != 0:
                failed = True
        else:
            print(f"Warning: {test_file} not found in the current directory.")
    if failed:
        print("\nSome tests failed.")
        sys.exit(1)
    else:
        print("\nAll tests passed successfully.")

if __name__ == "__main__":
    main()
