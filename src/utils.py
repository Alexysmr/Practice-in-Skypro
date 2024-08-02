import json
import os.path
from pathlib import Path
from src.external_api import currency_exchange_rate


def input_transactions(filename="operations.json") -> list:
    """Функция принимает на вход путь до JSON-файла и
    возвращает список словарей с данными о финансовых транзакциях"""
    main_path = Path(__file__).resolve().parents[1]
    operations_file = os.path.join(main_path, "data", filename)
    if os.path.exists(operations_file) and os.stat(operations_file).st_size != 0:
        with open(operations_file, encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list) and len(data) != 0:
            return data
        else:
            return []
    else:
        return []


def currency_exchange(filename: str) -> list:
    """Функция принимает на вход транзакцию и возвращает сумму транзакции
    (amount) в рублях, тип данных — float"""
    amount_list = []
    data = input_transactions(filename)
    if len(data) != 0:
        course = currency_exchange_rate()  # Запрос курса USD и EUR через модуль external_api.py
        usd_course = course[0]
        eur_course = course[1]
        if isinstance(usd_course, float) and isinstance(eur_course, float):
            for x in data:
                try:
                    amount = float(x.get('operationAmount', "").get('amount', ""))
                    currency_code = x.get('operationAmount', "").get('currency', "").get('code', "")
                    # id_number = x.get("id")
                    if currency_code == "USD":
                        amount = round(float(amount * usd_course), 2)
                    elif currency_code == "EUR":
                        amount = round(float(amount * eur_course), 2)
                    # print("Операция: ", id_number, "Cумма в рублях:", amount, "Валюта: ", currency_code, sep=" ")
                    amount_list.append(amount)
                except AttributeError:
                    continue
            if len(amount_list) != 0:
                # print(f"Курс за 1-цу валюты в рублях: USD= {usd_course}, EUR= {eur_course}")
                return amount_list
            else:
                return ["Отсутствуют данные транзакций"]
        else:
            return ["Ошибка получения курса валют"]
    else:
        return ["Отсутствуют данные транзакций"]
