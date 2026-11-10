import pytest

from src.external_api import financier_operation, transaction_to_currency, get_transaction, CACHE, smart_file_loader
from tests.conftest import test_csv_file, test_xlsx_file
#                                Для csv, excel | Для обращения к апи | Это декоратор | Это кэш | Это умный загрузчик


import src.external_api


def test_financier_operation_with_xlsx(test_xlsx_file):
    # Подменяем глобальный путь на новый временный .xlsx файл
    src.external_api.path = str(test_xlsx_file)

    # Запускаем функцию
    result = src.external_api.financier_operation()

    # Проверяем, что эксель прочитался и распарсился в словарь по ID
    assert isinstance(result, dict)
    assert 3598919 in result
    assert result[3598919]['status'] == 'EXECUTED'
    assert result[593027]['amount'] == 30368

def test_financier_operation_with_csv(test_csv_file):
    # Подменяем глобальный путь на новый временный .xlsx файл
    src.external_api.path = str(test_csv_file)

    # Запускаем функцию
    result = src.external_api.financier_operation()

    # Проверяем, что эксель прочитался и распарсился в словарь по ID
    assert isinstance(result, dict)
    assert 3598919 in result
    assert result[3598919]['status'] == 'EXECUTED'
    assert result[593027]['amount'] == 30368