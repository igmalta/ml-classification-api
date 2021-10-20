# Test utils components.
# python -m pytest tests/ai/test_utils.py

import pytest

from ai import utils


@pytest.fixture
def device():
    return utils.set_device(False)


def test_set_device(device):
    assert device == -1


def test_load_classification_model(device):
    assert utils.load_classification_model(device) is not None
