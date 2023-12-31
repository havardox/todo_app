import urllib.parse
import datetime

from pydantic import BaseModel
from fastapi import Depends, HTTPException, APIRouter, Query, Request, Response

from todo_app.schemas import TodoSchema
from todo_app.responses import (
    DELETE_TODO_RESPONSES,
    FETCH_USER_RESPONSES,
    CREATE_TODO_RESPONSES,
    GET_TODO_RESPONSES,
    LIST_TODOS_RESPONSES,
    UPDATE_TODO_RESPONSES,
)
import todo_app.models as models
from todo_app.db import SessionLocal, engine
from todo_app.routers.auth import get_current_active_user

router = APIRouter(
    prefix="/todo", tags=["todo"], responses={404: {"description": "Not Found"}}
)

models.Base.metadata.create_all(bind=engine)


# ___________ Create ___________ #
@router.post(
    "/", status_code=201, responses=FETCH_USER_RESPONSES | CREATE_TODO_RESPONSES
)
async def create_todo(
    request: Request,
    response: Response,
    todo_schema: TodoSchema,
    user: models.User = Depends(get_current_active_user),
):
    """
    Create a new todo item.

    Parameters:
    - `todo_schema`: The schema representing the todo item data.
    - `user`: The currently authenticated user.

    Returns:
    - `Response`: HTTP response indicating the success of the operation.
    """
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
        response.headers["Location"] = urllib.parse.urljoin(
            str(request.url), str(todo.id)
        )


# ___________ Read ___________ #
@router.get(
    "/user",
    status_code=200,
    responses=FETCH_USER_RESPONSES | LIST_TODOS_RESPONSES,
)
async def list_todos(
    date_from: datetime.date
    | None = Query(None, description="The starting date filter."),
    date_until: datetime.date
    | None = Query(None, description="The ending date filter."),
    user: models.User = Depends(get_current_active_user),
):
    """
    Retrieve todos for the authenticated user based on optional date filters.

    Parameters:
    - `date_from`: The starting date filter.
    - `date_until`: The ending date filter.
    - `user`: The currently authenticated user.

    Returns:
    - List of todos created by the user.
    """
    with SessionLocal() as session:
        query = session.query(models.Todo).filter(models.Todo.user == user)
        if date_from is not None:
            query = query.filter(models.Todo.date_due >= date_from)
        if date_until is not None:
            query = query.filter(
                models.Todo.date_due <= date_until,
            )
        all_todos = query.all()
    return all_todos


@router.get(
    "/{todo_id}", status_code=200, responses=FETCH_USER_RESPONSES | GET_TODO_RESPONSES
)
async def get_todo(todo_id: int, user: models.User = Depends(get_current_active_user)):
    """
    Retrieve a specific todo item for the authenticated user.

    Parameters:
    - `todo_id`: The ID of the todo item to retrieve.
    - `user`: The currently authenticated user.

    Returns:
    - The requested todo item.
    """
    with SessionLocal() as session:
        todo = (
            session.query(models.Todo)
            .filter(models.Todo.id == todo_id, models.Todo.user == user)
            .first()
        )

    if todo is None:
        raise HTTPException(
            status_code=404, detail=GET_TODO_RESPONSES[404]["description"]
        )
    return todo


# ___________ Update ___________ #
@router.put(
    "/{todo_id}",
    status_code=204,
    responses=FETCH_USER_RESPONSES | UPDATE_TODO_RESPONSES,
)
async def update_todo(
    todo_id: int,
    todo_schema: TodoSchema,
    user: models.User = Depends(get_current_active_user),
):
    """
    Update an existing todo item for the authenticated user.

    Parameters:
    - `todo_id`: The ID of the todo item to update.
    - `todo_schema`: The schema representing the updated todo item data.
    - `user`: The currently authenticated user.

    Returns:
    - `Response`: HTTP response indicating the success of the operation.
    """
    with SessionLocal() as session:
        todo = (
            session.query(models.Todo)
            .filter(models.Todo.id == todo_id, models.Todo.user == user)
            .first()
        )

        if todo is None:
            raise HTTPException(
                status_code=404, detail=UPDATE_TODO_RESPONSES[404]["description"]
            )

        todo.title = todo_schema.title
        todo.description = todo_schema.description
        todo.done = todo_schema.done
        todo.priority = todo_schema.priority

        session.add(todo)
        session.commit()


# ___________ Delete ___________ #
@router.delete(
    "/{todo_id}",
    status_code=204,
    responses=FETCH_USER_RESPONSES | DELETE_TODO_RESPONSES,
)
async def delete_todo(todo_id: int, user: dict = Depends(get_current_active_user)):
    """
    Delete a todo item for the authenticated user.

    Parameters:
    - `todo_id`: The ID of the todo item to delete.
    - `user`: The currently authenticated user.

    Returns:
    - `Response`: HTTP response indicating the success of the operation.
    """
    with SessionLocal() as session:
        todo = (
            session.query(models.Todo)
            .filter(models.Todo.id == todo_id, models.Todo.user == user)
            .first()
        )

        if todo is None:
            raise HTTPException(status_code=404, detail=DELETE_TODO_RESPONSES[404]["descrtiption"])

        session.query(models.Todo).filter(models.Todo.id == todo_id).delete()
        session.commit()
