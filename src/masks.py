def get_mask_card_number(numbers: any) -> str:
    """Функция получения номера банковской карты и вывода в заданном формате"""
    card_numbers = []
    for num in numbers:
        if num.isdigit():
            card_numbers.append(int(num))
    if len(card_numbers) == 16:
        first_group = "".join(str(item) for item in card_numbers[0:4])
        second_group = "".join(str(item) for item in card_numbers[4:6])
        last_group = "".join(str(item) for item in card_numbers[-4:])
        mask_number = f"{first_group} {second_group}** **** {last_group}"
        return mask_number
    else:
        return "Введён некорректный номер карты"


def get_mask_account(bank_account: str) -> str:
    """Функция получения банковского счёта и вывода в заданном формате"""
    account_numbers = []
    for num in bank_account:
        if num.isdigit():
            account_numbers.append(int(num))
    if len(account_numbers) == 20:
        mask = "".join(str(item) for item in account_numbers[0:])
        mask_account = f"**{mask[-4:]}"
        return mask_account
    else:
        return "Введён некорректный номер счёта"
