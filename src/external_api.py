from test_file import operations_data
from collections import Counter
import functools
import re
from pathlib import Path
import pandas as pd
import logging
import os
from functools import wraps
from typing import Any, Callable, ParamSpec, TypeVar, Union
import requests
from dotenv import load_dotenv
from src.utils import json_to_dict

FuncParams = ParamSpec("FuncParams")
FuncReturn = TypeVar("FuncReturn")


load_dotenv()
API_KEY = os.getenv('API_KEY')

path = ""
CACHE: dict = {}  # Здесь будут лежать абсолютно все валюты относительно рублю


def smart_file_loader(path_file):
    """ Умный загрузчик.
     Смотрит расширение файла и если он есть в условиях то возращает его обратно"""
    file_extension = Path(path_file).suffix
    if file_extension == ".csv":
        print("Обнаружен файл с расширением .csv")
        return pd.read_csv(path_file, sep=';',)
    elif file_extension == ".xlsx":
        print("Обнаружен файл с расширением .xlsx")
        return pd.read_excel(path_file)
    elif file_extension == ".json":
        print("Обнаружен файл с расширением .json")
        return json_to_dict(path_file)
    else:
        raise ValueError(f"Такой формат {file_extension} пока что не поддерживается")



def get_transaction(get_path: Callable) -> Callable:
    """ Прикольна """
    def my_decorator(func: Callable) -> Any | None:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:

                file_path = get_path()

                if file_path is None or str(file_path).strip().lower() == "none":
                    processed_file = None
                else:
                    processed_file = smart_file_loader(file_path)
                result = func(processed_file, *args, **kwargs)




                return result
            except Exception as e:
                print(f"{func.__name__} error: {e}. Inputs: {args}, {kwargs}")
                return None
        return wrapper
    return my_decorator

# Декоратор выше ↑↑↑ сделал чтоб можно было добавлять новые функции той что представлена ниже ↓↓↓
@get_transaction(get_path=lambda: path)
def transaction_to_currency(processed_file: Any, currency: tuple = ("USD", "EUR"), base_currency : str = "RUB") -> list[float]:
    """Кидает запрос на сайт https://api.apilayer.com с актуальной информацией о курсе валют относительна base_currency"""
    result = []

    base = base_currency

    global CACHE

    if not CACHE:
        try:
            url = f"https://api.apilayer.com/exchangerates_data/latest?base={base}"
            headers: dict = {'apikey': API_KEY}
            response = requests.get(url, headers=headers)
            get_actual_rates = response.json()

            if "rates" in get_actual_rates:
                CACHE = get_actual_rates["rates"]
            print(
                "CACHE <-- кэш сохранен и обращение к api совершенно только один раз"
            ) # Если это вылезет много раз то будет хреново очень
        except requests.RequestException as e:
            print(f"Сетевая ошибка: {e}")
        except Exception as e:
            print(f"Ошибка при запросе к API {e}")

    rates = CACHE

    for trans in processed_file:
        if not trans or "operationAmount" not in trans or "currency" not in trans["operationAmount"]:
            result.append(0)
            continue
        currency_code = trans["operationAmount"]["currency"]["code"]
        operation_amount = trans.get("operationAmount", {})  # Бяка битая строка не пройдет
        amount = float(operation_amount.get("amount", 0))

        if currency_code == base: # Точнее ето base_currency вместо base, но пофиг
                    # Если транзакция уже в RUB, конвертировать не нужно
                    result.append(amount)

        elif currency_code in currency and currency_code in rates:      # amount_in_base_currency это валюта                         0w0
                amount_in_base_currency = amount / rates[currency_code] # из которой мы хотели конвертировать: base_currency: str = "RUB"
                result.append(float(round(amount_in_base_currency, 2))) # Округляем после 2 запятых
        else:
                result.append(amount)

    return result

@get_transaction(get_path=lambda: path)
def financier_operation(processed_file: Any, ) -> Any:
    """Конвертирует .csv .xlsx .json и ему подобные в список словарей"""
    ext = Path(path).suffix
    result = []
    if ext == ".csv":
        for index, row in processed_file.iterrows():
            row_to_dict = row.to_dict()
            result.append(row_to_dict)          # result[row_to_dict['id']] = row_to_dict
    elif ext == ".xlsx": # Я боялся что нужно будет применять другой метод для .xlsx, но вроде все нормально
        for index, row in processed_file.iterrows():
            row_to_dict = row.to_dict()
            result.append(row_to_dict)          # result[row_to_dict['id']] = row_to_dict
    elif ext == ".json":
        for item in processed_file:
            if 'id' in item:
                result.append(item)     # result[item['id']] = item
    else:
        raise ValueError(f"Такой формат {ext} пока что не поддерживается")
    return result


