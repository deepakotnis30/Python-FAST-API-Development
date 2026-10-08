from operator import le
from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, Field, conint
from datetime import datetime



class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title:'str'
    content:'str'
    published: bool = True

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int   
    created_at: datetime
    owner_id: int
    owner: UserOut

class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1)]