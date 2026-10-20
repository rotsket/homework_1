import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("Mastercard 4276 3800 1234 5678", "Mastercard 4276 38** **** 5678"),
        ("счет 4276 3800 1234 5678", "счет **5678"),
        ("1234 5678 9012 3678", "Карта 1234 56** **** 3678"),
        ("Mastercard 1234AAAA5678ASDSAD90123678abcdef", "Mastercard 1234 56** **** 3678"),
        ("Mastercard 343434343434343", "Mastercard 3434 34** **** 343"),  # 15 цифр
        ("Mastercard 1234567890123456789", "Mastercard 1234 56** **** 3456 789"),  # 19 цифр
        ("Mastercard 4000123456789", "Mastercard 4000 12** **** 9"),  # 13 цифр
    ],
)
def test_mask_card(card_number, expected):
    """Проверка номера карты с: инт, стр, с буквами, с разной длиной карты, наличие "счет" """
    assert mask_account_card(card_number) == expected


def test_mask_card_invalid(invalid_card_number):
    """проверка неправильной длины"""
    for item in invalid_card_number:
        with pytest.raises(ValueError):
            mask_account_card(item)


@pytest.mark.parametrize(
    "date, expected",
    [
        ("2026-09-27T00:47:00Z", "2026.09.27"),
        ("2026-09-27", "2026.09.27"),
        ("2026-09-27T00:4dsf7sdf:00fdsfsdZ", "2026.09.27"),
    ],
)
def test_get_date(date, expected):
    assert get_date(date) == expected


@pytest.mark.parametrize(
    "date, expected",
    [
        ("2026-T00:47:00Z", "2026.09.27"),
        ("2026", "2026.09.27"),
        ("2026-0asdsad9-27T00:4dsf7sdf:00fdsfsdZ", "2026.09.27"),
    ],
)
def test_get_date_invalid(date, expected):
    with pytest.raises(ValueError):
        get_date(date)
