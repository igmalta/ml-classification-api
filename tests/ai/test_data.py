# Test data components.
# python -m pytest tests/ai/test_data.py

import pytest

from ai import data


@pytest.mark.parametrize(
    "text, clean_text",
    [
        ("Hello World 2021", "hello world"),
        ("HELLO WORLD", "hello world"),
        ("Mailto:info@mail.com, https://test.com/", "mailto info"),
        ("Hello \n\n Magic \t World", "hello magic world"),
        ("Phone number: +5411415111", "phone number"),
    ],
)
def test_clean_text(text, clean_text):
    assert data.clean_text(text=text) == clean_text
