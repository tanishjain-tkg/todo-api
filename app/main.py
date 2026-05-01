from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from dotenv import load_dotenv
from app.database import create_db, get_session
from app.models import Todo
import os

load_dotenv()

app = FastAPI(title=os.getenv("APP_NAME", "ToDo API"))

@app.on_event("startup")
def on_startup():
    create_db()

@app.get("/")
def home():
    return {"message": "Welcome to Todo API"}

@app.get("/health")
def health():
    return {"status": "running"}

#Get all todos
@app.get("/todos")
def get_todos(session: Session = Depends(get_session)):
    todos = session.exec(select(Todo)).all()
    return todos

#Get one todo by id
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int, session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

#Create a todo
@app.post("/todos")
def create_todo(todo: Todo, session: Session = Depends(get_session)):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

#Update a todo
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated: Todo, session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.title = updated.title
    todo.description = updated.description
    todo.completed = updated.completed
    session.commit()
    session.refresh(todo)
    return todo

#Delete a todo
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
    return {"message": "Todo deleted"}