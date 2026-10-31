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

def get_transaction(get_path: Callable[[], Union[str, None]]) -> Callable[FuncParams, FuncReturn]:
    """ Прикольна """
    def my_decorator(func) -> Any | None:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                path_to_file = get_path()
                if not path_to_file:
                    raise FileNotFoundError
                transaction = json_to_dict(path_to_file)
                kwargs['transaction'] = transaction
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                print(f"{func.__name__} error: {e}. Inputs: {args}, {kwargs}")
                return None
        return wrapper
    return my_decorator

# Декоратор выше ↑↑↑ сделал чтоб можно было добавлять новые функции той что представлена ниже ↓↓↓
@get_transaction(get_path=lambda: path)
def transaction_to_currency(transaction: list, currency: tuple = ("USD", "EUR"), base_currency : str = "RUB") -> list[float | int | None]:
    result=[
        # Здесь будет результат, который возвращается листом с int и float
    ]
    set_currency = set()
    for trans in transaction:
        if trans and "operationAmount" in trans and "currency" in trans["operationAmount"]:
            set_currency.add(trans["operationAmount"]["currency"]["code"])

    base = base_currency

    if base_currency in set_currency:
        set_currency.remove(base)

    symbols = ",".join(set_currency)

    if not symbols:
        return [float(trans["operationAmount"]["amount"]) for trans in transaction if trans and "operationAmount" in trans]


    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbols}&base={base}"
    headers = {'apikey': API_KEY}

    try:
        response = requests.get(url, headers=headers)
        get_actual_rates = response.json()

        if "rates" not in get_actual_rates:
            print(f"Ошибка связанная с API: {get_actual_rates}")
            return [float(trans["operationAmount"]["amount"]) for trans in transaction]

        rates = get_actual_rates["rates"]

    except Exception as e:
        print(f"Ошибка при запросе к API {e}")
        return [float(trans["operationAmount"]["amount"]) for trans in transaction]

    for trans in transaction:
        if not trans or "operationAmount" not in trans or "currency" not in trans["operationAmount"]:
            continue

        currency_code = trans["operationAmount"]["currency"]["code"]
        amount = float(trans["operationAmount"]["amount"])

        if currency_code == base: # Точнее ето base_currency вместо base, но пофиг
                # Если транзакция уже в RUB, конвертировать не нужно
                result.append(amount)

        elif currency_code in currency and currency_code in rates:
            # здесь была какаято строка бухехе                      # amount_in_base_currency это валюта                          0w0
            amount_in_base_currency = amount / rates[currency_code] # из которой мы хотели конвертировать: base_currency : str = "RUB"
            result.append(round(amount_in_base_currency, 2)) # Округляем после 2 запятых

        else:
            result.append(amount)

    return result


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