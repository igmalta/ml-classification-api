# ai/data.py
# Data processing operations.

import re
import string


def clean_text(text: str) -> str:
    """
    Transform all text to lowercase, remove white spaces and special symbols.

    Args:
        text (str): Text to process.

    Returns:
        str: Processed text.
    """
    # Transform all text to lowercase
    text = text.lower()
    # Remove white spaces and special symbols
    text = re.sub(r"https*\S+", " ", text)
    text = re.sub(r"@\S+", " ", text)
    text = re.sub(r"#\S+", " ", text)
    text = re.sub(r"\'\w+", "", text)
    text = re.sub("[%s]" % re.escape(string.punctuation), " ", text)
    text = re.sub(r"\w*\d+\w*", "", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = text.strip()
    return text
