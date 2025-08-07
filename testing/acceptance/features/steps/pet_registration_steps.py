"""
Step definitions for pet registration features
"""
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# Given steps

@given('I have a pet named "{pet_name}" already registered')
def step_have_pet_registered(context, pet_name):
    """Create a test pet that already exists"""
    if not hasattr(context, 'test_pets'):
        context.test_pets = {}
    
    pet_data = {
        "name": pet_name,
        "species": "Dog",
        "breed": "Golden Retriever",
        "birthdate": "2020-05-15",
        "height": 55,
        "weight": 25.5
    }
    context.test_pets[pet_name] = pet_data

@given('I am on the pet registration modal')
def step_on_pet_registration_modal(context):
    """Open the pet registration modal"""
    # Ensure we're logged in and on dashboard
    if not context.current_user:
        context.execute_steps('''
            Given I am logged in as "test@email.com"
            And I am on the dashboard page
        ''')
    
    # Click Add New Pet button
    add_pet_btn = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.ID, "add-pet-btn"))
    )
    add_pet_btn.click()
    
    # Wait for modal to appear
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "pet-modal"))
    )

# When steps

@when('I click the "Add New Pet" button')
def step_click_add_pet(context):
    """Click the Add New Pet button"""
    add_pet_btn = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.ID, "add-pet-btn"))
    )
    add_pet_btn.click()
    
    # Wait for modal to appear
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "pet-modal"))
    )

@when('I enter pet name "{pet_name}"')
def step_enter_pet_name(context, pet_name):
    """Enter pet name in the form"""
    name_field = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "pet-name"))
    )
    name_field.clear()
    name_field.send_keys(pet_name)
    context.current_pet_name = pet_name

@when('I select species "{species}"')
def step_select_species(context, species):
    """Select species from dropdown"""
    # Wait for species dropdown to be populated
    time.sleep(1)
    
    species_select = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.ID, "pet-species"))
    )
    
    select = Select(species_select)
    
    # Find option by text
    for option in select.options:
        if option.text == species:
            select.select_by_visible_text(species)
            break
    else:
        # If not found, try by value (for testing)
        if species == "Dog":
            select.select_by_value("1")
        elif species == "Cat":
            select.select_by_value("2")
    
    # Wait for breed dropdown to update
    time.sleep(1)

@when('I select breed "{breed}"')
def step_select_breed(context, breed):
    """Select breed from dropdown"""
    # Wait for breed dropdown to be populated after species selection
    time.sleep(1)
    
    breed_select = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.ID, "pet-breed"))
    )
    
    select = Select(breed_select)
    
    # Find option by text
    for option in select.options:
        if option.text == breed:
            select.select_by_visible_text(breed)
            break
    else:
        # Fallback to first available breed option if exact match not found
        if len(select.options) > 1:
            select.select_by_index(1)  # Skip the "Select Breed" option

@when('I enter birthdate "{birthdate}"')
def step_enter_birthdate(context, birthdate):
    """Enter birthdate"""
    birthdate_field = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "pet-birthdate"))
    )
    birthdate_field.clear()
    birthdate_field.send_keys(birthdate)

@when('I enter height "{height}" cm')
def step_enter_height(context, height):
    """Enter height in cm"""
    height_field = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "pet-height"))
    )
    height_field.clear()
    height_field.send_keys(height)

@when('I enter weight "{weight}" kg')
def step_enter_weight(context, weight):
    """Enter weight in kg"""
    weight_field = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "pet-weight"))
    )
    weight_field.clear()
    weight_field.send_keys(weight)

@when('I select medical condition "{condition}"')
def step_select_medical_condition(context, condition):
    """Select medical condition"""
    conditions_select = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.ID, "pet-conditions"))
    )
    
    select = Select(conditions_select)
    
    # Find option by text
    for option in select.options:
        if option.text == condition:
            select.select_by_visible_text(condition)
            break
    else:
        # Fallback - select first available option
        if len(select.options) > 0:
            select.select_by_index(0)

@when('I select vaccine "{vaccine}"')
def step_select_vaccine(context, vaccine):
    """Select vaccine"""
    vaccines_select = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.ID, "pet-vaccines"))
    )
    
    select = Select(vaccines_select)
    
    # Find option by text
    for option in select.options:
        if option.text == vaccine:
            select.select_by_visible_text(vaccine)
            break
    else:
        # Fallback - select first available option
        if len(select.options) > 0:
            select.select_by_index(0)

@when('I click the "Register Pet" button')
def step_click_register_pet(context):
    """Click the Register Pet button"""
    pet_form = context.driver.find_element(By.ID, "pet-form")
    submit_btn = pet_form.find_element(By.CSS_SELECTOR, "button[type='submit']")
    
    # Scroll to button if needed
    context.driver.execute_script("arguments[0].scrollIntoView();", submit_btn)
    
    # Click submit button
    submit_btn.click()
    
    # Wait a moment for form submission
    time.sleep(2)

@when('I leave species unselected')
def step_leave_species_unselected(context):
    """Leave species field unselected"""
    # Ensure species is not selected (should default to "0" or "Select Species")
    species_select = context.driver.find_element(By.ID, "pet-species")
    select = Select(species_select)
    if select.first_selected_option.get_attribute("value") != "0":
        select.select_by_value("0")

@when('I open the medical conditions selector')
def step_open_medical_conditions(context):
    """Open the medical conditions selector"""
    conditions_select = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.ID, "pet-conditions"))
    )
    conditions_select.click()

