from typing import Literal
from fastapi import Depends, HTTPException, APIRouter, Response, status
import datetime

from todo_app.schemas import TodoSchema
import todo_app.models as models
from todo_app.db import SessionLocal, engine
from todo_app.routers.auth import get_current_active_user

router = APIRouter(
    prefix="/todo", tags=["todo"], responses={404: {"description": "Not Found"}}
)

models.Base.metadata.create_all(bind=engine)

# ___________ Create ___________ #


@router.post("/")
async def create_todo(
    todo_schema: TodoSchema,
    user: models.User = Depends(get_current_active_user),
):
    with SessionLocal() as session:
        
        todo = models.Todo()
        todo.title = todo_schema.title
        todo.description = todo_schema.description
        todo.priority = todo_schema.priority
        todo.done = todo_schema.done
        todo.user = user

        session.add(todo)
        session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ___________ Read ___________ #


@router.get("/user")
async def get_todos(date_from: datetime.date | None = None, date_until: datetime.date | None = None, user: models.User = Depends(get_current_active_user)):
    with SessionLocal() as session:
        all_todos = session.query(models.Todo).filter(models.Todo.user == user).all()
    if all_todos is not None:
        return all_todos
    raise HTTPException(status_code=404, detail="No todos found")


@router.get("/{todo_id}")
async def get_todo(todo_id: int, user: models.User = Depends(get_current_active_user)):
    
    with SessionLocal() as session:
        todo = (
            session.query(models.Todo)
            .filter(models.Todo.id == todo_id, models.Todo.user == user)
            .first()
        )

    if todo is not None:
        return todo
    raise HTTPException(status_code=404, detail="Todo not found")


# ___________ Update ___________ #


@router.put("/{todo_id}")
async def update_todo(
    todo_id: int, todo_schema: TodoSchema, user: models.User = Depends(get_current_active_user)
):
    with SessionLocal() as session:
        todo = (
            session.query(models.Todo)
            .filter(models.Todo.id == todo_id, models.Todo.user == user)
            .first()
        )

        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")

        todo.title = todo_schema.title
        todo.description = todo_schema.description
        todo.done = todo_schema.done
        todo.priority = todo_schema.priority

        session.add(todo)
        session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ___________ Delete ___________ #


@router.delete("/{todo_id}")
async def delete_todo(todo_id: int, user: dict = Depends(get_current_active_user)):
    with SessionLocal() as session:
        todo = (
            session.query(models.Todo)
            .filter(models.Todo.id == todo_id, models.Todo.user == user)
            .first()
        )

        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")

        session.query(models.Todo).filter(models.Todo.id == todo_id).delete()
        session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)