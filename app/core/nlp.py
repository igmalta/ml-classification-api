# app/core/nlp.py
# Classifier FastAPI endpoint

from typing import Dict

from fastapi import APIRouter, Depends, status

from ai import utils
from app.api import nlp
from app.config import logger
from app.schema import schemas
from app.schema.oa2 import get_current_user

# Define classifier endpoint
router = APIRouter(tags=["NLP"], prefix="/nlp")


@router.on_event("startup")
def startup() -> None:
    """
    Load a Transformer pre-trained model before the application starts up.
    """
    # It is necessary set as global variables
    global device
    global model
    # Device: CPU or GPU
    device = utils.set_device(cuda=False)
    # Load Transformer model
    model = utils.load_classification_model(device)
    logger.info("Load Transformer pre-trained model DONE .")


@router.post("/", status_code=status.HTTP_200_OK)
def classifier(
    request: schemas.Classifier, current_user: schemas.User = Depends(get_current_user)
) -> Dict:
    """
    Takes an input text sequence, normalizes it, and predicts the probability
    that the sequence belongs to a custom class category. There can be any number
    of candidate classes.

    Args:
        **sequence** (str): Input text to classify.
        **candidate_labels** (str): Candidate labels to set as categories.
        current_user (schemas.User, optional): Authorized user.

    Returns:
        Dict: The probability that the input text belongs to a custom class
        category.
    """

    inference = nlp.classifier(
        text=request.sequence, candidate_labels=request.candidate_labels, model=model
    )
    logger.success("Candidate labels probability inference DONE .")
    return inference
