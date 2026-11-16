import time
from pprint import pprint

import src
from src.generators import transaction_descriptions
from src.processing import filter_by_state, sort_by_date
from src.external_api import financier_operation, find_object, counter_operations, transaction_to_currency

support_formates = ["EXECUTED", "CANCELED", "PENDING"]

error_status = False

def main():
    # --------------------------------------------------------------

    mods = (input('''Привет! Добро пожаловать в программу работы 
с банковскими транзакциями. 
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла'''))
    path = ""
    print(mods)
    if "1" in mods:
        path = "../data/operations.json"
    elif "2" in mods:
        path = "../data/transactions.csv"
    elif "3" in mods:
        path = "../data/transactions_excel.xlsx"

    src.external_api.path = path

    file = financier_operation() # [*]
    # print(file) # sdfg

    # --------------------------------------------------------------

    while True:
        filtered_formats = input(str(f'''Введите статус, по которому необходимо выполнить фильтрацию. 
    Доступные для фильтровки статусы: {", ".join(support_formates)}''')).upper()

        if filtered_formats in support_formates:
            print(filtered_formats) # sdf
            file = filter_by_state(file, filtered_formats)  # [*]
            break
        else:
            print(f"Статус {filtered_formats} не поддерживается, повторите ввод\n")

    if not file and error_status:
        raise ValueError(f"Пустой список: {file}")

    print(f"Программа: Операции отфильтрованы по статусу {filtered_formats}")

    # --------------------------------------------------------------

    data_status = input("Отсортировать операции по дате? Да/Нет")
    if data_status.lower() == "да":
        data_status = True
    else:
        data_status = False

    reverse = input("Отсортировать по возрастанию или по убыванию?")
    if reverse.lower() == "убыванию":
        reverse = True
    elif reverse.lower() == "возрастанию":
        reverse = False
    else:
        reverse = None

    currency = input("Выводить только рублевые транзакции? Да/Нет")
    if currency.lower() == "да":
        currency = True
    else:
        currency = False

    find = input('''Отфильтровать список транзакций по определенному слову 
в описании? Да/Нет''')
    if find.lower() == "да":
        find = input(str("Ведите слово"))
    else:
        find = False

    print("Распечатываю итоговый список транзакций...")

    # --------------------------------------------------------------

    if data_status:
        if not reverse:
            file = sort_by_date(file)
        else:
            file = sort_by_date(file, reverse=reverse)
    if currency:
        file = transaction_to_currency(file)
    if find:
        file = find_object(file, find, mode="values")

    # --------------------------------------------------------------

    print (file)
    if file:
        print("Распечатываю итоговый список транзакций...")
        counter = counter_operations(file, "id", mode=True)
        time.sleep(1)
        print(f"Всего банковских операций по выборке: {len(counter)}")
        for transaction in file:
            pprint(transaction, indent=4)
            print("-" * 75)
    else:
        print('''Программа: Не найдено ни одной транзакции, подходящей под ваши
условия фильтрации''')

