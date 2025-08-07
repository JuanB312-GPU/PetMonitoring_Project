"""
Robust BDD Test Runner for PetCare Monitor Acceptance Tests
This runner includes database connection checks and better error handling
"""
import os
import sys
import subprocess
import time
import requests
import psycopg2
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def check_postgresql():
    """Check if PostgreSQL is running and accessible"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="Diminumero12",
            database="PetMonitoring"
        )
        conn.close()
        print("✅ PostgreSQL database is accessible")
        return True
    except psycopg2.OperationalError as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        print("💡 Please ensure PostgreSQL is running and the database 'PetMonitoring' exists")
        return False
    except Exception as e:
        print(f"❌ Database check failed: {e}")
        return False

def wait_for_database():
    """Wait for database to be ready"""
    print("🔍 Checking database connection...")
    max_attempts = 10
    
    for attempt in range(max_attempts):
        if check_postgresql():
            return True
        
        if attempt < max_attempts - 1:
            print(f"⏳ Attempt {attempt + 1}/{max_attempts} failed, retrying in 3 seconds...")
            time.sleep(3)
    
    print("❌ Database not available after all attempts")
    return False

def install_requirements():
    """Install required packages for acceptance testing"""
    requirements_file = Path(__file__).parent / "requirements_acceptance.txt"
    
    if requirements_file.exists():
        print("📦 Installing acceptance test requirements...")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ], check=True, capture_output=True, text=True)
            print("✅ Requirements installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install requirements: {e}")
            print(f"STDOUT: {e.stdout}")
            print(f"STDERR: {e.stderr}")
            sys.exit(1)
    else:
        print("⚠️ Requirements file not found, assuming packages are installed")

def start_application():
    """Start the PetCare Monitor application"""
    print("🚀 Starting PetCare Monitor application...")
    
    try:
        # Change to project root directory
        os.chdir(project_root)
        
        # Start the FastAPI application
        app_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main:app", 
            "--host", "0.0.0.0", "--port", "8000", "--reload"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait for application to start
        print("⏳ Waiting for application to start...")
        time.sleep(15)  # Give more time for startup
        
        # Check if application is responding
        max_attempts = 20
        for attempt in range(max_attempts):
            try:
                response = requests.get("http://localhost:8000", timeout=5)
                if response.status_code == 200:
                    print(f"✅ Application started successfully at http://localhost:8000")
                    return app_process
            except requests.exceptions.RequestException:
                pass
            
            if attempt < max_attempts - 1:
                print(f"⏳ Waiting for app to respond... {attempt + 1}/{max_attempts}")
                time.sleep(2)
        
        print("❌ Application did not respond after startup")
        app_process.terminate()
        return None
        
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        return None

def run_dry_run_tests():
    """Run tests in dry-run mode to check for syntax issues"""
    features_dir = Path(__file__).parent / "features"
    
    print("🔍 Running dry-run tests (syntax check)...")
    
    try:
        result = subprocess.run([
            "behave", 
            str(features_dir),
            "--dry-run",
            "--verbose",
            "--format", "pretty"
        ], capture_output=True, text=True, check=False)
        
        if result.returncode == 0:
            print("✅ Dry-run tests passed - no syntax errors")
            print(result.stdout)
        else:
            print("❌ Dry-run tests failed:")
            print(result.stdout)
            print(result.stderr)
            
        return result.returncode == 0
        
    except FileNotFoundError:
        print("❌ behave not found. Please install it using: pip install behave")
        return False
    except Exception as e:
        print(f"❌ Error running dry-run tests: {e}")
        return False

def run_acceptance_tests():
    """Run the BDD acceptance tests using behave"""
    features_dir = Path(__file__).parent / "features"
    
    print("🧪 Running BDD acceptance tests...")
    print(f"Features directory: {features_dir}")
    
    # Set environment variables
    os.environ['BASE_URL'] = 'http://localhost:8000'
    
    try:
        # Run behave with verbose output
        result = subprocess.run([
            "behave", 
            str(features_dir),
            "--verbose",
            "--no-capture",
            "--format", "pretty",
            "--tags", "~@skip"  # Skip tests tagged with @skip
        ], check=False)
        
        return result.returncode == 0
        
    except FileNotFoundError:
        print("❌ behave not found. Please install it using: pip install behave")
        return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def cleanup_test_data():
    """Clean up test data from database"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="Diminumero12",
            database="PetMonitoring"
        )
        cursor = conn.cursor()
        
        # Delete test users
        cursor.execute("DELETE FROM \"USER\" WHERE email LIKE '%test%' OR email LIKE '%example%'")
        conn.commit()
        
        cursor.close()
        conn.close()
        print("🧹 Test data cleaned up")
    except Exception as e:
        print(f"⚠️ Could not clean test data: {e}")

def main():
    """Main test runner function"""
    print("🚀 PetCare Monitor - Robust BDD Acceptance Test Runner")
    print("=" * 70)
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--install":
            install_requirements()
            return
        elif command == "--dry-run":
            install_requirements()
            success = run_dry_run_tests()
            sys.exit(0 if success else 1)
        elif command == "--db-check":
            success = wait_for_database()
            sys.exit(0 if success else 1)
        elif command == "--cleanup":
            cleanup_test_data()
            return
        elif command == "--help":
            print("Usage:")
            print("  python test_runner_robust.py --install     Install requirements")
            print("  python test_runner_robust.py --dry-run     Run syntax check only")
            print("  python test_runner_robust.py --db-check    Check database connection")
            print("  python test_runner_robust.py --cleanup     Clean test data")
            print("  python test_runner_robust.py               Run all tests")
            return
    
    # Install requirements
    install_requirements()
    
    # Check database first
    if not wait_for_database():
        print("❌ Cannot proceed without database connection")
        sys.exit(1)
    
    # Run dry-run first
    print("\\n" + "="*50)
    if not run_dry_run_tests():
        print("❌ Dry-run tests failed, stopping execution")
        sys.exit(1)
    
    # Start application
    print("\\n" + "="*50)
    app_process = start_application()
    
    if not app_process:
        print("❌ Could not start application")
        sys.exit(1)
    
    success = False
    try:
        # Run all acceptance tests
        print("\\n" + "="*50)
        success = run_acceptance_tests()
        
        if success:
            print("\\n🎉 All acceptance tests passed!")
        else:
            print("\\n❌ Some acceptance tests failed")
            
    except KeyboardInterrupt:
        print("\\n⏹️ Tests interrupted by user")
        
    finally:
        # Stop application
        print("\\n🛑 Stopping application...")
        if app_process:
            app_process.terminate()
            try:
                app_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                app_process.kill()
        
        # Clean up test data
        cleanup_test_data()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
