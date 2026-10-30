import functools
import os

import requests
from dotenv import load_dotenv

from src.utils import json_to_dict

from functools import wraps

from typing import Callable, Generator, Union, Any, ParamSpec, TypeVar

FuncParams = ParamSpec("FuncParams")
FuncReturn = TypeVar("FuncReturn")

# Приколюха чтоб json_to_dict понимал откуда ему брать данные
# иначе ниче не вернет

load_dotenv()
path = ""
API_KEY = os.getenv('API_KEY')

def get_transaction(get_path: Union[str, None] = None) -> Callable[FuncParams, FuncReturn]:
    """ Прикольна """
    def my_decorator(func) -> Any | None:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                path_to_file = get_path
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

@get_transaction(get_path=lambda: path) # type: ignore[arg-type]
def transaction_to_currency(currency: str, transaction: dict) -> list[float | int | None]:
    result=[
        # Здесь будет результат, который возвращается листом с int и float
    ]
    get_actual_currency = []
    set_currency = set()
    for trans in transaction:
        set_currency.add(trans["currency"]["code"])

    symbols = "RUB"
    base = list(set_currency)

    url = f"https://api.apilayer.com/exchangerates_data/latest?{symbols}=symbols&base={base}"
    headers = {'apikey': API_KEY}

    response = requests.get(url, headers=headers)

    get_actual_currency.append(response)

    for trans in transaction:
        currency_code = trans["operationAmount"]["currency"]["code"]
        amount = trans["operationAmount"]["amount"]
        if currency_code in ("USD", "EUR"):
            amount = trans["operationAmount"]["amount"]
            rate = get_actual_currency["rates"][currency_code]
            result.append(amount / rate)

        else:
            result.append(amount)
    return result


path = "data/operations.json"
result = transaction_to_currency()
print(result)












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
