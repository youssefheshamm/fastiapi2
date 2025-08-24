from pydantic import BaseModel, validator
from sqlalchemy import Column, Integer, String
from app.database import Base
from typing import Optional


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)


class TaskCreate(BaseModel):
    title: str
    description: str


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    @validator("title")
    def title_not_empty(cls, value):
        if value is not None and not value.strip():
            raise ValueError("Title cannot be empty")
        return value
