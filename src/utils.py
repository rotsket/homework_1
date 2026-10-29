import requests

import json


def json_to_dict(file_path : str) -> dict:
    try:
        with open(file_path , 'r', encoding="utf-8") as f:
            operations = json.load(f)
            return operations
    except (FileNotFoundError, json.JSONDecodeError):
        return {}











    # try:
    #     response = request
    #     with open(site) as json_file:
    #         try:
    #             currency_data = json.load(json_file)
    #         except json.decoder.JSONDecodeError:
    #             print("Ошибка обработки данных")
    # except FileNotFoundError:
    #     print("Ф айл не найден")
    #
    #
    #
    # return False