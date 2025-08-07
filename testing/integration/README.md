# Integration Testing Guide - PetCare Monitor

## Overview

This document describes the integration testing strategy for the PetCare Monitor project. Integration tests are designed to validate the correct interaction between the API endpoints, the database, and the application logic as a whole.

## Test Structure

Integration tests are located in the `testing/integration/` directory. Each test file targets a specific set of endpoints or features, for example:

- `test_report.py`: Tests for report creation and retrieval endpoints.
- `test_beh.py`: Tests for activities, feedings, and related endpoints.
- `test_auth.py`: Test for user registration and related endpoints.
- `test_login.py`: Test for user login and related endpoints.
- `test_pet.py`: Test for profile pet creation and related endpoints.
- `test_form.py`: Test for medical conditions, vaccines and related endpoints.

## Libraries Used

The following Python libraries are used for integration testing:

- `pytest`: Test runner and assertion library.
- `fastapi.testclient` (from FastAPI): To simulate HTTP requests to the API.
- `requests` and `httpx`: For advanced HTTP requests (if needed).
- `psycopg2-binary`: PostgreSQL database driver (for direct DB setup/teardown if required).

All dependencies are listed in `requirements.txt` in this folder.

## Database State for Testing

Integration tests may require different database states depending on the scenario:

### 1. Empty Database
- Use an empty database when you want to test error handling, such as when a resource is not found (e.g., requesting a report for a non-existent user or pet).
- Recommended for tests that expect 404 Not Found or similar errors.

### 2. Populated Database
- Use a populated database with sample data for tests that require existing users, pets, activities, feedings, or reports.
- Recommended for tests that expect successful creation, retrieval, or update of resources (e.g., creating a report for an existing pet, retrieving activities for a user).
- You can use fixtures or seed scripts to populate the database before running these tests.

**Tip:**
- For reliable results, reset the database to a known state before each test run. This can be done using setup/teardown methods, fixtures, or by running a database reset script.


## How to Run Integration Tests

> **Important:** To execute the integration tests, the test files must be placed in the project root directory alongside the `main.py` file. This ensures correct imports and application context for FastAPI.

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Ensure your PostgreSQL database is running and configured as per your `.env` or `settings.py`.
3. (Optional) Populate the database with test data if required.
4. Run the tests:
   ```bash
   pytest
   ```

## Best Practices

- Use a dedicated test database to avoid affecting production data.
- Clean up or reset the database between test runs to ensure consistent results.
- Use descriptive test names and assertions to make debugging easier.
- Document any required test data or setup steps in this README.

## Example Test Scenarios

- Creating a report for an existing pet (requires populated DB).
- Attempting to create a report for a non-existent pet (requires empty or specific DB state).
- Retrieving all reports for a user (requires populated DB).
- Handling errors when no data is found (requires empty DB).

---

**Maintained by:** PetCare Monitor Team
