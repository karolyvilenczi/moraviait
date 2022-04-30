
from pydantic import BaseModel

from typing import (
    List
)

# ---------------------------------------------------------------

# User and Users
# -----------------------------
# base user schema
class UserSchema(BaseModel):
    last_name: str
    first_name: str
    age: int

    class Config:
        orm_mode = True
# -----------------------------

# User schema for UPDATE / PUT
class UpdateUserSchema(UserSchema):
    id : int

# -----------------------------
class AllUsersSchema(BaseModel):
    users: List[UserSchema]

    
