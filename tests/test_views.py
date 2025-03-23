import pytest
import json
from unittest.mock import patch
from dateutil import parser

from src.utils import read_transactions_data
from src.views import filtering_transactions


@pytest.fixture
def data_df_return_one_row_w():
    data_df = read_transactions_data("operations_test.xlsx")[0]
    current_datetime = parser.parse("03 dec 2024 17:14")
    period = "W"
    return data_df, current_datetime, period


@pytest.fixture
def data_df_return_one_row_m():
    data_df = read_transactions_data("operations_test.xlsx")[0]
    current_datetime = parser.parse("03 dec 2024 17:14")
    period = "M"
    return data_df, current_datetime, period


@pytest.fixture
def data_df_return_one_row_y():
    data_df = read_transactions_data("operations_test.xlsx")[0]
    current_datetime = parser.parse("03 dec 2024 17:14")
    period = "Y"
    return data_df, current_datetime, period


@pytest.fixture
def data_df_return_one_row_all():
    data_df = read_transactions_data("operations_test.xlsx")[0]
    current_datetime = parser.parse("03 dec 2024 17:14")
    period = "ALL"
    return data_df, current_datetime, period


@pytest.fixture
def data_df_return_one_row_w_ng():
    data_df = read_transactions_data("operations_test.xlsx")[0]
    current_datetime = parser.parse("03 nov 2024 17:14")
    period = "W"
    return data_df, current_datetime, period


@pytest.fixture
def currencys_rate():
    return [{'currency': 'USD', 'rate': 91.0}, {'currency': 'EUR', 'rate': 101.0}]


@pytest.fixture
def stocks_price():
    return [{'price': 1234.0, 'stock': 'AAPL'},
            {'price': 1235.0, 'stock': 'AMZN'},
            {'price': 1236.0, 'stock': 'GOOGL'},
            {'price': 1237.0, 'stock': 'MSFT'},
            {'price': 1238.0, 'stock': 'TSLA'}]


@pytest.fixture
def result_filtering_transactions_one_row():
    return ({"expenses": {"total_amount": 80, "main": [{"category": "Фастфуд", "amount": 80},
                                                       {"category": "Остальное", "amount": 0}],
                          "transfers_and_cash": [{"category": "Наличные", "amount": 0},
                                                 {"category": "Переводы", "amount": 0}]},
            "income": {"total_amount": 0, "main": []},
             "currency_rates": [{"currency": "USD", "rate": 91.0}, {"currency": "EUR", "rate": 101.0}],
             "stock_prices": [{"price": 1234.0, "stock": "AAPL"}, {"price": 1235.0, "stock": "AMZN"},
                              {"price": 1236.0, "stock": "GOOGL"}, {"price": 1237.0, "stock": "MSFT"},
                              {"price": 1238.0, "stock": "TSLA"}]})


def test_filtering_transactions_w(data_df_return_one_row_w, currencys_rate, stocks_price, monkeypatch,
                                  result_filtering_transactions_one_row):
    data_df, current_datetime, period = data_df_return_one_row_w
    with (patch('src.views.currency_exchange_rate', return_value=currencys_rate),
          patch('src.views.get_stocks_price', return_value=stocks_price)):
        assert filtering_transactions(data_df, current_datetime, period) == json.dumps(
            result_filtering_transactions_one_row, ensure_ascii=False, indent=4)


def test_filtering_transactions_m(data_df_return_one_row_m, currencys_rate, stocks_price, monkeypatch,
                                  result_filtering_transactions_one_row):
    data_df, current_datetime, period = data_df_return_one_row_m
    with (patch('src.views.currency_exchange_rate', return_value=currencys_rate),
          patch('src.views.get_stocks_price', return_value=stocks_price)):
        assert filtering_transactions(data_df, current_datetime, period) == json.dumps(
            result_filtering_transactions_one_row, ensure_ascii=False, indent=4)


def test_filtering_transactions_y(data_df_return_one_row_y, currencys_rate, stocks_price, monkeypatch,
                                  result_filtering_transactions_one_row):
    data_df, current_datetime, period = data_df_return_one_row_y
    with (patch('src.views.currency_exchange_rate', return_value=currencys_rate),
          patch('src.views.get_stocks_price', return_value=stocks_price)):
        assert filtering_transactions(data_df, current_datetime, period) == json.dumps(
            result_filtering_transactions_one_row, ensure_ascii=False, indent=4)


def test_filtering_transactions_all(data_df_return_one_row_all, currencys_rate, stocks_price, monkeypatch,
                                    result_filtering_transactions_one_row):
    data_df, current_datetime, period = data_df_return_one_row_all
    with (patch('src.views.currency_exchange_rate', return_value=currencys_rate),
          patch('src.views.get_stocks_price', return_value=stocks_price)):
        assert filtering_transactions(data_df, current_datetime, period) == json.dumps(
            result_filtering_transactions_one_row, ensure_ascii=False, indent=4)


def test_filtering_transactions_w_ng(data_df_return_one_row_w_ng, currencys_rate, stocks_price, monkeypatch,
                                     result_filtering_transactions_one_row):
    data_df, current_datetime, period = data_df_return_one_row_w_ng
    with (patch('src.views.currency_exchange_rate', return_value=currencys_rate),
          patch('src.views.get_stocks_price', return_value=stocks_price)):
        assert filtering_transactions(data_df, current_datetime, period) == ("Транзакций за указанный период не "
                                                                             "обнаружено. Работа функции завершена")
