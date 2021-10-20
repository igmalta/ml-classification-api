# ai/utils.py
# Utility functions.

import os
from datetime import datetime
from functools import wraps
from typing import Dict

import torch
import transformers
from decouple import config
from fastapi import Request

MODEL_PATH = config("MODEL_PATH", cast=str)
ZERO_SHOT_MODEL = config("ZERO_SHOT_MODEL", cast=str)


def set_device(cuda: bool) -> int:
    """Set the device for computation.
    Args:
        cuda (bool): Determine whether to use GPU or not (if available).
    Returns:
        int: Index of a currently selected device, CPU or GPU.
    """
    device = torch.device("cuda" if (torch.cuda.is_available() and cuda) else "cpu")
    if device.type == "cuda":
        device = int(torch.cuda.current_device())
    else:
        device = -1
    return device


def load_classification_model(device: int) -> transformers.pipelines.base.Pipeline:
    """
    Load a pre-trained model from Transformer library to perform Zero-Shot text
    classification.

    Args:
        device (int): Index of a currently selected device, CPU or GPU.

    Returns:
        transformers.pipelines.base.Pipeline: Pre-trained Transformer model.
    """
    # You could omit using "MODEL_PATH" and download the model from Hugging Face
    # to the cache
    model = transformers.pipeline(
        "zero-shot-classification", model=os.path.join(MODEL_PATH, ZERO_SHOT_MODEL), device=device
    )
    return model


def construct_response(f: dict) -> Dict:
    """Construct a JSON response for an endpoint's results.

    Args:
        f (dict): Additional data to add to the response.

    Returns:
        Dict: Response message.
    """

    @wraps(f)
    def wrap(request: Request, *args, **kwargs):
        results = f(request, *args, **kwargs)
        # Construct response
        response = {
            "message": results["message"],
            "method": request.method,
            "status-code": results["status-code"],
            "timestamp": datetime.now().isoformat(),
            "url": request.url._url,
        }
        # Add data
        if "data" in results:
            response["data"] = results["data"]
        return response

    return wrap
