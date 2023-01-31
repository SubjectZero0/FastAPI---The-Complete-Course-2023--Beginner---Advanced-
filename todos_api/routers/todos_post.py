from fastapi import APIRouter, Depends, status

from database.get_db import get_db
from sqlalchemy.orm import Session

from models import Todos, PostTodo
from .todos_get import http_exception_404

router = APIRouter(
    prefix='/todos',
    tags=['todos'],

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


@router.put('/{todo_id}')
async def patch_specific_todo(todo_final: PostTodo,
                              todo_id: int = Todos,
                              db: Session = Depends(get_db)) -> dict:

    """Endpoint To patch a specific todo"""

    todo_origin = db.query(Todos).filter(todo_id == Todos.id).first()

    if todo_origin is None:
        raise http_exception_404()

    todo_origin.title = todo_final.title
    todo_origin.description = todo_final.description
    todo_origin.priority = todo_final.priority
    todo_origin.complete = todo_final.complete

    db.add(todo_origin)
    db.commit()

    return {'status': status.HTTP_200_OK, 'transaction': 'successful'}


@router.delete('/{todo_id}')
async def delete_specific_todo(todo_id: int = Todos,
                               db: Session = Depends(get_db)) -> dict:

    """Endpoint to delete a specific Todo"""

    todo_origin = db.query(Todos).filter(todo_id == Todos.id).first()

    if todo_origin is None:
        raise http_exception_404()

    db.delete(todo_origin)
    db.commit()

    return {'status': status.HTTP_204_NO_CONTENT, 'transaction': 'successful deletion'}
