# Code Challenge Description

## Overview

This document summarizes the key tasks completed during the Daiichi Sankyo API code challenge, including API development, authentication, database refactoring, testing, and CI/CD pipeline implementation.

## Completed Tasks and Pull Requests

### KAN-1: Create Initial API Endpoints for Customer and Product Interactions

- Added API endpoints to retrieve customer interaction counts per channel and product interaction counts grouped by customer type.
- Integrated the endpoints into the Flask app with error handling.
- **Note**: This task was mistakenly merged into the `main` branch instead of a dedicated branch after the pull request.

### KAN-2: Create an Authorization Method for the API

- Implemented JWT token-based authentication with role-based access control.
- Restricted admin routes and secured the API endpoints.

### KAN-3: Refactor to Use a Different Database Management Library

- Switched from `psycopg2` to SQLAlchemy ORM for database interactions.
- Updated the controllers and database logic to work with SQLAlchemy.

### KAN-4: Refactor Testing

- Refactored the test suite and added unit, integration, and end-to-end tests.
- Integrated `pytest-mock` to mock external dependencies during testing.

### KAN-5: Create a CI/CD Pipeline

- Set up a CI/CD pipeline using GitHub Actions to automate testing, building, and deployment.
- Configured Docker Compose for service management and added `pytest` for automated tests.
- Ensured database migrations and proper cleanup of Docker resources in the pipeline.

## Conclusion

The project successfully implemented API endpoints, authentication, database refactoring, testing improvements, and CI/CD pipeline automation.


- **GitHub Repository**: [Daiichi Sankyo Assignment](https://github.com/sky4689524/daiichi_sankyo_assignment)
- **Jira Board**: [KAN Board](https://daiichisankyohanwool.atlassian.net/jira/software/projects/KAN/boards/1)

If you need access to the Jira board, please let me know, and I will provide access.

## Contact

For further information or assistance, please contact **zerg468@gmail.com**.