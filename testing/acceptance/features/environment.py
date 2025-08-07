"""
Environment setup for BDD tests using behave
"""
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
from urllib.parse import urljoin

def before_all(context):
    """Setup before all tests"""
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    
    # Initialize WebDriver with error handling
    try:
        service = Service(ChromeDriverManager().install())
        context.driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"Failed to initialize Chrome WebDriver: {e}")
        print("Trying to use system Chrome...")
        try:
            # Try without ChromeDriverManager
            context.driver = webdriver.Chrome(options=chrome_options)
        except Exception as e2:
            print(f"Failed to initialize system Chrome: {e2}")
            print("WebDriver initialization failed. Please ensure Chrome is installed.")
            raise e2
    
    context.driver.implicitly_wait(10)
    
    # Application configuration
    context.base_url = os.getenv('BASE_URL', 'http://localhost:8000')
    context.api_base_url = urljoin(context.base_url, '/api')
    
    # Test data storage
    context.test_users = {}
    context.test_pets = {}
    context.current_user = None
    context.current_pet = None
    
    # Wait for application to be ready
    wait_for_application(context)

def after_all(context):
    """Cleanup after all tests"""
    try:
        if hasattr(context, 'driver') and context.driver is not None:
            context.driver.quit()
            print("WebDriver closed successfully")
    except Exception as e:
        print(f"Error closing WebDriver: {e}")

def before_scenario(context, scenario):
    """Setup before each scenario"""
    try:
        # Ensure we have a valid page loaded before clearing storage
        if not hasattr(context, 'driver') or context.driver is None:
            print("WebDriver not available, skipping scenario setup")
            return
            
        # Navigate to base URL first to ensure we have a valid page
        context.driver.get(context.base_url)
        
        # Clear cookies and local storage with error handling
        try:
            context.driver.delete_all_cookies()
        except Exception as e:
            print(f"Could not clear cookies: {e}")
            
        try:
            context.driver.execute_script("localStorage.clear();")
        except Exception as e:
            print(f"Could not clear localStorage: {e}")
            
        try:
            context.driver.execute_script("sessionStorage.clear();")
        except Exception as e:
            print(f"Could not clear sessionStorage: {e}")
        
        # Reset test data for each scenario
        context.current_user = None
        context.current_pet = None
        
    except Exception as e:
        print(f"Error in before_scenario: {e}")
        # Continue with the test even if setup fails

def after_scenario(context, scenario):
    """Cleanup after each scenario"""
    try:
        # Take screenshot on failure
        if scenario.status == "failed" and hasattr(context, 'driver') and context.driver is not None:
            screenshot_name = f"failed_{scenario.name.replace(' ', '_')}.png"
            screenshot_path = os.path.join("screenshots", screenshot_name)
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            
            try:
                context.driver.save_screenshot(screenshot_path)
                print(f"Screenshot saved: {screenshot_path}")
            except Exception as e:
                print(f"Could not save screenshot: {e}")
                
    except Exception as e:
        print(f"Error in after_scenario: {e}")

def wait_for_application(context, timeout=30):
    """Wait for the application to be ready"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(context.base_url, timeout=5)
            if response.status_code == 200:
                print(f"Application is ready at {context.base_url}")
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    
    raise Exception(f"Application not ready after {timeout} seconds")
