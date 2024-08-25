def mask_account_card(name_numbers: str) -> any:
    """Функция получения названия и номера банковской карты и вывода в заданном формате"""
    card_numbers = []
    card_name = ""
    symbols = (
        "=",
        "+",
        "-",
        "(",
        ")",
        "[",
        "]",
        "@",
        "!",
        "'",
        ".",
        ",",
        "&",
        "?",
        "/",
        "<",
        ">",
        "*",
        ":",
        ";",
        "#",
        "№",
        '"',
        " ",
    )
    if name_numbers != "":
        for element in name_numbers:
            if element.isdigit():
                card_numbers.append(int(element))
            elif element in symbols:
                card_name += " "
            elif element.isalpha():
                card_name += element
    else:
        card_name = "Отсутствует название карты. "
    card_name_cut = card_name.strip()
    if card_name_cut == "":
        card_name_cut = "Отсутствует название карты. "
    if len(card_numbers) == 16:
        first_group = "".join(str(item) for item in card_numbers[0:4])
        second_group = "".join(str(item) for item in card_numbers[4:6])
        last_group = "".join(str(item) for item in card_numbers[-4:])
        mask_card = f"{first_group} {second_group}** **** {last_group}"
    else:
        mask_card = "Введён некорректный номер карты"
    return card_name_cut, mask_card


def mask_account(bank_user_account: str) -> str:
    """Функция получения банковского счёта и вывода в заданном формате"""
    account_numbers = []
    for element in bank_user_account:
        if element.isdigit():
            account_numbers.append(int(element))
    if len(account_numbers) == 20:
        mask = "".join(str(item) for item in account_numbers[0:])
        mask_account = f"Счёт **{mask[-4:]}"
        return mask_account
    else:
        return "Введены некорректные данные счёта"


def get_date(full_date_time: str) -> str:
    """Функция изменения формата времени в заданный"""
    separate_date = ""
    symbols = (",", ".", "/", "*", ":", " ")
    if len(full_date_time) != "" and full_date_time != "-":
        count = 0
        for element in full_date_time:
            if count != 10:
                if element in symbols:
                    element = "-"
                separate_date += element
                count += 1
    else:
        return "Ошибка ввода даты"
    intermediate = separate_date.split("-")
    if intermediate[2].isdigit() and intermediate[1].isdigit() and intermediate[0].isdigit():
        correct_date = intermediate[2] + "." + intermediate[1] + "." + intermediate[0]
    else:
        correct_date = "Ошибка ввода даты"
    return correct_date
