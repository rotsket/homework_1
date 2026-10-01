from typing import Any


def filter_by_state(data_list: list[dict[str, Any]], states: str = "EXECUTED") -> list[dict[str, Any]]:
    """Принимает список словарей и опционально значение для ключа state"""
    new_list = []

    for item in data_list:
        if item.get("state") == states:
            new_list.append(item)

    return new_list


def sort_by_date(data_list: list[dict[str, Any]], reverse: bool = True) -> list[dict[str, Any]]:
    """Принимает список словарей и необязательный параметр, задающий порядок сортировки"""
    return sorted(data_list, key=lambda x: x.get("date", ""), reverse=reverse)
