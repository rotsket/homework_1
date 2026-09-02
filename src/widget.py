from src.masks import get_mask_card_number
from typing import Union

def mask_account_card(card_number: Union[str, int]) -> str:
    """ Функция которая умеет обрабатывать информацию как о картах, так и о счетах """
    card_account = []
    card_num = ""

    ### ЦИКЛ ЧТОБЫ ОТДЕЛИТЬ БУКВЫ(НАЗВАНИЕ КАРТЫ) ОТ ЦИФР(ЦИФРЫ КАРТЫ)
    for num_item in str(card_number).split(" "):
        if num_item.isalpha():
            card_account.append(num_item)
        else:
            card_num += num_item

    ### ПРОВЕРКА КОДА НА ПУСТУЮ СТРОКУ ИНАЧЕ ВЫВОДИМ ИМЯ КАРТЫ
    if not card_account:
        card_account = "Счет"
    else:
        card_account = " ".join(card_account)

    return str(f"{card_account} {get_mask_card_number(card_num)}")

if __name__ == "__main__":
    print(mask_account_card("7000792289606361"))