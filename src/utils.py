import json
import logging
from pathlib import Path

# Вычисляем путь к папке logs
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# --- Логер модуля utils ---
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOG_DIR / "utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def json_to_dict(file_path: str) -> list[dict]:
    if not file_path.endswith(".json"):
        logger.error("Файл не имеет расширения .json: %s", file_path)
        return []

    logger.info("Чтение JSON из файла: %s", file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            operations = json.load(f)

            if isinstance(operations, list):
                logger.debug("Успешно прочитано записей: %d", len(operations))
                return operations

            logger.error("JSON не является списком: %s", file_path)
            return []

    except FileNotFoundError:
        logger.error("Файл не найден: %s", file_path)
        return []

    except json.JSONDecodeError as e:
        logger.error("Ошибка парсинга JSON в %s: %s", file_path, e)
        return []










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