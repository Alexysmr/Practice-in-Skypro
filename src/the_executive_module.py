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


def read_transactions_data(file_name: str) -> dict | str:
    """Функция получения и подготовки данных по типу файла данных"""
    logger.info(f"Старт. Выбран файл {file_name}")
    file_path = os.path.join(main_path, "data", file_name)
    if os.path.exists(file_path) and os.stat(file_path).st_size != 0:
        with open(file_path, encoding="utf-8") as f:
            if re.search(r"\b\w+\.json\b", file_name):
                json_data = json.load(f)
                if isinstance(json_data, list):
                    loaded_data = json_data
                    for i in loaded_data:
                        if len(i) != 0:
                            i["amount"] = i.get('operationAmount').get('amount', "")
                            i["currency_name"] = i.get('operationAmount').get('currency').get('name', "")
                            i["currency_code"] = i.get('operationAmount').get('currency').get('code', "")
                            i.pop('operationAmount')
                        else:
                            continue
                    logger.info("JSON считан, преобразован")
                else:
                    logger.info("Данных в формате list[dict] в JSON файле отсутствуют")
                    loaded_data = "Отсутствуют данные выбранного формата"

            elif re.search(r"\b\w+\.csv\b", file_name):
                loaded_data = []
                for row in csv.DictReader(f, delimiter=';'):
                    loaded_data.append(row)
                logger.info("CSV считан, преобразован")

            elif re.search(r"\b\w+\.xlsx\b", file_name):
                loaded_data = []
                readed_data = pd.read_excel(file_path, sheet_name=0, header=0, index_col=None, na_values=['', ' '],
                                            keep_default_na=False, na_filter=True)
                transform_data = readed_data.to_dict('index')
                for i in transform_data:
                    loaded_data.append(transform_data[i])
                logger.info("XLSX считан, преобразован")
            logger.info("Данные возвращены. Функция завершена")
            return loaded_data


def filter_by_status(loaded_data: list | dict, search_line: str) -> list[dict]:
    """Функция фильтрации данных по статусу "EXECUTED", "CANCELED", "PENDING" """
    filtered_data = []
    logger.info("Старт")
    for i in range(0, len(loaded_data)):
        m = loaded_data[i]
        for key, value in m.items():
            # print(key, value, len(str(value)), type(value))
            if type(value) is float and value is np.nan or value == " " or value == "":
                loaded_data[i][key] = ""
        if len(loaded_data[i]) == 0 or loaded_data[i]["date"] == "" or loaded_data[i]["state"] == "":
            logger.info(f"Длина словаря: {len(loaded_data[i])}.Пустая строка detected")
            continue
        else:
            try:
                x = loaded_data[i]["state"]
                if re.search(search_line, x):
                    filtered_data.append(loaded_data[i])
            except Exception as ex:
                logger.error(
                    f"ОШИБКА: {ex}- {loaded_data[i]}, тип словаря: {type(loaded_data[i])}, "
                    f"Длина словаря: {len(loaded_data[i])}. Продолжаем")
                # print(f"ОШИБКА {ex} - {loaded_data[i]}")
                continue
    if len(filtered_data) == 0:
        logger.info(f"Данных со статусом {search_line} не обнаружено.")
        exit(f"Данных со статусом {search_line} не обнаружено.\nРабота программы завершена.")
    else:
        logger.info(f"Операции отфильтрованы по статусу {search_line} и возвращены. Функция завершена.")
        print("Операции отфильтрованы по статусу", ''.join(search_line))
    return filtered_data


def final_calculation(transactions_by_status: list | dict, choice: dict) -> any:
    """Функция окончательной сортировки и подсчёта типа транзакций"""
    df = pd.DataFrame(transactions_by_status)
    title = list(itertools.islice(choice.keys(), 1))
    filter_1 = df[title[0]] == choice[title[0]]
    if choice.get('currency_code'):
        title = list(itertools.islice(choice.keys(), 2))
        filter_2 = df[title[1]] == choice[title[1]]
        filtered_df = df[filter_1 & filter_2]
    else:
        filtered_df = df[filter_1]
    count_category = Counter(filtered_df[title[0]])
    filtered_transactions = filtered_df.to_dict("records")
    logger.info(f"Функция final_calculation выполнена {filtered_transactions}, {count_category}")
    if len(filtered_transactions) == 0:
        exit("Даные по выбранным критериям не обнаружены.\nРабота программы завершена.")
    return filtered_transactions, count_category
