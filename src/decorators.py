from functools import wraps
import sys
from typing import Union, Callable, TypeVar, ParamSpec


FuncParams = ParamSpec("FuncParams")
FuncReturn = TypeVar("FuncReturn")


def logging(file_name: Union[str, None] = None) -> Callable[[Callable[FuncParams, FuncReturn]], Callable[FuncParams, FuncReturn]]:
    """Декоратор с логами для учета результатов и ошибок"""
    def my_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            try:
                output = f"Вызов функции {func.__name__}\n"
                result = func(*args, **kwargs)
                output += f"{func.__name__} Результат {result}"

                if file_name:
                    with open(file_name, "a", encoding="utf-8") as file:
                        file.write(output)
                else:
                    sys.stdout.write(output)
                return result


            except Exception as e:
                error_output = f"{func.__name__} error: {e}. Inputs: {args}, {kwargs}\n"
                if file_name:
                    with open(file_name, "a", encoding="utf-8") as file:
                        file.write(error_output)
                else:
                    sys.stdout.write(error_output)

                raise e

        return wrapper
    return my_decorator


