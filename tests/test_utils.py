import pytest
import datetime
import unittest
from pandas import DataFrame
from pandas import Timestamp
from unittest.mock import patch

from src.utils import read_transactions_data, currency_exchange_rate, the_beginning_of_the_event, get_stocks_price


def test_read_transaction():
    """Тест функции чтения и подготовки данных из файла"""
    assert type(read_transactions_data("operations_test.xlsx")[0]) is DataFrame
    assert read_transactions_data("operations_test.xlsx")[1] == [{'MCC': 5814,
                                                                  'number_of_week': 49,
                                                                  'Бонусы (включая кэшбэк)': 1,
                                                                  'Валюта операции': 'RUB',
                                                                  'Валюта платежа': 'RUB',
                                                                  'Дата операции': Timestamp('2024-12-03 17:14:21'),
                                                                  'Дата платежа': '2024-12-03',
                                                                  'Категория': 'Фастфуд',
                                                                  'Кэшбэк': 0,
                                                                  'Номер карты': '*7197',
                                                                  'Округление на инвесткопилку': 0,
                                                                  'Описание': 'Ip nelikaev',
                                                                  'Статус': 'OK',
                                                                  'Сумма операции': -80,
                                                                  'Сумма операции с округлением': 80,
                                                                  'Сумма платежа': -80}]


def test_read_transaction_ng_one():
    """Тест функции чтения и подготовки данных из файла"""
    with pytest.raises(SystemExit):
        read_transactions_data("operation_test_ng.xlsx")


def test_read_transaction_ng_two():
    """Тест функции чтения и подготовки данных из файла"""
    with pytest.raises(SystemExit):
        read_transactions_data("operations_test_ng.xlsx")


def test_beginning_of_the_event_rear_date_m(monkeypatch):
    """Тест функции получения от пользователя даты и периода"""
    with unittest.mock.patch('builtins.input', side_effect=["31-01-2023", "ь"]):
        assert the_beginning_of_the_event() == (
            datetime.datetime(2023, 1, 31, 23, 59, 59, 999999), "M")


def test_beginning_of_the_event_rear_date_w(monkeypatch):
    """Тест функции получения от пользователя даты и периода"""
    with unittest.mock.patch('builtins.input', side_effect=["31-01-2023", "ц"]):
        assert the_beginning_of_the_event() == (
            datetime.datetime(2023, 1, 31, 23, 59, 59, 999999), "W")


def test_beginning_of_the_event_rear_date_y(monkeypatch):
    """Тест функции получения от пользователя даты и периода"""
    with unittest.mock.patch('builtins.input', side_effect=["31-01-2023", "н"]):
        assert the_beginning_of_the_event() == (
            datetime.datetime(2023, 1, 31, 23, 59, 59, 999999), 'Y')


def test_beginning_of_the_event_rear_date_all(monkeypatch):
    """Тест функции получения от пользователя даты и периода"""
    with unittest.mock.patch('builtins.input', side_effect=["31-01-2023", "фдд"]):
        assert the_beginning_of_the_event() == (
            datetime.datetime(2023, 1, 31, 23, 59, 59, 999999), 'ALL')


def test_beginning_of_the_event_future_date_m(monkeypatch):
    """Тест функции получения от пользователя даты и периода"""
    with (unittest.mock.patch('builtins.input', side_effect=["31-01-2028", ""])):
        assert the_beginning_of_the_event()[1] == "M"


def test_beginning_of_the_event_future_date(monkeypatch):
    """Тест функции получения от пользователя даты и периода """
    with (unittest.mock.patch('builtins.input', side_effect=["31-01-2028", ""])):
        assert type(the_beginning_of_the_event()[0]) is datetime.datetime


def test_beginning_of_the_event_date_error(monkeypatch):
    """Тест функции получения от пользователя даты и периода"""
    with (unittest.mock.patch('builtins.input', side_effect=["text", ""])):
        assert type(the_beginning_of_the_event()[0]) is datetime.datetime


def test_beginning_of_the_event_date_today(monkeypatch):
    """Тест функции получения от пользователя даты и периода"""
    with (unittest.mock.patch('builtins.input', side_effect=[f"{datetime.datetime.now().date()}", ""])):
        assert type(the_beginning_of_the_event()[0]) is datetime.datetime


@patch('src.utils.requests.request')
def test_currency_exchange_rate(mock_request):
    """Тест функции запроса курса валют"""
    mock_request.return_value.status_code = 200
    mock_request.return_value.json.return_value = {"info": {"rate": 91.32654187}}
    assert currency_exchange_rate() == [{'currency': 'USD', 'rate': 91.32654187},
                                        {'currency': 'EUR', 'rate': 91.32654187}]


@patch('src.utils.requests.request')
def test_currency_exchange_rate_miss(mock_request):
    """Тест функции запроса курса валют"""
    mock_request.return_value.status_code = 410
    mock_request.return_value.json.return_value = {"info": {"rate": 91.32654187}}
    assert currency_exchange_rate() == [{'currency': 'USD', 'rate': 'Ошибка получения курса'},
                                        {'currency': 'EUR', 'rate': 'Ошибка получения курса'}]


@patch('src.utils.requests.request')
def test_currency_exchange_rate_miss_two(mock_request):
    """Тест функции запроса курса валют"""
    mock_request.return_value.status_code = 200
    mock_request.return_value.json.return_value = ""
    assert currency_exchange_rate() == [{'currency': 'USD', 'rate': 'Ошибка получения курса'},
                                        {'currency': 'EUR', 'rate': 'Ошибка получения курса'}]


@patch('src.utils.requests.get')
def test_get_stocks_price(mock_request):
    """Тест функции запроса курса акций"""
    mock_request.return_value.json.return_value = {"Global Quote": {"05. price": 1234.0}}
    assert get_stocks_price() == [{'price': 1234.0, 'stock': 'AAPL'},
                                  {'price': 1234.0, 'stock': 'AMZN'},
                                  {'price': 1234.0, 'stock': 'GOOGL'},
                                  {'price': 1234.0, 'stock': 'MSFT'},
                                  {'price': 1234.0, 'stock': 'TSLA'}]


@patch('src.utils.requests.get')
def test_get_stocks_price_miss(mock_request):
    """Тест функции запроса курса акций"""
    mock_request.return_value.json.return_value = ""
    assert get_stocks_price() == [{'price': 'Ошибка получения курса акций', 'stock': 'AAPL'},
                                  {'price': 'Ошибка получения курса акций', 'stock': 'AMZN'},
                                  {'price': 'Ошибка получения курса акций', 'stock': 'GOOGL'},
                                  {'price': 'Ошибка получения курса акций', 'stock': 'MSFT'},
                                  {'price': 'Ошибка получения курса акций', 'stock': 'TSLA'}]
