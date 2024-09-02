from collections import Counter

import pytest

from src.the_executive_module import filter_by_status, final_calculation, read_transactions_data

filename_list = ["operations4.json", "operations0.json", "operations1.json", "transactions_0.csv",
                 "transactions_excel_0.xlsx", "prosto.file", "transactions_1.csv", "transactions_excel_1.xlsx"]


@pytest.fixture
def expected_json_read_transactions_data():
    return [{'amount': '31957.58', 'currency_code': 'RUB', 'currency_name': 'руб.',
             'date': '2019-08-26T10:50:58.294041', 'description': 'Перевод организации',
             'from': 'Maestro 1596837868705199', 'id': 441945886, 'state': 'EXECUTED',
             'to': 'Счет 64686473678894779589'},
            {'amount': '8221.37', 'currency_code': 'USD', 'currency_name': 'USD',
             'date': '2019-07-03T18:35:29.512364', 'description': 'Перевод организации',
             'from': 'MasterCard 7158300734726758', 'id': 41428829, 'state': 'EXECUTED',
             'to': 'Счет 35383033474447895560'},
            {'amount': '9824.07', 'currency_code': 'USD', 'currency_name': 'USD',
             'date': '2018-06-30T02:08:58.425572', 'description': 'Перевод организации',
             'from': 'Счет 75106830613657916952', 'id': 939719570, 'state': 'EXECUTED',
             'to': 'Счет 11776614605963066702'},
            {'amount': '79114.93', 'currency_code': 'EUR', 'currency_name': 'EUR',
             'date': '2019-04-04T23:20:05.206878', 'description': 'Перевод со счета на счет',
             'from': 'Счет 19708645243227258542', 'id': 142264268, 'state': 'EXECUTED',
             'to': 'Счет 75651667383060284188'}]


@pytest.fixture
def expected_csv_read_transactions_data():
    return [{'amount': '16210', 'currency_code': 'PEN', 'currency_name': 'Sol', 'date': '2023-09-05T11:30:32Z',
             'description': 'Перевод организации', 'from': 'Счет 58803664561298323391', 'id': '650703',
             'state': 'EXECUTED', 'to': 'Счет 39745660563456619397'},
            {'amount': '29740', 'currency_code': 'COP', 'currency_name': 'Peso', 'date': '2020-12-06T23:00:58Z',
             'description': 'Перевод с карты на карту', 'from': 'Discover 3172601889670065', 'id': '3598919',
             'state': 'EXECUTED', 'to': 'Discover 0720428384694643'},
            {'amount': '30368', 'currency_code': 'TZS', 'currency_name': 'Shilling', 'date': '2023-07-22T05:02:01Z',
             'description': 'Перевод с карты на карту', 'from': 'Visa 1959232722494097', 'id': '593027',
             'state': 'CANCELED', 'to': 'Visa 6804119550473710'},
            {'amount': '29482', 'currency_code': 'IDR', 'currency_name': 'Rupiah', 'date': '2020-08-02T09:35:18Z',
             'description': 'Перевод с карты на карту', 'from': 'Discover 0325955596714937', 'id': '366176',
             'state': 'EXECUTED', 'to': 'Visa 3820488829287420'},
            {'amount': '23789', 'currency_code': 'UYU', 'currency_name': 'Peso', 'date': '2021-02-01T11:54:58Z',
             'description': 'Открытие вклада', 'from': '', 'id': '5380041',
             'state': 'CANCELED', 'to': 'Счет 23294994494356835683'}]


@pytest.fixture
def expected_xlsx_read_transactions_data():
    return [{'amount': 16210.0, 'currency_code': 'PEN', 'currency_name': 'Sol', 'date': '2023-09-05T11:30:32Z',
             'description': 'Перевод организации', 'from': 'Счет 58803664561298323391', 'id': 650703.0,
             'state': 'EXECUTED', 'to': 'Счет 39745660563456619397'},
            {'amount': 30368.0, 'currency_code': 'TZS', 'currency_name': 'Shilling', 'date': '2023-07-22T05:02:01Z',
             'description': 'Перевод с карты на карту', 'from': 'Visa 1959232722494097', 'id': 593027.0,
             'state': 'CANCELED', 'to': 'Visa 6804119550473710'},
            {'amount': 29553.0, 'currency_code': 'CNY', 'currency_name': 'Yuan Renminbi',
             'date': '2021-11-27T00:46:09Z', 'description': 'Перевод организации',
             'from': 'American Express 6477627838877562', 'id': 632926.0, 'state': 'PENDING',
             'to': 'Счет 88381741644903346269'},
            {'amount': 23789.0, 'currency_code': 'UYU', 'currency_name': 'Peso', 'date': '2021-02-01T11:54:58Z',
             'description': 'Открытие вклада', 'from': '', 'id': 5380041.0, 'state': 'CANCELED',
             'to': 'Счет 23294994494356835683'},
            {'amount': 25261.0, 'currency_code': 'UAH', 'currency_name': 'Hryvnia', 'date': '2023-06-23T19:46:34Z',
             'description': 'Открытие вклада', 'from': '', 'id': 5429839.0, 'state': 'EXECUTED',
             'to': 'Счет 76768135089446747029'},
            {'amount': 18891.0, 'currency_code': 'CNY', 'currency_name': 'Yuan Renminbi',
             'date': '2023-08-03T16:00:37Z', 'description': 'Открытие вклада', 'from': '', 'id': 1068715.0,
             'state': 'PENDING', 'to': 'Счет 04362233061130879079'},
            {'amount': 16101.0, 'currency_code': 'COP', 'currency_name': 'Peso', 'date': '2020-08-15T15:35:06Z',
             'description': 'Перевод организации', 'from': 'American Express 7606039262578692', 'id': 1408892.0,
             'state': 'EXECUTED', 'to': 'Счет 35266864227613549441'}]


