from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Relationship

from pydantic import BaseModel, Field, EmailStr

from typing import Optional
from database.db import Base

# ----------------------------------------------------------------


class Todos(Base):
    """Model-table for Todos"""
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = Relationship('Users', back_populates="todos")


class PostTodo(BaseModel):
    """Model for POST todo"""
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6)
    complete: bool
    owner_id: int

# --------------------------------------------------------------


class Users(Base):
    """
    Model/Table for Users.
    One to Many relationship with Todos.

    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    todos = Relationship('Todos', back_populates='owner')


class CreateUser(BaseModel):
    """
    Pydantic Model for creating a user.
    """
    username: str
    password: str
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
