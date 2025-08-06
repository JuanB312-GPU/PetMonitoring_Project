"""
Step definitions for user authentication features
"""
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import requests

# Given steps

@given('a user exists with email "{email}" and password "{password}"')
def step_user_exists_with_credentials(context, email, password):
    """Create a test user with specific credentials"""
    user_data = {
        "name": "Test User",
        "email": email,
        "phone": "3001234567",
        "password": password,
        "confirmPassword": password
    }
    
    # Try to register user via API
    try:
        response = requests.post(
            f"{context.api_base_url}/auth/register",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code in [200, 201]:
            context.test_users[email] = user_data
            print(f"Test user created: {email}")
        else:
            print(f"Failed to create test user. Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Warning: Could not create test user via API: {e}")
        # Store for later use
        context.test_users[email] = user_data

@given('I am on the login page')
def step_on_login_page(context):
    """Navigate to login page"""
    context.driver.get(context.base_url)
    
    # Wait for page to load
    WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.ID, "login-btn"))
    )
    
    # Click login button to open modal
    login_btn = context.driver.find_element(By.ID, "login-btn")
    login_btn.click()
    
    # Wait for modal to appear
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "auth-modal"))
    )
    
    # Wait for login form to be visible
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "login-form"))
    )

@given('I am logged in as "{email}"')
def step_logged_in_as(context, email):
    """Log in with specific user credentials"""
    # First navigate to home page
    context.driver.get(context.base_url)
    
    # Get user data
    if email in context.test_users:
        user_data = context.test_users[email]
    else:
        # Create default test user
        user_data = {
            "name": "Test User", 
            "email": email, 
            "password": "Password123!"
        }
        # Try to create user first
        try:
            requests.post(
                f"{context.api_base_url}/auth/register",
                json={**user_data, "phone": "3001234567", "confirmPassword": "Password123!"},
                headers={"Content-Type": "application/json"}
            )
            print(f"Created test user for login: {email}")
        except Exception as e:
            print(f"Could not create test user: {e}")
            pass
    
    # Open login modal
    WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.ID, "login-btn"))
    )
    login_btn = context.driver.find_element(By.ID, "login-btn")
    login_btn.click()
    
    # Wait for login form
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "login-form"))
    )
    
    # Fill login form
    email_field = context.driver.find_element(By.ID, "login-email")
    password_field = context.driver.find_element(By.ID, "login-password")
    
    email_field.send_keys(email)
    password_field.send_keys(user_data["password"])
    
    # Submit login form
    login_form = context.driver.find_element(By.ID, "login-form")
    submit_btn = login_form.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_btn.click()
    
    # Wait for successful login
    try:
        WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "nav-user"))
        )
        context.current_user = {"email": email, **user_data}
    except TimeoutException:
        print(f"Warning: Could not log in user {email}")

@given('I am on the dashboard page')
def step_on_dashboard_page(context):
    """Navigate to dashboard page"""
    # If not logged in, this will show guest content
    context.driver.get(context.base_url)
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "home-page"))
    )

# When steps

@when('I enter email "{email}"')
def step_enter_login_email(context, email):
    """Enter email in login form"""
    email_field = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "login-email"))
    )
    email_field.clear()
    email_field.send_keys(email)

@when('I enter password "{password}"')
def step_enter_login_password(context, password):
    """Enter password in login form"""
    password_field = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "login-password"))
    )
    password_field.clear()
    password_field.send_keys(password)

@when('I click the login button')
def step_click_login(context):
    """Click the login button"""
    login_form = context.driver.find_element(By.ID, "login-form")
    submit_btn = login_form.find_element(By.CSS_SELECTOR, "button[type='submit']")
    
    # Scroll to button if needed
    context.driver.execute_script("arguments[0].scrollIntoView();", submit_btn)
    
    # Click submit button
    submit_btn.click()
    
    # Wait a moment for form submission
    time.sleep(2)

