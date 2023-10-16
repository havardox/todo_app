from fastapi import FastAPI
import uvicorn

import todo_app.models as models
from todo_app.db import engine
from todo_app.routers import auth
from todo_app.config import settings

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router, tags=["auth"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)