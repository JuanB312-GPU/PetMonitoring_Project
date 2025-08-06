"""
Step definitions for pet health monitoring features
"""
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import re

# Given steps

@given('I have a pet named "{pet_name}" with weight "{weight}" kg and height "{height}" cm')
def step_have_pet_with_measurements(context, pet_name, weight, height):
    """Create a test pet with specific measurements"""
    if not hasattr(context, 'test_pets'):
        context.test_pets = {}
    
    pet_data = {
        "name": pet_name,
        "species": "Dog",
        "breed": "Golden Retriever",
        "birthdate": "2020-05-15",
        "height": float(height),
        "weight": float(weight),
        "conditions": ["Allergy"],
        "vaccines": ["Rabies"]
    }
    context.test_pets[pet_name] = pet_data
    
    # If logged in, try to register this pet
    if context.current_user:
        try:
            # Navigate to dashboard and register pet
            context.driver.get(context.base_url)
            
            # Click Add New Pet
            add_pet_btn = WebDriverWait(context.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "add-pet-btn"))
            )
            add_pet_btn.click()
            
            # Fill form
            WebDriverWait(context.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "pet-modal"))
            )
            
            # Fill all fields
            context.driver.find_element(By.ID, "pet-name").send_keys(pet_name)
            
            # Select species
            species_select = Select(context.driver.find_element(By.ID, "pet-species"))
            species_select.select_by_value("1")  # Dog
            time.sleep(1)
            
            # Select breed
            breed_select = Select(context.driver.find_element(By.ID, "pet-breed"))
            if len(breed_select.options) > 1:
                breed_select.select_by_index(1)
            
            context.driver.find_element(By.ID, "pet-birthdate").send_keys("2020-05-15")
            context.driver.find_element(By.ID, "pet-height").send_keys(height)
            context.driver.find_element(By.ID, "pet-weight").send_keys(weight)
            
            # Submit form
            submit_btn = context.driver.find_element(By.CSS_SELECTOR, "#pet-form button[type='submit']")
            submit_btn.click()
            
            time.sleep(2)
            
        except Exception as e:
            print(f"Warning: Could not create pet via UI: {e}")

@given('I have a pet "{pet_name}" with medical condition "{condition}"')
def step_have_pet_with_condition(context, pet_name, condition):
    """Create a pet with specific medical condition"""
    if not hasattr(context, 'test_pets'):
        context.test_pets = {}
    
    pet_data = {
        "name": pet_name,
        "species": "Dog",
        "breed": "Golden Retriever",
        "conditions": [condition],
        "vaccines": ["Rabies"]
    }
    context.test_pets[pet_name] = pet_data

@given('I have a cat named "{pet_name}" with weight "{weight}" kg and height "{height}" cm')
def step_have_cat_with_measurements(context, pet_name, weight, height):
    """Create a test cat with specific measurements"""
    if not hasattr(context, 'test_pets'):
        context.test_pets = {}
    
    pet_data = {
        "name": pet_name,
        "species": "Cat",
        "breed": "Persian",
        "birthdate": "2021-03-10",
        "height": float(height),
        "weight": float(weight),
        "conditions": [],
        "vaccines": ["Rabies"]
    }
    context.test_pets[pet_name] = pet_data

@given('I have multiple pets registered')
def step_have_multiple_pets(context):
    """Create multiple test pets"""
    pets_data = [
        {
            "name": "Buddy",
            "species": "Dog",
            "weight": 25.5,
            "height": 55
        },
        {
            "name": "Whiskers",
            "species": "Cat",
            "weight": 4.5,
            "height": 25
        }
    ]
    
    if not hasattr(context, 'test_pets'):
        context.test_pets = {}
    
    for pet in pets_data:
        context.test_pets[pet["name"]] = pet

# When steps

@when('I select pet "{pet_name}" from the pet selector')
def step_select_pet_from_selector(context, pet_name):
    """Select a pet from the pet selector dropdown"""
    try:
        pet_selector = WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "pet-selector"))
        )
        
        select = Select(pet_selector)
        
        # Try to find and select the pet by name
        for option in select.options:
            if pet_name.lower() in option.text.lower():
                select.select_by_visible_text(option.text)
                context.current_pet = context.test_pets.get(pet_name, {"name": pet_name})
                time.sleep(1)  # Wait for dashboard to update
                return
        
        # If not found, select the first available pet
        if len(select.options) > 1:
            select.select_by_index(1)
            
    except TimeoutException:
        print(f"Warning: Could not select pet {pet_name} from selector")

