# app/core/auth.py
# Login FastAPI endpoint

import json
from datetime import timedelta
from typing import Dict

from decouple import config
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.models import models
from app.schema.hash import Hash
from app.schema.token import create_access_token

ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)

# Define login endpoint
router = APIRouter(
    prefix="/login",
    tags=["Authentication"],
)


@router.post("/")
def login(request: OAuth2PasswordRequestForm = Depends()) -> Dict:
    """Registered users login form and credentials check.

    Args:
        **grant_type** (str, optional): The way in which an application obtains an
        access token.
        **username** (str): User email.
        **password** (str): Password.
        **scope** (str, optional): One or more strings separated by spaces that
        indicate what permissions the application requests.
        **client_id** (str, optional): The public client id of the application,
        obtained when the developer registered it for the first time.
        **client_secret** (str, optional): The private client id of the application,
        obtained when the developer registered it for the first time.

    Raises:
        HTTPException: Error 404: User not found.
        HTTPException: Error 404: Incorrect password.

    Returns:
        Dict: Access token (JWT token).
    """

    # Try to retrieve the user in the db
    user = models.User.objects(email=request.username).first()
    # Error if username or password doesn't exist
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")
    if not Hash.verify(user["password"], request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password")
    # Transform object retrieved from the db into json
    user = json.loads(user.to_json())
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Create token access
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
