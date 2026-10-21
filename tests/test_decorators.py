import os

import pytest

from src.decorators import logging

# --------------------------------------


@logging()
def add(x, y):
    return x + y


@logging(file_name="test_log.txt")
def add_file(x, y):
    return x + y


# Функции со сложением -------------------


@logging()
def divide(x, y):
    return x / y


@logging(file_name="test_error_log.txt")
def divide_file(x, y):
    return x / y


# Функции с делением --------------------


def test_logging_add(capsys):
    result = add(1, 2)
    assert result == 3

    captured = capsys.readouterr()

    assert "Вызов функции add" in captured.out
    assert "add Результат 3" in captured.out


def test_logging_add_file():
    if os.path.exists("test_log.txt"):
        os.remove("test_log.txt")

    with pytest.raises(TypeError):
        add_file(1, "2124")

    with open("test_log.txt", "r", encoding="utf-8") as file:
        log = file.read()

    assert "add_file error:" in log
    assert "Inputs: (1, '2124'), {}" in log

    os.remove("test_log.txt")


# Тесты со сложением ---------------------


def test_logging_divide(capsys):
    result = divide(10, 5)
    assert result == 2

    captured = capsys.readouterr()

    assert "Вызов функции divide" in captured.out
    assert "divide Результат 2" in captured.out


def test_logging_divide_file():
    if os.path.exists("test_error_log.txt"):
        os.remove("test_error_log.txt")

    with pytest.raises(TypeError):
        divide_file(1, "231")
    with pytest.raises(ZeroDivisionError):
        divide_file(1, 0)

    with open("test_error_log.txt", "r", encoding="utf-8") as file:
        log = file.read()

    assert "divide_file error:" in log
    assert "Inputs: (1, '231'), {}" in log

    os.remove("test_error_log.txt")


# Тесты с делением ------------------------
