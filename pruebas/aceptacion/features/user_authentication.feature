Feature: User Authentication
  As a registered user
  I want to log into my account
  So that I can access my pets' information

  Background:
    Given the PetCare Monitor application is running
    And I am on the home page

  Scenario: Successful login with valid credentials
    Given a user exists with email "juan.perez@email.com" and password "Password123!"
    And I am on the login page
    When I enter email "juan.perez@email.com"
    And I enter password "Password123!"
    And I click the login button
    Then I should be successfully authenticated
    And I should be redirected to the dashboard
    And I should see the welcome message "Welcome back, Juan Pérez!"
    And I should see the logout button in the navigation

  Scenario: Login fails with invalid credentials
    Given I am on the login page
    When I enter email "invalid@email.com"
    And I enter password "wrongpassword"
    And I click the login button
    Then I should see the error message "Invalid credentials"
    And I should remain on the login page
    And I should not be authenticated

  Scenario: Login fails with empty credentials
    Given I am on the login page
    When I click the login button without entering credentials
    Then I should see validation errors for required fields
    And I should remain on the login page

  Scenario: Successful logout
    Given I am logged in as "juan.perez@email.com"
    And I am on the dashboard page
    When I click the logout button
    Then I should be logged out successfully
    And I should be redirected to the home page
    And I should see the login and register buttons
    And I should not see the logout button
