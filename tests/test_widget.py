from src.widget import mask_account_card, get_date
import pytest


@pytest.mark.parametrize(
    "name_numbers, expected",
    [
        ("Visa-Classic №254652398565478", ("Visa Classic", "Введён некорректный номер карты")),
        ("Visa-Classic -2546*5239*8565*4789", ("Visa Classic", "2546 52** **** 4789")),
        ("Maestro - 5236-5478/9845 6547", ("Maestro", "5236 54** **** 6547")),
        ("", ("Отсутствует название карты.", "Введён некорректный номер карты")),
        ("Visa-Classic -2546", ("Visa Classic", "Введён некорректный номер карты")),
        ("Visa/Gold", ("Visa Gold", "Введён некорректный номер карты")),
    ],
)
def test_mask_account_card(name_numbers, expected):
    assert mask_account_card(name_numbers) == expected


@pytest.mark.parametrize(
    "full_date_time, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2024:03:11T02:26:18.671407", "11.03.2024"),
        ("2024/03/11T02:26:18.671407", "11.03.2024"),
        ("", "Ошибка ввода даты"),
        ("T02:26:18.671407-2024/03/11", "Ошибка ввода даты"),
    ],
)
def test_get_date(full_date_time, expected):
    assert get_date(full_date_time) == expected
