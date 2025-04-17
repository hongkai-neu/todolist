'''
FastAPI app for a TODO list

This is the entry point for the API

Endpoints:
- GET /todos/
- POST /todos/
- GET /todos/{todo_id}
- DELETE /todos/{todo_id}
- GET /todos/missing-priorities/
'''

from fastapi import FastAPI, HTTPException
from typing import List
from app.models.todo_item import TodoItem
from app.core.priority_queue import PriorityQueue
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="TODO LIST API",
    description="A simple TODO application with priority queue implementation",
    version="1.0.0"
)

# CORS middleware: All origins are allowed for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the priority queue data structure to store the todos items temporarily
todo_queue = PriorityQueue()

@app.get("/")
async def root():
    return {"message": "Welcome to the TODO API"}

@app.post("/todos/", response_model=TodoItem)
async def create_todo(todo: TodoItem):
    return todo_queue.add_item(todo)

# Get all todo items
@app.get("/todos/", response_model=List[TodoItem])
async def get_all_todos():
    return todo_queue.get_all_items()

# Get a todo item by id
@app.get("/todos/{todo_id}", response_model=TodoItem)
async def get_todo(todo_id: int):
    todo = todo_queue.get_item(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="TODO item not found")
    return todo

# Delete a todo item by id
@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    if not todo_queue.delete_item(todo_id):
        raise HTTPException(status_code=404, detail="TODO item not found")
    return {"message": "TODO item deleted successfully"}

# Get all missing priorities
@app.get("/todos/missing-priorities/", response_model=List[int])
async def get_missing_priorities():
    return todo_queue.get_missing_priorities()