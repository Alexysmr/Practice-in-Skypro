def mask_account_card(name_numbers: str) -> tuple:
    """Функция получения названия и номера банковской карты и вывода в заданном формате"""
    card_numbers = []
    card_name = ""
    for num in name_numbers:
        if num.isdigit():
            card_numbers.append(int(num))
        elif num.isalpha() or num == " ":
            card_name += num
    card_name_cut = card_name.strip()
    first_group = "".join(str(item) for item in card_numbers[0:4])
    second_group = "".join(str(item) for item in card_numbers[4:6])
    last_group = "".join(str(item) for item in card_numbers[-4:])
    mask_card = f"{first_group} {second_group}** **** {last_group}"
    return card_name_cut, mask_card


def mask_account(bank_account: str) -> str:
    """Функция получения банковского счёта и вывода в заданном формате"""
    account_numbers = []
    for num in bank_account:
        if num.isdigit():
            account_numbers.append(int(num))
    mask = "".join(str(item) for item in account_numbers[0:])
    mask_account = f"Счёт **{mask[-4:]}"
    return mask_account


def get_date(full_date_time: str) -> str:
    """Функция изменения формата времени в заданный"""
    separate_date = ""
    n = 0
    for element in full_date_time:
        if n != 10:
            separate_date += element
            n += 1
    intermediate = separate_date.split("-")
    intermediate.reverse()
    correct_date = intermediate[0] + "." + intermediate[1] + "." + intermediate[2]
    return correct_date
