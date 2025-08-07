"""
Step definitions for user registration features
"""
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import requests
import json

# Given steps

@given('the PetCare Monitor application is running')
def step_application_running(context):
    """Verify the application is running"""
    context.driver.get(context.base_url)
    try:
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    except TimeoutException:
        raise Exception("Application is not running or not accessible")

@given('I am on the home page')
def step_on_home_page(context):
    """Navigate to home page"""
    context.driver.get(context.base_url)
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "app"))
    )

@given('I am on the registration page')
def step_on_registration_page(context):
    """Navigate to registration page"""
    context.driver.get(context.base_url)
    
    # Wait for page to load
    WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.ID, "register-btn"))
    )
    
    # Click register button to open modal
    register_btn = context.driver.find_element(By.ID, "register-btn")
    register_btn.click()
    
    # Wait for modal to appear
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "auth-modal"))
    )
    
    # Wait for register form to be visible
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "register-form"))
    )

@given('a user exists with email "{email}"')
def step_user_exists(context, email):
    """Create a test user"""
    # Store test user data
    user_data = {
        "name": "Test User",
        "email": email,
        "phone": "3001234567",
        "password": "Password123!",
        "confirmPassword": "Password123!"
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
            print(f"Test user created successfully: {email}")
        else:
            print(f"Failed to create test user. Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Warning: Could not create test user via API: {e}")
        # Store for later use in tests
        context.test_users[email] = user_data

# When steps

@when('I enter name "{name}"')
def step_enter_name(context, name):
    """Enter name in registration form"""
    name_field = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "register-name"))
    )
    name_field.clear()
    name_field.send_keys(name)
    context.current_user_name = name

@when('I enter phone "{phone}"')
def step_enter_phone(context, phone):
    """Enter phone in registration form"""
    phone_field = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "register-phone"))
    )
    phone_field.clear()
    phone_field.send_keys(phone)

@when('I confirm password "{confirm_password}"')
def step_confirm_password(context, confirm_password):
    """Enter password confirmation"""
    confirm_field = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "register-confirm-password"))
    )
    confirm_field.clear()
    confirm_field.send_keys(confirm_password)

@when('I click the register button')
def step_click_register(context):
    """Click the register button"""
    register_form = context.driver.find_element(By.ID, "register-form")
    submit_btn = register_form.find_element(By.CSS_SELECTOR, "button[type='submit']")
    
    # Scroll to button if needed
    context.driver.execute_script("arguments[0].scrollIntoView();", submit_btn)
    
    # Click submit button
    submit_btn.click()
    
    # Wait a moment for form submission
    time.sleep(2)

# Then steps

@then('I should be redirected to the dashboard')
def step_redirected_to_dashboard(context):
    """Verify redirection to dashboard"""
    try:
        # Wait for modal to close
        WebDriverWait(context.driver, 10).until_not(
            EC.visibility_of_element_located((By.ID, "auth-modal"))
        )
        
        # Check if user content is visible (indicating successful login)
        WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "user-content"))
        )
        
        # Verify logout button is present (indicates user is logged in)
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, "logout-btn"))
        )
        
    except TimeoutException:
        raise AssertionError("User was not redirected to dashboard after registration")

@then('I should see the welcome message "{message}"')
def step_see_welcome_message(context, message):
    """Verify welcome message is displayed"""
    try:
        welcome_element = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, "welcome-message"))
        )
        actual_message = welcome_element.text
        assert message in actual_message, f"Expected '{message}' in welcome message, but got '{actual_message}'"
    except TimeoutException:
        raise AssertionError(f"Welcome message '{message}' not found")

@then('I should see my user account created successfully')
def step_account_created_successfully(context):
    """Verify account was created successfully"""
    # Check that user is now logged in (logout button visible)
    try:
        WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "nav-user"))
        )
        
        # Check that auth buttons are hidden
        nav_auth = context.driver.find_element(By.ID, "nav-auth")
        assert "hidden" in nav_auth.get_attribute("class"), "Auth buttons should be hidden when logged in"
        
    except TimeoutException:
        raise AssertionError("User account does not appear to be created successfully")

@then('I should see the error message "{error_message}"')
def step_see_error_message(context, error_message):
    """Verify error message is displayed"""
    try:
        # Wait a bit for error message to appear
        time.sleep(1)
        
        # Look for error message in various possible locations
        error_selectors = [
            ".form-error",
            ".error-message",
            ".alert-error",
            "[class*='error']"
        ]
        
        error_found = False
        for selector in error_selectors:
            try:
                error_elements = context.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in error_elements:
                    if element.is_displayed() and error_message.lower() in element.text.lower():
                        error_found = True
                        break
                if error_found:
                    break
            except:
                continue
        
        assert error_found, f"Error message '{error_message}' not found on page"
        
    except Exception as e:
        raise AssertionError(f"Could not verify error message '{error_message}': {str(e)}")

@then('I should remain on the registration page')
def step_remain_on_registration_page(context):
    """Verify user remains on registration page"""
    try:
        # Check that the registration modal is still visible
        modal = context.driver.find_element(By.ID, "auth-modal")
        assert modal.is_displayed(), "Registration modal should still be visible"
        
        # Check that register form is visible
        register_form = context.driver.find_element(By.ID, "register-form")
        assert register_form.is_displayed(), "Registration form should still be visible"
        
    except Exception as e:
        raise AssertionError(f"User did not remain on registration page: {str(e)}")

@then('I should see validation errors for email format')
def step_see_email_validation_errors(context):
    """Verify email format validation errors"""
    # HTML5 validation or custom validation should prevent submission
    email_field = context.driver.find_element(By.ID, "register-email")
    
    # Check HTML5 validation state
    validation_message = context.driver.execute_script(
        "return arguments[0].validationMessage;", email_field
    )
    
    assert validation_message != "", f"Email field should have validation message"
