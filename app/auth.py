from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
import jwt
from app.db import SessionLocal
from passlib.context import CryptContext
from datetime import datetime, timedelta

from app.models import User
from app.db import SessionLocal

SECRET_KEY = "your-secret-key"  # Replace with a strong secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """
    Verify the plain text password against the hashed password.

    Parameters:
        - plain_password (str): The plain text password provided by the user.
        - hashed_password (str): The hashed password stored in the database.

    Returns:
        - bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db, email: str):
    """
    Retrieve a user from the database based on their email.

    Parameters:
        - db: Database session.
        - email (str): Email of the user to retrieve.

    Returns:
        - User: The user object retrieved from the database.
    """
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db, email: str, password: str):
    """
    Authenticate a user based on their email and password.

    Parameters:
        - db: Database session.
        - email (str): Email of the user to authenticate.
        - password (str): Password provided by the user.

    Returns:
        - User: The authenticated user object if successful, None otherwise.
    """
    user = get_user(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta):
    """
    Create an access token with expiration time.

    Parameters:
        - data (dict): Data to include in the token.
        - expires_delta (timedelta): Expiration time for the token.

    Returns:
        - str: The generated access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(db=Depends(SessionLocal), token: str = Depends(oauth2_scheme)):
    """
    Get the current authenticated user.

    Parameters:
        - db: Database session.
        - token (str): Access token provided by the client.

    Returns:
        - User: The authenticated user object.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(db, email)
    if user is None:
        raise credentials_exception
    return user