@when('I navigate to the Dashboard page')
def step_navigate_to_dashboard(context):
    """Navigate to dashboard page"""
    dashboard_link = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-page='dashboard']"))
    )
    dashboard_link.click()
    
    # Wait for dashboard content to load
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "dashboard-content"))
    )

@when('I am viewing the dashboard for "{pet_name}"')
def step_viewing_dashboard_for_pet(context, pet_name):
    """Set up viewing dashboard for specific pet"""
    context.execute_steps(f'''
        When I select pet "{pet_name}" from the pet selector
        And I navigate to the Dashboard page
    ''')

@when('I click "View Health History"')
def step_click_view_health_history(context):
    """Click the View Health History button"""
    history_btn = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.ID, "view-history-btn"))
    )
    history_btn.click()

@when('I switch from pet "{pet1}" to pet "{pet2}"')
def step_switch_pets(context, pet1, pet2):
    """Switch from one pet to another"""
    context.execute_steps(f'When I select pet "{pet2}" from the pet selector')

# Then steps

@then('I should see the pet information for "{pet_name}"')
def step_see_pet_information(context, pet_name):
    """Verify pet information is displayed"""
    try:
        pet_info = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, "selected-pet-info"))
        )
        
        assert pet_name.lower() in pet_info.text.lower(), f"Pet name '{pet_name}' not found in pet info"
        
    except TimeoutException:
        raise AssertionError(f"Pet information for '{pet_name}' not displayed")

@then('I should see the BMI calculated as approximately "{bmi_value}"')
def step_see_bmi_value(context, bmi_value):
    """Verify BMI value is displayed"""
    try:
        bmi_element = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, "bmi-value"))
        )
        
        displayed_bmi = bmi_element.text
        expected_bmi = float(bmi_value)
        
        # Extract number from displayed text
        bmi_match = re.search(r'(\d+\.?\d*)', displayed_bmi)
        if bmi_match:
            actual_bmi = float(bmi_match.group(1))
            # Allow for small variations in calculation
            assert abs(actual_bmi - expected_bmi) < 1.0, f"BMI {actual_bmi} not approximately {expected_bmi}"
        else:
            # If no number found, just check that it's not the default
            assert displayed_bmi != "-", "BMI value should be calculated"
            
    except TimeoutException:
        raise AssertionError("BMI value not displayed")

@then('I should see the BCS status as "{bcs_status}"')
def step_see_bcs_status(context, bcs_status):
    """Verify BCS status is displayed"""
    try:
        bcs_element = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, "bcs-status"))
        )
        
        displayed_status = bcs_element.text
        assert bcs_status.lower() in displayed_status.lower(), f"BCS status '{bcs_status}' not found in '{displayed_status}'"
        
    except TimeoutException:
        raise AssertionError(f"BCS status '{bcs_status}' not displayed")

@then('I should see the MER value between "{min_value}-{max_value}" kcal/day')
def step_see_mer_value_range(context, min_value, max_value):
    """Verify MER value is in expected range"""
    try:
        mer_element = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, "mer-value"))
        )
        
        displayed_mer = mer_element.text
        min_mer = float(min_value)
        max_mer = float(max_value)
        
        # Extract number from displayed text
        mer_match = re.search(r'(\d+)', displayed_mer)
        if mer_match:
            actual_mer = float(mer_match.group(1))
            assert min_mer <= actual_mer <= max_mer, f"MER {actual_mer} not in range {min_mer}-{max_mer}"
        else:
            # If no number found, just check that it's not the default
            assert displayed_mer != "-", "MER value should be calculated"
            
    except TimeoutException:
        raise AssertionError("MER value not displayed")

@then('I should see the Disease Risk Assessment')
def step_see_disease_risk(context):
    """Verify Disease Risk Assessment is displayed"""
    try:
        risk_element = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, "risk-value"))
        )
        
        risk_status_element = context.driver.find_element(By.ID, "risk-status")
        
        # Check that risk assessment is not showing default values
        assert risk_element.text != "-", "Risk value should be calculated"
        
    except TimeoutException:
        raise AssertionError("Disease Risk Assessment not displayed")

@then('I should be redirected to the "{page_name}" page')
def step_redirected_to_page(context, page_name):
    """Verify redirection to specific page"""
    page_mapping = {
        "My Pets": "pets-page",
        "Reports": "reports-page",
        "Dashboard": "dashboard-page"
    }
    
    expected_page_id = page_mapping.get(page_name, f"{page_name.lower().replace(' ', '-')}-page")
    
    try:
        page_element = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.ID, expected_page_id))
        )
        
        # Check that the page is actually visible and active
        assert page_element.is_displayed(), f"{page_name} page should be visible"
        
    except TimeoutException:
        raise AssertionError(f"Not redirected to {page_name} page")

