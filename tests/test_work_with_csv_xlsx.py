import os
import os.path
from unittest.mock import Mock, patch

import pytest

from src.work_with_csv_xlsx import reading_csv, reading_xlsx


@pytest.fixture
def expected_reading_csv_xlsx():
    return 'Работа функции завершена.'


@pytest.fixture
def expected_reading_csv_xlsx_file_error():
    return 'Работа функции завершена с ошибкой: Файл не найден или пуст.'


@pytest.fixture
def expected_reading_csv_xlsx_name_error():
    return 'Работа функции завершена с ошибкой: Имя файла данных отсутствует'


def test_reading_csv(expected_reading_csv_xlsx, expected_reading_csv_xlsx_file_error,
                     expected_reading_csv_xlsx_name_error):
    """Тестирование функции reading_csv"""
    file_name_csv = 'transactions.csv'
    assert reading_csv(file_name_csv) == expected_reading_csv_xlsx

    file_name_csv = 'operations.csv'
    assert reading_csv(file_name_csv) == expected_reading_csv_xlsx_file_error

    file_name_csv = ''
    assert reading_csv(file_name_csv) == expected_reading_csv_xlsx_name_error


def test_reading_xlsx(expected_reading_csv_xlsx, expected_reading_csv_xlsx_file_error,
                      expected_reading_csv_xlsx_name_error):
    """Тестирование функции reading_xlsx"""
    file_name_xlsx = 'transactions_excel.xlsx'
    assert reading_xlsx(file_name_xlsx) == expected_reading_csv_xlsx

    file_name_xlsx = 'operation.xlsx'
    assert reading_xlsx(file_name_xlsx) == expected_reading_csv_xlsx_file_error

    file_name_xlsx = ''
    assert reading_xlsx(file_name_xlsx) == expected_reading_csv_xlsx_name_error


@patch('src.work_with_csv_xlsx.os.path')
def test_reading_csv_1(mock_parametr, expected_reading_csv_xlsx_file_error):
    """Тестирование функции reading_csv"""
    mock_data = Mock(return_value=[''])
    file_name_csv = mock_data
    assert reading_csv(file_name_csv) == expected_reading_csv_xlsx_file_error

    mock_parametr.return_value.os.path = False
    os.path.exists = mock_parametr
    file_name_csv = 'transactions.csv'
    assert reading_csv(file_name_csv) == 'Работа функции завершена с ошибкой: bad argument type for built-in operation'


@patch('src.work_with_csv_xlsx.os.path')
def test_reading_xlsx_1(mock_parametr, expected_reading_csv_xlsx_file_error):
    """Тестирование функции reading_xlsx"""
    mock_data = Mock(return_value=[''])
    file_name_xlsx = mock_data
    assert reading_xlsx(file_name_xlsx) == expected_reading_csv_xlsx_file_error
    mock_parametr.return_value.os.path = False
    os.path.exists = mock_parametr
    file_name_xlsx = 'transactions_excel.xlsx'
    assert reading_xlsx(file_name_xlsx) == 'Работа функции завершена с ошибкой: '
