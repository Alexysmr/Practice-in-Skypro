def get_mask_card_number(numbers: list) -> str:
    """Функция получения номера банковской карты и вывода в заданном формате"""
    card_numbers = []
    for num in numbers:
        card_numbers.append(int(num))
    first_group = "".join(str(item) for item in card_numbers[0:4])
    second_group = "".join(str(item) for item in card_numbers[4:6])
    last_group = "".join(str(item) for item in card_numbers[12:])
    mask_number = f"{first_group} {second_group}** **** {last_group}"
    return mask_number


def get_mask_account(bank_account: list) -> str:
    """Функция получения банковского счёта и вывода в заданном формате"""
    account_numbers = []
    for num in bank_account:
        account_numbers.append(int(num))
    mask = "".join(str(item) for item in account_numbers[0:])
    mask_account = f"**{mask[2:]}"
    return mask_account
