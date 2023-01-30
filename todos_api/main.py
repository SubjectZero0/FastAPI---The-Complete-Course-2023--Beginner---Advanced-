from fastapi import FastAPI
from database.db import engine
from routers import todos_get
import models

app = FastAPI()

models.Base.metadata.create_all(bind = engine)

app.include_router(todos_get.router)

