from fastapi import APIRouter, Depends, status, HTTPException

from database.get_db import get_db
from sqlalchemy.orm import Session

from models import Todos, PostTodo
from .todos_get import http_exception_404
from auth.routers.auth import decode_token

router = APIRouter(
    prefix='/todos',
    tags=['todos'],

)


@router.post("/")
async def create_a_new_todo(todo: PostTodo,
                            db: Session = (Depends(get_db)),
                            user=Depends(decode_token)) -> dict:
    """
    Endpoint for creating a Todo.
    User has to be authorized to make a Todo.
    """

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Not Authorized')

    todo_model = Todos()

    todo_model.owner_id = user.get('id')
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
                              db: Session = Depends(get_db),
                              user=Depends(decode_token)) -> dict:

    """
    Endpoint To patch a specific todo
    User has to be authorized and can only
    update their own todos.
    """

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Not Authorized')

    todo_origin = db.query(Todos)\
        .filter(Todos.owner_id == user.get('id'))\
        .filter(todo_id == Todos.id).first()

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
                               db: Session = Depends(get_db),
                               user=Depends(decode_token)) -> dict:

    """Endpoint to delete a specific Todo"""

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Not Authorized')

    todo_origin = db.query(Todos)\
        .filter(Todos.owner_id == user.get('id'))\
        .filter(todo_id == Todos.id).first()

    if todo_origin is None:
        raise http_exception_404()

    db.delete(todo_origin)
    db.commit()

    return {'status': status.HTTP_204_NO_CONTENT, 'transaction': 'successful deletion'}
