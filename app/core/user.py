# app/core/user.py
# User register FastAPI endpoint

from typing import Dict

from fastapi import APIRouter, Form, HTTPException, status

from app.api import user
from app.models import models
from app.schema import schemas

# Define user register endpoint
router = APIRouter(tags=["Users"], prefix="/users")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(
    email: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    password: str = Form(...),
) -> Dict:
    """New user registration form to save into the db.

    Args:
        **email** (str): A new user email.
        **first_name** (str): First name of the new user.
        **last_name** (str): Last name of the new user.
        **password** (str): Chosen password of the new user.

    Raises:
        HTTPException: Error 409: The username already exists.

    Returns:
        Dict: Username (email).
    """
    # Try to retrieve the user in the db
    user_exists = models.User.objects(email=email).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"The username already exists"
        )
    return user.create(email, first_name, last_name, password)
