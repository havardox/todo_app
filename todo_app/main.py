from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi, get_openapi_operation_metadata
import uvicorn

import todo_app.models as models
from todo_app.db import engine
from todo_app.routers import auth, todo

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router, tags=["auth"])
app.include_router(todo.router, tags=["todo"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
