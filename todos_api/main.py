from fastapi import FastAPI
from database.db import engine
from routers import todos_get, todos_post
from auth.routers import create_user, auth
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(todos_get.router)
app.include_router(todos_post.router)
app.include_router(create_user.router)
app.include_router(auth.router)
