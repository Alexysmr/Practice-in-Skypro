import datetime
import json
import logging
import os
from pathlib import Path
from typing import Any, List

import pandas as pd
import requests
from dateutil import parser
from dotenv import load_dotenv
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
file_handler = logging.FileHandler(f"{main_path}/logs/utils.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s %(funcName)s %(lineno)d: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

datetime_now = parser.parse(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
now = datetime.datetime.now()
choice_date = "{:%Y-%m-}{}".format(now, now.day - 1)  # Данные из Америки, у них наше сегодня ещё не наступило

main_path = Path(__file__).resolve().parents[1]
dotenv_path = os.path.join(main_path, ".apisett.env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
user_settings_path = os.path.join(main_path, "data", "user_settings.json")
if os.path.exists(user_settings_path) and os.stat(user_settings_path).st_size != 0:
    with open(user_settings_path, encoding="utf-8") as f:
        json_data = json.load(f)
        user_currencies = json_data.get("user_currencies", "")
        stocks = json_data.get("user_stocks", "")


def currency_exchange_rate() -> list[dict]:
    """Получение текущего курса валют посредством API"""
    logger.info("Старт")
    print("currency_exchange_rate strt")
    headers_currency = {"apikey": f"{os.getenv('API_LAYER_KEY')}"}
    currency_rates = []
    payload = {}
    for currency in user_currencies:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount=1"
        try:
            response = requests.request("GET", url, headers=headers_currency, data=payload)
            status_code = response.status_code
            if status_code < 400:
                result = response.json()
                rate = result.get("info", "").get("rate", "")
                currency_rates.append({"currency": currency, "rate": rate})
                logger.info("Курс валют получен")
            else:
                logger.info("Ошибка получения курса валют")
                currency_rates.append({"currency": currency, "rate": "Ошибка получения курса"})
        except Exception as ex:
            logger.info(f"Проблемы {ex}")
            currency_rates.append({"currency": currency, "rate": "Ошибка получения курса"})
            continue
    print("currency_exchange_rate endd")
    return currency_rates


def get_stocks_price() -> list[dict]:
    """Получение курса акций посредством API"""
    logger.info("Старт")
    print("get_stocks_price strt")
    price_of_stocks = []
    for stock in stocks:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey=\
                {os.getenv('API_ALPHAVANTAGE_KEY')}"
        try:
            r = requests.get(url).json()
            price = r.get("Global Quote").get("05. price")
            price_of_stocks.append({"stock": stock, "price": price})
            logger.info(f"Курс акций {stock} получен")
        except Exception as ex:
            price_of_stocks.append({"stock": stock, "price": "Ошибка получения курса акций"})
            logger.info(f"Ошибка {stock} {ex} получения курса акций ")
            continue
    print("get_stocks_price endd")
    return price_of_stocks


def read_transactions_data(file_name: str) -> tuple[DataFrame, list[Any]]:
    """Функция чтения и подготовки данных"""
    logger.info("Старт кода чтения из XLSX")
    print("read_transactions_data strt")
    file_path = os.path.join(main_path, "data", file_name)
    loaded_data = []
    cl = columns_list
    if os.path.exists(file_path) and os.stat(file_path).st_size != 0:
        readed_data = pd.read_excel(
            file_path, sheet_name=0, header=0, index_col=None, na_values=None, keep_default_na=False, na_filter=False
        )
        transform_data = readed_data.to_dict("index")
        for k in transform_data:
            m = transform_data[k]
            if m.get("Кэшбэк", 0) == "":
                m["Кэшбэк"] = 0
            if (
                type(m) is not dict
                or len(m) == 0
                or m.get(f"{cl[0]}") == ""
                or m.get(f"{cl[0]}") > datetime_now
                or m.get(f"{cl[2]}") == ""
                or m.get(f"{cl[2]}") == "FAILED"
                or m.get(f"{cl[3]}") == ""
                or m.get(f"{cl[4]}") == ""
                or m.get(f"{cl[5]}") == ""
                or m.get(f"{cl[6]}") == ""
                or m.get(f"{cl[7]}") == ""
                or m.get(f"{cl[8]}") == ""
            ):
                continue
            else:
                m["number_of_week"] = m[columns_list[0]].isocalendar()[1]
                m[columns_list[1]] = str(m.get(columns_list[1], ""))[:10]
                m[columns_list[7]] = m.get(columns_list[7]).capitalize()
                m[columns_list[8]] = m.get(columns_list[8]).capitalize()
                loaded_data.append(m)
    if len(loaded_data) != 0:
        logger.info("XLSX считан, преобразован в DF, возвращен")
        data_from_file_df = pd.DataFrame(loaded_data)
        print("read_transactions_data endd")
        return data_from_file_df, loaded_data
    else:
        logger.info(
            "Выбранный файл отсутствует или не содержит необходимой информациии." "\nРабота программы завершена."
        )
        exit("Выбранный файл отсутствует или не содержит необходимой информациии.\nРабота программы завершена.")


def the_beginning_of_the_event():
    """Функция получения у пользователя даты и периода"""
    logger.info("Старт")
    print("the_beginning_of_the_event strt")
    current_datetime = None
    period_list = ["W", "M", "Y", "ALL", "Ь", "Ц", "Н", "ФДД"]
    input_date = input(
        "Чтобы произвести анализ транзакций введите необходимую дату цифрами в формате ДД-ММ-ГГГГ\n"
        "Чтобы произвести анализ транзакций на текущие дату и время нажмите Enter:\n-> "
    )
    if input_date != "":
        try:
            input_date = parser.parse(f"{input_date} 23:59:59.999999")
            if input_date.date() < datetime_now.date():
                current_datetime = input_date
            elif input_date.date() > datetime_now.date():
                current_datetime = datetime_now
                print("Введены некорректные данные, анализ транзакций будет произведён на текущие дату и время")
            elif input_date.date() == datetime_now.date():
                current_datetime = datetime_now
                print("Анализ транзакций будет произведён на текущие дату и время")
        except Exception as ex:
            logger.info(f"{ex} Нечитаемая дата, анализ транзакций будет произведён на текущие дату и время")
            current_datetime = datetime_now
            print("Введены некорректные данные, анализ транзакций будет произведён на текущие дату и время")
    else:
        current_datetime = datetime_now
        print("Анализ транзакций будет произведён на текущие дату и время")
        logger.info("Нажат enter, анализ данных будет произведен на текущую дату")
    period = input(
        "Чтобы произвести анализ транзакций за неделю, на которую приходится дата, введите W\n"
        "Чтобы произвести анализ транзакций за год, на который приходится дата, введите Y\n"
        "Чтобы произвести анализ всех доступных транзакций до указанной даты, введите ALL\n"
        "Чтобы произвести анализ транзакций за месяц, на который приходится дата, "
        "нажмите Enter\n -> "
    ).upper()
    year = current_datetime.year
    month = current_datetime.month
    number_of_week = current_datetime.isocalendar()[1]
    if period not in period_list or period == "M" or period == "Ь" or period == "":
        period = "M"
        start_month_date = datetime.datetime(year, month, 1, 0, 0, 0)
        print(f"Анализ транзакций будет произведён с {start_month_date} по {current_datetime}")
    if period == "W" or period == "Ц":
        period = "W"
        print(f"Анализ транзакций будет произведён за {number_of_week}-ю неделю {year} года")
    if period == "Y" or period == "Н":
        begin_year = datetime.datetime(year, 1, 1, 0, 0, 0)
        period = "Y"
        print(f"Анализ транзакций будет произведён с {begin_year} по {current_datetime}")
    if period == "ALL" or period == "ФДД":
        period = "ALL"
        print("Будет произведён анализ всех доступных транзакций до выбранной даты")
    logger.info(f"Выбор даты: {current_datetime}, Период: {period}")
    print("the_beginning_of_the_event endd")
    return current_datetime, period