@get_transaction(get_path=lambda: "none")
def find_object(processed_file: Any , data: list[dict] | dict, search: str, mode="Any") -> list[dict]: # Заглушка processed_file
    """ Получает словари и находит объект, указанный вторым аргументом """
    result = []

    if isinstance(data, dict):
        data = list(data.values())
    elif not isinstance(data, list):
        raise TypeError(f"Функция ожидает list или dict, но получен тип: {type(data).__name__}")

    pattern = re.compile(rf'{re.escape(search)}', flags=re.IGNORECASE)
    if mode.lower() == "values":
        for item in data:
            for value in item.values():
                if value and pattern.search(str(value)):
                    result.append(item)
                    break
    elif mode.lower() == "key":
        for item in data:
            for key in item.keys():
                if pattern.search(str(key)):
                    result.append(item)
                    break
    else:
        for item in data:
            for key, value in item.items():
                if pattern.search(str(key)) or pattern.search(str(value)):
                    result.append(item)
                    break
    return result

@get_transaction(get_path=lambda: "none")
def counter_operations(processed_file, data:list[dict], categories:str, mode: bool = False) -> list[dict] | dict: # Заглушка processed_file
    """Функция ищет кол - во событий по descriptions.
    Если задать mode = True, то мы начинаем считать кол - во значений в ключе"""
    categories_lower = {categories.lower()} if isinstance(categories, str) else {str(cat).lower() for cat in categories}
    categories_set = set(categories_lower) if isinstance(categories_lower, list) else set(categories_lower)

    if mode: # Этот блок проходится по ключам и считает их значения
        descriptions = [x.get(categories) for x in data if categories in x]
        result = Counter(descriptions)
        return result

    else: # Этот блок проходится по значения в ключе description
        descriptions = [transaction.get('description') for transaction in data
                        if transaction.get('description')
                        and str(transaction.get('description')).lower() in categories_set
                        ]
        return Counter(descriptions)



# if __name__ == "__main__":
#     products = [
#         {"id": 101, "name": "Смартфон Alpha X", "category": "Смартфоны", "price": 45000, "in_stock": True,
#          "rating": 4.7},
#         {"id": 102, "name": "Ноутбук ProBook 15", "category": "Ноутбуки", "price": 85000, "in_stock": False,
#          "rating": 4.5},
#         {"id": 103, "name": "Беспроводные наушники AirSound", "category": "Аксессуары", "price": 7500, "in_stock": True,
#          "rating": 4.2},
#         {"id": 104, "name": "Умные часы Chrono V2", "category": "Аксессуары", "price": 12000, "in_stock": True,
#          "rating": 3.9},
#         {"id": 105, "name": "Смартфон Beta Lite", "category": "Смартфоны", "price": 23000, "in_stock": True,
#          "rating": 4.1},
#         {"id": 106, "name": "Планшет Tab Ultra", "category": "Планшеты", "price": 54000, "in_stock": False,
#          "rating": 4.6},
#         {"id": 107, "name": "Игровой монитор Vision 27", "category": "Мониторы", "price": 31000, "in_stock": True,
#          "rating": 4.8},
#     ]
#     path = "../data/transactions_excel.xlsx"
#
#     result1 = find_object(products, "Планшет")
#     print(result1)


# if __name__ == "__main__":
#     # Было: path = "data/operations.json"
#     # Меняем на:
#     path = "../data/transactions_excel.xlsx"
#
#     lists = financier_operation()
#     result1 = find_object(lists, "Счет 53688013223998817599")
#     print(lists)


if __name__ == "__main__":
    path = "../data/operations.json"
    result2 = transaction_to_currency()
    print(result2)


#mount = 5
#from_ = "EUR"
#to = "USD"
#url = f"https://api.apilayer.com/exchangerates_data/convert?to={to}&from={from_}&amount={amount}"
#headers = {'apikey': API_KEY}
#response = requests.get(url, headers=headers)
#print(response.json())

# = trans["operationAmount"]["amount"]
     #       from_ = trans["currency"]["code"]
       #     to = "RUB"
# f"https://api.apilayer.com/exchangerates_data/latest?{symbols}=symbols&base={base}"
