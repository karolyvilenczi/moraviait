
from pydantic import BaseModel

from typing import (
    List,
    Optional
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


# ---------------------------------------------------------------
# Article and Articles
# -----------------------------
# base user schema
class ArticleSchema(BaseModel):
    url: str
    text: str    

    class Config:
        orm_mode = True
# -----------------------------

# Article schema for UPDATE / PUT
class UpdateArticleSchema(ArticleSchema):
    id : int

# -----------------------------
class AllArticlesSchema(BaseModel):
    articles: List[ArticleSchema]


# ---------------------------------------------------------------
# Keyword schema
# -----------------------------
# base kw schema
class KeywordSchema(BaseModel):
    keywords: List[str]
    # show_keywords: Optional[str]

    class Config:
        orm_mode = True

    
