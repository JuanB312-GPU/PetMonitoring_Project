Feature: Pet Activity Management
  As a pet owner
  I want to record my pet's activities and feeding
  So that I can track their daily routine

  Background:
    Given the PetCare Monitor application is running
    And I am logged in as "juan.perez@email.com"
    And I have a pet named "Buddy" registered

  Scenario: Successfully add physical activity
    Given I am on the dashboard page
    And I can see the pet card for "Buddy"
    When I click "Add Activity" on the pet card
    Then I should see the activity modal open
    When I select activity "Walking"
    And I select frequency "Daily"
    And I click submit in the activity modal
    Then I should see the success message "Activity added successfully!"
    And the activity modal should close
    And the activity should be recorded for "Buddy"

  Scenario: Successfully add feeding information
    Given I am on the dashboard page
    And I can see the pet card for "Buddy"
    When I click "Add Food" on the pet card
    Then I should see the food modal open
    When I select food "Dry Food"
    And I select frequency "Twice daily"
    And I click submit in the food modal
    Then I should see the success message "Food added successfully!"
    And the food modal should close
    And the feeding should be recorded for "Buddy"

  Scenario: View recorded activities in pet history
    Given I have recorded activities for "Buddy"
    And I am on the "My Pets" page
    When I select pet "Buddy"
    Then I should see the "Recent Activities" section
    And I should see the previously recorded activities
    And I should see activity details like name and frequency

  Scenario: Activity modal closes on cancel
    Given I am on the dashboard page
    When I click "Add Activity" on the pet card for "Buddy"
    And the activity modal is open
    When I click the close button or click outside the modal
    Then the activity modal should close
    And no activity should be recorded

  Scenario: Food modal closes on cancel
    Given I am on the dashboard page
    When I click "Add Food" on the pet card for "Buddy"
    And the food modal is open
    When I click the close button or click outside the modal
    Then the food modal should close
    And no feeding should be recorded

  Scenario: Load available activities and foods
    When I open the activity modal
    Then I should see available activities like "Walking", "Running", "Playing"
    When I open the food modal
    Then I should see available foods like "Dry Food", "Wet Food", "Treats"
