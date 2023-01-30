from fastapi import APIRouter, Depends
from database.get_db import get_db
from sqlalchemy.orm import Session
from models import Todos

router = APIRouter(
    prefix='/todos',
    tags=['todos'],

    responses={404: {"description": "Not found"}}
)

@router.get("/")
async def get_all_todos(db:Session = Depends(get_db)):
    return db.query(Todos).all()