"""
Module for defining SQLAlchemy database engine and base.

This module defines the SQLAlchemy database engine and declarative base for creating models.

Variables:
    - SQLALCHEMY_DATABASE_URL (str): Database connection string.
    - engine: SQLAlchemy database engine.

Classes:
    - Base: Declarative base class for defining models.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Define your database connection string
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://fastapi_user:password@localhost/fastapi_blog_db"

# Create the engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



Base = declarative_base()
