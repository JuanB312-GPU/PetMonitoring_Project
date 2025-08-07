Feature: System Navigation
  As a user
  I want to navigate between different pages
  So that I can access all features of the application

  Background:
    Given the PetCare Monitor application is running
    And I am logged in as "juan.perez@email.com"

  Scenario: Navigate between main pages
    Given I am on the dashboard page
    When I click "My Pets" in the navigation
    Then I should be on the "My Pets" page
    And I should see all my registered pets
    When I click "Reports" in the navigation
    Then I should be on the "Reports" page
    And I should see generated reports or empty state
    When I click "Dashboard" in the navigation
    Then I should be back on the dashboard page
    And I should see the health metrics section

  Scenario: Navigation shows active page
    Given I am on the dashboard page
    When I navigate to different pages
    Then the active page should be highlighted in the navigation
    And the correct page content should be displayed

  Scenario: Pet selector works across pages
    Given I have multiple pets registered
    And I am on the dashboard page
    When I select a pet from the pet selector
    And I navigate to "My Pets" page
    Then the same pet should remain selected
    And the pet's information should be displayed

  Scenario: Responsive navigation behavior
    Given I am on any page of the application
    When I resize the browser window
    Then the navigation should remain accessible
    And all navigation links should be functional

  Scenario: Home page navigation
    Given I am on any page
    When I click the "PetCare Monitor" brand logo
    Then I should navigate to the main dashboard
    And I should see the main content area
