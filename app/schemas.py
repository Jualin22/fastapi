from datetime import datetime
from pydantic import BaseModel, EmailStr, conint
from typing import Optional


# Define pydantic Base Model
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


class PostCreate(PostBase):
    pass


class PostResponse(BaseModel):
    id: str
    title: str
    content: str
    published: bool = True
    created_at: datetime
    owner_id: str

    class Config:
        orm_mode = True


class PostOut(PostResponse):
    mail: str
    votes: int

    class Config:
        orm_mode = True


# Define pydantic Base Model
class UserBase(BaseModel):
    mail: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class UserResponse(BaseModel):
    mail: EmailStr
    id: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    mail: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]


class Vote(BaseModel):
    post_id: str
    dir: conint(le=1)
