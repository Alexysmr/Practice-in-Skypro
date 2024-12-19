import pytest
import unittest
import json
from unittest import mock

from src.utils import read_transactions_data
from src.services import searche_line, simple_search


@pytest.fixture
def data_df_return_one_row():
    data_df, data_dict = read_transactions_data("operations_test.xlsx")
    return data_df, data_dict


@pytest.mark.parametrize("test_input,expected", [("фастфуд", "Фастфуд"), ("ip nelikaev", "Ip nelikaev"), ("", "")])
def test_searche_line(monkeypatch, data_df_return_one_row, test_input, expected):
    """Тест функции вывода всех вариантов Категории и Описания и выбора пользователем одного из них"""
    with unittest.mock.patch('builtins.input', return_value=test_input):
        assert searche_line(data_df_return_one_row[0]) == expected


def test_simple_search_good(data_df_return_one_row):
    """Тест функции отбора транзакций по выбранному из Категории или Описания пользователем значению"""
    string_search = "Фастфуд"
    assert simple_search(string_search, data_df_return_one_row[1]) == json.dumps(
        [{"Дата операции": "2024-12-03 17:14:21", "Дата платежа": "2024-12-03",
          "Номер карты": "*7197", "Статус": "OK", "Сумма операции": -80, "Валюта операции": "RUB",
          "Сумма платежа": -80, "Валюта платежа": "RUB", "Кэшбэк": 0, "Категория": "Фастфуд",
          "MCC": 5814, "Описание": "Ip nelikaev", "Бонусы (включая кэшбэк)": 1,
          "Округление на инвесткопилку": 0, "Сумма операции с округлением": 80}],
        ensure_ascii=False, indent=4)


def test_simple_search_not_good(data_df_return_one_row):
    string_search = ""
    assert simple_search(string_search, data_df_return_one_row[1]) == ""
