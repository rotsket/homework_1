import pytest


@pytest.fixture
def card_number():
    return tuple(["4213470010295816"])

@pytest.fixture
def invalid_card_number():
    return tuple(["daqsdad", 22323, "12251"])