@when('I click the login button without entering credentials')
def step_click_login_empty(context):
    """Click login button with empty fields"""
    login_form = context.driver.find_element(By.ID, "login-form")
    submit_btn = login_form.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_btn.click()
    time.sleep(1)

@when('I click the logout button')
def step_click_logout(context):
    """Click the logout button"""
    logout_btn = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.ID, "logout-btn"))
    )
    logout_btn.click()
    time.sleep(1)

# Then steps

@then('I should be successfully authenticated')
def step_successfully_authenticated(context):
    """Verify successful authentication"""
    try:
        # Wait for modal to close
        WebDriverWait(context.driver, 10).until_not(
            EC.visibility_of_element_located((By.ID, "auth-modal"))
        )
        
        # Check if user navigation is visible
        WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "nav-user"))
        )
        
        # Check if logout button is present
        logout_btn = context.driver.find_element(By.ID, "logout-btn")
        assert logout_btn.is_displayed(), "Logout button should be visible when authenticated"
        
    except TimeoutException:
        raise AssertionError("User was not successfully authenticated")

@then('I should not be authenticated')
def step_not_authenticated(context):
    """Verify user is not authenticated"""
    try:
        # Check that auth buttons are still visible
        nav_auth = WebDriverWait(context.driver, 5).until(
            EC.visibility_of_element_located((By.ID, "nav-auth"))
        )
        assert nav_auth.is_displayed(), "Auth buttons should be visible when not authenticated"
        
        # Check that user nav is hidden
        nav_user = context.driver.find_element(By.ID, "nav-user")
        assert "hidden" in nav_user.get_attribute("class"), "User nav should be hidden when not authenticated"
        
    except TimeoutException:
        raise AssertionError("User appears to be authenticated when they should not be")

@then('I should see validation errors for required fields')
def step_see_required_field_errors(context):
    """Verify validation errors for required fields"""
    # Check HTML5 validation
    email_field = context.driver.find_element(By.ID, "login-email")
    password_field = context.driver.find_element(By.ID, "login-password")
    
    # At least one field should have validation message
    email_validation = context.driver.execute_script(
        "return arguments[0].validationMessage;", email_field
    )
    password_validation = context.driver.execute_script(
        "return arguments[0].validationMessage;", password_field
    )
    
    assert email_validation or password_validation, "Should have validation messages for required fields"

@then('I should be logged out successfully')
def step_logged_out_successfully(context):
    """Verify successful logout"""
    try:
        # Check that user nav is hidden
        WebDriverWait(context.driver, 10).until(
            lambda driver: "hidden" in driver.find_element(By.ID, "nav-user").get_attribute("class")
        )
        
        # Check that auth buttons are visible
        WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "nav-auth"))
        )
        
        context.current_user = None
        
    except TimeoutException:
        raise AssertionError("User was not logged out successfully")

@then('I should see the login and register buttons')
def step_see_auth_buttons(context):
    """Verify login and register buttons are visible"""
    try:
        login_btn = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "login-btn"))
        )
        register_btn = context.driver.find_element(By.ID, "register-btn")
        
        assert login_btn.is_displayed(), "Login button should be visible"
        assert register_btn.is_displayed(), "Register button should be visible"
        
    except TimeoutException:
        raise AssertionError("Login and register buttons are not visible")

@then('I should not see the logout button')
def step_not_see_logout_button(context):
    """Verify logout button is not visible"""
    nav_user = context.driver.find_element(By.ID, "nav-user")
    assert "hidden" in nav_user.get_attribute("class"), "Logout button should not be visible when logged out"

@then('I should see the logout button in the navigation')
def step_see_logout_button(context):
    """Verify logout button is visible in navigation"""
    try:
        logout_btn = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "logout-btn"))
        )
        assert logout_btn.is_displayed(), "Logout button should be visible in navigation"
    except TimeoutException:
        raise AssertionError("Logout button is not visible in navigation")
