"""
API routes for user authentication and post management.

This module defines API routes for user signup, login, adding posts, retrieving posts, and deleting posts.

Routes:
    - /signup/: Endpoint for user signup.
    - /login/: Endpoint for user login.
    - /addPost/: Endpoint for adding a new post.
    - /getPosts/: Endpoint for retrieving posts of the authenticated user.
    - /deletePost/: Endpoint for deleting a post of the authenticated user.
"""


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from cachetools import TTLCache

from app import schemas, crud, auth
from app.db import get_db

router = APIRouter()


@router.post("/signup/", response_model=schemas.Token)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint for user signup.

    Args:
        user (schemas.UserCreate): User creation details.
        db (Session): Database session.

    Returns:
        schemas.Token: Token response model.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.post("/login/", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Endpoint for user login.

    Args:
        user (schemas.UserLogin): User login details.
        db (Session): Database session.

    Returns:
        schemas.Token: Token response model.
    """
    db_user = crud.authenticate_user(db, email=user.email, password=user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/addPost/", response_model=schemas.Post)
def add_post(post: schemas.PostCreate, current_user: schemas.User = Depends(auth.get_current_user),
             db: Session = Depends(get_db)):
    """
    Endpoint for adding a new post.

    Args:
        post (schemas.PostCreate): Post creation details.
        current_user (schemas.User): Authenticated user.
        db (Session): Database session.

    Returns:
        schemas.Post: Created post response model.
    """
    return crud.create_post(db=db, post=post, user_id=current_user.id)



# Create an in-memory cache with a TTL (time-to-live) of 5 minutes
cache = TTLCache(maxsize=1000, ttl=300)


def cache_key(user_id: int):
    """Generate cache key based on user ID."""
    return f"user_{user_id}"


@router.get("/getPosts/", response_model=List[schemas.Post])
def get_posts(current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    """
    Endpoint for retrieving posts of the authenticated user.

    Args:
        current_user (schemas.User): Authenticated user.
        db (Session): Database session.

    Returns:
        List[schemas.Post]: List of posts belonging to the authenticated user.
    """
    """Get all posts added by the user, with response caching."""
    cached_posts = cache.get(cache_key(current_user.id))
    if cached_posts is not None:
        return cached_posts
    
    posts = crud.get_posts(db=db, user_id=current_user.id)
    # Cache the posts with the user's ID as the cache key
    cache[cache_key(current_user.id)] = posts
    return posts
    #return crud.get_posts(db=db, user_id=current_user.id)


@router.delete("/deletePost/", response_model=schemas.Post)
def delete_post(post_id: int, current_user: schemas.User = Depends(auth.get_current_user),
                db: Session = Depends(get_db)):
    """
    Endpoint for deleting a post of the authenticated user.

    Args:
        post_id (int): ID of the post to be deleted.
        current_user (schemas.User): Authenticated user.
        db (Session): Database session.

    Returns:
        schemas.Post: Deleted post response model.
    """
    return crud.delete_post(db=db, post_id=post_id, user_id=current_user.id)
