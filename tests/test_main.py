import src.main as main_module  # Импортируем сам модуль целиком
import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_dependencies(monkeypatch):
    """Фикстура для подмены внешних функций, чтобы не читать реальные файлы"""
    fake_transaction = {
        'id': 12345,
        'state': 'EXECUTED',
        'date': '2019-08-26T10:50:58.294041',
        'description': 'Перевод организации',
        'operationAmount': {'amount': '31957.58', 'currency': {'name': 'руб.', 'code': 'RUB'}}
    }
    fake_file_data = [fake_transaction]

    mock_financier = MagicMock(return_value=fake_file_data)
    mock_filter = MagicMock(return_value=fake_file_data)
    mock_sort = MagicMock(return_value=fake_file_data)
    mock_descriptions = MagicMock()
    mock_find = MagicMock(return_value=fake_file_data)
    mock_counter = MagicMock(return_value={"12345": 1})

    # Подменяем функции внутри импортированного модуля main_module
    monkeypatch.setattr(main_module, "financier_operation", mock_financier)
    monkeypatch.setattr(main_module, "filter_by_state", mock_filter)
    monkeypatch.setattr(main_module, "sort_by_date", mock_sort)
    monkeypatch.setattr(main_module, "transaction_descriptions", mock_descriptions)
    monkeypatch.setattr(main_module, "find_object", mock_find)
    monkeypatch.setattr(main_module, "counter_operations", mock_counter)

    return {
        "financier": mock_financier,
        "filter": mock_filter,
        "sort": mock_sort,
        "descriptions": mock_descriptions,
        "find": mock_find,
        "counter": mock_counter
    }


def test_main_success_flow(monkeypatch, capsys, mock_dependencies):
    inputs = iter(["1", "executed", "Нет", "нет", "Нет", "Нет"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Вызываем функцию через модуль
    main_module.main()

    captured = capsys.readouterr().out

    # Ищем строки, которые выводятся именно через print()
    assert "Программа: Операции отфильтрованы по статусу EXECUTED" in captured
    assert "Всего банковских операций по выборке: 1" in captured


def test_main_with_filters_and_sorting(monkeypatch, capsys, mock_dependencies):
    inputs = iter(["2", "CANCELED", "Да", "убыванию", "Да", "Да", "Перевод"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Вызываем функцию через модуль
    main_module.main()

    # Проверяем вызовы функций в соответствии с логикой main_Shit3c.py
    mock_dependencies["sort"].assert_called_once()
    mock_dependencies["descriptions"].assert_called_once_with(
        [{'id': 12345, 'state': 'EXECUTED', 'date': '2019-08-26T10:50:58.294041', 'description': 'Перевод организации',
          'operationAmount': {'amount': '31957.58', 'currency': {'name': 'руб.', 'code': 'RUB'}}}])
    mock_dependencies["find"].assert_called_once_with("Перевод")


def test_main_invalid_status_retry(monkeypatch, capsys, mock_dependencies):
    inputs = iter(["1", "INVALID", "PENDING", "Нет", "нет", "Нет", "Нет"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Вызываем функцию через модуль
    main_module.main()

    captured = capsys.readouterr().out
    assert "Статус INVALID не поддерживается, повторите ввод" in captured
