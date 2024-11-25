import datetime
import logging
from collections import Counter
from pathlib import Path
from typing import Optional

import dateutil
import dateutil.relativedelta
import pandas as pd
from dateutil import parser

main_path = Path(__file__).resolve().parents[1]
logger = logging.getLogger("__name__")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(f"{main_path}/logs/reports.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s %(funcName)s %(lineno)d: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


datetime_now = parser.parse(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def choice_options(data_df: pd.DataFrame) -> tuple[str, str]:
    """Функция получения и подготовки параметров для передачи в функцию spending_by_category"""
    logger.info("Старт")
    print("choice_options strt")
    current_datetime = None
    category_list = []
    count_category = Counter(data_df["Категория"])
    for key in count_category:
        category_list.append(key)
    input_date = input(
        "Введите дату цифрами в формате ДД-ММ-ГГГГ, чтобы выполнить отбор "
        "транзакций за три пред'идущих месяца\n"
        "Чтобы ввести текущую дату - просто нажмите Enter:\n-> "
    )
    if input_date != "":
        try:
            input_date = parser.parse(f"{input_date} 23:59:59.999999")
            if input_date.date() < datetime_now.date():
                current_datetime = input_date
            elif input_date.date() > datetime_now.date():
                current_datetime = ""
                print("Введено некорректное значение, отбор транзакций будет произведён на текущую дату")
            elif input_date.date() == datetime_now.date():
                current_datetime = ""
                print("Отбор транзакций будет произведён на текущую дату")
        except Exception as ex:
            logger.info(f"{ex} Нечитаемая или некорректная дата, отбор транзакций будет произведён на текущую дату")
            current_datetime = ""
            print("Введены некорректные данные, отбор транзакций будет произведён на текущую дату")
    else:
        current_datetime = None
        print("Отбор транзакций будет произведён на текущую дату")
        logger.info("Нажат enter, отбор данных будет произведен на текущую дату")
    for i, element in enumerate(category_list):
        if i % 5 == 0:
            print()
        print(element, end=", ")
    print()
    category = input(
        "Выберите и введите, из списка выше, категорию по которой нужно "
        "произвести отбор транзакций\nкатегории указаны из всех известных данных:-> "
    ).capitalize()
    if category not in category_list:
        category = input(
            "Совпадение не найдено.\nПопробуйте ещё раз выбрать из списка выше и ввести ,"
            "\nкатегорию по которой нужно произвести отбор транзакций:-> "
        ).capitalize()
        logger.info("Введено несуществующее значение категории. Вторая попытка")
        if category not in category_list:
            logger.info("Второй раз введено несуществующее значение категории. Работа завершена")
            exit("Совпадение не найдено. Работа программы завершена")
        else:
            logger.info(f"Со второй попытки выбор сделан {category}")
    else:
        logger.info(f"Выбор сделан: {category}, {str(current_datetime)}. Данные возвращены")
    print("choice_options endd")
    return category, str(current_datetime)


def decorator_spending(func):
    def wrapper(*args, output_file_name="Отчёт"):
        print("decorator_spending strt")
        input_file_name = input("Введите название файла отчёта или нажмите Enter: ")
        if input_file_name != "":
            output_file_name = input_file_name
        print("Файл отчёта: ", f"{output_file_name}.xlsx")
        output_data = func(*args)
        if type(output_data) is pd.DataFrame:
            output_data.to_excel(f"{main_path}/reports/{output_file_name}.xlsx", index=False)
            logger.info("Декоратор записи отбора транзакций за 3 месяца до указанной даты в формате XLSX выполнен")
        print("decorator_spending endd")

    return wrapper


@decorator_spending
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame | str:
    """Функция фильтрации транзакций по параметрам запроса пользователя"""
    logger.info("Старт")
    print("spending_by_category strt")
    if date == "" or date is None or date == "None":
        date = datetime_now
    else:
        date = parser.parse(f"{date} 23:59:59.999999")
    logger.info(f"Получена дата {date}")
    delta_date = (date - dateutil.relativedelta.relativedelta(months=3)).date()
    start_date = datetime.datetime(delta_date.year, delta_date.month, delta_date.day, 0, 0, 0)
    filter_transactions_df = transactions[
        (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= date)
        & (transactions["Категория"] == category)
    ]

    logger.info("Транзакции отфильтрованы в соответствии с запросом пользователя")
    print(f"Отбор транзакций будет произведён с {start_date.date()} по {date.date()} по категории " f'"{category}"')
    if filter_transactions_df.empty:
        filter_transactions_df = (
            f'Транзакции по категории "{category}" в периоде с {start_date.date()} по ' f"{date.date()}не обнаружены"
        )
        logger.info("По заданным параметрам транзакции не обнаружены")
    else:
        pd.set_option("display.max_rows", None)
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", None)
        logger.info("Отфильтрованные транзакции возвращены в формате DataFrame")
    print(filter_transactions_df)
    print("spending_by_category endd")
    return filter_transactions_df
