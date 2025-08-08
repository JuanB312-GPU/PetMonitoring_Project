# Stress Testing Guide - PetCare Monitor

## Overview

This folder contains the stress tests for the PetCare Monitor project, designed to evaluate the system's performance and stability under high load using Apache JMeter.

## Test Plan

The main test plan is defined in `StressTests.jmx`, which can be opened and executed with JMeter.

### CSV Files Used

- **user.csv**: Contains user data for registration and login scenarios. The columns are:
  - `name`: User's name
  - `email`: User's email
  - `phone`: User's phone number
  - `password`: User's password
  - `confirmPassword`: Confirmation of the password

  This file is used by the CSV Data Set Config element in JMeter to provide dynamic data for each thread/user during the test.

## JMeter Configuration

### Thread Groups

The test plan includes multiple Thread Groups to simulate different load scenarios:

- **Login Thread Group**
  - Number of Threads (users): 1000
  - Ramp-Up Period (seconds): 5
  - Loop Count: 2
  - Each thread simulates a user attempting to log in using credentials from `user.csv`.

- **Register Thread Group**
  - Number of Threads (users): 2000
  - Ramp-Up Period (seconds): 10
  - Loop Count: 2
  - Each thread simulates a user registration using data from `user.csv`.

- **Feedings Thread Group**
  - Number of Threads (users): 2000
  - Ramp-Up Period (seconds): 10
  - Loop Count: 2
  - Each thread simulates a GET request to the `/feedings` endpoint.

### Ramp-Up Period

The Ramp-Up Period determines how quickly all threads (users) are started. For example, with 1000 threads and a ramp-up of 5 seconds, JMeter will start 200 threads per second. This helps simulate a realistic surge in user activity.

### Loop Count

Each thread will execute its requests the specified number of times (Loop Count). For example, a Loop Count of 2 means each user will perform the scenario twice.

## How to Run the Stress Tests

1. Open `StressTests.jmx` in Apache JMeter.
2. Ensure the `user.csv` file is present at the path specified in the test plan (e.g., `C:/Users/AMD/Documents/Prueba1/user.csv`).
3. Adjust the number of threads, ramp-up period, or loop count as needed for your environment.
4. Start the test and monitor the results using the provided listeners (Summary Report, View Results Tree, etc.).

## Results and Analysis

- The test plan includes listeners to collect and visualize results, such as response times, error rates, and throughput.
- Use the Summary Report and View Results Tree to analyze system behavior under load.

## Notes

- Make sure your backend server and database can handle the configured load, or adjust the thread/ramp-up settings accordingly.
- The CSV file should contain enough unique users to avoid duplicate registration errors during the test.
- You can add or modify Thread Groups and requests in JMeter to simulate additional scenarios as needed.

---

**Maintained by:** PetCare Monitor Team
