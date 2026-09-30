import pytest

from src.generators import filter_by_currency


@pytest.mark.parametrize("cash, expected", [
    ("USD", {
  "id": 939719570,
  "state": "EXECUTED",
  "date": "2018-06-30T02:08:58.425572",
  "operationAmount": {
    "amount": 9824.07,
    "currency": {
      "name": "USD",
      "code": "USD"
    }
  },
  "description": "Перевод организации",
  "from": "Счет 75106830613657916952",
  "to": "Счет 11776614605963066702"
}
     ),   # Первый тест

    ("CANCELED", {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }
     ),   # Второй тест

])
def test_filter_by_currency(transaction, cash, expected):
    assert filter_by_currency(transaction, cash) == expected