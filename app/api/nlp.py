# app/api/nlp.py
# Text classification.

from typing import Dict, List

import transformers

from ai import data


def classifier(
    text: str,
    candidate_labels: List,
    model: transformers.pipelines.base.Pipeline,
) -> Dict:
    """
    Takes an input text sequence, normalizes it, and predicts the probability
    that the sequence belongs to a custom class category. There can be any number of
    candidate classes.

    Args:
        text (str): Input text to classify.
        candidate_labels (str): Candidate labels to set as categories.
        model (transformers.pipelines.base.Pipeline): Pre-trained Transformer
        model.

    Returns:
        Dict: The probability that the input text belongs to a custom class
        category.
    """

    # Normalizes input text
    text = data.clean_text(text)

    return model(text, candidate_labels)
