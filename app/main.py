# app/main.py
# FastAPI start app
# uvicorn app.main:app --reload

from typing import Dict

from fastapi import FastAPI, Request, status

from ai import utils
from app.core import auth, nlp, user
from app.database import mongodb

# Define app
app = FastAPI(
    title="Zero-Shot Classification API",
    description="Classification and evaluation of texts in English through\
                 Zero-Shot learning. This task allows classifying other data\
                 types different from those used to train the model with custom\
                 labels.",
    version="0.0.1",
)

# Add routes of endopints
app.include_router(mongodb.router)
app.include_router(auth.router)
app.include_router(nlp.router)
app.include_router(user.router)

# URL root
@app.get("/", tags=["General"])
@utils.construct_response
def index(request: Request) -> Dict:
    """Health check

    Args:
        request (Request): Health check message.

    Returns:
        Dict: Response message.
    """
    response = {
        "message": "Successful operation",
        "status-code": status.HTTP_200_OK,
        "data": {},
    }
    return response
