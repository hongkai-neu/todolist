# TODO API with Priority Queue

A FastAPI-based TODO application that implements a priority queue for managing tasks. Lower priority numbers indicate higher priority tasks.

## Features

- Create new TODO items with priorities
- List all TODO items
- Get specific TODO item by ID
- Delete TODO items
- View missing priorities in the current TODO list
- Priority-based task organization
- RESTful API with OpenAPI documentation

## Installation and Setup (Recommended to use uv for dependency management)

1. Clone the repository
```bash
git clone https://github.com/yourusername/todo-api.git
cd todo-api
```

2. Install uv if you don't have it yet

3. Install dependencies with uv or manually by creating a virtual environment and installing the dependencies
```bash
uv sync
```

## Running the Application
After activating the virtual environment, run the following commands to start the server:

`fastapi dev` will start the server in development mode with hot-reload enabled, while `fastapi run` will start the server in production mode.

The API will be available at `http://localhost:8000`
Documentation will be available at `http://localhost:8000/docs`

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Root Endpoint
- **GET** `/`
  - Welcome message endpoint
  - Response: `{"message": "Welcome to the TODO API"}`

### Create a TODO item
- **POST** `/todos/`
- Creates a new TODO item with priority
- Request body:
  ```json
  {
    "title": "Complete project documentation",
    "priority": 1,
    "completed": false
  }
  ```
- Response: Created TODO item with generated ID and timestamp

### Get all TODO items
- **GET** `/todos/`
- Returns a list of all TODO items sorted by priority
- Response: Array of TODO items

### Get a specific TODO item
- **GET** `/todos/{todo_id}`
- Returns a specific TODO item by ID
- Response: TODO item or 404 if not found

### Delete a TODO item
- **DELETE** `/todos/{todo_id}`
- Removes a TODO item by ID
- Response: Success message or 404 if not found

### Get missing priorities
- **GET** `/todos/missing-priorities/`
- Returns a list of priority numbers that are not currently in use
- Useful for maintaining a continuous priority sequence
- Response: Array of integers representing missing priorities

## Priority System

- Lower numbers indicate higher priority (1 is highest priority)
- Priorities must be positive integers
- The system automatically tracks missing priorities between the lowest and highest priority numbers in use
- Missing priorities can be retrieved to maintain a continuous sequence

## Running Tests
The project includes unit tests to ensure the functionality of the API and its components. The tests are located in the `tests` directory.

To run the tests:

```bash
# Install test dependencies first
uv sync --extra test

# Run all tests
pytest

# Run specific test file
uv run tests/test_endpoints.py

# Run tests with verbose output
pytest -v
```

## Development Tools

- FastAPI for the web framework
- Pydantic for data validation
- pytest for testing
- uv for dependency management
