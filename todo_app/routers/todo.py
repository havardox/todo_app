from typing import Literal
from fastapi import Depends, HTTPException, APIRouter, Query, Response, status
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
        todo.date_due = todo_schema.date_due
        todo.time_due = todo_schema.time_due
        todo.done = todo_schema.done
        todo.user = user

        session.add(todo)
        session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ___________ Read ___________ #


@router.get("/user")
async def get_todos(
    date_from: datetime.date | None = Query(None, description="The date the the task is set to be due"),
    date_until: datetime.date | None = Query(None, description="The time the the task is set to be due. Date must not be empty"),
    user: models.User = Depends(get_current_active_user),
):
    with SessionLocal() as session:
        query = session.query(models.Todo).filter(models.Todo.user == user)
        if date_from is not None:
            query = query.filter(models.Todo.date_due >= date_from)
        if date_until is not None:
            query = query.filter(
                models.Todo.date_due <= date_until,
            )
        all_todos = query.all()
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
    todo_id: int,
    todo_schema: TodoSchema,
    user: models.User = Depends(get_current_active_user),
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