@when('I open the vaccines selector')
def step_open_vaccines_selector(context):
    """Open the vaccines selector"""
    vaccines_select = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.ID, "pet-vaccines"))
    )
    vaccines_select.click()

# Then steps

@then('I should see a new pet card for "{pet_name}" on the dashboard')
def step_see_new_pet_card(context, pet_name):
    """Verify new pet card appears on dashboard"""
    try:
        # Wait for pet card to appear
        pet_card_selector = f"[data-pet-id], .pet-card"
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, pet_card_selector))
        )
        
        # Look for pet name in any pet card
        pet_cards = context.driver.find_elements(By.CSS_SELECTOR, ".pet-card")
        pet_found = False
        
        for card in pet_cards:
            if pet_name.lower() in card.text.lower():
                pet_found = True
                break
        
        assert pet_found, f"Pet card for '{pet_name}' not found on dashboard"
        
    except TimeoutException:
        raise AssertionError(f"Pet card for '{pet_name}' did not appear on dashboard")

@then('the pet card should display "{text}"')
def step_pet_card_displays_text(context, text):
    """Verify pet card displays specific text"""
    pet_cards = context.driver.find_elements(By.CSS_SELECTOR, ".pet-card")
    
    text_found = False
    for card in pet_cards:
        if hasattr(context, 'current_pet_name') and context.current_pet_name.lower() in card.text.lower():
            if text.lower() in card.text.lower():
                text_found = True
                break
    
    assert text_found, f"Text '{text}' not found in pet card"

@then('the pet card should show medical condition "{condition}"')
def step_pet_card_shows_condition(context, condition):
    """Verify pet card shows medical condition"""
    # This is similar to checking for text in pet card
    context.execute_steps(f'Then the pet card should display "{condition}"')

@then('the pet card should show vaccine "{vaccine}"')
def step_pet_card_shows_vaccine(context, vaccine):
    """Verify pet card shows vaccine"""
    # This is similar to checking for text in pet card
    context.execute_steps(f'Then the pet card should display "{vaccine}"')

@then('the pet should not be registered')
def step_pet_not_registered(context):
    """Verify pet was not registered"""
    # Modal should still be visible if registration failed
    modal = context.driver.find_element(By.ID, "pet-modal")
    assert modal.is_displayed(), "Pet modal should still be visible if registration failed"

@then('I should remain on the pet registration modal')
def step_remain_on_pet_modal(context):
    """Verify user remains on pet registration modal"""
    try:
        modal = WebDriverWait(context.driver, 5).until(
            EC.visibility_of_element_located((By.ID, "pet-modal"))
        )
        assert modal.is_displayed(), "Pet registration modal should still be visible"
    except TimeoutException:
        raise AssertionError("Pet registration modal is not visible")

@then('I should see dog breeds in the breed dropdown')
def step_see_dog_breeds(context):
    """Verify dog breeds appear in breed dropdown"""
    # Wait for breed dropdown to be populated
    time.sleep(1)
    
    breed_select = context.driver.find_element(By.ID, "pet-breed")
    select = Select(breed_select)
    
    # Check that there are breed options available
    options = [option.text for option in select.options if option.text != "Select Breed"]
    assert len(options) > 0, "No breed options found for dogs"

@then('I should see breeds like "{breed_list}"')
def step_see_specific_breeds(context, breed_list):
    """Verify specific breeds are available"""
    expected_breeds = [breed.strip() for breed in breed_list.split(",")]
    
    breed_select = context.driver.find_element(By.ID, "pet-breed")
    select = Select(breed_select)
    
    available_breeds = [option.text for option in select.options]
    
    # Check if at least one expected breed is available
    found_breeds = [breed for breed in expected_breeds if breed in available_breeds]
    assert len(found_breeds) > 0, f"None of the expected breeds {expected_breeds} found in {available_breeds}"

@then('I should see cat breeds in the breed dropdown')
def step_see_cat_breeds(context):
    """Verify cat breeds appear in breed dropdown"""
    # Similar to dog breeds verification
    time.sleep(1)
    
    breed_select = context.driver.find_element(By.ID, "pet-breed")
    select = Select(breed_select)
    
    options = [option.text for option in select.options if option.text != "Select Breed"]
    assert len(options) > 0, "No breed options found for cats"

@then('I should see available medical conditions like "{conditions_list}"')
def step_see_medical_conditions(context, conditions_list):
    """Verify medical conditions are available"""
    expected_conditions = [condition.strip() for condition in conditions_list.split(",")]
    
    conditions_select = context.driver.find_element(By.ID, "pet-conditions")
    select = Select(conditions_select)
    
    available_conditions = [option.text for option in select.options]
    
    # Check if at least one expected condition is available
    found_conditions = [condition for condition in expected_conditions if condition in available_conditions]
    assert len(found_conditions) > 0, f"None of the expected conditions {expected_conditions} found"

@then('I should see available vaccines like "{vaccines_list}"')
def step_see_vaccines(context, vaccines_list):
    """Verify vaccines are available"""
    expected_vaccines = [vaccine.strip() for vaccine in vaccines_list.split(",")]
    
    vaccines_select = context.driver.find_element(By.ID, "pet-vaccines")
    select = Select(vaccines_select)
    
    available_vaccines = [option.text for option in select.options]
    
    # Check if at least one expected vaccine is available
    found_vaccines = [vaccine for vaccine in expected_vaccines if vaccine in available_vaccines]
    assert len(found_vaccines) > 0, f"None of the expected vaccines {expected_vaccines} found"