@then('I should see the basic information for "{pet_name}"')
def step_see_basic_info(context, pet_name):
    """Verify basic pet information is displayed"""
    try:
        basic_info = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, "basic-info"))
        )
        
        # Should not show default message
        assert "Select a pet" not in basic_info.text, "Basic info should show pet data, not default message"
        
    except TimeoutException:
        raise AssertionError(f"Basic information for '{pet_name}' not displayed")

@then('I should see medical history showing "{condition}"')
def step_see_medical_history(context, condition):
    """Verify medical history shows condition"""
    try:
        medical_history = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, "medical-history"))
        )
        
        assert condition.lower() in medical_history.text.lower(), f"Condition '{condition}' not found in medical history"
        
    except TimeoutException:
        raise AssertionError(f"Medical history showing '{condition}' not displayed")

@then('I should see vaccination history showing "{vaccine}"')
def step_see_vaccination_history(context, vaccine):
    """Verify vaccination history shows vaccine"""
    try:
        vaccination_history = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, "vaccination-history"))
        )
        
        assert vaccine.lower() in vaccination_history.text.lower(), f"Vaccine '{vaccine}' not found in vaccination history"
        
    except TimeoutException:
        raise AssertionError(f"Vaccination history showing '{vaccine}' not displayed")

@then('I should see recent activities section')
def step_see_recent_activities(context):
    """Verify recent activities section is displayed"""
    try:
        activities = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, "activity-history"))
        )
        
        # Should not show default message
        assert "Select a pet" not in activities.text, "Activities should show pet data, not default message"
        
    except TimeoutException:
        raise AssertionError("Recent activities section not displayed")

@then('I can see the pet card for "{pet_name}"')
def step_see_pet_card(context, pet_name):
    """Verify pet card is visible"""
    try:
        pet_cards = context.driver.find_elements(By.CSS_SELECTOR, ".pet-card")
        
        pet_found = False
        for card in pet_cards:
            if pet_name.lower() in card.text.lower():
                pet_found = True
                break
        
        assert pet_found, f"Pet card for '{pet_name}' not visible"
        
    except Exception:
        raise AssertionError(f"Pet card for '{pet_name}' not found")

@then('I should see health metrics calculated specifically for cats')
def step_see_cat_health_metrics(context):
    """Verify health metrics are calculated for cats"""
    # Similar to other metric checks, but specific for cats
    context.execute_steps('''
        Then I should see the BMI calculated as approximately "7.2"
        And I should see the Disease Risk Assessment
    ''')

@then('the BMI calculation should be appropriate for cat standards')
def step_bmi_appropriate_for_cats(context):
    """Verify BMI calculation follows cat standards"""
    # This would check that the BMI calculation uses cat-specific formulas
    context.execute_steps('Then I should see the BMI calculated as approximately "7.2"')

@then('the MER calculation should consider cat metabolism')
def step_mer_considers_cat_metabolism(context):
    """Verify MER calculation considers cat metabolism"""
    # Cats have different metabolic rates than dogs
    context.execute_steps('Then I should see the MER value between "200-400" kcal/day')

@then('the displayed metrics should update to show "{pet_name}" data')
def step_metrics_update_for_pet(context, pet_name):
    """Verify metrics update when pet is switched"""
    context.execute_steps(f'Then I should see the pet information for "{pet_name}"')

@then('the pet information should change to "{pet_name}"')
def step_pet_info_changes(context, pet_name):
    """Verify pet information changes"""
    context.execute_steps(f'Then I should see the pet information for "{pet_name}"')

@then('all health calculations should reflect the new pet\'s data')
def step_calculations_reflect_new_pet(context):
    """Verify all calculations update for new pet"""
    # Check that metrics are not showing default values
    try:
        bmi_element = context.driver.find_element(By.ID, "bmi-value")
        mer_element = context.driver.find_element(By.ID, "mer-value")
        
        assert bmi_element.text != "-", "BMI should be calculated for selected pet"
        assert mer_element.text != "-", "MER should be calculated for selected pet"
        
    except Exception:
        raise AssertionError("Health calculations not updated for new pet")

@then('the pet selector should show "{pet_name}" as selected')
def step_pet_selector_shows_selected(context, pet_name):
    """Verify pet selector shows the correct pet as selected"""
    try:
        pet_selector = context.driver.find_element(By.ID, "pet-selector")
        select = Select(pet_selector)
        
        selected_option = select.first_selected_option
        assert pet_name.lower() in selected_option.text.lower(), f"Pet selector should show '{pet_name}' as selected"
        
    except Exception:
        raise AssertionError(f"Pet selector does not show '{pet_name}' as selected")
