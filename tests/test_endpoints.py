'''
Test the endpoints of the API
'''

import pytest
from fastapi.testclient import TestClient
from app.main import app, todo_queue
from app.models.todo_item import TodoItem
from app.core.priority_queue import PriorityQueue

@pytest.fixture
def client():
    # Clear the todo queue before each test
    todo_queue.clear_queue()
    return TestClient(app)

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the TODO API"}

def test_create_todo(client):
    todo_data = {
        "title": "Test Todo",
        "priority": 1
    }
    response = client.post("/todos/", json=todo_data)
    assert response.status_code == 200
    response_data = response.json()
    # Check the fields we sent
    assert response_data["title"] == todo_data["title"]
    assert response_data["priority"] == todo_data["priority"]
    # Verify the additional fields exist and have correct types
    assert "id" in response_data
    assert isinstance(response_data["id"], int)
    assert "created_at" in response_data
    assert "completed" in response_data
    assert not response_data["completed"]

    # Clean up
    client.delete(f"/todos/1")

def test_get_all_todos(client):
    # Create two todos
    todo_data1 = {
        "title": "Test Todo 1",
        "priority": 1
    }
    client.post("/todos/", json=todo_data1)
    todo_data2 = {
        "title": "Test Todo 2",
        "priority": 2
    }
    client.post("/todos/", json=todo_data2)

    response = client.get("/todos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2

    # Clean up
    client.delete(f"/todos/1")
    client.delete(f"/todos/2")

def test_get_todo(client):
    # First create a todo
    todo_data = {
        "title": "Test Todo 1",
        "priority": 1
    }
    # Create the todo and get the response
    create_response = client.post("/todos/", json=todo_data)
    created_todo = create_response.json()
    
    # Then get it using the ID that was actually assigned
    response = client.get(f"/todos/{created_todo['id']}")
    assert response.status_code == 200
    response_data = response.json()
    
    # Check the fields we sent
    assert response_data["title"] == todo_data["title"]
    assert response_data["priority"] == todo_data["priority"]
    # Verify the additional fields exist but don't check their exact values
    assert "created_at" in response_data
    assert "completed" in response_data

    # Clean up
    client.delete(f"/todos/1")

def test_get_nonexistent_todo(client):
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "TODO item not found"

def test_delete_todo(client):
    # First create a todo
    todo_data = {
        "title": "Test Todo 3",
        "priority": 3
    }
    client.post("/todos/", json=todo_data)
    
    # Delete the todo
    response = client.delete(f"/todos/1")
    assert response.status_code == 200
    assert response.json() == {"message": "TODO item deleted successfully"}
    
    # Verify it's deleted
    response = client.get(f"/todos/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "TODO item not found"

def test_delete_nonexistent_todo(client):
    response = client.delete("/todos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "TODO item not found"

def test_get_missing_priorities(client):
    todos = [
        {"title": "High Priority", "priority": 1},
        {"title": "Medium Priority", "priority": 3},
        {"title": "Low Priority", "priority": 5}
    ]
    
    created_todos = []
    print("\n=== Creating TODOs ===")
    for todo in todos:
        response = client.post("/todos/", json=todo)
        created_todo = response.json()
        created_todos.append(created_todo)
        print(f"Created TODO: {created_todo}")
    
    print("\n=== Getting Missing Priorities ===")
    # Get missing priorities
    response = client.get("/todos/missing-priorities/")
    print(f"Response Status Code: {response.status_code}")
    
    missing_priorities = response.json()
    print(f"Missing Priorities Response: {missing_priorities}")
    
    assert response.status_code == 200
    
    # Verify the response is a list
    assert isinstance(missing_priorities, list)
    
    # Since we created todos with priorities 1, 3, and 5,
    # we should expect priorities 2 and 4 to be missing
    assert 2 in missing_priorities
    assert 4 in missing_priorities
    assert len(missing_priorities) == 2
    
    print("\n=== Cleaning Up ===")
    # Clean up
    client.delete(f"/todos/1")
    client.delete(f"/todos/2")
    client.delete(f"/todos/3")