@pytest.fixture
def filterd_csv_by_executed():
    return [{'amount': '16210', 'currency_code': 'PEN', 'currency_name': 'Sol', 'date': '2023-09-05T11:30:32Z',
             'description': 'Перевод организации', 'from': 'Счет 58803664561298323391', 'id': '650703',
             'state': 'EXECUTED', 'to': 'Счет 39745660563456619397'},
            {'amount': '29740', 'currency_code': 'COP', 'currency_name': 'Peso', 'date': '2020-12-06T23:00:58Z',
             'description': 'Перевод с карты на карту', 'from': 'Discover 3172601889670065', 'id': '3598919',
             'state': 'EXECUTED', 'to': 'Discover 0720428384694643'},
            {'amount': '29482', 'currency_code': 'IDR', 'currency_name': 'Rupiah', 'date': '2020-08-02T09:35:18Z',
             'description': 'Перевод с карты на карту', 'from': 'Discover 0325955596714937', 'id': '366176',
             'state': 'EXECUTED', 'to': 'Visa 3820488829287420'}]


@pytest.fixture
def expected_wrong_read_transactions_data():
    return "Выбранный файл отсутствует или не содержит необходимой информациии.\nРабота программы завершена."


@pytest.fixture
def expected_final_calculation():
    return [{'amount': '16210', 'currency_code': 'PEN', 'currency_name': 'Sol', 'date': '2023-09-05T11:30:32Z',
             'description': 'Перевод организации', 'from': 'Счет 58803664561298323391', 'id': '650703',
             'state': 'EXECUTED', 'to': 'Счет 39745660563456619397'}]


def test_read_transactions_data(expected_wrong_read_transactions_data, expected_csv_read_transactions_data,
                                expected_json_read_transactions_data, expected_xlsx_read_transactions_data):
    """Тест функции чтения и подготовки данных для обработки"""
    assert read_transactions_data(filename_list[0]) == expected_json_read_transactions_data
    assert read_transactions_data(filename_list[6]) == expected_csv_read_transactions_data
    assert read_transactions_data(filename_list[7]) == expected_xlsx_read_transactions_data
    with pytest.raises(SystemExit) as message:
        read_transactions_data(filename_list[1])
    assert str(message.value) == expected_wrong_read_transactions_data
    with pytest.raises(SystemExit) as message:
        read_transactions_data(filename_list[2])
    assert str(message.value) == expected_wrong_read_transactions_data
    with pytest.raises(SystemExit) as message:
        read_transactions_data(filename_list[3])
    assert str(message.value) == expected_wrong_read_transactions_data
    with pytest.raises(SystemExit) as message:
        read_transactions_data(filename_list[4])
    assert str(message.value) == expected_wrong_read_transactions_data
    with pytest.raises(SystemExit) as message:
        read_transactions_data(filename_list[5])
    assert str(message.value) == expected_wrong_read_transactions_data


def test_filter_by_status(expected_csv_read_transactions_data, filterd_csv_by_executed):
    """Тест функции фильтрации по статусу"""
    search_line = ["EXECUTED", "CANCELED", "PENDING"]
    loaded_data = expected_csv_read_transactions_data
    assert filter_by_status(loaded_data, search_line[0]) == filterd_csv_by_executed
    with pytest.raises(SystemExit) as message:
        filter_by_status(loaded_data, search_line[2])
    assert str(message.value) == f"Данных со статусом {search_line[2]} не обнаружено.\nРабота программы завершена."


def test_final_calculation(filterd_csv_by_executed, expected_final_calculation):
    """Тест функции окончательной сортировки и подсчёта типа транзакций"""
    choice = {"description": "Перевод организации", "currency_code": "PEN"}
    final_countdown, count_category = final_calculation(filterd_csv_by_executed, choice)
    assert count_category == Counter({"Перевод организации": 1})
    assert final_countdown == expected_final_calculation
    choice = {"description": "Перевод организации", "currency_code": "RUB"}
    with pytest.raises(SystemExit) as message:
        final_countdown, count_category = final_calculation(filterd_csv_by_executed, choice)
    assert str(message.value) == "Даные по выбранным критериям не обнаружены.\nРабота программы завершена."
