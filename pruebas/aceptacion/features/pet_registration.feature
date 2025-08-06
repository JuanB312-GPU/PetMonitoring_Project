Feature: Pet Registration
  As a logged-in user
  I want to register my pets
  So that I can monitor their health

  Background:
    Given the PetCare Monitor application is running
    And I am logged in as "juan.perez@email.com"
    And I am on the dashboard page

  Scenario: Successful pet registration with complete data
    Given I am on the dashboard page
    When I click the "Add New Pet" button
    And I enter pet name "Buddy"
    And I select species "Dog"
    And I select breed "Golden Retriever"
    And I enter birthdate "2020-05-15"
    And I enter height "55" cm
    And I enter weight "25.5" kg
    And I select medical condition "Allergy"
    And I select vaccine "Rabies"
    And I click the "Register Pet" button
    Then I should see the success message "Pet registered successfully!"
    And I should see a new pet card for "Buddy" on the dashboard
    And the pet card should display "Golden Retriever"
    And the pet card should display weight "25.5 kg"
    And the pet card should display height "55 cm"
    And the pet card should show medical condition "Allergy"
    And the pet card should show vaccine "Rabies"

  Scenario: Pet registration fails with duplicate name
    Given I have a pet named "Buddy" already registered
    When I click the "Add New Pet" button
    And I enter pet name "Buddy"
    And I select species "Cat"
    And I select breed "Persian"
    And I enter birthdate "2021-03-10"
    And I enter height "30" cm
    And I enter weight "5.5" kg
    And I click the "Register Pet" button
    Then I should see the error message "Pet with this name already exists"
    And the pet should not be registered
    And I should remain on the pet registration modal

  Scenario: Pet registration fails with incomplete data
    Given I am on the dashboard page
    When I click the "Add New Pet" button
    And I enter pet name "Max"
    And I leave species unselected
    And I click the "Register Pet" button
    Then I should see the error message "Please select a species"
    And the pet should not be registered
    And I should remain on the pet registration modal

  Scenario: Species and breed validation
    Given I am on the pet registration modal
    When I select species "Dog"
    Then I should see dog breeds in the breed dropdown
    And I should see breeds like "Golden Retriever", "Labrador", "Bulldog"
    When I select species "Cat"
    Then I should see cat breeds in the breed dropdown
    And I should see breeds like "Persian", "Siamese", "Maine Coon"

  Scenario: Medical conditions and vaccines loading
    Given I am on the pet registration modal
    When I open the medical conditions selector
    Then I should see available medical conditions like "Allergy", "Diabetes", "Arthritis"
    When I open the vaccines selector
    Then I should see available vaccines like "Rabies", "Distemper", "Parvovirus"
