from typing import Optional
from sqlmodel import SQLModel

class UserCreate(SQLModel):
    username: str
    password: str
    role: str

class UserRead(SQLModel):
    id: int
    username: str
    role: str

class ProjectCreate(SQLModel):
    name: str
    description: str

class ProjectRead(SQLModel):
    id: int
    name: str
    description: str
    user_id: Optional[int]

