import json
import logging
from collections import Counter
from pathlib import Path
from typing import Any, List

import pandas as pd
from pandas import DataFrame

columns_list: List[Any] = [
    "Дата операции",
    "Дата платежа",
    "Статус",
    "Сумма операции",
    "Валюта операции",
    "Сумма платежа",
    "Валюта платежа",
    "Категория",
    "Описание",
]

main_path = Path(__file__).resolve().parents[1]
logger = logging.getLogger("__name__")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(f"{main_path}/logs/services.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s %(funcName)s %(lineno)d: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

category_and_description = []  # Категории и Описание


def searche_line(data_df: DataFrame) -> str:
    """Функция вывода всех вариантов Категории и Описания и выбора пользователем одного из них"""
    logger.info("Старт")
    print("searche_line strt")
    count_category = Counter(data_df[columns_list[7]])
    count_description = Counter(data_df[columns_list[8]])
    for key in count_category:
        category_and_description.append(key)
    for key in count_description:
        category_and_description.append(key)
    for i, element in enumerate(category_and_description):
        if i % 5 == 0:
            print()
        print(element, end=", ")
    print()
    logger.info("Список вариантов из Категория и Описание файла транзакций составлен и выведен в консоль")
    sign = input(
        "Выберите вариант, по которому необходимо произвести отбор транзакций,\n"
        "из списка выше и введите, отбор будет производиться из всех данных:-> "
    ).capitalize()
    if sign not in category_and_description:
        logger.info("Введён отсутствующий вариант, предлагается ещё попытка")
        sign = input(
            "Такого варианта нет в списке,\nпопробуйте ещё раз выбрать и ввести "
            "существующий вариант из списка выше:-> "
        ).capitalize()
        if sign not in category_and_description:
            logger.info("Второй раз введён остуствующий вариант. Работа функции завершена по exit")
            print("Такой категории нет в списке. Работа функции завершена.")
            sign = ""
            return sign
        else:
            logger.info("со второй попытки значение строки поиска для фильтрации транзакций получена, возвращена")
            print("Функция searche_line выполнена")
            return sign
    else:
        logger.info("Значение строки поиска для фильтрации транзакций получена, возвращена")
        print("searche_line endd")
        return sign


def simple_search(string_search: str, data_list_dict: list[dict]) -> json:
    """Функция отбора транзакций по выбранному из Категории или Описания пользователем значению"""
    logger.info("Старт")
    print("simple_search strt")
    sign = string_search
    if sign == "":
        print("Функция simple_search прервана")
        return sign
    df = pd.DataFrame(data_list_dict)
    df = df.drop("number_of_week", axis=1)
    logger.info("Список словарей транзакций преобразован в DF")
    filter_by_sign_df = df[(df[columns_list[7]] == sign) | (df[columns_list[8]] == sign)]
    logger.info(f"DF отфильтрован по значению {sign} из строки поиска")
    filter_by_sign_dict = filter_by_sign_df.to_dict("records")
    logger.info("DF - filter_by_sign_df преобразован в Dict - filter_by_sign_dict")
    for i in filter_by_sign_dict:
        i[columns_list[0]] = str(i.get(columns_list[0]))  # преобразование timestamp в столбце Дата операции в str
    logger.info("Данные в filter_by_sign_dict в ключе Дата операции преобразованы из timestamp в str")
    filter_by_sign_json = json.dumps(filter_by_sign_dict, ensure_ascii=False, indent=4)
    logger.info("filter_by_sign_dict преобразован в filter_by_sign_json и возвращён")
    print("simple_search endd")
    return filter_by_sign_json
