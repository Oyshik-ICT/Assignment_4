# User Management API

This project is a Flask-based RESTful API for user management with JWT authentication.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [API Documentation](#api-documentation)
6. [Database Migrations](#database-migrations)

## Prerequisites

- Python 3.7+
- PostgreSQL

## Installation

1. Clone the repository:

   ```
   git clone <repository-url>
   cd <project-directory>
   ```

2. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the project root directory with the following content:

   ```
   SECRET_KEY=your-secret-key
   ADMIN_REGISTRATION_CODE=your-admin-code
   DATABASE_URL=postgresql://username:password@localhost:5433/dbname
   JWT_SECRET_KEY=your-jwt-secret-key
   EMAIL_USER=your-email@example.com
   EMAIL_PASS=your-email-password
   ```

   Replace the placeholder values with your actual configuration.

2. Ensure your PostgreSQL server is running and the database specified in `DATABASE_URL` exists.

## Running the Application

1. Initialize the database (if it's your first time running the app):

   ```
   flask db upgrade
   ```

2. Run the application:

   ```
   python run.py
   ```

   The application will start running on `http://localhost:5000`.

## API Documentation

The API documentation is available via Swagger UI. Once the application is running, you can access it at:

```
http://localhost:5000/swagger
```

This interactive documentation provides details on all available endpoints, request/response formats, and allows you to test the API directly from the browser.

### Key Endpoints:

- `POST /register`: Register a new user
- `POST /login`: Authenticate a user and receive a JWT token
- `GET /users`: Get all users (admin only)
- `GET /users/<user_id>`: Get a specific user
- `PUT /users/<user_id>`: Update a user
- `DELETE /users/<user_id>`: Delete a user (admin only)

For detailed information on request/response formats and authentication requirements, please refer to the Swagger documentation.

## Database Migrations

This project uses Flask-Migrate for database migrations. If you make changes to the database models, follow these steps:

1. Generate a new migration:

   ```
   flask db migrate -m "Description of the changes"
   ```

2. Apply the migration:
   ```
   flask db upgrade
   ```
