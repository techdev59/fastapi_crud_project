"""
Module containing Pydantic models for user and post schemas.

This module defines Pydantic models representing the schema structures for users and posts.

Classes:
    - UserBase: Base schema for user data.
    - UserCreate: Schema for creating a new user.
    - UserLogin: Schema for user login.
    - Token: Schema for authentication token.
    - PostBase: Base schema for post data.
    - PostCreate: Schema for creating a new post.
    - Post: Schema for post data with additional configuration for ORM mode.
"""

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """
    Base schema for user data.

    Attributes:
        email (EmailStr): Email address of the user.
    """
    email: EmailStr


class UserCreate(UserBase):
    """
    Schema for creating a new user.

    Inherits:
        UserBase
    """
    password: str


class UserLogin(UserBase):
    """
    Schema for user login.

    Inherits:
        UserBase
    """
    password: str


class Token(BaseModel):
    """
    Schema for authentication token.

    Attributes:
        access_token (str): Access token.
        token_type (str): Type of token (default value: "bearer").
    """
    access_token: str
    token_type: str = "bearer"


class PostBase(BaseModel):
    """
    Base schema for post data.

    Attributes:
        text (str): Text content of the post.
    """
    text: str


class PostCreate(PostBase):
    """
    Schema for creating a new post.

    Inherits:
        PostBase
    """
    pass


class Post(PostBase):
    """
    Schema for post data with additional configuration for ORM mode.

    Inherits:
        PostBase

    Configures:
        orm_mode (bool): Whether the model is used in ORM mode (default value: True).
    """
    id: int

    class Config:
        orm_mode = True
