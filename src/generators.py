def filter_by_currency(transaction : list, curency : str) -> list:
    filtered_list = list()
    for item in transaction:
        try:
            if item.get("operationAmount", {}).get("currency", {}).get("code", {}) == curency:  # Путь до валюты
                filtered_list.append(item)

        except AttributeError:
            continue

    return filtered_list