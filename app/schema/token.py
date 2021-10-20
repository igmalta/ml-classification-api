# app/token/hash.py
# Credentials generation (JWT token)

from datetime import datetime, timedelta
from typing import Optional

from decouple import config
from fastapi import HTTPException
from jose import JWTError, jwt

# Openssl rand -hex 32
SECRET_KEY = config("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=60, cast=int)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a access token.

    Args:
        data (dict): Contains the username.
        expires_delta (Optional[timedelta], optional): Token expiration time.
        Defaults to None.

    Returns:
        str: Access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str, credentials_exception: HTTPException) -> str:
    """Validate user login credentials (token).

    Args:
        token (str): Access request token.
        credentials_exception (HTTPException): Error 401: Unauthorized user.

    Raises:
        credentials_exception: Could not validate credentials.
        credentials_exception: Could not validate credentials.

    Returns:
        str: Username.
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username
