import requests
import os
from pathlib import Path
from dotenv import load_dotenv


def currency_exchange_rate() -> list[float]:
    """Обращение к внешнему API для получения текущего курса валют"""
    main_path = Path(__file__).resolve().parents[1]
    dotenv_path = os.path.join(main_path, '.apisett.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    api_token = os.getenv('API_KEY')

    url_eur = "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=EUR&amount=1"
    url_usd = "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=1"

    payload_eur = {}
    payload_usd = {}
    headers = {"apikey": f"{api_token}"}

    response_eur = requests.request("GET", url_eur, headers=headers, data=payload_eur)
    status_code_eur = response_eur.status_code
    if status_code_eur < 400:
        result_eur = response_eur.json()
        eur_course = result_eur.get("info", "").get("rate", "")
    else:
        eur_course = ["error"]

    response_usd = requests.request("GET", url_usd, headers=headers, data=payload_usd)
    status_code_usd = response_usd.status_code
    if status_code_usd < 400:
        result_usd = response_usd.json()
        usd_course = result_usd.get("info", "").get("rate", "")
    else:
        usd_course = ["error"]

    change_course = [usd_course, eur_course]
    return change_course
