import json
import requests
import os
import os.path
from pathlib import Path
from typing import Any
from dotenv import load_dotenv


def input_transactions(filename: str) -> list[dict[Any, Any]]:
    """Функция принимает на вход путь до JSON-файла и
    возвращает список словарей с данными о финансовых транзакциях"""
    main_path = Path(__file__).resolve().parents[1]
    operations_file = os.path.join(main_path, "data", filename)
    if os.path.exists(operations_file) and os.stat(operations_file).st_size != 0:
        with open(operations_file, encoding="utf-8") as f:
            transactions_data = json.load(f)
        if isinstance(transactions_data, list) and len(transactions_data) != 0:
            return transactions_data
        else:
            return []
    else:
        return []


def currency_exchange(transactions_data: dict[Any, Any]) -> list:
    """Функция принимает на вход транзакцию и возвращает сумму транзакции
    (amount) в рублях, тип данных — float. Для пересчета из USD или EUR
    в рубли происходит обращение к внешнему API"""
    amount_list = []
    if len(transactions_data) != 0:
        main_path = Path(__file__).resolve().parents[1]
        dotenv_path = os.path.join(main_path, ".apisett.env")
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
        api_token = os.getenv("API_KEY")
        url_eur = "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=EUR&amount=1"
        url_usd = "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=1"
        payload_eur = {}
        payload_usd = {}
        headers = {"apikey": f"{api_token}"}
        response_eur = requests.request("GET", url_eur, headers=headers, data=payload_eur)
        status_code_eur = response_eur.status_code
        if status_code_eur < 400:
            result_eur = response_eur.json()
            eur_course = result_eur.get("result", "")
        else:
            eur_course = ["error"]
        response_usd = requests.request("GET", url_usd, headers=headers, data=payload_usd)
        status_code_usd = response_usd.status_code
        if status_code_usd < 400:
            result_usd = response_usd.json()
            usd_course = result_usd.get("result", "")
        else:
            usd_course = ["error"]

        if isinstance(usd_course, float) and isinstance(eur_course, float):
            for x in transactions_data:
                try:
                    amount = float(x.get("operationAmount", "").get("amount", ""))
                    currency_code = x.get("operationAmount", "").get("currency", "").get("code", "")
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
