from src.external_api import financier_operation
from test_file import operations_data
from typing import Any


def filter_by_state(data_list: list[dict[str, Any]], states: str = "EXECUTED") -> list[dict[str, Any]]:
    """Принимает список словарей и опционально значение для ключа state"""
    new_list = []




    items_to_filter = data_list.values() if isinstance(data_list, dict) else data_list


    for item in items_to_filter:
        if not isinstance(item, dict):
            continue

        if item.get("state") == states:
            new_list.append(item)

    return new_list


def sort_by_date(data_list: list[dict[str, Any]], reverse: bool = True) -> list[dict[str, Any]]:
    """Принимает список словарей и необязательный параметр, задающий порядок сортировки"""
    return sorted(data_list, key=lambda x: x.get("date", ""), reverse=reverse)


if __name__ == "__main__":
    print (filter_by_state(operations_data, "EXECUTED"))