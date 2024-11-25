import datetime
import json
import logging
from collections import Counter
from pathlib import Path
from typing import Any, List

from dateutil import parser
from pandas import DataFrame

from src.utils import currency_exchange_rate, get_stocks_price

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

event_response = {
    "expenses": {"total_amount": 0, "main": [], "transfers_and_cash": []},
    "income": {"total_amount": 0, "main": []},
    "currency_rates": [],
    "stock_prices": [],
}

ex_categories = ["Пополнения", "Переводы", "Наличные", "Бонусы", "Зарплата"]

main_path = Path(__file__).resolve().parents[1]
logger = logging.getLogger("__name__")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(f"{main_path}/logs/views.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s %(funcName)s %(lineno)d: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

datetime_now = parser.parse(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def filtering_transactions(data_df: DataFrame, current_datetime: datetime, period: str) -> any:
    """Фильтрация и сортировка транзакций по заданным параметрам"""
    print("filtering_transactions strt")
    df = data_df
    logger.info("Старт")
    count_category_list = []
    main = []
    income = []
    transfers_and_cash = []
    intermediate_main = {}
    cash = {}
    transfers = {}
    filter_by_date_df = None
    year = current_datetime.year
    month = current_datetime.month
    number_of_week = current_datetime.isocalendar()[1]
    if period == "W":
        filter_by_date_df = df[
            (df["number_of_week"] == number_of_week) & (df[columns_list[0]].dt.strftime("%Y").astype("int") == year)
        ]
    elif period == "Y":
        filter_by_date_df = df[(df[columns_list[0]].dt.strftime("%Y").astype("int") == year)]
    elif period == "M":
        start_month_date = datetime.datetime(year, month, 1, 0, 0, 0)
        filter_by_date_df = df[(df[columns_list[0]] >= start_month_date) & (df[columns_list[0]] <= current_datetime)]
    elif period == "ALL":
        filter_by_date_df = df[(df[columns_list[0]] < current_datetime)]  # ALL — все данные ДО указанной даты
    logger.info("DataFrame отфильтрован по дате и периоду")
    filter_by_date_df = filter_by_date_df.drop("number_of_week", axis=1)  # Столбец number_of_week удаляем
    income_df = filter_by_date_df[filter_by_date_df[columns_list[3]] > 0]  # Все поступления
    filter_by_date_df = filter_by_date_df.loc[filter_by_date_df[columns_list[3]] < 0]  # Вся расходная часть
    transfers_df = filter_by_date_df[filter_by_date_df[columns_list[7]] == ex_categories[1]]  # Расходы - Переводы
    cash_df = filter_by_date_df[filter_by_date_df[columns_list[7]] == ex_categories[2]]  # Расходы - Наличные
    event_response["expenses"]["total_amount"] = abs(int(round(filter_by_date_df[columns_list[3]].sum(), 0)))
    logger.info(f"Общая сумма расходов = {event_response["expenses"]["total_amount"]}")
    filter_by_date_df = filter_by_date_df[
        ~(filter_by_date_df[columns_list[7]] == ex_categories[1])
        & ~(filter_by_date_df[columns_list[7]] == ex_categories[2])
    ]
    logger.info("DataFrame отфильтрован от расходных Переводов и Наличных")
    count_category = Counter(filter_by_date_df[columns_list[7]]).most_common(7)
    logger.info(f"Получены {type(count_category)} 7-и самых частых категорий расходов без Переводов и Наличных")
    for i in count_category:
        count_category_list.append(i[0])
    others_category_filtered_df = filter_by_date_df[~filter_by_date_df[columns_list[7]].isin(count_category_list)]
    logger.info("Получен DF для категории расходов Остальное без Переводов и Наличных")
    for i in count_category_list:
        category_filtered_by_date_df = filter_by_date_df[filter_by_date_df[columns_list[7]] == i]
        intermediate_main["category"] = i
        intermediate_main["amount"] = abs(int(round(category_filtered_by_date_df[columns_list[3]].sum(), 0)))
        main.append(intermediate_main)
        intermediate_main = {}
    main = sorted(main, key=lambda x: x["amount"], reverse=True)
    intermediate_main["category"] = "Остальное"
    intermediate_main["amount"] = abs(int(round(others_category_filtered_df[columns_list[3]].sum(), 0)))
    main.append(intermediate_main)
    intermediate_main = {}
    event_response["expenses"]["main"] = main
    logger.info("7 сортированых частых категорий расходов + расходы Остальное внесены в отчёт")
    cash["category"] = ex_categories[2]
    cash["amount"] = abs(int(round(cash_df[columns_list[3]].sum(), 0)))
    transfers["category"] = ex_categories[1]
    transfers["amount"] = abs(int(round(transfers_df[columns_list[3]].sum(), 0)))
    transfers_and_cash.extend((cash, transfers))
    event_response["expenses"]["transfers_and_cash"] = sorted(
        transfers_and_cash, key=lambda x: x["amount"], reverse=True
    )
    logger.info("Расходы Переводы и Наличные посчитаны сортированы и внесены в отчёт")
    event_response["income"]["total_amount"] = int(round(income_df[columns_list[3]].sum(), 0))
    income_count_category = dict(Counter(income_df[columns_list[8]]))
    for key in income_count_category:
        income_category_df = income_df[income_df[columns_list[8]] == key]
        intermediate_main["category"] = str(key)
        intermediate_main["amount"] = abs(int(round(income_category_df[columns_list[3]].sum(), 0)))
        income.append(intermediate_main)
        intermediate_main = {}
    event_response["income"]["main"] = sorted(income, key=lambda x: x["amount"], reverse=True)
    logger.info("Раздел Поступления посчитан, сортирован и внесён в отчёт")
    event_response["currency_rates"] = currency_exchange_rate()
    event_response["stock_prices"] = get_stocks_price()
    logger.info("Курсы валют и курсы акций добавлены в отчёт")
    event_response_json = json.dumps(event_response, ensure_ascii=False, indent=4)
    logger.info("Весь отчёт по транзакциям: сформирован и преобразован в JSON формат, выведен в консоль, возвращён")
    print("filtering_transactions endd")
    return event_response_json
