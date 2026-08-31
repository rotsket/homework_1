def get_mask_card_number(card_number: int) -> str:
    """частично маскирует номер карты примерно: **** **XX XXXX ****"""
    correct_card_number = str(card_number).replace(" ", "")
    countdown = 0
    mask_number = ""

    if card_number <= 16:
        return "Введен неккоректный номер карты"

    for item in correct_card_number:
        countdown += 1
        mask_number += "*"
        if countdown == 4:
            mask_number += " "
            countdown = 0

    mask_number_list = list(mask_number.strip())

    # Расшифроваем часть карты
    mask_number_list[7] = correct_card_number[6]    # X
    mask_number_list[8] = correct_card_number[7]    # X
    mask_number_list[10] = correct_card_number[8]   # X
    mask_number_list[11] = correct_card_number[9]   # X
    mask_number_list[12] = correct_card_number[10]  # X
    mask_number_list[13] = correct_card_number[11]  # X

    return "".join(mask_number_list)


def get_mask_account(card_number: int) -> str:
    """оставляет последние четыре цифры карты -> **XXXX"""
    card_str = str(card_number)
    last_four = card_str[-4:]
    return f"**{last_four}"
