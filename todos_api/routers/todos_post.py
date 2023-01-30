from fastapi import APIRouter, Depends, HTTPException, status

from database.get_db import get_db
from sqlalchemy.orm import Session

from models import Todos, PostTodo

router = APIRouter(
    prefix='/todos',
    tags=['todos_post'],

)


@router.post("/")
async def create_a_new_todo(todo: PostTodo, db: Session = (Depends(get_db))) -> dict:

    todo_model = Todos()

    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()

    return {'status': status.HTTP_201_CREATED, 'transaction': 'successful'}
