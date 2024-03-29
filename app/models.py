"""
Module defining SQLAlchemy models for users and posts.

This module defines SQLAlchemy models for users and posts with their respective relationships.

Classes:
    - User: Represents a user in the database.
    - Post: Represents a post in the database.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


class User(Base):
    """
    Represents a user in the database.

    Attributes:
        id (int): The unique identifier for the user.
        email (str): Email address of the user.
        hashed_password (str): Hashed password of the user.
        posts (relationship): Relationship attribute defining the user's posts.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    posts = relationship("Post", back_populates="owner")


class Post(Base):
    """
    Represents a post in the database.

    Attributes:
        id (int): The unique identifier for the post.
        text (str): Text content of the post.
        owner_id (int): ID of the user who owns the post.
        owner (relationship): Relationship attribute defining the post's owner.
    """
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")
