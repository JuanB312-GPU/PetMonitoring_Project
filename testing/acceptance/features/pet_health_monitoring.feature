Feature: Pet Health Monitoring
  As a pet owner
  I want to monitor my pet's health metrics
  So that I can ensure they are healthy

  Background:
    Given the PetCare Monitor application is running
    And I am logged in as "juan.perez@email.com"
    And I have a pet named "Buddy" with weight "25.5" kg and height "55" cm

  Scenario: View pet health metrics on dashboard
    Given I am on the dashboard page
    When I select pet "Buddy" from the pet selector
    And I navigate to the Dashboard page
    Then I should see the pet information for "Buddy"
    And I should see the BMI calculated as approximately "8.42"
    And I should see the BCS status as "Normal"
    And I should see the MER value between "1200-1300" kcal/day
    And I should see the Disease Risk Assessment

  Scenario: Access pet medical history
    Given I have a pet "Buddy" with medical condition "Allergy"
    And I am viewing the dashboard for "Buddy"
    When I click "View Health History"
    Then I should be redirected to the "My Pets" page
    And I should see the basic information for "Buddy"
    And I should see medical history showing "Allergy"
    And I should see vaccination history showing "Rabies"
    And I should see recent activities section

  Scenario: Navigate to pet details by clicking pet card
    Given I am on the dashboard page
    And I can see the pet card for "Buddy"
    When I click on the pet card for "Buddy"
    Then I should be redirected to the dashboard
    And the pet selector should show "Buddy" as selected
    And I should see "Buddy"'s health metrics displayed

  Scenario: View health metrics for different pet types
    Given I have a cat named "Whiskers" with weight "4.5" kg and height "25" cm
    When I select pet "Whiskers" from the pet selector
    Then I should see health metrics calculated specifically for cats
    And the BMI calculation should be appropriate for cat standards
    And the MER calculation should consider cat metabolism

  Scenario: Health metrics update when pet is selected
    Given I am on the dashboard page
    And I have multiple pets registered
    When I switch from pet "Buddy" to pet "Whiskers"
    Then the displayed metrics should update to show "Whiskers" data
    And the pet information should change to "Whiskers"
    And all health calculations should reflect the new pet's data
