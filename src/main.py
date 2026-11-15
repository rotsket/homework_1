import time
from pprint import pprint

import src
from src.generators import transaction_descriptions
from src.processing import filter_by_state, sort_by_date
from src.external_api import financier_operation, find_object, counter_operations, transaction_to_currency

support_formates = ["EXECUTED", "CANCELED", "PENDING"]

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

    # if "2" in mods or "3" in mods:

    file = financier_operation() # [*]
    print(file) # sdfg

    # --------------------------------------------------------------

    filtered_formats = input(str(f'''Программа: Введите статус, по которому необходимо выполнить фильтрацию. 
Доступные для фильтровки статусы: {", ".join(support_formates)}'''))

    if filtered_formats in support_formates:
        print(filtered_formats) # sdf
        file_sorted = filter_by_state(file, filtered_formats)  # [*]
    else:
        raise ValueError(f"Фильтрация по {filtered_formats} недоступна.")



    print(f"Программа: Операции отфильтрованы по статусу {filtered_formats}")

    # --------------------------------------------------------------

    data_status = input("Отсортировать операции по дате? Да/Нет")
    if data_status.lower() == "да":
        data_status = True
    else:
        data_status = False

    reverse = input("Отсортировать по возрастанию или по убыванию?")
    if reverse.lower() == "да":
        reverse = True
    else:
        reverse = False

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
        sort_by_date(file_sorted, reverse=reverse)
    if currency:
        transaction_descriptions(file_sorted)
    if find:
        find_object(find)

    # --------------------------------------------------------------

    if file_sorted:
        print("Распечатываю итоговый список транзакций...")
        counter = counter_operations(file_sorted, "id")
        time.sleep(1)
        print(f"Всего банковских операций по выборке: {len(counter)}")
        pprint(file_sorted, indent=4)
    else:
        print('''Программа: Не найдено ни одной транзакции, подходящей под ваши
условия фильтрации''')





main()