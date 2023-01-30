from sqlalchemy import Boolean, Column, Integer, String
from pydantic import BaseModel, Field

from typing import Optional
from database.db import Base


class Todos(Base):
    """Model-table for Todos"""
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)


class PostTodo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6)
    complete: bool
