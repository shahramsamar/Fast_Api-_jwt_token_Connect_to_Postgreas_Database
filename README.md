# FastAPI JWT Token Connect to PostgreSQL Database

A FastAPI project that demonstrates how to authenticate users using JWT (JSON Web Tokens) and connect to a PostgreSQL database to manage user data. The application allows users to register, log in, and interact with a PostgreSQL database using authenticated JWT tokens.

## Features

- **User Authentication**: Users can register and log in to receive a JWT token.
- **PostgreSQL Database**: Connects to a PostgreSQL database to store user data.
- **JWT Authentication**: Secures API routes using JWT tokens for authenticated requests.
- **CRUD Operations**: Provides basic CRUD (Create, Read, Update, Delete) operations for managing user data.

## Requirements

- **Python 3.x**
- **FastAPI**: Web framework for building APIs.
- **Uvicorn**: ASGI server for serving the FastAPI app.
- **SQLAlchemy**: ORM for interacting with PostgreSQL.
- **Pydantic**: Data validation library.
- **JWT (JSON Web Tokens)**: Used for user authentication.
- **PostgreSQL**: Database used to store user data.

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/shahramsamar/Fast_Api-_jwt_token_Connect_to_Postgreas_Database.git
    cd Fast_Api-_jwt_token_Connect_to_Postgreas_Database
    ```

2. **Install Dependencies:**

    If you're using `pip`, run:

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up PostgreSQL Database:**

    Make sure you have a PostgreSQL instance running and create a database for this project.

    Example of creating a database:
    ```bash
    createdb fastapi_jwt_db
    ```

4. **Set up Database Connection**:

    Modify the `database.py` or environment variables to include your PostgreSQL connection string:

    ```python
    DATABASE_URL = "postgresql://username:password@localhost/fastapi_jwt_db"
    ```

5. **Run the Application**:

    To run the FastAPI app using Uvicorn:

    ```bash
    uvicorn main:app --reload
    ```

    This will start the server at `http://127.0.0.1:8000`.

### How to Use

1. **Register a User**:
    - Send a `POST` request to `/register/` with the username, email, and password to create a new user.

    Example request body:
    ```json
    {
        "username": "user1",
        "email": "user1@example.com",
        "password": "securepassword"
    }
    ```

2. **Login and Get Token**:
    - Send a `POST` request to `/login/` with the username and password to receive a JWT token.

    Example request body:
    ```json
    {
        "username": "user1",
        "password": "securepassword"
    }
    ```

    Response will include the JWT token to be used in subsequent requests.

3. **Access Protected Routes**:
    - Send requests to protected routes (like `/users/`) with the JWT token in the `Authorization` header as a Bearer token.

    Example header:
    ```
    Authorization: Bearer your_jwt_token
    ```

4. **Create User Data**:
    - Send a `POST` request to `/users/` to create new user data.

    Example request body:
    ```json
    {
        "name": "John Doe",
        "age": 30,
        "email": "johndoe@example.com"
    }
    ```

5. **Get User Data**:
    - Send a `GET` request to `/users/{user_id}/` to fetch data for a specific user.

6. **Update User Data**:
    - Send a `PUT` request to `/users/{user_id}/` to update user data.

7. **Delete User Data**:
    - Send a `DELETE` request to `/users/{user_id}/` to remove user data.

### Project Structure

- `main.py`: Contains the FastAPI application, route handlers, and database setup.
- `models.py`: Defines SQLAlchemy ORM models for User.
- `schemas.py`: Contains Pydantic models for data validation and response formatting.
- `auth.py`: Handles authentication logic using JWT.
- `database.py`: Configures the connection to the PostgreSQL database.
- `requirements.txt`: Lists necessary libraries and dependencies for the project.

### API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

### Example Requests

1. **Register User** (POST):
    ```bash
    curl -X 'POST' \
    'http://127.0.0.1:8000/register/' \
    -H 'Content-Type: application/json' \
    -d '{
        "username": "user1",
        "email": "user1@example.com",
        "password": "securepassword"
    }'
    ```

2. **Login and Get Token** (POST):
    ```bash
    curl -X 'POST' \
    'http://127.0.0.1:8000/login/' \
    -H 'Content-Type: application/json' \
    -d '{
        "username": "user1",
        "password": "securepassword"
    }'
    ```

3. **Create User Data** (POST):
    ```bash
    curl -X 'POST' \
    'http://127.0.0.1:8000/users/' \
    -H 'Authorization: Bearer your_jwt_token' \
    -H 'Content-Type: application/json' \
    -d '{
        "name": "John Doe",
        "age": 30,
        "email": "johndoe@example.com"
    }'
    ```

4. **Get User Data** (GET):
    ```bash
    curl -X 'GET' \
    'http://127.0.0.1:8000/users/1/' \
    -H 'Authorization: Bearer your_jwt_token'
    ```

### Contributing

Feel free to fork the project and submit pull requests for new features, improvements, or bug fixes.

## License

This project is open-source and available for educational purposes.

