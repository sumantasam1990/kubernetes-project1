from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI(title="Production-Grade TODO API")

# Models
class TodoItem(BaseModel):
    id: Optional[str] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# In-memory storage
todos = {}

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "healthy"}

@app.get("/todos", response_model=List[TodoItem])
async def get_todos():
    return list(todos.values())

@app.get("/todos/{todo_id}", response_model=TodoItem)
async def get_todo(todo_id: str):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos[todo_id]

@app.post("/todos", response_model=TodoItem, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate):
    todo_id = str(uuid.uuid4())
    new_todo = TodoItem(id=todo_id, **todo.dict())
    todos[todo_id] = new_todo
    return new_todo

@app.put("/todos/{todo_id}", response_model=TodoItem)
async def update_todo(todo_id: str, todo_update: TodoUpdate):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    current_todo = todos[todo_id]
    update_data = todo_update.dict(exclude_unset=True)
    
    updated_todo = current_todo.copy(update=update_data)
    todos[todo_id] = updated_todo
    return updated_todo

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: str):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos[todo_id]
    return None
