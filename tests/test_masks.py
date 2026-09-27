import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1234567890123678", "1234 56** **** 3678"),
        (1234567890123678, "1234 56** **** 3678"),  # Проверка на int
        ("1234 5678 9012 3678", "1234 56** **** 3678"),
        ("1234AAAA5678ASDSAD90123678abcdef", "1234 56** **** 3678"),
        ("343434343434343", "3434 34** **** 343"),  # 15 цифр
        ("1234567890123456789", "1234 56** **** 3456 789"),  # 19 цифр
        ("4000123456789", "4000 12** **** 9"),  # 13 цифр
    ],
)
def test_get_mask_card_number(card_number, expected):
    """Проверка номера карты с: инт, стр, с буквами, с разной длиной карты"""
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("4213470010295816", "**** **00 1029 ****"),
        (4213470010295816, "**** **00 1029 ****"),  # Проверка на int
        ("4213 4700 1029 5816", "**** **00 1029 ****"),
        ("42134700102qweqwe95816qweqweqw", "**** **00 1029 ****"),
    ],
)
def test_get_mask_card_number_reverse(card_number, expected):
    assert get_mask_card_number(card_number, reverse=True) == expected


def test_get_mask_card_number_invalid(invalid_card_number):
    """проверка неправильной длины"""
    for item in invalid_card_number:
        with pytest.raises(ValueError):
            get_mask_card_number(item)


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("4213470010295816", "**5816"),
        (4213470010295816, "**5816"),
        ("4213470010ss2asd9581s6", "**5816"),
        ("343434343434343", "**4343"),  # 15 цифр
        ("1234567890123456789", "**6789"),  # 19 цифр
        ("4000123456789", "**6789"),  # 13 цифр
    ],
)
def test_get_mask_account(card_number, expected):
    """Проверка номера карты с: инт, стр, с буквами, с разной длиной карты"""
    assert get_mask_account(card_number) == expected


def test_get_mask_account_invalid(invalid_card_number):
    """проверка неправильной длины"""
    for item in invalid_card_number:
        with pytest.raises(ValueError):
            get_mask_account(item)
