import functools
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

                if not file_path:
                    raise FileNotFoundError




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
def financier_operation(processed_file: Any, ):
    """Конвертирует .csv .xlsx и ему подобные в список словарей"""
    ext = Path(path).suffix
    result = {}
    if ext == ".csv":
        for index, row in processed_file.iterrows():
            row_to_dict = row.to_dict()
            result[row_to_dict['id']] = row_to_dict
    elif ext == ".xlsx": # Я боялся что нужно будет применять другой метод для .xlsx но вроде все нормально
        for index, row in processed_file.iterrows():
            row_to_dict = row.to_dict()
            result[row_to_dict['id']] = row_to_dict
    return result


if __name__ == "__main__":
    # Было: path = "data/operations.json"
    # Меняем на:
    path = "../data/transactions_excel.xlsx"

    result1 = financier_operation()
    print(result1)



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
