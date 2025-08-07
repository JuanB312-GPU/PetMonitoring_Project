Feature: Health Report Generation
  As a pet owner
  I want to generate health reports for my pets
  So that I can share them with veterinarians and track progress

  Background:
    Given the PetCare Monitor application is running
    And I am logged in as "juan.perez@email.com"
    And I have a pet named "Buddy" with complete health data

  Scenario: Successfully generate health report
    Given I am on the "My Pets" page
    And I have selected pet "Buddy"
    When I click "Generate Health Report"
    Then I should see a health report being generated
    And the report should include current health metrics
    And the report should include BMI, BCS, and MER values
    And the report should include medical history
    And the report should include vaccination records
    And the report should include recent activities

  Scenario: View generated reports
    Given I have generated health reports for my pets
    When I navigate to the "Reports" page
    Then I should see a list of all generated reports
    And each report should show the pet name
    And each report should show the generation date
    And each report should be accessible for viewing

  Scenario: Generate report with insufficient data
    Given I have a newly registered pet with minimal data
    When I try to generate a health report
    Then I should still be able to generate a basic report
    And the report should indicate missing data areas
    And the report should show available information

  Scenario: Reports page shows empty state
    Given I have not generated any reports yet
    When I navigate to the "Reports" page
    Then I should see an empty state message
    And I should see "No Reports Generated"
    And I should see instructions to generate reports from My Pets section

  Scenario: Report contains accurate health calculations
    Given I have a pet with specific measurements
    When I generate a health report
    Then the BMI calculation should be mathematically correct
    And the MER calculation should consider the pet's age and weight
    And the BCS assessment should be appropriate for the species
    And all metrics should match the dashboard values
