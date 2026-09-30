from typing import Union, Generator

def filter_by_currency(transaction : list, curency : str) -> list:
    filtered_list = list()
    for item in transaction:
        try:
            operation_amount = item.get("operationAmount", {})
            currency_info = operation_amount.get("currency", {})

            # Проверяем финальную строчку кода валюты
            if currency_info.get("code") == curency:
                filtered_list.append(item)

        except AttributeError:
            continue

    return filtered_list


def card_number_generator(range_1 : Union[int,str], range_2 : Union[int,str],length : Union[int,str] = 16) -> Generator[str, None, None]:
    length = int(length)
    starts = int(range_1)
    end = int(range_2)

    for start in range(starts, end + 1):
        raw_card_str = f"{start:0{length}d}"
        card_number = list()
        countdown = 0
        for item in raw_card_str:
            countdown += 1
            card_number.append(item)
            if countdown == 4:
                card_number += " "
                countdown = 0

        edit_card_number = "".join(card_number).strip()

        yield edit_card_number
