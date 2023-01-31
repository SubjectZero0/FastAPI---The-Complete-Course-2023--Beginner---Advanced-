from fastapi import APIRouter, Depends, status

from models import Users, CreateUser
from .todos_get import http_exception_404

from database.get_db import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext

# -------------------------------------------------------------------------

# create a context instance for bcrypt
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


# define function that hashes any password
def get_password_hash(password):
    return bcrypt_context.hash(password)

# -------------------------------------------------------------------------


# define router
router = APIRouter(
    prefix='/users',
    tags=['users']
)

# -------------------------------------------------------------------------


#  create "create user" router
@router.post('/create_user')
async def create_a_new_user(new_user: CreateUser,
                            db: Session = Depends(get_db)):
    """
    Endpoint for creating a new User
    """

    user_model = Users()

    user_model.username = new_user.username

    hashed_password = get_password_hash(new_user.password)
    user_model.hashed_password = hashed_password

    user_model.email = new_user.email
    user_model.first_name = new_user.first_name
    user_model.last_name = new_user.last_name
    user_model.is_active = True

    db.add(user_model)
    db.commit()

    return {'status': status.HTTP_201_CREATED, 'transaction': "User Created Successfully"}
