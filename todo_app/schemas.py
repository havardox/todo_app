from typing import Optional
from pydantic import BaseModel, Field


class TodoSchema(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(default=1, gt=1, lt=6, description="The priority must be between 1-6")
    done: bool


class CreateUserSchema(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str
 