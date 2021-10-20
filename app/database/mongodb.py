# app/database/mongodb.py
# MongoDB configuration

from decouple import config
from fastapi import APIRouter
from mongoengine import connect, disconnect

from app.config import logger

# Database params
DB_NAME = config("DB_NAME", cast=str)
DB_ALIAS = config("DB_ALIAS", cast=str)
DB_HOST = config("DB_HOST", cast=str)
DB_PORT = config("DB_PORT", cast=int)

# Define a router
router = APIRouter()


@router.on_event("startup")
def startup() -> None:
    """Connect to db before the application starts up."""

    # Connect to database
    connect(db=DB_NAME, alias=DB_ALIAS, host=DB_HOST, port=DB_PORT)
    logger.info("Database connection DONE .")


@router.on_event("shutdown")
def shutdown() -> None:
    """Disconnect the db when the application is shutting down."""

    # Disconnect database
    disconnect(alias=DB_ALIAS)
    logger.info("Database disconnected DONE .")
