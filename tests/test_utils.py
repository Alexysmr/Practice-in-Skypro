from unittest.mock import Mock
from unittest.mock import patch
from src.utils import currency_exchange, input_transactions


def test_input_transactions():
    """Тест функции чтения JSON-файла в модуле utils"""
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


# @patch()
@patch('src.utils.requests.request')
def test_currency_exchange(mock_request):
    """Тест функции конвертации валюты"""
    from src.utils import input_transactions
    data0 = input_transactions("operations2.json")  # файл не существует
    data1 = input_transactions("operations4.json")  # operations4.json содержит часть operations.json - 4 транзакции
    mock_data = Mock(return_value=[""])
    input_transactions = mock_data
    data2 = input_transactions()
    mock_data = Mock(return_value=[1, 4, 5])
    input_transactions = mock_data
    data3 = input_transactions()
    mock_data = Mock(return_value=["Просто текст"])
    input_transactions = mock_data
    data4 = input_transactions()
    mock_request.return_value.status_code = 200
    mock_request.return_value.json.return_value = {"result": 91.32654187}
    assert currency_exchange(data0) == ['Отсутствуют данные транзакций']
    assert currency_exchange(data1) == [31957.58, 750829.29, 897198.34, 7225292.97]
    assert currency_exchange(data2) == ['Отсутствуют данные транзакций']
    assert currency_exchange(data3) == ['Отсутствуют данные транзакций']
    assert currency_exchange(data4) == ['Отсутствуют данные транзакций']
    mock_data.assert_called()
