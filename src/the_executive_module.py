import csv
import itertools
import json
import logging
import os.path
import re
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

main_path = Path(__file__).resolve().parents[1]

logger = logging.getLogger('__name__')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(f'{main_path}/logs/executive_modul.log', 'w', encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s %(funcName)s %(lineno)d: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def read_transactions_data(file_name: str) -> list[dict | str]:
    """Функция чтения и подготовки данных по типу файла данных"""
    logger.info(f"Старт. Выбран файл {file_name}")
    file_path = os.path.join(main_path, "data", file_name)
    loaded_data = []
    if os.path.exists(file_path) and os.stat(file_path).st_size != 0:
        with open(file_path, encoding="utf-8") as f:
            if re.search(r"\b\w+\.json\b", file_name):
                json_data = json.load(f)
                if isinstance(json_data, list) and len(json_data) != 0:
                    prima_data = json_data
                    for i in prima_data:
                        if isinstance(i, dict) and len(i) != 0:
                            i["amount"] = i.get('operationAmount').get('amount', "")
                            i["currency_name"] = i.get('operationAmount').get('currency').get('name', "")
                            i["currency_code"] = i.get('operationAmount').get('currency').get('code', "")
                            i.pop('operationAmount')
                        else:
                            continue
                    logger.info("JSON считан, преобразован")
                else:
                    logger.info("Данных в формате list[dict] в JSON файле отсутствуют")

            elif re.search(r"\b\w+\.csv\b", file_name):
                prima_data = []
                for row in csv.DictReader(f, delimiter=';'):
                    prima_data.append(row)
                logger.info("CSV считан, преобразован")

            elif re.search(r"\b\w+\.xlsx\b", file_name):
                prima_data = []
                readed_data = pd.read_excel(file_path, sheet_name=0, header=0, index_col=None, na_values=['', ' '],
                                            keep_default_na=False, na_filter=True)
                transform_data = readed_data.to_dict('index')
                for i in transform_data:
                    prima_data.append(transform_data[i])
                logger.info("XLSX считан, преобразован")
            for i in prima_data:
                if isinstance(i, dict) and len(i) != 0:
                    for key, value in i.items():
                        if type(value) is float and value is np.nan or value == " " or value == "":
                            i[key] = ""
                    if i.get("id") and i.get("state") and i.get("date") and i.get("to") and i.get("description") != "":
                        loaded_data.append(i)
                    else:
                        continue
            logger.info("Данные возвращены. Функция завершена")
            return loaded_data if len(loaded_data) != 0 else exit(
                "Выбранный файл отсутствует или не содержит необходимой информациии.\nРабота программы завершена.")
    else:
        exit("Выбранный файл отсутствует или не содержит необходимой информациии.\nРабота программы завершена.")


def filter_by_status(loaded_data: list | dict, search_line: str) -> list[dict]:
    """Функция фильтрации данных по статусу "EXECUTED", "CANCELED", "PENDING" """
    filtered_data = []
    logger.info("Старт")
    for i in range(0, len(loaded_data)):
        try:
            x = loaded_data[i]["state"]
            if re.search(search_line, x):
                filtered_data.append(loaded_data[i])
        except Exception as ex:
            logger.error(f"ОШИБКА: {ex}- {loaded_data[i]}, тип словаря: {type(loaded_data[i])}, "
                         f"Длина словаря: {len(loaded_data[i])}. Продолжаем")
            continue
    if len(filtered_data) == 0:
        logger.info(f"Данных со статусом {search_line} не обнаружено.")
        exit(f"Данных со статусом {search_line} не обнаружено.\nРабота программы завершена.")
    else:
        logger.info(f"Операции отфильтрованы по статусу {search_line} и возвращены. Функция завершена.")
        print("Операции отфильтрованы по статусу", ''.join(search_line))
    return filtered_data


def filter_by_description(transactions_by_status: list[dict], search_line: str) -> list[dict]:
    """Функция фильтрации данных по типу "description" """
    filtered_data = []
    logger.info("Старт")
    for i in range(0, len(transactions_by_status)):
        try:
            x = transactions_by_status[i]["description"]
            if re.search(search_line, x):
                filtered_data.append(transactions_by_status[i])
        except Exception as ex:
            logger.error(f"ОШИБКА: {ex}- {transactions_by_status[i]}, тип словаря: {type(transactions_by_status[i])}, "
                         f"Длина словаря: {len(transactions_by_status[i])}. Продолжаем")
            continue
    if len(filtered_data) == 0:
        logger.info(f"Данных со статусом {search_line} не обнаружено.")
        exit(f"Транзакции типа {search_line} отсутствуют.\nРабота программы завершена.")
    else:
        logger.info(f"Операции отфильтрованы по типу {search_line} и возвращены. Функция завершена.")
        print("Операции отфильтрованы по типу", ''.join(search_line))
    return filtered_data


def final_calculation(transactions_by_description: list[dict], choice: dict) -> any:
    """Функция окончательной сортировки и подсчёта типа транзакций"""
    filtered_df = None
    count_category = None
    df = pd.DataFrame(transactions_by_description)
    if len(choice) != 0:
        title = list(itertools.islice(choice.keys(), 1))
        filter_1 = df[title[0]] == choice[title[0]]
        filtered_df = df[filter_1]
        count_category = Counter(filtered_df[title[0]])
    filtered_transactions = filtered_df.to_dict("records")
    logger.info(f"Функция final_calculation выполнена {filtered_transactions}, {count_category}")
    if len(filtered_transactions) == 0:
        exit("Даные по выбранным критериям не обнаружены.\nРабота программы завершена.")
    return filtered_transactions, count_category
