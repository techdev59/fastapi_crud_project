"""
Module containing functions for user and post management.

This module provides CRUD (Create, Read, Update, Delete) operations for users and posts
using SQLAlchemy and FastAPI.

Functions:
    - get_user_by_email(db: Session, email: str): Retrieve a user by email from the database.
    - create_user(db: Session, user: schemas.UserCreate): Create a new user in the database.
    - get_posts(db: Session, user_id: int): Retrieve all posts belonging to a specific user.
    - create_post(db: Session, post: schemas.PostCreate, user_id: int): Create a new post for a specific user.
    - delete_post(db: Session, post_id: int, user_id: int): Delete a post owned by a specific user.
"""

from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import models, schemas, auth
from fastapi import HTTPException


def get_user_by_email(db: Session, email: str):
    """
    Retrieve a user by email from the database.

    Args:
        db (Session): Database session.
        email (str): Email address of the user.

    Returns:
        User: User object if found, otherwise None.
    """
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    """
    Create a new user in the database.

    Args:
        db (Session): Database session.
        user (schemas.UserCreate): User creation details.

    Returns:
        User: Created user object.
    """
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_posts(db: Session, user_id: int):
    """
    Retrieve all posts belonging to a specific user.

    Args:
        db (Session): Database session.
        user_id (int): ID of the user whose posts are to be retrieved.

    Returns:
        List[Post]: List of posts belonging to the specified user.
    """
    return db.query(models.Post).filter(models.Post.owner_id == user_id).all()


def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    """
    Create a new post for a specific user.

    Args:
        db (Session): Database session.
        post (schemas.PostCreate): Post creation details.
        user_id (int): ID of the user who owns the post.

    Returns:
        Post: Created post object.
    """
    db_post = models.Post(**post.dict(), owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int, user_id: int):
    """
    Delete a post owned by a specific user.

    Args:
        db (Session): Database session.
        post_id (int): ID of the post to be deleted.
        user_id (int): ID of the user who owns the post.

    Returns:
        Post: Deleted post object.
    
    Raises:
        HTTPException: If the post is not found.
    """
    post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.owner_id == user_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return post
