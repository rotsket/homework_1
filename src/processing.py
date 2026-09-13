def filter_by_state(list: list, states: str = "EXECUTED") -> list:
    """Принимает список словарей и опционально значение для ключа state"""
    new_list = []

    for item in list:
        if item.get("state") == states:
            new_list.append(item)

    return new_list


def sort_by_date(list: list, reverse: bool = True) -> list:
    """Принимает список словарей и необязательный параметр, задающий порядок сортировки"""
    return sorted(list, key=lambda x: x["date"], reverse=reverse)
