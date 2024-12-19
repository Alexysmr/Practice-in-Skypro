import os
import pytest
import datetime
import unittest
from unittest import mock
from pathlib import Path
from dateutil import parser

from pandas import ExcelFile

from src.utils import read_transactions_data
from src.reports import choice_options, spending_by_category

main_path = Path(__file__).resolve().parents[1]
datetime_now = parser.parse(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


@pytest.fixture
def dataframe_ng_return():
    data_df = read_transactions_data("operations_test_ng.xlsx")[0]
    return data_df


@pytest.fixture
def dataframe_return():
    data_df = read_transactions_data("operations_test.xlsx")[0]
    return data_df


def test_choice_options_good_one(monkeypatch, dataframe_return):
    """Тест функции получения и подготовки параметров для передачи в функцию spending_by_category"""
    with unittest.mock.patch('builtins.input', side_effect=["03 dec 2023", "фастфуд"]):
        assert choice_options(dataframe_return) == ("Фастфуд", "2023-12-03 23:59:59.999999")


def test_choice_options_good_two(monkeypatch, dataframe_return):
    """Тест функции получения и подготовки параметров для передачи в функцию spending_by_category"""
    with unittest.mock.patch('builtins.input', side_effect=["01 march 2024", "", "фастфуд"]):
        assert choice_options(dataframe_return) == ("Фастфуд", "2024-03-01 23:59:59.999999")


def test_choice_options_good_three(monkeypatch, dataframe_return):
    """Тест функции получения и подготовки параметров для передачи в функцию spending_by_category"""
    with unittest.mock.patch('builtins.input', side_effect=["", "", "фастфуд"]):
        assert choice_options(dataframe_return) == ("Фастфуд", "None")


def test_choice_options_good_four(monkeypatch, dataframe_return):
    """Тест функции получения и подготовки параметров для передачи в функцию spending_by_category"""
    with unittest.mock.patch('builtins.input', side_effect=[f"{str(datetime_now.date())}", "", "фастфуд"]):
        assert choice_options(dataframe_return) == ("Фастфуд", "")


def test_choice_options_good_five(monkeypatch, dataframe_return):
    """Тест функции получения и подготовки параметров для передачи в функцию spending_by_category"""
    with unittest.mock.patch('builtins.input', side_effect=["08 march 2128", "", "фастфуд"]):
        assert choice_options(dataframe_return) == ("Фастфуд", "")


def test_choice_options_not_good(monkeypatch, dataframe_return):
    """Тест функции получения и подготовки параметров для передачи в функцию spending_by_category"""
    with unittest.mock.patch('builtins.input', side_effect=["03 dec 2024", "", "Аптека"]):
        with pytest.raises(SystemExit):
            choice_options(dataframe_return)


def test_spending_by_category(dataframe_return):
    """Тест функции фильтрации транзакций за 3 месяца по параметрам запроса пользователя"""
    with (unittest.mock.patch('builtins.input', return_value="Тестовый отчёт")):
        spending_by_category(dataframe_return, "Фастфуд", "2024-12-03 23:59:59.999999")
        report_file = os.path.join(main_path, "reports/Тестовый отчёт.xlsx")
        dict_report = ExcelFile(report_file).parse(ExcelFile(report_file).sheet_names[0]).to_dict('records')
        dict_report[0]["Дата операции"] = str(dict_report[0]["Дата операции"])
        assert os.path.exists(report_file) is True
        assert dict_report[0] == {'Дата операции': '2024-12-03 17:14:21', 'Дата платежа': '2024-12-03',
                                  'Номер карты': '*7197',
                                  'Статус': 'OK', 'Сумма операции': -80, 'Валюта операции': 'RUB',
                                  'Сумма платежа': -80,
                                  'Валюта платежа': 'RUB', 'Кэшбэк': 0, 'Категория': 'Фастфуд', 'MCC': 5814,
                                  'Описание': 'Ip nelikaev', 'Бонусы (включая кэшбэк)': 1,
                                  'Округление на инвесткопилку': 0,
                                  'Сумма операции с округлением': 80, 'number_of_week': 49}


def test_spending_by_category_ng(dataframe_return):
    """Тест функции фильтрации транзакций за 3 месяца по параметрам запроса пользователя"""
    with ((unittest.mock.patch('builtins.input', return_value="Неудачный отчёт"))):
        spending_by_category(dataframe_return, "Фастфуд", "2024-12-02 23:59:59.999999")
        report_file = os.path.join(main_path, "reports/Неудачный отчёт.xlsx")
        assert os.path.exists(report_file) is False
        assert spending_by_category(dataframe_return, "Фастфуд",
                                    "2024-12-02 23:59:59.999999") == ("Транзакции по категории \"Фастфуд\" "
                                                                      "в периоде с 2024-09-02 по 2024-12-02 "
                                                                      "не обнаружены")
