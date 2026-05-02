from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from dotenv import load_dotenv
from app.database import create_db, get_session
from app.models import Todo, User
from app.auth import get_current_user
from app.routers import router as auth_router
import os

load_dotenv()

app = FastAPI(title=os.getenv("APP_NAME", "Todo API"))

# Include auth routes
app.include_router(auth_router)

@app.on_event("startup")
def on_startup():
    create_db()

@app.get("/")
def home():
    return {"message": "Welcome to Todo API"}

@app.get("/health")
def health():
    return {"status": "running"}

# Get all todos (only current user's todos)
@app.get("/todos")
def get_todos(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    todos = session.exec(select(Todo).where(Todo.owner_id == current_user.id)).all()
    return todos

# Get one todo by id
@app.get("/todos/{todo_id}")
def get_todo(
    todo_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    todo = session.get(Todo, todo_id)
    if not todo or todo.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

# Create a todo
@app.post("/todos")
def create_todo(
    todo: Todo,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    todo.owner_id = current_user.id
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

# Update a todo
@app.put("/todos/{todo_id}")
def update_todo(
    todo_id: int,
    updated: Todo,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    todo = session.get(Todo, todo_id)
    if not todo or todo.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.title = updated.title
    todo.description = updated.description
    todo.completed = updated.completed
    session.commit()
    session.refresh(todo)
    return todo

# Delete a todo
@app.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    todo = session.get(Todo, todo_id)
    if not todo or todo.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
    return {"message": "Todo deleted"}