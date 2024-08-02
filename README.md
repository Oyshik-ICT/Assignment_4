# User Management API

This project is a Flask-based RESTful API for user management with JWT authentication.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [API Documentation](#api-documentation)
6. [Using the API](#using-the-api)
7. [Database Migrations](#database-migrations)

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

## Using the API

Here's a guide on how to use the main endpoints of the API using Swagger UI:

### 1. Register a new user

1. Navigate to the `/register` POST endpoint in Swagger UI.
2. Click on "Try it out".
3. Fill in the request body with user details:
   ```json
   {
     "username": "newuser",
     "first_name": "John",
     "last_name": "Doe",
     "email": "john@example.com",
     "password": "securepassword",
     "admin_code": "your-admin-code" // Include this only if registering as admin
   }
   ```
4. Click "Execute" to send the request.

### 2. Login

1. Navigate to the `/login` POST endpoint.
2. Click on "Try it out".
3. Fill in the request body:
   ```json
   {
     "username": "newuser",
     "password": "securepassword"
   }
   ```
4. Click "Execute" to get your JWT token.

### 3. Using the JWT token

For authenticated endpoints, you need to include the JWT token in the Authorization header:

1. Click on the "Authorize" button at the top of the Swagger UI.
2. In the "Value" field, enter: `Bearer your-jwt-token`
3. Click "Authorize" and then "Close".

Now all your requests will include this token.

### 4. Get all users (Admin only)

1. Make sure you're logged in as an admin and have set the JWT token.
2. Navigate to the `/users` GET endpoint.
3. Click "Try it out" and then "Execute".

### 5. Get, Update, or Delete a specific user

1. Navigate to the `/users/{user_id}` endpoint (GET, PUT, or DELETE).
2. Click "Try it out".
3. Enter the `user_id` in the path parameter field.
4. For PUT requests, provide the updated user information in the request body.
5. Click "Execute" to send the request.

### 6. Reset Password

To reset a password:

1. Navigate to the `/forgot-password` POST endpoint.
2. Click "Try it out".
3. Provide the email in the request body:
   ```json
   {
     "email": "user@example.com"
   }
   ```
4. Click "Execute". This will send a reset link to the user's email.
5. When the user receives the email, they should click on the reset link.
6. The link will lead to the `/reset-password/<token>` GET endpoint, which verifies the token.
7. If the token is valid, use the `/reset-password/<token>` POST endpoint to set a new password:
   ```json
   {
     "new_password": "newsecurepassword"
   }
   ```

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
