from sqlmodel import SQLModel, Field
from typing import Optional

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str = ""
    completed: bool = False
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    hashed_password: str