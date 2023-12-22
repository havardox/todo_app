from typing import Optional
import pydantic
from pydantic import BaseModel, Field, validator
import datetime


class TodoSchema(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(default=1, gt=0, lt=7, description="The priority must be between 1-6")
    date_due: datetime.date | None = None
    time_due: datetime.time | None = None
    done: bool

    @validator('time_due')
    @classmethod
    def date_must_exist_if_time(cls, value: str, values: dict):
        if "date_due" not in values:
            raise ValueError("time_due can't be set when date_due doesn't exist")

        return value

class CreateUserSchema(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str
 
