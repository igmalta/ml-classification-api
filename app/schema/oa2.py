# app/oa2/hash.py
# User authorization

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.schema.token import verify_token

# Add OAuth2 security to user login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """Validate user login credentials.

    Args:
        token (str, optional): Access token. Defaults to
        Depends(oauth2_scheme).

    Returns:
        str: Username.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "bearer"},
    )
    return verify_token(token, credentials_exception=credentials_exception)
