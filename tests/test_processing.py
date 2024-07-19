import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def clients_test_one():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019,07*03T18:35:29.512364"},
        {"id": 939719571, "state": "CANCELED", "date": "2018:06/30T02:08:58.425572"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018/06/30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018:09/12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018:10.14T08:21:33.419441"},
        {},
    ]


@pytest.fixture
def expected_one():
    return [
        {"date": "2019,07*03T18:35:29.512364", "id": 41428829, "state": "EXECUTED"},
        {"date": "2018/06/30T02:08:58.425572", "id": 939719570, "state": "EXECUTED"},
    ]


@pytest.fixture
def expected_canceled():
    return [
        {"id": 939719571, "state": "CANCELED", "date": "2018:06/30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018:09/12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018:10.14T08:21:33.419441"},
    ]


@pytest.fixture
def expected_date_sort():
    return [
        {"date": "Ошибка введённых данных"},
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719571, "state": "CANCELED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


@pytest.fixture
def expected_reverse_date_sort():
    return [
        {"id": 939719571, "state": "CANCELED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"date": "Ошибка-введённых данных"},
    ]


def test_filter_by_state(
    clients_test_one, expected_one, expected_canceled, expected_date_sort, expected_reverse_date_sort
):
    assert filter_by_state(clients_test_one) == expected_one
    assert filter_by_state(clients_test_one, state="CANCELED") == expected_canceled
    assert sort_by_date(clients_test_one) == expected_date_sort
    assert sort_by_date(clients_test_one, sort_reverse=False) == expected_reverse_date_sort
