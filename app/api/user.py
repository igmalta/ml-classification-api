# app/api/user.py
# User register.

from typing import Dict

from decouple import config
from mongoengine.context_managers import switch_db

from app.models import models
from app.schema.hash import Hash

DB_ALIAS = config("DB_ALIAS", cast=str)


def create(email: str, first_name: str, last_name: str, password: str) -> Dict:
    """
    Save into the database a new user registration form data. The password is
    hashed with multiple algorithms.

    Args:
        email (str): A new user email.
        first_name (str): First name of the new user.
        last_name (str): Last name of the new user.
        password (str): Chosen password of the new user.

    Returns:
        Dict: New user email.
    """

    # Hashed password
    hashedPassword = Hash.bcrypt(password)
    # User scheme
    user = models.User(
        email=email, first_name=first_name, last_name=last_name, password=hashedPassword
    )
    # Save input data form into db
    # "switch_db" would not be necessary since there is only one database
    with switch_db(user, DB_ALIAS) as user:
        user.save()
    return user
