from typing import Optional
from pydantic import BaseModel, Field, validator
import datetime


class TodoSchema(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(default=1, gt=0, lt=7, description="The priority must be between 1-6")
    datetime_due: datetime.datetime | None = None
    done: bool

    @validator("datetime_due")
    def ensure_date_range(cls, v):
        print(type(v))
        return v

class CreateUserSchema(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str
 