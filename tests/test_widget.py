import pytest

from src.widget import *

@pytest.mark.parametrize("card_number, expected", [
    ("Mastercard 4276 3800 1234 5678", "Mastercard 4276 3800 1234 5678"),
])