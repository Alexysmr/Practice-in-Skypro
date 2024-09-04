import json
import logging
import os
import os.path
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

main_path = Path(__file__).resolve().parents[1]

logger = logging.getLogger('__name__')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(f'{main_path}/logs/utils.log', 'w', encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s %(funcName)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def input_transactions(filename: str) -> list[dict[Any, Any]]:
    """Функция принимает на вход путь до JSON-файла и
    возвращает список словарей с данными о финансовых транзакциях"""
    logger.info("Старт")
    operations_file = os.path.join(main_path, "data", filename)
    if os.path.exists(operations_file) and os.stat(operations_file).st_size != 0:
        with open(operations_file, encoding="utf-8") as f:
            logger.info("Данные транзакции проверены и загружены")
            transactions_data = json.load(f)
        if isinstance(transactions_data, list) and len(transactions_data) != 0:
            logger.info("Данные транзакции проверены и возвращены. Функция выполнена.")
            return transactions_data
        else:
            logger.info(
                "Работа функции завершена с ошибкой: Данные функции не прошли проверку, возвращен пустой список.")
            return []
    else:
        logger.info(
            "Работа функции завершена с ошибкой: Файл с данными не существует или пуст, возвращен пустой список.")
        return []


def currency_exchange(transactions_data: dict[Any, Any]) -> list | str:
    """Функция принимает на вход транзакцию и возвращает сумму транзакции
    (amount) в рублях, тип данных — float. Для пересчета из USD или EUR
    в рубли происходит обращение к внешнему API"""
    logger.info("Старт")
    amount_list = []
    if len(transactions_data) != 0:
        # main_path = Path(__file__).resolve().parents[1]
        logger.info("len(transactions_data) != 0")
        dotenv_path = os.path.join(main_path, ".apisett.env")
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
        api_token = os.getenv("API_KEY")
        logger.info("Получен API_KEY")
        url_eur = "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=EUR&amount=1"
        url_usd = "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=1"
        payload_eur = {}
        payload_usd = {}
        headers = {"apikey": f"{api_token}"}
        logger.info("Отправляем запрос по API")
        try:
            response_eur = requests.request("GET", url_eur, headers=headers, data=payload_eur)
            status_code_eur = response_eur.status_code
            if status_code_eur < 400:
                result_eur = response_eur.json()
                logger.info("Получен курс EUR")
                eur_course = result_eur.get("result", "")
            else:
                logger.info("Ошибка получения курса EUR. Продолжаем.")
                eur_course = ["error"]
            response_usd = requests.request("GET", url_usd, headers=headers, data=payload_usd)
            status_code_usd = response_usd.status_code
            if status_code_usd < 400:
                result_usd = response_usd.json()
                logger.info("Получен курс USD")
                usd_course = result_usd.get("result", "")
            else:
                logger.info("Ошибка получения курса USD. Продолжаем.")
                usd_course = ["error"]

            if isinstance(usd_course, float) and isinstance(eur_course, float):
                logger.info("Проверка значений курса валют на соответствие требуемому формату пройдена")
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
                    except Exception as ex:
                        logger.error(f"Ошибка: {ex}. Продолжаем.")
                        continue
                if len(amount_list) != 0:
                    # print(f"Курс за 1-цу валюты в рублях: USD= {usd_course}, EUR= {eur_course}")
                    logger.info(
                        f"Программа выполнена и завершена: Получен результат пересчета транзакций: {amount_list}.")
                    return amount_list
                else:
                    logger.info("Работа программы завершена с ошибкой: Отсутствуют данные транзакций.")
                    return "Работа программы завершена с ошибкой: Отсутствуют данные транзакций."
            else:
                logger.info("Работа программы завершена с ошибкой: Ошибка получения курса валют.")
                return "Работа программы завершена с ошибкой: Ошибка получения курса валют."
        except Exception as ex:
            logger.error(f"Работа программы завершена с ошибкой:  {ex}.")
            return "Работа программы завершена с ошибкой: Ошибка получения курса валют."
    else:
        logger.info("Работа программы завершена с ошибкой: Отсутствуют данные транзакций.")
        return "Работа программы завершена с ошибкой: Отсутствуют данные транзакций."
