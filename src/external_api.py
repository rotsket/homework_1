import functools
import os
from functools import wraps
from typing import Any, Callable, ParamSpec, TypeVar, Union
import requests
from dotenv import load_dotenv
from src.utils import json_to_dict

FuncParams = ParamSpec("FuncParams")
FuncReturn = TypeVar("FuncReturn")

# Приколюха чтоб json_to_dict понимал откуда ему брать данные
# иначе ниче не вернет

load_dotenv()
API_KEY = os.getenv('API_KEY')

path = ""
CACHE = {}  # Здесь будут лежать абсолютно все валюты относительно рублю

def get_transaction(get_path: Callable[[], Union[str, None]]) -> Callable[FuncParams, FuncReturn]:
    """ Прикольна """
    def my_decorator(func) -> Any | None:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = [
                    # Сюда перенес перебор транзакций и по одному отправляю каждую транзакцию
                ]
                path_to_file = get_path()
                if not path_to_file:
                    raise FileNotFoundError
                transaction_or_interpreter = json_to_dict(path_to_file) # Потом можно сделать функцию, которая проверяет
                for trans in transaction_or_interpreter:                # Какие инструменты нужно применять
                    # По очереди передаем каждый словарь в функцию
                    res = func(trans, *args, **kwargs)
                    result.append(res)
                return result
            except Exception as e:
                print(f"{func.__name__} error: {e}. Inputs: {args}, {kwargs}")
                return None
        return wrapper
    return my_decorator

# Декоратор выше ↑↑↑ сделал чтоб можно было добавлять новые функции той что представлена ниже ↓↓↓
@get_transaction(get_path=lambda: path)
def transaction_to_currency(trans: dict, currency: tuple = ("USD", "EUR"), base_currency : str = "RUB") -> float:
    if not trans or "operationAmount" not in trans or "currency" not in trans["operationAmount"]:
            return 0.0

    currency_code = trans["operationAmount"]["currency"]["code"]

    operation_amount = trans.get("operationAmount", {}) # Бяка битая строка не пройдет
    amount = float(operation_amount.get("amount", 0))


    base = base_currency

    global CACHE

    if not CACHE:
        try:
            url = f"https://api.apilayer.com/exchangerates_data/latest?base={base}"
            headers = {'apikey': API_KEY}

            response = requests.get(url, headers=headers)
            get_actual_rates = response.json()

            if "rates" not in get_actual_rates:
                print(f"Ошибка связанная с API: {get_actual_rates}")
                return amount

            CACHE = get_actual_rates["rates"]
            print(
                "CACHE <-- кэш сохранен и обращение к api совершенно только один раз"
            ) # Если это вылезет много раз то будет хреново очень

        except Exception as e:
            print(f"Ошибка при запросе к API {e}")
            return amount

    rates = CACHE

    if currency_code == base: # Точнее ето base_currency вместо base, но пофиг
                # Если транзакция уже в RUB, конвертировать не нужно
                return amount

    elif currency_code in currency and currency_code in rates:      # amount_in_base_currency это валюта                          0w0
            amount_in_base_currency = amount / rates[currency_code] # из которой мы хотели конвертировать: base_currency : str = "RUB"
            return round(amount_in_base_currency, 2) # Округляем после 2 запятых

    else:
            return amount


if __name__ == "__main__":
    # Было: path = "data/operations.json"
    # Меняем на:
    path = "../data/operations.json"

    result1 = transaction_to_currency()
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


