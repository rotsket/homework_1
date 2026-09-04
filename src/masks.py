import re
from typing import Union


def get_mask_card_number(card_number: Union[int, str], reverse: bool = True) -> str:
    """частично маскирует номер карты примерно: **** **XX XXXX **** Если reverse True XXXX XX** **** XXXX"""
    correct_card_number = re.sub(r"[a-zA-Zа-яА-Я]", "", str(card_number).replace(" ", ""))
    countdown = 0
    mask_number = ""

    if len(correct_card_number) < 16:
        return "Введен некорректный номер карты"

    for item in correct_card_number:
        countdown += 1
        mask_number += "*" if reverse else item  # Если reverse=True то зездочка иначе цифру
        if countdown == 4:
            mask_number += " "
            countdown = 0

    mask_number_list = list(mask_number.strip())

    # Расшифроваем часть карты если reverse False, иначе наоборот зашифроваем
    if reverse:
        mask_number_list[7] = correct_card_number[6]  # X
        mask_number_list[8] = correct_card_number[7]  # X
        mask_number_list[10] = correct_card_number[8]  # X
        mask_number_list[11] = correct_card_number[9]  # X
        mask_number_list[12] = correct_card_number[10]  # X
        mask_number_list[13] = correct_card_number[11]  # X
    else:
        mask_number_list[7] = "*"
        mask_number_list[8] = "*"
        mask_number_list[10] = "*"
        mask_number_list[11] = "*"
        mask_number_list[12] = "*"
        mask_number_list[13] = "*"

    return "".join(mask_number_list)


def get_mask_account(card_number: Union[int, str]) -> str:
    """оставляет последние четыре цифры карты -> **XXXX"""
    correct_card_number = re.sub(r"[a-zA-Zа-яА-Я]", "", str(card_number).replace(" ", ""))
    last_four = correct_card_number[-4:]
    return f"**{last_four}"
