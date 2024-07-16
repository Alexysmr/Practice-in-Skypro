from src.masks import get_mask_card_number, get_mask_account


def test_get_mask_card_number():
    assert get_mask_card_number("1203145236525896") == "1203 14** **** 5896"
    assert get_mask_card_number("120314*52365-25896") == "1203 14** **** 5896"
    assert get_mask_card_number("") == "Введён некорректный номер карты"
    assert get_mask_card_number("120314*52365-2589") == "Введён некорректный номер карты" #"Номер короче на 1 цифру"


def test_get_mask_account():
    assert get_mask_account("25633652125445875612") == "**5612"
    assert get_mask_account((" 12345236654125860236")) == "**0236"
    assert get_mask_account(("12345236654125860236 ")) == "**0236"
    assert get_mask_account(("25 633-652125445+8756=12")) == "**5612"
    assert get_mask_account(()) == "Введён некорректный номер счёта"
    assert get_mask_account(("abcd56789043bfgd")) == "Введён некорректный номер счёта"