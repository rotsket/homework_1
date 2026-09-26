from typing import Union

from src.masks import get_mask_account, get_mask_card_number

from datetime import datetime


def mask_account_card(card_number: Union[str, int]) -> str:
    """Функция, которая умеет обрабатывать информацию как о картах, так и о счетах"""
    card_account = []
    card_num = ""

    # ЦИКЛ, ЧТОБЫ ОТДЕЛИТЬ БУКВЫ(НАЗВАНИЕ КАРТЫ) ОТ ЦИФР(ЦИФРЫ КАРТЫ)
    for num_item in str(card_number).split(" "):
        if num_item.isalpha():
            card_account.append(num_item)
        else:
            card_num += num_item

    mask_card = get_mask_card_number(
        card_num, reverse=False
    )  # Маскируем карту с помощью функции, передаем reverse=True, чтобы изменить порядок шифровки
    str_card_account = " ".join(card_account)

    # ПРОВЕРКА КОДА  НА ПУСТУЮ СТРОКУ ТО "Карта"  ЛИБО НА НАЛИЧИЕ "Счет"  ИНАЧЕ card_account
    if not card_account:
        card_account.append("Карта")
    if "Счет" in card_account or "счет" in card_account:
        mask_card = get_mask_account(card_num)
    else:
        str_card_account = " ".join(card_account)

    return str(f"{str_card_account} {mask_card}")


def get_date(date_str: str) -> str:
    """Преобразует формат даты через срезы строк."""
    correct_date = date_str[:10]

    item_date = correct_date.split("-")

    if len(item_date) == 3 and all(p.isdigit() for p in item_date):
        year, month, day = item_date
        return f"{year}.{month}.{day}"
    else:
        raise ValueError("Введенный формат не подходит")
