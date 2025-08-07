"""
Utility functions for BDD acceptance tests
"""
import random
import string
import time
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class TestHelpers:
    """Helper functions for common test operations"""
    
    @staticmethod
    def generate_random_email():
        """Generate a random email for testing"""
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"test_{random_string}@petcare-test.com"
    
    @staticmethod
    def generate_random_phone():
        """Generate a random phone number for testing"""
        return f"300{random.randint(1000000, 9999999)}"
    
    @staticmethod
    def generate_random_pet_name():
        """Generate a random pet name for testing"""
        pet_names = [
            "Buddy", "Max", "Charlie", "Cooper", "Rocky", "Bear", "Tucker", "Duke",
            "Luna", "Bella", "Daisy", "Lucy", "Molly", "Sadie", "Sophie", "Chloe",
            "Whiskers", "Mittens", "Shadow", "Tiger", "Smokey", "Felix", "Oscar"
        ]
        return random.choice(pet_names) + str(random.randint(1, 999))
    
    @staticmethod
    def generate_birthdate(min_age_years=1, max_age_years=15):
        """Generate a random birthdate for pets"""
        today = datetime.now()
        min_date = today - timedelta(days=max_age_years * 365)
        max_date = today - timedelta(days=min_age_years * 365)
        
        random_date = min_date + timedelta(
            days=random.randint(0, (max_date - min_date).days)
        )
        return random_date.strftime("%Y-%m-%d")
    
    @staticmethod
    def wait_for_element(driver, locator, timeout=10):
        """Wait for element to be present and return it"""
        try:
            return WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            raise AssertionError(f"Element {locator} not found within {timeout} seconds")
    
    @staticmethod
    def wait_for_clickable(driver, locator, timeout=10):
        """Wait for element to be clickable and return it"""
        try:
            return WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException:
            raise AssertionError(f"Element {locator} not clickable within {timeout} seconds")
    
    @staticmethod
    def wait_for_text_in_element(driver, locator, text, timeout=10):
        """Wait for specific text to appear in element"""
        try:
            return WebDriverWait(driver, timeout).until(
                EC.text_to_be_present_in_element(locator, text)
            )
        except TimeoutException:
            raise AssertionError(f"Text '{text}' not found in element {locator} within {timeout} seconds")
    
    @staticmethod
    def scroll_to_element(driver, element):
        """Scroll element into view"""
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)  # Brief pause after scroll
    
    @staticmethod
    def clear_and_send_keys(element, text):
        """Clear field and enter text"""
        element.clear()
        element.send_keys(text)
    
    @staticmethod
    def take_screenshot(driver, filename):
        """Take a screenshot and save it"""
        import os
        screenshots_dir = "screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)
        
        filepath = os.path.join(screenshots_dir, filename)
        driver.save_screenshot(filepath)
        return filepath
    
    @staticmethod
    def get_element_text_safe(driver, locator):
        """Safely get element text, return empty string if not found"""
        try:
            element = driver.find_element(*locator)
            return element.text
        except:
            return ""
    
    @staticmethod
    def is_element_present(driver, locator):
        """Check if element is present without waiting"""
        try:
            driver.find_element(*locator)
            return True
        except:
            return False
    
    @staticmethod
    def wait_for_page_load(driver, timeout=10):
        """Wait for page to load completely"""
        WebDriverWait(driver, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

class PetCareSelectors:
    """Common selectors for PetCare Monitor application"""
    
    # Navigation
    LOGIN_BTN = (By.ID, "login-btn")
    REGISTER_BTN = (By.ID, "register-btn")
    LOGOUT_BTN = (By.ID, "logout-btn")
    BRAND_LOGO = (By.ID, "nav-brand")
    PET_SELECTOR = (By.ID, "pet-selector")
    
    # Modals
    AUTH_MODAL = (By.ID, "auth-modal")
    PET_MODAL = (By.ID, "pet-modal")
    ACTIVITY_MODAL = (By.ID, "activity-modal")
    FOOD_MODAL = (By.ID, "food-modal")
    
    # Forms
    LOGIN_FORM = (By.ID, "login-form")
    REGISTER_FORM = (By.ID, "register-form")
    PET_FORM = (By.ID, "pet-form")
    ACTIVITY_FORM = (By.ID, "activity-form")
    FOOD_FORM = (By.ID, "food-form")
    
    # Login/Register Fields
    LOGIN_EMAIL = (By.ID, "login-email")
    LOGIN_PASSWORD = (By.ID, "login-password")
    REGISTER_NAME = (By.ID, "register-name")
    REGISTER_EMAIL = (By.ID, "register-email")
    REGISTER_PHONE = (By.ID, "register-phone")
    REGISTER_PASSWORD = (By.ID, "register-password")
    REGISTER_CONFIRM_PASSWORD = (By.ID, "register-confirm-password")
    
    # Pet Registration Fields
    PET_NAME = (By.ID, "pet-name")
    PET_SPECIES = (By.ID, "pet-species")
    PET_BREED = (By.ID, "pet-breed")
    PET_BIRTHDATE = (By.ID, "pet-birthdate")
    PET_HEIGHT = (By.ID, "pet-height")
    PET_WEIGHT = (By.ID, "pet-weight")
    PET_CONDITIONS = (By.ID, "pet-conditions")
    PET_VACCINES = (By.ID, "pet-vaccines")
    
    # Dashboard Elements
    BMI_VALUE = (By.ID, "bmi-value")
    BMI_STATUS = (By.ID, "bmi-status")
    BCS_VALUE = (By.ID, "bcs-value")
    BCS_STATUS = (By.ID, "bcs-status")
    MER_VALUE = (By.ID, "mer-value")
    MER_STATUS = (By.ID, "mer-status")
    RISK_VALUE = (By.ID, "risk-value")
    RISK_STATUS = (By.ID, "risk-status")
    
    # Pet Information
    SELECTED_PET_INFO = (By.ID, "selected-pet-info")
    BASIC_INFO = (By.ID, "basic-info")
    MEDICAL_HISTORY = (By.ID, "medical-history")
    VACCINATION_HISTORY = (By.ID, "vaccination-history")
    ACTIVITY_HISTORY = (By.ID, "activity-history")
    
    # Buttons
    ADD_PET_BTN = (By.ID, "add-pet-btn")
    VIEW_HISTORY_BTN = (By.ID, "view-history-btn")
    GENERATE_REPORT_BTN = (By.ID, "generate-report-btn")
    
    # Pages
    HOME_PAGE = (By.ID, "home-page")
    DASHBOARD_PAGE = (By.ID, "dashboard-page")
    PETS_PAGE = (By.ID, "pets-page")
    REPORTS_PAGE = (By.ID, "reports-page")
    
    # Content Areas
    GUEST_CONTENT = (By.ID, "guest-content")
    USER_CONTENT = (By.ID, "user-content")
    WELCOME_MESSAGE = (By.ID, "welcome-message")
    PETS_CONTAINER = (By.ID, "pets-container")
    REPORTS_GRID = (By.ID, "reports-grid")

class TestDataFactory:
    """Factory for creating test data"""
    
    @staticmethod
    def create_user_data():
        """Create test user data"""
        return {
            "name": f"Test User {random.randint(1, 1000)}",
            "email": TestHelpers.generate_random_email(),
            "phone": TestHelpers.generate_random_phone(),
            "password": "TestPassword123!"
        }
    
    @staticmethod
    def create_pet_data():
        """Create test pet data"""
        return {
            "name": TestHelpers.generate_random_pet_name(),
            "species": random.choice(["Dog", "Cat"]),
            "breed": random.choice(["Golden Retriever", "Labrador", "Persian", "Siamese"]),
            "birthdate": TestHelpers.generate_birthdate(),
            "height": random.randint(20, 70),
            "weight": round(random.uniform(2.0, 50.0), 1),
            "conditions": random.choice([[], ["Allergy"], ["Diabetes"], ["Allergy", "Arthritis"]]),
            "vaccines": random.choice([["Rabies"], ["Rabies", "Distemper"], ["Rabies", "Parvovirus"]])
        }
    
    @staticmethod
    def create_activity_data():
        """Create test activity data"""
        activities = ["Walking", "Running", "Playing", "Swimming", "Training"]
        frequencies = ["Daily", "Twice daily", "Weekly", "Occasionally"]
        
        return {
            "activity": random.choice(activities),
            "frequency": random.choice(frequencies)
        }
    
    @staticmethod
    def create_feeding_data():
        """Create test feeding data"""
        foods = ["Dry Food", "Wet Food", "Raw Food", "Treats", "Supplements"]
        frequencies = ["Once daily", "Twice daily", "Three times daily", "As needed"]
        
        return {
            "food": random.choice(foods),
            "frequency": random.choice(frequencies)
        }
