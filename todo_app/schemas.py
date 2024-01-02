from typing import Optional
import pydantic
from pydantic import BaseModel, Field, validator
import datetime


class TodoSchema(BaseModel):
    title: str = Field(..., min_length=5, max_length=256)
    description: str | None = Field(None, max_length=2048)
    priority: int = Field(default=1, gt=0, lt=7, description="The priority must be between 1-6")
    date_due: datetime.date | None = None
    time_due: datetime.time | None = None
    done: bool = False

    @validator('time_due')
    @classmethod
    def date_must_exist_if_time(cls, value: str, values: dict):
        if "date_due" not in values:
            raise ValueError("time_due can't be set when date_due doesn't exist")

        return value

class CreateUserSchema(BaseModel):
    username: str = Field(..., max_length=30)
    email: str = Field(..., max_length=320)
    first_name: str | None = Field(None, max_length=256)
    last_name: str | None = Field(None, max_length=256)
    password: str = Field(..., max_length=2048)

