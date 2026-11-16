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




    """ Прикольна """
def get_transaction(func: Callable) -> Any | None:
    @wraps(func)
    def wrapper(get_path, *args: Any, **kwargs: Any) -> Any:
        try:


            if get_path is None or str(get_path).strip().lower() == "none":
                processed_file = None
            else:
                processed_file = smart_file_loader(get_path)
            result = func(processed_file, *args, **kwargs)

            return result
        except Exception as e:
            print(f"{func.__name__} error: {e}. Inputs: {args}, {kwargs}")
            return None
    return wrapper


# Декоратор выше ↑↑↑ сделал чтоб можно было добавлять новые функции той что представлена ниже ↓↓↓
@get_transaction
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

@get_transaction
def financier_operation(processed_file: Any, ):
    """Конвертирует .csv .xlsx и ему подобные в список словарей"""
    result = {}

    for index, row in processed_file.iterrows():
        row_to_dict = row.to_dict()
        result[row_to_dict['id']] = row_to_dict

    return result


@get_transaction
def find_object(processed_file: Any , data: list[dict] | dict, search: str) -> list[dict]: # Заглушка processed_file
    """ Получает словари и находит объект, указанный вторым аргументом """
    result = []

    if isinstance(data, dict):
        data_list = list(data.values())
    elif isinstance(data, list):
        data_list = data
    else:
        raise TypeError(f"Функция ожидает list или dict, но получен тип: {type(data).__name__}")

    pattern = re.compile(rf'\b{re.escape(search)}\b', re.IGNORECASE )
    for item in data_list:
        for key, value in item.items():
            if pattern.search(str(key)) or pattern.search(str(value)):
                result.append(item)
                break
    return result

@get_transaction
def counter_operations(processed_file, data:list[dict], categories:list) -> list[dict] | dict: # Заглушка processed_file
    descriptions = [x.get(categories, "id") for x in data if categories in x]
    result = Counter(descriptions)
    return result
