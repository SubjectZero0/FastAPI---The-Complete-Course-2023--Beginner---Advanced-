from fastapi import APIRouter, Depends, HTTPException, status

from database.get_db import get_db
from sqlalchemy.orm import Session

from models import Todos

# --------------------------------------------------------------------------
#  Set up Router

router = APIRouter(
    prefix='/todos',
    tags=['todos'],

)
# ---------------------------------------------------------------------------

# define exceptions


def http_exception_404():
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not Found')


# ---------------------------------------------------------------------------
#  Define routes for GET requests

@router.get("/")
async def get_all_todos(db: Session = Depends(get_db)):
    """Get all the available todo list items"""
    return db.query(Todos).all()


@router.get('/{todo_id}')
async def get_specific_todo(todo_id: int, db: Session = Depends(get_db)):
    """Get a todo item by specifying the ID"""

    queryset = db.query(Todos).filter(Todos.id == todo_id).first()

    if queryset is None:
        raise http_exception_404()

    return queryset
