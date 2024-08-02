from unittest.mock import Mock
from unittest.mock import patch
import json
import os.path
from pathlib import Path
from src.utils import currency_exchange, input_transactions
from src.external_api import currency_exchange_rate


def test_input_transactions():
    assert input_transactions("operations0.json") == []  # operations0.json - пустой
    assert input_transactions("operations1.json") == [1, 4, 5]  # operations1.json - содержит список [1, 4, 5]
    assert input_transactions("operations2.json") == []  # operations2.json не существует
    assert input_transactions("operations3.json") == []  # operations3.json - содержит простой текст, не список
    assert input_transactions("operations4.json") == [  # operations4.json содержит часть operations.json - 4 транзакции
        {'id': 441945886, 'state': 'EXECUTED', 'date': '2019-08-26T10:50:58.294041',
         'operationAmount': {'amount': '31957.58', 'currency': {'name': 'руб.', 'code': 'RUB'}},
         'description': 'Перевод организации', 'from': 'Maestro 1596837868705199', 'to': 'Счет 64686473678894779589'},
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364',
         'operationAmount': {'amount': '8221.37', 'currency': {'name': 'USD', 'code': 'USD'}},
         'description': 'Перевод организации', 'from': 'MasterCard 7158300734726758',
         'to': 'Счет 35383033474447895560'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572',
         'operationAmount': {'amount': '9824.07', 'currency': {'name': 'USD', 'code': 'USD'}},
         'description': 'Перевод организации', 'from': 'Счет 75106830613657916952', 'to': 'Счет 11776614605963066702'},
        {'id': 142264268, 'state': 'EXECUTED', 'date': '2019-04-04T23:20:05.206878',
         'operationAmount': {'amount': '79114.93', 'currency': {'name': 'EUR', 'code': 'EUR'}},
         'description': 'Перевод со счета на счет', 'from': 'Счет 19708645243227258542',
         'to': 'Счет 75651667383060284188'}]


def test_currency_exchange():
    assert currency_exchange("operations1.json") == ['Отсутствуют данные транзакций']  # operations0.json - пустой
    assert currency_exchange("operations1.json") == [
        'Отсутствуют данные транзакций']  # operations1.json - содержит список [1, 4, 5]
    assert currency_exchange("operations2.json") == [
        'Отсутствуют данные транзакций']  # "operations2.json" не существует
    assert currency_exchange("operations3.json") == [
        'Отсутствуют данные транзакций']  # operations3.json - содержит простой текст, не список
