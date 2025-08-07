Feature: User Registration
  As a new user
  I want to register an account
  So that I can manage my pets' health

  Background:
    Given the PetCare Monitor application is running
    And I am on the home page

  Scenario: Successful user registration with valid data
    Given I am on the registration page
    When I enter name "Juan Pérez"
    And I enter email "juan.perez@email.com"
    And I enter phone "3001234567"
    And I enter password "Password123!"
    And I confirm password "Password123!"
    And I click the register button
    Then I should be redirected to the dashboard
    And I should see the welcome message "Welcome new pet lover, Juan Pérez!"
    And I should see my user account created successfully

  Scenario: Registration fails with duplicate email
    Given a user exists with email "juan.perez@email.com"
    And I am on the registration page
    When I enter name "Another User"
    And I enter email "juan.perez@email.com"
    And I enter phone "3009876543"
    And I enter password "Password123!"
    And I confirm password "Password123!"
    And I click the register button
    Then I should see the error message "Email already registered"
    And I should remain on the registration page

  Scenario: Registration fails with mismatched passwords
    Given I am on the registration page
    When I enter name "Juan Pérez"
    And I enter email "juan.perez@email.com"
    And I enter phone "3001234567"
    And I enter password "Password123!"
    And I confirm password "Password456!"
    And I click the register button
    Then I should see the error message "Passwords do not match"
    And I should remain on the registration page

  Scenario: Registration fails with invalid email format
    Given I am on the registration page
    When I enter name "Juan Pérez"
    And I enter email "invalid-email"
    And I enter phone "3001234567"
    And I enter password "Password123!"
    And I confirm password "Password123!"
    And I click the register button
    Then I should see validation errors for email format
    And I should remain on the registration page
