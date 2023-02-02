from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
import models
from sqlalchemy.orm import Session
from database.get_db import get_db
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
# -----------------------------------------------------------------------

# Authentication and OAUTH2 authorization

# -----------------------------------------------------------------------

# safeguard this
SECRET_KEY = 'sdklfjlashkdf3jhh3h3h3h3h3hsadlfjskf'
ALGORITHM = 'HS256'

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')

# -----------------------------------------------------------------------

router = APIRouter(
    prefix='/auth',
    tags=['users']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password, hashed_password):
    """
    Verifies a given password against its hashed counterpart
    """
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str,
                      password: str,
                      db: Session = Depends(get_db)):
    """
    Authenticates a user based on their credentials
    """

    user = db.query(models.Users).filter(
        models.Users.username == username).first()

    if not user:
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return user


def create_access_token(username: str,
                        user_id: int,
                        expires_delta: Optional[timedelta] = None):
    """
    Creates an access Token 
    """
    encode = {'sub': username, 'id': user_id}

    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(minutes=15)

    encode.update({'exp': expires})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# -----------------------------------------------------------------------


@router.post('/token')
async def get_auth_token(form_data: OAuth2PasswordRequestForm = Depends(),
                         db: Session = Depends(get_db)):
    """
    Login, to receive an access Token
    """
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    token_expiration = timedelta(minutes=20)
    token = create_access_token(user.username,
                                user.id,
                                expires_delta=token_expiration)

    return {'token': token}
